import scrapy
from bangumiSpider.spiders import SpiderDebug
from bangumiSpider.item.anime import AnimeItem
from bangumiSpider.item.episode import EpisodeItem
from bangumiSpider.item.subject import SubjectItem
from bangumiSpider.config import config
import json


class BangumiSubjectSpider(scrapy.Spider):
    name = 'bangumiSubjectSpider'
    allowed_domains = ['bgm.tv']
    start_urls = []
    id = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not SpiderDebug:
            self.start_urls = ['http://api.bgm.tv/subject/%s?responseGroup=large' % str(self.id)]
        else:
            self.start_urls = ['http://api.bgm.tv/subject/200?responseGroup=large']

    def parse(self, response):
        subject = SubjectItem()
        body = json.loads(response.body)
        subject['SubjectId'] = int(body['id'])
        subject['SubjectType'] = int(body['type'])
        if subject['SubjectType'] == 2:
            anime = AnimeItem()
            anime['bangumiId'] = subject['SubjectId']
            anime['name'] = body["name"].encode("utf-8").decode("utf-8")
            anime['chineseName'] = body["name_cn"].encode("utf-8").decode("utf-8")
            anime['startPlay'] = body["air_date"]
            anime['episodeCount'] = int(body["eps_count"])
            staff = body["staff"]
            producer = ''
            for stf in staff:
                for st in stf['jobs']:
                    if st.encode("utf-8").decode("utf-8") == "导演":
                        producer += (str(stf['name'].encode("utf-8").decode("utf-8"))) + ','
            anime['producer'] = producer[:-1]
            yield anime

            for e in body['eps']:
                ep = EpisodeItem()
                ep['aid'] = int(anime['bangumiId'])
                ep['epid'] = int(e['id'])
                ep['name'] = e['name'].encode("utf-8").decode("utf-8")
                ep['chineseName'] = e['name_cn'].encode("utf-8").decode("utf-8")
                ep['startPlay'] = e['airdate']
                ep['duration'] = e['duration']
                ep['sort'] = int(e['sort'])
                yield ep

        if self.id < config.SubjectMaxId:
            self.id += 1
            yield scrapy.Request(url='http://api.bgm.tv/subject/%s?responseGroup=large' % str(self.id),
                                 callback=self.parse)
