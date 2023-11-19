from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


@defer.inlineCallbacks
def run_scraping(
    runner: CrawlerRunner,
):
    #1. Tweets and statistics
    yield runner.crawl("scrape_nitter_tweets")

    #2. Vivino rewiews
    yield runner.crawl('scrape_vivino_reviews')

    #3. Vivino wishlists
    yield runner.crawl('scrape_vivino_wishlist')

    reactor.stop()


def main():
    configure_logging()
    settings = get_project_settings()
    settings.update(
        {
            "CONCURRENT_REQUESTS": 1,
            "CONCURRENT_REQUESTS_PER_IP": 1,
        }
    )
    try:
        run_scraping(
            runner=CrawlerRunner(
                settings
            ),
        )
        reactor.run()
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
