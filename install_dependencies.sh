#!/bin/bash

# سكريبت تثبيت متطلبات البوت المحسن
# Enhanced Bot Dependencies Installation Script

echo "🚀 بدء تثبيت متطلبات البوت المحسن..."
echo "=========================================="

# تحديد نظام التشغيل
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        echo "📦 تثبيت FFmpeg على Ubuntu/Debian..."
        sudo apt update
        sudo apt install -y ffmpeg
    elif command -v yum &> /dev/null; then
        echo "📦 تثبيت FFmpeg على CentOS/RHEL..."
        sudo yum install -y ffmpeg
    elif command -v dnf &> /dev/null; then
        echo "📦 تثبيت FFmpeg على Fedora..."
        sudo dnf install -y ffmpeg
    else
        echo "⚠️ نظام تشغيل غير معروف، يرجى تثبيت FFmpeg يدوياً"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "📦 تثبيت FFmpeg على macOS..."
    if command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        echo "⚠️ يرجى تثبيت Homebrew أولاً: https://brew.sh/"
    fi
else
    echo "⚠️ نظام تشغيل غير معروف، يرجى تثبيت FFmpeg يدوياً"
fi

echo "=========================================="
echo "🐍 تثبيت مكتبات Python..."

# تثبيت مكتبات Python
pip install --upgrade pip
pip install -r requirements.txt

echo "=========================================="
echo "🔍 التحقق من التثبيت..."

# التحقق من FFmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg مثبت بنجاح"
    ffmpeg -version | head -n 1
else
    echo "❌ FFmpeg غير مثبت"
fi

# التحقق من ffprobe
if command -v ffprobe &> /dev/null; then
    echo "✅ ffprobe مثبت بنجاح"
else
    echo "❌ ffprobe غير مثبت"
fi

echo "=========================================="
echo "🎯 تثبيت المكتبات الإضافية..."

# تثبيت مكتبات إضافية مفيدة
pip install --upgrade setuptools wheel

echo "=========================================="
echo "✨ تم الانتهاء من التثبيت!"
echo ""
echo "📋 للتشغيل:"
echo "python main.py"
echo ""
echo "🔧 في حالة وجود مشاكل:"
echo "1. تأكد من تثبيت FFmpeg"
echo "2. تأكد من تحديث pip"
echo "3. تأكد من وجود Python 3.8+"
echo ""
echo "🚀 البوت جاهز للتشغيل!"