from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



btn_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать гугл таблицу', callback_data='create_google_sheets')],
    [InlineKeyboardButton(text='Получить ссылку на таблицу', callback_data='get_link_google_sheets')],
    [InlineKeyboardButton(text='Внести траты', callback_data='set_wastes')],
    [InlineKeyboardButton(text='Изменить название таблицы', callback_data='change_name_table')]
])


btn_create_google_sheets = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать гугл таблицу', callback_data='create_google_sheets')]
])


btn_set_wastes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Внести траты', callback_data='set_wastes')]
])


btn_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить', callback_data='cancel')]
])


catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Еда', callback_data='meal')],
    [InlineKeyboardButton(text='Развлечения', callback_data='opt_entertainments')],
    [InlineKeyboardButton(text='Транспорт', callback_data='opt_transport')],
    [InlineKeyboardButton(text='Медецина', callback_data='opt_medicine')],
    [InlineKeyboardButton(text='Инвестиции', callback_data='opt_investment')],
    [InlineKeyboardButton(text='Дом', callback_data='opt_home')],
    [InlineKeyboardButton(text='Прочие расходы', callback_data='opt_other_expenses')]
])



catalog_meal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продукты', callback_data='opt_products')],
    [InlineKeyboardButton(text='Фастфуд', callback_data='opt_fastfood')],
    [InlineKeyboardButton(text='Сладкое', callback_data='opt_dessert')],
])


btn_dalete = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Удалить гугл таблицу', callback_data='delete_google_sheets')]
])