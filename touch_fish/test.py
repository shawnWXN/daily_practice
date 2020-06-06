#!/usr/bin/env python3
# -*- coding = utf-8 -*-
__author__ = 'shawn'
__date__ = '2019/8/10 9:41'


"""
下载网页并查找网页元素
"""
# import requests,bs4,webbrowser,pyperclip,os
# proxies = {
#   'http': 'http://F1331479:Leon168a@10.191.131.12:3128',
#   'https': 'https://F1331479:Leon168a@10.191.131.12:3128',
# }
# res = requests.get('http://yjsy.ncu.edu.cn/www/News_View.asp?NewsID=7985',proxies=proxies)
#
# try:
#   res.raise_for_status()
#   res.encoding = res.apparent_encoding
# except Exception as exc:
#   print('There was a problem:%s'%(exc))
#
# # print(len(res.text))
#
# bsoup = bs4.BeautifulSoup(res.text,features="html.parser")
# elems = bsoup.select('.t4_tr a')
# for e in elems:
#   print(e.text)
#   # print(e.attrs)


"""
自动打开Google搜索结果前几条页面
"""
# keyword = pyperclip.paste()
#
# res = requests.get('https://www.google.com.tw/search?q='+keyword,proxies=proxies)
# try:
#   res.raise_for_status()
#   res.encoding = res.apparent_encoding
# except Exception as exc:
#   print('There was a problem:%s'%(exc))
#
# bsoup = bs4.BeautifulSoup(res.text,features='html.parser')
# elems = bsoup.select('.r a')
# numOpen = min(3,len(elems))
#
# chromePath = r'C:\Users\Administrator.USER-20181225KU\AppData\Local\Google\Chrome\Application\chrome.exe'
# webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chromePath))
#
# for i in range(numOpen):
#   webbrowser.get('chrome').open_new_tab(elems[i].get('href'))


"""
从xkcd网站下载漫画
"""
# import requests,bs4,webbrowser,pyperclip,os
#
# proxies = {
#   'http': 'http://F1331479:Leon168a@10.191.131.12:3128',
#   'https': 'https://F1331479:Leon168a@10.191.131.12:3128',
# }
# # starting url
# url = 'http://xkcd.com'
#
# #create dir
# os.makedirs(os.path.join('E:\\','css'),exist_ok=True)
#
# # Download the page.
# while not url.endswith('#'):
#   print('Downloading page %s'%url)
#   res = requests.get(url,proxies=proxies)
#   try:
#     res.raise_for_status()
#     res.encoding = res.apparent_encoding
#   except Exception as exc:
#     print('There was a problem:%s'%(exc))
#
#   bsoup = bs4.BeautifulSoup(res.text,features='html.parser')
#
#
# # Find the URL of the comic image.
#   comicElem = bsoup.select('#comic img')
#   if comicElem == []:
#     print('Could not find comic image.')
#   else:
#     comicUrl = 'http:'+comicElem[0].get('src')
#     # Download the image.
#     print('Downloading image %s...' % (comicUrl))
#     res = requests.get(comicUrl,proxies=proxies)
#     res.raise_for_status()
#     #Save the image to ./xkcd.
#     imageFile = open(os.path.join('E:\\xkcd',os.path.basename(comicUrl)),'wb')
#     for chunk in res.iter_content(100000):
#       imageFile.write(chunk)
#     imageFile.close()
#
#   #Get the Prev button's url.
#   prevLink = bsoup.select('a[rel="prev"]')[0]
#   url = 'http://xkcd.com'+prevLink.get('href')
#
# print('Done.')


"""
访问首页并模拟点击搜索关键字
"""
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from util import create_proxyauth_extension
#
# #selenium启动chrome之授权代理插件
# proxyauth_plugin_path = create_proxyauth_extension(
#     proxy_host="10.191.131.12",
#     proxy_port=3128,
#     proxy_username="F1331479",
#     proxy_password="Leon168a"
# )
# co = webdriver.ChromeOptions()
# co.add_extension(proxyauth_plugin_path)

# 可以选择不加第一个参数,但要求driver.exe在运行环境的scrip目录下
# browser = webdriver.Chrome('./driver/chromedriver.exe', chrome_options=co)
# browser.get('https://www.zhihu.com/')
# assert '知乎' in browser.title
# elem = browser.find_element_by_id('Popover1-toggle')
# elem.send_keys('flask')
# elem.send_keys(Keys.RETURN)
# print(browser.page_source)


# from urllib import request
# from urllib.error import URLError
#
# user = 'F1331479'
# password = 'Leon168a'
# proxyserver = '10.191.131.12:3128'
# passwdmgr = request.HTTPPasswordMgrWithDefaultRealm()
# passwdmgr.add_password(None,proxyserver,user,password)
# proxyauth_handler = request.ProxyBasicAuthHandler(passwdmgr)
#
# opener = request.build_opener(proxyauth_handler)
# reqUrl = request.Request('https://www.python.org')
#
#
# response = opener.open(reqUrl)
# print(response.read().decode('utf-8'))


"""
读取json文件为python字典
"""
# import json
# json_file = './assy_lines_config.json'
# with open(json_file, mode='r', encoding='utf8') as f:
#     dic = json.load(f)
# print(dic)


"""
将一个字典存入json文件(部分，勿直接取消注释运行)
"""
# target_file = './2.json'
# with open(target_file, 'w', encoding='utf8') as f:
#   json.dump(dic, f, indent=4, ensure_ascii=False)  # 加上的indent参数是格式化json文件，让它以四个空格来美化文件


"""
将字符串转字典（字典转字符直接用str强转）
"""
# import ast
# s = "{'a':1, 'b':2}"
# d = ast.literal_eval(s)
# print(d)

"""
输入某一日期,返回该日期所在周的所有日期(从周一开始)
"""
# import datetime
# def week_get(vdate):
#     dayscount = datetime.timedelta(days=vdate.isoweekday())
#     dayfrom = vdate - dayscount + datetime.timedelta(days=1)
#     dayto = vdate - dayscount + datetime.timedelta(days=7)
#     print(' ~~ '.join([str(dayfrom), str(dayto)]))
#
#     week7 = []
#     i = 0
#     while (i <= 6):
#         week7.append('周' + str(i + 1) + ': ' + str(dayfrom + datetime.timedelta(days=i)))
#         i += 1
#     return week7
# if __name__ == '__main__':
#     vdate_str = '2019-03-19'
#     vdate = datetime.datetime.strptime(vdate_str, '%Y-%m-%d').date()
#
#     for week in week_get(vdate):
#         print(week)


"""
输入某一日期,返回该日期所在周的所有日期(从周一开始),并显示该周属于该年的第几周
"""
# import datetime
# def week_get(vdate):
#     dayscount = datetime.timedelta(days=vdate.isoweekday())
#     dayfrom = vdate - dayscount + datetime.timedelta(days=1)
#     dayto = vdate - dayscount + datetime.timedelta(days=7)
#     print(' ~~ '.join([str(dayfrom), str(dayto)]))
#
#     week7 = []
#     i = 0
#     while (i <= 6):
#         week7.append('周' + str(i + 1) + ': ' + str(dayfrom + datetime.timedelta(days=i)))
#         i += 1
#     return week7
# def weekInYear(vdate_str):
#     date = vdate_str
#     yearWeek = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10])).isocalendar()[0:2]
#     return str(yearWeek[0]) + '#' + str(yearWeek[1])
# if __name__ == '__main__':
#     vdate_str = '2019-05-31'
#     vdate = datetime.datetime.strptime(vdate_str, '%Y-%m-%d').date()
#
#     for week in week_get(vdate):
#         for weekYear in (weekInYear(vdate_str).split()):
#             print(weekYear, week)


"""
返回素数
"""
# def _odd_iter():
#     n = 1
#     while True:
#         n += 2
#         yield n
# def primes():
#     yield 2
#     it = _odd_iter()
#     while True:
#         n = next(it)
#         yield n
#         it = filter(lambda n: lambda x: x%n>0, it)
# for n in primes():
#     if n < 50:
#         print(n)
#     else:
#         break


"""
从IT的Oracle中获取MFGI的数据
"""
# import cx_Oracle as cx
# import json
# import datetime
# import requests
#
# times_fields = ['MACHINE_NAME', 'PASS_TIME', 'RUN_TIME', 'STANDBY_TIME', 'STOP_TIME','ERROR_TIME','PRODUCTCOUNT']
# logs_fields = ['MACHINE_NAME', 'START_TIME', 'END_TIME', 'DESCID', 'DESCRIPTION']
# status_fields = ['MACHINE_NAME', 'VARDATE', 'DESCID', 'DESCRIPTION','PRODUCTCOUNT']
#
# conn = cx.connect('SYSTEM/AUTO168!@192.168.13.195:1521/MFGIAUTO', encoding='UTF-8', nencoding='UTF-8')
#
# cur = conn.cursor()
#
# sql_times = """SELECT {0[0]},{0[1]},{0[2]},{0[3]},{0[4]},{0[5]},{0[6]} FROM SYSTEM.MFGI_ASSY_MACHINE_TIME
#         WHERE PASS_TIME >  to_date('2019-07-18 08:00:00','yyyy-mm-dd hh24:mi:ss')
#         AND PASS_TIME <= to_date('2019-07-25 08:00:00','yyyy-mm-dd hh24:mi:ss')""".format(times_fields)
#
# sql_logs = """SELECT {0[0]},{0[1]},{0[2]},{0[3]},{0[4]} FROM SYSTEM.MFGI_ASSY_MACHINE_ERROR""".format(logs_fields)
#
# # res = cur.execute(sql_times)
#
# res = cur.execute(sql_logs)
#
# result = res.fetchall()
#
# data_dict = {'times': [], 'logs': [], 'state': []}
#
# for tup in result:
#     # data_dict.get('times').append({times_fields[i]: v.strftime('%Y-%m-%d %H:%M:%S') if isinstance(v, datetime.datetime)else v for i, v in enumerate(tup)})
#
#     data_dict.get('logs').append({logs_fields[i]: v.strftime('%Y-%m-%d %H:%M:%S') if isinstance(v, datetime.datetime) else v for i, v in enumerate(tup)})
#
# headers = {'Content-Type': 'application/json'}
#
# respon = requests.post(
#     'http://10.167.219.250:8000/npbg/mfgi/assy-post-origin/',
#     headers=headers,
#     data=json.dumps(data_dict),
# ).text
#
# print(respon)
#
# cur.close()
#
# conn.close()

"""把六处数据从文件中读取出来并post到Genius"""
# import datetime
# import json
# import requests
# required_fields = [
#         'LOG_TIME',
#         'MACHINE_NAME',
#         'D600',
#         'D601',
#         'D602',
#         'D603',
#         'D604',
#         'D605',
#         'D606',
#         'D607',
#         'D608',
#         'D609',
#         'D610',
#         'D611',
#         'D612',
#     ]
# with open('E:\\11M.sql', 'r') as f:
#     result = []
#     count = 0
#     while True:
#         line = f.readline()
#         if line:
#             li = line.split(',', 15)  # 分割15下，形成16个元素的列表，前15是有效的(参考required_fields变量)
#             li.pop()  # 把最后一个多余的去掉
#             # 转换12小时制的字符串类型时间,如'10/15/2019 4:35:39 PM'
#             d = datetime.datetime.strptime(li[0], '%m/%d/%Y %I:%M:%S %p')
#             li[0] = d.strftime('%Y-%m-%d %H:%M:%S')
#             li[1] = li[1][3:]
#             result.append(li)
#             count += 1
#             if count == 1000:
#                 result = [dict(zip(required_fields, row)) for row in result]
#
#                 headers = {'Content-Type': 'application/json'}
#                 respon = requests.post(
#                     'http://10.167.219.250:8000/npbg/mfgvi/assy-post-origin/',
#                     headers=headers,
#                     data=json.dumps({'mfgvi_assy_first_data': result}),
#                 ).text
#                 print(json.loads(respon))
#                 count = 0
#                 result.clear()
#         else:
#             break


# import datetime
# import json
# import requests
# required_fields = [
#         'log_time',
#         'machine_name',
#         'D550',
#         'D551',
#         'D552',
#         'D553',
#         'D554',
#         'D555',
#         'D556',
#         'D557',
#         'D558',
#         'D559',
#         'D560',
#     ]
# with open('E:\\L3.sql', 'r') as f:
#     result = []
#     count = 0
#     while True:
#         line = f.readline()
#         if line:
#             li = line.split(',', 13)  # 分割15下，形成16个元素的列表，前15是有效的(参考required_fields变量)
#             li.pop()  # 把最后一个多余的去掉
#             if li[0].find('下午') == -1:
#                 li[0] = li[0].replace(' 上午', '') + ' AM'
#             else:
#                 li[0] = li[0].replace(' 下午', '') + ' PM'
#             # 转换12小时制的字符串类型时间,如'10/15/2019 4:35:39 PM'
#             d = datetime.datetime.strptime(li[0], '%Y/%m/%d %I:%M:%S %p')
#             li[0] = d.strftime('%Y-%m-%d %H:%M:%S')
#             li[1] = li[1][3:]
#             result.append(li)
#             count += 1
#             if count == 50:
#                 result = [dict(zip(required_fields, row)) for row in result]
#
#                 headers = {'Content-Type': 'application/json'}
#                 respon = requests.post(
#                     'http://localhost:8000/npbg/mfgiii/post-origin/',
#                     headers=headers,
#                     data=json.dumps({'mfgiii_assy_third_data': result}),
#                 ).text
#                 print(json.loads(respon))
#                 count = 0
#                 result.clear()
#         else:
#             break


"""把从Redis中拿出来的数据存至本地数据库"""
# import pymysql
# import datetime
# import re
#
# with open('E:\\data.txt', 'r') as f:
#     result = []
#     count = 0
#     while True:
#         line = f.readline()
#         if line:
#             li = re.split(r'\s+', line)
#             # 转换12小时制的字符串类型时间,如'10/15/2019 4:35:39 PM'
#             d = datetime.datetime.strptime(li[0] + ' ' + li[1], '%Y-%m-%d %H:%M:%S')
#             machine_name = li.pop(2)
#             li = [int(li[i]) for i in range(15) if i > 1]
#             li.insert(0, machine_name)
#             li.insert(0, d)
#             result.append(li)
#         else:
#             break
#
# # 取得连接，其中connect方法参数依次代表[‘数据库IP地址’，‘用户名’，‘密码’，‘数据库名’]
# connect = pymysql.connect('localhost', 'root', 'wang2702', 'practice')
#
# # 取得游标，其中pymysql.cursors.DictCursor代表取出来的结果集为[{'列名1':xxx, '列名2':xxx, ...}，{}，{}...]
# # 也可以不要这个参数，即默认游标，取出来的结果集为( (xxx, xxx, ...), (), (), () )
# cur = connect.cursor(pymysql.cursors.DictCursor)
#
# sql = 'REPLACE INTO tst VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# # 执行sql语句
# cur.executemany(sql, result)
#
# # 获取结果集
# # sql_result = cur.fetchall()
#
# # 提交事务
# connect.commit()
#
# # 关闭游标和数据库连接
# cur.close()
# connect.close()


"""查看MFGI有哪些机器的数据库连不上"""
# import cx_Oracle as cx
#
# conn = cx.connect('SYSTEM/AUTO168!@192.168.13.195:1521/MFGIAUTO', encoding='UTF-8', nencoding='UTF-8')
# cur = conn.cursor()
# sql = """SELECT * FROM SYSTEM.MFGI_MACHINE_IP WHERE temp2=0"""
# cur.execute(sql)
# result = cur.fetchall()
# for tup in result:
#     if tup[0] != '0':
#         print(tup)

"""
从MFGI的工作人员提供的异常对照excel表提取异常
"""
# import openpyxl as xl
# import re
# import json
#
# machine_section = {
#     'PTH': [
#         'Automatic_insertion_1',
#         'Automatic_insertion_2',
#         'Automatic_insertion_3',
#         'Quack_Battery_installation',
#         'PTH_AOI',
#         'ICT',
#     ],
#     'Pre-Assy': [
#         'SFP_heat_sink_installation',
#         'Anchor_heat_sink_installation',
#         'MB_screwing',
#         'Bottom_screwing',
#         'Stand_off_screwing',
#         'Doppler_heat_sink_installation',
#         'FAN_Air_baffle_installation',
#         'BST',
#     ],
#     'Assy': ['Semi_AOI', 'Top_cover_screwing1', 'Top_cover_screwing2', 'Assy_test', 'RFID_Paste_Label'],
#     'Pack': ['FST', 'Hi_pot', 'Packing_AOI'],
# }
# exception_detail = {}
# wb = xl.load_workbook('exception_bak.xlsx')
# sheet_list = wb.get_sheet_names()
# sheet_list.pop(0)
# sheet_list.pop(13)
# sheet_index = 0
# for sect_name, section_list in machine_section.items():
#     exception_detail.setdefault(sect_name, {})
#     for mac in section_list:
#         sheet = wb.get_sheet_by_name(sheet_list[sheet_index])
#         exception_detail.get(sect_name).setdefault(mac, [])
#         for i in range(4, 132):
#             exce_name = sheet['D{}'.format(i)].value
#             if exce_name is not None:
#                 exce_code1 = sheet['B{}'.format(i)].value.split('.')[0]
#                 exce_code2 = exce_name.split('-', maxsplit=1)[0]
#                 exce_name = exce_name.split('-', maxsplit=1)[1]
#                 if exce_name == '':
#                     continue
#                 exce_cause = sheet['G{}'.format(i)].value
#                 temp_list = re.split(r'\s+', exce_cause) if exce_cause else []
#                 exce_cause = '; '.join(temp_list) if temp_list else ''
#                 temp_list.clear()
#                 exce_handle = sheet['H{}'.format(i)].value
#                 temp_list = re.split(r'\s+', exce_handle)if exce_handle else []
#                 exce_handle = '; '.join(temp_list) if temp_list else ''
#                 exception_detail.get(sect_name).get(mac).append((exce_code1+'-'+exce_code2, exce_name, exce_cause, exce_handle))
#         sheet_index += 1
#
# target_file = './2.json'
# with open(target_file, 'w', encoding='utf-8') as f:
#   json.dump(exception_detail, f, indent=4, ensure_ascii=False)  # 加上的indent参数是格式化json文件，让它以四个空格来美化文件


"""将异常对照表的合并单元格拆开"""
# import openpyxl as xl
# wb = xl.load_workbook('exception.xlsx')
# sheet_list = wb.get_sheet_names()
# sheet_list.pop(0)
# sheet_list.pop(13)
# for sheet_name in sheet_list:
#     sheet = wb.get_sheet_by_name(sheet_name)
#     for cell in sheet.merged_cell_ranges:
#         tup = cell.bounds  # 假定A4:C5是合并的单元格，则得到(1,4,3,5)
#         # s = cell.coord  # 得到的是一个字符串，如"A4:C5"
#         if tup[0] >= 4 and tup[1] >= 4 and tup[2] <= 9 and tup[3] <= 131:
#             row = tup[1]
#             col = tup[0]
#             data = sheet.cell(row=row, column=col).value
#             sheet.unmerge_cells(cell.coord)
#             while col <= tup[2]:
#                 while row <= tup[3]:
#                     sheet.cell(row=row, column=col).value = data
#                     row += 1
#                 col += 1
# wb.save('exception_bak.xlsx')

# import openpyxl as xl
# import pymysql
# wb = xl.load_workbook('test_bak.xlsx')
# sheet_list = wb.get_sheet_names()
# result = []
# for sheet_name in sheet_list:
#     sheet = wb.get_sheet_by_name(sheet_name)
#     row = 2
#     flag = False
#     cell = 0
#     for row in range(2, 1000):
#         category = sheet.cell(row=row, column=1).value
#         if category is None:
#             break
#         station = sheet.cell(row=row, column=2).value
#         hostname = sheet.cell(row=row, column=3).value
#         slot_range = sheet.cell(row=row, column=4).value
#         slot_start = int(slot_range.split('-')[0])
#         slot_end = int(slot_range.split('-')[1])
#
#         if row != 2:
#             pre_category = sheet.cell(row=row - 1, column=1).value
#             pre_station = sheet.cell(row=row - 1, column=2).value
#             if pre_category != category or pre_station != station:
#                 cell = 0
#         for slot in range(slot_start, slot_end + 1):
#             cell += 1
#             result.append(
#                 [category, station, cell, hostname, slot]
#             )
# print(result)
#
# # 取得连接，其中connect方法参数依次代表[‘数据库IP地址’，‘用户名’，‘密码’，‘数据库名’]
# connect = pymysql.connect('10.167.219.250', 'npbg', 'Fox1230!', 'npbg')
#
# # 取得游标，其中pymysql.cursors.DictCursor代表取出来的结果集为[{'列名1':xxx, '列名2':xxx, ...}，{}，{}...]
# # 也可以不要这个参数，即默认游标，取出来的结果集为( (xxx, xxx, ...), (), (), () )
# cur = connect.cursor(pymysql.cursors.DictCursor)
#
# sql = 'REPLACE INTO mfgvi_test_cell_config VALUES (%s, %s, %s, %s, %s)'
# # 执行sql语句
# cur.executemany(sql, result)
#
# # 获取结果集
# # sql_result = cur.fetchall()
#
# # 提交事务
# connect.commit()
#
# # 关闭游标和数据库连接
# cur.close()
# connect.close()


"""随机菜单"""
# import random
# Order = [
#     '鸡翅', '青椒肉丝', '小鸡腿肉', '鱼', '排骨土豆', '炖猪蹄', '水煮肉片', '青椒炒蛋', '藕片', '土豆丝', '麻婆豆腐', '青椒西红柿',
#     '黄瓜火腿', '莴笋丝', '胡萝卜丝'
# ]
# index = random.randint(1, len(Order))
# print(Order[index-1])
# index = random.randint(1, len(Order))
# print(Order[index-1])


"""给六处测试2k工站传绿灯"""
# import time
# import json
# import requests
# import datetime
# request_body = {
#   "mfgvi_test_Barbados2K_data": [
#     {
#       "LOG_TIME": "",
#       "MACHINE_NAME": "Barbados_BDL_2K",
#       "D600": "0",
#       "D601": "0",
#       "D602": "0",
#       "D603": "2",
#       "D604": "0",
#       "D605": "0",
#       "D606": "0",
#       "D607": "0",
#       "D608": "0",
#       "D609": "0",
#       "D610": "0",
#       "D611": "0",
#       "D612": "0"
#     },
#     {
#       "LOG_TIME": "",
#       "MACHINE_NAME": "Barbados_BPM2_2K",
#       "D600": "0",
#       "D601": "0",
#       "D602": "0",
#       "D603": "2",
#       "D604": "0",
#       "D605": "0",
#       "D606": "0",
#       "D607": "0",
#       "D608": "0",
#       "D609": "0",
#       "D610": "0",
#       "D611": "0",
#       "D612": "0"
#     }
#   ]
# }
#
# while True:
#     now_time = datetime.datetime.now() - datetime.timedelta(seconds=10)
#     request_body.get('mfgvi_test_Barbados2K_data')[0]['LOG_TIME'] = now_time.strftime('%Y-%m-%d %H:%M:%S')
#     request_body.get('mfgvi_test_Barbados2K_data')[1]['LOG_TIME'] = now_time.strftime('%Y-%m-%d %H:%M:%S')
#     headers = {'Content-Type': 'application/json'}
#
#     respon = requests.post(
#         'http://10.132.46.51:80/npbg/mfgvi/test-post-origin/',
#         headers=headers,
#         data=json.dumps(request_body),
#     )
#     print('Response:', respon.status_code)
#     print(respon.text)
#     time.sleep(300)

# def consumer():
#     r= ''
#     while True:
#         n = yield r
#         if not n:
#             return
#         print('[CONSUMER] Consuming %s...' % n)
#         r = '200 OK'
# def produce(c):
#     c.send(None)
#     n = 0
#     while n < 5:
#         n += 1
#         print('[PRODUCE] Producing %s...' % n)
#         r = c.send(n)
#         print('[PRODUCE] return: %s...' % r )
#     c.close()
# c = consumer()
# produce(c)


# import pymssql
# # with语句与连接和游标一起使用，不必显式关闭游标和连接。
#
# with pymssql.connect('10.167.219.229:3000', 'sa', 'Wstg168!!!', 'FOCTestRecord2020') as conn:
#     with conn.cursor(as_dict=True) as cursor:
#         cursor.execute('SELECT machine, rectime, uuttype FROM dbo.tbl_record_202001 WHERE sernum=%s', 'FCW2353C0BP')
#         for row in cursor:
#             print("machine=%s, rectime=%s, uuttype=%s" % (row['machine'], row['rectime'], row['uuttype']))
#
# print(conn)
# print(cursor)
# 调用存储过程
# with pymssql.connect(server, user, password, "tempdb") as conn:
#     with conn.cursor(as_dict=True) as cursor:
#         cursor.execute("""
#         CREATE PROCEDURE FindPerson
#             @name VARCHAR(100)
#         AS BEGIN
#             SELECT * FROM persons WHERE name = @name
#         END
#         """)
#         cursor.callproc('FindPerson', ('Jane Doe',))
#         for row in cursor:
#             print("ID=%d, Name=%s" % (row['id'], row['name']))


# class Solution:
#     def canThreePartsEqualSum(self, A) -> bool:
#         tup = divmod(sum(A), 3)
#         if tup[1]:
#             return False
#
#         length = len(A)
#         i = j = None
#         lo = 0
#         hi = length - 1
#         while(lo + 1 < hi):
#             if not i:
#                 if sum(A[0:lo+1]) == tup[0]:
#                     i = lo
#                 else:
#                     lo += 1
#             if not j:
#                 if sum(A[hi: length]) == tup[0]:
#                     j = hi
#                 else:
#                     hi -= 1
#             if i is not None and j is not None:
#                 return True
#         return False
#
#
# if __name__ == '__main__':
#     S = Solution()
#     print(S.canThreePartsEqualSum([0,2,1,-6,6,-7,9,1,2,0,1]))


# import pymysql
# import openpyxl as xl
#
# wb = xl.open('UAG.xlsx')
#
# sheet = wb.get_sheet_by_name('Sheet4')
#
# data = []
# for i in range(1, 669):
#     category = sheet.cell(row=i, column=1).value
#     s_seq = sheet.cell(row=i, column=2).value
#     station = sheet.cell(row=i, column=3).value
#     cell_in_plc = sheet.cell(row=i, column=4).value
#     hostname = sheet.cell(row=i, column=5).value
#     slot = sheet.cell(row=i, column=6).value
#     uut = sheet.cell(row=i, column=8).value
#     source = sheet.cell(row=i, column=9).value
#     cost = sheet.cell(row=i, column=10).value
#     if isinstance(cost, str):
#         cost = cost[1:]
#         cost = eval(compile(cost, '', 'eval'))
#     data.append([
#         category, s_seq, station, cell_in_plc, hostname, slot, '', uut, source, cost
#     ])
#
# conn = pymysql.connect('10.167.219.250', 'npbg', 'Fox1230!', 'npbg')
# cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
# sql = """REPLACE INTO mfgvi_test_cell_config VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
# cur.executemany(sql, data)
#
# conn.commit()
#
# cur.close()
# conn.close()


# from collections import OrderedDict
# import openpyxl as xl
# import pymysql
# conn = pymysql.connect('10.167.219.250', 'npbg', 'Fox1230!', 'npbg')
# cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
#
# wb = xl.load_workbook('E:\\UDTS-OUTPUT-BAK.xlsx')
# sheet_names = wb.get_sheet_names()
#
# xlsx_data = {}
# for name in sheet_names:
#     sheet = wb.get_sheet_by_name(name)
#     col = 7
#     row = 2
#     data = []
#     reuse_set = set()
#     while 1:
#         if not sheet.cell(row=row, column=1).value:
#             break
#         row_data = [sheet.cell(row=row, column=i).value for i in range(1, col + 1)]
#         rst_str = row_data.pop().split(';')[-3][5:-1]
#         row_data.append(rst_str)
#         row_data.insert(0, name)
#         row_data[6] = row_data[6].strip(',')
#         if '%'.join(row_data[:3]) not in reuse_set:
#             data.append(row_data)
#         row += 1
#     xlsx_data.setdefault(name, data)
#
# for bu, sheet_list in xlsx_data.items():
#     sheet_list.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
#     # if bu == 'UAG':
#     #     temp_dict = OrderedDict()
#     #     for row_data in sheet_list:
#     #         c = row_data[1]
#     #         s = row_data[2]
#     #
#     #         solts = row_data[-1].split('`')[3::2]
#     #         if solts:
#     #             if row_data[3] == 'fxcavp637':
#     #                 solts = [i for i in range(101, 217) if i <= 116 or i >= 201]
#     #             for slot in solts:
#     #                 temp_dict.setdefault(c, {}).setdefault(s, []).append(
#     #                     [row_data[0].strip(),
#     #                      row_data[1].strip(),
#     #                      row_data[2].strip(),
#     #                      row_data[3].strip(),
#     #                      int(slot),
#     #                      row_data[6].strip(),
#     #                      row_data[5]
#     #                      ]
#     #                 )
#     #         else:
#     #             temp_dict.setdefault(c, {}).setdefault(s, []).append(
#     #                 [row_data[0].strip(),
#     #                  row_data[1].strip(),
#     #                  row_data[2].strip(),
#     #                  row_data[3].strip(),
#     #                  0,
#     #                  row_data[6].strip(),
#     #                  row_data[5] // int(row_data[4].split('(')[0])
#     #                  ]
#     #             )
#     #
#     #     sql = """INSERT INTO nsdi_tst_cell_config_bak VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#     #     s_index = 0
#     #     c_index = 0
#     #     for c, dict1 in temp_dict.items():
#     #         for s, li in dict1.items():
#     #             s_index += 1
#     #             for details in li:
#     #                 c_index += 1
#     #                 details.insert(2, s_index)
#     #                 details.insert(6, c_index)
#     #             c_index = 0
#     #             cur.executemany(sql, li)
#     #         s_index = 0
#     if bu == 'CSPG':
#         temp_dict = OrderedDict()
#         for row_data in sheet_list:
#             c = row_data[1]
#             s = row_data[2]
#             solts = row_data[-1].split('`')[3::2]
#             if solts:
#                 slot_num = int(row_data[4].split('(')[0])
#                 for slot in range(1, slot_num + 1):
#                     temp_dict.setdefault(c, {}).setdefault(s, []).append(
#                         [row_data[0].strip(),
#                          row_data[1].strip(),
#                          row_data[2].strip(),
#                          row_data[3].strip(),
#                          slot,
#                          row_data[6].strip(),
#                          row_data[5]
#                          ]
#                     )
#             else:
#                 temp_dict.setdefault(c, {}).setdefault(s, []).append(
#                     [row_data[0].strip(),
#                      row_data[1].strip(),
#                      row_data[2].strip(),
#                      row_data[3].strip(),
#                      0,
#                      row_data[6].strip(),
#                      row_data[5] // (int(row_data[4].split('(')[0]) if isinstance(row_data[4], str) else row_data[4])
#                      ]
#                 )
#
#         sql = """INSERT INTO nsdi_tst_cell_config_bak VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#         s_index = 0
#         c_index = 0
#         for c, dict1 in temp_dict.items():
#             for s, li in dict1.items():
#                 s_index += 1
#                 for details in li:
#                     c_index += 1
#                     details.insert(2, s_index)
#                     details.insert(6, c_index)
#                 c_index = 0
#                 cur.executemany(sql, li)
#             s_index = 0
# conn.commit()
# cur.close()
# conn.close()

# import pymysql
# conn = pymysql.connect('10.167.219.250', 'npbg', 'Fox1230!', 'npbg')
# cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
#
# sql = """SELECT *
# FROM nsdi_tst_cell_config_bak"""
# cur.execute(sql)
# rst = cur.fetchall()
#
# result = []
# for d in rst:
#     d['category'] = d['category'].replace('-', '_')
#     result.append(list(d.values()))
# sql = 'TRUNCATE TABLE npbg.nsdi_tst_cell_config_bak'
# cur.execute(sql)
# sql = """INSERT INTO nsdi_tst_cell_config_bak VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
# cur.executemany(sql, result)
# conn.commit()
# cur.close()
# conn.close()

# def func(str_arrays):
#     loop_count = min([len(s) for s in str_arrays])
#     common_str = ''
#     for i in range(loop_count):
#         for j, s in enumerate(str_arrays):
#             if s[:i+1] != str_arrays[0][:i+1]:
#                 break
#         else:
#             common_str = str_arrays[0][:i+1]
#     if common_str == '':
#         return '没有最大公共串'
#     return common_str
#
#
# if __name__ == '__main__':
#     s_arrays = []
#     print(func(s_arrays))

# 有一个大CSV文件，需要将数据转移到另一个CSV文件
# 谈谈多进程多线程
# 字符串的各内置方法
# redis数据类型。常见方法
# SQL

import pandas as pd
import numpy as np
import time

df = pd.DataFrame(np.random.randn(1000000, 14), index=pd.date_range('20180101 01', periods=1000000, freq='H'), columns=list('ABCDEFGHIJKLMN'))
df.to_csv('tst.csv')

s_time = time.time()
reader = pd.read_csv('tst.csv', chunksize=1000)
for chunk in reader:
    chunk.to_csv('tst_bak.csv', mode='a')
print('costs time ', time.time() - s_time)

import functools


