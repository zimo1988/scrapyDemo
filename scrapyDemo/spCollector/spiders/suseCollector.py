# -*- coding: utf-8 -*-
import scrapy
from ftplib import FTP

class SusecollectorSpider(scrapy.Spider):
    # get ftp resource
    name = 'suseCollector'
    handle_httpstatus_list = [404]

    def start_requests(self):
        yield scrapy.Request('ftp://ftp.suse.com/pub/projects/security/cvrf/cvrf-opensuse-su-2015%3A0226-1.xml',
                      meta={'ftp_user': 'anonymous', 'ftp_password': ''})

    def parse(self, response):
        print (response.body)

