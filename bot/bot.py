import praw
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import stopwords    # stopwords to clean the text

#set bot parameters -----------------------------
subreddit_name = 'futebol'
words_number = 20
submission_number = 20
# -----------------------------------------------

# import the reddit credentials from .json file
f = open('credentials.json', 'r')
credentials = json.load(f)
f.close()

# create the reddit instance
reddit = praw.Reddit(client_id=credentials['client_id'],
                     client_secret=credentials['client_secret'],
                     user_agent=credentials['user_agent'],
                     username=credentials['username'],
                     password=credentials['password'])
subreddit = reddit.subreddit(subreddit_name)

# add some stopwords related to the topic
new_stopwords = ['postagem', '/r/futebol,', 'adequada', 'comentário' ,'comentário.', '**downvote**', '**upvote**' , '^|', 'jogo', 'falar', 'ficar', '**reporte**', 'post!', '[^(flair', 'vc', 'time', '---']
stopwords.pt_stopwords = stopwords.pt_stopwords + new_stopwords

word_ranking = {}
# save words into a dictionary ranked by frequency
for submission in subreddit.hot(limit=submission_number):
    title = submission.title.lower()
    title = title.split()
    for word in title:
        if len(word) <= 1 or len(word) >= 15:
            continue
        if word not in stopwords.pt_stopwords:
            if word in word_ranking:
                word_ranking[word] += 1
            else:
                word_ranking[word] = 1
    submission.comments.replace_more(limit=None)
    for comment in submission.comments:
        comment_text = comment.body.lower()
        comment_text = comment_text.split()
        for word in comment_text:
            if len(word) <= 1 or len(word) >= 15:
                continue
            if word not in stopwords.pt_stopwords:
                if word in word_ranking:
                    word_ranking[word] += 1
                else:
                    word_ranking[word] = 1

# sort the dictionary by frequency and save 10 most frequent words
word_ranking = sorted(word_ranking.items(), key=lambda x: x[1], reverse=True)[:words_number]
print(word_ranking)

# saves it into a json file
with open('../results/word_ranking.json', 'w') as outfile:
    json.dump(word_ranking, outfile, indent=4)
    word_ranking = json.dumps(word_ranking, indent=4)

# draws a wordcloud from word_ranking
wordcloud = WordCloud(width=800, height=800, max_font_size=200, background_color='white').generate(word_ranking)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig('../results/wordcloud.png')