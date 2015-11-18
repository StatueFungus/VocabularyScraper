# -*- coding: utf-8 -*-

from collections import OrderedDict

import six
import scrapy
from scrapy.item import ItemMeta, Item

__author__ = 'benediktsuessmann'


class SortedDictItem(Item):
    """
    SortedDictItem is used to keep the order of the inserted elements.
    This is important when you export the item to any structured fileformat (e.g.: XML or JSON)
    """

    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:  # avoid creating dict for most common case
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v


@six.add_metaclass(ItemMeta)
class SortedItem(SortedDictItem):
    pass


class VocabularyList(SortedItem):
    """
    Represents one vocabularylist
    """
    xml_element_name = 'vocabularylist'
    category = scrapy.Field()
    language = scrapy.Field()
    topic = scrapy.Field()
    description = scrapy.Field()
    word_pools = scrapy.Field()


class WordPool(SortedItem):
    """
    Represents a pool of words at the same language-level
    """
    xml_element_name = 'wordpool'
    name = scrapy.Field()
    vocabularygroups = scrapy.Field()


class VocabularyGroup(SortedItem):
    """
    Represents a small group of words inside a wordpool
    """
    xml_element_name = 'vocabularygroup'
    name = scrapy.Field()
    vocabularies = scrapy.Field()


class Vocabulary(SortedItem):
    """
    Represents one single vocabulary
    """
    xml_element_name = 'vocabulary'
    language1 = scrapy.Field()
    language1_description = scrapy.Field()
    language2 = scrapy.Field()
    language2_description = scrapy.Field()
