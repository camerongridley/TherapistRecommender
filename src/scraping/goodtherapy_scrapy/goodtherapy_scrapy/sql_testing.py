import psycopg2
import scrapy
from items import TherapistItem

class SqlTest(object):
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def select_age_group_id(self, value:str)->int:
        self.cur.execute('''SELECT age_group_id FROM age_groups WHERE age_group=%(issue)s;''',
            {'age_group':value}
            )
        value_id = self.cur.fetchall()[0][0]
        return value_id

    def select_issue_id(self, value:str)->int:
        self.cur.execute('''SELECT issue_id FROM issues WHERE issue=%(issue)s;''',
            {'issue':value}
            )
        value_id = self.cur.fetchall()[0][0]
        return value_id

    def select_orientation_id(self, value:str)->int:
        self.cur.execute('''SELECT orientation_id FROM orientations WHERE orientation=%(orientation)s;''',
            {'orientation':value}
            )
        value_id = self.cur.fetchall()[0][0]
        return value_id

    def select_profession_id(self, value:str)->int:
        self.cur.execute('''SELECT profession_id FROM professions WHERE profession=%(profession)s;''',
            {'profession':value}
            )
        value_id = self.cur.fetchall()[0][0]
        return value_id

    def select_service_id(self, value:str)->int:
        self.cur.execute('''SELECT service_id FROM services WHERE service=%(service)s;''',
            {'service':value}
            )
        value_id = self.cur.fetchall()[0][0]
        return value_id

    def select_writing_sample_id(self, value:str)->int:
        self.cur.execute('''SELECT writing_sample_id FROM writing_samples WHERE writing_sample=%(writing_sample)s;''',
            {'writing_sample':value}
            )
        value_id = self.cur.fetchall()[0][0]
        return value_id

    def insert_therapist_age_group(self, therapist_id:int, age_group_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_age_groups VALUES (%(therapist_id)s, %(age_group_id)s);''',
            {'therapist_id':therapist_id, 'age_group_id':age_group_id}
            )

    def insert_therapist_issue(self, therapist_id:int, issue_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_issues VALUES (%(therapist_id)s, %(issue_id)s);''',
            {'therapist_id':therapist_id, 'issue_id':issue_id}
            )

    def insert_therapist_orientation(self, therapist_id:int, orientation_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_orientations VALUES (%(therapist_id)s, %(orientation_id)s);''',
            {'therapist_id':therapist_id, 'orientation_id':orientation_id}
            )

    def insert_therapist_profession(self, therapist_id:int, profession_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_professions VALUES (%(therapist_id)s, %(profession_id)s);''',
            {'therapist_id':therapist_id, 'profession_id':profession_id}
            )

    def insert_therapist_service(self, therapist_id:int, service_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_services VALUES (%(therapist_id)s, %(service_id)s);''',
            {'therapist_id':therapist_id, 'service_id':service_id}
            )

    def insert_therapist_writing_sample(self, therapist_id:int, writing_sample_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_writing_samples VALUES (%(therapist_id)s, %(writing_sample_id)s);''',
            {'therapist_id':therapist_id, 'writing_sample_id':writing_sample_id}
            )

    def insert_therapist_info(self, scrapy_item)->int:
        id = self.cur.execute('''INSERT INTO therapists VALUES (
            %(first_name)s, %(last_name)s, 
            %(address)s, %(primary_credential)s, 
            %(license_status)s, %(website)s, 
            %(info_source)s, %(verified)s, 
            %(license_num)s, %(license_state)s, 
            %(years_in_practice)s, %(school)s, 
            %(year_graduated)s)
            RETURNING therapist_id
            ;''',
            {'first_name':scrapy_item['first_name'], 'last_name':scrapy_item['last_name'], 
            'address':scrapy_item['address'], 'primary_credential':scrapy_item['primary_credential'], 
            'license_status':scrapy_item['license_status'], 'website':scrapy_item['website'],
            'info_source':scrapy_item['info_source'], 'verified':scrapy_item['verified'], 
            'license_num':scrapy_item['license_num'], 'license_state':scrapy_item['license_state'], 
            'years_in_practice':scrapy_item['years_in_practice'], 'school':scrapy_item['school'],
            'year_graduated':scrapy_item['year_graduated']}
            )

        return id

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

    sql_test = SqlTest(conn, cur)

    # print(sql_test.select_issue_id('Abandonment'))
    o_id = sql_test.select_orientation_id('Voice Dialogue')
    print(o_id)
    # sql_test.insert_therapist_orientation(1, o_id)
    #res = sql_test.select_something('orientations', 'orientation_id', 'orientation', 'Voice Dialogue')
    #print(res)
    
    # cur.execute('''BEGIN;''')
    # sql_test.insert_therapist_orientation(1, 3)
    # sql_test.insert_therapist_orientation(1, 2000)
    # cur.execute('''COMMIT;''')
    
    
    therapist_dict = [{'first_name':'first_name', 'last_name':'last_name', 
            'address':'address', 'primary_credential':'primary_credential', 
            'license_status':'license_status', 'website':'website',
            'info_source':'info_source', 'verified':'verified', 
            'license_num':'license_num', 'license_state':'license_state', 
            'years_in_practice':'years_in_practice', 'school':'school',
            'year_graduated':'year_graduated'}]

    item = TherapistItem()
    item['first_name'] = 'Bilbo'
    item['last_name'] = 'Baggins'
    item['address'] = '312 Hobbiton Ln'
    item['primary_credential'] = 'Master Thief'
    item['license_status'] = 'Active'
    item['website'] = 'www.prescious.com'
    item['info_source'] = 'GoodTherapy.com'
    item['verified'] = 'True'
    
    item['license_num'] = None
    item['license_state'] = None
    item['years_in_practice'] = None
    item['school'] = None
    item['year_graduated'] = None
    

    sql_test.insert_therapist_info(item)
    
    conn.commit()
        
    conn.close()