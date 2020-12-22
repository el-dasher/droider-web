from django.http import HttpResponse
from django.template import loader
from config.firebase_cfg import DATABASE, request_file


def index(request):
    template = loader.get_template("index.html")

    context = {
        "top_players_data": DATABASE.get().val()["TOP_PLAYERS"]["data"],
        "br_rank_css": request_file("br_rank.css"),
        "background_image": "https://media.gettyimages.com/videos/"
                            "fast-speed-line-loop-from-middle-to-the-outside-anime-motion-4k-video-"
                            "id1277595267?s=640x640"
    }

    for user in context["top_players_data"]:
        user: dict
        user["raw_pp"] = f"{float(user['raw_pp']):.2f}"

    return HttpResponse(template.render(context, request))
