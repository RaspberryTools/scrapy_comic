# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from comic.items import ComicItem
from copy import deepcopy


class comicSpider(scrapy.Spider):
    name = "comic"
    allowed_domains = ["comic.ck101.com"]
    start_urls = (
        'http://comic.ck101.com/comic/6643',
    )

    def parse(self, response):
        if response.xpath('//div[@class="pagination"]'):
            total_num = response.xpath('//div[@class="pagination"]/a/text()').re(r'\d+')[-1]
            total_num = int(total_num)
            urls = [response.url + '/1/0/' + str(i) for i in range(1, total_num+1)]
        else:
            urls = [response.url + '/0/0/1']
        for url in urls:
            r = Request(url, callback=self.parse_pagination)
            print url
            yield r

    def parse_pagination(self, response):
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
        total_num = len(response.xpath('/html/body/div[2]/div[2]/div[2]/select/option'))

        base_url = response.url[:-1]
        episode_pages = [base_url + str(i) for i in range(1, total_num+1)]
        local_item = response.meta['item']

        for index, page in enumerate(episode_pages):
            r = Request(page, callback=self.parse_episode_page)
            item = deepcopy(local_item)
            item['episode'] = episode
            item['img_num'] = index
            item['total_num'] = total_num
            r.meta['item'] = item
            yield r

    def parse_episode_page(self, response):
        item = response.meta['item']
        img_url = response.xpath('//*[@id="defualtPagePic"]/@src').extract()[0]
        item['image_urls'] = [img_url]
        return item

