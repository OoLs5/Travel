# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class XiechengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img_link = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    points = scrapy.Field()
    comments = scrapy.Field()
    visitor = scrapy.Field()
    say = scrapy.Field()

class City_Name(scrapy.Item):
    City_In_Chinese = scrapy.Field()
    City_In_English = scrapy.Field()
    num = scrapy.Field()

class FlightItem(scrapy.Item):
    flight_company = scrapy.Field()
    plane = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    From = scrapy.Field()
    To = scrapy.Field()
    total_time = scrapy.Field()
    food = scrapy.Field()
    cost = scrapy.Field()
    tp = scrapy.Field()

class HotelItem(scrapy.Item):
    hotel_name = scrapy.Field()
    location = scrapy.Field()
    points = scrapy.Field()
    picture = scrapy.Field()
    visitors = scrapy.Field()
    comment = scrapy.Field()

class FoodItem(scrapy.Item):
    img = scrapy.Field()
    name = scrapy.Field()
    points = scrapy.Field()



