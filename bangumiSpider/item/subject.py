import scrapy


class SubjectItem(scrapy.Item):
    SubjectId = scrapy.Field()
    SubjectType = scrapy.Field()
