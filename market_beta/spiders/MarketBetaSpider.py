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

        item['url'] = response.request.url
        
        item['title'] = hxs.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[2]/h1/span/text()').extract()
	    
        item['subTitle'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[2]/p/text()').extract()
	    
        item['productInfoMediaDetails'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[3]/text()').extract()
	
        item['description'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/div[1]/p[1]/span/text()').extract() + hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/text()').extract() + hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/div[1]/p[1]/text()').extract() + hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/div[1]/p/text()').extract()
	
        item['relatedProduct1'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[5]/div/div[2]/div/ol/li[1]/div/div/strong/a/text()').extract()
	
        item['relatedProduct2'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[5]/div/div[2]/div/ol/li[2]/div/div/strong/a/text()').extract()
	
        item['onDemand'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[4]/div[1]/div[1]/div[2]/text()').extract() 
    
        item['rent'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[4]/div[1]/div[2]/div[2]/form/div[1]/div/div/div/div/div[1]/label/text()').extract()
	
        item['price'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[4]/div[1]/div[2]/div[2]/form/div[1]/div/div/div/div/div[2]/label/text()').extract() 
	
        #NOTE:  ALSO SHOWING AS //*[@id="options-1360-list"]/div[1]/label
        item['director'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/div[2]/text()[1]').extract()
	
        item['publisher'] = hxs.xpath('//html/body/main/div/main/div[2]/div/div[3]/div[4]/div[2]/text()[2]').extract()
	    
        yield item

        # Now Recurse
        page = response.url
        domain = urlparse(page).netloc
        le = LinkExtractor()
        for link in le.extract_links(response):
            if link.url == 'https://market.beta.formed.org/shop-products/watch.html':
                        yield {'link':link,'domain': domain}
                        print ("*************** ")					
			if link.url == 'https://market.beta.formed.org/shop-products/listen.html':
						yield {'link':link,'domain': domain}
						print ("*************** ")				
			if link.url == 'https://market.beta.formed.org/shop-products/formed-subscriptions.html':
						yield {'link':link,'domain': domain}
						print ("*************** ")
						#print('MBS2- following %s from %s', link, domain)
				
