# pep_parse/spiders/pep.py

import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        rows = response.css('section#index-by-category tbody tr')
        for row in rows:
            td_tags = row.css('td')
            if len(td_tags) < 3:
                continue

            # ссылка на страницу PEP
            link = td_tags[2].css('a::attr(href)').get()
            if link:
                yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        number = response.css('h1.page-title::text').re_first(r'PEP\s+(\d+)')
        name = response.css('h1.page-title::text').re_first(
            r'PEP\s+\d+\s+–\s+(.*)')

        status = response.xpath(
            '//dt[starts-with(normalize-space(), "Status")]'
            '/following-sibling::dd[1]//text()'
        ).get()

        yield PepParseItem(
            number=number,
            name=name.strip() if name else '',
            status=status.strip() if status else '',
        )
