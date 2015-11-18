# -*- coding: utf-8 -*-

import os
import scrapy

from exporters import XmlVocabularyListItemExporter
from scrapy.exceptions import DropItem

__author__ = 'benediktsuessmann'

"""
Pipelines are called for every item that is returned from the spider.
The settings.py configures which specific pipelines are called and in which order.
"""


class XmlExportPipeline(object):
    """
    Exports an scrapy item to a specific xml file using the XmlVocabularyListItemExporter
    """

    def process_item(self, item, spider):
        category = item['category']
        language = item['language']
        topic = item['topic']

        if not category and language and topic:
            raise DropItem("No VocabularyListItem")

        base_path = "output"

        file_path = '%s/%s/%s/%s.xml' % (base_path,
                                         self._get_valid_dirname(category),
                                         self._get_valid_dirname(language),
                                         self._get_valid_dirname(topic))

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path, 'w+b') as f:
            self.exporter = XmlVocabularyListItemExporter(f, item_element='vocabularylist',
                                                          root_element='vocabularylists')
            self.exporter.start_exporting()
            self.exporter.export_item(item)
            self.exporter.finish_exporting()
            f.close()

        return item

    def _get_valid_dirname(self, name):
        dirname = name;

        dirname = dirname.replace("/", "-")

        return dirname


class ItemStripPipeline(object):
    """
    Pipeline that cleans up the values of the items.
    e.g. removes unnecessary blank spaces
    """

    def process_item(self, item, spider=None):
        for key in item.keys():
            item[key] = self._get_sripped_value(item[key])

        return item

    def _get_sripped_value(self, value):
        if isinstance(value, scrapy.Item):
            return self.process_item(value)

        if hasattr(value, 'items'):
            new_dict = {}

            for k, v in value.items():
                new_dict[k] = self._get_sripped_value(v)

            return new_dict
        elif hasattr(value, '__iter__'):
            new_list = []

            for k in value:
                new_list.append(self._get_sripped_value(k))

            return new_list
        else:
            return self._clean_up_value(value)

    def _clean_up_value(self, value):
        new_value = value

        if type(new_value) is str or type(new_value) is unicode:
            new_value = new_value.strip()
        else:
            new_value = unicode(new_value).strip()

        return new_value
