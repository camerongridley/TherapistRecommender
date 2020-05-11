import psycopg2
import scrapy
from items import TherapistItem
#from sql_inserts import SqlInserts
#from sql_selects import SqlSelects
from sql_queries import SqlQueries

class SqlTest(object):
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def select_age_group_id(self, value:str)->int:
        self.cur.execute('''SELECT age_group_id FROM age_groups WHERE age_group=%(age_group)s;''',
            {'age_group':value}
            )
        value_id = self.cur.fetchone()[0]
        return value_id

    def select_issue_id(self, value:str)->int:
        self.cur.execute('''SELECT issue_id FROM issues WHERE issue=%(issue)s;''',
            {'issue':value}
            )
        value_id = self.cur.fetchone()[0]
        return value_id

    def select_orientation_id(self, value:str)->int:
        self.cur.execute('''SELECT orientation_id FROM orientations WHERE orientation=%(orientation)s;''',
            {'orientation':value}
            )
        value_id = self.cur.fetchone()[0]
        return value_id

    def select_profession_id(self, value:str)->int:
        self.cur.execute('''SELECT profession_id FROM professions WHERE profession=%(profession)s;''',
            {'profession':value}
            )
        value_id = self.cur.fetchone()[0]
        return value_id

    def select_service_id(self, value:str)->int:
        self.cur.execute('''SELECT service_id FROM services WHERE service=%(service)s;''',
            {'service':value}
            )
        value_id = self.cur.fetchone()[0]
        return value_id

    def insert_therapist_age_groups(self, therapist_id:int, scrapy_item)->None:
        for val in scrapy_item.get('age_group_list'):
            age_group_id = self.select_age_group_id(val)
            self.cur.execute('''INSERT INTO therapist_age_groups VALUES (%(therapist_id)s, %(age_group_id)s);''',
            {'therapist_id':therapist_id, 'age_group_id':age_group_id}
            )

    def insert_therapist_issues(self, therapist_id:int, scrapy_item)->None:
        for val in scrapy_item.get('issues_list'):
            issue_id = self.select_age_group_id(val)
            self.cur.execute('''INSERT INTO therapist_issues VALUES (%(therapist_id)s, %(issue_id)s);''',
            {'therapist_id':therapist_id, 'issue_id':issue_id}
            )
    
    def insert_therapist_orientations(self, therapist_id:int, scrapy_item)->None:
        for val in scrapy_item.get('orientations_list'):
            orientation_id = self.select_age_group_id(val)
            self.cur.execute('''INSERT INTO therapist_orientations VALUES (%(therapist_id)s, %(orientation_id)s);''',
            {'therapist_id':therapist_id, 'orientation_id':orientation_id}
            )

    def insert_therapist_professions(self, therapist_id:int, scrapy_item)->None:
        for val in scrapy_item.get('issues_list'):
            profession_id = self.select_profession_id(val)
            self.cur.execute('''INSERT INTO therapist_professions VALUES (%(therapist_id)s, %(profession_id)s);''',
            {'therapist_id':therapist_id, 'profession_id':profession_id}
            )

    def insert_therapist_services(self, therapist_id:int, scrapy_item)->None:
        for val in scrapy_item.get('services_list'):
            service_id = self.select_service_id(val)
            self.cur.execute('''INSERT INTO therapist_services VALUES (%(therapist_id)s, %(service_id)s);''',
            {'therapist_id':therapist_id, 'service_id':service_id}
            )
            
    '''Replaced with writing sample just being a col in therapists'''
    # def insert_therapist_writing_samples(self, therapist_id:int, scrapy_item)->None:
    #     for val in scrapy_item.get('issues_list'):
    #         sample_id = self.select_writing_sample_id(val)
    #         self.cur.execute('''INSERT INTO therapist_writing_samples VALUES (%(therapist_id)s, %(sample_id)s);''',
    #         {'therapist_id':therapist_id, 'sample_id':sample_id}
    #         )
    # def select_writing_sample_id(self, value:str)->int:
    #     self.cur.execute('''SELECT sample_id FROM writing_samples WHERE sample=%(sample)s;''',
    #         {'sample':value}
    #         )
    #     value_id = self.cur.fetchone()[0]
    #     return value_id



    # def insert_therapist_services(self, therapist_id:int, issue_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_issues VALUES (%(therapist_id)s, %(issue_id)s);''',
    #         {'therapist_id':therapist_id, 'issue_id':issue_id}
    #         )

    # def insert_therapist_orientation(self, therapist_id:int, orientation_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_orientations VALUES (%(therapist_id)s, %(orientation_id)s);''',
    #         {'therapist_id':therapist_id, 'orientation_id':orientation_id}
    #         )

    # def insert_therapist_profession(self, therapist_id:int, profession_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_professions VALUES (%(therapist_id)s, %(profession_id)s);''',
    #         {'therapist_id':therapist_id, 'profession_id':profession_id}
    #         )

    # def insert_therapist_service(self, therapist_id:int, service_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_services VALUES (%(therapist_id)s, %(service_id)s);''',
    #         {'therapist_id':therapist_id, 'service_id':service_id}
    #         )

    # def insert_therapist_writing_sample(self, therapist_id:int, writing_sample_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_writing_samples VALUES (%(therapist_id)s, %(writing_sample_id)s);''',
    #         {'therapist_id':therapist_id, 'writing_sample_id':writing_sample_id}
    #         )

    def insert_therapist_info(self, scrapy_item)->int:
        #print(f'SCRAPY ITEM FIELD: {scrapy_item}')
        self.cur.execute('''INSERT INTO therapists (
        first_name, last_name, 
        address, primary_credential, 
        license_status, website, 
        info_source, verified,
        writing_sample) 
        VALUES (%(first_name)s,%(last_name)s,
        %(address)s, %(primary_credential)s,
        %(license_status)s, %(website)s,
        %(info_source)s, %(verified)s,
        %(writing_sample)s) 
        RETURNING therapist_id;''',

        {
        'first_name':scrapy_item.get('first_name'), 'last_name':scrapy_item.get('last_name'), 
        'address':scrapy_item.get('address'), 'primary_credential':scrapy_item.get('primary_credential'), 
        'license_status':scrapy_item.get('license_status'), 'website':scrapy_item.get('website'),
        'info_source':scrapy_item.get('info_source'), 'verified':bool(scrapy_item.get('verified')),
        'writing_sample':scrapy_item.get('writing_sample')
        
        #These are PsychologyToday fields, ignore for now
        #'license_num':int(scrapy_item.get('license_num')), 'license_state':scrapy_item.get('license_state'), 
        #'years_in_practice':int(scrapy_item.get('years_in_practice')), 'school':scrapy_item.get('school'),
        #'year_graduated':int(scrapy_item.get('year_graduated'))
        }
        )

        return self.cur.fetchone()[0]

    def insert_age_groups(self, scrapy_item) -> None:
        for val in scrapy_item.get('age_group_list'):
            self.cur.execute('''INSERT INTO age_groups (age_group) 
            VALUES (%s)
            ON CONFLICT DO NOTHING
            ;''', [val])

    def insert_issues(self, scrapy_item) -> None:
        for val in scrapy_item.get('issues_list'):
            self.cur.execute('''INSERT INTO issues (issue) 
            VALUES (%s)
            ON CONFLICT DO NOTHING
            ;''', [val])

    def insert_orientations(self, scrapy_item) -> None:
        for val in scrapy_item.get('orientations_list'):
            self.cur.execute('''INSERT INTO orientations (orientation) 
            VALUES (%s)
            ON CONFLICT DO NOTHING
            ;''', [val])
    
    def insert_professions(self, scrapy_item) -> None:
        for val in scrapy_item.get('professions_list'):
            self.cur.execute('''INSERT INTO professions (profession) 
            VALUES (%s)
            ON CONFLICT DO NOTHING
            ;''', [val])

    def insert_services(self, scrapy_item) -> None:
        for val in scrapy_item.get('services_list'):
            self.cur.execute('''INSERT INTO services (service) 
            VALUES (%s)
            ON CONFLICT DO NOTHING
            ;''', [val])

    # can't get thise to work, keep getting error: psycopg2.ProgrammingError: syntax error at or near "'table_name'"
    def insert_something(self, table, therapist_id:int, other_id:int)->None:
        # cur.execute('''INSERT INTO therapist_writing_samples VALUES (%(therapist_id)s, %(writing_sample_id)s);''',
        #     {'therapist_id':therapist_id, 'writing_sample_id':writing_sample_id}
        #     )
        sql = 'INSERT INTO %s VALUES (%s, %s);'
        self.cur.execute(sql, (table, therapist_id, other_id))

    def select_something(self, table, id_col, value_col, value):
        sql = 'SELECT %s FROM %s WHERE %s=%s;'
        self.cur.execute(sql, (id_col, table, value_col, value,))
        results = self.cur.fetchall()

        return results

if __name__ == '__main__':
    conn = psycopg2.connect(dbname='therapist_predictor', user='postgres', host='localhost', password='password')
    cur = conn.cursor()

    sql_test = SqlQueries(conn, cur)

    # mock lists standing in for scraped data in order to build a test scrapy item
    age_groups_list = ['123','456','789']
    issue_list = ['123','456','789']
    orientations_list = ['123','456','789']
    professions_list = ['123','456','789']
    services_list = ['123','456','789']

    item = TherapistItem()
    item['first_name'] = 'Jack'
    item['last_name'] = 'Torrence'
    item['address'] = '123 Hobbiton Ln'
    item['primary_credential'] = 'Psycho Killer'
    item['license_status'] = 'Active'
    item['website'] = 'www.lotr.com'
    item['info_source'] = 'GoodTherapy.com'
    item['verified'] = 'True'
    item['age_group_list'] = age_groups_list
    item['issues_list'] = issue_list
    item['orientations_list'] = orientations_list
    item['professions_list'] = professions_list
    item['services_list'] = services_list
    item['writing_sample'] = "All work and no play makes Jack a dull boy."


    #these are PsychToday fields, so ignore them for now
    item['license_num'] = None
    item['license_state'] = None
    item['years_in_practice'] = None
    item['school'] = None
    item['year_graduated'] = None

    
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