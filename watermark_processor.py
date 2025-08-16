"""
وحدة معالجة العلامة المائية للصور والفيديوهات - الإصدار المحسن
تدعم إضافة علامة مائية نصية أو صورة مع إعدادات مخصصة

التحسينات الرئيسية:
1. معالجة الوسائط مرة واحدة وإعادة استخدامها لكل الأهداف
2. تحسين ضغط الفيديو مع الحفاظ على الجودة
3. إرسال الفيديو بصيغة MP4
4. ذاكرة مؤقتة ذكية لتحسين الأداء

المتطلبات:
- FFmpeg لتحسين الفيديو
- OpenCV, Pillow, NumPy للمعالجة
"""
import os
import io
import logging
from PIL import Image, ImageDraw, ImageFont, ImageColor
import cv2
import numpy as np
from typing import Optional, Tuple, Union, Dict, Any
import tempfile
import subprocess
import json

logger = logging.getLogger(__name__)

class WatermarkProcessor:
    """معالج العلامة المائية للصور والفيديوهات - محسن"""
    
    def __init__(self):
        """تهيئة معالج العلامة المائية"""
        self.supported_image_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        self.supported_video_formats = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
        
        # Cache للملفات المعالجة مسبقاً
        self.processed_media_cache = {}
        
        # التحقق من توفر FFmpeg
        self.ffmpeg_available = self._check_ffmpeg_availability()
        
        if self.ffmpeg_available:
            logger.info("✅ FFmpeg متوفر - سيتم استخدامه لتحسين الفيديو")
        else:
            logger.warning("⚠️ FFmpeg غير متوفر - سيتم استخدام OpenCV كبديل")
    
    def _check_ffmpeg_availability(self) -> bool:
        """التحقق من توفر FFmpeg في النظام"""
        try:
            # التحقق من توفر ffmpeg
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            if result.returncode == 0:
                # التحقق من توفر ffprobe
                result_probe = subprocess.run(['ffprobe', '-version'], capture_output=True, text=True)
                return result_probe.returncode == 0
            return False
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def calculate_position(self, base_size: Tuple[int, int], watermark_size: Tuple[int, int], position: str, offset_x: int = 0, offset_y: int = 0) -> Tuple[int, int]:
        """حساب موقع العلامة المائية على الصورة/الفيديو مع الإزاحة اليدوية"""
        base_width, base_height = base_size
        watermark_width, watermark_height = watermark_size
        
        # تحديد الهامش (5% من حجم الصورة)
        margin = min(base_width, base_height) // 20
        
        position_map = {
            'top_left': (margin, margin),
            'top_right': (base_width - watermark_width - margin, margin),
            'top': ((base_width - watermark_width) // 2, margin),
            'bottom_left': (margin, base_height - watermark_height - margin),
            'bottom_right': (base_width - watermark_width - margin, base_height - watermark_height - margin),
            'bottom': ((base_width - watermark_width) // 2, base_height - watermark_height - margin),
            'center': ((base_width - watermark_width) // 2, (base_height - watermark_height) // 2)
        }
        
        base_position = position_map.get(position, position_map['bottom_right'])
        
        # إضافة الإزاحة اليدوية مع التأكد من البقاء داخل حدود الصورة
        final_x = max(0, min(base_position[0] + offset_x, base_width - watermark_width))
        final_y = max(0, min(base_position[1] + offset_y, base_height - watermark_height))
        
        logger.info(f"📍 الموقع الأساسي: {base_position}, الإزاحة: ({offset_x}, {offset_y}), الموقع النهائي: ({final_x}, {final_y})")
        
        return (final_x, final_y)
    
    def create_text_watermark(self, text: str, font_size: int, color: str, opacity: int, 
                            image_size: Tuple[int, int]) -> Image.Image:
        """إنشاء علامة مائية نصية"""
        try:
            # إنشاء صورة شفافة للنص
            img_width, img_height = image_size
            
            # حساب حجم الخط بناءً على حجم الصورة
            calculated_font_size = max(font_size, img_width // 25)  # زيادة حجم الخط
            
            # محاولة استخدام خط عربي إذا أمكن
            font = None
            try:
                # البحث عن خط عربي في النظام
                font_paths = [
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "/System/Library/Fonts/Arial.ttf",
                    "arial.ttf"
                ]
                
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        font = ImageFont.truetype(font_path, calculated_font_size)
                        break
            except Exception:
                pass
            
            if font is None:
                font = ImageFont.load_default()
            
            # حساب حجم النص
            dummy_img = Image.new('RGBA', (1, 1))
            dummy_draw = ImageDraw.Draw(dummy_img)
            text_bbox = dummy_draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # إنشاء صورة للنص مع خلفية شفافة
            text_img = Image.new('RGBA', (int(text_width + 20), int(text_height + 10)), (0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_img)
            
            # تحويل اللون إلى RGBA مع الشفافية
            try:
                if color.startswith('#'):
                    rgb_color = ImageColor.getcolor(color, "RGB")
                    rgba_color = rgb_color + (int(255 * opacity / 100),)
                else:
                    rgba_color = (255, 255, 255, int(255 * opacity / 100))
            except Exception:
                rgba_color = (255, 255, 255, int(255 * opacity / 100))
            
            # رسم النص
            text_draw.text((10, 5), text, font=font, fill=rgba_color)
            
            return text_img
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء العلامة المائية النصية: {e}")
            return None
    
    def calculate_smart_watermark_size(self, base_image_size: Tuple[int, int], watermark_size: Tuple[int, int], 
                                     size_percentage: int, position: str = 'bottom_right') -> Tuple[int, int]:
        """حساب حجم العلامة المائية الذكي حسب أبعاد الصورة والموضع"""
        base_width, base_height = base_image_size
        watermark_width, watermark_height = watermark_size
        
        # الحفاظ على النسبة الأصلية للعلامة المائية
        aspect_ratio = watermark_width / watermark_height
        
        # حساب الحجم بناءً على النسبة المئوية المطلوبة
        scale_factor = size_percentage / 100.0
        
        if size_percentage == 100:
            # للحجم 100%، استخدم كامل أبعاد الصورة الأساسية مع هامش صغير فقط
            new_width = int(base_width * 0.98)  # 98% لترك هامش صغير جداً
            new_height = int(base_height * 0.98)  # 98% لترك هامش صغير جداً
            
            # الحفاظ على النسبة إذا أمكن، وإلا استخدم الحجم الكامل
            calculated_height_from_width = int(new_width / aspect_ratio)
            calculated_width_from_height = int(new_height * aspect_ratio)
            
            # اختر الحجم الذي يحقق أقصى استفادة من المساحة
            if calculated_height_from_width <= new_height:
                # يمكن استخدام العرض الكامل
                new_height = calculated_height_from_width
            else:
                # استخدم الارتفاع الكامل وحساب العرض
                new_width = calculated_width_from_height
                
            logger.info(f"🎯 حجم 100%: أبعاد الصورة {base_image_size} → أبعاد العلامة {(new_width, new_height)}")
        else:
            # للنسب المئوية الأخرى، حساب عادي
            if position in ['top', 'bottom', 'center']:
                # للمواضع الأفقية، استخدم النسبة المئوية كاملة من العرض
                new_width = int(base_width * scale_factor)
            else:
                # للمواضع الركنية، استخدم نسبة معدلة
                new_width = int(base_width * scale_factor * 0.8)
            
            new_height = int(new_width / aspect_ratio)
            
            # تطبيق حدود معقولة للأحجام الأخرى
            max_allowed_width = base_width * 0.9  
            max_allowed_height = base_height * 0.7
            
            if new_width > max_allowed_width:
                new_width = int(max_allowed_width)
                new_height = int(new_width / aspect_ratio)
                
            if new_height > max_allowed_height:
                new_height = int(max_allowed_height)
                new_width = int(new_height * aspect_ratio)
        
        # تأكد من الحد الأدنى للحجم
        min_size = 20
        new_width = max(min_size, new_width)
        new_height = max(min_size, new_height)
        
        # تأكد من عدم تجاوز أبعاد الصورة الأساسية
        new_width = min(new_width, base_width - 10)  # هامش 10 بكسل
        new_height = min(new_height, base_height - 10)  # هامش 10 بكسل
        
        logger.info(f"📏 حساب حجم العلامة المائية: {size_percentage}% → {(new_width, new_height)} من أصل {base_image_size}")
        
        return (new_width, new_height)

    def load_image_watermark(self, image_path: str, size_percentage: int, opacity: int,
                           base_image_size: Tuple[int, int], position: str = 'bottom_right') -> Optional[Image.Image]:
        """تحميل وتحضير علامة مائية من صورة بحجم ذكي"""
        try:
            if not os.path.exists(image_path):
                logger.error(f"ملف الصورة غير موجود: {image_path}")
                return None
            
            # تحميل الصورة
            watermark_img = Image.open(image_path)
            
            # تحويل إلى RGBA للدعم الشفافية
            if watermark_img.mode != 'RGBA':
                watermark_img = watermark_img.convert('RGBA')
            
            # حساب الحجم الذكي
            original_size = watermark_img.size
            smart_size = self.calculate_smart_watermark_size(base_image_size, original_size, size_percentage, position)
            
            logger.info(f"📏 تحجيم العلامة المائية الذكي: {original_size} → {smart_size}")
            logger.info(f"🎯 إعدادات: نسبة {size_percentage}%, موضع {position}, أبعاد الصورة {base_image_size}")
            
            # تغيير حجم الصورة
            watermark_img = watermark_img.resize(smart_size, Image.Resampling.LANCZOS)
            
            # تطبيق الشفافية
            if opacity < 100:
                alpha = watermark_img.split()[-1]
                alpha = alpha.point(lambda p: int(p * opacity / 100))
                watermark_img.putalpha(alpha)
            
            return watermark_img
            
        except Exception as e:
            logger.error(f"خطأ في تحميل صورة العلامة المائية: {e}")
            return None
    
    def apply_watermark_to_image(self, image_bytes: bytes, watermark_settings: dict) -> Optional[bytes]:
        """تطبيق العلامة المائية على صورة"""
        try:
            # تحميل الصورة
            image = Image.open(io.BytesIO(image_bytes))
            
            # تحويل إلى RGB إذا لزم الأمر
            if image.mode not in ['RGB', 'RGBA']:
                image = image.convert('RGB')
            
            # إنشاء العلامة المائية
            watermark = None
            
            if watermark_settings['watermark_type'] == 'text' and watermark_settings['watermark_text']:
                color = watermark_settings['text_color'] if not watermark_settings['use_original_color'] else '#FFFFFF'
                watermark = self.create_text_watermark(
                    watermark_settings['watermark_text'],
                    watermark_settings['font_size'],
                    color,
                    watermark_settings['opacity'],
                    image.size
                )
            
            elif watermark_settings['watermark_type'] == 'image' and watermark_settings['watermark_image_path']:
                watermark = self.load_image_watermark(
                    watermark_settings['watermark_image_path'],
                    watermark_settings['size_percentage'],
                    watermark_settings['opacity'],
                    image.size,
                    watermark_settings.get('position', 'bottom_right')
                )
            
            if watermark is None:
                logger.warning("فشل في إنشاء العلامة المائية")
                return image_bytes
            
            # حساب موقع العلامة المائية مع الإزاحة اليدوية
            offset_x = watermark_settings.get('offset_x', 0)
            offset_y = watermark_settings.get('offset_y', 0)
            position = self.calculate_position(image.size, watermark.size, watermark_settings['position'], offset_x, offset_y)
            
            # تطبيق العلامة المائية
            if image.mode == 'RGBA':
                image.paste(watermark, position, watermark)
            else:
                # تحويل إلى RGBA لتطبيق العلامة المائية
                image = image.convert('RGBA')
                image.paste(watermark, position, watermark)
                # تحويل مرة أخرى إلى RGB
                image = image.convert('RGB')
            
            # حفظ الصورة بتنسيقها الأصلي أو PNG للحفاظ على الجودة
            output = io.BytesIO()
            
            # تحديد تنسيق الحفظ بناءً على الصورة الأصلية
            try:
                original_image = Image.open(io.BytesIO(image_bytes))
                original_format = original_image.format or 'PNG'
                
                # استخدام PNG للصور التي تحتوي على شفافية
                if image.mode == 'RGBA' or original_format == 'PNG':
                    image.save(output, format='PNG', optimize=True)
                elif original_format in ['JPEG', 'JPG']:
                    # تحويل RGBA إلى RGB للـ JPEG
                    if image.mode == 'RGBA':
                        background = Image.new('RGB', image.size, (255, 255, 255))
                        background.paste(image, mask=image.split()[-1])
                        image = background
                    image.save(output, format='JPEG', quality=95, optimize=True)
                else:
                    # استخدام PNG كتنسيق افتراضي
                    image.save(output, format='PNG', optimize=True)
            except Exception:
                # في حالة فشل تحديد التنسيق، استخدم PNG
                image.save(output, format='PNG', optimize=True)
                
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"خطأ في تطبيق العلامة المائية على الصورة: {e}")
            return image_bytes
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """الحصول على معلومات الفيديو باستخدام ffprobe أو OpenCV كبديل"""
        try:
            # محاولة استخدام ffprobe أولاً
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)
            
            # استخراج المعلومات المهمة
            video_stream = next((s for s in info['streams'] if s['codec_type'] == 'video'), None)
            format_info = info['format']
            
            if video_stream:
                return {
                    'width': int(video_stream.get('width', 0)),
                    'height': int(video_stream.get('height', 0)),
                    'fps': eval(video_stream.get('r_frame_rate', '30/1')),
                    'duration': float(format_info.get('duration', 0)),
                    'bitrate': int(format_info.get('bit_rate', 0)),
                    'size_mb': float(format_info.get('size', 0)) / (1024 * 1024),
                    'codec': video_stream.get('codec_name', 'unknown')
                }
            
            return {}
            
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"فشل في استخدام ffprobe: {e}")
            
            # استخدام OpenCV كبديل
            try:
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    logger.error(f"فشل في فتح الفيديو باستخدام OpenCV: {video_path}")
                    return {}
                
                # الحصول على خصائص الفيديو
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                # حساب المدة التقريبية
                duration = total_frames / fps if fps > 0 else 0
                
                # الحصول على حجم الملف
                file_size = os.path.getsize(video_path)
                size_mb = file_size / (1024 * 1024)
                
                cap.release()
                
                logger.info(f"✅ تم الحصول على معلومات الفيديو باستخدام OpenCV: {width}x{height}, {fps:.2f} FPS, {size_mb:.2f} MB")
                
                return {
                    'width': width,
                    'height': height,
                    'fps': fps,
                    'duration': duration,
                    'bitrate': int((file_size * 8) / duration) if duration > 0 else 0,
                    'size_mb': size_mb,
                    'codec': 'unknown'
                }
                
            except Exception as opencv_error:
                logger.error(f"فشل في الحصول على معلومات الفيديو باستخدام OpenCV: {opencv_error}")
                return {}
                
        except Exception as e:
            logger.error(f"خطأ عام في الحصول على معلومات الفيديو: {e}")
            return {}
    
    def optimize_video_compression(self, input_path: str, output_path: str, target_size_mb: float = None) -> bool:
        """تحسين ضغط الفيديو مع الحفاظ على الجودة"""
        try:
            # الحصول على معلومات الفيديو الأصلي
            video_info = self.get_video_info(input_path)
            if not video_info:
                logger.warning("فشل في الحصول على معلومات الفيديو، استخدام إعدادات افتراضية")
                return False
            
            original_size = video_info.get('size_mb', 0)
            original_bitrate = video_info.get('bitrate', 0)
            
            logger.info(f"📹 معلومات الفيديو الأصلي: {video_info['width']}x{video_info['height']}, "
                       f"{video_info['fps']:.2f} FPS, {original_size:.2f} MB")
            
            # حساب معدل البت الأمثل
            if target_size_mb and original_size > target_size_mb:
                # حساب معدل البت المطلوب للوصول للحجم المطلوب
                target_bitrate = int((target_size_mb * 8 * 1024 * 1024) / video_info['duration'])
                target_bitrate = max(target_bitrate, 500000)  # حد أدنى 500 kbps
            else:
                # استخدام معدل البت الأصلي مع تحسين بسيط
                target_bitrate = int(original_bitrate * 0.9)  # تقليل 10% للحفاظ على الجودة
            
            # استخدام FFmpeg إذا كان متوفراً
            if self.ffmpeg_available:
                try:
                    # إعدادات FFmpeg محسنة
                    cmd = [
                        'ffmpeg', '-i', input_path,
                        '-c:v', 'libx264',  # كودك H.264
                        '-preset', 'medium',  # توازن بين السرعة والجودة
                        '-crf', '23',  # جودة ثابتة (18-28 جيد، 23 مثالي)
                        '-maxrate', f'{target_bitrate}',
                        '-bufsize', f'{target_bitrate * 2}',
                        '-c:a', 'aac',  # كودك الصوت
                        '-b:a', '128k',  # معدل بت الصوت
                        '-movflags', '+faststart',  # تحسين التشغيل
                        '-y',  # استبدال الملف الموجود
                        output_path
                    ]
                    
                    logger.info(f"🎬 بدء تحسين الفيديو باستخدام FFmpeg: معدل البت المستهدف {target_bitrate/1000:.0f} kbps")
                    
                    # تنفيذ الضغط
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        # التحقق من النتيجة
                        final_info = self.get_video_info(output_path)
                        if final_info:
                            final_size = final_info.get('size_mb', 0)
                            compression_ratio = (original_size - final_size) / original_size * 100
                            
                            logger.info(f"✅ تم تحسين الفيديو بنجاح باستخدام FFmpeg: "
                                       f"{original_size:.2f} MB → {final_size:.2f} MB "
                                       f"(توفير {compression_ratio:.1f}%)")
                            return True
                        else:
                            logger.warning("تم إنشاء الفيديو ولكن فشل في التحقق من النتيجة")
                            return True
                    else:
                        logger.warning(f"فشل في استخدام FFmpeg: {result.stderr}")
                        # الانتقال إلى الطريقة البديلة
                        raise Exception("FFmpeg فشل في التنفيذ")
                        
                except Exception as ffmpeg_error:
                    logger.warning(f"فشل في استخدام FFmpeg: {ffmpeg_error}")
                    # الانتقال إلى الطريقة البديلة
            
            # استخدام OpenCV كبديل لضغط بسيط
            try:
                logger.info("🔄 استخدام OpenCV كبديل لضغط الفيديو...")
                
                # محاولة استخدام OpenCV لمعالجة الفيديو
                if self.optimize_video_with_opencv(input_path, output_path, target_size_mb):
                    logger.info("✅ تم معالجة الفيديو بنجاح باستخدام OpenCV")
                    return True
                else:
                    # إذا فشل OpenCV، استخدم النسخ البسيط
                    logger.warning("فشل في معالجة الفيديو باستخدام OpenCV، استخدام النسخ البسيط")
                    import shutil
                    shutil.copy2(input_path, output_path)
                    
                    logger.info(f"✅ تم نسخ الفيديو إلى {output_path} (بدون ضغط إضافي)")
                    if not self.ffmpeg_available:
                        logger.info("💡 للحصول على ضغط أفضل، قم بتثبيت FFmpeg")
                    else:
                        logger.info("💡 FFmpeg متوفر ولكن فشل في التنفيذ، تم استخدام النسخ البسيط")
                    
                    return True
                
            except Exception as opencv_error:
                logger.error(f"فشل في استخدام OpenCV كبديل: {opencv_error}")
                return False
                
        except Exception as e:
            logger.error(f"خطأ في تحسين ضغط الفيديو: {e}")
            return False
    
    def optimize_video_with_opencv(self, input_path: str, output_path: str, target_size_mb: float = None) -> bool:
        """تحسين الفيديو باستخدام OpenCV كبديل لـ FFmpeg"""
        try:
            # فتح الفيديو
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                logger.error(f"فشل في فتح الفيديو: {input_path}")
                return False
            
            # الحصول على خصائص الفيديو
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # حساب معدل البت المستهدف
            original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
            duration = total_frames / fps if fps > 0 else 0
            
            # تحديد معاملات التحسين بناءً على الحجم المستهدف
            scale_factor = 1.0
            fps_factor = 1.0
            
            if target_size_mb and original_size > target_size_mb:
                # حساب معامل التصغير المطلوب
                target_ratio = target_size_mb / original_size
                
                if target_ratio < 0.5:
                    # تقليل كبير - تقليل الدقة ومعدل الإطارات
                    scale_factor = 0.7
                    fps_factor = 0.75
                elif target_ratio < 0.8:
                    # تقليل متوسط - تقليل الدقة قليلاً
                    scale_factor = 0.85
                    fps_factor = 0.9
                else:
                    # تقليل بسيط - تقليل الدقة قليلاً جداً
                    scale_factor = 0.95
                    fps_factor = 0.95
                
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                new_fps = int(fps * fps_factor)
                
                logger.info(f"🔄 تحسين الفيديو: الدقة {width}x{height} → {new_width}x{new_height}, "
                           f"معدل الإطارات {fps} → {new_fps}")
            else:
                new_width, new_height = width, height
                new_fps = fps
            
            # إعداد كاتب الفيديو
            fourcc = cv2.VideoWriter.fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, new_fps, (new_width, new_height))
            
            if not out.isOpened():
                logger.error("فشل في إنشاء كاتب الفيديو")
                cap.release()
                return False
            
            logger.info(f"🎬 بدء معالجة الفيديو باستخدام OpenCV: {total_frames} إطار")
            
            frame_count = 0
            skip_frames = 1
            
            # حساب عدد الإطارات التي يجب تخطيها للحصول على معدل الإطارات المطلوب
            if new_fps < fps:
                skip_frames = int(fps / new_fps)
                logger.info(f"⏭️ تخطي {skip_frames - 1} إطار من كل {skip_frames} إطار")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # تخطي الإطارات إذا لزم الأمر
                if frame_count % skip_frames != 0:
                    frame_count += 1
                    continue
                
                # تغيير حجم الإطار إذا لزم الأمر
                if new_width != width or new_height != height:
                    frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
                
                # كتابة الإطار
                out.write(frame)
                
                frame_count += 1
                if frame_count % 100 == 0:
                    progress = (frame_count / total_frames) * 100
                    logger.info(f"معالجة الفيديو: {progress:.1f}% ({frame_count}/{total_frames})")
            
            # إغلاق الموارد
            cap.release()
            out.release()
            
            # التحقق من النتيجة
            if os.path.exists(output_path):
                final_size = os.path.getsize(output_path) / (1024 * 1024)
                compression_ratio = (original_size - final_size) / original_size * 100
                
                logger.info(f"✅ تم معالجة الفيديو بنجاح باستخدام OpenCV: "
                           f"{original_size:.2f} MB → {final_size:.2f} MB "
                           f"(توفير {compression_ratio:.1f}%)")
                return True
            else:
                logger.error("فشل في إنشاء ملف الفيديو")
                return False
                
        except Exception as e:
            logger.error(f"خطأ في معالجة الفيديو باستخدام OpenCV: {e}")
            return False
    
    def apply_watermark_to_video(self, video_path: str, watermark_settings: dict) -> Optional[str]:
        """تطبيق العلامة المائية على فيديو مع الحفاظ على الصوت والدقة"""
        try:
            # فتح الفيديو
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                logger.error(f"فشل في فتح الفيديو: {video_path}")
                return None
            
            # الحصول على خصائص الفيديو
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if fps <= 0 or total_frames <= 0:
                logger.error(f"خصائص الفيديو غير صحيحة: FPS={fps}, Frames={total_frames}")
                cap.release()
                return None
            
            logger.info(f"📹 معلومات الفيديو: {width}x{height}, {fps} FPS, {total_frames} إطار")
            
            # إنشاء ملف مؤقت للفيديو الجديد
            temp_dir = tempfile.gettempdir()
            temp_output = os.path.join(temp_dir, f"temp_watermarked_{os.path.basename(video_path)}")
            final_output = os.path.join(temp_dir, f"watermarked_{os.path.basename(video_path)}")
            
            # تغيير امتداد الملف إلى MP4
            if not final_output.endswith('.mp4'):
                final_output = os.path.splitext(final_output)[0] + '.mp4'
            
            # إعداد كاتب الفيديو - استخدام كودك H.264 للحفاظ على الجودة
            fourcc = cv2.VideoWriter.fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_output, fourcc, fps, (width, height))
            
            if not out.isOpened():
                logger.error("فشل في إنشاء كاتب الفيديو")
                cap.release()
                return None
            
            # تحضير العلامة المائية
            watermark_img = None
            
            if watermark_settings['watermark_type'] == 'text' and watermark_settings['watermark_text']:
                color = watermark_settings['text_color'] if not watermark_settings['use_original_color'] else '#FFFFFF'
                watermark_pil = self.create_text_watermark(
                    watermark_settings['watermark_text'],
                    watermark_settings['font_size'],
                    color,
                    watermark_settings['opacity'],
                    (width, height)
                )
                
                if watermark_pil:
                    # تحويل PIL إلى OpenCV
                    watermark_cv = cv2.cvtColor(np.array(watermark_pil), cv2.COLOR_RGBA2BGRA)
                    watermark_img = watermark_cv
                    
            elif watermark_settings['watermark_type'] == 'image' and watermark_settings['watermark_image_path']:
                watermark_pil = self.load_image_watermark(
                    watermark_settings['watermark_image_path'],
                    watermark_settings['size_percentage'],
                    watermark_settings['opacity'],
                    (width, height),
                    watermark_settings.get('position', 'bottom_right')
                )
                
                if watermark_pil:
                    # تحويل PIL إلى OpenCV
                    watermark_cv = cv2.cvtColor(np.array(watermark_pil), cv2.COLOR_RGBA2BGRA)
                    watermark_img = watermark_cv
            
            # حساب موقع العلامة المائية
            watermark_position = None
            if watermark_img is not None:
                watermark_height, watermark_width = watermark_img.shape[:2]
                offset_x = watermark_settings.get('offset_x', 0)
                offset_y = watermark_settings.get('offset_y', 0)
                watermark_position = self.calculate_position(
                    (width, height), 
                    (watermark_width, watermark_height), 
                    watermark_settings['position'], 
                    offset_x, 
                    offset_y
                )
            
            logger.info(f"🎬 بدء معالجة الفيديو: {total_frames} إطار")
            
            # معالجة كل إطار
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # تطبيق العلامة المائية إذا كانت موجودة
                if watermark_img is not None and watermark_position is not None:
                    try:
                        # إنشاء نسخة من الإطار
                        frame_with_watermark = frame.copy()
                        
                        # تطبيق العلامة المائية
                        x, y = watermark_position
                        
                        # التأكد من أن العلامة المائية تتناسب مع حدود الإطار
                        if x + watermark_width <= width and y + watermark_height <= height:
                            # تطبيق العلامة المائية مع الشفافية
                            if watermark_img.shape[2] == 4:  # RGBA
                                alpha = watermark_img[:, :, 3] / 255.0
                                alpha = np.expand_dims(alpha, axis=2)
                                
                                # دمج العلامة المائية مع الإطار
                                for c in range(3):  # BGR
                                    frame_with_watermark[y:y+watermark_height, x:x+watermark_width, c] = \
                                        frame_with_watermark[y:y+watermark_height, x:x+watermark_width, c] * (1 - alpha[:, :, 0]) + \
                                        watermark_img[:, :, c] * alpha[:, :, 0]
                            
                            frame = frame_with_watermark
                    except Exception as e:
                        logger.warning(f"فشل في تطبيق العلامة المائية على الإطار {frame_count}: {e}")
                
                # كتابة الإطار
                out.write(frame)
                
                frame_count += 1
                if frame_count % 100 == 0:
                    progress = (frame_count / total_frames) * 100
                    logger.info(f"معالجة الفيديو: {progress:.1f}% ({frame_count}/{total_frames})")
            
            # إغلاق الموارد
            cap.release()
            out.release()
            
            logger.info(f"✅ تم معالجة {frame_count} إطار بنجاح")
            
            # الآن نقوم بنسخ الصوت من الفيديو الأصلي إلى الفيديو المعالج
            # باستخدام FFmpeg للحفاظ على الصوت
            if self.ffmpeg_available:
                try:
                    logger.info("🔊 نسخ الصوت من الفيديو الأصلي...")
                    
                    # استخدام FFmpeg لدمج الفيديو المعالج مع الصوت الأصلي
                    cmd = [
                        'ffmpeg', '-y',
                        '-i', temp_output,  # الفيديو المعالج
                        '-i', video_path,   # الفيديو الأصلي (للصوت)
                        '-c:v', 'copy',     # نسخ الفيديو كما هو
                        '-c:a', 'aac',      # تحويل الصوت إلى AAC
                        '-b:a', '128k',     # معدل بت الصوت
                        '-map', '0:v:0',    # استخدام الفيديو من الملف الأول
                        '-map', '1:a:0',    # استخدام الصوت من الملف الثاني
                        final_output
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        logger.info("✅ تم دمج الصوت بنجاح")
                        # حذف الملف المؤقت
                        if os.path.exists(temp_output):
                            os.unlink(temp_output)
                        return final_output
                    else:
                        logger.warning(f"فشل في دمج الصوت: {result.stderr}")
                        # استخدام الملف المؤقت بدون صوت
                        shutil.copy2(temp_output, final_output)
                        if os.path.exists(temp_output):
                            os.unlink(temp_output)
                        return final_output
                        
                except Exception as e:
                    logger.warning(f"فشل في دمج الصوت: {e}")
                    # استخدام الملف المؤقت بدون صوت
                    shutil.copy2(temp_output, final_output)
                    if os.path.exists(temp_output):
                        os.unlink(temp_output)
                    return final_output
            else:
                # بدون FFmpeg، استخدم الملف المؤقت
                logger.warning("FFmpeg غير متوفر، الفيديو سيكون بدون صوت")
                shutil.copy2(temp_output, final_output)
                if os.path.exists(temp_output):
                    os.unlink(temp_output)
                return final_output
                
        except Exception as e:
            logger.error(f"خطأ في تطبيق العلامة المائية على الفيديو: {e}")
            # تنظيف الملفات المؤقتة
            for temp_file in [temp_output, final_output]:
                if os.path.exists(temp_file):
                    try:
                        os.unlink(temp_file)
                    except:
                        pass
            return None
    
    def should_apply_watermark(self, media_type: str, watermark_settings: dict) -> bool:
        """تحديد ما إذا كان يجب تطبيق العلامة المائية على نوع الوسائط"""
        if not watermark_settings.get('enabled', False):
            return False
        
        if media_type == 'photo' and not watermark_settings.get('apply_to_photos', True):
            return False
        
        if media_type == 'video' and not watermark_settings.get('apply_to_videos', True):
            return False
        
        if media_type == 'document' and not watermark_settings.get('apply_to_documents', False):
            return False
        
        return True
    
    def get_media_type_from_file(self, file_path: str) -> str:
        """تحديد نوع الوسائط من امتداد الملف"""
        ext = os.path.splitext(file_path.lower())[1]
        
        if ext in self.supported_image_formats:
            return 'photo'
        elif ext in self.supported_video_formats:
            return 'video'
        else:
            return 'document'
    
    def process_media_with_watermark(self, media_bytes: bytes, file_name: str, watermark_settings: dict) -> Optional[bytes]:
        """معالجة الوسائط مع العلامة المائية"""
        try:
            # تحديد نوع الوسائط
            media_type = self.get_media_type_from_file(file_name)
            
            if media_type == 'image':
                # معالجة الصور
                logger.info(f"🖼️ معالجة صورة: {file_name}")
                return self.apply_watermark_to_image(media_bytes, watermark_settings)
                
            elif media_type == 'video':
                # معالجة الفيديوهات
                logger.info(f"🎬 معالجة فيديو: {file_name}")
                
                # إنشاء ملف مؤقت للفيديو
                temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1])
                temp_input.write(media_bytes)
                temp_input.close()
                
                try:
                    # تطبيق العلامة المائية
                    watermarked_path = self.apply_watermark_to_video(temp_input.name, watermark_settings)
                    
                    if watermarked_path and os.path.exists(watermarked_path):
                        # الآن نقوم بضغط الفيديو مع الحفاظ على الدقة
                        compressed_path = tempfile.mktemp(suffix='.mp4')
                        
                        if self.compress_video_preserve_quality(watermarked_path, compressed_path):
                            logger.info("✅ تم ضغط الفيديو مع الحفاظ على الدقة")
                            final_path = compressed_path
                        else:
                            logger.warning("فشل في ضغط الفيديو، استخدام الفيديو الأصلي")
                            final_path = watermarked_path
                        
                        # قراءة الفيديو المعالج
                        with open(final_path, 'rb') as f:
                            watermarked_bytes = f.read()
                        
                        # تنظيف الملفات المؤقتة
                        os.unlink(temp_input.name)
                        if os.path.exists(watermarked_path):
                            os.unlink(watermarked_path)
                        if final_path != watermarked_path and os.path.exists(final_path):
                            os.unlink(final_path)
                        
                        return watermarked_bytes
                    else:
                        logger.warning("فشل في تطبيق العلامة المائية على الفيديو")
                        os.unlink(temp_input.name)
                        return media_bytes
                        
                except Exception as e:
                    logger.error(f"خطأ في معالجة الفيديو: {e}")
                    os.unlink(temp_input.name)
                    return media_bytes
            else:
                logger.warning(f"نوع وسائط غير مدعوم: {media_type}")
                return media_bytes
                
        except Exception as e:
            logger.error(f"خطأ في معالجة الوسائط: {e}")
            return media_bytes
    
    def process_media_once_for_all_targets(self, media_bytes: bytes, file_name: str, watermark_settings: dict, 
                                         task_id: int) -> Optional[bytes]:
        """معالجة الوسائط مرة واحدة وإعادة استخدامها لكل الأهداف"""
        try:
            # إنشاء مفتاح فريد للملف
            cache_key = f"{task_id}_{hash(media_bytes)}_{file_name}"
            
            # التحقق من وجود الملف في الذاكرة المؤقتة
            if cache_key in self.processed_media_cache:
                logger.info(f"🔄 إعادة استخدام الوسائط المعالجة مسبقاً للمهمة {task_id}")
                return self.processed_media_cache[cache_key]
            
            # معالجة الوسائط
            processed_media = self.process_media_with_watermark(media_bytes, file_name, watermark_settings)
            
            if processed_media and processed_media != media_bytes:
                # حفظ النتيجة في الذاكرة المؤقتة
                self.processed_media_cache[cache_key] = processed_media
                logger.info(f"✅ تم معالجة الوسائط وحفظها في الذاكرة المؤقتة للمهمة {task_id}")
                
                # تنظيف الذاكرة المؤقتة إذا أصبحت كبيرة جداً
                if len(self.processed_media_cache) > 50:
                    # حذف أقدم 10 عناصر
                    oldest_keys = list(self.processed_media_cache.keys())[:10]
                    for key in oldest_keys:
                        del self.processed_media_cache[key]
                    logger.info("🧹 تم تنظيف الذاكرة المؤقتة")
                
                return processed_media
            else:
                # إذا لم يتم تطبيق العلامة المائية، احفظ الملف الأصلي
                self.processed_media_cache[cache_key] = media_bytes
                return media_bytes
                
        except Exception as e:
            logger.error(f"خطأ في معالجة الوسائط مرة واحدة: {e}")
            return media_bytes
    
    def clear_cache(self):
        """مسح الذاكرة المؤقتة"""
        self.processed_media_cache.clear()
        logger.info("🧹 تم مسح الذاكرة المؤقتة للعلامة المائية")
    
    def get_cache_stats(self):
        """الحصول على إحصائيات الذاكرة المؤقتة"""
        return {
            'cache_size': len(self.processed_media_cache),
            'cache_keys': list(self.processed_media_cache.keys())
        }

    def compress_video_preserve_quality(self, input_path: str, output_path: str, target_size_mb: float = None) -> bool:
        """ضغط الفيديو مع الحفاظ على الدقة والجودة"""
        try:
            if not self.ffmpeg_available:
                logger.warning("FFmpeg غير متوفر، لا يمكن ضغط الفيديو")
                return False
            
            # الحصول على معلومات الفيديو
            video_info = self.get_video_info(input_path)
            if not video_info:
                logger.warning("فشل في الحصول على معلومات الفيديو")
                return False
            
            original_size = video_info.get('size_mb', 0)
            original_width = video_info.get('width', 0)
            original_height = video_info.get('height', 0)
            original_fps = video_info.get('fps', 30)
            duration = video_info.get('duration', 0)
            
            logger.info(f"📹 معلومات الفيديو الأصلي: {original_width}x{original_height}, {original_fps} FPS, {original_size:.2f} MB")
            
            # حساب معدل البت الأمثل
            if target_size_mb and original_size > target_size_mb:
                # حساب معدل البت المطلوب للوصول للحجم المستهدف
                target_bitrate = int((target_size_mb * 8 * 1024 * 1024) / duration)
                target_bitrate = max(target_bitrate, 500000)  # حد أدنى 500 kbps
                
                logger.info(f"🎯 الحجم المستهدف: {target_size_mb:.2f} MB, معدل البت: {target_bitrate/1000:.0f} kbps")
            else:
                # استخدام معدل البت الأصلي مع تحسين بسيط
                target_bitrate = int(video_info.get('bitrate', 2000000) * 0.8)  # تقليل 20%
                logger.info(f"🔄 تحسين بسيط: معدل البت {target_bitrate/1000:.0f} kbps")
            
            # إعدادات FFmpeg محسنة للحفاظ على الجودة
            cmd = [
                'ffmpeg', '-y',
                '-i', input_path,
                # إعدادات الفيديو - الحفاظ على الدقة
                '-c:v', 'libx264',           # كودك H.264
                '-preset', 'slow',           # بطيء للحصول على جودة أفضل
                '-crf', '18',                # جودة عالية (18 = جودة ممتازة)
                '-maxrate', f'{target_bitrate}',
                '-bufsize', f'{target_bitrate * 2}',
                '-profile:v', 'high',        # ملف H.264 عالي
                '-level', '4.1',             # مستوى متوافق
                # إعدادات الصوت
                '-c:a', 'aac',               # كودك الصوت
                '-b:a', '128k',              # معدل بت الصوت
                '-ar', '48000',              # معدل العينات
                # إعدادات إضافية
                '-movflags', '+faststart',   # تحسين التشغيل
                '-pix_fmt', 'yuv420p',       # تنسيق بكسل متوافق
                '-metadata', 'title=Enhanced Bot Video',
                output_path
            ]
            
            logger.info(f"🎬 بدء ضغط الفيديو مع الحفاظ على الدقة...")
            
            # تنفيذ الضغط
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # التحقق من النتيجة
                final_info = self.get_video_info(output_path)
                if final_info:
                    final_size = final_info.get('size_mb', 0)
                    final_width = final_info.get('width', 0)
                    final_height = final_info.get('height', 0)
                    final_fps = final_info.get('fps', 0)
                    
                    # التحقق من الحفاظ على الدقة
                    if final_width == original_width and final_height == original_height:
                        compression_ratio = (original_size - final_size) / original_size * 100
                        
                        logger.info(f"✅ تم ضغط الفيديو بنجاح مع الحفاظ على الدقة:")
                        logger.info(f"   📏 الدقة: {final_width}x{final_height} (محفوظة)")
                        logger.info(f"   🎬 معدل الإطارات: {final_fps} FPS")
                        logger.info(f"   📦 الحجم: {original_size:.2f} MB → {final_size:.2f} MB")
                        logger.info(f"   💾 التوفير: {compression_ratio:.1f}%")
                        
                        return True
                    else:
                        logger.warning(f"⚠️ تغيرت الدقة: {original_width}x{original_height} → {final_width}x{final_height}")
                        return False
                else:
                    logger.warning("تم إنشاء الفيديو ولكن فشل في التحقق من النتيجة")
                    return True
            else:
                logger.error(f"فشل في ضغط الفيديو: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"خطأ في ضغط الفيديو: {e}")
            return False