# -*- coding: utf-8 -*-

import os
from exporters import XmlVocabularyListItemExporter

__author__ = 'benediktsuessmann'


class XmlExportPipeline(object):

    def process_item(self, item, spider):

        category = item['category']
        language = item['language']
        topic = item['topic']

        base_path = "output"
        file_path = '%s/%s/%s/%s.xml' % (base_path, category, language, topic)

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
