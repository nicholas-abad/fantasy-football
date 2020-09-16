"""Run the gather_tweets.py script for all players in a given dataframe.
"""

import argparse
import subprocess

from tqdm import tqdm
import pandas as pd

parser = argparse.ArgumentParser(description="Run the entire data scraper for all players.")
parser.add_argument(
    "--path_to_dataset",
    action="store",
    dest="path_to_dataset",
    required=False,
    help="Path to the dataset that contains all of the player names. The player names must be in the column 'player_names'.",
    default="/home/nick/fantasy-football/data/2020_espn_draft_results.csv",
)

parser.add_argument(
    "--output_dir",
    action="store",
    dest="output_dir",
    required=False,
    help="The output directory where you want to save all of the csv files. Default: './output/'",
    default="./output/",
)

args = parser.parse_args()
path_to_dataset = args.path_to_dataset
output_dir = args.output_dir

def main(path_to_dataset, output_dir):
    column_name_of_all_players = "player_names"
    data = pd.read_csv(path_to_dataset, index_col=0)
    names_of_players = list(data["player_names"])

    # Execute gather_tweets.py for every player.
    for player in tqdm(names_of_players):
        subprocess.run(["python", "gather_tweets.py", "--search_term", f"{player}", "--output_dir", f"{output_dir}"])


if __name__ == "__main__":
    main(path_to_dataset, output_dir)
