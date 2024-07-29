from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader

from .items import ToscrapeItem


class ToScrapeLoader(ItemLoader):
    default_item_class = ToscrapeItem
    default_output_processor = TakeFirst()
