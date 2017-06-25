# from tqdm import tqdm
import numpy as np
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
                print("sleep for 5Min! -> " + time.ctime())
                time.sleep(5 * 60)
                print("continue! -> " + time.ctime())
            else:
                raise e

def bfs(api, head, maxDepth):
    bfsQ = queue.deque( [(head, 0)] )

    while len(bfsQ) != 0 and bfsQ[0][1] < maxDepth:
        nodeId = bfsQ.popleft()
        print("getting userId: ", nodeId)

        if not os.path.isfile("./downloaded/" + str(nodeId[0]) + ".npy"):
            friendsId = getFriendsId(api, nodeId[0])
            np.save("./downloaded/" + str(nodeId[0]), np.array(friendsId))
            for friendId in friendsId:
                bfsQ.append( (friendId, nodeId[1]+1) )

user_info = api.get_user(screen_name=args.name)
bfs(api, user_info._json['id'], args.limit)
