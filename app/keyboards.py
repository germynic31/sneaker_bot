from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# main kb for default users
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').insert('Корзина').add('Контакты')


# admin kb for administration
main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').insert('Корзина').add('Контакты').add('Админ-панель')


# admin panel for administration
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').insert('Удалить товар').add('Сделать рассылку').add('В главное меню')


# catalog list
catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(
    InlineKeyboardButton(text='Кроссовки', callback_data='sneakers'),
    InlineKeyboardButton(text='Футболки', callback_data='t-shirt'),
    InlineKeyboardButton(text='Штаны', callback_data='pants'),
)


# for add item
cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')
