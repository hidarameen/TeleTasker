FROM python:3.11-slim

# بيئة العمل
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=UTC

# تحديث النظام وتثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libavcodec-extra \
    libavformat-dev \
    libswscale-dev \
    libavutil-dev \
    libavdevice-dev \
    libavfilter-dev \
    libpostproc-dev \
    libx264-dev \
    libxvidcore-dev \
    libv4l-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgtk-3-0 \
    wget \
    curl \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

# مجلد العمل
WORKDIR /app

# نسخ requirements وتثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# إنشاء المجلدات المطلوبة
RUN mkdir -p /tmp/bot_temp /app/logs /app/data /app/watermark_images

# إعطاء صلاحيات
RUN chmod +x install_dependencies.sh start.sh || true

# فحص FFmpeg
RUN ffmpeg -version && ffprobe -version

# المنفذ
EXPOSE 8000

# تشغيل البوت
CMD ["python", "main.py"]

# أمر التشغيل
CMD ["python", "main.py"]
