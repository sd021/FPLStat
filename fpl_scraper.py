import requests
import json
import yaml
import pandas as pd
import numpy as np

overview_url = "https://fantasy.premierleague.com/drf/bootstrap-static"
base_pinfo_url = "https://fantasy.premierleague.com/drf/element-summary/"
teams_url = "https://fantasy.premierleague.com/drf/teams/"

class FPLScraper(object):
    def __init__(self, *args):
        self.load_data()

    # Load some of the data into memory to reduce number of GET api calls
    def load_data(self):
        html=requests.get(teams_url).text
        self.teams_info=json.loads(html)

        html=requests.get(overview_url).text
        self.overview_info=json.loads(html)

    # Create a dictionary to relate team codes to team names
    def create_team_info_dict(self):
        team_dict = {}

        for team in self.teams_info:
            team_dict[team["code"]] = team["name"]
        return team_dict

    # Create a dictionary of static info on each player
    def create_player_info_dict(self):
        big_dict = {}

        for player_json in self.overview_info["elements"]:
            player_info_dict = {}
            player_name = (player_json['first_name'] + " " +
                        player_json['second_name']).encode('utf-8')

            team_dict = self.create_team_info_dict()

            player_info_dict["name"] = player_name
            player_info_dict["value"] = player_json['now_cost'] / 10
            player_info_dict["team"] = team_dict[player_json["team_code"]]
            player_info_dict["goals_scored"] = player_json['goals_scored']
            player_info_dict["goals_conceded"] = player_json['goals_conceded']
            player_info_dict["total_points"] = player_json['total_points']
            player_info_dict["form"] = player_json['form']
            player_info_dict["assists"] = player_json['assists']
            player_info_dict["selected_by_percent"] = player_json['selected_by_percent']
            player_info_dict["bonus"] = player_json['bonus']


            big_dict[player_json['id']] = player_info_dict

        return big_dict

    # Create a dictionary for of a given attribute across all gameweeks
    def create_player_stats_dict(self, player_id, attribute):
        html=requests.get(base_pinfo_url + player_id).text
        player_info_json=json.loads(html)

        ret_dict = {}
        for gw in player_info_json["history"]:
            round = gw["round"]
            ret_dict[round] = float(gw[attribute])
        return ret_dict

    def create_player_dict(self):
        big_dict = {}

        for idx, player in enumerate(self.overview_info["elements"]):
            player_dict = {}

            p_id = str(player['id'])

            player_dict["points"] = self.create_player_stats_dict(p_id, "total_points")
            player_dict["ict"] = self.create_player_stats_dict(p_id, "ict_index")

            big_dict[player['id']] = player_dict

            if idx > 10:
                break
        
        return big_dict

    def create_df_from_dict(self, in_dict):
        df = pd.DataFrame.from_dict({(i, j): in_dict[i][j]
                                        for i in in_dict.keys()
                                        for j in in_dict[i].keys()},
                                    orient='index')
    
        return df

def main():
    fpl_scraper = FPLScraper()
    
    big_dict = fpl_scraper.create_player_dict()
    player_stats_df = fpl_scraper.create_df_from_dict(big_dict)
    player_stats_df.to_csv("out.csv")

   # player_stats_df = pd.read_csv("out.csv", index_col=[0, 1], skipinitialspace=True)

    player_info_dict = fpl_scraper.create_player_info_dict()

    print player_stats_df.T

    for idx in player_stats_df.index.levels[0]:
        pass
        #print player_info_dict[idx]["name"] + " " + str(player_stats_df.loc[(idx, "points")].corr(player_stats_df.loc[(idx, "ict")]))

if __name__ == '__main__':
    main()
