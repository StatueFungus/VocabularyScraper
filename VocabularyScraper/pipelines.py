# -*- coding: utf-8 -*-

from scrapy.exporters import XmlItemExporter

__author__ = 'benediktsuessmann'

class XmlExportPipeline(object):

    def process_item(self, item , spider):

        file = open('%s_%s.xml' % (item['category'], item['topic']), 'w+b')
        self.exporter = XmlItemExporter(file)
        self.exporter.start_exporting()
        self.exporter.export_item(item)
        self.exporter.finish_exporting()
        file.close()

        return item

