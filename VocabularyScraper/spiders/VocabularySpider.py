# -*- coding: utf-8 -*-

import scrapy
from VocabularyScraper.items import VocabularyList, Vocabulary

__author__ = 'benediktsuessmann'


class VocabularySpider(scrapy.Spider):
    name = 'vocabularyspider'
    allowed_domains = ['vokabeln.de']
    start_urls = [
        'http://vokabeln.de/v7/download.htm'
    ]

    def parse(self, response):
        categories = response.xpath('//div[@id="col3_content"]/table[1]/tbody/tr[not(@class)]')

        for category in categories:
            anchor = category.xpath('td[1]//a')

            url = response.urljoin(anchor.xpath('@href').extract_first())
            category = anchor.xpath('text()').extract_first()

            request = scrapy.Request(url, callback=self.parse_category_contents)
            request.meta['category'] = category
            yield request

    def parse_category_contents(self, response):
        category = response.meta['category']

        vocabulary_lists = response.xpath(
            '//div[@id="col3_content"]/table[2]/tbody/tr[not(@class)][position() < last()]')

        for vocabulary_list in vocabulary_lists:
            anchor = vocabulary_list.xpath('td[last()]//a[last()]')
            url = response.urljoin(anchor.xpath('@href').extract_first())
            language = vocabulary_list.xpath('td[1]/text()').extract_first()
            topic = vocabulary_list.xpath('td[2]/a/text()').extract_first()

            request = scrapy.Request(url, callback=self.parse_vocabularylist_contents)
            request.meta['category'] = category
            request.meta['language'] = language
            request.meta['topic'] = topic

            yield request

    def parse_vocabularylist_contents(self, response):
        page_content = response.xpath('//div[@id="col3_content"]')

        if not page_content:
            return

        description_table = page_content.xpath('table[3]')
        vocabulary_groups = page_content.xpath('table[position() > 3]')
        description = self._get_list_description(description_table, response.meta['language'], response.meta['topic'])

        vocabulary_list = VocabularyList()
        vocabulary_list['category'] = response.meta['category']
        vocabulary_list['language'] = response.meta['language']
        vocabulary_list['topic'] = response.meta['topic']
        vocabulary_list['description'] = description
        vocabulary_list['vocabularies'] = []

        vocabulary_list['vocabularies'].append(Vocabulary(language1="Englisch", language2="Deutsch"))

        return vocabulary_list

    def _get_list_description(self, table, language, topic):
        if not table:
            return None

        description = language + ' - ' + topic

        for row in table.xpath('tbody/tr'):
            if "Inhalt" in row.xpath('td[1]/strong/text()').extract_first():
                description = row.xpath('td[2]/text()').extract_first()

        return description
