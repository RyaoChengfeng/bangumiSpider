# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook
from bangumiSpider.item.anime import AnimeItem
from bangumiSpider.item.episode import EpisodeItem
from bangumiSpider.config import config
from pymongo import MongoClient


class BangumiAnimeMongoPipelines(object):
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', config.MONGODB_URI)
        db_name = spider.settings.get('MONGODB_DB_NAME', config.MONGODB_DB_NAME)
        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]

    def close_spider(self, spider):
        print("插入完成")
        self.db_client.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        if isinstance(item, AnimeItem):
            item = dict(item)
            self.db[config.AnimePageName].insert_one(item)


class BangumiEpisodeMongoPipelines(object):
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', config.MONGODB_URI)
        db_name = spider.settings.get('MONGODB_DB_NAME', config.MONGODB_DB_NAME)
        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]

    def close_spider(self, spider):
        print("插入完成")
        self.db_client.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        if isinstance(item, EpisodeItem):
            item = dict(item)
            self.db[config.EpisodePageName].insert_one(item)


class BangumiAnimeExcelPipelines(object):
    def __init__(self):
        self.file = 'Excelfile/bangumiAnime.xlsx'
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['bangumiId', 'name', 'chineseName', 'startPlay', 'producer', 'episodeCount'])

    def process_item(self, item, spider):
        # if isinstance(item, AnimeItem):
        item = dict(item)
        line = [item['bangumiId'], item['name'], item['chineseName'], item['startPlay'], item['producer'],
                item['episodeCount']]
        self.ws.append(line)
        print("bangumiAnime.xlsx已生成")
        return item

    def close_spider(self, spider):
        self.wb.save(self.file)  # 保存xlsx文件
