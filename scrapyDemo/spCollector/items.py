# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpcollectorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SolutionItem(scrapy.Item):
    id = scrapy.Field()
    solution = scrapy.Field()
