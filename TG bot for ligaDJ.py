from aiogram import Bot, Dispatcher, types, executor
import logging
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keydoards import keyboard_1
from sqllite import db_start, create_profile, edit_profile


async def on_startup(_):
    await db_start()


storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token, parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=storage)


class ProfileStatesGroup(StatesGroup):
    name = State()
    age = State()
    dj_name = State()
    id_vk = State()
    id_inst = State()
    gender = State()
    city = State()
    linc_mix = State()
    linc_logo = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer('Привет. Это бот Лиги Диджеев. Я принимаю заявки на 8 сезон.  '
                         'Если ты меня запустил, значит ты хочешь попасть на проект. И я очень рад этому.'
                         'Заранее подготовь ссылку на свой промоматериал для заявки '
                         '(видео или аудиомикс длительностью НЕ БОЛЕЕ 5 мин) и ссылку на логотип (если он у тебя имеется).'
                         'Как будешь готов, нажми кнопку "Создать"',
                         reply_markup=keyboard_1)
    await create_profile(user_id=message.from_user.id)


@dp.message_handler(Text(equals=['Создать']))
async def get_name(message: types.Message):
    await message.answer('Для начала напиши мне свои Имя и Фамилию.')
    await ProfileStatesGroup.name.set()


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.name)
async def get_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Укажи сколько тебе полных лет <b>(цифрами)</b>')
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit(), state=ProfileStatesGroup.age)
async def check_age(message: types.Message):
    await message.answer('Усп, что-то не то. Давай еще раз, укажи полных(без точек и запятых) лет цифрами')


@dp.message_handler(state=ProfileStatesGroup.age)
async def get_age(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer('DJ никнейм')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.dj_name)
async def get_dj_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['dj_name'] = message.text
    await message.answer('Как тебя найти Вконтакте?')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.id_vk)
async def get_id_vk(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['id_vk'] = message.text
    await message.answer('А в Instagram?')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.id_inst)
async def get_id_inst(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['id_inst'] = message.text
    await message.answer('Укажи свой пол: М или Ж?')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.gender)
async def get_gender(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await message.answer('В каком городе ты живешь?')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup. city)
async def get_city(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await message.answer('Скинь ссылку на свой промоматериал для заявки:')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.linc_mix)
async def get_linc_mix(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['linc_mix'] = message.text
    await message.answer('Отправь мне ссылку на свой логотип (если нет логотипа, то напиши «нет»)')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.linc_logo)
async def get_linc_logo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['linc_logo'] = message.text

    await edit_profile(state, user_id=message.from_user.id)
    await message.answer('Твоя заявка успешно создана. '
                         'Мы ее обязательно рассмотрим и если все ок, то обязательно с тобой свяжемся.'
                         'Подписывайся на страницы проекта Лига Диджеев в социальных сетях. '
                         'Мы везде  @ligadeejays (ВКонтакте, Телеграм, Инстаграм, YouTube).')
    await state.finish()
    print(data)   #удалить на релизе нужен для тестов

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
