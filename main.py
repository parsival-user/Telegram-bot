from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app import keyboard as kb
from app import database as db 
from dotenv import load_dotenv
import os

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print('Bot muvaffaqiyatli ishga tushurildi!')


class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAMpZY1KfgP5nIeCLAxS_W2ykoBNobAAAiAAA1m7_CWFipaaCE3JfTME')
    await message.answer(f"{message.from_user.full_name}, do'konimizga hush kelibsiz!",
                         reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f"Siz admin sifatida avtorizatsiyadan o'tdingiz!", reply_markup=kb.main_admin)
    

@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text=["Katalog"])
async def catalog(message: types.Message):
    await message.answer("Kataloglar bilan tanishing!", reply_markup=kb.katalog_list)


@dp.message_handler(text=["Savat"])
async def cart(message: types.Message):
    await message.answer("Savat bo'sh!")


@dp.message_handler(text=["Kontakt"])
async def contacts(message: types.Message):
    await message.answer("Sotib olish uchun bog'laning: @jorik_turaev")


@dp.message_handler(text=["Admin-panel"])
async def admin(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Siz admin-panelga kirdingiz!", reply_markup=kb.admin_panel)
    else:
        await message.reply("Sizni tushunmadim!")


@dp.message_handler(text=["Tovar qoshish"])
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer("Tovar turini tanlang", reply_markup=kb.katalog_list)
    else:
        await message.reply("Sizni tushunmadim!")


@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Tovar nomini yozing!', reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Tovarga izoh yozing")
    await NewOrder.next()


@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer("Tovar narxini yozing")
    await NewOrder.next()


@dp.message_handler(state=NewOrder.price)
async def add_item_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer("Tovar rasmini jo'nating")
    await NewOrder.next()


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Bu rasm emas!')


@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer("Tovar muvaffaqiyatli qo'shildi!", reply_markup=kb.admin_panel)
    await state.finish()


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply("Sizni tushunmadim!")



@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 't-shirt':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Siz futbolkalarni tanladingiz!')
    elif callback_query.data == 'shorts':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Siz shortiklarni tanladingiz!')
    elif callback_query.data == 'sneakers':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Siz krossovkalarni tanladingiz!')


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)