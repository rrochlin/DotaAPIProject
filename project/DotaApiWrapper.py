from requests import get
from time import sleep

API_BASE = r"https://api.opendota.com/api/{}?api_key={}"

def fetch_response(request):
    for _ in range(3):
        response = get(request)
        if (response.status_code == 200):
            return response
        sleep(1)
    raise Exception("api call failed")

class DotaAPIWrapper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def get_player(self, player_id):
        return fetch_response(API_BASE.format(f"players/{player_id}", self.api_key))
    
    def get_heroes(self):
        return fetch_response(API_BASE.format(f"heroes", self.api_key))
    
    def get_hero_stats(self):
        return fetch_response(API_BASE.format(f"heroStats", self.api_key))
    
    def get_constants(self):
        return fetch_response(API_BASE.format(f"constants", self.api_key))

    def get_hero_matchups(self, hero_id:int):
        return fetch_response(API_BASE.format(f"heroes/{hero_id}/matchups", self.api_key))

    def get_hero_items(self, hero_id:int):
        return fetch_response(API_BASE.format(f"heroes/{hero_id}/itemPopularity", self.api_key))