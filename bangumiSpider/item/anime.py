import scrapy


class AnimeItem(scrapy.Item):
    bangumiId = scrapy.Field()
    name = scrapy.Field()
    chineseName = scrapy.Field()
    startPlay = scrapy.Field()
    producer = scrapy.Field()
    episodeCount = scrapy.Field()
