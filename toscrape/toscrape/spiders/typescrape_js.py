import scrapy
from scrapy_playwright.page import PageMethod
from toscrape.loader import ToScrapeLoader


class ToScrapeJs(scrapy.Spider):
    name = "toscrape_js"

    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://quotes.toscrape.com/js/",
            callback=self.parse,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_method=[PageMethod("wait_for", "div.quote")],
            ),
            errback=self.errback,
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()
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
            yield response.follow(
                nex_page,
                callback=self.parse,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_method=[PageMethod("wait_for", "div.quote")],
                ),
                errback=self.errback,
            )

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
