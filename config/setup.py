from dotenv import load_dotenv
from pathlib import Path
from os import getenv

load_dotenv(Path(".") / ".env")

DJANGO_SECRET: str = getenv("DJANGO_SECRET")
DPP_BOARD_API: str = getenv("DPP_BOARD_API")
