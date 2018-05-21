import os

import scrapy
import unidecode
import re
from elasticsearch import Elasticsearch


ELASTIC_API_URL_HOST = os.environ['ELASTIC_API_URL_HOST']
ELASTIC_API_URL_PORT = os.environ['ELASTIC_API_URL_PORT']
ELASTIC_API_USERNAME = os.environ['ELASTIC_API_USERNAME']
ELASTIC_API_PASSWORD = os.environ['ELASTIC_API_PASSWORD']

es=Elasticsearch(host=ELASTIC_API_URL_HOST,
                 scheme='https',
                 port=ELASTIC_API_URL_PORT,
                 http_auth=(ELASTIC_API_USERNAME,ELASTIC_API_PASSWORD))


cleanString = lambda x: '' if x is None else unidecode.unidecode(re.sub(r'\s+',' ',x))
listActorsUrl = []
listofmovies = []


class ImdbscrapSpider(scrapy.Spider):
    name = 'imdbscrap'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/title/tt0076138/fullcredits/']


    def parse(self, response):

        c = 0
        for row in response.css("table.cast_list>tr"):
            article_url = row.css('td.itemprop>a::attr(href)').extract_first()
            idActor = ""
            try:
                idActor = cleanString(row.css('td.itemprop>a::attr(href)').extract_first().split('/')[2])
                listActorsUrl.append("https://www.imdb.com/name/" + idActor)

                es.index(index='imdb',
                         doc_type='movies',
                         id=uiid.uiid4(),
                         body={
                    'movie_id': cleanString(response.url.split('/')[4]),
                    "movie_name": cleanString(response.css('h3>a::text').extract_first()),
                    "movie_year": cleanString(
                        response.css('span.nobr::text').extract_first().split('(')[1].split(')')[0]),
                    'actor_name': cleanString(row.css('span.itemprop::text').extract_first()),
                    "actor_id": cleanString(row.css('td.itemprop>a::attr(href)').extract_first().split('/')[2]),
                    "role_name": cleanString(row.css('td.character>a::text').extract_first())
                })
            except:
                print("")


        for actor in listActorsUrl:
            yield response.follow(actor, callback=self.get_movies)









    def parse_movie(self, response):
        print("parsemovie")
        for row in response.css("table.cast_list>tr"):
            article_url = row.css('td.itemprop>a::attr(href)').extract_first()
            idActor = ""
            try:
                idActor = cleanString(row.css('td.itemprop>a::attr(href)').extract_first().split('/')[2])
                listActorsUrl.append("https://www.imdb.com/name/" + idActor)

                es.index(index='imdb',
                         doc_type='movies',
                         id=uiid.uiid4(),
                         body={
                    'movie_id': cleanString(response.url.split('/')[4]),
                    "movie_name": cleanString(response.css('h3>a::text').extract_first()),
                    "movie_year": cleanString(
                        response.css('span.nobr::text').extract_first().split('(')[1].split(')')[0]),
                    'actor_name': cleanString(row.css('span.itemprop::text').extract_first()),
                    "actor_id": cleanString(row.css('td.itemprop>a::attr(href)').extract_first().split('/')[2]),
                    "role_name": cleanString(row.css('td.character>a::text').extract_first())
                })
            except:
                print("")





    def get_movies(self, response):
        print("getmovie")

        for row in response.css("div.filmo-category-section a::attr(href)").extract():
            if "pro.imdb" not in row:
                listofmovies.append("https://www.imdb.com" + row)


        for movie in listofmovies:
            yield response.follow(movie, callback=self.parse_movie)

