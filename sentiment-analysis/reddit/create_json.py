"""Create a dictionary with the following format:
{
    post.id1 = {
        submission_title = "Josh Jacobs is the GOAT",
        submission_author = "author_of_the_post",
        upvote_ratio = "upvote_ratio_of_the_post",
        score = "score_of_the_post",
        top_comments = [
            Comment(id=12345),
            Comment(id=34567),
        ],
        top_comments_score = [
            1234 # corresponds to the score of the first comment in top_comments
            123456 # second comment in top_comments
        ]
    
    },
    post.id2 = {
        ...
    }
    
}
"""

import argparse
import datetime
import json
import os

import pandas as pd
from tqdm import tqdm

import praw

parser = argparse.ArgumentParser(description="Define the arguments in the create_json.py file.")
parser.add_argument(
    "--subreddit",
    action="store",
    dest="subreddit",
    required=False,
    help="The subreddit that you want to scrape (i.e. fantasyfootball, nfl, etc.). Default: fantasyfootball",
    default="fantasyfootball",
)
parser.add_argument(
    "--num_submissions",
    action="store",
    dest="num_submissions",
    required=False,
    help="The number of submissions that you want to scrape. Default: 100",
    default=100,
)
parser.add_argument(
    "--time_filter",
    action="store",
    dest="time_filter",
    required=False,
    help="The time filter that you want to use (i.e. 'month', 'day', etc.). Default: 'month'",
    default="month",
)
parser.add_argument(
    "--json_output_dir",
    action="store",
    dest="json_output_dir",
    required=False,
    help="The output directory where you want to save your json file. Default: './output/'",
    default="./output/",
)
parser.add_argument(
    "--no_including_comments",
    dest="no_including_comments",
    action="store_true",
    help="If you do not want to include comments within the .json file, add this argument.",
)

args = parser.parse_args()
subreddit = args.subreddit
num_submissions = int(args.num_submissions)
time_filter = args.time_filter
json_output_dir = args.json_output_dir
no_including_comments = args.no_including_comments


# Accessing API using Secret token
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    usernme=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)


def generate_json_file(
    subreddit=subreddit,
    num_submissions=num_submissions,
    time_filter=time_filter,
    json_output_dir=json_output_dir,
    no_including_comments=False,
):
    # Define the subreddit
    subreddit = reddit.subreddit(subreddit)

    # Define the mode that you want to sort by (i.e. hot, new, etc.)
    top_subreddit_submissions = subreddit.top(
        limit=num_submissions,
        time_filter=time_filter,
    )

    ff_dict = {}

    print(f"Now creating the dictionary, which will contain {num_submissions} posts from the {subreddit} subreddit.")
    print(f"This will be saved in the folder {json_output_dir}.")
    print(f"Creating dictionary...")
    for submission in tqdm(top_subreddit_submissions):
        # Add basic information
        ff_dict[submission.id] = {}
        ff_dict[submission.id]["submission_title"] = submission.title
        ff_dict[submission.id]["submission_author"] = submission.author.name
        ff_dict[submission.id]["submission_upvote_ratio"] = submission.upvote_ratio
        ff_dict[submission.id]["submission_score"] = submission.score

        # Add top 10 comments for each post
        if not no_including_comments:
            top_level_comments = list(submission.comments)
            top_ten_comments = []
            top_ten_comments_scores = []
            for comment in top_level_comments[:10]:
                comment_instance = praw.models.Comment(reddit=reddit, id=comment)
                top_ten_comments.append(comment_instance.body)
                top_ten_comments_scores.append(comment_instance.score)

            ff_dict[submission.id]["top_comments"] = top_ten_comments
            ff_dict[submission.id]["top_comments_scores"] = top_ten_comments_scores
    print("Dictionary created! Now saving...")
    # Create output directory if this does not exist yet
    if not os.path.exists(json_output_dir):
        os.mkdir(json_output_dir)

    # Save the json file into output directory with the specific name.
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    whole_output_filename = (
        f"{json_output_dir}{current_date}_top_{num_submissions}_posts.json"
    )
    with open(whole_output_filename, "w") as fp:
        json.dump(ff_dict, fp)


if __name__ == "__main__":
    generate_json_file(
        subreddit=subreddit,
        num_submissions=num_submissions,
        time_filter=time_filter,
        json_output_dir=json_output_dir,
        no_including_comments=no_including_comments,
    )
