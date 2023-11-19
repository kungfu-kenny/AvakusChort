from scrapy import (
    Spider,
    Request,
)
import traceback
from time import sleep
from utils.selenium_webdriver import (
    Driver,
    EC,
    WebDriverWait,
)
from avakus.items import (
    get_cmp_ids,
    WishlistItem,
)


class VivinoListing(Spider):
    name = "scrape_vivino_wishlist"
    custom_settings = {
        "HTTPERROR_ALLOWED_CODES": [
            403,
            429,
        ],
    }

    def __init__(self):
        self._urls = [
            "https://www.vivino.com/users/arsen-av/wishlist",
        ]

    def start_requests(self):
        for url in self._urls:
            yield Request(
                url=url,
                method="GET",
                callback=self.parse_alternative,
            )

    @staticmethod
    def _get_review_number(stars: list) -> float:
        stars = [int(i.split("-")[1]) for i in stars]
        return float(0.01 * sum(stars))

    @staticmethod
    def _get_review_link(element: object) -> tuple:
        if not element:
            return None, None
        return element.get_attribute("href"), element.text

    @staticmethod
    def _get_review_product_year(name: str, text: str) -> int:
        return (
            int(i)
            if (i := text.split(name)[-1].strip()) and not any(f.isalpha() for f in i)
            else None
        )

    @staticmethod
    def _get_review_product_price(price: str) -> float:
        if not price or price.strip() == "-":
            return None
        return round(float(price.replace(",", ".").replace(" ", "")), 1)

    @staticmethod
    def _get_review_product_currency(curr: str) -> str:
        if not curr:
            return None
        if not curr[0].text:
            return None
        return curr[0].text.strip()

    @staticmethod
    def _develop_all_records(driver: object, btn_class: str) -> None:
        while True:
            driver.implicitly_wait(2.5)
            divs = driver.find_elements("css selector", "div.show-more")
            if (
                divs
                and (click := divs[0].find_element("css selector", btn_class))
                and click.size.get("height") > 0
            ):
                click.click()
                sleep(1)
            else:
                break
        return None

    @staticmethod
    def _load_all(driver, css_selector: str, count: bool = True):
        try:
            return WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(("css selector", css_selector))
                if count
                else EC.presence_of_element_located(("css selector", css_selector))
            )
        except Exception:
            print(traceback.format_exc())
            print("____________________________________________________________")
            return [] if count else None

    def parse_alternative(self, response):
        list_ids = get_cmp_ids(WishlistItem.file_path, 'cmp_id')
        with Driver(url=response.url) as driver:
            items = "div.activity-wine-card.activity-section.clearfix"
            while True:
                driver.execute_script(
                    "arguments[0].scrollIntoView(true);",
                    driver.find_elements("css selector", items)[::-1][0],
                )
                for review in driver.find_elements("css selector", items)[::-1]:
                    driver.execute_script("arguments[0].scrollIntoView(true);", review)
                    review_product_id = int(
                        review.get_attribute("data-vintage-id")
                    )
                    if review_product_id in list_ids:
                        continue

                    list_ids.append(review_product_id)
                    (
                        review_developer_link,
                        review_developer_name,
                    ) = self._get_review_link(
                        self._load_all(
                            review,
                            "span.text-small > a.link-muted",
                            False,
                        )
                    )
                    review_product_link, review_product = self._get_review_link(
                        self._load_all(
                            review,
                            "p.wine-name > a.link-muted.bold",
                            False,
                        )
                    )
                    review_product_year = self._get_review_product_year(
                        review_product,
                        self._load_all(
                            review,
                            "p.wine-name",
                            False,
                        ).text,
                    )
                    region_country = [
                        self._get_review_link(i)
                        for i in self._load_all(
                            review, "div.wine-info > div.text-mini > a"
                        )
                    ]
                    if region_country and len(region_country) == 2:
                        (
                            review_product_region,
                            review_product_country,
                        ) = region_country
                        (
                            review_product_region_link,
                            review_product_region_name,
                        ) = review_product_region
                        (
                            review_product_country_link,
                            review_product_country_name,
                        ) = review_product_country
                    else:
                        (
                            review_product_region_link,
                            review_product_region_name,
                        ) = (
                            None,
                            None,
                        )
                        (
                            review_product_country_link,
                            review_product_country_name,
                        ) = (
                            None,
                            None,
                        )
                    review_product_price = self._get_review_product_price(
                        self._load_all(
                            review,
                            "span.header-large.text-block.wine-info-value.wine-price-value",
                            False,
                        ).text
                    )
                    review_product_price_currency = self._get_review_product_currency(
                        self._load_all(
                            review,
                            "span.text-block.text-micro.wine-price-currency",
                        )
                    )
                    
                    sleep(0.05)
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
                if (
                    (
                        divs := driver.find_elements(
                            "css selector",
                            "div.show-more > button#btn-more",
                        )
                    ) and (click := divs[0])
                    and click.size.get("height") > 0
                ):
                    sleep(0.5) or click.click() or sleep(1.5)
                else:
                    break