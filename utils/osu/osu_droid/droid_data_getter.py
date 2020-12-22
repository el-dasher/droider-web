from abc import ABC
from datetime import datetime
from html.parser import HTMLParser
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

from config.setup import DPP_BOARD_API


# noinspection PyTypeChecker
async def get_droid_data(user_id):
    # noinspection PyGlobalUndefined

    old_data = []
    beatmap_data = []
    html_imgs = []

    user_url = f"http://ops.dgsrz.com/profile.php?uid={user_id}"
    droid_html = urlopen(user_url).read()
    droid_data_soup = BeautifulSoup(droid_html, features="html.parser")

    class DroidParser(HTMLParser, ABC):
        def handle_data(self, html_data):
            html_data = html_data.replace("\n", "").replace("\r", "").strip()
            if len(html_data) != 1 and html_data != "":
                # noinspection PyBroadException
                try:
                    if html_data[0] != "{" and html_data[-1] != "}":

                        html_data = html_data.strip().split("/")

                        old_data.append(html_data.copy())

                        if old_data[old_data.index(html_data) - 1][0] != html_data[0]:
                            beatmap_name = old_data[old_data.index(html_data) - 1][0]
                        else:
                            beatmap_name = None

                        html_data[0] = datetime.strptime(html_data[0].strip(), "%Y-%m-%d %H:%M:%S")
                        html_data.append(beatmap_name)

                        beatmap_data.append(html_data)

                except Exception:
                    pass

        def handle_starttag(self, tag, attrs):
            if tag == "img":
                html_imgs.append(attrs)

    droid_parser = DroidParser()
    droid_parser.feed(str(droid_data_soup))

    beatmap_dicts = {}

    dpp_board_url = f"http://droidppboard.herokuapp.com/api/getplayertop?key={DPP_BOARD_API}&uid={user_id}"
    dpp_user_data = None

    # noinspection PyBroadException
    try:
        dpp_user_data = requests.get(dpp_board_url).json()
    except Exception:
        raw_pp = "OFFLINE"
        pp_data = "OFFLINE"
    else:
        raw_pp = None
        pp_data = None

        # noinspection PyBroadException
        try:
            raw_pp = dpp_user_data["data"]["pp"]["total"]
            pp_data = dpp_user_data["data"]["pp"]["list"]
        except Exception:
            pass

    for i, data in enumerate(beatmap_data):
        beatmap_dicts[f"rs_{i}"] = {
            "username": old_data[26][0],
            "beatmap": data[5],
            "date": data[0],
            "score": data[1],
            "mods": data[2],
            "combo": int(data[3][:-2]),
            "accuracy": float(data[4][:-1])
        }

    try:
        user_data = dict(username=old_data[26][0], avatar_url=html_imgs[3][0][1], user_id=user_id,
                         country=old_data[27][0], raw_pp=raw_pp, pp_data=pp_data, total_score=old_data[-13][0],
                         overall_acc=float(old_data[-11][0][:-1]), playcount=int(old_data[-9][0]))
    except ValueError:
        user_data = dict(username=old_data[26][0], avatar_url=html_imgs[3][0][1], user_id=user_id,
                         country=old_data[27][0], raw_pp=raw_pp, pp_data=pp_data, all_pp_data=dpp_user_data,
                         total_score=old_data[-12][0], overall_acc=float(old_data[-10][0][:-1]), playcount="Erro!")

    data_dict = dict(user_data=user_data, beatmap_data=beatmap_dicts)

    """
    if pp_data != "offline":
        await save_droid_uid_data(user_id, user_data)
    """
    # return data_dicts

    return dict(data_dict)
