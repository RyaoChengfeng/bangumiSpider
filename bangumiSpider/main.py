from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import cmdline

if __name__ == '__main__':
    # cmdline.execute('scrapy crawl bangumiSubjectSpider'.split())
    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl('bangumiSubjectSpider')
    # crawler.crawl('bangumiAnimeSpider')
    # crawler.crawl('bangumiEpisodeSpider')
    # crawler.crawl('爬虫名3')
    crawler.start()
