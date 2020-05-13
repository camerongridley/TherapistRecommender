import requests
import psycopg2
import scrapy
from items import TherapistItem
#from sql_inserts import SqlInserts
#from sql_selects import SqlSelects
from sql_queries import SqlQueries
from good_therapy_scraper import GoodTherapySoupScraper

class SqlTest(object):
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

if __name__ == '__main__':
    conn = psycopg2.connect(dbname='therapist_predictor', user='postgres', host='localhost', password='password')
    cur = conn.cursor()

    sql_test = SqlQueries(conn, cur)

    # mock lists standing in for scraped data in order to build a test scrapy item
    age_groups_list = ['group 1','group 2']
    issue_list = ['issue 1', 'issue 2']
    orientations_list = ['orientation 1', 'orientation 2']
    professions_list = ['profession 1', 'profession 2']
    services_list = ['service 1', 'service 2']

    mock_item = TherapistItem()
    mock_item['first_name'] = 'Frodo'
    mock_item['last_name'] = 'Torrence'
    mock_item['full_name'] = mock_item['first_name'] + mock_item['last_name']
    mock_item['street'] = '123 Hobbiton Ln'
    mock_item['city'] = 'The Shire'
    mock_item['state'] = 'CA'
    mock_item['zip_code'] = '84712'
    mock_item['phone'] = '303.763.0282 ext 123'
    mock_item['primary_credential'] = 'Psycho Killer'
    mock_item['license_status'] = 'Active'
    mock_item['website'] = 'www.lotr.com'
    mock_item['info_source'] = 'GoodTherapy.com'
    mock_item['verified'] = 'True'
    mock_item['age_group_list'] = age_groups_list
    mock_item['issues_list'] = issue_list
    mock_item['orientations_list'] = orientations_list
    mock_item['professions_list'] = professions_list
    mock_item['services_list'] = services_list
    mock_item['writing_sample'] = "All work and no play makes Jack a dull boy."

    #these are PsychToday fields, so ignore them for now
    # mock_item['license_num'] = None
    # mock_item['license_state'] = None
    # mock_item['years_in_practice'] = None
    # mock_item['school'] = None
    # mock_item['year_graduated'] = None

    def build_therapist_item(therapist_info_dict:dict):
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

    
    real_url = 'https://www.goodtherapy.org/therapists/profile/eric-eichler-20190613'
    good_scraper = GoodTherapySoupScraper(starting_url=real_url, is_local_file=False)

    #local_url = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Jennifer.html'
    #good_scraper = GoodTherapySoupScraper(starting_url=local_url, is_local_file=True)
    
    

    soup = good_scraper.get_soup()

    all_data = good_scraper.get_all_data(soup)
    real_item = build_therapist_item(all_data)

    item = real_item
    '''********************************************************
    BASIC SQL TESTING
    ********************************************************'''
    # print(sql_test.select_issue_id('Abandonment'))
    # o_id = sql_test.select_orientation_id('Voice Dialogue')
    # print(o_id)
    # sql_test.insert_therapist_orientation(1, o_id)
    #res = sql_test.select_something('orientations', 'orientation_id', 'orientation', 'Voice Dialogue')
    #print(res)
    
    # cur.execute('''BEGIN;''')
    # sql_test.insert_therapist_orientation(1, 3)
    # sql_test.insert_therapist_orientation(1, 2000)
    # cur.execute('''COMMIT;''')

    '''********************************************************
    THERAPIST TABLE TESTING
    ********************************************************'''
    breakpoint()
    sql_test.select_full_name(item['full_name'])
    therapist_id = sql_test.insert_therapist_info(item)
    print(f'Therapist ID: {therapist_id}')

    '''********************************************************
    SUPPORT TABLE TESTING
    ********************************************************'''

    
    sql_test.insert_age_groups(item)
    sql_test.insert_issues(item)
    sql_test.insert_orientations(item)
    sql_test.insert_professions(item)
    sql_test.insert_services(item)

    #therapist_id = 13
    sql_test.insert_therapist_age_groups(therapist_id, item)
    sql_test.insert_therapist_issues(therapist_id, item)
    sql_test.insert_therapist_orientations(therapist_id, item)
    sql_test.insert_therapist_professions(therapist_id, item)
    sql_test.insert_therapist_services(therapist_id, item)

    conn.commit()
        
    conn.close()