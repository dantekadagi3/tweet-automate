import tweepy
import config
import json
import random
import time
import os
from datetime import datetime
from tweepy.errors import TweepyException, TooManyRequests

LOCK_FILE = "/tmp/twitter_post.lock"



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


def acquire_lock():
    if os.path.exists(LOCK_FILE):
        print(" Script already running. Exiting.")
        return False
    open(LOCK_FILE, "w").close()
    return True

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def allowed_time_window(start=9, end=21):
    hour = datetime.now().hour
    return start <= hour < end



def post_tweet():
    if not acquire_lock():
        return

    try:
        if not allowed_time_window():
            print(" Outside posting hours. Skipping.")
            return

        base_path = f"{config.VPS_DIRECTORY}data/"
        quotes = read_json(base_path + "quotes.json")
        posted = read_json(base_path + "posted.json")
        hashtags = read_json(base_path + "hashtags.json")

        available = [q for q in quotes if q not in posted]
        if not available:
            print(" No new quotes available.")
            return

        text = random.choice(available)

        # Add 1–3 hashtags
        tag_count = random.randint(1, min(3, len(hashtags)))
        tags = " ".join(random.sample(hashtags, tag_count))

        tweet = f"{text}\n\n{tags}"

        client = get_client()
        client.create_tweet(text=tweet)

        posted.append(text)
        write_json(base_path + "posted.json", posted)

        print(" Tweet posted")
        print(tweet)

        time.sleep(random.randint(60, 180))

    except TooManyRequests:
        print(" Rate limited. Sleeping 15 minutes.")
        time.sleep(900)

    except TweepyException as e:
        print(f" Twitter error: {e}")

    finally:
        release_lock()



if __name__ == "__main__":
    post_tweet()
