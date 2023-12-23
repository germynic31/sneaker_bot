from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# main kb for default users
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')


# admin kb for administration
main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')


# admin panel for administration
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку')


catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(
    InlineKeyboardButton(text='Кроссовки', url='https://github.com/germynic31'),
    InlineKeyboardButton(text='Футболки', url='https://github.com/germynic31'),
    InlineKeyboardButton(text='Штаны', url='https://github.com/germynic31'),
)
