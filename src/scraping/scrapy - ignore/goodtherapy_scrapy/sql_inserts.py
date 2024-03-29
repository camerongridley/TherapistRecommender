import psycopg2

class SqlInserts(object):
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

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
            
    def insert_therapist_info(self, scrapy_item)->int:
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

    # def insert_therapist_info(self, scrapy_item):
    #     #print(f'SCRAPY ITEM FIELD: {scrapy_item}')
    #     self.cur.execute('''INSERT INTO therapists (
    #     first_name, last_name, 
    #     address, primary_credential, 
    #     license_status, website, 
    #     info_source, verified) 
    #     VALUES (%(first_name)s,%(last_name)s,
    #     %(address)s, %(primary_credential)s,
    #     %(license_status)s, %(website)s,
    #     %(info_source)s, %(verified)s) 
    #     RETURNING therapist_id;''',

    #     {
    #     'first_name':scrapy_item.get('first_name'), 'last_name':scrapy_item.get('last_name'), 
    #     'address':scrapy_item.get('address'), 'primary_credential':scrapy_item.get('primary_credential'), 
    #     'license_status':scrapy_item.get('license_status'), 'website':scrapy_item.get('website'),
    #     'info_source':scrapy_item.get('info_source'), 'verified':bool(scrapy_item.get('verified')), 
        
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


    # def insert_therapist_age_group2(self, therapist_id:int, age_group_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_age_groups VALUES (%(therapist_id)s, %(age_group_id)s) 
    #     ON CONFLICT DO NOTHING;''',
    #         {'therapist_id':therapist_id, 'age_group_id':age_group_id}
    #         )

    # def insert_therapist_issue(self, therapist_id:int, issue_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_issues VALUES (%(therapist_id)s, %(issue_id)s) 
    #     ON CONFLICT DO NOTHING;''',
    #         {'therapist_id':therapist_id, 'issue_id':issue_id}
    #         )

    # def insert_therapist_orientation(self, therapist_id:int, orientation_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_orientations VALUES (%(therapist_id)s, %(orientation_id)s) 
    #     ON CONFLICT DO NOTHING;''',
    #         {'therapist_id':therapist_id, 'orientation_id':orientation_id}
    #         )

    # def insert_therapist_profession(self, therapist_id:int, profession_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_professions VALUES (%(therapist_id)s, %(profession_id)s) 
    #     ON CONFLICT DO NOTHING;''',
    #         {'therapist_id':therapist_id, 'profession_id':profession_id}
    #         )

    # def insert_therapist_service(self, therapist_id:int, service_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_services VALUES (%(therapist_id)s, %(service_id)s) 
    #     ON CONFLICT DO NOTHING;''',
    #         {'therapist_id':therapist_id, 'service_id':service_id}
    #         )

    # def insert_therapist_writing_sample(self, therapist_id:int, sample_id:int)->None:
    #     self.cur.execute('''INSERT INTO therapist_writing_samples VALUES (%(therapist_id)s, %(sample_id)s) 
    #     ON CONFLICT DO NOTHING;''',
    #         {'therapist_id':therapist_id, 'sample_id':sample_id}
            )
