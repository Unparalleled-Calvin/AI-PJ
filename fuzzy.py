import skfuzzy as fuzz
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

score_range = np.arange(0, 1.1, 0.01)
Good = fuzz.trimf(score_range, [0.6, 1, 1])
Average = fuzz.trimf(score_range, [0.3, 0.5, 0.7])
Poor = fuzz.trimf(score_range, [0, 0, 0.4])

def Education_fuzzy(education, plot=False):
    High = fuzz.trimf(score_range, [0.8, 1, 1])
    Medium = fuzz.trimf(score_range, [0.5, 0.65, 0.85])
    Low = fuzz.trimf(score_range, [0, 0, 0.55])
    education_Good = fuzz.interp_membership(score_range, Good, education)
    education_Average = fuzz.interp_membership(score_range, Average, education)
    education_Poor = fuzz.interp_membership(score_range, Poor, education)
    rule1 = education_Good
    rule2 = education_Average
    rule3 = education_Poor
    Education_High = np.fmin(rule1, High)
    Education_Medium = np.fmin(rule2, Medium)
    Education_Low = np.fmin(rule3, Low)
    aggregated = np.fmax(Education_High, np.fmax(Education_Medium, Education_Low))
    Education = fuzz.defuzz(score_range, aggregated, 'centroid')
    activation = fuzz.interp_membership(score_range, aggregated, Education)
    if plot:
        plot_fuzzy(Education, activation, Low, Medium, High, aggregated)
    return Education

def Consuming_fuzzy(entertainment, consuming, plot=False):
    Plenty = fuzz.trimf(score_range, [0.7, 1, 1])
    Normal = fuzz.trimf(score_range, [0.3, 0.55, 0.75])
    Short = fuzz.trimf(score_range, [0, 0, 0.4])
    entertainment_Good = fuzz.interp_membership(score_range, Good, entertainment)
    entertainment_Average = fuzz.interp_membership(score_range, Average, entertainment)
    entertainment_Poor = fuzz.interp_membership(score_range, Poor, entertainment)
    consuming_Good = fuzz.interp_membership(score_range, Good, consuming)
    consuming_Average = fuzz.interp_membership(score_range, Average, consuming)
    consuming_Poor = fuzz.interp_membership(score_range, Poor, consuming)
    rule4 = np.fmax(entertainment_Good, consuming_Good)
    rule5 = np.fmax(np.fmin(entertainment_Average, 1 - consuming_Good),np.fmin(consuming_Average, 1 - entertainment_Good))
    rule6 = np.fmin(entertainment_Poor, consuming_Poor)
    Consuming_Plenty = np.fmin(rule4, Plenty)
    Consuming_Normal = np.fmin(rule5, Normal)
    Consuming_Short = np.fmin(rule6, Short)
    aggregated = np.fmax(Consuming_Plenty, np.fmax(Consuming_Normal, Consuming_Short))
    Consuming = fuzz.defuzz(score_range, aggregated, 'centroid')
    activation = fuzz.interp_membership(score_range, aggregated, Consuming)
    if plot:
        plot_fuzzy(Consuming, activation, Short, Normal, Plenty, aggregated)
    return Consuming

def Health_fuzzy(health, sport, plot=False):
    High = fuzz.trimf(score_range, [0.8, 1, 1])
    Medium = fuzz.trimf(score_range, [0.5, 0.65, 0.85])
    Low = fuzz.trimf(score_range, [0, 0, 0.55])
    health_Good = fuzz.interp_membership(score_range, Good, health)
    health_Average = fuzz.interp_membership(score_range, Average, health)
    health_Poor = fuzz.interp_membership(score_range, Poor, health)
    sport_Good = fuzz.interp_membership(score_range, Good, sport)
    sport_Average = fuzz.interp_membership(score_range, Average, sport)
    sport_Poor = fuzz.interp_membership(score_range, Poor, sport)
    rule7 = np.fmax(health_Good, sport_Good)
    rule8 = np.fmin(health_Average, 1 - sport_Good)
    rule9 = np.fmin(health_Poor, 1 - sport_Good)
    Health_High = np.fmin(rule7, High)
    Health_Medium = np.fmin(rule8, Medium)
    Health_Low = np.fmin(rule9, Low)
    aggregated = np.fmax(Health_High, np.fmax(Health_Medium, Health_Low))
    Health = fuzz.defuzz(score_range, aggregated, 'centroid')
    activation = fuzz.interp_membership(score_range, aggregated, Health)
    if plot:
        plot_fuzzy(Health, activation, Low, Medium, High, aggregated)
    return Health

def Tourism_fuzzy(tourism, restaurant, plot=False):
    Rich = fuzz.trimf(score_range, [0.8, 1, 1])
    Normal = fuzz.trimf(score_range, [0.5, 0.65, 0.85])
    Short = fuzz.trimf(score_range, [0, 0, 0.55])
    tourism_Good = fuzz.interp_membership(score_range, Good, tourism)
    tourism_Average = fuzz.interp_membership(score_range, Average, tourism)
    tourism_Poor = fuzz.interp_membership(score_range, Poor, tourism)
    restaurant_Good = fuzz.interp_membership(score_range, Good, restaurant)
    restaurant_Average = fuzz.interp_membership(score_range, Average, restaurant)
    restaurant_Poor = fuzz.interp_membership(score_range, Poor, restaurant)
    rule4 = np.fmax(tourism_Good, restaurant_Good)
    rule5 = np.fmax(np.fmin(tourism_Average, 1 - restaurant_Good),np.fmin(restaurant_Average, 1 - tourism_Good))
    rule6 = np.fmin(tourism_Poor, restaurant_Poor)
    Tourism_Rich = np.fmin(rule4, Rich)
    Tourism_Normal = np.fmin(rule5, Normal)
    Tourism_Short = np.fmin(rule6, Short)
    aggregated = np.fmax(Tourism_Rich, np.fmax(Tourism_Normal, Tourism_Short))
    Tourism = fuzz.defuzz(score_range, aggregated, 'centroid')
    activation = fuzz.interp_membership(score_range, aggregated, Tourism)
    if plot:
        plot_fuzzy(Tourism, activation, Short, Normal, Rich, aggregated)
    return Tourism

def Transportation_fuzzy(transportation, plot=False):
    Convenient = fuzz.trimf(score_range, [0.7, 1, 1])
    Normal = fuzz.trimf(score_range, [0.4, 0.55, 0.75])
    Inconvenient = fuzz.trimf(score_range, [0, 0, 0.45])
    transportation_Good = fuzz.interp_membership(score_range, Good, transportation)
    transportation_Average = fuzz.interp_membership(score_range, Average, transportation)
    transportation_Poor = fuzz.interp_membership(score_range, Poor, transportation)
    rule1 = transportation_Good
    rule2 = transportation_Average
    rule3 = transportation_Poor
    Transportation_Convenient = np.fmin(rule1, Convenient)
    Transportation_Normal = np.fmin(rule2, Normal)
    Transportation_Inconvenient = np.fmin(rule3, Inconvenient)
    aggregated = np.fmax(Transportation_Convenient, np.fmax(Transportation_Normal, Transportation_Inconvenient))
    Transportation = fuzz.defuzz(score_range, aggregated, 'centroid')
    activation = fuzz.interp_membership(score_range, aggregated, Transportation)
    if plot:
        plot_fuzzy(Transportation, activation, Inconvenient, Normal, Convenient)
    return Transportation

def plot_fuzzy(X, activation, A, B, C, aggregated, title=""):
    score0 = np.zeros_like(score_range)
    fig, ax0 = plt.subplots(figsize=(6, 3))
    ax0.plot(score_range, A, 'b', linewidth=0.5, linestyle='--', )
    plt.plot(score_range, B, 'g', linewidth=0.5, linestyle='--')
    ax0.plot(score_range, C, 'r', linewidth=0.5, linestyle='--')
    ax0.fill_between(score_range, score0, aggregated, facecolor='Orange', alpha=0.7)
    ax0.plot([X, X], [0, activation], 'k', linewidth=1.5, alpha=0.9)
    ax0.set_title(title)
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
    plt.tight_layout()

def calc_one_fuzzy_scores(index, row: pd.DataFrame):
    transportation, entertainment, consuming, health, sport, education, restaurant, tourism = row.iloc[9:] #图省事来点魔法数字哈哈哈哈
    scores = {
        "教育质量": Education_fuzzy(education),
        "消费场所": Consuming_fuzzy(entertainment, consuming),
        "医疗健康": Health_fuzzy(health, sport),
        "旅游资源": Tourism_fuzzy(tourism, restaurant),
        "交通运输": Transportation_fuzzy(transportation)
    }
    return pd.DataFrame(scores, [index])

def calc_all_fuzzy_scores(estates: pd.DataFrame):
    fuzzy_scores = [calc_one_fuzzy_scores(index, row) for index, row in estates.iterrows()]
    fuzzy_scores = pd.concat(fuzzy_scores, axis = 0) # 纵向拼接
    return fuzzy_scores

def get_fuzzy_estates(estates: pd.DataFrame=None, filename="fuzzy_estates.csv"):
    try:
        fuzzy_estates = pd.read_csv(filename)
    except FileNotFoundError:
        if estates is None:
            raise Exception("The file is not found, so estates cannot be None.")
        fuzzy_estates = pd.concat([estates.iloc[:,:9], calc_all_fuzzy_scores(estates)], axis = 1)
        fuzzy_estates.to_csv(filename, index=0)
    return fuzzy_estates