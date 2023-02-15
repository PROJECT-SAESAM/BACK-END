from common import config
from MyBackendPackage import assembling
from MyBackendPackage import dbaccessing
import numpy as np
import pandas as pd
import json
from fastapi import FastAPI



downloadschema_list = config.schemaconfig.downloadschemaname.value
parse_list = config.parseconfig.parselist.value
keyword_list = config.analyticsconfig.keywordlist.value
recommend_list = config.analyticsconfig.recommendlist.value

info = dbaccessing.func_dbdownload(parse_list[0], downloadschema_list[0])
kind = dbaccessing.func_dbdownload(parse_list[1], downloadschema_list[0])
dist = dbaccessing.func_dbdownload(parse_list[2], downloadschema_list[0])
menu = dbaccessing.func_dbdownload(parse_list[3], downloadschema_list[0])
review = dbaccessing.func_dbdownload(parse_list[4], downloadschema_list[0])

naver = dbaccessing.func_dbdownload(keyword_list[0], downloadschema_list[1])
saesam = dbaccessing.func_dbdownload(keyword_list[1], downloadschema_list[1])



app = FastAPI()



info = pd.read_csv(f"./data/info.csv", encoding = "utf-8", index_col = 0)
kind = pd.read_csv(f"./data//kind.csv", encoding = "utf-8", index_col = 0)
dist = pd.read_csv(f"./data/dist.csv", encoding = "utf-8", index_col = 0)
menu = pd.read_csv(f"./data/menu.csv", encoding = "utf-8", index_col = 0)
review = pd.read_csv(f"./data/review.csv", encoding = "utf-8", index_col = 0)
naver = pd.read_csv(f"./data/naverkeyword.csv", encoding = "utf-8", index_col = 0)
saesam = pd.read_csv(f"./data/saesamkeyword.csv", encoding = "utf-8", index_col = 0)



df = pd.concat([info, kind.iloc[:, 1:], dist.iloc[:, 1:]], axis = 1)

id_list = list(df["id"].unique())

xs = []
ys = []
zs = []
ks = []

for i in range(len(id_list)) :
    x_df = menu[menu["id"] == id_list[i]]
    x = list(zip(x_df["menu_name"], x_df["menu_price"]))
    xs.append(x)

for i in range(len(id_list)) :
    y_df = review[review["id"] == id_list[i]]
    y = list(zip(y_df["review_keyword"], y_df["review_num"]))
    ys.append(y)

for i in range(len(id_list)) :
    z_df = naver[naver["id"] == id_list[i]]
    z = list(z_df["naverkeyword"])
    zs.append(z)

for i in range(len(id_list)) :
    k_df = saesam[saesam["id"] == id_list[i]]
    k = list(k_df["naverkeyword"])
    ks.append(k)

df["menu"] = xs
df["review"] = ys
df["naver"] = zs
df['saesam'] = ks




@app.get("/")
def get_all() :
    target_df = df.iloc[:45, :].reset_index(drop = True)

    target = target_df.to_dict(orient = 'records')
    result = json.dumps(target, ensure_ascii = False).encode('utf8')
    return result



@app.get("/items/{id}")
def get_id(id: int) :
    target_df = df[df["id"] == id].reset_index(drop = True)
    
    target = target_df.to_dict(orient = 'records')
    result = json.dumps(target, ensure_ascii = False).encode('utf8')
    return result



@app.get("/{local}")
def get_local(local: str) :
    target_df = df[df["local"] == local].iloc[:45, :].reset_index(drop = True)
    
    target = target_df.to_dict(orient = 'records')
    result = json.dumps(target, ensure_ascii = False).encode('utf8')
    return result



@app.get("/{local}/{kindcondition}")
def get_kind(local: str, kindcondition: str) :
    kind_condition = []

    if kindcondition is None : kind_condition = ""
    else : kind_condition = kindcondition.split(',')

    target_df = df[(df["local"] == local) & (df["kind_big"].isin(kind_condition))].reset_index(drop = True)
    
    target = target_df.to_dict(orient = 'records')
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

    target_df = df[(df["local"] == local) & (df["kind_big"].isin(kind_condition)) & (df["subway"].isin(subway_condition))].reset_index(drop = True)
    
    target = target_df.to_dict(orient = 'records')
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

    target_df = df[(df["local"] == local) & (df["kind_big"].isin(kind_condition)) & (df["subway"].isin(subway_condition)) & (df["walk"].isin(walk_condition))].reset_index(drop = True)
    
    target = target_df.to_dict(orient= 'records')
    result = json.dumps(target, ensure_ascii = False).encode('utf8')
    return result



@app.get("/{local}/{kindcondition}/{subwaycondition}/{walkcondition}/{keywordcondition}")
def get_keyword(local: str, kindcondition: str, subwaycondition: str, walkcondition: str, keywordcondition: str) :
    kind_condition = []
    subway_condition = []
    walk_condition = []
    keyword_condition = []

    if kindcondition is None : kind_condition = ""
    else : kind_condition = kindcondition.split(',')

    if subwaycondition is None : subway_condition = ""
    else : subway_condition = subwaycondition.split(',')

    if walkcondition is None : walk_condition = ""
    else : walk_condition = walkcondition.split(',')

    if keywordcondition is None : keyword_condition = ""
    else : keyword_condition = keywordcondition.split(',')

    target_df = df[(df["local"] == local) & (df["kind_big"].isin(kind_condition)) & (df["subway"].isin(subway_condition)) & (df["walk"].isin(walk_condition))].reset_index(drop = True)
    col_num = list(target_df.columns).index("saesam")

    no_index = []

    for k in range(len(target_df)) :
        for i in range(len(keyword_condition)) :
            if keyword_condition[i] not in target_df.iloc[k, col_num] : 
                no_index.append(k)
    
    try : target_df = target_df.drop(no_index, axis = 0).reset_index(drop = True)
    
    except : target_df = target_df
    
    finally :
        target = target_df.to_dict(orient= 'records')
        result = json.dumps(target, ensure_ascii = False).encode('utf8')
        return result