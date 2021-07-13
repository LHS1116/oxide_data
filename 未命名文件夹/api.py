# -*- coding: utf-8 -*-
import json
import os
import ssl
import time
from urllib import request
import urllib.request

import requests
from pyppeteer import launcher
import asyncio
from datetime import datetime, date, timedelta

from oxide_data.models import Record, News
from oxide_data.const import *

launcher.DEFAULT_ARGS.remove("--enable-automation")
from pyppeteer import launch
from bs4 import BeautifulSoup

nhc_host = "http://www.nhc.gov.cn"
isaa_host = "https://lab.isaaclin.cn"


def get_session():
    s = requests.session()
    payload = {
        "password": "ds1000001",
        "username": "ds1000"
    }
    resp = s.post("http://39.106.140.102:27031/api/access/login", json=payload)
    # print(resp.status_code)
    # me = s.get("http://39.106.140.102:27031/api/access/me")
    # print(me.text)
    return s


async def do_fetch_url(url) -> str:
    browser = await launch({'headless': False, 'dumpio': True, 'autoClose': True})
    page = await browser.newPage()
    # await page.waitForNavigation({'timeout': 1000 * 5})
    page.setDefaultNavigationTimeout(10000)
    await page.goto(url, {
        'timeout': 1000 * 10
    })
    await asyncio.wait([page.waitForNavigation()])
    data = await page.content()
    await browser.close()
    return data


def fetch_url(url):
    html = asyncio.get_event_loop().run_until_complete(do_fetch_url(url))
    return html


def url2bsobj(url):
    html = fetch_url(url)
    bsobj = BeautifulSoup(html, 'html.parser')
    return bsobj

def getTitleUrl(html):
    bsobj = BeautifulSoup(html, 'html.parser')
    titleList = bsobj.find('div', attrs={"class": "list"}).ul.find_all("li")
    for item in titleList:
        link = nhc_host + item.a["href"]
        title = item.a["title"]
        cur_date = item.span.text
        # if cur_date == '2021-06-28':
        #     yield title, link, cur_date
        yield title, link, cur_date


def getContent(html):
    bsobj = BeautifulSoup(html, 'html.parser')
    cnt = bsobj.find('div', attrs={"id": "xw_box"}).find_all("p")
    s = ""
    if cnt:
        for item in cnt:
            s += item.text
        return s


def get_vaccinated_count(cur_date=datetime.now().date().strftime("%Y-%m-%d")):
    vaccinated_path = "/xcs/yqjzqk/list_gzbd.shtml"
    vaccinated_url = nhc_host + vaccinated_path
    vaccinated_list_html = fetch_url(vaccinated_url)
    title_list = getTitleUrl(vaccinated_list_html)
    page_url = ""
    for title in title_list:
        print(title)

        if title[2] == cur_date:
            page_url = title[1]
            break
    if page_url != "":
        return int(float(fetch_url(page_url).split("接种新冠病毒疫苗")[1].split("万剂次")[0]) * 10000)
    return get_vaccinated_count((datetime.now() - timedelta(days=1)).date().strftime("%Y-%m-%d"))


def get_timestamp(dt: datetime = None):
    if dt is not None:
        return int(round(dt.timestamp()))
    return int(round(time.time(), 3))


def get_ali_data():
    host = 'https://ncovdata.market.alicloudapi.com'
    path = '/ncov/cityDiseaseInfoWithTrend'
    method = 'GET'
    appcode = '8edce7ec8635447b86e7c922b5efca6d'
    url = host + path

    req = urllib.request.Request(url)
    req.add_header('Authorization', 'APPCODE ' + appcode)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(req, context=ctx)
    content = response.read().decode("utf-8")
    if content:
        return content
    return None


def get_record_by_id_and_time(s, area, begin_time, end_time):
    print(area)
    url = backend_host + f'/api/records/?areaId={area}&beginTime={begin_time}&endTime={end_time}'
    resp = s.get(url)
    if resp.status_code == 200:
        print(resp.json())
        res = resp.json()
        if len(res) > 0:
            return res
    return {}


def get_ali_data_cn():
    s = get_session()
    content = get_ali_data()
    if content is None:
        return None
    content = json.loads(content)
    total_data_cn = content.get('country')
    trends = content.get('trend', [])
    yesterday = trends[-1]  # {'day': '7.06', 'sure_cnt': 119036, 'die_cnt': 5554, 'cure_cnt': 109729, 'doubt_cnt': 5, 'fullDay': 20210706}
    cur_date = total_data_cn.get('time').split()[0]
    print(cur_date)

    # total_vaccines = get_vaccinated_count(cur_date)
    total_vaccines = -1

    cur_date = datetime.strptime(cur_date, "%Y-%m-%d")
    yest_date = cur_date - timedelta(days=1)
    yest_timestamp = get_timestamp(yest_date)
    timestamp = get_timestamp(cur_date)
    print(yest_timestamp)
    print(datetime.fromtimestamp(yest_timestamp))

    cn_record = Record()
    total_cured = total_data_cn.get('totalCured', -1)
    total_death = total_data_cn.get('totalDeath', -1)
    total_cases = total_data_cn.get('totalConfirmed', -1)
    suspected_cases = total_data_cn.get('incDoubtful', -1)

    new_cases = total_cases - yesterday.get('sure_cnt')
    new_cured = total_cured - yesterday.get('cure_cnt')
    new_deaths = total_death - yesterday.get('die_cnt')

    cn_record.id = f"record_中国_{timestamp}"
    cn_record.areaId = '中国'
    cn_record.total_deaths = total_death
    cn_record.total_cured = total_cured
    cn_record.total_cases = total_cases
    cn_record.total_vaccines = total_vaccines
    cn_record.new_cured = new_cured
    cn_record.new_cases = new_cases
    cn_record.new_deaths = new_deaths
    cn_record.suspected_cases = suspected_cases
    cn_record.time = timestamp
    cn_record.severe_cases = 0
    cn_record.present_cases = total_cases - total_cured - total_death

    res = [cn_record.__dict__]
    province_list = content.get('provinceArray')
    for province in province_list:
        total_cured = province.get('totalCured', -1)
        total_death = province.get('totalDeath', -1)
        total_cases = province.get('totalConfirmed', -1)
        province_name_cn = province.get('childStatistic', "")
        if province_dict_cn.get(province_name_cn) is not None:
            pro = Record()
            # yest_id = f"record_{province_name_cn}_{yest_timestamp}"
            yest_rec_dict = get_record_by_id_and_time(s, province_name_cn, yest_timestamp, timestamp)
            pro.id = f"record_{province_name_cn}_{timestamp}"

            pro.areaId = province_name_cn
            pro.time = timestamp
            pro.total_cured = total_cured
            pro.total_deaths = total_death
            pro.total_cases = total_cases
            pro.total_vaccines = -1
            pro.present_cases = total_cases - total_cured - total_death
            pro.suspected_cases = -1
            pro.severe_cases = 0
            pro.new_deaths = total_death - yest_rec_dict.get('total_deaths', total_death)
            pro.new_cured = total_cured - yest_rec_dict.get('total_cured', total_cured)
            pro.new_cases = total_cases - yest_rec_dict.get('total_cases', total_cases)
            # pro_list.append(pro.__dict__)
            res.append(pro.__dict__)
    # return total_data_cn
    return res


def get_isaa_data():
    pass
def get_isaa_rumors():
    url = isaa_host + '/nCoV/api/rumors?rumorType=1&page=1&num=100'
    r = requests.get(url)
    print(r.json())
    # return r.json()

def get_isaa_news():
    url = isaa_host + '/nCoV/api/news?page=1&num=100'
    r = requests.get(url)
    print(r.json())
    return r.json()


def get_isaa_areas(area_name):
    url = isaa_host + f'/nCoV/api/area?latest=1&province={area_name}'
    r = requests.get(url)
    js = r.json()
    print(datetime.fromtimestamp(js['results'][0]['updateTime'] / 1000))
    print(r.json())


def get_tencent_area_data_i18n(country):
    url = 'https://wechat.wecity.qq.com/api/THPneumoniaOuterDataService/getForeignCountry'

    payload = {
        "args": {
            "req": {
                "country": f"{country}"
            }
        },
        "service": "THPneumoniaOuterDataService",
        "func": "getForeignCountry",
        "context": {
            "userId": "1f0beb43a1404d2591e1b9c23da2ce78"
        }
    }
    r = requests.post(url=url, json=payload)
    js = r.json()
    if js['msg'] == 'success':
        data = js['args']['rsp']
        history = data['countryHistory']
        today = data['countryInfo']
        return history, today
    return [], {}




def get_baidu_news():
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/'
    html = fetch_url(url)
    bsobj = BeautifulSoup(html, 'html.parser')
    print(bsobj.prettify())
    reports = bsobj.find_all('div', attrs={"class": "Virus_1-1-308_TB6x3k"})
    for report in reports:

        href = report.a['href']
        text = report.div.text
        print(href, text)
        # print(type(report))
    #     link = report.split()
    #     print()
    print(reports)


def tmp_post():
    pass
    # print(r.json())


# print(get_vaccinated_count(datetime(year=2021, month=7, day=6)))
# print(get_ali_data_cn())
# print(fetch_url("http://www.nhc.gov.cn/xcs/yqjzqk/list_gzbd.shtml"))
# print(get_vaccinated_count('2021-07-02'))
# get_isaa_news()
# get_isaa_rumors()
# get_isaa_areas('俄罗斯')
# tmp_post()
# get_baidu_news()

# get_gov_reports()