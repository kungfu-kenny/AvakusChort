from scrapy import (
    Spider,
    Request,
)
from utils.selenium_webdriver import (
    Driver,
)

class VivinoListing(Spider):
    name = 'vivino_listing'
    custom_settings = {
        "HTTPERROR_ALLOWED_CODES": [
            403,
            429,
        ],
    }


    def start_requests(self):
        yield Request(
            url='https://www.vivino.com/users/arsen-av',
            method="GET",
            callback=self.parse
        )
    
    @staticmethod
    def _get_review_number(stars:list) -> float:
        stars = [
            int(i.split('-')[1]) for i in stars
        ]
        return float(0.01 * sum(stars))

    @staticmethod
    def _get_review_link(element:object) -> tuple:
        return element.get_attribute("href"), element.text

    @staticmethod
    def _get_review_product_year(name:str, text:str) -> int:
        return int(text.split(name)[-1].strip())

    @staticmethod
    def _get_review_product_price(price:str) -> float:
        pass

    @staticmethod
    def _get_review_product_currency(curr:str) -> str:
        pass

    def parse(self, response):
        with Driver(url=response.url) as driver:
            # while True:
            #     divs = driver.find_elements("css selector", "div.show-more")
            #     if divs and (click:=divs[0].find_element("css selector", "button#btn-more-activities")):
            #         click.click()
            #     else:
            #         break
            for review in driver.find_elements("css selector", "div.user-activity-item"):
                developer_link, developer_name = self._get_review_link(
                    review.find_element("css selector", "span.text-small > a.link-muted")
                )
                review_product_link, review_product = self._get_review_link(
                    review.find_element("css selector", "p.wine-name > a.link-muted.bold")
                )
                review_product_year = self._get_review_product_year(
                    review_product, 
                    review.find_element("css selector", "p.wine-name").text
                )
                
                review_product_region, review_product_country = [
                    self._get_review_link(i)
                    for i in review.find_elements("css selector", "div.wine-info > div.text-mini > a")
                ]
                review_product_region_link, review_product_region_name = review_product_region
                review_product_country_link, review_product_country_name = review_product_country

                review_product_price = ''
                review_product_price_currency = ''

                review_text = review.find_element("css selector", "p.tasting-note.text-larger").text
                review_score = self._get_review_number(
                    [
                        i.get_attribute("class") for i in 
                        review.find_elements("css selector", "span.rating.rating-xs.text-inline-block > i")
                    ]
                )
                print(review_product_region_link)
                print(review_product_link, review_product_year)
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            