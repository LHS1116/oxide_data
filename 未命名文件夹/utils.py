import csv
import hashlib
import os
import random
import threading
from typing import Dict

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'oxide_data.settings'
django.setup()

from oxide_data.models import *
from oxide_data.api import *

vaccions = {}


def sha_256(text):
    sha = hashlib.sha256()
    sha.update(text)
    res = sha.hexdigest()
    return res


def get_timestamp(dt: datetime = None, ms=True):
    if dt is not None:
        ts = int(round(dt.timestamp()))
        return ts * 1000 if ms else ts
    ts = int(round(time.time(), 3))
    return ts * 1000 if ms else ts


def str2timestamp(time_str: str) -> int:
    format_str = "%Y-%m-%d %H:%M:%S"
    # "2021-01-04 05:22:02"
    _time = datetime.strptime(time_str, format_str)
    return int(round(_time.timestamp(), 3))


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


def is_municipality(province_name_cn):
    return len(province_cities.get(province_name_cn, [])) <= 1


def init_vaccions():
    data = json.load(open('./vaccinations.json', 'r'))
    tmp = {}
    for dt in data:
        tmp[dt['country']] = dt['data']
    # print(tmp.keys())
    # cts = tmp.keys()
    # print(tmp.get('United States'))
    # for k in tmp.keys():
    #     if country_dict_en.get(k) is None:
    #         print(k)
    for country_name_en in country_dict_en:

        country_name_cn = country_dict_en.get(country_name_en)
        vc_country = {}
        histories = tmp.get(country_name_en)

        if histories is not None:
            cnt = len(histories)
            total = 0
            for i in range(cnt):
                history = histories[i]
                _date = history['date']
                try:
                    if i == 0:
                        # total = history['daily_vaccinations']
                        total = history.get('daily_vaccinations', 0)
                    else:
                        # total += history['daily_vaccinations']
                        total += history.get('daily_vaccinations', 0)
                except Exception as e:

                    print(country_name_cn)
                    print(history)
                    raise e
                vc_country[_date] = total
        # if country_name_cn == '美国':
        #     print("mg")
        #     print(histories)
            vaccions[country_name_cn] = vc_country


"""csv处理相关"""


def csv2list(file_name: str) -> List[dict]:
    csv_reader = csv.reader(open(file_name, encoding='UTF-8-sig'))
    column_flag = False
    column_name = []
    res = []
    for row in csv_reader:
        if not column_flag:
            column_name = row
            column_flag = True
        else:
            row = list(map(lambda t: t if t != "" else None, row))
            res.append(dict(zip(column_name, row)))
    return res


def sync_world_record(timestamp: int, instance: dict):
    world_info = world_dict.get(timestamp, {})
    world_info['id'] = f"record_世界_{timestamp}"
    world_info['areaId'] = '世界'
    world_info['time'] = timestamp
    # world_info_dict = world_info.__dict__
    keys = ['total_cases', 'new_cases', 'new_cured', 'new_deaths', 'present_cases', 'severe_cases', 'suspected_cases',
            'total_cases', 'total_cured', 'total_deaths', 'total_vaccines']
    for key in keys:
        value = instance.get(key)
        if world_info.get(key) is None:
            world_info[key] = value
        else:
            if value != -1:
                world_info[key] += value
    world_dict[timestamp] = world_info


def dict2record_i18n(area_daily_dict: Dict):
    # for
    # province_name_en = area_daily_dict.get("Province_State", area_daily_dict.get("Province/State"))

    # country_name_en = area_daily_dict.get("Country_Region", area_daily_dict.get("Country/Region"))
    country_name_en = area_daily_dict.get("location")
    continent = area_daily_dict.get("continent")
    if continent is None:
        return None
    instance = Record()
    country_name_cn = country_dict_en.get(country_name_en)
    if country_name_cn is None:
        country_name_cn = country_name_en
    # if country_name_cn == "中国":
    #     return None
    cur_date = area_daily_dict.get("date")
    instance.areaId = country_name_cn

    flag = int(random.random() * 1000)
    instance.time = int(round(datetime.strptime(cur_date, "%Y-%m-%d").timestamp()))
    instance.id = f"record_{country_name_cn}_{instance.time}"
    new_cases = area_daily_dict.get("new_cases")
    new_cases = -1 if new_cases is None else int(float(new_cases))
    instance.new_cases = new_cases

    total_cases = area_daily_dict.get("total_cases")
    total_cases = -1 if total_cases is None else int(float(total_cases))
    instance.total_cases = total_cases

    # present_cases =

    new_deaths = area_daily_dict.get("new_deaths")
    new_deaths = -1 if new_deaths is None else int(float(new_deaths))
    instance.new_deaths = new_deaths

    total_deaths = area_daily_dict.get("total_deaths")
    total_deaths = -1 if total_deaths is None else int(float(total_deaths))
    instance.total_deaths = total_deaths

    total_vaccines = area_daily_dict.get("total_vaccinations")
    total_vaccines = -1 if total_vaccines is None else int(float(total_vaccines))
    instance.total_vaccines = total_vaccines

    severe_cases = area_daily_dict.get("icu_patients")
    severe_cases = -1 if severe_cases is None else int(float(severe_cases))
    instance.severe_cases = severe_cases

    instance.suspected_cases = -1
    instance.new_cured = -1
    instance.total_cured = -1
    instance.present_cases = instance.total_cases - instance.total_deaths
    sync_world_record(instance.time, instance.__dict__)
    return instance.__dict__


def dict2record_cn(area_daily_dict: Dict):
    # for
    # province_name_en = area_daily_dict.get("Province_State", area_daily_dict.get("Province/State"))

    # country_name_en = area_daily_dict.get("Country_Region", area_daily_dict.get("Country/Region"))
    # country_name_en = area_daily_dict.get("location")
    # continent = area_daily_dict.get("continent")
    # if continent is None:
    #     return None
    instance = Record()
    country_name_cn = "中国"
    province_name_cn = area_daily_dict.get("provinceName")
    cur_date = area_daily_dict.get("updateTime")
    instance.areaId = province_name_cn
    # flag = int(random.random() * 1000)

    instance.time = int(round(datetime.strptime(cur_date, "%Y/%m/%d %H:%M").replace(hour=0, minute=0).timestamp()))
    instance.id = f"record_{province_name_cn}_{instance.time}"

    instance.new_cases = -1

    total_cases = area_daily_dict.get("province_confirmedCount")
    total_cases = -1 if total_cases is None else int(float(total_cases))
    instance.total_cases = total_cases

    suspect_cases = area_daily_dict.get("province_suspectedCount")
    suspect_cases = -1 if suspect_cases is None else int(float(suspect_cases))
    instance.suspected_cases = suspect_cases

    instance.new_deaths = -1

    total_deaths = area_daily_dict.get("province_deadCount")
    total_deaths = -1 if total_deaths is None else int(float(total_deaths))
    instance.total_deaths = total_deaths

    instance.total_vaccines = -1
    #
    # severe_cases = area_daily_dict.get("icu_patients")
    # severe_cases = -1 if severe_cases is None else int(float(severe_cases))
    instance.severe_cases = -1

    # instance.suspected_cases = -1
    instance.new_cured = -1

    total_cured = area_daily_dict.get("province_curedCount")
    total_cured = -1 if total_cured is None else int(float(total_cured))

    instance.total_cured = total_cured
    instance.present_cases = instance.total_cases - instance.total_deaths

    return instance.__dict__


def dict2risky_area(area_daily_dict: Dict):
    instance = RiskyArea()
    instance.areaId = area_daily_dict.get('area')
    instance.description = area_daily_dict.get('description')
    instance.riskyAreaId = f"risk_area_{get_timestamp(ms=False)}"
    instance.risk = area_daily_dict.get('level')
    return instance


def insert_instance_list(s, resource_name, instances):
    js = instances
    if not isinstance(instances[0], dict):
        js = list(map(lambda x: x.__dict__, instances))
    resp = s.put(backend_host + f'/api/{resource_name}', json=js)
    return resp


def insert_instance(s, resource_name, instance, method='post'):
    js = instance
    if not isinstance(instance, dict):
        js = js.__dict__
    if method == 'post':
        resp = s.post(backend_host + f'/api/{resource_name}', json=js)
    else:
        resp = s.put(backend_host + f'/api/{resource_name}', json=js)

    return resp


"""调用后端接口录入数据"""


def init_country():
    countries = []
    for country_name_cn in country_dict_cn.keys():
        country_name_en = country_dict_cn.get(country_name_cn)[0]
        instance = Area()
        instance.id = country_name_cn
        instance.level = 1
        instance.is_china = True if country_name_cn == "中国" else False
        instance.china = instance.is_china
        instance.parentId = '世界'
        countries.append(instance)
    return countries


def init_province():
    provinces = []
    for province_name_cn in province_dict_cn.keys():
        province_name_en = province_dict_cn.get(province_name_cn)
        instance = Area()
        instance.id = province_name_cn
        instance.parentId = "中国"
        instance.level = 2
        instance.is_china = True
        instance.china = True
        provinces.append(instance)
    return provinces


def init_city():
    cities = []
    for province_name in province_cities.keys():
        _cities = province_cities.get(province_name)
        if len(cities) > 1:
            for city in _cities:
                instance = Area()
                instance.id = city
                instance.parentId = province_name
                instance.level = 3
                instance.is_china = True
                instance.china = True
                cities.append(instance)
    return cities


def init_area():
    res = []
    world = Area()
    world.parentId = None
    world.id = "世界"
    world.level = 0
    world.is_china = False
    res.append(world)
    res.extend(init_country())
    res.extend(init_province())
    res.extend(init_city())
    return res


def insert_task(area_daily_list, s):
    instances = list(map(lambda x: dict2record_i18n(x), area_daily_list))
    resp = insert_instance_list(s, 'records', instances)
    print(f'-status: {resp.status_code}-content：{resp.content}')


def init_record_i18n(s):
    area_daily_list = csv2list("/Users/bytedance/Downloads/调研数据/owid/owid-covid-data.csv")
    instances = []
    flag = 0
    cnt = 5000
    # threads = []
    # for i in range(0, len(area_daily_list), cnt):
    #     task_list = area_daily_list[i:i + cnt]
    #     threads.append(threading.Thread(target=insert_task, args=[task_list, s]))
    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()

    # return list(filter(lambda x: x is not None, map(lambda x: dict2record_i18n(x), area_daily_list)))

    for area_daily_dict in area_daily_list:
        if len(instances) >= 5000:
            # js = list(map(lambda x: x.__dict__, instances))
            js = instances
            resp = insert_instance_list(s, 'records', js)
            flag += 1
            print(f'flag: {flag}-status: {resp.status_code}-content：{resp.content}')
            if resp.status_code != 200:
                print(js)
                return
            instances.clear()
        instance = dict2record_i18n(area_daily_dict)
        if instance is not None:
            # print(instance)
            # instance.time /= 1000
            # print(instance.time)
            instances.append(instance)
    if len(instances) > 0:
        # js = list(map(lambda x: x.__dict__, instances))
        js = instances
        resp = insert_instance_list(s, 'records', js)
        flag += 1
        print(f'flag: {flag}-{resp.status_code}-{resp.text}')
        instances.clear()


def get_record_cn():
    area_daily_list = csv2list("/Users/bytedance/Downloads/调研数据/dxy/DXYArea1.csv")
    return list(filter(lambda x: x is not None, map(lambda x: dict2record_cn(x), area_daily_list)))


def init_record_from_json(s):
    path = '../data/records_2021-07-06.json'
    cnt = 5000
    flag = 0
    with open(path, 'r') as f:
        data = json.load(f)
        for i in range(0, len(data), cnt):
            js = data[i:i + cnt]
            resp = insert_instance_list(s, 'records', js)
            flag += 1
            print(f'flag: {flag}-status: {resp.status_code}-content：{resp.content}')


def get_record_i18n():
    area_daily_list = csv2list("/Users/bytedance/Downloads/调研数据/owid/owid-covid-data.csv")
    return list(filter(lambda x: x is not None, map(lambda x: dict2record_i18n(x), area_daily_list)))


def init_record_cn(s):
    area_daily_list = csv2list("/Users/bytedance/Downloads/调研数据/dxy/DXYArea1.csv")
    # return list(filter(lambda x: x is not None, map(lambda x: dict2record_cn(x), area_daily_list)))

    instances = []
    flag = 0
    for area_daily_dict in area_daily_list:
        if len(instances) >= 5000:
            # js = list(map(lambda x: x.__dict__, instances))
            js = instances
            resp = s.put(backend_host + '/api/records', json=js)
            flag += 1
            # print(js)
            print(f'flag: {flag}-status: {resp.status_code}-content：{resp.content}')
            if resp.status_code != 200:
                print(js)
                return
            instances.clear()
        instance = dict2record_cn(area_daily_dict)
        if instance is not None:
            # pass
            # print(instance)
            # instance.time /= 1000
            instances.append(instance)
    if len(instances) > 0:
        # js = list(map(lambda x: x.__dict__, instances))
        js = instances
        resp = s.put(backend_host + '/api/records', json=js)
        flag += 1
        print(f'flag: {flag}-{resp.status_code}-{resp.text}')
        instances.clear()


def format_json():
    json_path = 'world.json'
    cnt = 5000
    with open(json_path, 'r') as f:
        data = json.load(f)
        features = data["features"]
        # print(features[0].get("properties"))
        count = 0
        for feature in features:
            properties = feature.get("properties")
            if properties is not None:
                count += 1
                country_name_en = properties.get('name')
                if country_name_en is not None:
                    country_name_cn = country_dict_en.get(country_name_en)
                    if country_name_cn is None:
                        print(country_name_en)
                    else:
                        properties['name'] = country_name_cn

        print(count)
        with open('world1.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False)
        # json.dump()
        # print(len(features))
        # print(data.keys())
    # print(dt)


def save_json(save_path, data):
    assert save_path.split('.')[-1] == 'json'
    with open(save_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False)


def save_insatnces(instances: list, name):
    dt = datetime.now().date()
    file_name = f'../data/{name}_{dt}.json'
    save_json(file_name, instances)


def insert_area(s):
    area_list = init_area()
    areas = list(map(lambda x: x.__dict__, area_list))
    resp = s.put(backend_host + '/api/areas', json=areas)
    print(f'{resp.status_code}-{resp.text}-{resp.content}')


# def insert_news(s):


def get_areas(s):
    resp = s.get(backend_host + '/api/areas')
    print(resp.content)


def get_records(s, area_id="", cur_date=datetime.now()):
    area_id = '澳大利亚'

    begin_time = get_timestamp(datetime(year=2021, day=1, month=4))
    end_time = get_timestamp(datetime.now())
    url = backend_host + f"""/api/records?areaId="{area_id}"&beginTime={begin_time}&endTime={end_time}"""
    print(url)
    resp = s.get(url)
    print(resp.content)


"""合并国内数据源"""


def fix_insert_multi(s):
    bd1 = datetime.strptime('2020-01-22', "%Y-%m-%d")
    ed1 = datetime.strptime('2020-04-22', "%Y-%m-%d")

    bd2 = datetime.strptime('2020-04-23', "%Y-%m-%d")
    ed2 = datetime.strptime('2020-07-23', "%Y-%m-%d")

    bd3 = datetime.strptime('2020-04-24', "%Y-%m-%d")
    ed3 = datetime.strptime('2020-07-24', "%Y-%m-%d")

    bd4 = datetime.strptime('2020-07-25', "%Y-%m-%d")
    ed4 = datetime.strptime('2020-11-25', "%Y-%m-%d")

    bd5 = datetime.strptime('2020-11-26', "%Y-%m-%d")
    ed5 = datetime.strptime('2021-01-23', "%Y-%m-%d")

    bd6 = datetime.strptime('2021-01-24', "%Y-%m-%d")
    ed6 = datetime.strptime('2021-04-24', "%Y-%m-%d")

    bd7 = datetime.strptime('2021-04-25', "%Y-%m-%d")
    ed7 = datetime.strptime('2021-06-30', "%Y-%m-%d")

    threads = []
    threads.append(threading.Thread(target=fix_insert, args=[s, bd1, ed1]))
    threads.append(threading.Thread(target=fix_insert, args=[s, bd2, ed2]))
    threads.append(threading.Thread(target=fix_insert, args=[s, bd3, ed3]))
    threads.append(threading.Thread(target=fix_insert, args=[s, bd4, ed4]))
    threads.append(threading.Thread(target=fix_insert, args=[s, bd5, ed5]))
    threads.append(threading.Thread(target=fix_insert, args=[s, bd6, ed6]))
    threads.append(threading.Thread(target=fix_insert, args=[s, bd7, ed7]))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def fix_insert(s, begin_date, end_date):
    # cur_date = datetime.strptime('2020-01-22', "%Y-%m-%d")
    cur_date = begin_date
    fun = lambda x: -1 if x == "" or x is None else int(float(x))
    while cur_date <= end_date:
        print(cur_date)
        timestamp = get_timestamp(cur_date)
        tmp_list = []
        path = f"/Users/bytedance/Downloads/调研数据/csse_jhu/csse_covid_19_daily_reports/{str(cur_date.month).zfill(2)}-{str(cur_date.day).zfill(2)}-{str(cur_date.year).zfill(2)}.csv"
        area_daily_list = csv2list(path)
        area_daily_list = filter(
            lambda x: x.get('Country_Region', x.get('Country/Region')) in ['China', 'Mainland China'], area_daily_list)
        for area_daily_dict in area_daily_list:
            try:
                province_name_en = area_daily_dict.get('Province_State', area_daily_dict.get('Province/State'))
                if province_name_en is not None:
                    assert isinstance(province_name_en, str)
                    province_name_en = province_name_en.strip()
                    province_name_cn = province_dict_en.get(province_name_en)
                    if province_name_cn is None:
                        print(f'pne-{province_name_en}')
                    else:
                        rc_id_in_db = f'record_{province_name_cn}_{timestamp}'
                        rc_in_db = get_record_by_id_and_time(s, rc_id_in_db)
                        rec = Record()
                        if len(rc_in_db) == 0:
                            rec.id = f'record_{province_name_cn}_{timestamp}'
                            rec.time = timestamp
                            # print(area_daily_dict)
                            rec.total_cases = fun(area_daily_dict.get('Confirmed', ""))
                            rec.total_deaths = fun(area_daily_dict.get('Deaths', ""))
                            rec.total_cured = fun(area_daily_dict.get('Recovered', ""))
                            rec.total_vaccines = -1
                            rec.new_cases = -1
                            rec.new_deaths = -1
                            rec.new_cured = -1
                            rec.areaId = province_name_cn
                            rec.suspected_cases = -1
                            rec.present_cases = rec.total_cases - rec.total_deaths - rec.total_cured
                            rec.severe_cases = -1
                            tmp_list.append(rec.__dict__)
            except Exception as e:
                print(area_daily_dict)
                raise e

        cur_date += timedelta(days=1)
        if len(tmp_list) != 0:
            print(f"ins{len(tmp_list)}")
            resp = insert_instance_list(s, 'records', tmp_list)
            if resp.status_code != 200:
                print(tmp_list)
                return

                # print(type(rc_in_db))
                # rec =
                # rec.time = timestamp
                # rec.

    # cnt = 5000 * 21
    # flag = 0
    # with open(path, 'r') as f:
    #     data = json.load(f)
    #     js = data[cnt:]
    #     for j in js:

    #     resp = insert_instance_list(s, 'records', js)
    #     flag += 1
    #     print(f'flag: {flag}-status: {resp.status_code}-content：{resp.content}')


def get_fix_record(begin_date, end_date, record_dict):
    cur_date = begin_date
    fun = lambda x: -1 if x == "" or x is None else int(float(x))
    res = []
    while cur_date <= end_date:
        print(cur_date)
        timestamp = get_timestamp(cur_date)
        tmp_list = []
        path = f"/Users/bytedance/Downloads/调研数据/csse_jhu/csse_covid_19_daily_reports/{str(cur_date.month).zfill(2)}-{str(cur_date.day).zfill(2)}-{str(cur_date.year).zfill(2)}.csv"
        area_daily_list = csv2list(path)
        area_daily_list = filter(
            lambda x: x.get('Country_Region', x.get('Country/Region')) in ['China', 'Mainland China'], area_daily_list)
        for area_daily_dict in area_daily_list:
            try:
                province_name_en = area_daily_dict.get('Province_State', area_daily_dict.get('Province/State'))
                if province_name_en is not None:
                    assert isinstance(province_name_en, str)
                    province_name_en = province_name_en.strip()
                    province_name_cn = province_dict_en.get(province_name_en)
                    if province_name_cn is None:
                        print(f'pne-{province_name_en}-')
                    else:
                        rid = f'record_{province_name_cn}_{timestamp}'
                        rc_in_db = record_dict.get(rid)
                        rec = Record()
                        if rc_in_db is None:
                            rec.id = rid
                            rec.time = timestamp
                            # print(area_daily_dict)
                            rec.total_cases = fun(area_daily_dict.get('Confirmed', ""))
                            rec.total_deaths = fun(area_daily_dict.get('Deaths', ""))
                            rec.total_cured = fun(area_daily_dict.get('Recovered', ""))
                            rec.total_vaccines = -1
                            rec.new_cases = -1
                            rec.new_deaths = -1
                            rec.new_cured = -1
                            rec.areaId = province_name_cn
                            rec.suspected_cases = -1
                            rec.present_cases = rec.total_cases - rec.total_deaths - rec.total_cured
                            rec.severe_cases = -1
                            tmp_list.append(rec.__dict__)
            except Exception as e:
                print(area_daily_dict)
                raise e

        cur_date += timedelta(days=1)
        if len(tmp_list) != 0:
            print(f"ins{len(tmp_list)}")
            res.extend(tmp_list)
    return res


def insert_rumors():
    rumors = get_isaa_rumors()['results']
    s = get_session()
    res = []
    for rumor in rumors:
        rum = Tip()
        rum.content = rumor['body']
        rum.title = f"{rumor['title']}"
        rum.type = '辟谣'
        # rum.senderId = "1"
        # res.append(rum.__dict__)
        # save_json('../data/rumors_2021-07-09.json', res)
        resp = insert_instance(s, 'tips', rum.__dict__)
        if resp.status_code != 200:
            print(rum.__dict__)
            print(f'{resp.status_code}-{resp.text}-{resp.content}')
        # print('ok')
        # res.append(rum.__dict__)
    # print(res)


def tmp_tips():
    # url = 'https://h5.baike.qq.com/mobile/tag_article.html?name=%E4%B8%93%E9%A2%98&tagId=94686&src=cancer_straight&adtag=wxjk.op.dkyq.rmkp&VNK=b908ce87&tag=%E7%83%AD%E7%82%B9%E7%A7%91%E6%99%AE'
    # r =requests.get(url)
    # bsobj =url2bsobj(url)
    # # bsobj = BeautifulSoup(r, 'html.praser')
    # print(bsobj.find_all('div', attrs={'class', 'content-detail'}))
    # # print(r.text)
    tip_list = []
    for t in tips:
        tip = Tip()
        tip.title = t['title']
        tip.type = '常识'
        tip.content = t['content']
        tip.id = f"tip_{sha_256(tip.title.encode())}"
        tip_list.append(tip.__dict__)
    s = get_session()
    r = insert_instance_list(s, 'tips', tip_list)
    print(r.status_code)

    # print(tip_list)
def insert_tips():
    s = get_session()
    tips_list = []
    for i in range(3):
        if i == 0:
            url = "http://www.nhc.gov.cn/xcs/kpzs/list_gzbdfkzs.shtml"
        else:
            url = f"http://www.nhc.gov.cn/xcs/kpzs/list_gzbdfkzs_{i + 1}.shtml"

        bsobj = url2bsobj(url)
        lines = bsobj.find_all('li')
        print(lines)
        for line in lines:
            link = nhc_host + line.a['href']
            title = line.a.text
            # time = get_timestamp(datetime.strptime(line.span.text, "%Y-%m-%d"))
            tip = Tip()
            tip.title = title
            tip.type = '常识'
            tip.content = link
            tip.id = f"tip_{sha_256(link.encode())}"
            tips_list.append(tip.__dict__)
    resp = insert_instance_list(s, 'tips', tips_list)
    if resp.status_code == 200:
        print(f"[{datetime.now()}] update tips Done")
    else:
        print(f"[{datetime.now()}] update tips Failed -- {resp.status_code}")
    print(tips_list)


"""数据保存"""


def save_areas():
    area_list = init_area()
    areas = list(map(lambda x: x.__dict__, area_list))
    save_insatnces(areas, 'areas')


def save_records(s):
    instance = []
    cn_record = get_record_cn()
    i18n_record = get_record_i18n()
    cn_map = dict(zip(map(lambda x: x.id, cn_record), cn_record))
    fix_record = get_fix_record()

    wkl = world_dict.keys()
    wl = list(map(lambda x: world_dict.get(x), wkl))
    # print(wl)
    print(len(wl))
    # resp = insert_instance_list(s, 'records', wl)
    instance.extend(cn_record)
    instance.extend(i18n_record)
    instance.extend(wl)
    save_insatnces(instance, 'records')


def insert(s):
    insert_area(s)
    # get_areas(s)
    t1 = threading.Thread(target=init_record_cn, args=[s])
    t2 = threading.Thread(target=init_record_i18n, args=[s])
    # t1 = threading.Thread(target=init_record_from_json, args=[s])
    # t2 = threading.Thread(target=init_area, args=[s])
    t1.start()
    # t2.start()
    # init_record_i18n(s)
    t1.join()
    # t2.join()
    wkl = world_dict.keys()
    wl = list(map(lambda x: world_dict.get(x), wkl))
    print(wl)
    insert_instance_list(s, 'records', wl)

    # init_record_cn(s)
    # get_records(s)



if __name__ == '__main__':
    # init_vaccions()/
    # print(vaccions['美国'])
    # insert_oversea_history()
    # get_cn_history()
    # tmp_tips()
    # insert_rumors()
    save_json('../data/vaccination_rate.json', vacc_rate_dict)
