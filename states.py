from aiogram.fsm.state import State, StatesGroup


class RecommendationStates(StatesGroup):
    selecting_meal_type = State()
    selecting_cuisine = State()
    selecting_cooking_time = State()
    selecting_dietary = State()
    entering_ingredients = State()
    viewing_recommendation = State()
