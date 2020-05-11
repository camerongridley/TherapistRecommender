# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TherapistItem(scrapy.Item):
    # define the fields for your item here like:
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    address = scrapy.Field()
    primary_credential = scrapy.Field()
    license_status = scrapy.Field()
    website = scrapy.Field()
    info_source = scrapy.Field()
    creation_date = scrapy.Field()
    verified = scrapy.Field()
    license_num = scrapy.Field()
    license_state = scrapy.Field()
    years_in_practice = scrapy.Field()
    school = scrapy.Field()
    year_graduated = scrapy.Field()
    age_group_list = scrapy.Field()
    issues_list = scrapy.Field()
    orientations_list = scrapy.Field()
    professions_list = scrapy.Field()
    services_list = scrapy.Field()
    writing_sample = scrapy.Field()
    html_source_code = scrapy.Field()

# class AgeGroupItem(scrapy.Item):
#     age_group = scrapy.Field()

# class IssueItem(scrapy.Item):
#     issue = scrapy.Field()

# class OrientationItem(scrapy.Item):
#     orientation = scrapy.Field()

# class ProfessionItem(scrapy.Item):
#     profession = scrapy.Field()

# class ServiceItem(scrapy.Item):
#     service = scrapy.Field()

# class WritingSampleItem(scrapy.Item):
#     sample = scrapy.Field()
#     source = scrapy.Field()

