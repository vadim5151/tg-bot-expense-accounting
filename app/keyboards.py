from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder



btn_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Внести траты'), KeyboardButton(text='Получить ссылку на таблицу')],
    [KeyboardButton(text='Получить сведения'), KeyboardButton(text='Конструктор')]
],
                        resize_keyboard=True)


btn_create_google_sheets = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать гугл таблицу', callback_data='create_google_sheets')]
])


btn_set_wastes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Внести траты', callback_data='set_wastes')]
])


btn_cancel_data = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить', callback_data='cancel_data')]
])


btn_cancel_category = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить', callback_data='cancel_category')]
])
# catalog = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Еда', callback_data='meal')],
#     [InlineKeyboardButton(text='Развлечения', callback_data='opt_entertainments')],
#     [InlineKeyboardButton(text='Транспорт', callback_data='opt_transport')],
#     [InlineKeyboardButton(text='Медецина', callback_data='opt_medicine')],
#     [InlineKeyboardButton(text='Инвестиции', callback_data='opt_investment')],
#     [InlineKeyboardButton(text='Дом', callback_data='opt_home')],
#     [InlineKeyboardButton(text='Прочие расходы', callback_data='opt_other_expenses')]
# ])



catalog_meal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продукты', callback_data='opt_products')],
    [InlineKeyboardButton(text='Фастфуд', callback_data='opt_fastfood')],
    [InlineKeyboardButton(text='Сладкое', callback_data='opt_dessert')],
])


btn_dalete = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Удалить гугл таблицу', callback_data='delete_google_sheets')]
])


btn_konstruktor = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить новую категорию', callback_data='add_new_category')],
    [InlineKeyboardButton(text='Удалить категорию', callback_data='delete_category')],
    [InlineKeyboardButton(text='Переиминовать таблицу', callback_data='rename_table')],
    [InlineKeyboardButton(text='Удалить расходы', callback_data='delete_wastes')]
])


async def catalog(all_category):
    keyboard = InlineKeyboardBuilder()

    
    for category in all_category:
        keyboard.add(InlineKeyboardButton(text=category, callback_data=f'opt_{category}'))

    return keyboard.adjust(1).as_markup()


btn_delete_email=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Удалить почту', callback_data='delete_email')]
])

# async def get_all_category(all_category):
#     keyboard = InlineKeyboardBuilder()

#     for category in all_category:
#         keyboard.add(InlineKeyboardButton(text=category, callback_data=f'opt_{category}'))

    # return keyboard.adjust(1).as_markup()