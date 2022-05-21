import time
from typing import Dict, Tuple, Any
import emoji
import requests
import bs4
from bs4 import BeautifulSoup
import json

URL_WASD = "https://wasdparty.com/"
URL_DOTAIX = "https://dotaix.xyz/api/matches?live=true"

HEADERS = {
    "Accept": "/*/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 "
                  "Safari/537.36",
}

win_percent_wasd = 52
win_percent_dotaix = 60
forecast_not_ready_plug = "Прогноз пока не готов, но выйдет в ближайшее время"

list_emoji = [":no_entry:", ":check_mark_button:"]


def get_soup(url):
    request = requests.get(url, headers=HEADERS)
    source = request.text
    soup = BeautifulSoup(source, "lxml")
    return soup


def get_matches_wasd(url: str = URL_WASD) -> dict | str:
    soup = get_soup(url)
    wasd_info = {}
    teams = soup.find_all("div", class_="teams")
    for team in teams:
        try:
            tag_success_team = team.find("div", class_="team-percent-success")
            tag_sucking_team = team.find("div", class_="team-percent-danger")
            percent_success_team = tag_success_team.text.strip()[:-2]
            percent_sucking_team = tag_sucking_team.text.strip()[:-2]
            name_success_team = tag_success_team.find_next(class_="white mt-2").text.strip()
            name_sucking_team = tag_sucking_team.find_next(class_="white mt-2").text.strip()
            if int(percent_success_team.split(".")[0]) > win_percent_wasd:
                wasd_info[tuple([name_success_team, name_sucking_team])] = tuple(
                    [percent_success_team, percent_sucking_team])
        except AttributeError:
            break
    return wasd_info if wasd_info else "На текущий момент прогнозов нет, воспользуйтесь ботом позже"


def get_matches_dotaix(url: str = URL_DOTAIX) -> str | dict[tuple[Any, ...], tuple[Any, ...]]:
    dotaix_info = {}
    request = requests.get(url, headers=HEADERS)
    json_info = request.text
    json_info = json.loads(json_info)
    if not json_info:
        return "На текущий момент прогнозов нет, воспользуйтесь ботом позже"
    for dict in json_info:
        pick_power = dict.get("percentage").get("pick_power", forecast_not_ready_plug)
        pick_team_power = dict.get("percentage").get("pick_power_team_based", forecast_not_ready_plug)
        radiant_team_name = dict.get("radiant_team", forecast_not_ready_plug)
        dire_team_name = dict.get("dire_team", forecast_not_ready_plug)
        check = f"{pick_power}*{pick_team_power}*{radiant_team_name}*{dire_team_name}"
        if any(map(lambda text: text == forecast_not_ready_plug, check.split("*"))):
            return forecast_not_ready_plug
        numbers_percentage = [num for num in pick_power] + [num for num in pick_team_power]
        if any(map(lambda num: num > win_percent_dotaix, numbers_percentage)):
            dotaix_info[tuple([radiant_team_name, dire_team_name])] = tuple([pick_power, pick_team_power])
    return dotaix_info if dotaix_info else "Нет подходящих матчей"


def text_formatting(info: dict, site: str):
    result_text = []
    if site == 'wasd':
        for key, value in info.items():
            result_text.append(
                f"{key[0]} : {key[1]}\n{value[0]}%{emoji.emojize(list_emoji[value[0] == max(value)])}{'-' * (len(key[0]) + len(key[1]) - 9)}{value[1]}%{emoji.emojize(list_emoji[value[1] == max(value)])}")
        return "\n\n".join(result_text)
    elif site == 'dotaix':
        for key, value in info.items():
            result_text.append(
                f"{key[0]} : {key[1]}\n{value[0][0]}%{emoji.emojize(list_emoji[value[0][0] == max(value[0])])}{'-' * (len(key[0]) + len(key[1]) - 6)}{value[0][1]}%{emoji.emojize(list_emoji[value[0][1] == max(value[0])])}\n{value[1][0]}%{emoji.emojize(list_emoji[value[1][0] == max(value[1])])}{'-' * (len(key[0]) + len(key[1]) - 6)}{value[1][1]}%{emoji.emojize(list_emoji[value[1][1] == max(value[1])])}")
        return "\n\n".join(result_text)
