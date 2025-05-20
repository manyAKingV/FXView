# import scrapy
# from urllib.parse import quote, urljoin
# from company_spider.items import CompanyInfoItem
# import json

# class CompanyInfoSpider(scrapy.Spider):
#     name = "company_spider"

#     def __init__(self, company_name=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.company_name = company_name

#     def start_requests(self):
#         query = quote(f"{self.company_name} 官网")
#         search_url = f"https://www.bing.com/search?q={query}"

#         headers = {
#             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
#         }

#         yield scrapy.Request(
#             url=search_url,
#             headers=headers,
#             callback=self.parse_search_results,
#             dont_filter=True
#         )

#     def parse_search_results(self, response):
#         # 从搜索结果中获取第一个链接（b_algo 是搜索结果块）
#         first_result = response.xpath('//li[@class="b_algo"]/h2/a/@href').get()
#         if first_result:
#             headers = {
#                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
#             }
#             yield scrapy.Request(
#                 url=first_result,
#                 headers=headers,
#                 callback=self.parse_company_page,
#                 meta={'website': first_result}
#             )
#         else:
#             self.logger.warning(f"未找到搜索结果：{self.company_name}")

#     def parse_company_page(self, response):
#         website = response.meta['website']

#         # 提取网站简介
#         description = response.xpath('//meta[@name="description"]/@content').get()
#         if not description:
#             description = response.xpath('//meta[@property="og:description"]/@content').get()

#         # 提取 logo（icon 链接）
#         logo_href = response.xpath('//link[contains(@rel, "icon")]/@href').get()
#         if not logo_href:
#             logo_href = "/favicon.ico"

#         logo_url = urljoin(website, logo_href)
        
#         # 查找结构化数据
#         script_data = response.xpath(
#             '//script[@type="application/ld+json"]/text()'
#         ).get()
    
#         if script_data:
#             data = json.loads(script_data)
#             company_spider = next(
#                 (item for item in data if item.get('@type') == 'Organization'), 
#                 {}
#             )
#             creation_time = company_spider.get('foundingDate', '未知')
#         else:
#             creation_time = '未知'

#         item = CompanyInfoItem()
#         item['name'] = self.company_name
#         item['website'] = website
#         item['description'] = description or ""
#         item['logo_url'] = logo_url
#         item['creation_time'] = creation_time
#         yield item

# company_spider.py（保持不变）
import scrapy
from urllib.parse import quote, urljoin
from company_spider.items import CompanyInfoItem
import json

class CompanyInfoSpider(scrapy.Spider):
    name = "company_spider"

    def __init__(self, company_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_name = company_name

    def start_requests(self):
        query = quote(f"{self.company_name} 官网")
        search_url = f"https://www.bing.com/search?q={query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        yield scrapy.Request(
            url=search_url,
            headers=headers,
            callback=self.parse_search_results,
            dont_filter=True
        )

    def parse_search_results(self, response):
        first_result = response.xpath('//li[@class="b_algo"]/h2/a/@href').get()
        if first_result:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            }
            yield scrapy.Request(
                url=first_result,
                headers=headers,
                callback=self.parse_company_page,
                meta={'website': first_result}
            )
        else:
            self.logger.warning(f"未找到搜索结果：{self.company_name}")

    def parse_company_page(self, response):
        website = response.meta['website']

        description = response.xpath('//meta[@name="description"]/@content').get()
        if not description:
            description = response.xpath('//meta[@property="og:description"]/@content').get()

        logo_href = response.xpath('//link[contains(@rel, "icon")]/@href').get()
        if not logo_href:
            logo_href = "/favicon.ico"

        logo_url = urljoin(website, logo_href)
        
        script_data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        creation_time = '未知'
        if script_data:
            try:
                data = json.loads(script_data)
                company_spider = next(
                    (item for item in data if item.get('@type') == 'Organization'), 
                    {}
                )
                # creation_time = company_spider.get('foundingDate', '未知')
                creation_time = self.extract_structured_data(response)
            except json.JSONDecodeError:
                pass

        item = CompanyInfoItem()
        item['name'] = self.company_name
        item['website'] = website
        item['description'] = description or ""
        item['logo_url'] = logo_url
        item['creation_time'] = creation_time
        yield item
        
        
        
