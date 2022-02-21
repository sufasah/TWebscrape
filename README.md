# Internship Task (KZFps0nCik6x3cyj)

***Dependencies***:
* [chromedriver.exe](./chromedriver.exe) file for windows 32 and Chrome version 90.
* Python version 3 used.

***Modules installed via pip***
* requests
* selenium
* flask

### How to use ?

At first, to create [tweets.csv](./tweets.csv) file which will be filled with fetched tweets from twitter searched by given search key at the task you have to execute [get_tweets_from_twitter.py](./get_tweets_from_twitter.py). After [tweets.csv](tweets.csv) filled, To see datas in the file via web interface, You have to execute [file_tweets_to_webapi.py](./file_tweets_to_webapi.py) which is Flask web api module. At the end, you can open your browser and send a get request to url http://127.0.0.1:5000/api/tweets.

**Notes**: Iteration count in [get_tweets_from_twitter.py](./get_tweets_from_twitter.py) file, can be changed.
