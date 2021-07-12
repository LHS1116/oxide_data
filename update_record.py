import csv
import hashlib
import json
import os
import random
import sys
import threading
import time
import traceback
from datetime import datetime
from typing import Dict

import requests

vaccions = {}

country_dict_en = {
    'Afghanistan': '阿富汗',
    'Albania': '阿尔巴尼亚',
    'Algeria': '阿尔及利亚',
    'American Samoa': '东萨摩亚',
    'Andorra': '安道尔共和国',
    'Angola': '安哥拉',
    'Anguilla': '安圭拉岛',
    'Antigua and Barbuda': '安提瓜和巴布达',
    'Argentina': '阿根廷',
    'Armenia': '亚美尼亚',
    'Ascension': '阿森松',
    'Australia': '澳大利亚',
    'Austria': '奥地利',
    'Azerbaijan': '阿塞拜疆',
    'Bahamas': '巴哈马',
    'Bahrain': '巴林',
    'Bangladesh': '孟加拉国',
    'Barbados': '巴巴多斯',
    'Belarus': '白俄罗斯',
    'Belgium': '比利时',
    'Belize': '伯利兹',
    'Benin': '贝宁',
    'Bermuda Is': '百慕大群岛',
    'Bhutan': '不丹',
    'Bolivia': '玻利维亚',
    'Bosnia and Herzegovina': '波斯尼亚和黑塞哥维那',
    'Botswana': '博茨瓦纳',
    'Brazil': '巴西',
    'Brunei': '文莱',
    'Bulgaria': '保加利亚',
    'Burkina Faso': '布基纳法索',
    'Burma': '缅甸',
    'Burundi': '布隆迪',
    'Cabo Verde': '佛得角',
    'Cambodia': '柬埔寨',
    'Cameroon': '喀麦隆',
    'Canada': '加拿大',
    'Cayman Is': '开曼群岛',
    'Central African Republic': '中非共和国',
    'Chad': '乍得',
    'Chile': '智利',
    'China': '中国',
    'Colombia': '哥伦比亚',
    'Comoros': '科摩罗',
    'Congo': '刚果',
    'Congo (Brazzaville)': '刚果(布拉柴维尔)',
    'Congo (Kinshasa)': '刚果(金)',
    'Cook Is': '库克群岛',
    'Costa Rica': '哥斯达黎加',
    "Cote d'Ivoire": '科特迪瓦',
    'Croatia': '克罗地亚',
    'Cuba': '古巴',
    'Cyprus': '塞浦路斯',
    'Czech Republic': '捷克',
    'Czechia': '捷克',
    'Denmark': '丹麦',
    'Diamond Princess': '钻石公主号游轮',
    'Djibouti': '吉布提',
    'Dominica': '多米尼加',
    'Dominica Rep': '多米尼加共和国',
    'Dominican Republic': '多米尼加共和国',
    'EI Salvador': '萨尔瓦多',
    'Ecuador': '厄瓜多尔',
    'Egypt': '埃及',
    'El Salvador': '萨尔瓦多',
    'Equatorial Guinea': '赤道几内亚',
    'Eritrea': '厄立特里亚',
    'Estonia': '爱沙尼亚',
    'Eswatini': '埃斯瓦蒂尼',
    'Ethiopia': '埃塞俄比亚',
    'Fiji': '斐济',
    'Finland': '芬兰',
    'France': '法国',
    'French Guiana': '法属圭亚那',
    'French Polynesia': '法属玻利尼西亚',
    'Gabon': '加蓬',
    'Gambia': '冈比亚',
    'Georgia': '格鲁吉亚',
    'Germany': '德国',
    'Ghana': '加纳',
    'Gibraltar': '直布罗陀',
    'Greece': '希腊',
    'Grenada': '格林纳达',
    'Guam': '关岛',
    'Guatemala': '危地马拉',
    'Guinea': '几内亚',
    'Guinea-Bissau': '几内亚比绍',
    'Guyana': '圭亚那',
    'Haiti': '海地',
    'Holy See': '梵蒂冈',
    'Honduras': '洪都拉斯',
    'Hongkong': '香港',
    'Hong Kong': '香港',
    'Hungary': '匈牙利',
    'Iceland': '冰岛',
    'India': '印度',
    'Indonesia': '印度尼西亚',
    'Iran': '伊朗',
    'Iraq': '伊拉克',
    'Ireland': '爱尔兰',
    'Israel': '以色列',
    'Italy': '意大利',
    'Ivory Coast': '科特迪瓦',
    'Jamaica': '牙买加',
    'Japan': '日本',
    'Jordan': '约旦',
    'Kampuchea (Cambodia )': '柬埔寨',
    'Kampuchea': '柬埔寨',
    'Kazakhstan': '哈萨克斯坦',
    'Kazakstan': '哈萨克斯坦',
    'Kenya': '肯尼亚',
    'Kiribati': '基里巴斯',
    'Korea': '韩国',
    'South Korea': '韩国',
    'Korea, South': '韩国',
    'Kosovo': '科索沃',
    'Kuwait': '科威特',
    'Kyrgyzstan': '吉尔吉斯坦',
    'Laos': '老挝',
    'Latvia': '拉脱维亚',
    'Lebanon': '黎巴嫩',
    'Lesotho': '莱索托',
    'Liberia': '利比里亚',
    'Libya': '利比亚',
    'Liechtenstein': '列支敦士登',
    'Lithuania': '立陶宛',
    'Luxembourg': '卢森堡',
    'MS Zaandam': '尚丹号邮轮',
    'Macao': '澳门',
    'Macau': '澳门',
    'Madagascar': '马达加斯加',
    'Mainland China': '中国',
    'Malawi': '马拉维',
    'Malaysia': '马来西亚',
    'Maldives': '马尔代夫',
    'Mali': '马里',
    'Malta': '马耳他',
    'Mariana Is': '马里亚那群岛',
    'Marshall Islands': '马绍尔群岛',
    'Martinique': '马提尼克',
    'Mauritania': '毛里塔尼亚',
    'Mauritius': '毛里求斯',
    'Mexico': '墨西哥',
    'Micronesia': '密克罗尼西亚联邦',
    'Moldova': '摩尔多瓦',
    'Monaco': '摩纳哥',
    'Mongolia': '蒙古',
    'Montenegro': '黑山共和国',
    'Montserrat Is': '蒙特塞拉特岛',
    'Morocco': '摩洛哥',
    'Mozambique': '莫桑比克',
    'Namibia': '纳米比亚',
    'Nauru': '瑙鲁',
    'Nepal': '尼泊尔',
    'Netheriands Antilles': '荷属安的列斯',
    'Netherlands': '荷兰',
    'New Zealand': '新西兰',
    'Nicaragua': '尼加拉瓜',
    'Niger': '尼日尔',
    'Nigeria': '尼日利亚',
    'North Korea': '朝鲜',
    'North Macedonia': '北马其顿',
    'Norway': '挪威',
    'Oman': '阿曼',
    'Pakistan': '巴基斯坦',
    'Palau': '帕劳',
    'Panama': '巴拿马',
    'Papua New Cuinea': '巴布亚新几内亚',
    'Papua New Guinea': '巴布亚新几内亚',
    'Paraguay': '巴拉圭',
    'Peru': '秘鲁',
    'Philippines': '菲律宾',
    'Poland': '波兰',
    'Portugal': '葡萄牙',
    'Puerto Rico': '波多黎各',
    'Qatar': '卡塔尔',
    'Reunion': '留尼旺',
    'Romania': '罗马尼亚',
    'Russia': '俄罗斯',
    'Rwanda': '卢旺达',
    'Saint Kitts and Nevis': '圣基茨和尼维斯',
    'Saint Lucia': '圣卢西亚',
    'Saint Vincent': '圣文森特岛',
    'Saint Vincent and the Grenadines': '文森特和格林纳丁斯',
    'Samoa': '萨摩亚',
    'Samoa Eastern': '东萨摩亚(美)',
    'Samoa Western': '西萨摩亚',
    'San Marino': '圣马力诺',
    'Sao Tome and Principe': '圣多美和普林西比',
    'Saudi Arabia': '沙特阿拉伯',
    'Senegal': '塞内加尔',
    'Serbia': '塞尔维亚',
    'Seychelles': '塞舌尔',
    'Sierra Leone': '塞拉利昂',
    'Singapore': '新加坡',
    'Slovakia': '斯洛伐克',
    'Slovenia': '斯洛文尼亚',
    'Solomon Islands': '所罗门群岛',
    'Saint Helena Solomon Is': '圣赫勒拿所罗门群岛',
    'Somali': '索马里',
    'Somalia': '索马里',
    'South Africa': '南非',
    'South Sudan': '南苏丹',
    'Spain': '西班牙',
    'Sri Lanka': '斯里兰卡',
    'SriLanka': '斯里兰卡',
    'St.Lucia': '圣卢西亚',
    'St.Vincent': '圣文森特',
    'Sudan': '苏丹',
    'Summer Olympics 2020': '2020年夏季奥运会',
    'Suriname': '苏里南',
    'Swaziland': '斯威士兰',
    'Sweden': '瑞典',
    'Switzerland': '瑞士',
    'Syria': '叙利亚',
    'Taiwan': '台湾省',
    'Taiwan*': '台湾',
    'Tajikistan': '塔吉克斯坦',
    'Tanzania': '坦桑尼亚',
    'Thailand': '泰国',
    'Timor-Leste': '东帝汶',
    'Togo': '多哥',
    'Tonga': '汤加',
    'Trinidad and Tobago': '特立尼达和多巴哥',
    'Tunisia': '突尼斯',
    'Turkey': '土耳其',
    'Turkmenistan': '土库曼斯坦',
    'US': '美国',
    'United States': '美国',
    'Uganda': '乌干达',
    'Ukraine': '乌克兰',
    'United Arab Emirates': '阿拉伯联合酋长国',
    'United Kingdom': '英国',
    'United States of America': '美国',
    'USA': '美国',
    'Uruguay': '乌拉圭',
    'Uzbekistan': '乌兹别克斯坦',
    'Vanuatu': '瓦努阿图',
    'Venezuela': '委内瑞拉',
    'Vietnam': '越南',
    'West Bank and Gaza': '西岸和加沙',
    'W. Sahara': '撒哈拉',
    'Greenland': '格陵兰岛',
    'Yemen': '也门',
    'Yugoslavia': '南斯拉夫',
    'Zaire': '扎伊尔',
    'Zambia': '赞比亚',
    'Zimbabwe': '津巴布韦',
    'Aruba': '阿鲁巴', 'Bermuda': '百慕大', 'Bonaire Sint Eustatius and Saba': '博内尔圣尤斯特修斯和萨巴',
    'British Virgin Islands': '英属维尔京群岛', 'Cape Verde': '佛得角', 'Cayman Islands': '开曼群岛', 'Cook Islands': '库克群岛',
    'Curacao': '库拉索', 'Democratic Republic of Congo': '刚果民主共和国', 'Faeroe Islands': '法罗群岛', 'Falkland Islands': '福克兰群岛',
    'Guernsey': '根西岛', 'Isle of Man': '马恩岛', 'Jersey': '泽西岛', 'Micronesia (country)': '密克罗尼西亚', 'Montserrat': '蒙特塞拉特',
    'Myanmar': '缅甸', 'New Caledonia': '新喀里多尼亚', 'Northern Cyprus': '北塞浦路斯', 'Palestine': '巴勒斯坦', 'Pitcairn': '皮特凯恩',
    'Saint Helena': '圣赫勒拿', 'Sint Maarten (Dutch part)': '圣马丁岛', 'Timor': '帝汶', 'Turks and Caicos Islands': '特克斯和凯科斯群岛',
    'Tuvalu': '图瓦卢', 'Vatican': '梵蒂冈', 'Wallis and Futuna': '瓦利斯和富图纳'

}

country_dict_cn = {'阿富汗': ['Afghanistan'], '阿尔巴尼亚': ['Albania'], '阿尔及利亚': ['Algeria'], '东萨摩亚': ['American Samoa'],
                   '安道尔共和国': ['Andorra'], '安哥拉': ['Angola'], '安圭拉岛': ['Anguilla'], '安提瓜和巴布达': ['Antigua and Barbuda'],
                   '阿根廷': ['Argentina'], '亚美尼亚': ['Armenia'], '阿森松': ['Ascension'], '澳大利亚': ['Australia'],
                   '奥地利': ['Austria'], '阿塞拜疆': ['Azerbaijan'], '巴哈马': ['Bahamas'], '巴林': ['Bahrain'],
                   '孟加拉国': ['Bangladesh'], '巴巴多斯': ['Barbados'], '白俄罗斯': ['Belarus'], '比利时': ['Belgium'],
                   '伯利兹': ['Belize'], '贝宁': ['Benin'], '百慕大群岛': ['Bermuda Is'], '不丹': ['Bhutan'], '玻利维亚': ['Bolivia'],
                   '波斯尼亚和黑塞哥维那': ['Bosnia and Herzegovina'], '博茨瓦纳': ['Botswana'], '巴西': ['Brazil'], '文莱': ['Brunei'],
                   '保加利亚': ['Bulgaria'], '布基纳法索': ['Burkina Faso'], '缅甸': ['Burma', 'Myanmar'], '布隆迪': ['Burundi'],
                   '佛得角': ['Cabo Verde', 'Cape Verde'], '柬埔寨': ['Cambodia', 'Kampuchea (Cambodia )', 'Kampuchea'],
                   '喀麦隆': ['Cameroon'], '加拿大': ['Canada'], '开曼群岛': ['Cayman Is', 'Cayman Islands'],
                   '中非共和国': ['Central African Republic'], '乍得': ['Chad'], '智利': ['Chile'],
                   '中国': ['China', 'Mainland China'], '哥伦比亚': ['Colombia'], '科摩罗': ['Comoros'], '刚果': ['Congo'],
                   '刚果(布拉柴维尔)': ['Congo (Brazzaville)'], '刚果(金)': ['Congo (Kinshasa)'],
                   '库克群岛': ['Cook Is', 'Cook Islands'], '哥斯达黎加': ['Costa Rica'],
                   '科特迪瓦': ["Cote d'Ivoire", 'Ivory Coast'], '克罗地亚': ['Croatia'], '古巴': ['Cuba'], '塞浦路斯': ['Cyprus'],
                   '捷克': ['Czech Republic', 'Czechia'], '丹麦': ['Denmark'], '钻石公主号游轮': ['Diamond Princess'],
                   '吉布提': ['Djibouti'], '多米尼加': ['Dominica'], '多米尼加共和国': ['Dominica Rep', 'Dominican Republic'],
                   '萨尔瓦多': ['EI Salvador', 'El Salvador'], '厄瓜多尔': ['Ecuador'], '埃及': ['Egypt'],
                   '赤道几内亚': ['Equatorial Guinea'], '厄立特里亚': ['Eritrea'], '爱沙尼亚': ['Estonia'], '埃斯瓦蒂尼': ['Eswatini'],
                   '埃塞俄比亚': ['Ethiopia'], '斐济': ['Fiji'], '芬兰': ['Finland'], '法国': ['France'],
                   '法属圭亚那': ['French Guiana'], '法属玻利尼西亚': ['French Polynesia'], '加蓬': ['Gabon'], '冈比亚': ['Gambia'],
                   '格鲁吉亚': ['Georgia'], '德国': ['Germany'], '加纳': ['Ghana'], '直布罗陀': ['Gibraltar'], '希腊': ['Greece'],
                   '格林纳达': ['Grenada'], '关岛': ['Guam'], '危地马拉': ['Guatemala'], '几内亚': ['Guinea'],
                   '几内亚比绍': ['Guinea-Bissau'], '圭亚那': ['Guyana'], '海地': ['Haiti'], '梵蒂冈': ['Holy See', 'Vatican'],
                   '洪都拉斯': ['Honduras'], '香港': ['Hongkong', 'Hong Kong'], '匈牙利': ['Hungary'], '冰岛': ['Iceland'],
                   '印度': ['India'], '印度尼西亚': ['Indonesia'], '伊朗': ['Iran'], '伊拉克': ['Iraq'], '爱尔兰': ['Ireland'],
                   '以色列': ['Israel'], '意大利': ['Italy'], '牙买加': ['Jamaica'], '日本': ['Japan'], '约旦': ['Jordan'],
                   '哈萨克斯坦': ['Kazakhstan', 'Kazakstan'], '肯尼亚': ['Kenya'], '基里巴斯': ['Kiribati'],
                   '韩国': ['Korea', 'South Korea', 'Korea, South'], '科索沃': ['Kosovo'], '科威特': ['Kuwait'],
                   '吉尔吉斯坦': ['Kyrgyzstan'], '老挝': ['Laos'], '拉脱维亚': ['Latvia'], '黎巴嫩': ['Lebanon'], '莱索托': ['Lesotho'],
                   '利比里亚': ['Liberia'], '利比亚': ['Libya'], '列支敦士登': ['Liechtenstein'], '立陶宛': ['Lithuania'],
                   '卢森堡': ['Luxembourg'], '尚丹号邮轮': ['MS Zaandam'], '澳门': ['Macao', 'Macau'], '马达加斯加': ['Madagascar'],
                   '马拉维': ['Malawi'], '马来西亚': ['Malaysia'], '马尔代夫': ['Maldives'], '马里': ['Mali'], '马耳他': ['Malta'],
                   '马里亚那群岛': ['Mariana Is'], '马绍尔群岛': ['Marshall Islands'], '马提尼克': ['Martinique'],
                   '毛里塔尼亚': ['Mauritania'], '毛里求斯': ['Mauritius'], '墨西哥': ['Mexico'], '密克罗尼西亚联邦': ['Micronesia'],
                   '摩尔多瓦': ['Moldova'], '摩纳哥': ['Monaco'], '蒙古': ['Mongolia'], '黑山共和国': ['Montenegro'],
                   '蒙特塞拉特岛': ['Montserrat Is'], '摩洛哥': ['Morocco'], '莫桑比克': ['Mozambique'], '纳米比亚': ['Namibia'],
                   '瑙鲁': ['Nauru'], '尼泊尔': ['Nepal'], '荷属安的列斯': ['Netheriands Antilles'], '荷兰': ['Netherlands'],
                   '新西兰': ['New Zealand'], '尼加拉瓜': ['Nicaragua'], '尼日尔': ['Niger'], '尼日利亚': ['Nigeria'],
                   '朝鲜': ['North Korea'], '北马其顿': ['North Macedonia'], '挪威': ['Norway'], '阿曼': ['Oman'],
                   '巴基斯坦': ['Pakistan'], '帕劳': ['Palau'], '巴拿马': ['Panama'],
                   '巴布亚新几内亚': ['Papua New Cuinea', 'Papua New Guinea'], '巴拉圭': ['Paraguay'], '秘鲁': ['Peru'],
                   '菲律宾': ['Philippines'], '波兰': ['Poland'], '葡萄牙': ['Portugal'], '波多黎各': ['Puerto Rico'],
                   '卡塔尔': ['Qatar'], '留尼旺': ['Reunion'], '罗马尼亚': ['Romania'], '俄罗斯': ['Russia'], '卢旺达': ['Rwanda'],
                   '圣基茨和尼维斯': ['Saint Kitts and Nevis'], '圣卢西亚': ['Saint Lucia', 'St.Lucia'],
                   '圣文森特岛': ['Saint Vincent'], '文森特和格林纳丁斯': ['Saint Vincent and the Grenadines'], '萨摩亚': ['Samoa'],
                   '东萨摩亚(美)': ['Samoa Eastern'], '西萨摩亚': ['Samoa Western'], '圣马力诺': ['San Marino'],
                   '圣多美和普林西比': ['Sao Tome and Principe'], '沙特阿拉伯': ['Saudi Arabia'], '塞内加尔': ['Senegal'],
                   '塞尔维亚': ['Serbia'], '塞舌尔': ['Seychelles'], '塞拉利昂': ['Sierra Leone'], '新加坡': ['Singapore'],
                   '斯洛伐克': ['Slovakia'], '斯洛文尼亚': ['Slovenia'], '所罗门群岛': ['Solomon Islands'],
                   '圣赫勒拿所罗门群岛': ['Saint Helena Solomon Is'], '索马里': ['Somali', 'Somalia'], '南非': ['South Africa'],
                   '南苏丹': ['South Sudan'], '西班牙': ['Spain'], '斯里兰卡': ['Sri Lanka', 'SriLanka'], '圣文森特': ['St.Vincent'],
                   '苏丹': ['Sudan'], '2020年夏季奥运会': ['Summer Olympics 2020'], '苏里南': ['Suriname'], '斯威士兰': ['Swaziland'],
                   '瑞典': ['Sweden'], '瑞士': ['Switzerland'], '叙利亚': ['Syria'], '台湾省': ['Taiwan'], '台湾': ['Taiwan*'],
                   '塔吉克斯坦': ['Tajikistan'], '坦桑尼亚': ['Tanzania'], '泰国': ['Thailand'], '东帝汶': ['Timor-Leste'],
                   '多哥': ['Togo'], '汤加': ['Tonga'], '特立尼达和多巴哥': ['Trinidad and Tobago'], '突尼斯': ['Tunisia'],
                   '土耳其': ['Turkey'], '土库曼斯坦': ['Turkmenistan'],
                   '美国': ['US', 'United States', 'United States of America', 'USA'], '乌干达': ['Uganda'],
                   '乌克兰': ['Ukraine'],
                   '阿拉伯联合酋长国': ['United Arab Emirates'], '英国': ['United Kingdom'], '乌拉圭': ['Uruguay'],
                   '乌兹别克斯坦': ['Uzbekistan'], '瓦努阿图': ['Vanuatu'], '委内瑞拉': ['Venezuela'], '越南': ['Vietnam'],
                   '西岸和加沙': ['West Bank and Gaza'], '撒哈拉': ['W. Sahara'], '格陵兰岛': ['Greenland'], '也门': ['Yemen'],
                   '南斯拉夫': ['Yugoslavia'], '扎伊尔': ['Zaire'], '赞比亚': ['Zambia'], '津巴布韦': ['Zimbabwe'], '阿鲁巴': ['Aruba'],
                   '百慕大': ['Bermuda'], '博内尔圣尤斯特修斯和萨巴': ['Bonaire Sint Eustatius and Saba'],
                   '英属维尔京群岛': ['British Virgin Islands'], '库拉索': ['Curacao'],
                   '刚果民主共和国': ['Democratic Republic of Congo'], '法罗群岛': ['Faeroe Islands'],
                   '福克兰群岛': ['Falkland Islands'], '根西岛': ['Guernsey'], '马恩岛': ['Isle of Man'], '泽西岛': ['Jersey'],
                   '密克罗尼西亚': ['Micronesia (country)'], '蒙特塞拉特': ['Montserrat'], '新喀里多尼亚': ['New Caledonia'],
                   '北塞浦路斯': ['Northern Cyprus'], '巴勒斯坦': ['Palestine'], '皮特凯恩': ['Pitcairn'], '圣赫勒拿': ['Saint Helena'],
                   '圣马丁岛': ['Sint Maarten (Dutch part)'], '帝汶': ['Timor'], '特克斯和凯科斯群岛': ['Turks and Caicos Islands'],
                   '图瓦卢': ['Tuvalu'], '瓦利斯和富图纳': ['Wallis and Futuna']}

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

city_name_dict = {
    "北京": "北京市",
    "天津": "天津市",
    "石家庄": "石家庄市",
    "唐山": "唐山市",
    "秦皇岛": "秦皇岛市",
    "邯郸": "邯郸市",
    "邢台": "邢台市",
    "保定": "保定市",
    "张家口": "张家口市",
    "承德": "承德市",
    "沧州": "沧州市",
    "廊坊": "廊坊市",
    "衡水": "衡水市",
    "太原": "太原市",
    "大同": "大同市",
    "阳泉": "阳泉市",
    "长治": "长治市",
    "晋城": "晋城市",
    "朔州": "朔州市",
    "晋中": "晋中市",
    "运城": "运城市",
    "忻州": "忻州市",
    "临汾": "临汾市",
    "吕梁": "吕梁市",
    "呼和浩特": "呼和浩特市",
    "包头": "包头市",
    "乌海": "乌海市",
    "赤峰": "赤峰市",
    "通辽": "通辽市",
    "鄂尔多斯": "鄂尔多斯市",
    "呼伦贝尔": "呼伦贝尔市",
    "巴彦淖尔": "巴彦淖尔市",
    "乌兰察布": "乌兰察布市",
    "兴安盟": "兴安盟",
    "锡林郭勒盟": "锡林郭勒盟",
    "阿拉善盟": "阿拉善盟",
    "沈阳": "沈阳市",
    "大连": "大连市",
    "鞍山": "鞍山市",
    "抚顺": "抚顺市",
    "本溪": "本溪市",
    "丹东": "丹东市",
    "锦州": "锦州市",
    "营口": "营口市",
    "阜新": "阜新市",
    "辽阳": "辽阳市",
    "盘锦": "盘锦市",
    "铁岭": "铁岭市",
    "朝阳": "朝阳市",
    "葫芦岛": "葫芦岛市",
    "长春": "长春市",
    "吉林市": "吉林市",
    "四平": "四平市",
    "辽源": "辽源市",
    "通化": "通化市",
    "白山": "白山市",
    "松原": "松原市",
    "白城": "白城市",
    "延边": "延边朝鲜族自治州",
    "哈尔滨": "哈尔滨市",
    "齐齐哈尔": "齐齐哈尔市",
    "鸡西": "鸡西市",
    "鹤岗": "鹤岗市",
    "双鸭山": "双鸭山市",
    "大庆": "大庆市",
    "伊春": "伊春市",
    "佳木斯": "佳木斯市",
    "七台河": "七台河市",
    "牡丹江": "牡丹江市",
    "黑河": "黑河市",
    "绥化": "绥化市",
    "大兴安岭地区": "大兴安岭地区",
    "上海": "上海市",
    "南京": "南京市",
    "无锡": "无锡市",
    "徐州": "徐州市",
    "常州": "常州市",
    "苏州": "苏州市",
    "南通": "南通市",
    "连云港": "连云港市",
    "淮安": "淮安市",
    "盐城": "盐城市",
    "扬州": "扬州市",
    "镇江": "镇江市",
    "泰州": "泰州市",
    "宿迁": "宿迁市",
    "杭州": "杭州市",
    "宁波": "宁波市",
    "温州": "温州市",
    "嘉兴": "嘉兴市",
    "湖州": "湖州市",
    "绍兴": "绍兴市",
    "金华": "金华市",
    "衢州": "衢州市",
    "舟山": "舟山市",
    "台州": "台州市",
    "丽水": "丽水市",
    "合肥": "合肥市",
    "芜湖": "芜湖市",
    "蚌埠": "蚌埠市",
    "淮南": "淮南市",
    "马鞍山": "马鞍山市",
    "淮北": "淮北市",
    "铜陵": "铜陵市",
    "安庆": "安庆市",
    "黄山": "黄山市",
    "滁州": "滁州市",
    "阜阳": "阜阳市",
    "宿州": "宿州市",
    "六安": "六安市",
    "亳州": "亳州市",
    "池州": "池州市",
    "宣城": "宣城市",
    "福州": "福州市",
    "厦门": "厦门市",
    "莆田": "莆田市",
    "三明": "三明市",
    "泉州": "泉州市",
    "漳州": "漳州市",
    "南平": "南平市",
    "龙岩": "龙岩市",
    "宁德": "宁德市",
    "南昌": "南昌市",
    "景德镇": "景德镇市",
    "萍乡": "萍乡市",
    "九江": "九江市",
    "新余": "新余市",
    "鹰潭": "鹰潭市",
    "赣州": "赣州市",
    "吉安": "吉安市",
    "宜春": "宜春市",
    "抚州": "抚州市",
    "上饶": "上饶市",
    "济南": "济南市",
    "青岛": "青岛市",
    "淄博": "淄博市",
    "枣庄": "枣庄市",
    "东营": "东营市",
    "烟台": "烟台市",
    "潍坊": "潍坊市",
    "济宁": "济宁市",
    "泰安": "泰安市",
    "威海": "威海市",
    "日照": "日照市",
    "临沂": "临沂市",
    "德州": "德州市",
    "聊城": "聊城市",
    "滨州": "滨州市",
    "菏泽": "菏泽市",
    "郑州": "郑州市",
    "开封": "开封市",
    "洛阳": "洛阳市",
    "平顶山": "平顶山市",
    "安阳": "安阳市",
    "鹤壁": "鹤壁市",
    "新乡": "新乡市",
    "焦作": "焦作市",
    "濮阳": "濮阳市",
    "许昌": "许昌市",
    "漯河": "漯河市",
    "三门峡": "三门峡市",
    "南阳": "南阳市",
    "商丘": "商丘市",
    "信阳": "信阳市",
    "周口": "周口市",
    "驻马店": "驻马店市",
    "武汉": "武汉市",
    "黄石": "黄石市",
    "十堰": "十堰市",
    "宜昌": "宜昌市",
    "襄阳": "襄阳市",
    "鄂州": "鄂州市",
    "荆门": "荆门市",
    "孝感": "孝感市",
    "荆州": "荆州市",
    "黄冈": "黄冈市",
    "咸宁": "咸宁市",
    "随州": "随州市",
    "恩施": "恩施土家族苗族自治州",
    "长沙": "长沙市",
    "株洲": "株洲市",
    "湘潭": "湘潭市",
    "衡阳": "衡阳市",
    "邵阳": "邵阳市",
    "岳阳": "岳阳市",
    "常德": "常德市",
    "张家界": "张家界市",
    "益阳": "益阳市",
    "郴州": "郴州市",
    "永州": "永州市",
    "怀化": "怀化市",
    "娄底": "娄底市",
    "湘西土家族苗族自治州": "湘西土家族苗族自治州",
    "广州": "广州市",
    "韶关": "韶关市",
    "深圳": "深圳市",
    "珠海": "珠海市",
    "汕头": "汕头市",
    "佛山": "佛山市",
    "江门": "江门市",
    "湛江": "湛江市",
    "茂名": "茂名市",
    "肇庆": "肇庆市",
    "惠州": "惠州市",
    "梅州": "梅州市",
    "汕尾": "汕尾市",
    "河源": "河源市",
    "阳江": "阳江市",
    "清远": "清远市",
    "东莞": "东莞市",
    "中山": "中山市",
    "潮州": "潮州市",
    "揭阳": "揭阳市",
    "云浮": "云浮市",
    "南宁": "南宁市",
    "柳州": "柳州市",
    "桂林": "桂林市",
    "梧州": "梧州市",
    "北海": "北海市",
    "防城港": "防城港市",
    "钦州": "钦州市",
    "贵港": "贵港市",
    "玉林": "玉林市",
    "百色": "百色市",
    "贺州": "贺州市",
    "河池": "河池市",
    "来宾": "来宾市",
    "崇左": "崇左市",
    "海口": "海口市",
    "三亚": "三亚市",
    "三沙": "三沙市",
    "儋州": "儋州市",
    "重庆": "重庆市",
    "成都": "成都市",
    "自贡": "自贡市",
    "攀枝花": "攀枝花市",
    "泸州": "泸州市",
    "德阳": "德阳市",
    "绵阳": "绵阳市",
    "广元": "广元市",
    "遂宁": "遂宁市",
    "内江": "内江市",
    "乐山": "乐山市",
    "南充": "南充市",
    "眉山": "眉山市",
    "宜宾": "宜宾市",
    "广安": "广安市",
    "达州": "达州市",
    "雅安": "雅安市",
    "巴中": "巴中市",
    "资阳": "资阳市",
    "阿坝藏族羌族自治州": "阿坝藏族羌族自治州",
    "甘孜藏族自治州": "甘孜藏族自治州",
    "凉山彝族自治州": "凉山彝族自治州",
    "贵阳": "贵阳市",
    "六盘水": "六盘水市",
    "遵义": "遵义市",
    "安顺": "安顺市",
    "毕节": "毕节市",
    "铜仁": "铜仁市",
    "黔西南布依族苗族自治州": "黔西南布依族苗族自治州",
    "黔东南苗族侗族自治州": "黔东南苗族侗族自治州",
    "黔南布依族苗族自治州": "黔南布依族苗族自治州",
    "昆明": "昆明市",
    "曲靖": "曲靖市",
    "玉溪": "玉溪市",
    "保山": "保山市",
    "昭通": "昭通市",
    "丽江": "丽江市",
    "普洱": "普洱市",
    "临沧": "临沧市",
    "楚雄彝族自治州": "楚雄彝族自治州",
    "红河哈尼族彝族自治州": "红河哈尼族彝族自治州",
    "文山壮族苗族自治州": "文山壮族苗族自治州",
    "西双版纳傣族自治州": "西双版纳傣族自治州",
    "大理白族自治州": "大理白族自治州",
    "德宏傣族景颇族自治州": "德宏傣族景颇族自治州",
    "怒江傈僳族自治州": "怒江傈僳族自治州",
    "迪庆藏族自治州": "迪庆藏族自治州",
    "拉萨": "拉萨市",
    "日喀则": "日喀则市",
    "昌都": "昌都市",
    "林芝": "林芝市",
    "山南": "山南市",
    "那曲": "那曲市",
    "阿里地区": "阿里地区",
    "西安": "西安市",
    "铜川": "铜川市",
    "宝鸡": "宝鸡市",
    "咸阳": "咸阳市",
    "渭南": "渭南市",
    "延安": "延安市",
    "汉中": "汉中市",
    "榆林": "榆林市",
    "安康": "安康市",
    "商洛": "商洛市",
    "兰州": "兰州市",
    "嘉峪关": "嘉峪关市",
    "金昌": "金昌市",
    "白银": "白银市",
    "天水": "天水市",
    "武威": "武威市",
    "张掖": "张掖市",
    "平凉": "平凉市",
    "酒泉": "酒泉市",
    "庆阳": "庆阳市",
    "定西": "定西市",
    "陇南": "陇南市",
    "临夏回族自治州": "临夏回族自治州",
    "甘南藏族自治州": "甘南藏族自治州",
    "西宁": "西宁市",
    "海东": "海东市",
    "海北藏族自治州": "海北藏族自治州",
    "黄南藏族自治州": "黄南藏族自治州",
    "海南藏族自治州": "海南藏族自治州",
    "果洛藏族自治州": "果洛藏族自治州",
    "玉树藏族自治州": "玉树藏族自治州",
    "海西蒙古族藏族自治": "海西蒙古族藏族自治州",
    "银川": "银川市",
    "石嘴山": "石嘴山市",
    "吴忠": "吴忠市",
    "固原": "固原市",
    "中卫": "中卫市",
    "乌鲁木齐": "乌鲁木齐市",
    "克拉玛依": "克拉玛依市",
    "吐鲁番地区": "吐鲁番市",
    "哈密": "哈密市",
    "昌吉回族自治州": "昌吉回族自治州",
    "博尔塔拉蒙古自治州": "博尔塔拉蒙古自治州",
    "巴音郭楞蒙古自治州": "巴音郭楞蒙古自治州",
    "阿克苏地区": "阿克苏地区",
    "克孜勒苏柯尔克孜自治州": "克孜勒苏柯尔克孜自治州",
    "喀什地区": "喀什地区",
    "和田地区": "和田地区",
    "伊犁州": "伊犁哈萨克自治州",
    "塔城地区": "塔城地区",
    "阿勒泰地区": "阿勒泰地区",
    "台北": "台北市",
    "高雄": "高雄市",
    "台南": "台南市",
    "台中": "台中市",
    "南投": "南投县",
    "基隆": "基隆市",
    "新竹": "新竹县",
    "嘉义": "嘉义县",
    "新北": "新北市",
    "宜兰": "宜兰县",
    "桃园": "桃园市",
    "苗栗": "苗栗县",
    "彰化": "彰化县",
    "云林": "云林县",
    "屏东": "屏东县",
    "台东": "台东县",
    "花莲": "花莲县",
    "澎湖": "澎湖县",
    "香港": "香港特别行政区",
    "澳门": "澳门特别行政区"
}

backend_host = "http://39.106.140.102:27031"

province_name_dict = dict(zip(simple_province_name, complex_province_name))


class Record(object):
    areaId: str
    id: str
    new_cases: int
    new_cured: int
    new_deaths: int
    present_cases: int
    severe_cases: int
    suspected_cases: int
    time: int
    total_cases: int
    total_cured: int
    total_deaths: int
    total_vaccines: int


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


def get_timestamp(dt: datetime = None, ms=True):
    if dt is not None:
        ts = int(round(dt.timestamp()))
        return ts * 1000 if ms else ts
    ts = int(round(time.time(), 3))
    return ts * 1000 if ms else ts


def insert_instance_list(s, resource_name, instances):
    js = instances
    if not isinstance(instances[0], dict):
        js = list(map(lambda x: x.__dict__, instances))
    resp = s.put(backend_host + f'/api/{resource_name}', json=js)
    return resp


def init_vaccions():
    # data = json.load(open('./vaccinations.json', 'r'))
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json'
    r = requests.get(url)
    data = r.json()
    tmp = {}
    for dt in data:
        tmp[dt['country']] = dt['data']

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
                        total = history.get('daily_vaccinations', 0)
                    else:
                        total += history.get('daily_vaccinations', 0)
                except Exception as e:

                    print(country_name_cn)
                    print(history)
                    raise e
                vc_country[_date] = total

            vaccions[country_name_cn] = vc_country


def update_city_record(s):
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?'
    r = requests.get(url)
    js = json.loads(
        r.text.encode().decode('unicode_escape').split('caseList')[1].split('caseOutsideList')[0][2:-1][:-1])
    res = []
    for province in js:
        # print(province)
        cities = province['subList']
        timestamp = int(province['relativeTime'])
        for city in cities:
            area = city['city']
            if city_name_dict.get(area) is None:
                continue
            rec = Record()
            rec.areaId = city_name_dict.get(area)
            rec.total_cases = city['confirmed']
            rec.total_deaths = city['died']
            rec.total_cured = city['crued']
            rec.total_vaccines = -1
            rec.severe_cases = -1
            rec.new_cases = city['confirmedRelative']
            rec.new_deaths = 0
            rec.new_cured = 0
            rec.suspected_cases = 0
            rec.present_cases = city['curConfirm']
            rec.time = timestamp
            rec.id = f'record_{rec.areaId}_{timestamp}'
            res.append(rec.__dict__)
    resp = insert_instance_list(s, 'records', res)
    if resp.status_code != 200:
        print(res)
        print(f"[{datetime.now()}] update_record_cities Failed -- {resp.status_code}")
    else:
        print(f"[{datetime.now()}] update_record_cities Done")
    # print(res)


def update_china_history(s):
    # url = f'https://voice.baidu.com/newpneumonia/getv2?target=trend&isCaseIn=1&from=mola-virus&area=全国&stage=publish'
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?'
    r = requests.get(url)
    data = r.text.encode().decode('unicode_escape').split('"trend":')[1].split(',"foreignLastUpdatedTime"')[0].split(
        'caseOutsideList')[0]
    trend = json.loads(data)
    lists = trend['list']
    update_date = trend['updateDate']

    cnt = len(update_date)

    flag = 340
    for i in range(cnt - 1):
        lst = update_date[i].split('.')
        lst1 = update_date[i + 1].split('.')

        if int(lst[0]) * 100 + int(lst[1]) > int(lst1[0]) * 100 + int(lst1[1]):
            flag = i
            break
    for i in range(cnt):
        if i <= flag:
            update_date[i] = "2020." + update_date[i]
        else:
            update_date[i] = '2021.' + update_date[i]
    # print(list(map(lambda x: x['name'], lists)))
    recode_data_list = lists[:8]  # ['确诊', '疑似', '治愈', '死亡', '新增确诊', '新增疑似', '新增治愈', '新增死亡']
    recode_data_dict = dict(zip(map(lambda x: x['name'], recode_data_list), map(lambda x: x['data'], recode_data_list)))
    res = []
    for i in range(cnt):
        _time = datetime.strptime(update_date[i], "%Y.%m.%d")
        rec = Record()
        rec.time = get_timestamp(_time, False)
        rec.total_cases = recode_data_dict.get('确诊')[i]
        rec.total_deaths = recode_data_dict.get('死亡')[i]
        rec.total_cured = recode_data_dict.get('治愈')[i]
        rec.new_cured = recode_data_dict.get('新增治愈')[i]
        rec.new_cases = recode_data_dict.get('新增确诊')[i]
        rec.new_deaths = recode_data_dict.get('新增死亡')[i]
        rec.suspected_cases = recode_data_dict.get('疑似')[i]
        rec.total_vaccines = vaccions.get('中国', {}).get(str(_time.date()),
                                                        -1 if len(res) == 0 else res[-1]['total_vaccines'])
        rec.severe_cases = -1
        rec.areaId = '中国'
        rec.id = f'record_中国_{rec.time}'
        res.append(rec.__dict__)
    resp = insert_instance_list(s, 'records', res)
    if resp.status_code != 200:
        print(res)
        print(f"[{datetime.now()}] update_record_中国 Failed -- {resp.status_code}")
    else:
        print(f"[{datetime.now()}] update_record_中国 Done")


def get_province_history(province, s):
    # url = 'https://feiyan.wecity.qq.com/wuhan/dist/index.html#/map-detail?province=北京'
    # url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?city=%E4%BA%91%E5%8D%97-%E4%BA%91%E5%8D%97'
    url = f'https://voice.baidu.com/newpneumonia/getv2?target=trend&isCaseIn=1&from=mola-virus&area={province}&stage=publish'
    r = requests.get(url)
    js = r.json()
    # print(js)
    if js['status'] != 0:
        return
    # print(js['status'])
    data = js['data'][0]
    # dt =r.text[0]
    # data = json.loads(dt)['data'][0]
    trend = data['trend']
    lists = trend['list']
    update_date = trend['updateDate']

    cnt = len(update_date)
    confirmed_trend = lists[0]['data']
    cured_trend = lists[1]['data']
    death_trend = lists[2]['data']
    new_confirmed_trend = lists[3]['data']
    flag = 340
    for i in range(cnt - 1):
        lst = update_date[i].split('.')
        lst1 = update_date[i + 1].split('.')
        # print(lst)
        # print(lst1)
        if int(lst[0]) * 100 + int(lst[1]) > int(lst1[0]) * 100 + int(lst1[1]):
            flag = i
            break
    # print(flag)
    for i in range(cnt):
        if i <= flag:
            update_date[i] = "2020." + update_date[i]
        else:
            update_date[i] = '2021.' + update_date[i]
    # print(confirmed_trend)
    records = []
    for i in range(cnt):
        # key_of_lists:['确诊', '治愈', '死亡', '新增确诊']
        _date = update_date[i]

        rec = Record()
        rec.areaId = province_name_dict.get(province, "")
        # print(update_date[i])
        _time = datetime.strptime(update_date[i], "%Y.%m.%d")
        timestamp = get_timestamp(_time, False)
        rec.id = f"record_{province}_{timestamp}"
        confirmed = confirmed_trend[i]
        cured = cured_trend[i]
        death = death_trend[i]
        rec.total_deaths = death
        rec.total_cases = confirmed
        rec.total_cured = cured
        rec.present_cases = confirmed - cured - death
        if i == 0:
            new_confirmed = new_cured = new_deaths = -1
        else:
            new_cured = cured - cured_trend[i - 1]
            new_deaths = death - death_trend[i - 1]
            new_confirmed = confirmed - confirmed_trend[i - 1]
        rec.new_cured = new_cured
        rec.new_cases = new_confirmed
        rec.new_deaths = new_deaths
        rec.total_vaccines = -1
        rec.suspected_cases = -1
        rec.severe_cases = -1
        rec.time = timestamp
        records.append(rec.__dict__)

    # print(records)
    resp = insert_instance_list(s, 'records', records)
    if resp.status_code != 200:
        print(records)
        print(f"[{datetime.now()}] update_record_{province} Failed -- {resp.status_code}")
    else:
        print(f"[{datetime.now()}] update_record_{province} Done")
    # print(data)
    #


def update_cn_history(s):
    for name in simple_province_name:
        get_province_history(name, s)
    print(f"[{datetime.now()}] update_record_cn Done")


def update_oversea_history(s):
    for name in country_dict_cn.keys():
        res = get_oversea_history(name)
        if len(res) != 0:
            resp = insert_instance_list(s, 'records', res)
            if resp.status_code != 200:
                print(res)
                print(f"[{datetime.now()}] update_record_{name} Failed -- {resp.status_code}")
            else:
                print(f"[{datetime.now()}] update_record_{name} Done")
    print(f"[{datetime.now()}] update_record_oversea Done")


def get_oversea_history(country):
    name = country
    if country == '日本':
        name = '日本本土'
    url = "https://wechat.wecity.qq.com/api/THPneumoniaOuterDataService/getForeignCountry"
    payload = {
        "args": {
            "req": {
                "country": name
            }
        },
        "service": "THPneumoniaOuterDataService",
        "func": "getForeignCountry",
        "context": {
            "userId": "1f0beb43a1404d2591e1b9c23da2ce78"
        }
    }
    res = []
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        js = r.json()
        countryHistory = js['args']['rsp']['countryHistory']
        cnt = len(countryHistory)
        res = []
        for i in range(cnt):
            item = countryHistory[i]
            _time = datetime.strptime(item['newDay'], '%Y-%m-%d')
            timestamp = get_timestamp(_time, False)
            confirmed = item['confirm']
            deaths = item['dead']
            cured = item['heal']

            new_confirmed = item['modifyConfirm'] if i == 0 else confirmed - countryHistory[i - 1]['confirm']
            new_cured = -1 if i == 0 else cured - countryHistory[i - 1]['heal']
            new_deaths = -1 if i == 0 else deaths - countryHistory[i - 1]['dead']
            rec = Record()
            rec.time = timestamp
            rec.total_cases = confirmed
            rec.total_cured = cured
            rec.total_deaths = deaths
            rec.present_cases = confirmed - deaths - cured
            rec.areaId = country
            rec.id = f'record_{country}_{timestamp}'
            rec.new_cured = new_cured
            rec.new_cases = new_confirmed
            rec.new_deaths = new_deaths
            rec.suspected_cases = -1
            rec.total_vaccines = vaccions.get(country, {}).get(str(_time.date()),
                                                               -1 if len(res) == 0 else res[-1]['total_vaccines'])
            rec.severe_cases = -1
            res.append(rec.__dict__)
    return res


if __name__ == '__main__':
    init_vaccions()
    s = get_session()
    while True:
        try:
            update_china_history(s)
            update_city_record(s)
            update_oversea_history(s)
            update_cn_history(s)
            time.sleep(5 * 60)
        except Exception as e:
            trace_back = sys.exc_info()[2]
            traceback.print_tb(trace_back)
            break


