import scrapy
from tcc.items import TccItem

class TripAdvisorItalianFullSpider(scrapy.Spider):
    name = 'TripadvisorFull FRA'
    allowed_domains = ['tripadvisor.fr']
    start_urls = ['https://www.tripadvisor.fr/ShowForum-g1-i11064-General_Discussion.html']

    # 1. get the first page
    # 2. get all topic links
    # 3. go for the first topic responses
    # 4. parse the posts
    # 5. get the next page
    # 6. go to 2 or end
    # 7. end

    def parse(self, response):
        # get the first main page links
        list_link = response.css("table.topics tr td b a::attr(href)").extract()
        for topic_link in list_link:
            # for each link go to the posts response
            print(topic_link)
            yield response.follow(topic_link, self.parse_responses_page)

        # get the second main page and beyond
        next_main_page = response.css("a.sprite-pageNext::attr(href)").extract_first()
        yield response.follow(next_main_page, self.parse)

    def parse_responses_page(self, reponsesPage):
        for response in reponsesPage.css("div.postcontent"):
            title = "".join(response.css("div.postTitle ::text").extract())
            text = "".join(response.css("div.postBody ::text").extract())
            date = response.css("div.postDate::text").extract_first()
            source = 'tripadvisor_french'
            link = reponsesPage.url

            # before run change the name of the output file in pipelines.py
            parsed = TccItem(title=title, text=text, date=date, source=source, link=link)
            next_page = response.css("a.sprite-pageNext::attr(href)").extract_first()

            # inside a response page navigate
            if next_page is not None:
                yield response.follow(next_page, self.parse_responses_page)

            yield parsed