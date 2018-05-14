import scrapy
import unidecode
import re

cleanString = lambda x: '' if x is None else unidecode.unidecode(re.sub(r'\s+',' ',x))


class ImdbscrapSpider(scrapy.Spider):
    name = 'imdbscrap'
    '''allowed_domains = ['https://www.imdb.com/title/tt0096463/fullcredits/']'''
    allowed_domains = ['https://www.imdb.com/title/', 'https://www.imdb.com/name/']
    start_urls = ['https://www.imdb.com/title/tt0076138/fullcredits/']

    def parse(self, response):
        for row in response.css("table.cast_list>tr"):
            article_url = row.css('td.itemprop>a::attr(href)').extract_first()


            try:
                yield {
                    'movie_id': cleanString(response.url.split('/')[4]),
                    "movie_name": cleanString(response.css('h3>a::text').extract_first()),
                    "movie_year": cleanString(response.css('span.nobr::text').extract_first().split('(')[1].split(')')[0]),
                    'actor_name': cleanString(row.css('span.itemprop::text').extract_first()),
                    "actor_id": cleanString(row.css('td.itemprop>a::attr(href)').extract_first().split('/')[2]),
                    "role_name": cleanString(row.css('td.character>a::text').extract_first())
                }
            except:
                print("")



            next_page = article_url
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_article)


    def parse_article(self, response):
        print("ejnfopwefwepfnn'fb2fp32b9f")
        yield {
             'movie_id': cleanString(cleanString(response.url.split('/')[4])),
                "movie_name": cleanString(response.css('h3>a::text').extract_first()),
                "movie_year": cleanString(response.css('span.nobr::text').extract_first().split('(')[1].split(')')[0]),
                'actor_name': cleanString(response.css('span.itemprop::text').extract_first()),
                "actor_id": cleanString(response.css('td.itemprop>a::attr(href)').extract_first().split('/')[2]),
                "role_name": cleanString(response.css('td.character>a::text').extract_first())
        }


