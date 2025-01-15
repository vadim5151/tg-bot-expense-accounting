from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from datetime import *
from aiogram.filters.callback_data import CallbackData

from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, get_user_locale
import time

from aiogram.types import CallbackQuery

from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

import app.keyboards as kb
from google_sheets import *
import app.database.requests as rq
from app.database.requests import *



router = Router()


class Data(StatesGroup):
    name_new_category = State()
    tg_id = State()
    title = State()
    id_google_sheets = State()
    date = State()
    category = State()
    amount = State()



@router.message(CommandStart())
async def cmd_start(message: Message):
    # await delete((await get_data_google_sheets()).id_google_sheets)
    await rq.set_user(message.from_user.id)

    if await get_categories(message.from_user.id) == []:
        for i in ['Развлечение', 'Еда', 'Транспорт', 'Медецина', 'Инвестиции', 'Дом', 'Прочие расходы']:
            await rq.set_category(i, message.from_user.id)
   
    await message.answer('Здравствуйте! Я — бот по учёту расходов', reply_markup=kb.btn_main)
    await message.answer('Для начала работы необходимо создать гугл-таблицу, куда будут записываться ваши расходы', reply_markup=kb.btn_create_google_sheets)


@router.callback_query(F.data == 'set_wastes')
async def wastes(callback: CallbackQuery):
    await callback.answer('')

    tg_id = callback.from_user.id

    if tg_id not in sorted(await get_tg_id_from_google_sheets()):
        await callback.message.answer('У вас нет гугл таблицы', reply_markup=kb.btn_create_google_sheets)

    else:
        await callback.message.answer('Выберите нужную категорию', reply_markup=await kb.catalog(await get_categories(callback.from_user.id)))


@router.callback_query(F.data == 'meal')
async def meal(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Выберите нужную подкатегорию', reply_markup=kb.catalog_meal)


# @router.message(Data.date)
# async def show_calendar(message: Message):
#     calendar = SimpleCalendar(locale=await get_user_locale(message.from_user))
#     calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
#     await message.answer('Выберите дату',reply_markup=await calendar.start_calendar())
    


@router.callback_query(SimpleCalendarCallback.filter(), Data.date)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(locale=await get_user_locale(callback_query.from_user), show_alerts=True)
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date=date.strftime("%d.%m.%Y"))
        await callback_query.message.edit_text(f"Вы выбрали {date.strftime("%d.%m.%Y")}")

    await callback_query.message.answer('Подождите, данные добавляются')
        
    data = await state.get_data()
    tg_id = data['tg_id']
    print((await filter_name_google_sheets(tg_id)))
    # print((await get_info_google_sheets()).user_tg_id)
    # print((GoogleSheets).filter((GoogleSheets.user_tg_id == tg_id)))
    # print(((await get_info_google_sheets()).name_table).filter((await get_info_google_sheets()).user_tg_id == tg_id))

    await rq.set_data(data['date'], data['category'], data['amount'], tg_id)
    
    await update_table(
        (await filter_name_google_sheets(tg_id)),
        [data['date'], data['category'], f"{data['amount']}₽"])

    await callback_query.message.answer(f'Данные добавлены успешно\n {data["date"]} {data['category']} {data["amount"]}', reply_markup=kb.btn_cancel_data)

    await state.clear()

# async def get_amount(message: Message, state: FSMContext):
#     await state.update_data(amount=message.text)
#     await state.set_state(Data.date)
#     await message.answer(f'Введите дату ', reply_markup= await on_date_selected())
    

@router.message(Data.amount)
async def get_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(Data.date)

    await state.update_data(tg_id=message.from_user.id)

    calendar = SimpleCalendar(locale=await get_user_locale(message.from_user))
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    await message.answer('Выберите дату',reply_markup=await calendar.start_calendar())
# async def get_date(message: Message, state: FSMContext):
#     await state.update_data(date=message.text)

#     data = await state.get_data()

    # await rq.set_data(data['date'], data['category'], data['amount'], (await get_info_google_sheets()).user_tg_id)

    # update_table((await get_info_google_sheets()).name_table,[data['date'], data['category'], f"{data['amount']}₽"])

#     await message.answer(f'Данные добавлены успешно\n {data["date"]} {data['category']} {data["amount"]}', reply_markup=kb.btn_cancel)

#     await state.clear()


@router.callback_query(F.data.startswith('opt_'))
async def get_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')

    action = callback.data[4:]

    for i in await get_categories(callback.from_user.id):
        print(action)
        if action == i:
            await state.update_data(category=i) 

    await state.set_state(Data.amount)
    await callback.message.answer('Введите сумму')


@router.callback_query(F.data == 'create_google_sheets')
async def create_gooogle_sheets(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    tg_id = callback.from_user.id
    if tg_id in sorted(await get_tg_id_from_google_sheets()):
        await callback.message.answer(
            f'''У вас уже есть гугл таблица
            {await filter_name_google_sheets(tg_id)}.
              https://docs.google.com/spreadsheets/u/0/d/{await filter_id_google_sheets(tg_id)}''',
              reply_markup=kb.btn_set_wastes)

    else:
        await state.set_state(Data.title)
        await callback.message.answer('Как хотите назвать таблицу?')

   
@router.message(Data.title)
async def get_date(message: Message, state: FSMContext):
    await message.answer('Секунду... Таблица создается')
    await state.update_data(title=message.text)

    data = await state.get_data()

    title = data['title']
    id_google_sheets = await create_table(title)

    await state.update_data(id_google_sheets=id_google_sheets)
   
    await rq.set_data_google_sheets(data['title'], id_google_sheets, message.from_user.id)

    await update_table(title,['Дата', 'Категория', 'Сумма'])
    # create_worksheet(title)
    await message.answer(f'Таблица успешна создана✅\nCсылка на таблицу: https://docs.google.com/spreadsheets/u/0/d/{id_google_sheets}')
    await message.answer('Теперь можно внести первые расходы', reply_markup=kb.btn_set_wastes)


@router.callback_query(F.data == 'cancel_data')
async def cancel(callback: CallbackQuery):
    await callback.answer('')

    tg_id = callback.from_user.id

    await callback.message.edit_text('Подождите, данные удаляются')

    last_filled_row_index, last_row_data = await find_last_row(await filter_name_google_sheets(tg_id))

    await delete_value_data(tg_id)

    await callback.message.edit_text(f'Данные удалены\n{last_row_data[0]} {last_row_data[1]} {last_row_data[2]}')

    await delete_data_sheet(await filter_name_google_sheets(tg_id), last_filled_row_index)


@router.message(F.text == 'Внести траты')
async def wastes(message: Message):
    tg_id = message.from_user.id

    all_title_worksheets = await get_title_worksheet(await filter_name_google_sheets(tg_id))

    current_month_year = datetime.now().strftime("%B-%Y")

    if current_month_year not in all_title_worksheets:
        await create_worksheet(await filter_name_google_sheets(tg_id))
    
    if tg_id not in sorted(await get_tg_id_from_google_sheets()):
        await message.answer('У вас нет гугл таблицы', reply_markup=kb.btn_create_google_sheets)

    else:
        await message.answer('Выберите нужную категорию', reply_markup=await kb.catalog(await get_categories(message.from_user.id)))


@router.message(F.text == 'Получить ссылку на таблицу')
async def get_link_google_sheets(message: Message):
    tg_id = message.from_user.id

    await message.answer(f'Ваша ссылка на таблицу: https://docs.google.com/spreadsheets/u/0/d/{await filter_id_google_sheets(tg_id)}')


@router.message(F.text == 'Получить сведения')
async def get_diagram(message: Message):
    tg_id = message.from_user.id

    current_month_year = datetime.now().strftime("%B-%Y") 

    title = await filter_name_google_sheets(tg_id)

    last_filled_row_index, last_row_data = await find_last_row(title)

    all_values = await get_values(await filter_name_google_sheets(tg_id), last_filled_row_index)

    await message.answer(f'Ваши траты в {current_month_year}:\n{all_values}')


@router.message(F.text == 'Конструктор')
async def konstruktor(message: Message):
    await message.answer(f'Что вы хотите сделать:', reply_markup=kb.btn_konstruktor)


@router.callback_query(F.data == 'add_new_category')
async def add_new_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')

    await state.set_state(Data.name_new_category)
    await callback.message.answer('Как хотите назвать новую категорию')


@router.message(Data.name_new_category)
async def add_new_categor(message: Message, state: FSMContext):
    await state.update_data(name_new_category=message.text)

    data = await state.get_data()
    
    if data['name_new_category'] not in await get_categories(message.from_user.id):
        await rq.set_category(
            data['name_new_category'][0].upper()+data['name_new_category'][1:],
            message.from_user.id)
        
        await message.answer('Категория успешно добавлена', reply_markup= kb.btn_cancel_category)

    else:
        await message.answer('Такая категория уже существует')

    await state.clear()


@router.message(F.data == 'cancel_category')
async def cancel(callback: CallbackQuery):
    await callback.answer('')

    await callback.message.edit_text('Подождите, категория удаляется')

    await delete_category(callback.from_user.id)

    await callback.message.edit_text('Категория удалена')


