import json

import scrapy
from scrapy import FormRequest
from scrapy.crawler import CrawlerProcess
from itertools import cycle


class WikifiedText(scrapy.Item):
    text = scrapy.Field()
    entities = scrapy.Field()


class BrankWikifier(scrapy.Spider):
    name = 'gus_variables'

    custom_settings = {'FEED_FORMAT': 'jsonlines',
                       'FEED_URI': 'wikified.jl'}
    base_url = 'http://www.wikifier.org/annotate-article'
    # TODO This should be passed as a parameter through setup
    user_keys = ('vanfmxwemngacoystnhmrlcblktwvs',
                 'hymvsuyrmtismqnuwuwmqmslrqzplf',
                 'ysklqjwqxjkiqrazohwkqvrgatufww',
                 'lzxoilwzmflmnxmiuwznbaffwhsjrh',
                 'ffbsyckziuogmlsjdzmjzicslwyymj',
                 'nahxvoprkelotojpggokmawboelnjy')
    proportion = 0.5

    def start_requests(self):
        user_keys = cycle(self.user_keys)
        for text in self.texts:
            params = {
                'userKey': next(user_keys),
                'text': text,
                'nTopDfValuesToIgnore': str(200)  # TODO Make it configurable
            }
            yield FormRequest(self.base_url,
                              self.parse,
                              formdata=params,
                              meta={'text': text})

    def parse(self, response):
        content = json.loads(response.body_as_unicode())
        text = response.meta['text']
        yield from self._handle(content, text)

    def _handle(self, content, text):

        def is_valid_annotation(ann):
            return (ann['cosine'] >= -1
                    and len(ann['support']) > 0
                    and ann['pageRank'] >= 0)

        total_page_rank = sum(ann['pageRank']
                              for ann
                              in content['annotations']
                              if is_valid_annotation(ann))
        max_cum_page_rank = self.proportion * total_page_rank
        cum_page_rank = 0
        valid_annotations = filter(is_valid_annotation, content['annotations'])
        top = sorted(valid_annotations,
                     key=lambda ann: ann['pageRank'],
                     reverse=True)

        entities = []
        for ann in top:
            # TODO Remove stop words
            support = ann['support'][0]  # TODO only first?
            phrase = text[support['chFrom']:support['chTo'] + 1]
            e = {}
            e['phrase'] = phrase
            e['kb_url'] = ann['url']
            e['kb_id'] = ann['wikiDataItemId']
            entities.append(e)
            cum_page_rank += ann['pageRank']
            if cum_page_rank >= max_cum_page_rank:
                break

        wikified = WikifiedText()
        wikified['text'] = text
        wikified['entities'] = entities

        yield wikified


def wikify(texts):
    # TODO Log also review id
    process = CrawlerProcess(settings=get_settings(), install_root_handler=True)
    process.crawl(BrankWikifier, texts=texts)
    process.start()


def get_settings(api_key=None):
    settings = {
        'CONCURRENT_REQUESTS': 10,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'DOWNLOAD_DELAY': 2,
        'DOWNLOADER_STATS': True,
    }
    return settings
