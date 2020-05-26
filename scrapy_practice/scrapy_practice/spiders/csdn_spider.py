import scrapy


class CSDNSpider(scrapy.Spider):
    name = 'csdn'

    allow_domains = ['csdn.net']

    start_urls = [
        'https://blog.csdn.net/diuleilaomu'
    ]

    def parse(self, response):
        item_name = ['原创', '粉丝', '获赞', '评论', '访问', '积分', '收藏', '周排名', '总排名']
        item = response.css('.text-center .count::text').getall()
        for i, count in enumerate(item):
            print('%s: %s' % (item_name[i], count), end='\t')
        print('')

        for href in response.css('.article-list a::attr(href)').getall():
            yield response.follow(href, callback=self.parse_article)

    def parse_article(self, response):
        print({
            'Title': response.css('.title-article::text').get(),
            'Read-count': response.css('.read-count::text').get(),
        })