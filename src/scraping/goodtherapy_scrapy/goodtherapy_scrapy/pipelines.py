import psycopg2
from .sql_inserts import SqlInserts
from .sql_selects import SqlSelects

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class GoodtherapyScrapyPipeline:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(dbname='therapist_predictor', user='postgres', host='localhost', password='password')
        self.cur = self.conn.cursor()

    def select_issue_id(self, issue_name:str)->int:
        issue_id = self.cur.execute('''SELECT issue_id FROM issues WHERE issue = %(issue)s;''',
            {'issue':issue_name}
            )

        return issue_id

    def process_item(self, item, spider):
        print("***************************** IN PIPELINE ***************************")
        print(item)
        
        sql_insert  = SqlInserts(self.conn, self.cur)

        self.cur.execute('''BEGIN;''')

        # insert into therapists table and get resulting id
        therapist_id = sql_insert.insert_therapist_info(item)

        '''
        https://stackoverflow.com/questions/7760052/insert-python-list-into-postgres-database
        cur.executemany(
            """INSERT INTO "%s" (data) VALUES (%%s)""" % (args.tableName),rows)

        Using parametrized arguments helps prevent SQL injection.

        The table name can not be parametrized, so we do have to use string interpolation to place the table name in the SQL query. %%s gets escapes the percent sign and becomes %s after string interpolation.

        By the way, (as a_horse_with_no_name has already pointed out) you can use the INSERT INTO ... SELECT form of INSERT to perform both SQL queries as one:

        cur.execute(
            """INSERT INTO %s (data)
            SELECT data FROM Table1
            WHERE lat=-20.004189 AND lon=-63.848004""" % (args.tableName))

        Per the question in the comments, if there are multiple fields, then the SQL becomes:

        cur.executemany(
            """INSERT INTO {t} (lat,lon,data1,data2) 
            VALUES (%s,%s,%s,%s)""".format(t=args.tableName),rows)

        (If you use the format method, then you don't have to escape all the other %ss.)
        '''

        #loop through lists of fields and insert each item into respective table
        # MAKE SURE DOESN"T STOP COMMIT IF THE VALUE ALREADY EXISTS - if so move outside BEGIN/COMIT
        age_groups = item['age_group_list']
        issues = item['issues_list']
        orientations = item['orientations_list']
        professions = item['professions_list']
        services = item['services_list']
        writing_samples = item['writing_samples_list']

        # loops go here

        # insert into lookup tables with therapist_id
        # get support table ids by selecting by value 
        for val in age_groups:
            # select age_group_id
            # insert into lookup table
            pass

        self.cur.execute('''COMMIT;''')


        return item

    