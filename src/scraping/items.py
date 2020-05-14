# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TherapistItem(scrapy.Item):
    # define the fields for your item here like:
    full_name = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    street = scrapy.Field()
    state = scrapy.Field()
    city = scrapy.Field()
    zip_code = scrapy.Field()
    phone = scrapy.Field()
    primary_credential = scrapy.Field()
    license_status = scrapy.Field()
    website = scrapy.Field()
    info_source = scrapy.Field()
    creation_date = scrapy.Field()
    verified = scrapy.Field()
    age_group_list = scrapy.Field()
    issues_list = scrapy.Field()
    orientations_list = scrapy.Field()
    professions_list = scrapy.Field()
    services_list = scrapy.Field()
    writing_sample = scrapy.Field()

    # PsychologyToday-specific fields
    # license_num = scrapy.Field()
    # license_state = scrapy.Field()
    # years_in_practice = scrapy.Field()
    # school = scrapy.Field()
    # year_graduated = scrapy.Field()


