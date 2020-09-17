# Get Baseline Predictions
Using only the gathered fantasy football auction values (fantasy_football_auction_values.csv) and the actual auction values (2020_espn_draft_results.csv), run several algorithms (RF, XGBoost, NN, etc.) to develop an initial baseline prediction to see if including sentiment analysis on Reddit/Twitter has any effect.
## Preliminary Results
NOTE: These results were conducted using absolutely no hyperparameter tuning or any type of edit to the model that might improve performance. Additionally, these were constructed using 10 different training/testing splits split into 80/20 and the average was computed among these scores.
- Decision Trees:
    - MSE: 43.52
    - MAE: 3.78
    - R2: 0.83
- Random Forests:
    - MSE: 17.47
    - MAE: 2.30
    - R2: 0.92
- XGBoost:
    - MSE:18.51
    - MAE: 2.45
    - R2: 0.92