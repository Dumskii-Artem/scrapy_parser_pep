# pep_parse/spiders/pep.py
import re

import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = [f'https://{domain}/' for domain in allowed_domains]

    def parse(self, response):
        for href in response.css(
            'section#index-by-category tbody '
            'tr td:nth-child(3) a::attr(href)'
        ).getall():
            yield response.follow(href, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        yield PepParseItem(
            number=re.search(r'PEP\s+(\d+)', title).group(1),
            name=re.search(r'PEP\s+\d+\s+–\s+(.*)', title).group(1).strip(),
            status=response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get().strip(),
        )
