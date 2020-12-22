from django.http import HttpResponse
from django.template import loader
from config.firebase_cfg import DATABASE, request_file


def index(request):
    template = loader.get_template("index.html")

    context = {
        "top_players_data": DATABASE.get().val()["TOP_PLAYERS"]["data"],
    }
    
    for user in context["top_players_data"]:
        user: dict
        user["raw_pp"] = f"{float(user['raw_pp']):.2f}"

    return HttpResponse(template.render(context, request))
