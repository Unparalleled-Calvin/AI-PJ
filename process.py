import pandas as pd
from score import get_func, km_max
import geopy.distance
import json
import fuzzy

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

def calc_one_type_scores(type: str, subtypes: list, data_dict: dict, locations: pd.DataFrame, norm = True): # 计算locations中所有的分数 
    scores = []
    for index, data in locations.iterrows():
        location = [data["纬度"], data["经度"]]
        score = sum([calc_score(data_dict[subtype], location) for subtype in subtypes])
        scores.append(score)
    if norm:
        max_score, min_score = max(scores), min(scores)
        scores = [(score-min_score)/(max_score-min_score) for score in scores]
    scores = pd.DataFrame(scores, columns=[type])
    return scores

def calc_all_types_scores(types: dict, data_dict: dict, locations: pd.DataFrame, norm = True): # 计算并拼接所有type下locations的分数
    type_scores = [calc_one_type_scores(type, subtypes, data_dict, locations, norm) for type, subtypes in types.items()]
    type_scores = pd.concat(type_scores, axis = 1) # 横向拼接
    return type_scores

def get_estates(subtype_dict=None, yangpu_data=None, filename="estates.csv"): # 获得初步处理的各处房源信息，包括各个具体poi的得分，如果没有文件则会自动运行计算
    try:
        estates = pd.read_csv(filename)
    except FileNotFoundError:
        if subtype_dict is None or yangpu_data is None:
            raise Exception("The file is not found, so sybtupe_dict and yangpu_data cannot be None.")
        estates = yangpu_data[yangpu_data.loc[:, "大类"].isin(["商务住宅", "酒店住宿"])]
        estates.index = range(len(estates))
        locations = estates.loc[:, ["纬度", "经度"]]
        subtype_data_dict = split_data(yangpu_data)
        estates = pd.concat([estates, calc_all_types_scores(subtype_dict, subtype_data_dict, locations)], axis = 1)
        estates.to_csv(filename, index=0)
    return estates

def get_subtype_dict(filename="subtype.json"): # 读入要计算贡献的poi类别
    with open(filename, "r", encoding="utf8") as f:
        subtype_dict = json.load(f)
    return subtype_dict



if __name__ == "__main__":
    # data = pd.read_csv("上海市POI数据.csv")
    # yangpu_data = data[data.loc[:,"区域"] == "杨浦区"]
    subtype_dict = get_subtype_dict()
    estates = get_estates()
    estates_fuzzy = fuzzy.get_fuzzy_estates(estates)