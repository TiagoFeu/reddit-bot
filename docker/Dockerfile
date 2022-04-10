FROM continuumio/anaconda3
WORKDIR /home/reddit-bot
RUN conda install jupyter -y --quiet && mkdir /home/reddit-bot -p
RUN conda install -c conda-forge praw
RUN conda install -c conda-forge wordcloud
EXPOSE 8888