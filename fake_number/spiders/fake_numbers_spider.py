import scrapy


class FakePhone(scrapy.Spider):
    # spider name
    name = "numbers"
    start_urls = ["https://fakenumber.org/"]

    def parse(self, response):
        for title in response.css("div.row"):
            yield {
                "phone_number": title.css("h4::text").getall(),
                #'phone_numbers': title.css("div.grid_6 h4 a::text").getall()
            }
            for numbers in response.css("div.grid3"):
                yield {
                    "phone_numbers1": numbers.css("h4::text").getall(),
                }

            current_pages = response.css("h4 a::attr(href)").getall()
            for url in current_pages:
                url = response.urljoin(url)
                yield scrapy.Request(url, callback=self.parse)

        all_pages = response.css("nav")[2].css("ul a::attr(href)").getall()
        for url in all_pages:
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse)
