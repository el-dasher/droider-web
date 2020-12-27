from django.http import HttpResponse
from django.template import loader
from config.firebase_cfg import DATABASE
from utils.osu.osu_droid.droid_data_getter import get_droid_data
from utils.osu.osu_std.pp_calculator import get_ppv2
from utils.osu.osu_droid.br_pp_calculator import get_bpp


def format_pp(user_data):
    for user in user_data:
        user: dict
        user["raw_pp"] = f"{float(user['raw_pp']):.2f}"

    return user_data


def board(request):
    template = loader.get_template("leaderboard/index.html")

    context = {
        "top_players_data": DATABASE.get().val()["TOP_PLAYERS"]["data"],
    }

    format_pp(context["top_players_data"])

    return HttpResponse(template.render(context, request))


async def user_page(request, user_id):
    template = loader.get_template("userpage/index.html")

    context: dict = dict(
        user_data=(await get_droid_data(user_id))["user_data"]
    )

    try:
        context["user_data"]["raw_pp"] = f'{context["user_data"]["raw_pp"]:.2f}'
    except TypeError:
        pass

    return HttpResponse(template.render(context, request))


def calculate(request):
    template = loader.get_template("osu_calc/index.html")
    params = request.GET

    map_id, mods, misses, accuracy, combo = "", "NM", 0, 100, None

    if len(params) >= 1:
        try:
            map_id = params["map_id"].split("/")[-1]
            mods: str = params["mods"]
            try:
                accuracy = float(params["acc"])
            except (KeyError, ValueError):
                pass
            try:
                combo = int(float((params["combo"])))
            except (KeyError, ValueError):
                pass
        except KeyError:
            try:
                map_id = params["map_id"].split("/")[-1]
            except KeyError:
                return HttpResponse("O id ou link do mapa não foi informado!")
        finally:
            # noinspection PyBroadException
            try:
                context = {
                    "pp_data": [
                        {
                            "name": "ppv2",
                            "calculated": get_ppv2(map_id, mods, misses, accuracy, combo, formatted=True)
                        },
                        {
                            "name": "bpp",
                            "calculated": get_bpp(map_id, mods, misses, accuracy, combo, formatted=True)
                        }
                    ]
                }
            except Exception:
                return HttpResponse(f"{map_id} é um link ou id ínvalido")
    else:
        context = {}

    return HttpResponse(template.render(context, request))


def invite(request):
    template = loader.get_template("invite/index.html")

    return HttpResponse(template.render({}, request))
