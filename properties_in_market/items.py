# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PropertiesInMarketItem(scrapy.Item):
    identifier = scrapy.Field()
    city = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    beds = scrapy.Field()
    baths = scrapy.Field()
    description = scrapy.Field()
    features = scrapy.Field()
    single_family_detached_1y_price_change = scrapy.Field()
    single_family_detached_5y_price_change = scrapy.Field()
    aggregate_1y_price_change = scrapy.Field()
    aggregate_5y_price_change = scrapy.Field()
    high_schools_score = scrapy.Field()
    primary_schools_score = scrapy.Field()
    transit_friendly_score = scrapy.Field()
    groceries_score = scrapy.Field()
    restaurants_score = scrapy.Field()
    pedestrian_friendly_score = scrapy.Field()
    cycling_friendly_score = scrapy.Field()
    car_friendly_score = scrapy.Field()
    vibrant_score = scrapy.Field()
    shopping_score = scrapy.Field()
    daycares_score = scrapy.Field()
    nightlife_score = scrapy.Field()
    cafes_score = scrapy.Field()
    quiet_score = scrapy.Field()
    parks_score = scrapy.Field()
    greenery_score = scrapy.Field()
    life_stage = scrapy.Field()
    employment_type = scrapy.Field()
    average_household_income = scrapy.Field()
    average_number_of_children = scrapy.Field()
    no_certificate_diploma_degree = scrapy.Field()
    high_school_certificate_or_equivalent = scrapy.Field()
    apprenticeship_trade_certificate_diploma = scrapy.Field()
    college_non_university_certificate = scrapy.Field()
    university_certificate_below_bachelor = scrapy.Field()
    university_degree = scrapy.Field()
    by_car = scrapy.Field()
    by_public_transit = scrapy.Field()
    by_walking = scrapy.Field()
    by_bicycle = scrapy.Field()
    by_other_methods = scrapy.Field()
    apartments_low_and_high_rise = scrapy.Field()
    houses = scrapy.Field()
    one_person = scrapy.Field()
    one_family = scrapy.Field()
    two_plus_people = scrapy.Field()
    two_plus_families = scrapy.Field()
    age0_to_4 = scrapy.Field()
    age5_to_9 = scrapy.Field()
    age10_to_14 = scrapy.Field()
    age15_to_19 = scrapy.Field()
    age20_to_34 = scrapy.Field()
    age35_to_49 = scrapy.Field()
    age50_to_64 = scrapy.Field()
    age65_to_79 = scrapy.Field()
    age80_plus = scrapy.Field()
    en_only = scrapy.Field()
    fr_only = scrapy.Field()
    en_and_fr = scrapy.Field()
    other = scrapy.Field()
    mother_tongue = scrapy.Field()
    owners = scrapy.Field()
    renters = scrapy.Field()