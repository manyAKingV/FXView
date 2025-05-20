import scrapy

class CompanyInfoItem(scrapy.Item):
    name = scrapy.Field()
    website = scrapy.Field()
    description = scrapy.Field()
    logo_url = scrapy.Field()
    creation_time = scrapy.Field()  # 新增字段
    original_logo_path = scrapy.Field()
    svg_logo_path = scrapy.Field()
