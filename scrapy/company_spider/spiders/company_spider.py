import scrapy
from urllib.parse import quote, urljoin
from company_spider.items import CompanyInfoItem
from scrapy import Selector
import re
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
            dont_filter=True,
        )

    def parse_search_results(self, response):
        first_result = response.xpath('//li[@class="b_algo"]/h2/a/@href').get()
        if first_result:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
            yield scrapy.Request(
                url=first_result,
                headers=headers,
                callback=self.parse_company_page,
                meta={"website": first_result},
            )
        else:
            self.logger.warning(f"未找到搜索结果：{self.company_name}")

    def parse_company_page(self, response):
        sh
        website = response.meta["website"]

        description = response.xpath('//meta[@name="description"]/@content').get()
        if not description:
            description = response.xpath(
                '//meta[@property="og:description"]/@content'
            ).get()

        logo_href = response.xpath('//link[contains(@rel, "icon")]/@href').get()
        if not logo_href:
            logo_href = "/favicon.ico"

        logo_url = urljoin(website, logo_href)

        script_data = response.xpath(
            '//script[@type="application/ld+json"]/text()'
        ).get()
        creation_time = "未知"
        if script_data:
            try:
                data = json.loads(script_data)
                company_spider = next(
                    (item for item in data if item.get("@type") == "Organization"), {}
                )
                creation_time = company_spider.get("foundingDate", "未知")
                # creation_time = self.extract_structured_data(response)
            except json.JSONDecodeError:
                pass

        item = CompanyInfoItem()
        item["name"] = self.company_name
        item["website"] = website
        item["description"] = description or ""
        item["logo_url"] = logo_url
        item["creation_time"] = creation_time
        yield item


    # def extract_established_year(self, response) -> str:
    #     """提取公司成立年份"""
    #     sel = Selector(response)
    #     year = "未知"

    #     # 方式1：JSON-LD结构化数据（优先级最高）
    #     script_data = sel.xpath('//script[@type="application/ld+json"]/text()').get()
    #     if script_data:
    #         try:
    #             # 清洗非法转义字符
    #             cleaned_data = re.sub(r'\\[\'"]', "", script_data)
    #             data = json.loads(cleaned_data)

    #             # 支持多类型解析
    #             org_types = ["Organization", "Corporation", "Company"]
    #             company_data = next(
    #                 (
    #                     item
    #                     for item in (data if isinstance(data, list) else [data])
    #                     if item.get("@type") in org_types
    #                 ),
    #                 {},
    #             )

    #             # 处理不同日期格式
    #             if "foundingDate" in company_data:
    #                 date_str = company_data["foundingDate"]
    #                 if match := re.search(r"\d{4}", date_str):
    #                     year = match.group()
    #                     return year  # 结构化数据优先返回
    #         except Exception as e:
    #             self.logger.warning(f"JSON-LD解析异常: {str(e)}")

    #     # 方式2：微数据（Microdata）解析
    #     if year == "未知":
    #         micro_year = sel.xpath('//*[@itemprop="foundingDate"]/text()').get()
    #         if micro_year and (match := re.search(r"\d{4}", micro_year)):
    #             year = match.group()
    #             return year

    #     # 方式3：智能文本匹配（优化正则）
    #     patterns = [
    #         # 精准匹配模式
    #         r"(?:成立|创立|注册)[于：]?\s*(\d{4})\s*年",
    #         # 模糊匹配模式
    #         r"(?:20\d{2})[年\-/]",
    #         # 备案信息模式
    #         r"<td>成立日期</td>\s*<td>.*?(\d{4})",
    #     ]

    #     for pattern in patterns:
    #         if match := re.search(pattern, response.text):
    #             year = match.group(1) if len(match.groups()) >= 1 else match.group()
    #             # 验证合理性
    #             if 1900 < int(year) <= datetime.now().year:
    #                 return year

    #     # 保底方案：页面关键词定位
    #     keywords = ["companyYear", "est-year", "found-year"]
    #     for kw in keywords:
    #         css_selector = f"div.{kw}, span#{kw}"
    #         elem_text = sel.css(css_selector).xpath("text()").get()
    #         if elem_text and (match := re.search(r"\d{4}", elem_text)):
    #             year = match.group()
    #             break

    #     return year
