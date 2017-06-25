# from tqdm import tqdm
# import numpy as np
import argparse
import tweepy
import queue
import time
import os

## get args
parser = argparse.ArgumentParser(description=
    "Simple Friends Conections Downloader", usage='%(prog)s -n <screen_name> [options]')

parser.add_argument('-n', '--name', required=True, metavar="screen_name",
                    help='target screen_name')

parser.add_argument('-l', '--limit', metavar='N', type=int, default=10,
                    help='limit the number of tweets to retreive (default=1000)')

args = parser.parse_args()

from secrets import consumer_key, consumer_secret, access_token, access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def getFriendsId(api, id):
    itr = tweepy.Cursor(api.friends_ids, id=id).items()
    res = []
    while True:

        try:
            for friendId in itr:
                res.append(friendId)
            return res

        except tweepy.TweepError as e:
            if e.response.status_code == 429:
                print("sleep for 15Min")
                time.sleep(15 * 60)
                print("start over!")
            else:
                raise e

def bfs(api, table, head, maxDepth):
    bfsQ = queue.deque( [(head, 0)] )

    while len(bfsQ) != 0 and bfsQ[0][1] < maxDepth:
        nodeId = bfsQ.popleft()
        print( nodeId )

        if not nodeId[0] in table:
            friendsId = getFriendsId(api, nodeId[0])
            table[ nodeId[0] ] = friendsId
            for friendId in friendsId:
                bfsQ.append( (friendId, nodeId[1]+1) )

table = {}
user_info = api.get_user(screen_name=args.name)
bfs(api, table, user_info._json['id'], 2)
print( table )
