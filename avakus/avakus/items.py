# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import os
import json
import scrapy


FOLDER = os.getcwd() + '/storage/'
os.path.exists(FOLDER) or os.mkdir(FOLDER)

def write_json(file_path:str, file_value:dict) -> None:
    if os.path.exists(file_path):
        with open(file_path, "r") as file_json:
            data = json.load(file_json)
            data.append(file_value)
    else:
        data = [file_value]
    with open(file_path, 'w') as file_json:
        json.dump(
            data, 
            file_json, 
            indent=4,
        )

def get_cmp_id(file_path:str, key:str, search:int) -> bool:
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r") as file_json:
        data = json.load(file_json)
        presence = False
        for f in data:
            if f[key] == search:
                presence = True
    return presence

def get_cmp_ids(file_path:str) -> list:
    ids = []
    if not os.path.exists(file_path):
        return ids
    with open(file_path, 'r') as file_json:
        data = json.load(file_json)
        for review in data:
            ids.append(review.get("review_id"))
    return ids


class TweetItem(scrapy.Item):
    name = 'tweet_item'
    file_path = FOLDER + 'tweets.json'
    post_id = scrapy.Field()
    post_link = scrapy.Field()
    post_time = scrapy.Field()
    post_comment_count = scrapy.Field()
    post_retweet_count = scrapy.Field()
    post_like_count = scrapy.Field()
    post_quote_count = scrapy.Field()
    post_watch_count = scrapy.Field()
    post_text = scrapy.Field()

    def process_item(self):
        dct = dict(self)
        if not get_cmp_id(
            TweetItem.file_path, 
            'post_id', 
            dct["post_id"]
        ):
            write_json(
                TweetItem.file_path, 
                dct
            )

class TweetProfileItem(scrapy.Item):
    name = 'tweet_profile_item'
    file_path = FOLDER + 'tweets_profile.json'
    profile_name = scrapy.Field()
    profile_link = scrapy.Field()
    profile_username = scrapy.Field()
    profile_description = scrapy.Field()
    profile_location = scrapy.Field()
    profile_website = scrapy.Field()
    profile_joindate = scrapy.Field()
    profile_tweets = scrapy.Field()
    profile_following = scrapy.Field()
    profile_followers = scrapy.Field()
    profile_likes = scrapy.Field()
    profile_image_stats = scrapy.Field()
    profile_datetime_check = scrapy.Field()

    def process_item(self):
        dct = dict(self)
        write_json(
            TweetProfileItem.file_path, 
            dct
        )

class ReviewItem(scrapy.Item):
    name = 'review_item'
    file_path = FOLDER + 'reviews.json'
    review_id = scrapy.Field()
    review_datetime = scrapy.Field()
    likes = scrapy.Field()
    text = scrapy.Field()
    score = scrapy.Field()
    cmp_id = scrapy.Field()
    product_name = scrapy.Field()
    product_link = scrapy.Field()
    product_year = scrapy.Field()
    product_developer = scrapy.Field()
    product_developer_link = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    region = scrapy.Field()
    region_link = scrapy.Field()
    country = scrapy.Field()
    country_link = scrapy.Field()
    review_write = scrapy.Field()
    review_write_ago = scrapy.Field()

    def process_item(self):
        dct = dict(self)
        if not get_cmp_id(
            ReviewItem.file_path, 
            'cmp_id', 
            dct["cmp_id"]
        ):
            write_json(
                ReviewItem.file_path, 
                dct
            )


class WishlistItem(scrapy.Item):
    name = "wishlist_item"
    file_path = FOLDER + "wishlist.json"
    cmp_id = scrapy.Field()
    product_name = scrapy.Field()
    product_link = scrapy.Field()
    product_year = scrapy.Field()
    product_developer = scrapy.Field()
    product_developer_link = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    region = scrapy.Field()
    region_link = scrapy.Field()
    country = scrapy.Field()
    country_link = scrapy.Field()

    def process_item(self):
        dct = dict(self)
        if not get_cmp_id(
            WishlistItem.file_path, 
            'cmp_id', 
            dct["cmp_id"]
        ):
            write_json(
                WishlistItem.file_path, 
                dct
            )

