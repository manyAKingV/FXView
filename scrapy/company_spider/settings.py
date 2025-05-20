
# # 基础配置
# BOT_NAME = 'company_spider'
# SPIDER_MODULES = ['company_spider.spiders']  # 适配目录结构[7](@ref)
# NEWSPIDER_MODULE = 'company_spider.spiders'  # 新爬虫生成路径[8](@ref)
# ROBOTSTXT_OBEY = False  # 不遵守robots.txt[5](@ref)

# # 请求头配置
# USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# # 反爬策略
# DOWNLOAD_DELAY = 2  # 基础请求间隔[3,5](@ref)
# RANDOMIZE_DOWNLOAD_DELAY = True  # 随机化延迟(±50% of DOWNLOAD_DELAY)[5](@ref)
# RETRY_TIMES = 3  # 失败重试次数[4](@ref)
# DOWNLOAD_TIMEOUT = 15  # 请求超时时间[4](@ref)
# CONCURRENT_REQUESTS = 8  # 并发请求量[3](@ref)

# # 数据管道
# ITEM_PIPELINES = {
#     'company_spider.pipelines.CompanyInfoPipeline': 300,
# }

# # 输出配置
# # FEED_FORMAT = 'json'
# # FEED_URI = 'output/%(name)s/%(company_name)s.json'  # 动态文件名需配合爬虫参数[5](@ref)
# # FEED_EXPORT_FIELDS = ['company_name', 'industry', 'location']  # 建议定义输出字段顺序[5](@ref)

# FEED_EXPORTERS = {
#     'yaml': 'your_project_name.exporters.YamlItemExporter',
# }
# FEED_FORMAT = 'yaml'
# FEED_URI = 'output.yml'  # 输出文件名
# FEED_EXPORT_ENCODING = 'utf-8'  # 中文编码保障[5](@ref)


# settings.py
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

# 中间件配置（新增）
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
#     'company_spider.middlewares.RandomProxyMiddleware': 100,
# }

# 调试配置
# HTTPCACHE_ENABLED = False
# LOG_LEVEL = 'DEBUG'  