# -*- coding: utf-8 -*-

import sys
from exporters import XmlVocabularyListItemExporter

__author__ = 'benediktsuessmann'


class XmlExportPipeline(object):

    def process_item(self, item, spider):

        file = open('%s_%s.xml' % (item['category'], item['topic']), 'w+b')

        self.exporter = XmlVocabularyListItemExporter(file, item_element='vocabularylist',
                                                      root_element='vocabularylists')
        self.exporter.start_exporting()
        self.exporter.export_item(item)
        self.exporter.finish_exporting()
        file.close()

        return item
