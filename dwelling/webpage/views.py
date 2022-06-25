from django.shortcuts import render
from urllib.parse import unquote
import folium
import pandas as pd
import numpy as np

HOME, HOTEL, BUSINESS = 0, 1, 2
ADEQUATE, NORMAL, SHORT = 0, 1, 2

color_dict = {
    "交通设施" : "blue",
    "休闲娱乐" : "darkred", 
    "公司企业" : "black",
    "医疗保健" : "red",
    "商务住宅" : "lightgray",
    "政府机构" : "lightred",
    "旅游景点" : "green",
    "汽车相关" : "lightgreen",
    "生活服务" : "lightgreen",
    "科教文化" : "purple",
    "自然地物" : "darkgreen",
    "行政地标" : "darkpurple",
    "购物消费" : "beige",
    "运动健身" : "cadetblue",
    "酒店住宿" : "pink",
    "金融机构" : "gray",
    "餐饮美食" : "orange",
}

estate_types_dict = {
    HOME: {
        ADEQUATE: ["住宅区", "商住两用楼宇", "别墅"],
        NORMAL: ["住宅区", "商住两用楼宇"],
        SHORT: ["住宅区"],
    },
    HOTEL: {
        ADEQUATE: ["宾馆酒店", "旅馆招待所", "经济型连锁酒店", "三星级宾馆", "四星级宾馆", "五星级宾馆", "青年旅舍"],
        NORMAL: ["宾馆酒店", "旅馆招待所", "经济型连锁酒店", "青年旅舍"],
        SHORT: ["旅馆招待所", "经济型连锁酒店", "青年旅舍"]
    },
    BUSINESS: {
        ADEQUATE: ["写字楼", "商住两用楼宇", "产业园区"],
        NORMAL: ["写字楼", "商住两用楼宇"],
        SHORT: ["商住两用楼宇"],
    },
}

# Create your views here.
def servey(request):
    if request.method == "POST":
        data = parse_data(unquote(request.body.decode()))
        estate_type = data["房源类型"]
        weight = [data["教育质量上乘"], data["消费场所多样"], data["医疗健康保证"], data["旅游资源丰富"], data["交通运输便捷"]]
        budget = data["预算"]
        print(data)
        recommend(estate_type, weight, budget)
        return render(request, "map.html")
    else:
        return render(request, "servey.html")

#以下为工具函数
def parse_data(data_str: str):
    data = {}
    for pair in data_str.split("&"):
        k,v = pair.split("=")
        data[k] = int(v)
    return data

def draw_map(estates: pd.DataFrame, filename="./html/map.html"):
    yangpu_url = "https://geo.datav.aliyun.com/areas_v3/bound/310110.json"
    gaode_url = "http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}"
    map = folium.Map(location=[31.27,121.52], zoom_start=12, tiles = gaode_url, attr = "default")
    folium.GeoJson(
        yangpu_url,
        style_function=lambda feature: {
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
            "dashArray": "5, 5"
        }
    ).add_to(map)
    for index, row in estates.iterrows():
        type = row["大类"]
        longitude = row["经度"]
        latitude = row["纬度"]
        name = row["名称"]
        folium.Marker(location=[latitude, longitude],
                popup=folium.Popup(name, max_width=10), icon=folium.Icon(color=color_dict[type])).add_to(map)
    if filename:
        map.save(filename)
    return map

def recommend(estate_type, weight, budget):
    estates = pd.read_csv("../fuzzy_estates.csv")
    types = estate_types_dict[estate_type][budget] #查找estate_type和budget对应类别
    estates = estates[estates["中类"].isin(types)] #根据类别筛选出房源
    estates.index = range(len(estates)) #重置行索引
    weight = np.array(weight)
    scores = estates.iloc[:, 9:].values #所有房源的五项得分
    scores = scores.dot(weight.T) #点乘权重向量
    index = (-scores).argsort() #获取降序排序的索引
    estates = estates.loc[index, :] #根据索引重新排序房源
    draw_map(estates.iloc[:5, :]) #在地图上标注出前五个房源