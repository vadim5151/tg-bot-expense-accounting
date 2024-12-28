from ssl import SSLContext
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb



router = Router()

class Data(StatesGroup):
    date = State()
    amount = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет {message.from_user.first_name},', reply_markup=kb.btn_wastes)


@router.callback_query(F.data == 'wastes')
async def wastes(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите нужную категорию', reply_markup=kb.catalog)


@router.callback_query(F.data == 'meal')
async def meal(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Выберите нужную подкатегорию', reply_markup=kb.catalog_meal)

@router.callback_query(F.data.in_({'entertainments', 'transport', 'medicine', 'investment', 'home', 'other_expenses'}))
async def meal(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Ведите сумму')


@router.callback_query(F.data == 'amount')
async def amount(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(Data.amount)
    await callback.message.answer('Ведите сумму')


@router.message(Data.amount)
async def get_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(Data.date)
    await message.answer('Ведите дату (в формате XX.YY.ZZ)')


@router.message(Data.date)
async def get_date(message: Message, state):
    await state.update_data(date=message.text)
    data = await state.get_data()
    await message.answer(f'amount:{data["amount"]}\ndate:{data["date"]}')
    await state.clear()
