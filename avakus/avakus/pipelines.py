# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy import Item
from scrapy.exceptions import DropItem


class AvakusPipeline:
    def process_item(self, item, spider):
        match item:
            case Item(name="wishlist_item" | "review_item"):
                item.process_item()
            case _:
                raise DropItem(f"Such item does not exist! Dropping {item=}")
        return item