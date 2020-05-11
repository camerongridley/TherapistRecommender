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
        print(item)
        
        sql  = SqlQueries(self.conn, self.cur)

        self.cur.execute('''BEGIN;''')

        # insert into therapists table and get resulting id
        therapist_id = sql.insert_therapist_info(item)


        # insert list fields
        sql.insert_age_groups(item)
        sql.insert_issues(item)
        sql.insert_orientations(item)
        sql.insert_professions(item)
        sql.insert_services(item)
        sql.insert_writing_sample(item)
        
        age_groups = item.get('age_group_list')
        issues = item.get('issues_list')
        orientations = item.get('orientations_list')
        professions = item.get('professions_list')
        services = item.get('services_list')
        writing_samples = item.get('writing_samples_list')

        # loops go here

        # insert into lookup tables with therapist_id
        # get support table ids by selecting by value 
        for val in age_groups:
            # select age_group_id
            # insert into lookup table
            pass

        self.cur.execute('''COMMIT;''')


        return item

    