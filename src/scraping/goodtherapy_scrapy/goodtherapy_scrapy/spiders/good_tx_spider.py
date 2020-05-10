import scrapy
from ..items import TherapistItem
from ..good_therapy_scraper import GoodTherapySoupScraper

class GoodTherapySpider(scrapy.Spider):
    name = "goodtx"
    #'https://www.goodtherapy.org/search2.html?search[therapist_search]=Find%20a%20Therapist&search[state]=&search[zipcode]=denver,%20colorado&search[lat]=39.7392358&search[lon]=-104.990251&search[miles]=25&search[city_log]=Denver&search[city_log_short]=Denver&search[state_log]=Colorado&search[state_log_short]=CO&search[country_log]=United%20States&search[country_log_short]=US&search[p]=19'
    start_urls = ["file:///home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Denver/SearchResults1.html"]
    #start_urls = ['https://www.goodtherapy.org/therapists/profile/jessica-fern-cooley-20170717']
    #scrapy shell file:///home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Denver/SearchResults1.html


    # can use the start_urls class var instead of the start_requests() method
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    '''The parse() method usually parses the response, extracting the scraped data as dicts 
    and also finding new URLs to follow and creating new requests (Request) from them.'''
    def parse(self, response):
        
        profile_links = response.css('div.therapist_middle_section a::attr(href)').getall()
        therapist_item = TherapistItem()

        
        for link in profile_links:

            # title = quote.css('span.text::text').extract()
            # author = quote.css('.author::text').extract()
            # tag = quote.css('.tag::text').extract()

            soup_scraper = GoodTherapySoupScraper(link).get_soup()
            therapist_info = soup_scraper.getall
            
            print(f'{therapist_info}\n')

            # therapist_items['title'] = title
            # therapist_items['author'] = author
            # therapist_items['tag'] = tag
            
            yield therapist_item
            
        # POTENTIALLY DO A .POP FROM A LIST OF HTML PAGES CREATED AT OBJECT INSTANTIATION
        next_page = None#response.css('li.next a::attr(href)').get()

        if next_page is not None:
            #recursive 
            yield response.follow(next_page, callback=self.parse)

        # default code for scrapy.com tutorial - commented out after doing the builtwithpython youtube tutorial
        # title = response.css('title::text').extract()
        # yield {'titletext' : title} 

        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)