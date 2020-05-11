import scrapy
from os import listdir
from os.path import isfile, join
from ..items import TherapistItem
from ..good_therapy_scraper import GoodTherapySoupScraper

class GoodTherapySpider(scrapy.Spider):
    name = "goodtx"

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.search_results_file_paths = self.get_search_results_paths()

    #'https://www.goodtherapy.org/search2.html?search[therapist_search]=Find%20a%20Therapist&search[state]=&search[zipcode]=denver,%20colorado&search[lat]=39.7392358&search[lon]=-104.990251&search[miles]=25&search[city_log]=Denver&search[city_log_short]=Denver&search[state_log]=Colorado&search[state_log_short]=CO&search[country_log]=United%20States&search[country_log_short]=US&search[p]=19'
    #start_urls = ["file:///home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Denver/SearchResults1.html"]
    start_urls = ['file:///home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/ShortResults.html']
    #start_urls = ['https://www.goodtherapy.org/therapists/profile/jessica-fern-cooley-20170717']
    #scrapy shell file:///home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Denver/SearchResults1.html
    #start_urls = self.search_results_file_paths

    # can use the start_urls class var instead of the start_requests() method
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def get_search_results_paths(self)->list:
        #mypath = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Denver/'
        mypath = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/'
        prefix = 'file://'
        return [(prefix + mypath + f) for f in listdir(mypath) if isfile(join(mypath, f))]

    # pass therapist info dict received from GoodTherapyScraper.get_all_data()
    def build_therapist_item(self, therapist_info_dict:dict):
        therapist_item = TherapistItem()
        therapist_item['full_name'] = therapist_info_dict['full_name']
        therapist_item['first_name'] = therapist_info_dict['first_name']
        therapist_item['last_name'] = therapist_info_dict['last_name']
        therapist_item['street'] = therapist_info_dict['street']
        therapist_item['city'] = therapist_info_dict['city']
        therapist_item['state'] = therapist_info_dict['state']
        therapist_item['zip_code'] = therapist_info_dict['zip_code']
        therapist_item['phone'] = therapist_info_dict['phone']
        therapist_item['primary_credential'] = therapist_info_dict['primary_credential']
        therapist_item['license_status'] = therapist_info_dict['license_status']
        therapist_item['website'] = therapist_info_dict['website']
        therapist_item['info_source'] = therapist_info_dict['info_source']
        therapist_item['verified'] = therapist_info_dict['verified']
        therapist_item['age_group_list'] = therapist_info_dict['age_group_list']
        therapist_item['issues_list'] = therapist_info_dict['issues_list']
        therapist_item['orientations_list'] = therapist_info_dict['orientations_list']
        therapist_item['professions_list'] = therapist_info_dict['professions_list']
        therapist_item['services_list'] = therapist_info_dict['services_list']
        therapist_item['writing_sample'] = therapist_info_dict['writing_sample']

        return therapist_item

    '''The parse() method usually parses the response, extracting the scraped data as dicts 
    and also finding new URLs to follow and creating new requests (Request) from them.'''
    # Loops through a list of search results pages, finding and following the links for all
    # of the therapist's profiles so they can be scraped
    def parse(self, response):
        
        # In a therapist search result page, links to individual profile pages are found in the tags 'div.therapist_middle_section'
        profile_links = response.css('div.therapist_middle_section a::attr(href)').getall()
        print(f'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ - {profile_links}')
        

        
        for link in profile_links:
            
            # title = quote.css('span.text::text').extract()
            # author = quote.css('.author::text').extract()
            # tag = quote.css('.tag::text').extract()

            good_tx_scraper = GoodTherapySoupScraper(link, False)
            soup = good_tx_scraper.get_soup()
            therapist_info_dict = good_tx_scraper.get_all_data(soup)
            therapist_item = self.build_therapist_item(therapist_info_dict)
            # #Build Scrapy Item
            # therapist_item['full_name'] = therapist_info_dict['full_name']
            # therapist_item['first_name'] = therapist_info_dict['first_name']
            # therapist_item['last_name'] = therapist_info_dict['last_name']
            # therapist_item['address'] = therapist_info_dict['address']
            # #therapist_item['phone'] = therapist_info_dict['phone']
            # therapist_item['primary_credential'] = therapist_info_dict['primary_credential']
            # therapist_item['license_status'] = therapist_info_dict['license_status']
            # therapist_item['website'] = therapist_info_dict['website']
            # therapist_item['info_source'] = therapist_info_dict['info_source']
            # therapist_item['verified'] = therapist_info_dict['verified']
            # therapist_item['age_group_list'] = therapist_info_dict['age_group_list']
            # therapist_item['issues_list'] = therapist_info_dict['issues_list']
            # therapist_item['orientations_list'] = therapist_info_dict['orientations_list']
            # therapist_item['professions_list'] = therapist_info_dict['professions_list']
            # therapist_item['services_list'] = therapist_info_dict['services_list']
            # therapist_item['writing_sample'] = therapist_info_dict['writing_sample']
            
            #PsychologyToday-specific fields
            # therapist_item['license_num'] = therapist_info_dict['license_num']
            # therapist_item['license_state'] = therapist_info_dict['license_state']
            # therapist_item['years_in_practice'] = therapist_info_dict['years_in_practice']
            # therapist_item['school'] = therapist_info_dict['school']
            # therapist_item['year_graduated'] = therapist_info_dict['year_graduated']
            
            yield therapist_item
            
        # For now, there are no pages to follow
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