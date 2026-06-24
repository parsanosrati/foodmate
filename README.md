# FoodMate AI 🍽

یک بات هوشمند تلگرام برای پیشنهاد غذا با استفاده از Gemini AI

## راه‌اندازی محلی

### ۱. کلون کردن پروژه
```bash
git clone https://github.com/your-username/foodmate.git
cd foodmate
```

### ۲. نصب dependencies
```bash
pip install -r requirements.txt
```

### ۳. تنظیم متغیرهای محیطی
```bash
cp .env.example .env
```
فایل `.env` رو باز کن و مقادیر رو پر کن:
```
TELEGRAM_BOT_TOKEN=توکن_بات_تلگرامت
GEMINI_API_KEY=کلید_API_جمینات
```

### ۴. اجرا
```bash
python bot.py
```

## دیپلوی روی Render

۱. پروژه رو روی GitHub بذار
۲. در Render یه **Background Worker** جدید بساز
۳. ریپازیتوری GitHub رو وصل کن
۴. Environment Variables رو اضافه کن:
   - `TELEGRAM_BOT_TOKEN`
   - `GEMINI_API_KEY`
۵. دیپلوی کن!

## ساختار پروژه

```
foodmate/
├── bot.py          # هسته اصلی بات
├── ai.py           # ارتباط با Gemini AI
├── keyboards.py    # دکمه‌های تلگرام
├── messages.py     # متن‌های پیام
├── states.py       # حالت‌های FSM
├── requirements.txt
├── Procfile
└── .env.example
```
