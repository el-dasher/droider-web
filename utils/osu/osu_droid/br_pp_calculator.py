import pyttanko
import requests
from typing import Union

CALC_OSU_FILE_PATH = "resources/osu/calc.osu"
PARSER = pyttanko.parser()


def get_bpp(beatmap_id, mods: str = "NM", misses: int = 0, accuracy: float = 100.00, formatted: bool = False):
    """
    :param formatted: returns with 2 floats decimals if set to true
    :param accuracy: accuracy of the play
    :param misses: number of misses of the play
    :param mods: a string of the mods used e.g: DTHD
    :param beatmap_id: id of the beatmap you want to get br pp info
    :return: a dict: {raw_pp, aim_pp, speed_pp, acc_pp, acc_percent}
    """
    mods: Union[str, int] = mods.upper()
    beatmap_data: str = str(requests.get(f"https://osu.ppy.sh/osu/{beatmap_id}", allow_redirects=True
                                         ).content).replace("\\n", "\n").replace("\\r", "\r"
                                                                                 )[2:][:-2].replace("\n", "")

    with open(CALC_OSU_FILE_PATH, "w+") as recent_file:
        recent_file.write(beatmap_data)
        recent_file.close()

    beatmap: pyttanko.beatmap = PARSER.map(open(CALC_OSU_FILE_PATH))

    beatmap.od = beatmap.od - 4
    beatmap.cs = beatmap.cs - 4

    if "PR" in mods:
        beatmap.od = beatmap.od + 4
    if "SC" in mods:
        beatmap.cs = beatmap.cs + 4
    if "REZ" in mods:
        beatmap.ar -= 0.5
        beatmap.cs -= 1
        beatmap.od = beatmap.od / 2
        beatmap.hp = beatmap.hp / 2

    mods: int = pyttanko.mods_from_str(mods)

    beatmap.nobjects = beatmap.ncircles + beatmap.nspinners + beatmap.nsliders

    stars = pyttanko.diff_calc().calc(beatmap)

    accuracy = pyttanko.acc_round(accuracy, beatmap.nobjects, misses)

    n300 = accuracy[0]
    n100 = accuracy[1]
    n50 = accuracy[2]

    raw_pp, aim_pp, speed_pp, acc_pp, acc_percent = pyttanko.ppv2(
        stars.aim, stars.speed, bmap=beatmap, mods=mods, nmiss=misses, n300=n300, n100=n100, n50=n50)

    raw_pp -= aim_pp
    raw_pp -= speed_pp

    aim_pp = aim_pp ** 0.9
    speed_pp = speed_pp ** 0.9

    raw_pp += aim_pp
    raw_pp += speed_pp

    if not formatted:
        return {
            "raw_pp": f"{raw_pp}",
            "aim_pp": f"{aim_pp}",
            "speed_pp": f"{speed_pp}",
            "acc_pp": f"{acc_pp}",
            "acc_percent": f"{acc_percent}"
        }
    else:
        return {
            "raw_pp": f"{raw_pp: .2f}",
            "aim_pp": f"{aim_pp: .2f}",
            "speed_pp": f"{speed_pp: .2f}",
            "acc_pp": f"{acc_pp: .2f}",
            "acc_percent": f"{acc_percent: .2f}"
        }
