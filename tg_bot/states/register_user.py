from aiogram.fsm.state import StatesGroup, State


class InputUserStudyGroup(StatesGroup):
    waiting_for_msg = State()
