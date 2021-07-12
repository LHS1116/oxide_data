import hashlib
import json
import sys
import time
import traceback
from datetime import datetime

import requests
from pyppeteer import launcher
import asyncio

launcher.DEFAULT_ARGS.remove("--enable-automation")
from pyppeteer import launch
from bs4 import BeautifulSoup

backend_host = "http://39.106.140.102:27031"
isaa_host = "https://lab.isaaclin.cn"

province_cities = {'北京市': ['北京市'],
                   '天津市': ['天津市'],
                   '河北省': ['石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市', '张家口市', '承德市', '沧州市', '廊坊市', '衡水市'],
                   '山西省': ['太原市', '大同市', '阳泉市', '长治市', '晋城市', '朔州市', '晋中市', '运城市', '忻州市', '临汾市', '吕梁市'],
                   '内蒙古自治区': ['呼和浩特市', '包头市', '乌海市', '赤峰市', '通辽市', '鄂尔多斯市', '呼伦贝尔市', '巴彦淖尔市', '乌兰察布市', '兴安盟', '锡林郭勒盟',
                              '阿拉善盟'],
                   '辽宁省': ['沈阳市', '大连市', '鞍山市', '抚顺市', '本溪市', '丹东市', '锦州市', '营口市', '阜新市', '辽阳市', '盘锦市', '铁岭市', '朝阳市',
                           '葫芦岛市'], '吉林省': ['长春市', '吉林市', '四平市', '辽源市', '通化市', '白山市', '松原市', '白城市', '延边朝鲜族自治州'],
                   '黑龙江省': ['哈尔滨市', '齐齐哈尔市', '鸡西市', '鹤岗市', '双鸭山市', '大庆市', '伊春市', '佳木斯市', '七台河市', '牡丹江市', '黑河市', '绥化市',
                            '大兴安岭地区'],
                   '上海市': ['上海市'],
                   '江苏省': ['南京市', '无锡市', '徐州市', '常州市', '苏州市', '南通市', '连云港市', '淮安市', '盐城市', '扬州市', '镇江市', '泰州市', '宿迁市'],
                   '浙江省': ['杭州市', '宁波市', '温州市', '嘉兴市', '湖州市', '绍兴市', '金华市', '衢州市', '舟山市', '台州市', '丽水市'],
                   '安徽省': ['合肥市', '芜湖市', '蚌埠市', '淮南市', '马鞍山市', '淮北市', '铜陵市', '安庆市', '黄山市', '滁州市', '阜阳市', '宿州市', '六安市',
                           '亳州市', '池州市', '宣城市'],
                   '福建省': ['福州市', '厦门市', '莆田市', '三明市', '泉州市', '漳州市', '南平市', '龙岩市', '宁德市'],
                   '江西省': ['南昌市', '景德镇市', '萍乡市', '九江市', '新余市', '鹰潭市', '赣州市', '吉安市', '宜春市', '抚州市', '上饶市'],
                   '山东省': ['济南市', '青岛市', '淄博市', '枣庄市', '东营市', '烟台市', '潍坊市', '济宁市', '泰安市', '威海市', '日照市', '临沂市', '德州市',
                           '聊城市', '滨州市', '菏泽市'],
                   '河南省': ['郑州市', '开封市', '洛阳市', '平顶山市', '安阳市', '鹤壁市', '新乡市', '焦作市', '濮阳市', '许昌市', '漯河市', '三门峡市', '南阳市',
                           '商丘市', '信阳市', '周口市', '驻马店市'],
                   '湖北省': ['武汉市', '黄石市', '十堰市', '宜昌市', '襄阳市', '鄂州市', '荆门市', '孝感市', '荆州市', '黄冈市', '咸宁市', '随州市',
                           '恩施土家族苗族自治州'],
                   '湖南省': ['长沙市', '株洲市', '湘潭市', '衡阳市', '邵阳市', '岳阳市', '常德市', '张家界市', '益阳市', '郴州市', '永州市', '怀化市', '娄底市',
                           '湘西土家族苗族自治州'],
                   '广东省': ['广州市', '韶关市', '深圳市', '珠海市', '汕头市', '佛山市', '江门市', '湛江市', '茂名市', '肇庆市', '惠州市', '梅州市', '汕尾市',
                           '河源市', '阳江市', '清远市', '东莞市', '中山市', '潮州市', '揭阳市', '云浮市'],
                   '广西壮族自治区': ['南宁市', '柳州市', '桂林市', '梧州市', '北海市', '防城港市', '钦州市', '贵港市', '玉林市', '百色市', '贺州市', '河池市',
                               '来宾市', '崇左市'],
                   '海南省': ['海口市', '三亚市', '三沙市', '儋州市'],
                   '重庆市': ['重庆市'],
                   '四川省': ['成都市', '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市', '广元市', '遂宁市', '内江市', '乐山市', '南充市', '眉山市', '宜宾市',
                           '广安市', '达州市', '雅安市', '巴中市', '资阳市', '阿坝藏族羌族自治州', '甘孜藏族自治州', '凉山彝族自治州'],
                   '贵州省': ['贵阳市', '六盘水市', '遵义市', '安顺市', '毕节市', '铜仁市', '黔西南布依族苗族自治州', '黔东南苗族侗族自治州', '黔南布依族苗族自治州'],
                   '云南省': ['昆明市', '曲靖市', '玉溪市', '保山市', '昭通市', '丽江市', '普洱市', '临沧市', '楚雄彝族自治州', '红河哈尼族彝族自治州', '文山壮族苗族自治州',
                           '西双版纳傣族自治州', '大理白族自治州', '德宏傣族景颇族自治州', '怒江傈僳族自治州', '迪庆藏族自治州'],
                   '西藏自治区': ['拉萨市', '日喀则市', '昌都市', '林芝市', '山南市', '那曲市', '阿里地区'],
                   '陕西省': ['西安市', '铜川市', '宝鸡市', '咸阳市', '渭南市', '延安市', '汉中市', '榆林市', '安康市', '商洛市'],
                   '甘肃省': ['兰州市', '嘉峪关市', '金昌市', '白银市', '天水市', '武威市', '张掖市', '平凉市', '酒泉市', '庆阳市', '定西市', '陇南市',
                           '临夏回族自治州', '甘南藏族自治州'],
                   '青海省': ['西宁市', '海东市', '海北藏族自治州', '黄南藏族自治州', '海南藏族自治州', '果洛藏族自治州', '玉树藏族自治州', '海西蒙古族藏族自治州'],
                   '宁夏回族自治区': ['银川市', '石嘴山市', '吴忠市', '固原市', '中卫市'],
                   '新疆维吾尔自治区': ['乌鲁木齐市', '克拉玛依市', '吐鲁番市', '哈密市', '昌吉回族自治州', '博尔塔拉蒙古自治州', '巴音郭楞蒙古自治州', '阿克苏地区',
                                '克孜勒苏柯尔克孜自治州', '喀什地区', '和田地区', '伊犁哈萨克自治州', '塔城地区', '阿勒泰地区'],
                   '台湾省': ['台北市', '高雄市', '台南市', '台中市', '南投县', '基隆市', '新竹市', '嘉义市', '新北市', '宜兰县', '新竹县', '桃园市', '苗栗县',
                           '彰化县', '嘉义县', '云林县', '屏东县', '台东县', '花莲县', '澎湖县'],
                   '香港特别行政区': ['香港特别行政区'],
                   '澳门特别行政区': ['澳门特别行政区']}


class RiskyArea(object):
    riskyAreaId: str
    areaId: str  # 一般为市的id
    risk: str  # "low" | "mid" | "high";
    description: str  # e.g. 广东省 深圳市 宝安区 福永街道下十围商住街71号新蓝天公寓


class News(object):
    id: str
    title: str
    link: str
    time: int
    type: str  # enum "msg" | "gov"; # 可能不会用到这些type，取决于数据能否整理出


#


def sha_256(text):
    sha = hashlib.sha256()
    sha.update(text)
    res = sha.hexdigest()
    return res


def save_json(save_path, data):
    assert save_path.split('.')[-1] == 'json'
    with open(save_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False)


async def do_fetch_url(url) -> str:
    browser = await launch({'headless': False, 'dumpio': True, 'autoClose': True})
    page = await browser.newPage()
    page.setDefaultNavigationTimeout(15000)
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


def get_timestamp(dt: datetime = None):
    if dt is not None:
        return int(round(dt.timestamp()) * 1000)
    return int(round(time.time(), 3) * 1000)


def str2timestamp(time_str: str) -> int:
    format_str = "%Y-%m-%d %H:%M:%S"
    # "2021-01-04 05:22:02"
    _time = datetime.strptime(time_str, format_str)
    return int(round(_time.timestamp(), 3) * 1000)


def get_session():
    s = requests.session()
    payload = {
        "password": "ds1000001",
        "username": "ds1000"
    }
    s.post("http://39.106.140.102:27031/api/access/login", json=payload)
    return s


def is_municipality(province_name_cn):
    return len(province_cities.get(province_name_cn, [])) <= 1


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


def delete_instances(s, resource_name, instance=None):
    url = backend_host + f'/api/{resource_name}'
    # if instance is not None:
    #     url += f'/{instance.id}'
    resp = s.delete(url)
    return resp


def format_reports(_line):
    host = "http://www.nhc.gov.cn/"
    line = _line.a
    link = host + line['href']
    title = line.get('title')
    fun = lambda x: x.split('/')[-1].split('.')[0]
    if title is not None:
        gov_news_yqtb = News()
        gov_news_yqtb.time = get_timestamp(datetime.strptime(_line.span.text, "%Y-%m-%d"))
        gov_news_yqtb.id = 0
        gov_news_yqtb.title = title
        gov_news_yqtb.link = link
        gov_news_yqtb.type = 'gov'
        gov_news_yqtb.id = f"news_gov_{fun(link)}"
        return gov_news_yqtb.__dict__
    return None


def update_gov_reports(s):
    gov_news_list = []
    for i in range(3):
        if i > 0:
            yqtb_url = f"http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_{i + 1}.shtml"
            jzqk_url = f"http://www.nhc.gov.cn/xcs/yqjzqk/list_gzbd_{i + 1}.shtml"
        else:
            yqtb_url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
            jzqk_url = f"http://www.nhc.gov.cn/xcs/yqjzqk/list_gzbd.shtml"

        yqtb_html = fetch_url(yqtb_url)
        jzqk_html = fetch_url(jzqk_url)
        bsobj1 = BeautifulSoup(yqtb_html, 'html.parser')
        bsobj2 = BeautifulSoup(jzqk_html, 'html.parser')
        yqtb_lines = bsobj1.find_all('li')
        jzqk_lines = bsobj2.find_all('li')

        cnt = max(len(yqtb_lines), len(jzqk_lines))
        for i in range(cnt):
            if i < len(yqtb_lines):
                yqtb_line = yqtb_lines[i]
                tmp = format_reports(yqtb_line)
                if tmp is not None:
                    gov_news_list.append(tmp)
            if i < len(jzqk_lines):
                jzqk_line = jzqk_lines[i]
                tmp = format_reports(jzqk_line)
                if tmp is not None:
                    gov_news_list.append(tmp)

    resp = insert_instance_list(s, 'news', gov_news_list)
    if resp.status_code == 200:
        print(f"[{datetime.now()}] update gov news Done")
    else:
        print(f"[{datetime.now()}] update gov news Failed -- {resp.status_code}")
    save_json(f'../data/gov_news_{datetime.now().date()}.json', gov_news_list)
    return gov_news_list


def update_newly_risky_areas(s):
    risky_areas = []
    url = 'http://bmfw.www.gov.cn/yqfxdjcx/risk.html'
    html = fetch_url(url)
    bsobj = BeautifulSoup(html, 'html.parser')
    # print(bsobj.prettify())
    h_contents = bsobj.find_all('div', attrs={'class': 'h-header'})
    for h_content in h_contents:
        area = h_content.text.split("高风险")[0]
        position = h_content.table.tr.find('td', attrs={'class': 'h-td1'}).text
        ra = RiskyArea()
        area_names = area.split()
        # print(area_names)
        province_name_cn = area_names[0]
        if is_municipality(province_name_cn):
            ra.areaId = province_name_cn
        else:
            ra.areaId = area_names[1]
        ra.risk = "high"
        ra.riskyAreaId = f"risk_area_{get_timestamp()}"
        ra.description = area + position
        risky_areas.append(ra.__dict__)

    m_contents = bsobj.find_all('div', attrs={'class': 'm-header'})
    for m_content in m_contents:
        area = m_content.text.split("中风险")[0]
        position = m_content.table.tr.find('td', attrs={'class': 'm-td1'}).text
        ra = RiskyArea()
        area_names = area.split()
        province_name_cn = area_names[0]
        if is_municipality(province_name_cn):
            ra.areaId = province_name_cn
        else:
            ra.areaId = area_names[1]
        ra.risk = "mid"
        ra.riskyAreaId = f"risk_area_{get_timestamp()}"
        ra.description = area + " " + position
        risky_areas.append(ra.__dict__)
    # print(risky_areas)
    r = delete_instances(s, 'risky-areas')
    if r.status_code == 200:
        r = insert_instance_list(s, 'risky-areas', risky_areas)
        if r.status_code == 200:
            print(f"[{datetime.now()}] update risky area Done")
        else:
            print(f"[{datetime.now()}] update risky area Failed -- {r.status_code}")

    else:
        print(f"[{datetime.now()}] update risky area Failed -- delete failed")
    # save_json(f'../data/risky_area_{datetime.now().date()}.json', risky_areas)


def update_baidu_news(s):
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/'
    html = fetch_url(url)
    bsobj = BeautifulSoup(html, 'html.parser')
    # print(bsobj.prettify())
    infos = bsobj.find_all('div', attrs={"data-click": "{'act': 'news_more_click'}"})
    print(infos)
    ns_list = []
    for info in infos:
        ns = News()
        report = info.find('div', attrs={"class": "Virus_1-1-308_TB6x3k"})
        time_str = '2021年' + ''.join(
            map(lambda x: x.text, info.find('div', attrs={"class": "Virus_1-1-308_2myqYf"}).find_all('span')))
        _time = datetime.strptime(time_str, "%Y年%m月%d日%H:%M")
        href = report.a['href']
        text = report.div.text
        ns.link = href
        ns.title = text
        ns.time = get_timestamp(_time)
        ns.type = 'msg'
        ns.id = f"news_{sha_256(ns.link.encode())}"
        ns_list.append(ns.__dict__)
    # resp = insert_instance_list(s, 'news', ns_list)
    # if resp.status_code != 200:
    #     print(f"[{datetime.now()}] update_baidu_news Failed -- {resp.status_code}")
    # else:
    #     print(f"[{datetime.now()}] update_baidu_news Done")
    return ns_list


def get_isaa_news():
    url = isaa_host + '/nCoV/api/news?page=1&num=100'
    r = requests.get(url)
    newses = r.json()['results']
    # print(newses)
    ns_list = []
    for news in newses:
        ns = News()
        ns.title = news['title']
        ns.link = news['sourceUrl']
        ns.content = news['summary']
        ns.id = f"news_{sha_256(ns.link.encode())}"
        ns.type = 'msg'
        ns.time = news['pubDate']
        ns_list.append(ns.__dict__)
    return ns_list


def update_isaa_news(s):
    ns_list = get_isaa_news()
    resp = insert_instance_list(s, 'news', ns_list)
    if resp.status_code != 200:
        print(f"[{datetime.now()}] update_news Failed -- {resp.status_code}")
    else:
        print(f"[{datetime.now()}] update_news Done")
    return ns_list


def update_news(s):
    baidu_news = update_baidu_news(s)
    isaa_news = update_isaa_news(s)
    baidu_news.extend(isaa_news)
    save_json(f'../news_{datetime.now().date()}.json', isaa_news)


def run():
    s = get_session()
    # update_news(s)
    update_isaa_news(s)
    update_gov_reports(s)
    update_newly_risky_areas(s)


if __name__ == '__main__':
    while True:
        try:
            run()
            time.sleep(5 * 60)
        except Exception as e:
            trace_back = sys.exc_info()[2]
            traceback.print_tb(trace_back)
            # break
