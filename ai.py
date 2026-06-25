import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """تو یک سرآشپز حرفه‌ای و دستیار هوشمند آشپزی به اسم FoodMate AI هستی.

وظیفه اصلی تو اینه که یک پیشنهاد غذایی کامل با دستور پخت دقیق بدی.

قوانین مهم:
- همیشه فارسی جواب بده
- حتماً دستور پخت کامل و گام به گام بنویس
- مقدار دقیق مواد رو بنویس (مثلاً ۲۰۰ گرم مرغ، ۳ قاشق روغن)
- از ایموجی مناسب استفاده کن
- لحن دوستانه و انگیزشی داشته باش
- اگه کاربر محدودیت رژیمی داره، کاملاً رعایت کن
- اگه کاربر کم‌کالری یا رژیمی خواست، کالری کم و مواد سالم پیشنهاد بده

فرمت جواب باید دقیقاً اینطور باشه و هیچ بخشی رو حذف نکن:

🍽 **[نام غذا]**
_[یک جمله توضیح جذاب و اشتهاآور]_

━━━━━━━━━━━━━━━
📊 **اطلاعات کلی:**
⏱ زمان آماده‌سازی: [زمان]
🔥 سختی پخت: [آسان / متوسط / حرفه‌ای]
🍴 برای: [تعداد نفر] نفر
🥗 کالری هر وعده: [عدد] کیلوکالری

━━━━━━━━━━━━━━━
🛒 **مواد لازم:**
[لیست مواد با مقدار دقیق، هر ماده یک خط با ایموجی مناسب]

━━━━━━━━━━━━━━━
👨‍🍳 **دستور پخت:**
[حداقل ۵ مرحله کامل و دقیق، شماره‌گذاری شده]

━━━━━━━━━━━━━━━
💡 **نکته سرآشپز:**
[یک نکته مفید برای بهتر شدن طعم یا سرو]

━━━━━━━━━━━━━━━
🍴 **پیشنهاد سرو:**
[چطور سرو کنیم، با چی بخوریم]

━━━━━━━━━━━━━━━
🔀 **اگه این رو دوست نداشتی، اینا رو امتحان کن:**
• [غذای مشابه ۱]
• [غذای مشابه ۲]
• [غذای مشابه ۳]
"""


async def get_food_recommendation(context: dict) -> str:
    """
    Get a complete food recommendation with full recipe from Gemini.

    Args:
        context: Dictionary containing user preferences and selections

    Returns:
        Formatted recommendation string in Persian with full recipe
    """
    try:
        user_message = _build_user_message(context)
        logger.info(f"Requesting recommendation. Context: {context}")

        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\n{user_message}",
            generation_config=genai.types.GenerationConfig(
                temperature=0.85,
                max_output_tokens=2000,
            ),
        )

        result = response.text.strip()
        logger.info("Successfully received recommendation from Gemini")
        return result

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise


def _build_user_message(context: dict) -> str:
    """Build a detailed user message from context dictionary."""

    if context.get("surprise"):
        return (
            "یک غذای خوشمزه و محبوب پیشنهاد بده که بیشتر مردم دوست دارن. "
            "چیزی که هم خوشمزه باشه هم نسبتاً راحت بپزیم. "
            "دستور پخت کامل با تمام جزئیات بنویس."
        )

    parts = ["کاربر این مشخصات رو انتخاب کرده. یک غذای مناسب با دستور پخت کامل پیشنهاد بده:\n"]

    meal_type = context.get("meal_type", "")
    if meal_type:
        parts.append(f"• وعده غذایی: {meal_type}")

    cuisine = context.get("cuisine", "")
    if cuisine:
        parts.append(f"• سبک آشپزی: {cuisine}")

    cooking_time = context.get("cooking_time", "")
    if cooking_time:
        parts.append(f"• زمان پخت: {cooking_time}")

    dietary = context.get("dietary", "")
    if dietary and dietary != "بدون محدودیت":
        parts.append(f"• رژیم/محدودیت غذایی: {dietary} — این رو جدی بگیر و کاملاً رعایت کن")

    spicy = context.get("spicy", "")
    if spicy and spicy != "هر میزان تندی":
        parts.append(f"• میزان تندی: {spicy}")

    difficulty = context.get("difficulty", "")
    if difficulty and difficulty != "هر سطحی":
        parts.append(f"• سطح دشواری: {difficulty}")

    ingredients = context.get("ingredients", "").strip()
    if ingredients and ingredients not in ("هر چیزی", "هر چی", "-", "", "ندارم"):
        parts.append(f"• مواد موجود در خونه: {ingredients} — سعی کن از این مواد استفاده کنی")
    else:
        parts.append("• مواد: هر چیزی که مناسب باشه")

    parts.append("\nحتماً دستور پخت کامل و گام به گام بنویس. هیچ بخشی رو حذف نکن.")
    return "\n".join(parts)
