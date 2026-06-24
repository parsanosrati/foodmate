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
# /start
# ───────────────────────────────────────────────

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        Messages.WELCOME.format(name=message.from_user.first_name),
        reply_markup=main_menu_keyboard(),
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(Messages.HELP)


# ───────────────────────────────────────────────
# Main Menu
# ───────────────────────────────────────────────

@dp.callback_query(F.data == "recommend")
async def start_recommendation(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        Messages.SELECT_MEAL_TYPE,
        reply_markup=meal_type_keyboard(),
    )
    await state.set_state(RecommendationStates.selecting_meal_type)
    await callback.answer()


@dp.callback_query(F.data == "surprise")
async def surprise_me(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(Messages.LOADING)
    try:
        result = await get_food_recommendation(context={
            "meal_type": "هر چیزی",
            "cuisine": "هر نوعی",
            "cooking_time": "هر مدتی",
            "dietary": "بدون محدودیت",
            "ingredients": "",
            "surprise": True,
        })
        await callback.message.edit_text(
            result,
            reply_markup=recipe_actions_keyboard(),
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Surprise error: {e}")
        await callback.message.edit_text(Messages.ERROR, reply_markup=main_menu_keyboard())
    await callback.answer()


@dp.callback_query(F.data == "help_menu")
async def help_menu(callback: CallbackQuery):
    await callback.message.edit_text(Messages.HELP, reply_markup=main_menu_keyboard())
    await callback.answer()


# ───────────────────────────────────────────────
# Recommendation Flow
# ───────────────────────────────────────────────

@dp.callback_query(RecommendationStates.selecting_meal_type)
async def select_meal_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(meal_type=callback.data)
    await callback.message.edit_text(
        Messages.SELECT_CUISINE,
        reply_markup=cuisine_keyboard(),
    )
    await state.set_state(RecommendationStates.selecting_cuisine)
    await callback.answer()


@dp.callback_query(RecommendationStates.selecting_cuisine)
async def select_cuisine(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cuisine=callback.data)
    await callback.message.edit_text(
        Messages.SELECT_COOKING_TIME,
        reply_markup=cooking_time_keyboard(),
    )
    await state.set_state(RecommendationStates.selecting_cooking_time)
    await callback.answer()


@dp.callback_query(RecommendationStates.selecting_cooking_time)
async def select_cooking_time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cooking_time=callback.data)
    await callback.message.edit_text(
        Messages.SELECT_DIETARY,
        reply_markup=dietary_keyboard(),
    )
    await state.set_state(RecommendationStates.selecting_dietary)
    await callback.answer()


@dp.callback_query(RecommendationStates.selecting_dietary)
async def select_dietary(callback: CallbackQuery, state: FSMContext):
    await state.update_data(dietary=callback.data)
    await callback.message.edit_text(Messages.ASK_INGREDIENTS)
    await state.set_state(RecommendationStates.entering_ingredients)
    await callback.answer()


@dp.message(RecommendationStates.entering_ingredients)
async def enter_ingredients(message: Message, state: FSMContext):
    ingredients = message.text.strip()
    await state.update_data(ingredients=ingredients)
    data = await state.get_data()

    loading_msg = await message.answer(Messages.LOADING)

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
        await loading_msg.edit_text(Messages.ERROR, reply_markup=main_menu_keyboard())
        await state.clear()


# ───────────────────────────────────────────────
# Post-recommendation Actions
# ───────────────────────────────────────────────

@dp.callback_query(F.data == "new_recommendation")
async def new_recommendation(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        Messages.SELECT_MEAL_TYPE,
        reply_markup=meal_type_keyboard(),
    )
    await state.set_state(RecommendationStates.selecting_meal_type)
    await callback.answer()


@dp.callback_query(F.data == "rate")
async def ask_rating(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        Messages.ASK_RATING,
        reply_markup=rating_keyboard(),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("rating_"))
async def receive_rating(callback: CallbackQuery, state: FSMContext):
    rating = callback.data.replace("rating_", "")
    stars = "⭐" * int(rating)
    await callback.message.edit_text(
        Messages.RATING_THANKS.format(stars=stars),
        reply_markup=main_menu_keyboard(),
    )
    await state.clear()
    await callback.answer()


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        Messages.MAIN_MENU,
        reply_markup=main_menu_keyboard(),
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
