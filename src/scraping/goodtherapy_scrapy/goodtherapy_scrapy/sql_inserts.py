import psycopg2

class SqlInserts(object):
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def insert_therapist_age_group(self, therapist_id:int, age_group_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_age_groups VALUES (%(therapist_id)s, %(age_group_id)s) 
        ON CONFLICT DO NOTHING;''',
            {'therapist_id':therapist_id, 'age_group_id':age_group_id}
            )

    def insert_therapist_issue(self, therapist_id:int, issue_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_issues VALUES (%(therapist_id)s, %(issue_id)s) 
        ON CONFLICT DO NOTHING;''',
            {'therapist_id':therapist_id, 'issue_id':issue_id}
            )

    def insert_therapist_orientation(self, therapist_id:int, orientation_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_orientations VALUES (%(therapist_id)s, %(orientation_id)s) 
        ON CONFLICT DO NOTHING;''',
            {'therapist_id':therapist_id, 'orientation_id':orientation_id}
            )

    def insert_therapist_profession(self, therapist_id:int, profession_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_professions VALUES (%(therapist_id)s, %(profession_id)s) 
        ON CONFLICT DO NOTHING;''',
            {'therapist_id':therapist_id, 'profession_id':profession_id}
            )

    def insert_therapist_service(self, therapist_id:int, service_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_services VALUES (%(therapist_id)s, %(service_id)s) 
        ON CONFLICT DO NOTHING;''',
            {'therapist_id':therapist_id, 'service_id':service_id}
            )

    def insert_therapist_writing_sample(self, therapist_id:int, writing_sample_id:int)->None:
        self.cur.execute('''INSERT INTO therapist_writing_samples VALUES (%(therapist_id)s, %(writing_sample_id)s) 
        ON CONFLICT DO NOTHING;''',
            {'therapist_id':therapist_id, 'writing_sample_id':writing_sample_id}
            )

    def insert_therapist_info(self, item):
        # self.cur.execute('''INSERT INTO quotes values (%(title)s,%(author)s,%(tag)s);''',
        # {'title': item['title'][0], 'author' : item['author'][0], 'tag' : item['tag'][0] })
        therapist_id = self.cur.execute(
            '''INSERT INTO therapists (first_name, last_name, address, 
                primary_credential, license_status, website, 
                info_source, verified, license_num, 
                license_state, years_in_practice, school, 
                year_graduated) 
            VALUES (%(first_name)s,%(last_name)s,%(address)s,
                %(primary_credential)s, %(license_status)s,%(website)s,
                %(info_source)s,%(verified)s,%(license_num)s,
                %(license_state)s,%(years_in_practice)s,%(school)s,
                %(year_graduated)s)
            RETURNING therapist_id;''',
                {'first_name': item['first_name'][0], 'last_name' : item['last_name'][0], 'address' : item['address'][0],
                'primary_credential' : item['primary_credential'][0], 'license_status' : item['license_status'][0], 'website' : item['website'][0],
                'info_source' : item['info_source'][0], 'verified' : item['verified'][0], 'license_num' : item['license_num'][0],
                'license_state' : item['license_state'][0], 'years_in_practice' : item['years_in_practice'][0], 'school' : item['school'][0],
                'year_graduated' : item['year_graduated'][0]
                })
        #self.cur.execute('''INSERT INTO quotes values (%(title)s,%(author)s,%(tag)s);''',
        #{'title': item['title'][0], 'author' : item['author'][0], 'tag' : item['tag'][0] })

        self.conn.commit()

        return therapist_id
