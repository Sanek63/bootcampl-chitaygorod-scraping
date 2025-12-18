import scrapy

from chitaygorod.items import ChitaygorodItem


class ChitaiGorodRuSpider(scrapy.spiders.SitemapSpider):
    name = "chitai_gorod_ru"
    allowed_domains = ["chitai-gorod.ru"]

    sitemap_follow = ["/products"]
    sitemap_urls = ["https://www.chitai-gorod.ru/sitemap.xml"]
    sitemap_rules = [("product/", "parse"),]

    currency_mapping = {
        "₽": "RUB"
    }

    custom_settings = {
        "ITEM_PIPELINES": {
            "chitaygorod.pipelines.MongoPipeline": 300
        }
    }

    def _extract_price_info(self, response: scrapy.http.Response) -> tuple[int, str]:
        old_price_raw = response.xpath("//span[@class='product-offer-price__old-text']/text()").get()
        if old_price_raw:
            old_price_parts = old_price_raw.replace("&nbsp;", "").strip().split(" ")
            return int(old_price_parts[0]), self.currency_mapping[old_price_parts[1]]

        new_price = response.xpath("//div[@class='product-offer']//meta[@itemprop='price']/@content").get()
        if not new_price:
            return 0, "RUB"
        if "." in new_price:
            new_price = new_price.split(".")[0]
        new_currency = response.xpath("//div[@class='product-offer']//meta[@itemprop='priceCurrency']/@content").get()
        return int(new_price), new_currency

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        isbn = response.xpath("//span[@itemprop='isbn']/span/text()").get()
        if not isbn:
            return

        author = response.xpath('//ul[@class="product-authors"]//li/a/text()').get()
        description = response.xpath("//section[@class='product-description-short product-detail-page__short-text']/div[@class='product-description-short__text']/text()").get()
        # price_amount = response.xpath("//meta[contains(@itemprop, 'price')]/@content").get()
        # price_currency = response.xpath("//meta[contains(@itemprop, 'priceCurrency')]/@content").get()
        price_amount, price_currency = self._extract_price_info(response)
        rating_value = response.xpath("//span[@class='product-rating-detail__count']/text()").get()
        rating_count = response.xpath("//span[contains(., 'оценок')]/@content").get()
        publication_year = response.xpath("//span[@itemprop='datePublished']//span/text()").get()
        pages_cnt = response.xpath("//div[@id='properties']//span[@itemprop='numberOfPages']/span/text()").get()
        publisher = response.xpath('//span[@itemprop="publisher"]/@content').get()
        book_cover = response.xpath("//div[@class='product-preview']//img/@src").get()
        source_url = response.url

        return ChitaygorodItem(
            title=title,
            author=author,
            description=description,
            price_amount=price_amount,
            price_currency=price_currency,
            rating_value=rating_value,
            rating_count=rating_count,
            publication_year=publication_year,
            isbn=isbn,
            pages_cnt=pages_cnt,
            publisher=publisher,
            book_cover=book_cover,
            source_url=source_url,
        )
