# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from comic.items import ComicItem


class comicSpider(scrapy.Spider):
    name = "comic"
    allowed_domains = ["comic.ck101.com"]
    start_urls = (
        'http://comic.ck101.com/comic/170/0/0/1',
    )

    def parse(self, response):
        name = response.xpath('/html/body/div[4]/div[2]/div[1]/ul/li[3]/h1/text()').extract()[0]
        # filter '/'
        name = name.split('/')[0].strip()
        for episode_url in response.xpath('/html/body/div[4]/div[2]/div[6]/div[1]/ul/li/a/@href').extract():
            episode_url = 'http://comic.ck101.com' + episode_url

            r = Request(episode_url, callback=self.parse_episode)
            item = ComicItem()
            item['name'] = name
            r.meta['item'] = item

            yield r

    def parse_episode(self, response):

        episode = response.xpath('//*[@id="topNav"]/div/div[1]/h2/strong/text()').extract()[0].strip()
        total_image_num = len(response.xpath('/html/body/div[2]/div[2]/div[2]/select/option'))

        base_url = response.url[:-1]
        episode_pages = [base_url + str(i) for i in range(1, total_image_num+1)]

        for index, page in enumerate(episode_pages):
            print page
            r = Request(page, callback=self.parse_episode_page)
            item = response.meta['item']
            item['episode'] = episode
            item['img_num'] = index
            r.meta['item'] = item
            yield r

    def parse_episode_page(self, response):
        item = response.meta['item']
        for img_url in response.xpath('//*[@id="defualtPagePic"]/@src').extract():
            print img_url
            item['image_urls'] = [img_url]
        return item



