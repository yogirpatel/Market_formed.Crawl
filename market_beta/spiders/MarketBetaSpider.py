# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector	 
from market_beta.items import MarketBetaItem
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
import re
from scrapy.contrib.loader.processor import Compose, MapCompose
from w3lib.html import replace_escape_chars, remove_tags


class MarketBetaSpider(CrawlSpider):
   # print ("MBS2 Start")
    name = 'products'
    allowed_domains = ['market.beta.formed.org']
    start_urls = [
        'https://market.beta.formed.org/shop-products/watch.html','https://market.beta.formed.org/shop-products/listen.html','https://market.beta.formed.org/shop-products/formed-subscriptions.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        item = MarketBetaItem()
        #item.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)		
        item['url'] = response.request.url     			
        item['title'] = hxs.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[2]/h1/span/text()[normalize-space()]').extract()		
        item['subTitle'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[2]/p/text()[normalize-space()]').extract()	    
        item['productInfoMediaDetails'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[3]/text()[normalize-space()]').extract()
        item['description'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/div[1]/p[1]/span/text()[normalize-space()]').extract() + hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/text()[normalize-space()]').extract() + hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/div[1]/p[1]/text()[normalize-space()]').extract() + hxs.xpath('.//*[@id="product__description"]/div[1]/p/text()[normalize-space()]').extract()
        item['relatedProduct1'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[5]/div/div[2]/div/ol/li[1]/div/div/strong/a/text()[normalize-space()]').extract()
        item['relatedProduct2'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[5]/div/div[2]/div/ol/li[2]/div/div/strong/a/text()[normalize-space()]').extract()
        item['onDemand'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[4]/div[1]/div[1]/div[2]/text()[normalize-space()]').extract() 
        item['rent'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[4]/div[1]/div[2]/div[2]/form/div[1]/div/div/div/div/div[1]/label/text()[normalize-space()]').extract()
        item['price'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[4]/div[1]/div[2]/div[2]/form/div[1]/div/div/div/div/div[2]/label/text()[normalize-space()]').extract() 
	    #NOTE:  ALSO SHOWING AS //*[@id="options-1360-list"]/div[1]/label
        item['director'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/div[2]/text()[1][normalize-space()]').extract()   item['publisher'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/div[2]/text()[2][normalize-space()]').extract()  	
        yield item
        # Now Recurse
        page = response.url
        domain = urlparse(page).netloc
        le = LinkExtractor()
        for link in le.extract_links(response):
            if link.url == 'https://market.beta.formed.org/shop-products/watch.html':
                        yield {'link':link,'domain': domain}
                        print ("*************** ")					
            elif link.url == 'https://market.beta.formed.org/shop-products/listen.html':
						yield {'link':link,'domain': domain}
						print ("*************** ")				
            elif link.url == 'https://market.beta.formed.org/shop-products/formed-subscriptions.html':
						yield {'link':link,'domain': domain}
						print ("*************** ")
						#print('MBS2- following %s from %s', link, domain)
				
