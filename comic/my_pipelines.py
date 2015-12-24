# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagePipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url in item['image_urls']:
            # 这里我把item传过去,因为后面需要用item里面的书名和章节作为文件名
            yield scrapy.Request(img_url, meta={'item': item})
    def item_completed(self, results, item, info):
        print results
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        # 从URL提取图片的文件名
        img_name = str(item['img_num']) + '.' + item['image_urls'][0].split('.')[-1]

        filepath = item['name'] + '/' + item['episode'] + '/' + img_name
        return filepath
