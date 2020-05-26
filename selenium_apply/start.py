#!/usr/bin/env python3
# -*- coding = utf-8 -*-
__author__ = 'shawn'
__date__ = '2019/8/5 16:54'

"""
Updated at  2019/07/26
@title: 使用selenium库自动报加班
@author: shawn
"""
import json
import time
import sys
import datetime

from chaojiying import Chaojiying_Client
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

co = webdriver.ChromeOptions()
co.add_argument('--user-agent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"')
co.add_argument('--disable-infobars')  # 清除浏览器上方“正在受自动化软件控制”字样
co.add_argument('--headless')   # 无头模式
co.add_argument('--log-level=3')   # 禁用日志:0代表显示所有(它也是默认值),1代表显示warning以及更重大的log,2代表error以及更重大的log,3代表只显示fatal的log

# 创建超级鹰实例
chaojiying = Chaojiying_Client('shawnWXN', '123456', '23642c06785d415bfb0e9a738adfce91')

# 打开登陆页
host = 'http://10.132.37.98/'
browser = webdriver.Chrome('./driver/chromedriver.exe', chrome_options=co)
wait = WebDriverWait(browser, 10)
browser.get(host)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))

# 加载任务文件
with open('task.json', encoding='utf8') as f:
    task_dict = json.load(f)
default_start_time = task_dict.get('default_start_time', '17:00')
default_end_time = task_dict.get('default_end_time', '19:00')
default_continuous = task_dict.get('default_continuous', 'Y')

print('{}开始登陆:HRM:系统'.format(task_dict.get('username')))

# 登陆
while True:
    username = browser.find_element_by_id('txtUserName')
    password = browser.find_element_by_id('txtPassWord')
    captcha_input = browser.find_element_by_name('CaptchaControl1')
    login_button = browser.find_element_by_id('Btn_Login')
    username.clear()

    username.send_keys(task_dict.get('username'))
    password.send_keys(task_dict.get('password'))

    img_tag = browser.find_element_by_css_selector('#Table2 img')
    img_byte = img_tag.screenshot_as_png
    # 向打码平台发送验证码
    try:
        captcha_result = chaojiying.PostPic(img_byte, 1902)
    # 如果超级鹰实例创建失败或者发送不了验证码，就用pillow显示，然后让用户手动输入
    except Exception:
        Image.open(BytesIO(img_byte)).show()
        pic_str = input('請輸入驗證碼\n>')
    else:
        # 如果识别不了验证码，就手动
        if captcha_result.get('pic_str', '') == '':
            Image.open(BytesIO(img_byte)).show()
            pic_str = input('請輸入驗證碼\n>')
        else:
            pic_str = captcha_result.get('pic_str', 'null')
    finally:
        captcha_input.send_keys(pic_str)

    login_button.click()
    try:
        login_alert = browser.switch_to.alert
    except Exception as e:
        break
    else:
        time.sleep(1)
        print('error:{}'.format(login_alert.text))
        # 如果alert显示密码输入错误XXXX的字样，就立刻终止程序，防止错误次数多锁号
        if '密碼輸入錯誤' in login_alert.text:
            browser.close()
            sys.exit(0)
        # 如果alert显示'修改密碼XXX'的字样，就立刻终止程序，提示去修改网域密码
        elif '修改密碼' in login_alert.text:
            browser.close()
            sys.exit(0)
        else:
            login_alert.accept()
            if captcha_result and captcha_result.get('im_id'):
                chaojiying.ReportError(captcha_result.get('im_id'))


# 打开左侧导航栏获取用户姓名和登陆时间
browser.get(host+'System/frmLeft.aspx')
print('Welcome {}, login at {}'.format(browser.find_element_by_id('lbl_Name').text, browser.find_element_by_id('lbl_Time').text))

# 开始扫描当月考勤
# wk = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "日"}
# today = datetime.date.today()
# first_date = today.replace(day=1)
# while first_date < today:
#     browser.get(host + 'Duty/frmAnalysis.aspx')
#
#     txt_date = browser.find_element_by_id('txtDates')
#     txt_date.clear()
#     txt_date.send_keys(first_date.strftime("%Y/%m/%d"))
#
#     browser.find_element_by_id('btnSearch').send_keys(Keys.ENTER)
#
#     result_tr_list = browser.find_elements_by_xpath('//*[@id="DG_RESULT"]/tbody/tr[2]/td')
#
#     print('{}(周{}) 考勤:{}, '.format(first_date.strftime('%Y/%m/%d'), wk.get(first_date.isoweekday()), result_tr_list[5].text), end='')
#     if result_tr_list[5].text == '正常':
#
#         if result_tr_list[12].text == ' ':
#             continuous_flag = True
#             start_str = '17:30:00'
#             start_time = datetime.datetime(first_date.year, first_date.month, first_date.day, 17, 30)
#         else:
#             continuous_flag = False
#             start_str = result_tr_list[12].text
#             start_time = datetime.datetime(first_date.year, first_date.month, first_date.day, 18, 30)
#
#         end_str = result_tr_list[13].text
#         end_time = datetime.datetime.strptime(end_str, '%H:%M:%S')
#         end_time = end_time.replace(year=first_date.year, month=first_date.month, day=first_date.day)
#
#         over_time = (end_time - start_time).seconds
#         # 最小加班0.5H
#         over_time = over_time // 1800 / 2
#         print('{}加班{}H, 从{}~{}'.format('连班' if continuous_flag else '不连班', over_time, start_str, end_str))
#         task_dict.setdefault('practical_job', []).append({
#             "have_predict": "False",
#             "date": first_date.strftime('%Y/%m/%d'),
#             "start_time": start_time.strftime('%H:%M'),
#             "end_time": end_time.strftime('%H:%M'),
#             "continuous": 'Y' if continuous_flag else 'N'
#         })
#     elif result_tr_list[5].text in ['周六', '周日']:
#         if result_tr_list[13].text == ' ':
#             print('没有上班')
#         else:
#             print('有上班, 从08:30:00~17:30:00')
#             task_dict.setdefault('practical_job', []).append({
#                 "have_predict": "True",
#                 "date": first_date.strftime('%Y/%m/%d'),
#                 "start_time": '08:30',
#                 "end_time": '17:30',
#                 "continuous": 'N'
#             })
#     else:
#         print('异常分钟数{}'.format(result_tr_list[6].text))
#
#     first_date += datetime.timedelta(days=1)
#
# print('pause')
# 开始预报加班
for job_dict in task_dict.get('prediction_job', []):
    print('开始预报{} {}~{}的加班...'.format(
        job_dict.get('date', 'null'),
        job_dict.get('start_time', default_start_time),
        job_dict.get('end_time', default_end_time)
        ),
        end=''
    )
    browser.get(host+'OW/frmForcastDetail.aspx?ActionType=0&PreURL=frmForcast')

    start_date = browser.find_element_by_id('txtOWStartDate')
    start_date.clear()
    start_date.send_keys(job_dict.get('date', 'null'))
    start_minute = browser.find_element_by_id('txtOWStartTime')
    start_minute.clear()
    start_minute.send_keys(job_dict.get('start_time', default_start_time))

    end_date = browser.find_element_by_id('txtOWEndDate')
    end_date.clear()
    end_date.send_keys(job_dict.get('date', 'null'))
    end_minute = browser.find_element_by_id('txtOWEndTime')
    end_minute.clear()
    end_minute.send_keys(job_dict.get('end_time', default_end_time))

    Select(browser.find_element_by_id('drpISCClass')).select_by_value(job_dict.get('continuous', default_continuous))

    reason_area = browser.find_element_by_id('txtReason')
    reason_area.clear()
    reason_area.send_keys(task_dict.get('reason', ''))

    browser.find_element_by_id('btnCalOWHours').send_keys(Keys.ENTER)

    try:
        cal_alert = browser.switch_to.alert
    except Exception as e:
        tb_list = browser.find_elements_by_css_selector('#TBar table table')
        submit = tb_list[1].find_elements_by_tag_name('td')[1]
        submit.click()
        try:
            submit_alert = browser.switch_to.alert
        except Exception as e:
            print('系统错误')
        else:
            submit_alert.accept()
            print('作業成功')
    else:
        print('错误:{}'.format(cal_alert.text))
        cal_alert.accept()

# 开始获取加班预报资料了
# print('开始获取本月加班预报资料...', end='')
# browser.get(host+'OW/frmOWSearch.aspx')
# # first_date = datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
# first_date = datetime.date(2019,6,1)
# last_date_add_one = first_date.replace(month=first_date.month+1)
# last_date = last_date_add_one - datetime.timedelta(days=1)
#
# Select(browser.find_element_by_id('drp_SignStatus')).select_by_value("2")  # 选择签核状态“已通过”的
#
# start_day = browser.find_element_by_id('txtDates')
# start_day.clear()
# start_day.send_keys(first_date.strftime('%Y/%m/%d'))
#
# end_day = browser.find_element_by_id('txtDatee')
# end_day.clear()
# end_day.send_keys(last_date.strftime('%Y/%m/%d'))
#
# Select(browser.find_element_by_id('drp_OWType')).select_by_value("1")  # 选择查看类型为“预报”
#
# browser.find_element_by_id('btn_Search').click()  # 点击查询\
#
# try:
#     result_tr_list = browser.find_elements_by_css_selector('#DG_Result tr')
# except Exception as e:
#     print('本月还没有预报资料!')
# else:
#     tr_list_length = len(result_tr_list)
#     for i, tr in enumerate(result_tr_list):
#         dict_temp = {}
#         if i == 0 or i == tr_list_length-1:
#             continue
#         td_list = tr.find_elements_by_tag_name('td')
#         for index, td in enumerate(td_list):
#             if index == 7:
#                 start_str = td.text
#                 start = datetime.datetime.strptime(start_str, '%Y/%m/%d %H:%M')
#             if index == 8:
#                 end_str = td.text
#                 end = datetime.datetime.strptime(end_str, '%Y/%m/%d %H:%M')
#         else:
#             dict_temp['have_predict'] = 'True'
#             dict_temp['date'] = start.strftime('%Y/%m/%d')
#             dict_temp['start_time'] = (start.replace(hour=8) if start == end else start).strftime('%H:%M')
#             dict_temp['end_time'] = (end.replace(hour=17) if start == end else end).strftime('%H:%M')
#             dict_temp['continuous'] = 'N'
#             task_dict.setdefault('practical_job', []).append(dict_temp)
#     print('完成!')

# 开始实报加班
for job_dict in task_dict.get('practical_job', []):
    print('开始{}实报{} {}~{}的加班...'.format(
        '加班' if job_dict.get('have_predict', 'False') == 'True' else '直接',
        job_dict.get('date', 'null'),
        job_dict.get('start_time', default_start_time),
        job_dict.get('end_time', default_end_time)
        ),
        end=''
    )
    if job_dict.get('have_predict', 'False') == 'True':
        browser.get(host+'Overtime/frmapply.aspx')

        s = Select(browser.find_element_by_id('ddlPredictDate'))
        index = [i for i, opt in enumerate(s.options) if opt != '' and opt.text.split(' ')[0] == job_dict.get('date')]
        if index:
            s.select_by_index(index[0])
            Select(browser.find_element_by_id('ddlSuper')).select_by_value(job_dict.get('continuous', default_continuous))

            Select(browser.find_element_by_id('drp_OvertimeStartHour')).select_by_value(job_dict.get('start_time', default_start_time).split(':')[0])
            minute_start = browser.find_element_by_id('txt_OvertimeStartMin')
            minute_start.clear()
            minute_start.send_keys(job_dict.get('start_time', default_start_time).split(':')[1])

            Select(browser.find_element_by_id('drp_OvertimeEndHour')).select_by_value(
                job_dict.get('end_time', default_start_time).split(':')[0])
            minute_start = browser.find_element_by_id('txt_OvertimeEndMin')
            minute_start.clear()
            minute_start.send_keys(job_dict.get('end_time', default_start_time).split(':')[1])

            browser.find_element_by_id('btnCalc').click()

            try:
                cal_alert = browser.switch_to.alert
            except Exception as e:
                tb_list = browser.find_elements_by_css_selector('#TBar table table')
                tb_list[1].find_elements_by_tag_name('td')[1].click()
                try:
                    result_alert = browser.switch_to.alert
                except Exception:
                    print('系统错误!')
                else:
                    print(result_alert.text)
                    result_alert.accept()
            else:
                print('错误:{}'.format(cal_alert.text))
                cal_alert.accept()
        else:
            print('錯誤:未找到該日的預報資料,請修改have_predict=False來嘗試直接實報')
    else:
        browser.get(host+'Overtime/frmapply.aspx?ottype=nopredict')

        Select(browser.find_element_by_id('ddlSuper')).select_by_value(job_dict.get('continuous', default_continuous))

        browser.find_element_by_id('txt_OvertimeStartDate').send_keys(job_dict.get('date', 'null'))
        hour_start = Select(browser.find_element_by_id('drp_OvertimeStartHour'))
        hour_start.select_by_value(job_dict.get('start_time', default_start_time).split(':')[0])
        minute_start = browser.find_element_by_id('txt_OvertimeStartMin')
        minute_start.clear()
        minute_start.send_keys(job_dict.get('start_time', default_start_time).split(':')[1])

        browser.find_element_by_id('txt_OvertimeEndDate').send_keys(job_dict.get('date', 'null'))
        hour_end = Select(browser.find_element_by_id('drp_OvertimeEndHour'))
        hour_end.select_by_value(job_dict.get('end_time', default_end_time).split(':')[0])
        minute_end = browser.find_element_by_id('txt_OvertimeEndMin')
        minute_end.clear()
        minute_end.send_keys(job_dict.get('end_time', default_end_time).split(':')[1])

        reason = browser.find_element_by_id('txtReason')
        reason.send_keys(task_dict.get('reason', ''))

        browser.find_element_by_id('btnCalc').click()

        try:
            cal_alert = browser.switch_to.alert
        except Exception as e:
            tb_list = browser.find_elements_by_css_selector('#TBar table')
            tb_list[2].find_elements_by_tag_name('td')[1].click()

            try:
                result_alert = browser.switch_to.alert
            except Exception:
                print('系统错误!')
            else:
                print(result_alert.text)
                result_alert.accept()
        else:
            print('错误:{}'.format(cal_alert.text))
            cal_alert.accept()
browser.close()
print('Complete,good bye!')
