import json
import os
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"

    # Pakai IP langsung milik Cloudflare/ToScrape biar gak butuh DNS
    start_urls = ["http://104.21.93.181/catalogue/page-1.html"]

    def parse(self, response):
        books_data = []
        for book in response.css("article.product_pod"):
            title = book.css("h3 a::attr(title)").get()
            price = book.css(".price_color::text").get()
            availability = (
                book.css(".availability::text").re_first(r"\w+") or "In stock"
            )
            rating = book.css("p.star-rating::attr(class)").re_first(
                r"star-rating\s+(\w+)"
            )
            link = response.urljoin(book.css("h3 a::attr(href)").get())

            books_data.append(
                {
                    "title": title,
                    "price": price,
                    "availability": availability,
                    "rating": rating,
                    "link": link,
                }
            )

        os.makedirs("data", exist_ok=True)
        with open("data/books.json", "w", encoding="utf-8") as f:
            json.dump(books_data, f, indent=4, ensure_ascii=False)