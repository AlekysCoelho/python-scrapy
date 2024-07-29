from typing import Iterable

import scrapy
from scrapy import Request
from toscrape.loader import ToScrapeLoader


class ToScrapeScrollSpider(scrapy.Spider):
    name = "toscrape_scroll"

    def start_requests(self) -> Iterable[Request]:

        yield scrapy.Request(
            url="https://quotes.toscrape.com/api/quotes?page=1",
            callback=self.parse,
            meta={"page": 1},
        )

    def parse(self, response):
        data_json = response.json()
        for data in data_json["quotes"]:

            loader = ToScrapeLoader(**data)
            loader.add_value("author", data["author"].get("name", "None"))
            loader.add_value("text", data["text"])
            loader.add_value("tags", data["tags"])
            item = loader.load_item()
            yield item

        if data_json.get("has_next"):
            current_page = response.meta.get("page")
            next_page = current_page + 1
            yield scrapy.Request(
                url=f"https://quotes.toscrape.com/api/quotes?page={next_page}",
                callback=self.parse,
                meta={"page": next_page},
            )
