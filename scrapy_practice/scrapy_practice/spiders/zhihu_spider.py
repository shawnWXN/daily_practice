import scrapy


class ZhiHuSpider(scrapy.Spider):
    name = 'zhihu'

    allow_domains = ['zhihu.com']

    start_urls = [
        'https://www.zhihu.com/explore'
    ]

    def parse(self, response):
        for href in response.css('.ExploreSpecialCard-contentTitle::attr(href)'):
            yield response.follow(href, callback=self.parse_article)

    def parse_article(self, response):
        yield {
            'Title': response.css('.QuestionHeader-title::text').get(),
            'Desc': response.xpath('//*[@id="QuestionAnswers-answers"]/div/div/div/div[1]/h4/span/text()').get(),
            'NumberBoard': response.css('.NumberBoard-itemValue::text').getall(),
        }