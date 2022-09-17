# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AvakusItem(scrapy.Item):
    name = 'review_item'
    
    wine_name = scrapy.Field()
    wine_price = scrapy.Field()

    wine_name = scrapy.Field()
    wine_developer = scrapy.Field()
    wine_city = scrapy.Field()
    wine_country = scrapy.Field()