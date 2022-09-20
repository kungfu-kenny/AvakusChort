from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


@defer.inlineCallbacks
def run_scraping(
    runner: CrawlerRunner,
):
    yield runner.crawl('vivino_listing')

    reactor.stop()


def main():
    configure_logging()
    try:
        run_scraping(
            runner=CrawlerRunner(get_project_settings()),
        )
        reactor.run()
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
