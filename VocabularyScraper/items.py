# -*- coding: utf-8 -*-

import scrapy


class VocabularyList(scrapy.Item):
    xml_element_name = 'vocabularylist'
    category = scrapy.Field()
    language = scrapy.Field()
    topic = scrapy.Field()
    description = scrapy.Field()
    vocabularies = scrapy.Field()


class WordPool(scrapy.Item):
    xml_element_name = 'wordpool'
    name = scrapy.Field()
    vocabularygroups = scrapy.Field()


class VocabularyGroup(scrapy.Item):
    xml_element_name = 'vocabularygroup'
    number = scrapy.Field()
    vocabularies = scrapy.Field()


class Vocabulary(scrapy.Item):
    xml_element_name = 'vocabulary'
    language1 = scrapy.Field()
    language2 = scrapy.Field()
