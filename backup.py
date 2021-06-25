import scrapy
from imdbtutorial.items import MovieItem,CastItem

class ImdbSpiderSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['imdb.com']
    start_urls = ["http://www.imdb.com/chart/top"]

    def parse(self, response):
        movies =response.css('table[data-caller-name="chart-top250movie"] tbody[class="lister-list"] tr')
        for movie in movies:

            yield {
                "title": movie.css("td[class='titleColumn'] a::text").extract_first(),
                "year": movie.css("td[class='titleColumn'] span::text").extract_first().strip("() "),
                "rating": movie.css("td[class='ratingColumn imdbRating'] strong::text").extract_first(),