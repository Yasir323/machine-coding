from typing import List


class Tweet:

    def __init__(self, tweetId: int, timestamp: int):
        self.tweetId = tweetId
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f"{self.tweetId}"


class User:

    def __init__(self, userId: int):
        self.userId = userId
        self.tweets = []
        self.following = set()

    def add_tweet(self, tweetId: Tweet):
        self.tweets.append(tweetId)

    def follow(self, followeeId: int):
        if followeeId != self.userId:
            self.following.add(followeeId)

    def unfollow(self, followeeId: int):
        if followeeId != self.userId:
            if followeeId in self.following:
                self.following.remove(followeeId)

    def __str__(self) -> str:
        return f"{self.userId}"


class Twitter:

    def __init__(self):
        self.users = {}
        self.tweet_count = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        user = self.users.get(userId)
        if not user:
            user = User(userId)
            self.users[userId] = user
        self.tweet_count += 1
        tweet = Tweet(tweetId, self.tweet_count)
        user.add_tweet(tweet)

    def getNewsFeed(self, userId: int) -> List[int]:
        user = self.users.get(userId)
        if user:
            all_tweets = user.tweets.copy()
            for followeeId in user.following:
                followee = self.users.get(followeeId)
                if followee:
                    all_tweets.extend(followee.tweets)
            return [tweet.tweetId for tweet in list(sorted(all_tweets, key=lambda x: x.timestamp, reverse=True))[:10]]

    def follow(self, followerId: int, followeeId: int) -> None:
        user = self.users.get(followerId)
        if not user:
            user = User(followerId)
            self.users[followerId] = user
        user.follow(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        user = self.users.get(followerId)
        if user:
            user.unfollow(followeeId)
