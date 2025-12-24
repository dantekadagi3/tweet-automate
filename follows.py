import tweepy
import config
import json
import random
import time
from tweepy.errors import TweepyException, TooManyRequests



def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_client():
    return tweepy.Client(
        bearer_token=config.BEARER_TOKEN,
        consumer_key=config.API_KEY,
        consumer_secret=config.API_KEY_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_token_secret=config.ACCESS_TOKEN_SECRET,
        wait_on_rate_limit=True  
    )



def follow_people(
    max_follows_per_run=5,
    sleep_min=15,
    sleep_max=40
):
    following_path = f"{config.VPS_DIRECTORY}data/following.json"
    to_follow_path = f"{config.VPS_DIRECTORY}data/tofollow.json"

    following = set(read_json(following_path))
    targets = read_json(to_follow_path)

    if not targets:
        print(" No target accounts found.")
        return

    client = get_client()
    seed_account = random.choice(targets)
    seed_id = seed_account["userId"]

    print(f" Mining followers from: {seed_account.get('username', seed_id)}")

    follows_done = 0

    try:
        followers = client.get_users_followers(
            id=seed_id,
            max_results=50
        ).data or []

        for user in followers:
            if follows_done >= max_follows_per_run:
                print(" Follow limit reached for this run.")
                break

            if user.id in following:
                continue

            try:
                client.follow_user(user.id)
                following.add(user.id)
                follows_done += 1

                print(f" Followed @{user.username}")

                sleep_time = random.randint(sleep_min, sleep_max)
                time.sleep(sleep_time)

            except TooManyRequests:
                print(" Rate limit hit. Sleeping for 15 minutes.")
                time.sleep(900)
                break

            except TweepyException as e:
                print(f" Failed to follow @{user.username}: {e}")
                continue

    except TweepyException as e:
        print(f" Failed to fetch followers: {e}")

    write_json(following_path, list(following))
    print(f" Run complete. Followed {follows_done} users.")


if __name__ == "__main__":
    follow_people()
