from aiogram.fsm.state import State, StatesGroup


class NatsTestSG(StatesGroup):
    enter_text = State()
