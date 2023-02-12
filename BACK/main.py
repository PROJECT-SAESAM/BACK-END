import numpy as np
import pandas as pd
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder



app = FastAPI()

df = pd.read_csv(f"data/test.tsv", encoding = "utf-8", index_col = 0, sep = '\t')



class RequestCondition(BaseModel) :
    kindcondition : List[str] = ["맛집", "카페", "술집"]
    # subwaycondition : list = list(df["subway"].unique())
    # walkcondition : list = list(df["walk"].unique())
    # keywordcondition : List[list] = list(df["review_keyword"].unique())
    



@app.get("/{local}")
def get_local(local: str) :
    id_list = []
    target = df[df["local"] == local].to_dict(orient = 'records')
    for i in range(len(target)) : id_list.append(target[i]["id"])
    result = dict(zip(id_list, target))

    return jsonable_encoder(result)

# {"detail":[{"loc":["body"],"msg":"field required","type":"value_error.missing"}]}

@app.get("/{local}/items")
def get_local(local: str, req: RequestCondition) :
    
    req_dict = req.dict()
    target = df[(df["local"] == local) & (df["kind_big"].isin(req_dict["kindcondition"]))].to_dict(orient = 'records')

    id_list = []
    for i in range(len(target)) : id_list.append(target[i]["id"])
    
    result = dict(zip(id_list, target))

    return jsonable_encoder(result)


{0(==id) : {~~~~~}, 1: {~~~~}}


# @app.get("/{local}/{kind_big}/{subway}")
# def get_local(local: str, kind_big: List, subway: List) :
#     id_list = []
#     target = df[(df["local"] == local) & (df["kind_big"].isin(kind_big)) & (df["subway"].isin(subway))].to_dict(orient = 'records')
#     for i in range(len(target)) : id_list.append(target[i]["id"])
#     result = dict(zip(id_list, target))

#     return jsonable_encoder(result)



# @app.get("/{local}/{kind_big}/{subway}/{walk}")
# def get_local(local: str, kind_big: List, subway: List, walk: List) :
#     id_list = []
#     target = df[(df["local"] == local) & (df["kind_big"].isin(kind_big)) & (df["subway"].isin(subway)) & (df["walk"].isin(walk))].to_dict(orient = 'records')
#     for i in range(len(target)) : id_list.append(target[i]["id"])
#     result = dict(zip(id_list, target))

#     return jsonable_encoder(result)



# @app.get("/{local}/{kind_big}/{subway}/{walk}")
# def get_local(local: str, kind_big: List, subway: List, walk: List) :
#     id_list = []
#     target = df[(df["local"] == local) & (df["kind_big"].isin(kind_big)) & (df["subway"].isin(subway)) & (df["walk"].isin(walk))].to_dict(orient = 'records')
#     for i in range(len(target)) : id_list.append(target[i]["id"])
#     result = dict(zip(id_list, target))

#     return jsonable_encoder(result)