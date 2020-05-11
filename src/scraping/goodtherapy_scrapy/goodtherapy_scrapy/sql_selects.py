import psycopg2

class SqlSelects(object):
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