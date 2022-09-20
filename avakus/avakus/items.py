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

