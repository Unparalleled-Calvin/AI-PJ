import pandas as pd
from score import get_func, km_max
import geopy.distance
import pickle

def split_data(yangpu_data: pd.DataFrame): # 返回{subtype: DataFrame}
    subtypes = list(yangpu_data.loc[:, "中类"].unique())
    subtype_data_dict = {}
    for subtype in subtypes:
        subtype_data_dict[subtype] = yangpu_data[yangpu_data.loc[:, "中类"] == subtype]
    return subtype_data_dict

def calc_score(subtype_data: pd.DataFrame, location: list): # 计算subtype_data对一个location=[latitute, longitude]的分数
    func = get_func()
    score = 0
    for index, data in subtype_data.iterrows():
        location_ = (data["纬度"], data["经度"])
        distance = geopy.distance.geodesic(location_, location).km
        score += func(distance) if distance <= km_max else 0
    return score

def calc_one_type_scores(type: str, data_dict: pd.DataFrame, locations: pd.DataFrame, norm = True): # 计算locations中所有的分数 
    type_data = data_dict[type]
    scores = []
    for index, data in locations.iterrows():
        location = [data["纬度"], data["经度"]]
        score = calc_score(type_data, location)
        scores.append(score)
    if norm:
        max_score, min_score = max(scores), min(scores)
        scores = [(score-min_score)/(max_score-min_score) for score in scores]
    scores = pd.DataFrame(scores, columns=[type])
    return scores

def calc_all_types_scores(types: list, data_dict: pd.DataFrame, locations: pd.DataFrame, norm = True): # 计算并拼接所有type下locations的分数
    type_scores = [calc_one_type_scores(type, data_dict, locations, norm) for type in types]
    type_scores = pd.concat(type_scores, axis = 1) # 横向拼接
    return type_scores

if __name__ == "__main__":
    data = pd.read_csv("上海市POI数据.csv")
    yangpu_data = data[data.loc[:,"区域"] == "杨浦区"]
    subtype_data_dict = split_data(yangpu_data)
    subtype_dict = {
        "traffic_subtypes": [
            "地铁站",
            "公交车站",
            "停车场",
        ],
        "entertainment_subtypes": [
            "KTV",
            "网吧",
            "电影院",
        ],
        "shopping_subtypes": [
            "超市",
            "商业街",
            "购物中心",
        ],
        "medical_subtypes": [
            "综合医院",
            "专科医院",
            "医药保健销售",
        ],
        "sport_subtypes": [
            "篮球场馆",
            "综合体育馆",
            "足球场",
            "健身中心",
        ],
        "academic_subtypes": [
            "中学",
            "小学",
            "高等院校",
            "博物馆",
            "图书馆",
        ],
        "food_subtypes": [
            "中国菜",
            "外国菜",
            "小吃快餐",
        ],
        "tourism_subtypes": [
            "公园",
            "景点",
            "纪念馆",
        ]
    }
    subtypes = []
    for types in subtype_dict.values():
        subtypes.extend(types)
    estates = yangpu_data[yangpu_data.loc[:, "大类"].isin(["商务住宅", "酒店住宿"])]
    estates.index = range(len(estates))
    locations = estates.loc[:, ["纬度", "经度"]]
    estates = pd.concat([estates, calc_all_types_scores(subtypes, subtype_data_dict, locations)], axis = 1)
    with open("estates.pkl", "wb") as f:
        pickle.dump(estates, f)