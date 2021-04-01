import scrapy


class EpisodeItem(scrapy.Item):
    aid = scrapy.Field()  # int
    epid = scrapy.Field()  # int
    name = scrapy.Field()
    chineseName = scrapy.Field()
    startPlay = scrapy.Field()
    duration = scrapy.Field()
    sort = scrapy.Field()  # int
