from aiogram import types


def get_keyboard_choice_site_matches():
    keyboard_choice_site_matches = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Информация на сайте WASD", "Информация на сайте DOTAIX"]
    keyboard_choice_site_matches.add(*buttons)
    return keyboard_choice_site_matches
