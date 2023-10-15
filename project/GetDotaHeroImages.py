from requests import get
from configparser import ConfigParser
from DotaApiWrapper import DotaAPIWrapper
from shutil import copyfileobj
import multiprocessing as mp
from pathlib import Path
from itertools import repeat


def get_hero_info(home: Path) -> list:
    config = ConfigParser()
    config.read(Path(home, "Web.config"))
    config["SECRETS"]["api_key"]
    api = DotaAPIWrapper(config["SECRETS"]["api_key"])
    return api.get_hero_stats().json()

def download_image(info: dict, home: Path) -> None:
    r = get(f"https://cdn.dota2.com/{info['img']}", stream=True)
    file = Path(home, f"project/assets/images/{info['localized_name']}.png")
    with open(file, "wb") as out_file:
        copyfileobj(r.raw, out_file)

def main():
    home = Path(__file__).parent.parent.resolve()
    hero_info = get_hero_info(home)
    with mp.Pool(mp.cpu_count()//2) as pool:
        pool.starmap(download_image, zip(hero_info, repeat(home)))

if __name__ == "__main__":
    main()
