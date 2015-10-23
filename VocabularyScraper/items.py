# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VocabularyList(scrapy.Item):
    xml_element_name = 'vocabularylist'
    category = scrapy.Field()
    language = scrapy.Field()
    topic = scrapy.Field()
    description = scrapy.Field()
    vocabularies = scrapy.Field()


class Vocabulary(scrapy.Item):
    xml_element_name = 'vocabulary'
    language1 = scrapy.Field()
    language2 = scrapy.Field()
