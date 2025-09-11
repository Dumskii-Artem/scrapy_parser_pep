# pep_parse/spiders/pep.py

import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = [f'https://{domain}/' for domain in allowed_domains]

    def parse(self, response):
        for row in response.css('section#index-by-category tbody tr'):
            if len(row.css('td')) < 3:
                continue
            yield response.follow(
                row.css('td:nth-child(3) a::attr(href)').get(),
                callback=self.parse_pep
            )

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        number = title.re.search(r'PEP\s+(\d+)', title).group(1)
        name = title.re.search(r'PEP\s+\d+\s+–\s+(.*)', title).group(1)
        status = response.css('dt:contains("Status") + dd abbr::text').get()

        yield PepParseItem(
            number=number,
            name=name.strip(),
            status=status.strip(),
        )
