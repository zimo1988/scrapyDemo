# -*- coding: utf-8 -*-
import scrapy
import re
from spCollector.items import SolutionItem

class SusesolutionSpider(scrapy.Spider):
    name = 'suseSolution'
    start_urls = ['https://lists.opensuse.org/opensuse-security-announce/']

    def parse(self, response):
        for group in response.xpath('//div[@class="year_group"]'):
            for tr in group.xpath('.//tr'):
                item_url = tr.xpath('.//td[3]/a/@href').extract_first()
                if item_url is not None:
                    if int(item_url.split('/')[0].split('-')[0]) > 2014:
                        yield scrapy.Request(url=response.urljoin(item_url), callback=self.parse_subject)

    def parse_subject(self, response):
        for td in response.xpath('//td[@class="msubject"]'):
            item_url = td.xpath('.//a/@href').extract_first()
            if item_url is not None:
                yield scrapy.Request(url=response.url.replace('date.html', item_url), callback=self.parse_item)

    def parse_item(self, response):
        content = response.xpath('//div[@class="body"]').extract_first()
        item = self.parse_solution(response.url, content)
        yield item

    def parse_solution(self, url, content):
        try:
            item = SolutionItem()
            content = content.replace('<br>', '\n')
            match_obj = re.search(r'Announcement ID:.+\n', content, re.M | re.I)
            if match_obj:
                item['id'] = match_obj.group().replace('Announcement ID:', '').strip()
                item['id'] = item['id'] .replace(' ', '')
                match_obj = re.search(r'Patch Instructions:[\s\S]+Package List:', content, re.M | re.I)
                if match_obj:
                    item['solution'] = match_obj.group().replace('Package List:', '').replace('Patch Instructions:', '').strip()
                    item['solution'] = item['solution'].replace('\n\n', '\n').strip()
                    return item
                else:
                    print("Parsing error, html file \"{0}\" is not well-formed".format(url))
            else:
                print("Parsing error, html file \"{0}\" is not well-formed".format(url))

        except:
            print("Parsing error, html file \"{0}\" is not well-formed".format(url))

