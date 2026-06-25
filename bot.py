import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from keyboards import (
    main_menu_keyboard,
    meal_type_keyboard,
    cuisine_keyboard,
    cooking_time_keyboard,
    dietary_keyboard,
    spicy_keyboard,
    difficulty_keyboard,
    rating_keyboard,
    recipe_actions_keyboard,
)
from messages import Messages
from ai import get_food_recommendation
from states import RecommendationStates

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())


# ───────────────────────────────────────────────
# /start و /help
# ───────────────────────────────────────────────

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        Messages.WELCOME.format(name=message.from_user.first_name),
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(Messages.HELP, parse_mode="Markdown")


# ───────────────────────────────────────────────
# منوی اصلی
# ───────────────────────────────────────────────

@dp.callback_query(F.data == "recommend")
async def start_recommendation(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        Messages.SELECT_MEAL_TYPE,
        reply_markup=meal_type_keyboard(),
        parse_mode="Markdown",
    )
    await state.set_state(RecommendationStates.selecting_meal_type)
    await callback.answer()


@dp.callback_query(F.data == "surprise")
async def surprise_me(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    loading_msg = await callback.message.answer(Messages.LOADING, parse_mode="Markdown")
    try:
        result = await get_food_recommendation(context={"surprise": True})
        await loading_msg.edit_text(result, reply_markup=recipe_actions_keyboard(), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Surprise error: {e}")
        await loading_msg.edit_text(Messages.ERROR, reply_markup=main_menu_keyboard(), parse_mode="Markdown")
    await callback.answer()


@dp.callback_query(F.data == "help_menu")
async def help_menu(callback: CallbackQuery):
    await callback.message.answer(Messages.HELP, parse_mode="Markdown")
    await callback.answer()


# ───────────────────────────────────────────────
# مرحله ۱ — وعده غذایی
# ───────────────────────────────────────────────

@dp.callback_query(RecommendationStates.selecting_meal_type, F.data == "type_meal_type")
async def ask_type_meal_type(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(Messages.TYPE_MEAL_TYPE, parse_mode="Markdown")
    await state.set_state(RecommendationStates.typing_meal_type)
    await callback.answer()


@dp.message(RecommendationStates.typing_meal_type)
async def receive_typed_meal_type(message: Message, state: FSMContext):
    value = message.text.strip()
    await state.update_data(meal_type=value)
    await message.answer(Messages.SELECTION_SAVED.format(value=value), parse_mode="Markdown")
    await message.answer(Messages.SELECT_CUISINE, reply_markup=cuisine_keyboard(), parse_mode="Markdown")
    await state.set_state(RecommendationStates.selecting_cuisine)


@dp.callback_query(RecommendationStates.selecting_meal_type)
async def select_meal_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(meal_type=callback.data)
    await callback.message.answer(
        Messages.SELECTION_SAVED.format(value=callback.data),
        parse_mode="Markdown",
    )
    await callback.message.answer(Messages.SELECT_CUISINE, reply_markup=cuisine_keyboard(), parse_mode="Markdown")
    await state.set_state(RecommendationStates.selecting_cuisine)
    await callback.answer()


# ───────────────────────────────────────────────
# مرحله ۲ — سبک آشپزی
# ───────────────────────────────────────────────

@dp.callback_query(RecommendationStates.selecting_cuisine, F.data == "type_cuisine")
async def ask_type_cuisine(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(Messages.TYPE_CUISINE, parse_mode="Markdown")
    await state.set_state(RecommendationStates.typing_cuisine)
    await callback.answer()


@dp.message(RecommendationStates.typing_cuisine)
async def receive_typed_cuisine(message: Message, state: FSMContext):
    value = message.text.strip()
    await state.update_data(cuisine=value)
    await message.answer(Messages.SELECTION_SAVED.format(value=value), parse_mode="Markdown")
    await message.answer(Messages.SELECT_COOKING_TIME, reply_markup=cooking_time_keyboard(), parse_mode="Markdown")
    await state.set_state(RecommendationStates.selecting_cooking_time)


@dp.callback_query(RecommendationStates.selecting_cuisine)
async def select_cuisine(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cuisine=callback.data)
    await callback.message.answer(
        Messages.SELECTION_SAVED.format(value=callback.data),
        parse_mode="Markdown",
    )
    await callback.message.answer(Messages.SELECT_COOKING_TIME, reply_markup=cooking_time_keyboard(), parse_mode="Markdown")
    await state.set_state(RecommendationStates.selecting_cooking_time)
    await callback.answer()


# ───────────────────────────────────────────────
# مرحله ۳ — زمان پخت
# ───────────────────────────────────────────────

@dp.callback_query(RecommendationStates.selecting_cooking_time, F.data == "type_cooking_time")
async def ask_type_cooking_time(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(Messages.TYPE_COOKING_TIME, parse_mode="Markdown")
    await state.set_state(RecommendationStates.typing_cooking_time)
    await callback.answer()


@dp.message(RecommendationStates.typing_cooking_time)
async def receive_typed_cooking_time(message: Message, state: FSMContext):
    value = message.text.strip()
    await state.update_data(cooking_time=value)
    await message.answer(Messages.SELECTION_SAVED.format(value=value), parse_mode="Markdown")
    await message.answer(Messages.SELECT_DIETARY, reply_markup=dietary_keyboard(), parse_mode="Markdown")
    await state.set_state(RecommendationStates.selecting_dietary)


@dp.callback_query(RecommendationStates.selecting_cooking_time)
async def select_cooking_time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cooking_time=callback.data)
    await callback.message.answer(
        Messages.SELECTION_SAVED.format(value=callback.data),
        parse_mode="Markdown",
    )
    await callback.message.answer(Messages.SELECT_DIETARY, reply_markup=dietary_keyboard(), parse_mode="Markdown")
    await state.set_state(RecommendationStates.selecting_dietary)
    await callback.answer()


# ───────────────────────────────────────────────
# مرحله ۴ — رژیم غذایی
# ───────────────────────────────────────────────

@dp.callback_query(RecommendationStates.selecting_dietary, F.data == "type_dietary")
async def ask_type_dietary(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(Messages.TYPE_DIETARY, parse_mode="Markdown")
    await state.set_state(RecommendationStates.typing_dietary)
    await callback.answer()


@dp.message(RecommendationStates.typing_dietary)
async def receive_typed_dietary(message: Message, state: FSMContext):
    value = message.text.strip()
    await state.update_data(dietary=value)
    await message.answer(Messages.SELECTION_SAVED.format(value=value), parse_mode="Markdown")
    await message.answer(Messages.SELECT_SPICY, reply_markup=spicy_keyboard(), parse_mode="Markdown")
    await state.set_state(RecommendationStates.selecting_spicy)


@dp.callback_query(RecommendationStates.selecting_dietary)
async def select_dietary(callback: CallbackQuery, state: FSMContext):
    await state.update_data(dietary=callback.data)
    await callback.message.answer(
        Messages.SELECTION_SAVED.format(value=callback.data),
        parse_mode="Markdown",
    )
    await callback.message.answer(Messages.SELECT_SPICY, reply_markup=spicy_keyboard(), parse_mode="Markdown")
    await state.set_state(RecommendationStates.selecting_spicy)
    await callback.answer()


# ───────────────────────────────────────────────
# مرحله ۵ — تندی
# ───────────────────────────────────────────────

@dp.callback_query(RecommendationStates.selecting_spicy)
async def select_spicy(callback: CallbackQuery, state: FSMContext):
    await state.update_data(spicy=callback.data)
    await callback.message.answer(
        Messages.SELECTION_SAVED.format(value=callback.data),
        parse_mode="Markdown",
    )
    await callback.message.answer(Messages.ASK_INGREDIENTS, parse_mode="Markdown")
    await state.set_state(RecommendationStates.entering_ingredients)
    await callback.answer()


# ───────────────────────────────────────────────
# مرحله ۶ — مواد موجود و دریافت پیشنهاد
# ───────────────────────────────────────────────

@dp.message(RecommendationStates.entering_ingredients)
async def enter_ingredients(message: Message, state: FSMContext):
    ingredients = message.text.strip()
    await state.update_data(ingredients=ingredients)
    data = await state.get_data()

    loading_msg = await message.answer(Messages.LOADING, parse_mode="Markdown")

    try:
        result = await get_food_recommendation(context=data)
        await loading_msg.edit_text(
            result,
            reply_markup=recipe_actions_keyboard(),
            parse_mode="Markdown",
        )
        await state.set_state(RecommendationStates.viewing_recommendation)
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        await loading_msg.edit_text(Messages.ERROR, reply_markup=main_menu_keyboard(), parse_mode="Markdown")
        await state.clear()


# ───────────────────────────────────────────────
# بعد از پیشنهاد
# ───────────────────────────────────────────────

@dp.callback_query(F.data == "new_recommendation")
async def new_recommendation(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        Messages.SELECT_MEAL_TYPE,
        reply_markup=meal_type_keyboard(),
        parse_mode="Markdown",
    )
    await state.set_state(RecommendationStates.selecting_meal_type)
    await callback.answer()


@dp.callback_query(F.data == "rate")
async def ask_rating(callback: CallbackQuery):
    await callback.message.answer(Messages.ASK_RATING, reply_markup=rating_keyboard(), parse_mode="Markdown")
    await callback.answer()


@dp.callback_query(F.data.startswith("rating_"))
async def receive_rating(callback: CallbackQuery, state: FSMContext):
    rating = callback.data.replace("rating_", "")
    stars = "⭐" * int(rating)
    await callback.message.answer(
        Messages.RATING_THANKS.format(stars=stars),
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )
    await state.clear()
    await callback.answer()


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        Messages.MAIN_MENU,
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


# ───────────────────────────────────────────────
# Fallback
# ───────────────────────────────────────────────

@dp.message()
async def fallback(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(Messages.UNKNOWN, reply_markup=main_menu_keyboard())


async def main():
    logger.info("FoodMate AI Bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
