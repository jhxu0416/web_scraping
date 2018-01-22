import requests
import pandas as pd
import time
def init_emoji_code(file_path):
    with open(file_path, "r") as f:
        text_list = f.read().split("\n")

    code_list = []
    emoji_data = {}

    for text in text_list:
        code = text.split("\t")[0]
        code_list.append(code)
        emoji_data[code] = []

    return code_list, emoji_data


def emoji_scraping(emoji_code):
    URL = "http://www.emojitracker.com/api/details/"+str(emoji_code)
    json_response = requests.get(URL).json()
    recent_tweets = json_response['recent_tweets']
    if len(recent_tweets) > 0:
        print("Get {} tweets with emoji {}".format(len(recent_tweets), json_response['char']))
    else:
        print("Fail to get data")
    return pd.DataFrame.from_dict(recent_tweets)

def single_trail(trial, num):
    code_list, emoji_data = init_emoji_code("emoji_code.txt")
    for i in range(num):
        for code in code_list:
            try:
                emoji_data[code].append(emoji_scraping(code))
            except:
                pass
        print("***********sleep 30 sec ***********")
        time.sleep(30)

    for i in range(len(code_list)):
        df = pd.concat(emoji_data[code_list[i]])
        file_name = "data/"+str(code_list[i])+'_'+str(trial)+".csv"
        df.to_csv(file_name)
    print("Done trail #{}".format(trial))

if __name__ == "__main__":
    trail_start_idx = int(input("total trail start index:"))
    trail_end_idx = int(input("total trail end index:"))
    print("total trail number: {}".format(trail_end_idx-trail_start_idx))
    num = int(input("number of tweets(*10) per trail:"))
    print("number of tweets per trail:".format(num*10))
    for trial in range(trail_start_idx, trail_end_idx):
        single_trail(trial, num)
    print("************* FINISHED *************")