import psycopg2
import scrapy
from items import TherapistItem

class SqlQueries(object):
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def full_name_exists(self, full_name:str)->bool:
        if self.select_full_name(full_name) is not None:
            return True
        else:
            return False

    def select_full_name(self, value:str)->int:
        self.cur.execute('''SELECT therapist_id FROM therapists WHERE full_name=%(full_name)s;''',
            {'full_name':value}
            )
        if self.cur.rowcount <= 0:
            return None
        else:
            return self.cur.fetchone()[0]

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
        ls = scrapy_item.get('age_group_list')
        if ls is not None:
            for val in ls:
                age_group_id = self.select_age_group_id(val)
                self.cur.execute('''INSERT INTO therapist_age_groups VALUES (%(therapist_id)s, %(age_group_id)s);''',
                {'therapist_id':therapist_id, 'age_group_id':age_group_id}
                )

    def insert_therapist_issues(self, therapist_id:int, scrapy_item)->None:
        ls = scrapy_item.get('issues_list')
        if ls is not None:
            for val in ls:
                issue_id = self.select_issue_id(val)
                self.cur.execute('''INSERT INTO therapist_issues VALUES (%(therapist_id)s, %(issue_id)s);''',
                {'therapist_id':therapist_id, 'issue_id':issue_id}
                )
    
    def insert_therapist_orientations(self, therapist_id:int, scrapy_item)->None:
        ls = scrapy_item.get('orientations_list')
        if ls is not None:
            for val in ls:
                orientation_id = self.select_orientation_id(val)
                self.cur.execute('''INSERT INTO therapist_orientations VALUES (%(therapist_id)s, %(orientation_id)s);''',
                {'therapist_id':therapist_id, 'orientation_id':orientation_id}
                )

    def insert_therapist_professions(self, therapist_id:int, scrapy_item)->None:
        ls = scrapy_item.get('professions_list')
        if ls is not None:
            for val in ls:
                profession_id = self.select_profession_id(val)
                self.cur.execute('''INSERT INTO therapist_professions VALUES (%(therapist_id)s, %(profession_id)s);''',
                {'therapist_id':therapist_id, 'profession_id':profession_id}
                )

    def insert_therapist_services(self, therapist_id:int, scrapy_item)->None:
        ls = scrapy_item.get('services_list')
        if ls is not None:
            for val in ls:
                service_id = self.select_service_id(val)
                self.cur.execute('''INSERT INTO therapist_services VALUES (%(therapist_id)s, %(service_id)s);''',
                {'therapist_id':therapist_id, 'service_id':service_id}
                )

    def insert_therapist_info(self, scrapy_item)->int:
        #print(f'SCRAPY ITEM FIELD: {scrapy_item}')
        self.cur.execute('''INSERT INTO therapists (
        first_name, last_name, 
        street, city,
        state, zip_code,
        phone, primary_credential, 
        license_status, website, 
        info_source, verified,
        writing_sample, full_name) 
        VALUES (%(first_name)s,%(last_name)s,
        %(street)s, %(city)s, 
        %(state)s, %(zip_code)s, 
        %(phone)s, %(primary_credential)s,
        %(license_status)s, %(website)s,
        %(info_source)s, %(verified)s,
        %(writing_sample)s, %(full_name)s
        ) 
        RETURNING therapist_id;''',

        {
        'first_name':scrapy_item.get('first_name'), 'last_name':scrapy_item.get('last_name'), 
        'street':scrapy_item.get('street'),'city':scrapy_item.get('city'),
        'state':scrapy_item.get('state'),'zip_code':scrapy_item.get('zip_code'),
        'phone':scrapy_item.get('phone'), 'primary_credential':scrapy_item.get('primary_credential'), 
        'license_status':scrapy_item.get('license_status'), 'website':scrapy_item.get('website'),
        'info_source':scrapy_item.get('info_source'), 'verified':bool(scrapy_item.get('verified')),
        'writing_sample':scrapy_item.get('writing_sample'), 'full_name':scrapy_item.get('full_name')

        #These are PsychologyToday fields, ignore for now
        #'license_num':int(scrapy_item.get('license_num')), 'license_state':scrapy_item.get('license_state'), 
        #'years_in_practice':int(scrapy_item.get('years_in_practice')), 'school':scrapy_item.get('school'),
        #'year_graduated':int(scrapy_item.get('year_graduated'))
        }
        )

        return self.cur.fetchone()[0]

    def insert_age_groups(self, scrapy_item) -> None:
        ls = scrapy_item.get('age_group_list')
        if ls is not None:
            for val in ls:
                self.cur.execute('''INSERT INTO age_groups (age_group) 
                VALUES (%s)
                ON CONFLICT DO NOTHING
                ;''', [val])

    def insert_issues(self, scrapy_item) -> None:
        ls = scrapy_item.get('issues_list')
        if ls is not None:
            for val in ls:
                self.cur.execute('''INSERT INTO issues (issue) 
                VALUES (%s)
                ON CONFLICT DO NOTHING
                ;''', [val])

    def insert_orientations(self, scrapy_item) -> None:
        ls = scrapy_item.get('orientations_list')
        if ls is not None:
            for val in ls:
                self.cur.execute('''INSERT INTO orientations (orientation) 
                VALUES (%s)
                ON CONFLICT DO NOTHING
                ;''', [val])
    
    def insert_professions(self, scrapy_item) -> None:
        ls = scrapy_item.get('professions_list')
        if ls is not None:
            for val in ls:
                self.cur.execute('''INSERT INTO professions (profession) 
                VALUES (%s)
                ON CONFLICT DO NOTHING
                ;''', [val])

    def insert_services(self, scrapy_item) -> None:
        ls = scrapy_item.get('services_list')
        if ls is not None:
            for val in ls:
                self.cur.execute('''INSERT INTO services (service) 
                VALUES (%s)
                ON CONFLICT DO NOTHING
                ;''', [val])
