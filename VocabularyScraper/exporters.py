# -*- coding: utf-8 -*-

import logging
import scrapy
from scrapy.exporters import XmlItemExporter

__author__ = 'benediktsuessmann'


class XmlVocabularyListItemExporter(XmlItemExporter):

    def export_item(self, item, element_name=None):
        if not element_name:
            if hasattr(item, 'xml_element_name'):
                element_name = item.xml_element_name
            else:
                element_name = self.item_element

        self.xg.startElement(element_name, {})
        for name, value in self._get_serialized_fields(item, default_value=''):
            self._export_xml_field(name, value)
        self.xg.endElement(element_name)

    def _export_xml_field(self, name, serialized_value):
        if isinstance(serialized_value, scrapy.Item):
            logging.warning(name)
            self.export_item(serialized_value)

            return

        self.xg.startElement(name, {})

        if hasattr(serialized_value, 'items'):
            for subname, value in serialized_value.items():
                self._export_xml_field(subname, value)
        elif hasattr(serialized_value, '__iter__'):
            for value in serialized_value:
                self._export_xml_field('value', value)
        else:
            self._xg_characters(serialized_value)
        self.xg.endElement(name)