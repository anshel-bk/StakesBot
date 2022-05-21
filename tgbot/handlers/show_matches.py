import emoji

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from tgbot.keyboards.reply import get_keyboard_choice_site_matches
from tgbot.services.get_matches import get_matches_wasd, get_matches_dotaix


async def site_choice(message: types.Message):
    keyboard = get_keyboard_choice_site_matches()
    text = f"Выберите сайт с которого хотите посмотреть информацию о матчах"
    await message.answer(text, reply_markup=keyboard)
    await OrderMatches.waiting_for_site_name.set()


async def show_info_about_matches_wasd(message: types.Message, state: FSMContext):
    info = get_matches_wasd()
    result_text = []
    for key,value in info.items():
        result_text.append(f"{key} {value}")
    await message.answer("\n".join(result_text))


async def show_info_about_matches_dotaix(message: types.Message, state: FSMContext):
    info = get_matches_dotaix()
    result_text = []
    for key,value in info.items():
        result_text.append(f"{key[0]} : {key[1]}\n{'  '*(len(key[0])-4)}{value[0][0]}% : {value[0][1]}%\n{'  '*(len(key[0])-4)}{value[1][0]}% : {value[1][1]}%")
    await message.answer("\n".join(result_text))


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Врзвращаемся к странице выбора команд бота", reply_markup=types.ReplyKeyboardRemove())


def show_matches(dp: Dispatcher):
    dp.register_message_handler(site_choice, commands="matches")
    dp.register_message_handler(show_info_about_matches_wasd, Text(equals="Сайт WASD", ignore_case=True),
                                state=OrderMatches.waiting_for_site_name)
    dp.register_message_handler(show_info_about_matches_dotaix, Text(equals="Сайт DOTAIX", ignore_case=True),
                                state=OrderMatches.waiting_for_site_name)
    dp.register_message_handler(cmd_cancel, Text(equals="Назад", ignore_case=True), state="*")


class OrderMatches(StatesGroup):
    waiting_for_site_name = State()
