from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from google_sheets import *
import app.database.requests as rq
from app.database.requests import *


router = Router()


class Data(StatesGroup):
    title = State()
    id_google_sheets = State()
    date = State()
    category = State()
    amount = State()



@router.message(CommandStart())
async def cmd_start(message: Message):
    # await delete((await get_data_google_sheets()).id_google_sheets)
    await rq.set_user(message.from_user.id)
    await message.answer('Здравствуйте! Я — бот по учёту расходов')
    await message.answer('Для начала работы необходимо создать гугл-таблицу, куда будут записываться ваши расходы', reply_markup=kb.btn_create_google_sheets)


@router.callback_query(F.data == 'set_wastes')
async def wastes(callback: CallbackQuery):
    await callback.answer('')
    if (await get_info_google_sheets()) == None :
        await callback.message.answer('У вас нет гугл таблицы', reply_markup=kb.btn_main)
    else:
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

    data = await state.get_data()

    await rq.set_data(data['date'], data['category'], data['amount'], (await get_info_google_sheets()).user_tg_id)

    update_table((await get_info_google_sheets()).name_table,[data['date'], data['category'], f"{data['amount']}₽"])

    await message.answer(f'{data["date"]} {data['category']} {data["amount"]}')
    await message.answer('Данные добавлены успешно', reply_markup=kb.btn_cancel)

    await state.clear()


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
    
    if (await get_info_google_sheets()) != None:
        await callback.message.answer(f'У вас уже есть гугл таблица {(await get_info_google_sheets()).name_table}. https://docs.google.com/spreadsheets/u/0/d/{(await get_info_google_sheets()).id_google_sheets}', reply_markup=kb.btn_set_wastes)
    else:
        await state.set_state(Data.title)
        await callback.message.answer('Как хотите назвать таблицу?')

   
@router.message(Data.title)
async def get_date(message: Message, state: FSMContext):
    await message.answer('Секунду... Таблица создается')
    await state.update_data(title=message.text)

    data = await state.get_data()

    title = data['title']
    id_google_sheets = create_table(title)

    await state.update_data(id_google_sheets=id_google_sheets)
   
    await rq.set_data_google_sheets(data['title'], id_google_sheets, (await get_user_tg_id()).tg_id)

    update_table(title,['Дата', 'Категория', 'Сумма'])
    
    await message.answer(f'Таблица успешна создана✅\nCсылка на таблицу: https://docs.google.com/spreadsheets/u/0/d/{id_google_sheets}')
    await message.answer('Теперь можно внести первые расходы', reply_markup=kb.btn_set_wastes)


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery):
    await callback.answer('')

    last_filled_row_index, last_row_data = find_last_row((await get_info_google_sheets()).name_table)
    await callback.message.answer(f'Данные удалены\n{last_row_data[0]} {last_row_data[1]} {last_row_data[2]}')

    await delete_value()
    delete_data_sheet((await get_info_google_sheets()).name_table, last_filled_row_index)


    

# @router.callback_query(F.data == 'get_link_google_sheets')
# async def get_link_google_sheets(callback: CallbackQuery):
#     await callback.message.answer(f'Ссылка на вашу гугл таблицу {title}: {link_google_sheets}')


# @router.callback_query(F.data == 'change_name_table')
# async def change_name_table(callback: CallbackQuery):
#     await callback.message.answer('Напишите название новой таблицы')

