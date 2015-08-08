
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ApsaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    start_date=scrapy.Field()
    due_date=scrapy.Field()
    desc=scrapy.Field()
    school=scrapy.Field()
    post_date=scrapy.Field()
    url=scrapy.Field()
    pass