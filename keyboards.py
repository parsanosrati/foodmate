from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍽 پیشنهاد غذا", callback_data="recommend")],
        [InlineKeyboardButton(text="🎲 شگفت‌زده‌ام کن!", callback_data="surprise")],
        [InlineKeyboardButton(text="❓ راهنما", callback_data="help_menu")],
    ])


def meal_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌅 صبحانه", callback_data="صبحانه"),
            InlineKeyboardButton(text="☀️ ناهار", callback_data="ناهار"),
        ],
        [
            InlineKeyboardButton(text="🌙 شام", callback_data="شام"),
            InlineKeyboardButton(text="🍿 میان‌وعده", callback_data="میان‌وعده"),
        ],
        [
            InlineKeyboardButton(text="🍰 دسر", callback_data="دسر"),
            InlineKeyboardButton(text="🎯 هر چیزی", callback_data="هر چیزی"),
        ],
    ])


def cuisine_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇮🇷 ایرانی", callback_data="ایرانی"),
            InlineKeyboardButton(text="🇮🇹 ایتالیایی", callback_data="ایتالیایی"),
        ],
        [
            InlineKeyboardButton(text="🇯🇵 ژاپنی", callback_data="ژاپنی"),
            InlineKeyboardButton(text="🇨🇳 چینی", callback_data="چینی"),
        ],
        [
            InlineKeyboardButton(text="🇲🇽 مکزیکی", callback_data="مکزیکی"),
            InlineKeyboardButton(text="🇮🇳 هندی", callback_data="هندی"),
        ],
        [
            InlineKeyboardButton(text="🌍 هر نوعی", callback_data="هر نوعی"),
        ],
    ])


def cooking_time_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⚡ زیر ۱۵ دقیقه", callback_data="زیر ۱۵ دقیقه"),
            InlineKeyboardButton(text="🕐 ۱۵ تا ۳۰ دقیقه", callback_data="۱۵ تا ۳۰ دقیقه"),
        ],
        [
            InlineKeyboardButton(text="🕑 ۳۰ تا ۶۰ دقیقه", callback_data="۳۰ تا ۶۰ دقیقه"),
            InlineKeyboardButton(text="🍲 بیشتر از یه ساعت", callback_data="بیشتر از یه ساعت"),
        ],
        [
            InlineKeyboardButton(text="⏰ فرقی نمی‌کنه", callback_data="هر مدتی"),
        ],
    ])


def dietary_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🥗 گیاهخوار", callback_data="گیاهخوار"),
            InlineKeyboardButton(text="🌱 وگان", callback_data="وگان"),
        ],
        [
            InlineKeyboardButton(text="🚫🌾 بدون گلوتن", callback_data="بدون گلوتن"),
            InlineKeyboardButton(text="🚫🥛 بدون لبنیات", callback_data="بدون لبنیات"),
        ],
        [
            InlineKeyboardButton(text="✅ محدودیتی ندارم", callback_data="بدون محدودیت"),
        ],
    ])


def recipe_actions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 پیشنهاد جدید", callback_data="new_recommendation"),
            InlineKeyboardButton(text="⭐ امتیاز بده", callback_data="rate"),
        ],
        [
            InlineKeyboardButton(text="🏠 منوی اصلی", callback_data="back_to_menu"),
        ],
    ])


def rating_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1⭐", callback_data="rating_1"),
            InlineKeyboardButton(text="2⭐", callback_data="rating_2"),
            InlineKeyboardButton(text="3⭐", callback_data="rating_3"),
            InlineKeyboardButton(text="4⭐", callback_data="rating_4"),
            InlineKeyboardButton(text="5⭐", callback_data="rating_5"),
        ],
    ])
