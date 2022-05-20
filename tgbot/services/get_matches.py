import time
from typing import Dict, Tuple, Any

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
forecast_not_ready_plug = "Прогноз пока не готов"


def get_soup(url):
    print(url)
    request = requests.get(url, headers=HEADERS)
    source = request.text
    soup = BeautifulSoup(source, "lxml")
    return soup


def get_matches_wasd(url: str = URL_WASD) -> dict:
    soup = get_soup(url)
    wasd_info = {}
    teams = soup.find_all("div", class_="teams")
    for team in teams:
        try:
            tag_success_team = team.find("div", class_="team-percent-success")
            tag_sucking_team = team.find("div", class_="team-percent-danger")
            percent_success_team = tag_success_team.text.strip()
            percent_sucking_team = tag_sucking_team.text.strip()
            name_success_team = tag_success_team.find_next(class_="white mt-2").text.strip()
            name_sucking_team = tag_sucking_team.find_next(class_="white mt-2").text.strip()
            if int(percent_success_team.split(".")[0]) > win_percent_wasd:
                wasd_info[tuple([name_success_team, name_sucking_team])] = tuple(
                    [percent_success_team, percent_sucking_team])
        except AttributeError:
            continue
    return wasd_info


def get_matches_dotaix(url: str = URL_DOTAIX) -> str | dict[tuple[Any, ...], tuple[Any, ...]]:
    dotaix_info = {}
    request = requests.get(url, headers=HEADERS)
    json_info = request.text
    json_info = json.loads(json_info)
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


print(get_matches_dotaix(URL_DOTAIX))