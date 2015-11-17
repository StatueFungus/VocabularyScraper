# -*- coding: utf-8 -*-

from collections import OrderedDict

import scrapy

from VocabularyScraper.items import VocabularyList, WordPool, VocabularyGroup, Vocabulary

__author__ = 'benediktsuessmann'


class VocabularySpider(scrapy.Spider):
    name = 'vocabularyspider'
    allowed_domains = ['vokabeln.de']
    start_urls = [
        'http://vokabeln.de/v7/download.htm'
    ]

    def parse(self, response):
        """
        parses all categories and searches a link to each
        """

        categories = response.xpath('//div[@id="col3_content"]/table[1]/tbody/tr[not(@class)]')

        for category in categories:
            anchor = category.xpath('td[1]//a')

            url = response.urljoin(anchor.xpath('@href').extract_first())
            category = anchor.xpath('text()').extract_first()

            # request the category page
            request = scrapy.Request(url, callback=self.parse_category_contents)
            request.meta['category'] = category
            yield request

    def parse_category_contents(self, response):
        """
        parses a category page and searchs for links to each vocabularylist inside this category
        """

        category = response.meta['category']

        vocabulary_lists = response.xpath(
            '//div[@id="col3_content"]/table[2]/tbody/tr[not(@class)][position() < last()]')

        for vocabulary_list in vocabulary_lists:
            anchor = vocabulary_list.xpath('td[last()]//a[last()]')
            url = response.urljoin(anchor.xpath('@href').extract_first())
            language = vocabulary_list.xpath('td[1]/text()').extract_first()
            topic = vocabulary_list.xpath('td[2]/a/text()').extract_first()

            #  request the page of the specific vocabulary page
            request = scrapy.Request(url, callback=self.parse_vocabularylist_contents)
            request.meta['category'] = category
            request.meta['language'] = language
            request.meta['topic'] = topic

            yield request

    def parse_vocabularylist_contents(self, response):
        """
        parses the content of a vocabularylist and returns it as a vocabularyListItem
        """

        page_content = response.xpath('//div[@id="col3_content"]')

        if not page_content:
            return

        description_table = page_content.xpath('table[3]')
        vocabulary_groups = page_content.xpath('table[position() > 3]')

        # description of the content in this vocabulary list
        description = self._get_list_description(description_table, response.meta['language'], response.meta['topic'])

        # wordpools are stored in a ordered list to keep the order when exporting them
        word_pools = OrderedDict()
        for vocabulary_group in vocabulary_groups:
            word_pool = self._get_word_pool(vocabulary_group)
            vocabulary_group_item = self._get_vocabulary_group_item(vocabulary_group)

            if word_pool not in word_pools:
                word_pools[word_pool] = WordPool(name=word_pool, vocabularygroups=[])

            word_pools[word_pool]['vocabularygroups'].append(vocabulary_group_item)

        vocabulary_list = VocabularyList()
        vocabulary_list['category'] = response.meta['category']
        vocabulary_list['language'] = response.meta['language']
        vocabulary_list['topic'] = response.meta['topic']
        vocabulary_list['description'] = description
        vocabulary_list['word_pools'] = word_pools.values()

        return vocabulary_list

    def _get_list_description(self, table, language, topic):
        """
        parses the description of a vocabularylist
        """

        if not table:
            return None

        description = language + ' - ' + topic

        for row in table.xpath('tbody/tr'):
            if "Inhalt" in row.xpath('td[1]/strong/text()').extract_first():
                description = row.xpath('td[2]/text()').extract_first()

        return description

    def _get_word_pool(self, vocabulary_group):
        """
        parses the word pool of a vocabularygroup
        """

        vocabulary_group_header = self._get_vocabulary_group_header(vocabulary_group)

        word_pool = "Basiswortschatz"
        return word_pool

    def _get_vocabulary_group_item(self, vocabulary_group):
        """
        parses and returns a vocabulary group
        """

        group_item = VocabularyGroup()
        group_item['number'] = 1
        vocabularies = group_item['vocabularies'] = []
        vocabulary_group_body = self._get_vocabulary_group_body(vocabulary_group)

        for row in vocabulary_group_body:
            vocabulary = self._get_vocabulary_item(row)
            if vocabulary is not None:
                vocabularies.append(vocabulary)

        return group_item

    def _get_vocabulary_item(self, row):
        """
        parses and returns one single vocabulary
        """

        vocabulary = Vocabulary()

        # checks if the table data is not empty
        col1 = row.xpath('td[1]//text()').extract()
        if col1 and col1[0].strip():
            vocabulary['language1'] = col1[0]
            vocabulary['language1_description'] = "\n".join(col1[1:])
        else:
            return None

        # checks if the table data is not empty
        col2 = row.xpath('td[2]//text()').extract()
        if col2 and col2[0].strip():
            vocabulary['language2'] = col2[0]
            vocabulary['language2_description'] = "\n".join(col2[1:])
        else:
            return None

        return vocabulary

    def _get_vocabulary_group_header(self, vocabulary_group):
        """
        returns the tr-element of the vocabulary-group with class='header'
        """

        return vocabulary_group.xpath('tbody/tr[@class="header"]')

    def _get_vocabulary_group_body(self, vocabulary_group):
        """
        returns every tr-element of the vocabulary-group except the first (header)
        """

        return vocabulary_group.xpath('tbody/tr[not(@class="header")]')
