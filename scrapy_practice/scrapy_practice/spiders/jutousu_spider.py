import scrapy
from scrapy.selector import Selector


class JutousuSpider(scrapy.Spider):
    name = 'jutousu'

    allow_domains = ['ts.21cn.com']

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Host': 'ts.21cn.com',
            # 'Referer': 'http://ts.21cn.com/',
            # 'referer': 'https://mm.taobao.com/search_tstar_model.htm?spm=719.1001036.1998606017.2.KDdsmP',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'cookie': 'channelId=null; apm_ct=20200604093108164; apm_sid=F4798B7F7B77E585EBB3286392F98AF8; apm_uid=BE0197A56733E0D1000865E90E9DBCAD; apm_ip=10.167.2.109; apm_ua=3159E548B459A213A1C6A2A1736EE626'
        },
    }

    def start_requests(self):
        url = [
            'http://ts.21cn.com/json/indexPcMorePost/order/ctime/pageNo/1',
            'http://ts.21cn.com/json/indexPcMorePost/order/itfin/pageNo/1'
        ]
        return url

    def parse(self, response):
        selector = Selector(response['message'])
        self.log(selector)
        # item_name = ['原创', '粉丝', '获赞', '评论', '访问', '积分', '收藏', '周排名', '总排名']
        # item = response.css('.text-center .count::text').getall()
        # for i, count in enumerate(item):
        #     print('%s: %s' % (item_name[i], count), end='\t')
        # print('')
        #
        # for href in response.css('.article-list a::attr(href)').getall():
        #     yield response.follow(href, callback=self.parse_article)