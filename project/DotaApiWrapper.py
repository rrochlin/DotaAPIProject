from requests import get, Response
from time import sleep
from pickle import dump, load
from os import getcwd
from pathlib import Path

API_BASE = r"https://api.opendota.com/api/{}{}"

def fetch_response(request) -> Response:
    for _ in range(3):
        response = get(request)
        if (response.status_code == 200):
            return response
        sleep(1)
    raise Exception("api call failed")

class DotaAPIWrapper:
    def __init__(self, api_key: str=None, refresh_heroes: bool=False):
        self.api_key = r"api_key={}".format(api_key) if api_key else ""
        self.heroes = self.get_heroes(refresh_heroes)
        
    def get_player(self, player_id) -> Response:
        return fetch_response(API_BASE.format(f"players/{player_id}", self.api_key))
    
    def get_heroes(self, refresh=False) -> dict():
        file_path = Path(getcwd(),"assetts","static_objects","heroes.pkl").resolve()
        if refresh or not Path.exists(file_path):
            heroes = fetch_response(API_BASE.format(f"heroes", self.api_key))
            with open(file_path, "wb") as file:
                dump({hero["id"]:hero for hero in heroes.json()}, file=file)
        with open(file_path, "rb") as file:
            return load(file=file)
    
    def get_hero_stats(self) -> Response:
        return fetch_response(API_BASE.format(f"heroStats", self.api_key))
    
    def get_constants(self) -> Response:
        return fetch_response(API_BASE.format(f"constants", self.api_key))

    def get_hero_matchups(self, hero_id:int) -> Response:
        return fetch_response(API_BASE.format(f"heroes/{hero_id}/matchups", self.api_key))

    def get_hero_items(self, hero_id:int) -> Response:
        return fetch_response(API_BASE.format(f"heroes/{hero_id}/itemPopularity", self.api_key))