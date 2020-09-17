import argparse

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

from tqdm import tqdm
from xgboost import XGBRegressor

parser = argparse.ArgumentParser(description="Get the MSE, MAE, and R2 Predictions")
parser.add_argument(
    "--path_to_actual_results",
    action="store",
    dest="path_to_actual_results",
    required=False,
    help="Path to the actual results from the 2020 ESPN draft. Default: ./data/2020_espn_draft_results.csv",
    default="./data/2020_espn_draft_results.csv",
)
parser.add_argument(
    "--path_to_accumulated_results",
    action="store",
    dest="path_to_accumulated_results",
    required=False,
    help="Path to the accumulated predictions for auction values. Default: ./data/fantasy_football_auction_values_with_sentiment.csv",
    default="./data/fantasy_football_auction_values_with_sentiment.csv",
)
args = parser.parse_args()
path_to_actual_results = args.path_to_actual_results
path_to_accumulated_results = args.path_to_accumulated_results

def evaluate_dataset(path_to_actual_results, path_to_accumulated_results, actual_results_index_col=0):
    actual_data = pd.read_csv(path_to_actual_results, index_col=actual_results_index_col)
    accumulated_data = pd.read_csv(path_to_accumulated_results)

    data = pd.merge(actual_data, accumulated_data, left_on="player_names", right_on="Player_Names").drop("Player_Names", axis=1)
    data = data[data['keepers'] != True].drop("keepers", axis=1)

    for model in [DecisionTreeRegressor(), RandomForestRegressor(), XGBRegressor()]:
        # Decision Trees
        mse = []
        mae = []
        r2 = []
        for i in tqdm(range(10)):
            xtrain, xtest, ytrain, ytest = train_test_split(data.drop(["player_names", "bid_amounts"], axis=1), data["bid_amounts"], test_size=0.20)
            model.fit(xtrain, ytrain)
            predictions = model.predict(xtest)
            mse.append(mean_squared_error(predictions, ytest))
            mae.append(mean_absolute_error(predictions, ytest))
            r2.append(r2_score(predictions, ytest))
        print(str(model))
        print(f"MSE: {np.mean(mse)}")
        print(f"MAE: {np.mean(mae)}")
        print(f"R2: {np.mean(r2)}")

if __name__ == "__main__":
    evaluate_dataset(path_to_actual_results, path_to_accumulated_results)