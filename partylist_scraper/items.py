# partylist_scraper/items.py

import scrapy

class PartylistResult(scrapy.Item):
    Year = scrapy.Field()
    Party_list = scrapy.Field()
    Votes = scrapy.Field()
    Percentage = scrapy.Field()
    Seats = scrapy.Field()
