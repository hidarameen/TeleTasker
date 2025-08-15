
FROM python:3.11-slim

# تحديث النظام وتنصيب المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات
COPY requirements.txt .
COPY pyproject.toml .

# تنصيب المكتبات المطلوبة
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كامل المشروع
COPY . .

# إنشاء مجلدات البيانات
RUN mkdir -p watermark_images attached_assets

# تعيين المتغيرات البيئية
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# فتح المنفذ
EXPOSE 5000

# تشغيل البوت
CMD ["python", "main.py"]
