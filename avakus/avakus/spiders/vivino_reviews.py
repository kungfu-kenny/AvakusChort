from scrapy import (
    Spider,
    Request,
)
from utils.selenium_webdriver import (
    Driver,
    EC,
    WebDriverWait,
)
from avakus.items import (
    ReviewItem, 
    WishlistItem,
)


class VivinoListing(Spider):
    name = 'vivino_listing'
    custom_settings = {
        "HTTPERROR_ALLOWED_CODES": [
            403,
            429,
        ],
    }

    def __init__(self):
        self._urls = [
            ('https://www.vivino.com/users/arsen-av', 'review'),
            ('https://www.vivino.com/users/arsen-av/wishlist', 'wishlist'),
        ]

    def start_requests(self):
        for url, url_type in self._urls:
            yield Request(
                url=url,
                method="GET",
                callback=self.parse,
                cb_kwargs={
                    "url_type": url_type,
                }
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
        return int(i) if (i:=text.split(name)[-1].strip()) and not any(f.isalpha() for f in i) else None

    @staticmethod
    def _get_review_product_price(price:str) -> float:
        if not price or price.strip() == "-":
            return None
        return round(
            float(price.replace(",", ".").replace(" ", "")),
            1
        )

    @staticmethod
    def _get_review_product_currency(curr:str) -> str:
        if not curr:
            return None
        if not curr[0].text:
            return None 
        return curr[0].text.strip()

    @staticmethod
    def _develop_all_records(driver:object, btn_class:str) -> None:
        while True:
            divs = driver.find_elements("css selector", "div.show-more")
            if divs and (click:=divs[0].find_element("css selector", btn_class)) and click.size.get("height") > 0:
                click.click()
                driver.implicitly_wait(1)
            else:
                break
        return None

    #TODO check the alternative
    def parse_alternative(self, response, url_type:str):
        with Driver(url=response.url) as driver:
            if url_type == 'review':
                btn_class = "button#btn-more-activities"
                items = "div.user-activity-item"
            elif url_type == 'wishlist':
                btn_class = "button.btn.btn-default.btn-md.btn-distinct.btn-flow"
                items = "div.activity-wine-card.activity-section.clearfix"
            while True:
                if url_type == "review":
                    for review in WebDriverWait(driver, 100).until(
                        EC.presence_of_all_elements_located(
                            (
                                "css selector", 
                                items
                            )
                        )
                    ):
                        review_developer_link, review_developer_name = self._get_review_link(
                            review.find_element("css selector", "span.text-small > a.link-muted")
                        )
                        review_product_link, review_product = self._get_review_link(
                            review.find_element("css selector", "p.wine-name > a.link-muted.bold")
                        )
                        review_product_year = self._get_review_product_year(
                            review_product, 
                            review.find_element("css selector", "p.wine-name").text
                        )
                        
                        region_country = [
                            self._get_review_link(i)
                            for i in review.find_elements("css selector", "div.wine-info > div.text-mini > a")
                        ]
                        if region_country:
                            review_product_region, review_product_country = region_country
                            review_product_region_link, review_product_region_name = review_product_region
                            review_product_country_link, review_product_country_name = review_product_country
                        else:
                            review_product_region_link, review_product_region_name = None, None
                            review_product_country_link, review_product_country_name = None, None

                        review_product_price = self._get_review_product_price(
                            review.find_element(
                                "css selector", 
                                "span.header-large.text-block.wine-info-value.wine-price-value"
                            ).text
                        )
                        review_product_price_currency = self._get_review_product_currency(
                            review.find_elements(
                                "css selector", 
                                "span.text-block.text-micro.wine-price-currency"
                            )
                        )

                        if url_type == "review":
                            review_product_id = int(
                                review.find_element(
                                    "css selector", 
                                    "div.activity-wine-card.activity-section.clearfix"
                                ).get_attribute("data-vintage-id")
                            )
                            review_datetime = review.find_element("css selector", "a.link-muted.bold.inflate").get_attribute("title")
                            review_likes = int(
                                review.get_attribute("data-likes-count")
                            )
                            review_id = int(
                                review.get_attribute("data-id")
                            )
                            review_text = review.find_element("css selector", "p.tasting-note.text-larger").text
                            review_score = self._get_review_number(
                                [
                                    i.get_attribute("class") for i in 
                                    review.find_elements("css selector", "span.rating.rating-xs.text-inline-block > i")
                                ]
                            )
                            yield ReviewItem(
                                review_id = review_id,
                                review_datetime=review_datetime,
                                likes = review_likes,
                                text = review_text,
                                score = review_score,
                                cmp_id = review_product_id,
                                product_name = review_product,
                                product_link = review_product_link,
                                product_year = review_product_year,
                                product_developer = review_developer_name,
                                product_developer_link = review_developer_link,
                                price = review_product_price,
                                currency = review_product_price_currency,
                                region = review_product_region_name,
                                region_link = review_product_region_link,
                                country = review_product_country_name,
                                country_link = review_product_country_link,
                            )
                        elif url_type == "wishlist":
                            review_product_id = int(
                                review.get_attribute("data-vintage-id")
                            )
                        
                            yield WishlistItem(
                                cmp_id = review_product_id,
                                product_name = review_product,
                                product_link = review_product_link,
                                product_year = review_product_year,
                                product_developer = review_developer_name,
                                product_developer_link = review_developer_link,
                                price = review_product_price,
                                currency = review_product_price_currency,
                                region = review_product_region_name,
                                region_link = review_product_region_link,
                                country = review_product_country_name,
                                country_link = review_product_country_link
                            )

                divs = driver.find_elements("css selector", "div.show-more")
                if divs and (click:=divs[0].find_element("css selector", btn_class)) and click.size.get("height") > 0:
                    click.click()
                    driver.implicitly_wait(1)
                else:
                    break
            
    def parse(self, response, url_type:str):
        with Driver(url=response.url) as driver:
            if url_type == 'review':
                self._develop_all_records(
                    driver,
                    "button#btn-more-activities"
                )
                reviews = WebDriverWait(driver, 100).until(
                    EC.presence_of_all_elements_located(
                        (
                            "css selector", 
                            "div.user-activity-item"
                        )
                    )
                )
            elif url_type == 'wishlist':
                self._develop_all_records(
                    driver,
                    "button.btn.btn-default.btn-md.btn-distinct.btn-flow"
                )
                reviews = driver.find_elements(
                    "css selector", 
                    "div.activity-wine-card.activity-section.clearfix"
                )
            
            for review in reviews:
                review_developer_link, review_developer_name = self._get_review_link(
                    review.find_element("css selector", "span.text-small > a.link-muted")
                )
                review_product_link, review_product = self._get_review_link(
                    review.find_element("css selector", "p.wine-name > a.link-muted.bold")
                )
                review_product_year = self._get_review_product_year(
                    review_product, 
                    review.find_element("css selector", "p.wine-name").text
                )
                
                region_country = [
                    self._get_review_link(i)
                    for i in review.find_elements("css selector", "div.wine-info > div.text-mini > a")
                ]
                if region_country:
                    review_product_region, review_product_country = region_country
                    review_product_region_link, review_product_region_name = review_product_region
                    review_product_country_link, review_product_country_name = review_product_country
                else:
                    review_product_region_link, review_product_region_name = None, None
                    review_product_country_link, review_product_country_name = None, None

                review_product_price = self._get_review_product_price(
                    review.find_element(
                        "css selector", 
                        "span.header-large.text-block.wine-info-value.wine-price-value"
                    ).text
                )
                review_product_price_currency = self._get_review_product_currency(
                    review.find_elements(
                        "css selector", 
                        "span.text-block.text-micro.wine-price-currency"
                    )
                )

                if url_type == "review":
                    review_product_id = int(
                        review.find_element(
                            "css selector", 
                            "div.activity-wine-card.activity-section.clearfix"
                        ).get_attribute("data-vintage-id")
                    )
                    review_datetime = review.find_element("css selector", "a.link-muted.bold.inflate").get_attribute("title")
                    review_likes = int(
                        review.get_attribute("data-likes-count")
                    )
                    review_id = int(
                        review.get_attribute("data-id")
                    )
                    review_text = review.find_element("css selector", "p.tasting-note.text-larger").text
                    review_score = self._get_review_number(
                        [
                            i.get_attribute("class") for i in 
                            review.find_elements("css selector", "span.rating.rating-xs.text-inline-block > i")
                        ]
                    )
                    yield ReviewItem(
                        review_id = review_id,
                        review_datetime=review_datetime,
                        likes = review_likes,
                        text = review_text,
                        score = review_score,
                        cmp_id = review_product_id,
                        product_name = review_product,
                        product_link = review_product_link,
                        product_year = review_product_year,
                        product_developer = review_developer_name,
                        product_developer_link = review_developer_link,
                        price = review_product_price,
                        currency = review_product_price_currency,
                        region = review_product_region_name,
                        region_link = review_product_region_link,
                        country = review_product_country_name,
                        country_link = review_product_country_link,
                    )
                elif url_type == "wishlist":
                    review_product_id = int(
                        review.get_attribute("data-vintage-id")
                    )
                
                    yield WishlistItem(
                        cmp_id = review_product_id,
                        product_name = review_product,
                        product_link = review_product_link,
                        product_year = review_product_year,
                        product_developer = review_developer_name,
                        product_developer_link = review_developer_link,
                        price = review_product_price,
                        currency = review_product_price_currency,
                        region = review_product_region_name,
                        region_link = review_product_region_link,
                        country = review_product_country_name,
                        country_link = review_product_country_link
                    )