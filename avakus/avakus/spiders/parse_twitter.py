from scrapy import (
    Spider,
    Request,
)
from utils.selenium_webdriver import (
    Driver,
    EC,
    WebDriverWait,
)


class TwitterListing(Spider):
    name = "twitter_listing"
    custom_settings = {
        "HTTPERROR_ALLOWED_CODES": [
            403,
            429,
        ],
    }

    def start_requests(self):
        yield Request(
            url="https://twitter.com/avakovarsen",
            method="GET",
            callback=self.parse,
        )

    def parse(self, response):
        print(response.url)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")