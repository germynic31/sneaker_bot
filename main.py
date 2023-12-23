import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from keyboards import main, main_admin, admin_panel, catalog_list


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # await message.answer_sticker('CAACAgIAAxkBAAMOZYYcUZBhkksvbXgBfEucDBgOViIAArlAAAKbGRhI_vHRR7mXpkQzBA')
    await message.answer(
        f'{message.from_user.first_name}, добро пожаловать в магазин кроссовок!',
        reply_markup=main
    )
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(
            f'Вы авторизовались как администратор',
            reply_markup=main_admin
        )


@dp.message_handler(commands=['id'])
async def answer(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer(f'Каталог пуст!', reply_markup=catalog_list)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста!')


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Покупать товар у него {os.getenv("ADMIN_USERNAME")}')


@dp.message_handler(text='Админ-панель')
async def open_admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ панель', reply_markup=admin_panel)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')


if __name__ == '__main__':
    executor.start_polling(dp)
