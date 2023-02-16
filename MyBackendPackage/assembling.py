import numpy as np
import pandas as pd



def assemble_func(info, kind, dist, menu, review, saesam, naver) :
    df = pd.merge(info, kind, on = 'id')
    df = pd.merge(df, dist, on = 'id')

    id_list = list(df["id"].unique())

    xs = []
    ys = []
    ks = []
    zs = []

    for i in range(len(id_list)) :
        x_df = menu[menu["id"] == id_list[i]]
        x = list(zip(x_df["menu_name"], x_df["menu_price"]))
        xs.append(x)

    for i in range(len(id_list)) :
        y_df = review[review["id"] == id_list[i]]
        y = list(zip(y_df["review_keyword"], y_df["review_num"]))
        ys.append(y)

    for i in range(len(id_list)) :
        k_df = saesam[saesam["id"] == id_list[i]]
        k = list(k_df["saesamkeyword"])
        ks.append(k)

    for i in range(len(id_list)) :
        z_df = naver[naver["id"] == id_list[i]]
        z = list(z_df["naverkeyword"])
        zs.append(z)

    df["menu"] = xs
    df["review"] = ys
    df['saesam'] = ks
    df["naver"] = zs

    return df