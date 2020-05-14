import psycopg2
from sql_queries import SqlQueries

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
        
        sql  = SqlQueries(self.conn, self.cur)

        # create new therapist and get resulting id
        #self.cur.execute('''BEGIN;''')
        therapist_id = sql.insert_therapist_info(item)

        # with therapist id update and insert relational tables
        sql.insert_age_groups(item)
        sql.insert_issues(item)
        sql.insert_orientations(item)
        sql.insert_professions(item)
        sql.insert_services(item)

        sql.insert_therapist_age_groups(therapist_id, item)
        sql.insert_therapist_issues(therapist_id, item)
        sql.insert_therapist_orientations(therapist_id, item)
        sql.insert_therapist_professions(therapist_id, item)
        sql.insert_therapist_services(therapist_id, item)
        #self.cur.execute('''COMMIT;''')

        self.conn.commit()

        return item


    