import scrapy

from scrapy.loader import ItemLoader

from ..items import PolarisbanklimitedItem
from itemloaders.processors import TakeFirst


class PolarisbanklimitedSpider(scrapy.Spider):
	name = 'polarisbanklimited'
	start_urls = [
		'https://www.polarisbanklimited.com/media-center/polaris-news/',
		'https://www.polarisbanklimited.com/media-center/press-release/'
	]

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="entry-title"]/text()').get()
		description = response.xpath('//div[@class="siteorigin-widget-tinymce textwidget"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time[@class="entry-date"]/text()').get()

		item = ItemLoader(item=PolarisbanklimitedItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
