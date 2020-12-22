from django.http import HttpResponse
from django.template import loader
from config.firebase_cfg import DATABASE


def format_pp(user_data):
    for user in user_data:
        user: dict
        user["raw_pp"] = f"{float(user['raw_pp']):.2f}"

    return user_data


def index(request):
    template = loader.get_template("leaderboard/index.html")

    context = {
        "top_players_data": DATABASE.get().val()["TOP_PLAYERS"]["data"],
    }

    format_pp(context["top_players_data"])

    return HttpResponse(template.render(context, request))


def user_page(request, user_id):
    template = loader.get_template("userpage/index.html")

    context = {
        "user_data": list(filter(lambda e: e["user_id"] == user_id, DATABASE.get().val()["TOP_PLAYERS"]["data"]))[0],
    }
    context["user_data"]["raw_pp"] = f"{context['user_data']['raw_pp']:.2f}"
    
    return HttpResponse(template.render(context, request))
