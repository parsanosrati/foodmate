import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """تو یک دستیار هوشمند آشپزی به اسم FoodMate AI هستی.
وقتی کاربر اطلاعات غذایی می‌ده، یک پیشنهاد غذایی کامل و خوشمزه به فارسی می‌دی.

قوانین مهم:
- همیشه به فارسی جواب بده
- پیشنهادت باید عملی و قابل پخت باشه
- اطلاعات کامل و مفید بده
- از ایموجی مناسب استفاده کن
- لحن دوستانه و انگیزشی داشته باش

فرمت جواب باید دقیقاً اینطور باشه:

🍽 **[نام غذا]**
[یک جمله توضیح کوتاه و جذاب]

⏱ زمان پخت: [زمان]
🔥 سختی: [آسان/متوسط/سخت]
🥗 کالری تقریبی: [عدد] کیلوکالری

---
**🛒 مواد لازم:**
[لیست مواد با مقدار]

---
**👨‍🍳 طرز تهیه:**
[مراحل پخت به صورت شماره‌گذاری شده]

---
**💡 نکته آشپزی:**
[یک نکته مفید]

---
**🍴 ۳ پیشنهاد مشابه:**
[سه غذای مشابه]
"""


async def get_food_recommendation(context: dict) -> str:
    """
    Get food recommendation from Gemini based on user context.

    Args:
        context: Dictionary containing user preferences

    Returns:
        Formatted recommendation string in Persian
    """
    try:
        user_message = _build_user_message(context)
        logger.info(f"Requesting recommendation for context: {context}")

        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\n{user_message}",
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                max_output_tokens=1500,
            ),
        )

        result = response.text.strip()
        logger.info("Successfully received recommendation from Gemini")
        return result

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise


def _build_user_message(context: dict) -> str:
    """Build the user message from context dictionary."""

    if context.get("surprise"):
        return (
            "یک غذای جالب و خوشمزه پیشنهاد بده که بیشتر مردم دوست دارن. "
            "چیزی که هم خوشمزه باشه هم نسبتاً آسون باشه بپزیم."
        )

    parts = ["لطفاً یک غذا پیشنهاد بده با این مشخصات:"]

    if context.get("meal_type"):
        parts.append(f"• وعده غذایی: {context['meal_type']}")

    if context.get("cuisine"):
        parts.append(f"• سبک آشپزی: {context['cuisine']}")

    if context.get("cooking_time"):
        parts.append(f"• زمان پخت: {context['cooking_time']}")

    if context.get("dietary"):
        parts.append(f"• محدودیت غذایی: {context['dietary']}")

    ingredients = context.get("ingredients", "").strip()
    if ingredients and ingredients not in ("هر چیزی", "هر چی", "-", ""):
        parts.append(f"• مواد موجود خونه: {ingredients}")
    else:
        parts.append("• مواد: هر چیزی که مناسب باشه")

    parts.append("\nیک پیشنهاد کامل با دستور پخت بده.")
    return "\n".join(parts)
