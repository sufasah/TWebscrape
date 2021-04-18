import os
import csv
from datetime import datetime
from time import sleep
from selenium import webdriver
from tweet import Tweet
from functools import cmp_to_key

# setting profile
browser_profile = webdriver.ChromeOptions()
browser_profile.add_experimental_option('prefs',{'intl.accept_languages':'en,en_US'})

# creating browser
browser = webdriver.Chrome('chromedriver.exe',options=browser_profile)
browser.maximize_window()

# fetching datas

browser.get("https://twitter.com/search?q=request%20for%20startup&src=typed_query&f=live")

tweets=[]
iter_for_scroll=20

def tweets_from_raw(tweets_raw,tweets):
    for tweet_raw in tweets_raw:
        tweet = Tweet()

        # getting top
        img_anchor = tweet_raw.find_element_by_css_selector("div:nth-child(1) a[href]")
        tweet.userLink = img_anchor.get_attribute("href")
        tweet.user_img_link = img_anchor.find_element_by_css_selector("img[src]").get_attribute("src")

        title_autos = tweet_raw.find_elements_by_css_selector("div:nth-child(2) > div:nth-child(1) a div[dir='auto']")
        
        tweet.userTitle = title_autos[0].text
        if len(title_autos[1].find_elements_by_css_selector("svg")) > 0:
            tweet.user_verified=True
        else:
            tweet.user_verified=False
        
        tweet.user = tweet_raw.find_element_by_css_selector("div:nth-child(2) > div:nth-child(1) a div[dir='ltr']").text

        time_anchor=tweet_raw.find_element_by_xpath("./div[2]/div[1]/div/div[1]/div[1]/a")

        tweet.statusLink = time_anchor.get_attribute("href")

        tweet.time = time_anchor.find_element_by_css_selector("time").get_attribute("datetime")
        #2021-04-18T15:16:36.000Z
        tweet.time = datetime.strptime(tweet.time,"%Y-%m-%dT%H:%M:%S.000Z")

        # getting content
        content_raw = tweet_raw.find_element_by_xpath("./div[2]/div[2]/div[1]/div[1]")

        tweet.content= content_raw.text
        tweet.contentLang= content_raw.get_attribute("lang")

        # getting attachment
        attachment_raw = tweet_raw.find_element_by_xpath("./div[2]/div[2]/div[2]")

        tweet.attachment = {
            "links":[],
            "imageUrls":[],
            "textData":attachment_raw.text,
        }

        for linkRaw in attachment_raw.find_elements_by_css_selector("a[href]"):
            tweet.attachment["links"].append(linkRaw.get_attribute("href"))
        
        for imageRaw in attachment_raw.find_elements_by_css_selector("img[src]"):
            tweet.attachment["imageUrls"].append(imageRaw.get_attribute("src"))
        
        # getting bottom
        bottomElems =  tweet_raw.find_elements_by_css_selector("div[data-testid='reply'],div[data-testid='retweet'],div[data-testid='like']>div>div:nth-child(2)")

        def format_counts(x):
            replaced = int(x.replace("K","").replace("M","").replace("B",""))
            if x.find("K") > -1:
                return replaced*1000
            elif x.find("M") > -1:
                return replaced*1000000
            elif x.find("B") > -1:
                return replaced*1000000000
            
            return replaced
            
        tweet.reply_count = bottomElems[0].text
        tweet.reply_count = format_counts(tweet.reply_count) if tweet.reply_count!="" else 0

        tweet.retweet_count = bottomElems[1].text
        tweet.retweet_count = format_counts(tweet.retweet_count) if tweet.retweet_count!="" else 0

        tweet.like_count = bottomElems[2].text
        tweet.like_count = format_counts(tweet.like_count) if tweet.like_count!="" else 0

        tweet.format_values()
        tweets.append(tweet)
    

while iter_for_scroll != 0:
    sleep(2)
    tweets_raw=browser.find_elements_by_css_selector("div[data-testid='tweet']")
    tweets_from_raw(tweets_raw,tweets)
    browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
    iter_for_scroll -= 1
    print(f"Iteration Remaining: {iter_for_scroll} - Tweet Count: {len(tweets)}")

# sort tweets and write to file

def tweet_comp(a:Tweet,b:Tweet):
    if(a.retweet_count > b.retweet_count):
        return -1
    
    if(a.retweet_count < b.retweet_count):
        return 1

    if(a.like_count > b.like_count):
        return -1
    
    if(a.like_count < b.like_count):
        return 1
    
    if(a.reply_count > b.reply_count):
        return -1
    
    if(a.reply_count < b.reply_count):
        return 1

    if(a.time >= b.time):
        return -1
    
    return 1

tweets.sort(key=cmp_to_key(tweet_comp))

with open("tweets.csv","w",encoding="utf-16") as tf:
    fields=[]
    for field in tweets[0].__dict__:
        fields.append(field)
    tweet_writer = csv.DictWriter(tf,fieldnames=fields,delimiter=Tweet.csv_delimiter)
    tweet_writer.writeheader()

    for tweet in tweets:
        tweet_writer.writerow(tweet.__dict__)

tf.close()
