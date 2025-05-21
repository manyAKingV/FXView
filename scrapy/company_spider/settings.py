# 基础配置
BOT_NAME = 'company_spider'
SPIDER_MODULES = ['company_spider.spiders']
NEWSPIDER_MODULE = 'company_spider.spiders'
ROBOTSTXT_OBEY = False

# 请求头配置
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# 反爬策略
DOWNLOAD_DELAY = 3  # 调整为更合理的延迟
RANDOMIZE_DOWNLOAD_DELAY = True
RETRY_TIMES = 3
DOWNLOAD_TIMEOUT = 15
CONCURRENT_REQUESTS = 4  # 降低并发避免封禁
AUTOTHROTTLE_ENABLED = True  # 新增自动限速

# 文件存储配置
FILES_STORE = '../../company'  # 根据项目结构调整路径
IMAGES_STORE = '../../company'

# 数据管道（重要调整）
ITEM_PIPELINES = {
    'company_spider.pipelines.CompanyFilesPipeline': 300,
    # 'scrapy.pipelines.files.FilesPipeline': 1
}

# 输出配置（禁用FEED导出）
FEED_EXPORT_ENCODING = 'utf-8'

