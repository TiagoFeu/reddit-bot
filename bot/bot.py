import praw
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import stopwords    # stopwords to clean the text

#set bot parameters -----------------------------
subreddit_name = 'futebol'
# -----------------------------------------------

# import the reddit credentials from .json file
file = open('credentials.json', 'r')
credentials = json.load(file)

# create the reddit instance
reddit = praw.Reddit(client_id=credentials['client_id'],
                     client_secret=credentials['client_secret'],
                     user_agent=credentials['user_agent'],
                     username=credentials['username'],
                     password=credentials['password'])

subreddit = reddit.subreddit(subreddit_name)

