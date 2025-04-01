from aiogram.fsm.state import StatesGroup, State


class InputTeacherName(StatesGroup):
    waiting_for_msg = State()
