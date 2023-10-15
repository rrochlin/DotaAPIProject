from configparser import ConfigParser
from DotaApiWrapper import DotaAPIWrapper
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import PIL
import logging

# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

class DotaAnalysisWrapper():
    def __init__(self, use_creds: bool=False):
        self.home = Path(__file__).parent.resolve()
        self.api = self.get_api(use_creds)

    def get_api(self, use_creds: bool) -> DotaAPIWrapper:
        config = ConfigParser()
        if use_creds:
            config.read(Path(self.home.parent.resolve(), "Web.config"))
            api_key = config["SECRETS"]["api_key"]
            return DotaAPIWrapper(api_key)
        return DotaAPIWrapper()

    def plot_matchups(self, hero_id: int, window: int=5) -> bool:
        try:
            heroes = self.api.heroes
            results = self.api.get_hero_matchups(hero_id=hero_id).json()
            lim = window+1
            xlim_games = max([res["games_played"] for res in results[:lim-1]])
            xlim_win_perc = max([res["wins"]/res["games_played"] for res in results[:lim-1]])
            fig = plt.figure(figsize=(5, 100*(lim/len(heroes))))
            s = "  Hero      Win Percentage          Matches       "
            title = plt.subplot2grid((lim,5), (0,0), colspan=5, fig=fig)
            title.text(0,0,s, fontsize=13)
            title.set_axis_off()
            for idx,res in enumerate(results[:lim-1]):
                file = Path(self.home,"assetts","images",f"{heroes[res['hero_id']]['localized_name']}.png")
                plot_img = plt.subplot2grid((lim,5), (idx+1,0), colspan=1, fig=fig)
                plot_img.imshow(np.asarray(PIL.Image.open(file)))
                plot_img.set_title(heroes[res['hero_id']]['localized_name'])
                plot_img.set_axis_off()
                matches_bar = plt.subplot2grid((lim,5), (idx+1,3), colspan=2, fig=fig)
                matches_bar.barh(0, res["games_played"], color=tableau20[6])
                matches_bar.barh(0, res["wins"], color=tableau20[7])
                matches_bar.set_xlim(xmax=xlim_games)
                matches_bar.set_title(f'{res["wins"]}/{res["games_played"]}')
                matches_bar.set_axis_off()
                win_perc_bar = plt.subplot2grid((lim,5), (idx+1,1), colspan=2, fig=fig)
                win_perc_bar.barh(0, res["wins"]/res["games_played"], color=tableau20[4])
                win_perc_bar.set_xlim(xmax=xlim_win_perc)
                win_perc_bar.set_title(f'{1/res["games_played"]*res["wins"]:.2%}')
                win_perc_bar.set_axis_off()
            plt.tight_layout()
            plt.savefig(Path(self.home,"assetts","graphs",f"{heroes[hero_id]['localized_name']}Matchups.png"))
            return True
        except Exception as e:
            logging.error(e)
            return False
