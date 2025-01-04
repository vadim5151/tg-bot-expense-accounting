from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from google_sheets import *



router = Router()


title = ''

class Title(StatesGroup):
    title = State()


class Data(StatesGroup):
    date = State()
    category = State()
    amount = State()



@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, что вы хотите?', reply_markup=kb.btn_main)


@router.callback_query(F.data == 'wastes')
async def wastes(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Выберите нужную категорию', reply_markup=kb.catalog)


@router.callback_query(F.data == 'meal')
async def meal(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Выберите нужную подкатегорию', reply_markup=kb.catalog_meal)


@router.message(Data.amount)
async def get_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(Data.date)
    await message.answer('Введите дату (в формате XX.YY.ZZ)')
    

@router.message(Data.date)
async def get_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)

    # await state.clear()
    data = await state.get_data()
    print(data)
    print(title)

    update_table(title, [data['date'], data['category'], data['amount']])

    await message.answer(f'amount:{data["amount"]}\ndate:{data["date"]}\ncategory:{data['category']}\ntitle:{title}')


@router.callback_query(F.data.startswith('opt_'))
async def get_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    action = callback.data[4:]

    all_category = {
        'entertainments':'Развлечение',
        'transport':'Транспорт',
        'medicine':'Медецина',
        'investment':'Инвестиции',
        'home':'Дом',                 
        'other_expenses':'Прочие расходы',                 
        'dessert':'Сладкое',
        'fastfood':'Фастфуд',
        'products':'Продукты',
    }

    for i in all_category.keys():
        if action == i:
            await state.update_data(category=all_category[i]) 

    await state.set_state(Data.amount)
    await callback.message.answer('Введите сумму')


@router.callback_query(F.data == 'create_google_sheets')
async def create_gooogle_sheets(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(Title.title)
    await callback.message.answer('Как хотите назвать таблицу?')

   
@router.message(Title.title)
async def get_date(message: Message, state: FSMContext):
    global title

    await message.answer('Секунду...')
    await state.update_data(title=message.text)

    data = await state.get_data()
    title = data['title']

    link_google_sheets = create_table(title)

    update_table(title,['Дата', 'Категория', 'Сумма'])

    await message.answer(f'Таблица успешна создана✅\nCсылка на таблицу: {link_google_sheets}')




