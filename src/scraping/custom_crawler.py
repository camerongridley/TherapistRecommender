import scrapy
from os import listdir
from os.path import isfile, join
from random import randint
from time import sleep
from bs4 import BeautifulSoup
import psycopg2
from items import TherapistItem
#from pipelines import GoodtherapyScrapyPipeline
from good_therapy_scraper import GoodTherapySoupScraper
import datetime as dt
import pickle

from sql_queries import SqlQueries

class LocalCrawler(object):

    def __init__(self, log_path='../logs'):
        #dir_path = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Denver/'
        self.log_path = log_path

    def get_search_results_paths(self, path:str, prefix='file://')->list:
        #dir_path = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Denver/'
        # dir_path = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/'
        # prefix = 'file://'
        # return [(prefix + dir_path + f) for f in listdir(dir_path) if isfile(join(dir_path, f))]
        self.dir_path = path
        self.prefix = prefix
        self.file_list = [(self.prefix + self.dir_path + f) for f in listdir(self.dir_path) if isfile(join(self.dir_path, f))]

        return self.file_list
        
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

    def scrape_profile_page(self, profile_links):
        sql_pipeline = SqlPipeline()
        sql_pipeline.create_connection()
        logger = Logger(self.log_path)

        # for each profile link, go to that url and scrape the therapist information with GoodTherapySoupScraper class
        for link in profile_links:
            # pause between requests
            sleep(randint(1,3))
            good_tx_scraper = GoodTherapySoupScraper(starting_url=link, is_local_file=False)
            profile_soup = good_tx_scraper.get_soup()
            
            therapist_info_dict = good_tx_scraper.get_all_data(profile_soup)
            if therapist_info_dict is not None:
                therapist_item = self.build_therapist_item(therapist_info_dict)
                #print(therapist_item)
                sql_pipeline.process_item(therapist_item, logger)       

        sql_pipeline.close_connection()
        logger.save_to_file()

    def crawl_pickle_files(self, pickle_files):
        for p in pickle_files:
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(f'@@@@@@@@@@@@@@@@@@@ PICKLE FILE: {p} @@@@@@@@@@@@@@@@@@@')
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            links = pickle.load( open( p, "rb" ) )
            self.scrape_profile_page(links)

    def crawl_local_html_file(self):
        sql_pipeline = SqlPipeline()
        sql_pipeline.create_connection()
        logger = Logger(self.dir_path)

        #sort files for better legibility of log
        self.file_list.sort()

        for f in self.file_list:
            profile_links = []
            str_crawl = f'Crawling page: {f}\n'
            print(str_crawl)
            logger.log_message(str_crawl)

            #get links off page
            # In a therapist search result page, links to individual profile pages are found in the tags 'div.therapist_middle_section'
            links_soup = BeautifulSoup(open(f), "html.parser")
            profile_divs = links_soup.findAll("div", {"class": "therapist_middle_section"})  #response.css('div.therapist_middle_section a::attr(href)').getall()
            for div in profile_divs:
                [profile_links.append(link['href']) for link in div.find_all('a', href=True)]
                
            str_links = f'Found profile links: - {profile_links}\n\n'
            print(str_links)
            logger.log_message(str_links)
            

            self.scrape_profile_page(profile_links)
            # # for each profile link, go to that url and scrape the therapist information with GoodTherapySoupScraper class
            # for link in profile_links:
            #     good_tx_scraper = GoodTherapySoupScraper(link, False)
            #     profile_soup = good_tx_scraper.get_soup()
                
            #     therapist_info_dict = good_tx_scraper.get_all_data(profile_soup)
            #     if therapist_info_dict is not None:
            #         therapist_item = self.build_therapist_item(therapist_info_dict)
            #         #print(therapist_item)
            #         sql_pipeline.process_item(therapist_item, logger)        

        sql_pipeline.close_connection()
        logger.save_to_file()

class SqlPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(dbname='therapist_predictor', user='postgres', host='localhost', password='password')
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    # def select_issue_id(self, issue_name:str)->int:
    #     issue_id = self.cur.execute('''SELECT issue_id FROM issues WHERE issue = %(issue)s;''',
    #         {'issue':issue_name}
    #         )

    #     return issue_id

    def process_item(self, item, logger):
        print("***************************** IN PIPELINE ***************************")
        
        sql  = SqlQueries(self.conn, self.cur)

        # create new therapist and get resulting id
        try:
            # see if thereapist is already in database
            if sql.full_name_exists(item['full_name']) == False:
                therapist_id = sql.insert_therapist_info(item)
                str_creating = f'Created therapist id: {therapist_id} for {item["full_name"]}'
                print(str_creating)
                logger.log_message(str_creating)

                # with therapist id update and insert relational tables
                sql.insert_age_groups(item)
                sql.insert_issues(item)
                sql.insert_orientations(item)
                sql.insert_professions(item)
                sql.insert_services(item)

                sql.insert_therapist_age_groups(therapist_id, item)
                sql.insert_therapist_issues(therapist_id, item)
                sql.insert_therapist_orientations(therapist_id, item)
                sql.insert_therapist_professions(therapist_id, item)
                sql.insert_therapist_services(therapist_id, item)

                self.conn.commit()
                
                str_saved = f'Therapist saved to Postgres: {item.get("full_name")}'
                print(str_saved)
                logger.log_message(str_saved)

            else:
                skipping_msg = f'SKIPPING {item["full_name"]} - Therapist already exists in database.'
                print(skipping_msg)
                logger.log_message(skipping_msg)

        except Exception as e:
            logger.log_message(f'\nPOSTGRES ERROR:{e}')
            print(f'POSTGRES ERROR: {e}')
        
        

        return item

class Logger(object):
    def __init__(self, dir_to_save_file):
        self.dir_to_save_file = dir_to_save_file
        self.log = []

    def log_message(self, message):
        self.log.append(message)

    def print_log(self):
        pass

    def save_to_file(self):
        filename = self.dir_to_save_file + 'therapist_scrape_and_save_log' + str(dt.datetime.now()) + '.txt'
        with open(filename, 'w') as f:
            for item in self.log:
                f.write("%s\n" % item)

if __name__ == '__main__':
    crawler = LocalCrawler()
    # '''
    # Supply the directory that contains the search results files manually saved from GoodTherapy.com.
    # These files contain the links to the therapist found in the seach performed. The cralwer scrapes
    # each of these and saves the profile into the database.
    # '''
    # prefix = ''
    # # include forward slacs('/') at the beginning and end of the path
    # #denver_listings = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Denver/'
    # #boulder_listings = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Boulder/'
    # #springs_listings = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/COSprings/'
    # #ft_collins_listings = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/FortCollins/'
    # #vail_listings = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Vail/'

    # test = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Utah/'

    # cities_lisitings = [test]
    
    # for city in cities_lisitings:

    #     path = city
    #     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    #     print(f'@@@@@@@@@@@@@@@@@@@ CRAWLING {city} @@@@@@@@@@@@@@@@@@@')
    #     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    #     crawler.get_search_results_paths(path, prefix)
    #     crawler.crawl_local_html_file()

    
    pickle_files = ['nyc_links_leftovers_1.pkl']
    crawler.crawl_pickle_files(pickle_files)

