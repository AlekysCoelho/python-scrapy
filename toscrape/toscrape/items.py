import scrapy
from itemloaders.processors import Join, MapCompose


def define_thumbnail_absolute_url(url, loader_context):
    """Join the image URL with the response URL."""
    return loader_context["response"].urljoin(url)


def remove_double_quote_characters(value):
    """remove double quote characters"""
    return value.strip("“”")


class ToscrapeItem(scrapy.Item):
    text = scrapy.Field(input_processor=MapCompose(remove_double_quote_characters))
    author = scrapy.Field()
    tags_links = scrapy.Field(
        input_processor=MapCompose(define_thumbnail_absolute_url),
        output_processor=Join(", "),
    )
    tags_names = scrapy.Field(output_processor=Join(", "))
    tags = scrapy.Field(output_processor=Join(", "))
