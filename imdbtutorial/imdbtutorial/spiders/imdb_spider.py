import scrapy
from imdbtutorial.items import MovieItem, CastItem
class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    base_url = "https://imdb.com"
    start_urls = ['https://www.imdb.com/chart/top' ,]

    def parse(self, response):
        # table coloums of all the movies
        columns = response.css('table[data-caller-name="chart-top250movie"] tbody[class="lister-list"] tr')
        for col in columns:

            rating = col.css("td[class='titleColumn']::text").extract_first().strip()

            rel_url = col.css("td[class='titleColumn'] a::attr('href')").extract_first().strip()

            col_url = self.base_url + rel_url

            yield scrapy.Request(col_url, callback=self.parseDetailItem, meta={'rating': rating})


    def parseDetailItem(self, response):

        item = MovieItem()

        item["rating"] = response.meta["rating"]

        item['title'] = response.css('div[class="title_wrapper"] h1::text').extract_first().strip()
        item["summary"] = response.css("div[class='summary_text']::text").extract_first().strip()
        item['directors'] = response.css('div[class="credit_summary_item"] a::text').extract()[0].strip()
        item['writers'] = response.css('div[class="credit_summary_item"] a::text').extract()[1].strip()
        item["genre"] = response.xpath \
            ("//*[@id='title-overview-widget']/div[1]/div[2]/div/div[2]/div[2]/div/a[1]/text()").extract_first().strip()
        item["runtime"] = response.xpath \
            ("//*[@id='title-overview-widget']/div[1]/div[2]/div/div[2]/div[2]/div/time/text()").extract_first().strip()


        item["cast"] = list()


        for cast in response.css("table[class='cast_list'] tr")[1:]:
            castItem = CastItem()
            castItem["name"] = cast.xpath("td[2]/a/text()").extract_first().strip()
            castItem["character"] = cast.css("td[class='character'] a::text").extract_first()
            item["cast"].append(castItem)

        return item