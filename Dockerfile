# Dockerfile للبوت المحسن مع دعم FFmpeg
# Enhanced Bot Dockerfile with FFmpeg support

FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# تحديث النظام وتثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgtk-3-0 \
    libavcodec-extra \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavresample-dev \
    libpostproc-dev \
    libswscale-dev \
    libavutil-dev \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات
COPY requirements.txt .

# تثبيت مكتبات Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# إنشاء مجلد للملفات المؤقتة
RUN mkdir -p /tmp/bot_temp

# تعيين الصلاحيات
RUN chmod +x install_dependencies.sh

# فتح المنافذ المطلوبة
EXPOSE 8000

# أمر التشغيل
CMD ["python", "main.py"]
