class Tweet:
    csv_delimiter="~"
    csv_delimiter_dumpval="##-delim-##"

    def __init__(self):
        self.user_link=""
        self.user_img_link=""
        self.user_title=""
        self.user=""
        self.user_verified=None
        self.status_link=""
        self.time=""
        self.content=""
        self.content_lang=""
        self.attachment={}
        self.reply_count=0
        self.retweet_count=0
        self.like_count=0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.user_title}"

    def format_values(self):
        def format(x):
            return x.strip("\n").replace(Tweet.csv_delimiter,Tweet.csv_delimiter_dumpval)

        self.user_title=format(self.user_title)
        self.user=format(self.user)
        self.user_verified=None
        self.content=format(self.content)
        self.attachment["textData"]=format(self.attachment["textData"])
