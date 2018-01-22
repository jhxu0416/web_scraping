import tweepy
from tweepy.streaming import StreamListener
import pandas as pd
import json

#define listener
class Listener(StreamListener):
    def on_data(self, raw_data):
        try:
            tweet = json.loads(raw_data)
            with open('tweet.json', 'a') as f:
                json.dump(tweet, f)
        except BaseException:
            print('fail to save into json')
            pass
        #control the max limit
        #if self.tweet_number >= self.max_tweets:
        #    print('Limit {} tweets reached'.format(self.tweet_number))
        #    return False

    #http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

def enter_query():
    input_var = input("Enter your query(format: #something): ")
    if len(str(input_var)) == 0:
        print("Empty query")
        return enter_query()
    else:
        if str(input_var)[0] == "#":
            # correct format
            print("Search query is {}".format(input_var))
            return input_var
        else:
            q = input("Do you mean query = #" +str(input_var) + "? (y/n)")
            if q.lower() == "y":
                input_var = "#"+str(input_var)
                print("Search query is {}".format(input_var))
                return input_var
            else:
                print("Re-enter your query")
                return enter_query()

def enter_Tweet_num():
    input_num = input("How many tweet you want to scrap(max 30)?: ")
    if input_num.isdigit():
        input_num = int(input_num)
        if input_num <= 30 and input_num >= 1:
            print("Scraping {} tweets".format(input_num))
            return input_num
        else:
            print("Scraping number out of range([1,30]). Please re-enter your search number")
            return enter_Tweet_num()
    else:
        print("Your input is not a valid positive integer. Please re-enter your search number")
        return enter_Tweet_num()

if __name__ == '__main__':
    query = enter_query()
    search_num = enter_Tweet_num()

    consumer_key = '####'
    consumer_secret = '####'
    access_token = '####'
    access_secret = '####'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    #http://docs.tweepy.org/en/v3.5.0/api.html


    results = api.search(q = query, count = search_num)
    df = [pd.DataFrame.from_dict(result._json, orient='index') for result in results]

    df1 = pd.concat(df, axis=1)

    df1.columns = list(range(1,len(results)+1))
    df1.to_csv('raw_data.csv')

    print('Done Twitter Scraping')

