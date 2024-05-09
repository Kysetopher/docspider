from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

class CustomCrawlerProcess(CrawlerProcess):
    def _signal_shutdown(self, signum, _):
        """Shut down the scraping process gracefully."""
        reactor.stop()

    def start(self, stop_after_crawl=True):
        """Start the crawling process without setting up default signal handlers."""
        if stop_after_crawl:
            self._stop_after_crawl()
        reactor.run(installSignalHandlers=False)  # Avoid setting up signal handlers

def run_spider(spider_cls):
    settings = get_project_settings()
    process = CustomCrawlerProcess(settings)
    process.crawl(spider_cls)
    process.start()