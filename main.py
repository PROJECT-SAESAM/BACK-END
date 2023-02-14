import numpy as np
import pandas as pd
import json
from fastapi import FastAPI



app = FastAPI()



# 데이터 불러오기 (경로 주의)
info = pd.read_csv(f"./data/info.tsv", encoding = "utf-8", index_col = 0, sep = '\t')
kind = pd.read_csv(f"./data/kind.tsv", encoding = "utf-8", index_col = 0, sep = '\t')
dist = pd.read_csv(f"./data/dist.tsv", encoding = "utf-8", index_col = 0, sep = '\t')
menu = pd.read_csv(f"./data/menu.tsv", encoding = "utf-8", index_col = 0, sep = '\t')
count = pd.read_csv(f"./data/count.tsv", encoding = "utf-8", index_col = 0, sep = '\t')
review = pd.read_csv(f"./data/review.tsv", encoding = "utf-8", index_col = 0, sep = '\t')

df = pd.concat([info, kind.iloc[:, 2:], dist.iloc[:, 2:], count.iloc[:, 2:]], axis = 1)

id_list = list(menu["id"].unique())
xs = []
ys = []

for i in range(len(id_list)) :
    x_df = menu[menu["id"] == id_list[i]]
    x = list(zip(x_df["menu_name"], x_df["menu_price"]))
    xs.append(x)

for i in range(len(id_list)) :
    y_df = review[review["id"] == id_list[i]]
    y = list(zip(y_df["review_keyword"], y_df["review_num"]))
    ys.append(y)

df["menu"] = xs
df["review"] = ys

df = df.fillna(-1)

def re_dist(x) :
    if x == 1 : x = "5분미만"
    elif x == 2 : x = "5분이상10분미만"
    elif x == 3 : x = "10분이상15분미만"
    elif x == 4 : x = "15분이상"
    else : x = "정보없음"
    return x

df['walk'] = df['walk'].apply(re_dist)

re_col = df.columns
re_type = ['int', 'str', 'str', 'str', 'str', 'str', 'str', 'str', 'str', 'str', 'str', 'str', 'str', 'float', 'str', 'float', 'float', 'object', 'object']

for i in range(len(re_col)) :
    df[re_col[i]] = df[re_col[i]].astype(re_type[i])



@app.get("/")
def get_all() :
    
    target = df.iloc[:45, :].to_dict(orient = 'records')
    result = json.dumps(target, ensure_ascii = False).encode('utf8')
    
    return result



@app.get("/{local}")
def get_local(local: str) :

    target = df[df["local"] == local].iloc[:45, :].to_dict(orient = 'records')
    result = json.dumps(target, ensure_ascii = False).encode('utf8')
    
    return result



@app.get("/{local}/{kindcondition}")
def get_kind(local: str, kindcondition: str) :

    kind_condition = []

    if kindcondition is None : kind_condition = ""
    else : kind_condition = kindcondition.split(',')

    target = df[(df["local"] == local) & (df["kind_big"].isin(kind_condition))].to_dict(orient = 'records')
    result = json.dumps(target, ensure_ascii = False).encode('utf8')

    return result



@app.get("/{local}/{kindcondition}/{subwaycondition}")
def get_subway(local: str, kindcondition: str, subwaycondition: str) :

    kind_condition = []
    subway_condition = []

    if kindcondition is None : kind_condition = ""
    else : kind_condition = kindcondition.split(',')

    if subwaycondition is None : subway_condition = ""
    else : subway_condition = subwaycondition.split(',')

    target = df[(df["local"] == local) & (df["kind_big"].isin(kind_condition)) & (df["subway"].isin(subway_condition))].to_dict(orient = 'records')
    result = json.dumps(target, ensure_ascii = False).encode('utf8')

    return result



@app.get("/{local}/{kindcondition}/{subwaycondition}/{walkcondition}")
def get_dist(local: str, kindcondition: str, subwaycondition: str, walkcondition: str) :

    kind_condition = []
    subway_condition = []
    walk_condition = []

    if kindcondition is None : kind_condition = ""
    else : kind_condition = kindcondition.split(',')

    if subwaycondition is None : subway_condition = ""
    else : subway_condition = subwaycondition.split(',')

    if walkcondition is None : walk_condition = ""
    else : walk_condition = walkcondition.split(',')

    target = df[(df["local"] == local) & (df["kind_big"].isin(kind_condition)) & (df["subway"].isin(subway_condition)) & (df["walk"].isin(walk_condition))].to_dict(orient= 'records')
    result = json.dumps(target, ensure_ascii = False).encode('utf8')

    return result