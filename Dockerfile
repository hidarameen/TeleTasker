# Dockerfile للبوت المحسن مع دعم FFmpeg
# Enhanced Bot Dockerfile with FFmpeg support

FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# تحديث النظام وتثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    # FFmpeg الأساسي
    ffmpeg \
    # مكتبات الوسائط
    libavcodec-extra \
    libavformat-dev \
    libswscale-dev \
    libavutil-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavresample-dev \
    libpostproc-dev \
    # مكتبات الفيديو
    libx264-dev \
    libxvidcore-dev \
    libv4l-dev \
    # مكتبات الصور
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    # مكتبات OpenCV
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgtk-3-0 \
    # أدوات إضافية
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات أولاً (لتحسين التخزين المؤقت)
COPY requirements.txt .

# تثبيت مكتبات Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# إنشاء المجلدات المطلوبة
RUN mkdir -p /tmp/bot_temp \
    && mkdir -p /app/logs \
    && mkdir -p /app/data \
    && mkdir -p /app/watermark_images

# تعيين الصلاحيات
RUN chmod +x install_dependencies.sh \
    && chmod +x start.sh

# التحقق من تثبيت FFmpeg
RUN ffmpeg -version \
    && ffprobe -version

# فتح المنافذ المطلوبة
EXPOSE 8000

# أمر التشغيل
CMD ["python", "main.py"]
