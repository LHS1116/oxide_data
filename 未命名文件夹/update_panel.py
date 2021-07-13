# -*- coding: utf-8 -*-

import json
import sys
import time
import traceback
from datetime import datetime

import requests
from bs4 import BeautifulSoup

backend_host = "http://39.106.140.102:27031"

simple_province_name = [
    '安徽',
    '北京',
    '福建',
    '甘肃',
    '广东',
    '广西',
    '贵州',
    '海南',
    '河北',
    '河南',
    '黑龙江',
    '湖北',
    '湖南',
    '吉林',
    '江苏',
    '江西',
    '辽宁',
    '内蒙古',
    '宁夏',
    '青海',
    '山东',
    '山西',
    '陕西',
    '上海',
    '四川',
    '天津',
    '西藏',
    '新疆',
    '云南',
    '浙江',
    '重庆',
    '香港',
    '澳门',
    '台湾',
]

complex_province_name = [
    '安徽省',
    '北京市',
    '福建省',
    '甘肃省',
    '广东省',
    '广西壮族自治区',
    '贵州省',
    '海南省',
    '河北省',
    '河南省',
    '黑龙江省',
    '湖北省',
    '湖南省',
    '吉林省',
    '江苏省',
    '江西省',
    '辽宁省',
    '内蒙古自治区',
    '宁夏回族自治区',
    '青海省',
    '山东省',
    '山西省',
    '陕西省',
    '上海市',
    '四川省',
    '天津市',
    '西藏自治区',
    '新疆维吾尔自治区',
    '云南省',
    '浙江省',
    '重庆市',
    '香港特别行政区',
    '澳门特别行政区',
    '台湾省'
]

province_name_dict = dict(zip(simple_province_name, complex_province_name))

class Panel(object):
    active: int
    activeDelta: int
    areaId: str
    cured: int
    curedDelta: int
    death: int
    deathDelta: int
    time: int
    totalCases: int
    totalCasesDelta: int
    vaccine: int
    vaccineDelta: int

    @staticmethod
    def from_resp(newly_data: dict):
        panel = Panel()
        panel.death = newly_data['died']
        panel.cured = newly_data['cured']
        panel.active = newly_data['curConfirm']
        panel.totalCases = newly_data['confirmed']

        panel.deathDelta = newly_data['diedRelative']
        panel.curedDelta = newly_data['curedRelative']
        panel.activeDelta = newly_data['curConfirmRelative']
        panel.totalCasesDelta = newly_data['confirmedRelative']
        return panel


def get_session():
    s = requests.session()
    payload = {
        "password": "ds1000001",
        "username": "ds1000"
    }
    s.post("http://39.106.140.102:27031/api/access/login", json=payload)

    return s


def get_timestamp(dt: datetime = None):
    if dt is not None:
        return int(round(dt.timestamp()))
    return int(round(time.time(), 3))



def get_vaccine_count():
    url = "https://cov19.cc/report.json"
    js = requests.get(url).json()
    data = js['regions']
    world_data = data['world']
    country_list = world_data['list']
    # print(country_list)
    # cn_data = data['china']
    cn_data = list(filter(lambda x: x['country'] == 'China', country_list))[0]
    return world_data['totals']['vaccinated'], cn_data['vaccinated']


def get_yesterday_panel(s, area_id):
    yesterday_timestamp = get_timestamp(datetime.now().replace(minute=0, hour=0, microsecond=0))
    url = f"{backend_host}/api/panel-records?areaId={area_id}&endTime={yesterday_timestamp}&limit=1"
    r = s.get(url).json()
    if len(r) == 0:
        return {}
    return r[0]



def save_json(save_path, data):
    assert save_path.split('.')[-1] == 'json'
    with open(save_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False)

def get_panel_cn_and_i18n(s, html):
    bsobj = BeautifulSoup(html, 'html.parser')
    # cnt = bsobj.find_all('script', attrs={"class": "VirusSummarySix_1-1-306_3wCKWi"})
    # print(bsobj.prettify())
    cnt = bsobj.find('script', attrs={"id": "captain-config"})
    cnt_str = cnt.string

    data_dict = json.loads(cnt_str)
    assert isinstance(data_dict, dict)
    data_dict = data_dict.get('component', [{}])[0]
    # print(data_dict['page'])
    # print(data_dict.keys())
    newly_data_cn = data_dict['summaryDataIn']
    newly_data_i18n = data_dict['summaryDataOut']
    # save_json('../data/panel_data_dict_2021-07-09.json', data_dict)
    # save_json('../data/panel_cn_2021-07-09.json', newly_data_cn)
    # save_json('../data/panel_i18n_2021-07-09.json', newly_data_i18n)
    cur_time = get_timestamp()

    vaccine_world, vaccine_cn = get_vaccine_count()
    panel_cn = Panel.from_resp(newly_data_cn)
    panel_cn.vaccine = vaccine_cn
    panel_cn.areaId = '中国'
    panel_cn.time = cur_time

    panel_i18n = Panel.from_resp(newly_data_i18n)
    panel_i18n.vaccine = vaccine_world
    panel_i18n.areaId = '世界'
    panel_i18n.time = cur_time

    ystd_vaccines_cn = get_yesterday_panel(s, '中国').get('vaccine', panel_cn.vaccine + 1)
    ystd_vaccines_i18n = get_yesterday_panel(s, '世界').get('vaccine', panel_i18n.vaccine + 1)

    panel_cn.vaccineDelta = panel_cn.vaccine - ystd_vaccines_cn
    panel_i18n.vaccineDelta = panel_i18n.vaccine - ystd_vaccines_i18n
    #
    return panel_cn, panel_i18n


def update_panel_data():
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/'
    # html = fetch_url(url)
    html = requests.get(url).text
    html = html.encode().decode('unicode_escape')
    s = get_session()
    # get_panel_cn_and_i18n(s, html)
    panel_cn, panel_i18n = get_panel_cn_and_i18n(s, html)
    r1 = insert_panel(s, panel_cn)
    r2 = insert_panel(s, panel_i18n)
    #
    print(f"[{datetime.now()}]update_panel r1:Status:{r1.status_code}, Data: {panel_cn.__dict__}\n "
          f"r2:Status:{r2.status_code}, Data: {panel_i18n.__dict__}")


def insert_panel(s, panel: Panel):
    url = backend_host + '/api/panel-records'
    payload = panel.__dict__
    r = s.post(url, json=payload)
    return r


def tmp_num():
    url = 'https://www.hongheiku.com/'
    r = requests.get(url)
    # print(r.text)
    bsobj = BeautifulSoup(r.text, 'html.parser')
    # print(bsobj.prettify())
    prs = bsobj.find_all('tr')
    # print(prs)
    res = {}
    for pr in prs:
        t = pr.text.split('\n')
        print(t)
        print(t[1], t[2])
        name = t[1]
        count = t[2]
        if province_name_dict.get(name) is not None:
            res[name] = count




if __name__ == '__main__':
    while True:
        try:
            update_panel_data()
            time.sleep(5 * 60)
        except Exception as e:
            trace_back = sys.exc_info()[2]
            traceback.print_tb(trace_back)
            # break
    # update_panel_data()

    # tmp_num()
