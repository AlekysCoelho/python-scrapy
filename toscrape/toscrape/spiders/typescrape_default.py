import scrapy
from toscrape.loader import ToScrapeLoader


class ToScrapeDefaultSpider(scrapy.Spider):
    name = "toscrape_default"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            loader = ToScrapeLoader(selector=quote, response=response)
            loader.add_xpath("text", "./span[@class='text']/text()")
            loader.add_xpath("author", ".//small[@class='author']/text()")
            loader.add_xpath("tags_links", ".//div[@class='tags']/a/@href")
            loader.add_xpath("tags_names", ".//div[@class='tags']/a/text()")

            item = loader.load_item()
            yield item

        nex_page = response.xpath("//li[@class='next']/a/@href").get()
        if nex_page is not None:
            yield response.follow(nex_page, callback=self.parse)
