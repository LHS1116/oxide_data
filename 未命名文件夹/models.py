from typing import List

from django.db import models


class Area(object):
    id: str
    china: bool
    # area_label: str country：area_country；province：area_country_province; city: area_country_province_city
    # name: str
    parentId: str
    level: int #1：国家， 2：省/州， 3：城市
    is_china: bool #int不是，1是

    # label = models.CharField(max_length=64 null=False default="" verbose_name="地区唯一标识符")
    # name = models.CharField(max_length=64 null=False default="" verbose_name="中文名称")
    # parent_label = models.CharField(max_length=64 null=False default="" verbose_name="上级地区")
    # level = models.IntegerField(null=False default=1 verbose_name="地区等级")
    # is_china = models.IntegerField(null=False default=1 verbose_name="是否中国地区")
    #
    # class Meta:
    #     db_table = 'oxide_area'


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
#
# class AirLine(models.Model):
#     id: str
#     airports: List[str]  # 2个
#     flights: List[str]  # 多个 e.g. ["BW1537BW15int3"]
#     areas: List[str]  # 2个，为airportint23t对应的area的id
#
#
# class FlightCancellation(models.Model):
#     id: str
#     flight: str  # e.g. BW1537
#
#
# class Rail(models.Model):
#     id: str
#     name: str
#     passAreas: List[str]
#
#
# class Subscription(models.Model):
#     id: str
#     userId: str
#     areaId: str
#
#


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
    content: str
    type: str  # enum "政策" | "通告" | "疫情情况"; # 可能不会用到这些type，取决于数据能否整理出

#
class Tip(object):
    id: str
    title: str
    content: str
    type: str  # "常识" | "辟谣";

#
# class Question(models.Model):
#     id: str
#
#     senderId: str
#
#     title: str
#     content: str
#
#
# class Answer(models.Model):
#     id: str
#
#     senderId: str
#     questionId: str
#
#     isOfficial: bool
#
#     replyTo: str  # answerId
#
#     content: str
