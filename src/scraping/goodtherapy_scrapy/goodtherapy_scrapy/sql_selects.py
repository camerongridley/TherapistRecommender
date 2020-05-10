import psycopg2

class SqlSelects(object):
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

    # getting syntax error with this
    def select_something(self, table, id_col, value_col, value):
        sql = 'SELECT %s FROM %s WHERE %s=%s;'
        self.cur.execute(sql, (id_col, table, value_col, value,))
        results = self.cur.fetchall()

        return results