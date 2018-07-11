import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import fpl_scraper

def main():
    fpl = fpl_scraper.FPLScraper()

    big_dict = fpl.create_player_dict()
    player_stats_df = fpl.create_df_from_dict(big_dict)
    player_info_dict = fpl.create_player_info_dict()

    player_stats_df.unstack(level=0).plot()

    for idx in player_stats_df.index.levels[0]:
        pass
        #print player_info_dict[idx]["name"] + " " + str(player_stats_df.loc[(idx, "points")].corr(player_stats_df.loc[(idx, "ict")]))


if __name__ == '__main__':
    main()
