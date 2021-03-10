import os
from pathlib import Path

from environs import Env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = Env()
Env.read_env()

IGNORED_EXTENSIONS = ["pdf", "jpg", "jpeg", "png"]
OUTPUT_DIR = env.str("OUTPUT_DIR")
Path(OUTPUT_DIR).mkdir(exist_ok=True)

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    )
}
