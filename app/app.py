import tweepy, time, random, argparse
from configparser import ConfigParser
import pandas as pd
from pathlib import Path

config = ConfigParser(interpolation=None)
config.read('config.ini')
bearer_token = config['twitter']['bearer_token']

# Use argparse to process arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', required=True, help="Twitter username (required)")
args = parser.parse_args()

def following(username):
    client = tweepy.Client(bearer_token)
    username = username
    userfollowinglist = set()
    userid = client.get_user(username=username).data.id
    for response in tweepy.Paginator(client.get_users_following, userid,
                                        max_results=1000, limit=5):
        for id in response.data:
            userfollowinglist.add(str(id))

    return userfollowinglist

twitteruser = args.user
followerlist1 = following(twitteruser)
while True:
    newfollowers = set()
    followerlist2 = following(twitteruser)

    for follower in followerlist2:
        if follower not in followerlist1:
            newfollowers.add(str(follower))
    
    if not newfollowers:
        print("No new followers")
        minutes_to_wait = random.randrange(2,5)
        print(f'Waiting for {minutes_to_wait} minutes')
        time.sleep(minutes_to_wait * 60)
    else:
        print("Found new followers")
        data = newfollowers
        column = time.strftime("%Y%m%d-%H%M")
        df = pd.DataFrame(data=data, columns=[column])
        filepath = Path('../output/newfollowers.csv')
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if filepath.is_file():
            df_newfollowers = pd.read_csv(filepath)
            df_newfollowers[column] = df
            df_newfollowers.to_csv(filepath, index=False)
        else:
            df.to_csv(filepath, index=False)
            minutes_to_wait = random.randrange(2,5)
            print(f'Waiting for {minutes_to_wait} minutes')
            time.sleep(minutes_to_wait * 60)
    
    followerlist1 = followerlist2