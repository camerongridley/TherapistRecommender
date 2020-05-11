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

    # def select_age_group_id(self, value:str)->int:
    #     self.cur.execute('''SELECT age_group_id FROM age_groups WHERE age_group=%(age_group)s;''',
    #         {'age_group':value}
    #         )
    #     value_id = self.cur.fetchone()[0]
    #     return value_id

    # def select_issue_id(self, value:str)->int:
    #     self.cur.execute('''SELECT issue_id FROM issues WHERE issue=%(issue)s;''',
    #         {'issue':value}
    #         )
    #     value_id = self.cur.fetchone()[0]
    #     return value_id

    # def select_orientation_id(self, value:str)->int:
    #     self.cur.execute('''SELECT orientation_id FROM orientations WHERE orientation=%(orientation)s;''',
    #         {'orientation':value}
    #         )
    #     value_id = self.cur.fetchone()[0]
    #     return value_id

    # def select_profession_id(self, value:str)->int:
    #     self.cur.execute('''SELECT profession_id FROM professions WHERE profession=%(profession)s;''',
    #         {'profession':value}
    #         )
    #     value_id = self.cur.fetchone()[0]
    #     return value_id

    # def select_service_id(self, value:str)->int:
    #     self.cur.execute('''SELECT service_id FROM services WHERE service=%(service)s;''',
    #         {'service':value}
    #         )
    #     value_id = self.cur.fetchone()[0]
    #     return value_id

    # def insert_therapist_age_groups(self, therapist_id:int, scrapy_item)->None:
    #     for val in scrapy_item.get('age_group_list'):
    #         age_group_id = self.select_age_group_id(val)
    #         self.cur.execute('''INSERT INTO therapist_age_groups VALUES (%(therapist_id)s, %(age_group_id)s);''',
    #         {'therapist_id':therapist_id, 'age_group_id':age_group_id}
    #         )

    # def insert_therapist_issues(self, therapist_id:int, scrapy_item)->None:
    #     for val in scrapy_item.get('issues_list'):
    #         issue_id = self.select_age_group_id(val)
    #         self.cur.execute('''INSERT INTO therapist_issues VALUES (%(therapist_id)s, %(issue_id)s);''',
    #         {'therapist_id':therapist_id, 'issue_id':issue_id}
    #         )
    
    # def insert_therapist_orientations(self, therapist_id:int, scrapy_item)->None:
    #     for val in scrapy_item.get('orientations_list'):
    #         orientation_id = self.select_age_group_id(val)
    #         self.cur.execute('''INSERT INTO therapist_orientations VALUES (%(therapist_id)s, %(orientation_id)s);''',
    #         {'therapist_id':therapist_id, 'orientation_id':orientation_id}
    #         )

    # def insert_therapist_professions(self, therapist_id:int, scrapy_item)->None:
    #     for val in scrapy_item.get('issues_list'):
    #         profession_id = self.select_profession_id(val)
    #         self.cur.execute('''INSERT INTO therapist_professions VALUES (%(therapist_id)s, %(profession_id)s);''',
    #         {'therapist_id':therapist_id, 'profession_id':profession_id}
    #         )

    # def insert_therapist_services(self, therapist_id:int, scrapy_item)->None:
    #     for val in scrapy_item.get('services_list'):
    #         service_id = self.select_service_id(val)
    #         self.cur.execute('''INSERT INTO therapist_services VALUES (%(therapist_id)s, %(service_id)s);''',
    #         {'therapist_id':therapist_id, 'service_id':service_id}
    #         )
            
    # '''Replaced with writing sample just being a col in therapists'''
    # # def insert_therapist_writing_samples(self, therapist_id:int, scrapy_item)->None:
    # #     for val in scrapy_item.get('issues_list'):
    # #         sample_id = self.select_writing_sample_id(val)
    # #         self.cur.execute('''INSERT INTO therapist_writing_samples VALUES (%(therapist_id)s, %(sample_id)s);''',
    # #         {'therapist_id':therapist_id, 'sample_id':sample_id}
    # #         )
    # # def select_writing_sample_id(self, value:str)->int:
    # #     self.cur.execute('''SELECT sample_id FROM writing_samples WHERE sample=%(sample)s;''',
    # #         {'sample':value}
    # #         )
    # #     value_id = self.cur.fetchone()[0]
    # #     return value_id



    # # def insert_therapist_services(self, therapist_id:int, issue_id:int)->None:
    # #     self.cur.execute('''INSERT INTO therapist_issues VALUES (%(therapist_id)s, %(issue_id)s);''',
    # #         {'therapist_id':therapist_id, 'issue_id':issue_id}
    # #         )

    # # def insert_therapist_orientation(self, therapist_id:int, orientation_id:int)->None:
    # #     self.cur.execute('''INSERT INTO therapist_orientations VALUES (%(therapist_id)s, %(orientation_id)s);''',
    # #         {'therapist_id':therapist_id, 'orientation_id':orientation_id}
    # #         )

    # # def insert_therapist_profession(self, therapist_id:int, profession_id:int)->None:
    # #     self.cur.execute('''INSERT INTO therapist_professions VALUES (%(therapist_id)s, %(profession_id)s);''',
    # #         {'therapist_id':therapist_id, 'profession_id':profession_id}
    # #         )

    # # def insert_therapist_service(self, therapist_id:int, service_id:int)->None:
    # #     self.cur.execute('''INSERT INTO therapist_services VALUES (%(therapist_id)s, %(service_id)s);''',
    # #         {'therapist_id':therapist_id, 'service_id':service_id}
    # #         )

    # # def insert_therapist_writing_sample(self, therapist_id:int, writing_sample_id:int)->None:
    # #     self.cur.execute('''INSERT INTO therapist_writing_samples VALUES (%(therapist_id)s, %(writing_sample_id)s);''',
    # #         {'therapist_id':therapist_id, 'writing_sample_id':writing_sample_id}
    # #         )

    # def insert_therapist_info(self, scrapy_item)->int:
    #     #print(f'SCRAPY ITEM FIELD: {scrapy_item}')
    #     self.cur.execute('''INSERT INTO therapists (
    #     first_name, last_name, 
    #     address, primary_credential, 
    #     license_status, website, 
    #     info_source, verified,
    #     writing_sample) 
    #     VALUES (%(first_name)s,%(last_name)s,
    #     %(address)s, %(primary_credential)s,
    #     %(license_status)s, %(website)s,
    #     %(info_source)s, %(verified)s,
    #     %(writing_sample)s) 
    #     RETURNING therapist_id;''',

    #     {
    #     'first_name':scrapy_item.get('first_name'), 'last_name':scrapy_item.get('last_name'), 
    #     'address':scrapy_item.get('address'), 'primary_credential':scrapy_item.get('primary_credential'), 
    #     'license_status':scrapy_item.get('license_status'), 'website':scrapy_item.get('website'),
    #     'info_source':scrapy_item.get('info_source'), 'verified':bool(scrapy_item.get('verified')),
    #     'writing_sample':scrapy_item.get('writing_sample')
        
    #     #These are PsychologyToday fields, ignore for now
    #     #'license_num':int(scrapy_item.get('license_num')), 'license_state':scrapy_item.get('license_state'), 
    #     #'years_in_practice':int(scrapy_item.get('years_in_practice')), 'school':scrapy_item.get('school'),
    #     #'year_graduated':int(scrapy_item.get('year_graduated'))
    #     }
    #     )

    #     return self.cur.fetchone()[0]

    # def insert_age_groups(self, scrapy_item) -> None:
    #     for val in scrapy_item.get('age_group_list'):
    #         self.cur.execute('''INSERT INTO age_groups (age_group) 
    #         VALUES (%s)
    #         ON CONFLICT DO NOTHING
    #         ;''', [val])

    # def insert_issues(self, scrapy_item) -> None:
    #     for val in scrapy_item.get('issues_list'):
    #         self.cur.execute('''INSERT INTO issues (issue) 
    #         VALUES (%s)
    #         ON CONFLICT DO NOTHING
    #         ;''', [val])

    # def insert_orientations(self, scrapy_item) -> None:
    #     for val in scrapy_item.get('orientations_list'):
    #         self.cur.execute('''INSERT INTO orientations (orientation) 
    #         VALUES (%s)
    #         ON CONFLICT DO NOTHING
    #         ;''', [val])
    
    # def insert_professions(self, scrapy_item) -> None:
    #     for val in scrapy_item.get('professions_list'):
    #         self.cur.execute('''INSERT INTO professions (profession) 
    #         VALUES (%s)
    #         ON CONFLICT DO NOTHING
    #         ;''', [val])

    # def insert_services(self, scrapy_item) -> None:
    #     for val in scrapy_item.get('services_list'):
    #         self.cur.execute('''INSERT INTO services (service) 
    #         VALUES (%s)
    #         ON CONFLICT DO NOTHING
    #         ;''', [val])

    # # can't get thise to work, keep getting error: psycopg2.ProgrammingError: syntax error at or near "'table_name'"
    # def insert_something(self, table, therapist_id:int, other_id:int)->None:
    #     # cur.execute('''INSERT INTO therapist_writing_samples VALUES (%(therapist_id)s, %(writing_sample_id)s);''',
    #     #     {'therapist_id':therapist_id, 'writing_sample_id':writing_sample_id}
    #     #     )
    #     sql = 'INSERT INTO %s VALUES (%s, %s);'
    #     self.cur.execute(sql, (table, therapist_id, other_id))

    # def select_something(self, table, id_col, value_col, value):
    #     sql = 'SELECT %s FROM %s WHERE %s=%s;'
    #     self.cur.execute(sql, (id_col, table, value_col, value,))
    #     results = self.cur.fetchall()

    #     return results

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

    start_url = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Jennifer.html'
    good_scraper = GoodTherapySoupScraper(starting_url=start_url, is_local_file=True)
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
    cur.execute('''BEGIN;''')
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
    cur.execute('''COMMIT;''')

    conn.commit()
        
    conn.close()