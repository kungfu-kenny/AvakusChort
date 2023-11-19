from scrapy import (
    Spider, 
    Request,
)
import traceback
from time import sleep
from datetime import datetime
from utils.selenium_webdriver import (
    Driver,
    EC,
    WebDriverWait,
)
from avakus.items import (
    get_cmp_ids,
    TweetItem,
    TweetProfileItem,    
)


class NitterParser(Spider):
    name = 'scrape_nitter_tweets'

    def start_requests(self):
        yield Request(
            url='https://nitter.net/AvakovArsen',
            callback=self.parse,

        )

    @staticmethod
    def select_element(driver:object, css_selector:str) -> object:
        if (element:=driver.find_elements(
            "css selector",
            css_selector
            )
        ):
            return element[0]
        return None

    @staticmethod
    def select_number(element:object) -> int:
        if element and (i:=element.text.strip()):
            return int(i.replace(',', ''))
        return None

    @classmethod
    def select_posts(cls:object, driver:object) -> list:
        posts = []
        for element in WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (
                    "css selector",
                    "div.timeline-item"
                )
            )
        ):
            datetime_link = cls.select_element(element, "span.tweet-date > a")
            post_parameters = element.find_elements("css selector", "span.tweet-stat")
            post_link = i.get_attribute("href") if (i:=datetime_link) else None
            
            if len(post_parameters) == 5:
                comment_count, retweet, quote, like, watch = post_parameters
            elif len(post_parameters) == 4:
                watch = None
                comment_count, retweet, quote, like = post_parameters
            else:
                comment_count, retweet, quote, like, watch = None, None, None, None, None
            posts.append(
                {
                    "post_id": int(post_link.split("/status/")[-1].split("#m")[0]) if post_link else None,
                    "post_link": post_link,
                    "post_time": i.get_attribute("title") if (i:=datetime_link) else None,
                    "post_comment_count": cls.select_number(comment_count),
                    "post_retweet_count": cls.select_number(retweet),
                    "post_like_count": cls.select_number(like),
                    "post_quote_count": cls.select_number(quote),
                    "post_watch_count": cls.select_number(watch),
                    "post_text": i.text.strip() if (i:=cls.select_element(element, "div.tweet-content.media-body")) else None,
                }   
            )
        return posts

    @staticmethod
    def select_next(driver:object) -> tuple:
        if (next:=driver.find_elements("css selector", "div.show-more > a")):
            if next[-1] and next[-1].text.strip() == "Load more":
                return True, next[-1].get_attribute("href")
        return False, None

    def parse(self, response):
        list_tweets = get_cmp_ids(TweetItem.file_path, 'post_id')
        with Driver(url=response.request.url) as driver:
            next_page = True
            while next_page:
                for post in self.select_posts(driver):
                    if (
                        not post.get("post_id") or
                        post.get("post_id") in list_tweets
                    ):
                        continue
                    yield TweetItem(
                        post_id = post.get("post_id"),
                        post_link = post.get("post_link"),
                        post_time = post.get("post_time"),
                        post_comment_count = post.get("post_comment_count"),
                        post_retweet_count = post.get("post_retweet_count"),
                        post_like_count = post.get("post_like_count"),
                        post_quote_count = post.get("post_quote_count"),
                        post_watch_count = post.get("post_watch_count"),
                        post_text = post.get("post_text")
                    )
                
                next_page, next_page_link = self.select_next(driver)
                if not next_page_link:
                    next_page = False
                else:
                    sleep(0.4)
                    driver.get(next_page_link)
            profile = self.select_element(driver, 'a.profile-card-fullname')
            
            yield TweetProfileItem(
                profile_datetime_check = datetime.utcnow().strftime("%c"),
                profile_name = profile.get_attribute("title") if profile else None,
                profile_link = profile.get_attribute("href") if profile else None,
                profile_username = i.text.strip() if \
                    (i:=self.select_element(driver, "a.profile-card-username")) else None,
                profile_description = i.text.strip() if \
                    (i:=self.select_element(driver, "div.profile-bio > p")) else None,
                profile_location = i.text.strip() if \
                    (i:=self.select_element(driver, "div.profile-location")) else None,
                profile_website = i.text.strip() if \
                    (i:=self.select_element(driver, "div.profile-website")) else None,
                profile_joindate = i.text.strip() if \
                    (i:=self.select_element(driver, "div.profile-joindate")) else None,
                profile_tweets = self.select_number(i) if \
                    (i:=driver.find_element("css selector","li.posts > span.profile-stat-num")) else None,
                profile_following = self.select_number(i) if \
                    (i:=driver.find_element("css selector","li.following > span.profile-stat-num")) else None,
                profile_followers = self.select_number(i) if \
                    (i:=driver.find_element("css selector","li.followers > span.profile-stat-num")) else None,
                profile_likes = self.select_number(i) if \
                    (i:=driver.find_element("css selector","li.likes > span.profile-stat-num")) else None,
                profile_image_stats = i.text.strip() if \
                    (i:=self.select_element(driver, "div.photo-rail-header")) else None,
            )