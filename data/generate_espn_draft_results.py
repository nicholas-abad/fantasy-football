import pandas as pd
from espn_api.football import League
import os

espn_s2 = os.getenv("ESPN_S2")
swid = os.getenv("ESPN_SWID")

print("Authenticating...")
league = League(league_id=368028, year=2020, espn_s2=espn_s2, swid=swid)
print("Successfully Authenticated!")


def create_csv(output_filename):
    bid_amounts = [player.bid_amount for player in league.draft]
    player_names = [player.playerName for player in league.draft]
    keepers = [player.keeper_status for player in league.draft]
    round_num = [player.round_num for player in league.draft]
    round_pick = [player.round_pick for player in league.draft]

    df = pd.DataFrame(
        list(zip(player_names, bid_amounts, keepers, round_num, round_pick)),
        columns=["player_names", "bid_amounts", "keepers", "round_num", "round_pick"],
    )

    df.to_csv(output_filename)


if __name__ == "__main__":
    create_csv("./2020_espn_draft_results.csv")
