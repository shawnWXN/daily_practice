import requests
import json
from lxml import etree

header = {
    'Proxy-Authorization': 'Basic RjEzMzQ1MzU6c2hhd24xNjhh',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://ts.21cn.com/',
    'Cookie': 'channelId=null; apm_ct=20200604093108164; apm_uid=BE0197A56733E0D1000865E90E9DBCAD; apm_ip=10.167.2.109; apm_ua=3159E548B459A213A1C6A2A1736EE626',
    'Host': 'ts.21cn.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
}

proxy = {
    'http': 'http://F1331479:Leon168a@10.191.131.12:3128',
    'https': 'https://F1331479:Leon168a@10.191.131.12:3128',
}

for number in range(1, 2):
    resp = requests.get(url='http://ts.21cn.com/json/indexPcMorePost/order/hit/pageNo/{}'.format(number), headers=header, proxies=proxy)
    html = json.loads(resp.text).get('message')
    html = etree.parse(html, etree.HTMLParser)
    divs = html.xpath("//div[@class='ind_list_all']")
    # print(divs)
    # haha = divs.find('.ind_ding .label a')
    label_html = divs.findall('.ind_ding .label a')
    title_html = divs.findall('.con_info a')
    dt_html = divs.findall('.con_info p')
    dictionary = {}
    for e in label_html:
    #     print(div.text())
        # // *[ @ id = "nn0"] / div[1] / div[1] / p / span[3] / a
        # print(type(div))

        dictionary['label'] = e.text()
        dictionary['title'] = title_html[0].text()
        dictionary['dt'] = dt_html[0].text()
        print(dictionary)

