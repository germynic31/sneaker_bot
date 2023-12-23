import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

from app import keyboards as kb, database as db

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startapp(_):
    await db.db_start()
    print('Бот успешно запустился!')


class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    # await message.answer_sticker('CAACAgIAAxkBAAMOZYYcUZBhkksvbXgBfEucDBgOViIAArlAAAKbGRhI_vHRR7mXpkQzBA')
    await message.answer(
        f'{message.from_user.first_name}, добро пожаловать в магазин кроссовок!',
        reply_markup=kb.main
    )
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(
            f'Вы авторизовались как администратор',
            reply_markup=kb.main_admin
        )


@dp.message_handler(commands=['id'])
async def answer(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer(f'Каталог пуст!', reply_markup=kb.catalog_list)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста!')


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Покупать товар у него {os.getenv("ADMIN_USERNAME")}')


@dp.message_handler(text='Админ-панель')
async def open_admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ панель', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer(f'Выберите тип товара', reply_markup=kb.catalog_list)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state:FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Напишите название товара', reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Напишите описание товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Напишите цену товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.price)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте фотографию товара')
    await NewOrder.next()


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Это не фотография')


@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer('Товар успешно создан', reply_markup=kb.admin_panel)
    await state.finish()


@dp.message_handler(text='Отмена')
async def cancel_kb(message: types.Message):
    await message.answer('Вы отменили создание товара', reply_markup=kb.admin_panel)


@dp.message_handler(text='В главное меню')
async def main_kb(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы перешли в главное меню', reply_markup=kb.main_admin)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')


@dp.callback_query_handler()
async def callback_query_keyboards(callback_query: types.CallbackQuery):
    if callback_query.data == 'sneakers':
        await bot.send_message(callback_query.from_user.id, text='Вы выбрали кроссовки')
    elif callback_query.data == 't-shirt':
        await bot.send_message(callback_query.from_user.id, text='Вы выбрали футболки')
    elif callback_query.data == 'pants':
        await bot.send_message(callback_query.from_user.id, text='Вы выбрали штаны')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startapp, skip_updates=True)
