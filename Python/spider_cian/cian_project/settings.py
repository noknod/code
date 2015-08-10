# -*- coding: utf-8 -*-

# Scrapy settings for cian_project project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'cian_project'

SPIDER_MODULES = ['cian_project.spiders']
NEWSPIDER_MODULE = 'cian_project.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cian_project (+http://www.yourdomain.com)'

ITEM_PIPELINES = ['cian_project.pipelines.CianProjectPipeline']