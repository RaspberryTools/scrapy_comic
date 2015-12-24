# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class ComicItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    episode = Field()
    img_num = Field()
    image_urls = Field()
    image = Field()
