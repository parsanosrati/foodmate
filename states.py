from aiogram.fsm.state import State, StatesGroup


class RecommendationStates(StatesGroup):
    selecting_meal_type = State()
    typing_meal_type = State()
    selecting_cuisine = State()
    typing_cuisine = State()
    selecting_cooking_time = State()
    typing_cooking_time = State()
    selecting_dietary = State()
    typing_dietary = State()
    entering_ingredients = State()
    selecting_spicy = State()
    selecting_difficulty = State()
    viewing_recommendation = State()
