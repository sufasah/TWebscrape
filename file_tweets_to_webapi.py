import os
import csv
import json
from tweet import Tweet
from flask import Flask,jsonify

app = Flask(__name__)

@app.route("/api/tweets", methods=["GET"])
def getTweets():
    tweets=[]
    with open("tweets.csv",encoding="utf-16") as tf:
        tweet_reader = csv.DictReader(tf,delimiter=Tweet.csv_delimiter)

        for row in tweet_reader:
            for key in row:
                if(type(row[key]) == type("")):
                    row[key] = row[key].replace(Tweet.csv_delimiter_dumpval,Tweet.csv_delimiter)
            tweets.append(row)
    return jsonify(tweets)

    
if __name__ == "__main__":
    app.config['JSONIFY_PRETTYPRINT_REGULAR']=True
    app.run()
