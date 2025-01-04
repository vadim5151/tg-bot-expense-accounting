from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



btn_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Внести траты', callback_data='wastes')],
    [InlineKeyboardButton(text='Создать гугл таблицу', callback_data='create_google_sheets')]
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