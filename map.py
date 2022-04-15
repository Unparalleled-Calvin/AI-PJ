import folium
import pandas as pd
yangpu_url = "https://geo.datav.aliyun.com/areas_v3/bound/310110.json"
gaode_url = "http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}"

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


data = pd.read_csv("上海市POI数据.csv")
yangpu_data = data[data.loc[:,"区域"] == "杨浦区"]

cnt = 0
for i,row in yangpu_data.iterrows():
    class_ = row["大类"]
    longitude = row["经度"]
    latitude = row["纬度"]
    name = row["名称"]
    cnt += class_ == "商务住宅"
    if (class_ == "商务住宅" and cnt % 100 == 0) or i % 500==0:
        folium.Marker(location=[latitude, longitude],
                popup=name, icon=folium.Icon(color=color_dict[class_])).add_to(map)
map.save("result.html")