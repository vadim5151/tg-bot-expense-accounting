from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



btn_wastes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Траты', callback_data='wastes')]
])

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Еда', callback_data='meal')],
    [InlineKeyboardButton(text='Развлечения', callback_data='entertainments')],
    [InlineKeyboardButton(text='Транспорт', callback_data='transport')],
    [InlineKeyboardButton(text='Медецина', callback_data='medicine')],
    [InlineKeyboardButton(text='Инвестиции', callback_data='investment')],
    [InlineKeyboardButton(text='Дом', callback_data='home')],
    [InlineKeyboardButton(text='Прочие расходы', callback_data='other_expenses')]
])


catalog_meal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продукты', callback_data='amount')],
    [InlineKeyboardButton(text='Фастфуд', callback_data='amount')],
    [InlineKeyboardButton(text='Сладкое', callback_data='amount')],
])