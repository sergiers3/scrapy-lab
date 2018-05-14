from scrapy import cmdline

cmdline.execute("scrapy crawl imdbscrap -o imdb.json".split())