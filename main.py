from common import config
from MyBackendPackage import assembling, recommending, dbaccessing
from MyBackendPackage.jsonerror import NpEncoder
from dummy import dummy
import numpy as np
import pandas as pd
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()



origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



downloadschema_list = config.schemaconfig.downloadschemaname.value
parse_list = config.parseconfig.parselist.value
keyword_list = config.analyticsconfig.keywordlist.value

info = dbaccessing.func_dbdownload(parse_list[0], downloadschema_list[0])
kind = dbaccessing.func_dbdownload(parse_list[1], downloadschema_list[0])
dist = dbaccessing.func_dbdownload(parse_list[2], downloadschema_list[0])
menu = dbaccessing.func_dbdownload(parse_list[3], downloadschema_list[0])
review = dbaccessing.func_dbdownload(parse_list[4], downloadschema_list[0])
saesam = dbaccessing.func_dbdownload(keyword_list[0], downloadschema_list[1])
naver = dbaccessing.func_dbdownload(keyword_list[1], downloadschema_list[1])

df = assembling.assemble_func(info, kind, dist, menu, review, saesam, naver)
recommend_df = dummy.dummy_func()



@app.get("/")
def get_all() :
    target_df = df.iloc[:45, :].reset_index(drop = True)

    target = target_df.to_dict(orient = 'records')
    result = json.dumps(target, ensure_ascii = False, cls = NpEncoder).encode('utf8')
    return result



@app.get("/items/{id}")
def get_id(id: int) :
    target_df0 = df[df["id"] == id].reset_index(drop = True)
    target0 = target_df0.to_dict(orient = 'records')

    target_df1 = recommend_df[recommend_df['id'] == id].iloc[:, 1:].reset_index(drop = True)
    target1 = target_df1.to_dict(orient = 'records')

    target = target0 + target1
    result = json.dumps(target, ensure_ascii = False, cls = NpEncoder).encode('utf8')
    return result



@app.get("/{local}")
def get_local(local: str) :
    target_df = df[df["local"] == local].iloc[:45, :].reset_index(drop = True)
    
    target = target_df.to_dict(orient = 'records')
    result = json.dumps(target, ensure_ascii = False, cls = NpEncoder).encode('utf8')
    return result



@app.get("/{local}/{kindcondition}")
def get_kind(local: str, kindcondition: str) :
    kind_condition = []

    if kindcondition is None : kind_condition = ""
    else : kind_condition = kindcondition.split(',')

    target_df = df[(df["local"] == local) & (df["kind_big"].isin(kind_condition))].reset_index(drop = True)
    
    target = target_df.to_dict(orient = 'records')
    result = json.dumps(target, ensure_ascii = False, cls = NpEncoder).encode('utf8')
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
    result = json.dumps(target, ensure_ascii = False, cls = NpEncoder).encode('utf8')
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
    result = json.dumps(target, ensure_ascii = False, cls = NpEncoder).encode('utf8')
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
        result = json.dumps(target, ensure_ascii = False, cls = NpEncoder).encode('utf8')
        return result