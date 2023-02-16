from common import config, secret
from MyBackendPackage import dbaccessing
import numpy as np
import pandas as pd
import random



def dummy_df() :
    parse_list = ["info", "kind", "dist", "menu", "review"]
    downloadschema = "merged"

    df_list = []

    for i in range(len(parse_list)) :
        df = dbaccessing.func_dbdownload(parse_list[i], downloadschema)
        df_list.append(df)

    df = pd.concat([df_list[0], df_list[1].iloc[:, 1:], df_list[2].iloc[:, 1:]], axis = 1)

    id_list = list(df["id"].unique())

    xs0 = []
    xs1 = []
    ys0 = []
    ys1 = []

    for i in range(len(id_list)) :
        x_df = df_list[3][df_list[3]["id"] == id_list[i]]
        x0 = list(x_df["menu_name"])
        x1 = list(x_df["menu_price"])
        xs0.append(x0)
        xs1.append(x1)

    for i in range(len(id_list)) :
        y_df = df_list[4][df_list[4]["id"] == id_list[i]]
        y0 = list(y_df["review_keyword"])
        y1 = list(y_df["review_num"])
        ys0.append(y0)
        ys1.append(y1)

    df["menu_name"] = xs0
    df["menu_price"] = xs1
    df["review_keyword"] = ys0
    df["review_num"] = ys1

    df = df.reset_index(drop = True)

    return df

def dummy_food(df) :
    food_df = df[df['kind_big'] == '맛집'].reset_index(drop = True)
    cafe_df = df[df['kind_big'] == '카페'].reset_index(drop = True)
    drink_df = df[df['kind_big'] == '술집'].reset_index(drop = True)

    xs = list(food_df['id'].unique())

    id_subway = []

    for i in range(len(xs)) :
        subway = list(food_df[food_df['id'] == xs[i]]['subway'])[0]
        id_subway.append(subway)

    for i in range(len(id_subway)) :
        if id_subway[i] not in ["성수역", "뚝섬역", "서울숲역"] : id_subway[i] = "성수역"



    # 비슷한 가격대 맛집 추천
    recommend_first_id = []
    recommend_first_title = []
    recommend_first_img = []

    for i in range(len(xs)) :
        ys = xs.copy()
        y = ys[i]
        ys.remove(ys[i])
        recommend_first_id.append(random.sample(ys, 10))

    for i in range(len(recommend_first_id)) :
        titles = []
        imgs = []
        for k in range(len(recommend_first_id[i])) :
            id = recommend_first_id[i][k]
            x_df = food_df[food_df['id'] == id]
            title = list(x_df['title'])[0]
            img = list(x_df['image_place'])[0]
            titles.append(title)
            imgs.append(img)
        recommend_first_title.append(titles)
        recommend_first_img.append(imgs)



    # 근처 카페 추천
    recommend_second_id = []
    recommend_second_title = []
    recommend_second_img = []

    for i in range(len(xs)) :
        x_df = cafe_df[cafe_df['subway'] == id_subway[i]]
        x_id = list(x_df['id'].unique())
        recommend_second_id.append(random.sample(x_id, 10))

    for i in range(len(recommend_second_id)) :
        titles = []
        imgs = []
        for k in range(len(recommend_second_id[i])) :
            id = recommend_second_id[i][k]
            x_df = cafe_df[cafe_df['id'] == id]
            title = list(x_df['title'])[0]
            img = list(x_df['image_place'])[0]
            titles.append(title)
            imgs.append(img)
        recommend_second_title.append(titles)
        recommend_second_img.append(imgs)



    # 근처 술집 추천
    recommend_third_id = []
    recommend_third_title = []
    recommend_third_img = []

    for i in range(len(xs)) :
        x_df = drink_df[drink_df['subway'] == id_subway[i]]
        x_id = list(x_df['id'].unique())
        recommend_third_id.append(random.sample(x_id, 10))

    for i in range(len(recommend_third_id)) :
        titles = []
        imgs = []
        for k in range(len(recommend_third_id[i])) :
            id = recommend_third_id[i][k]
            x_df = drink_df[drink_df['id'] == id]
            title = list(x_df['title'])[0]
            img = list(x_df['image_place'])[0]
            titles.append(title)
            imgs.append(img)
        recommend_third_title.append(titles)
        recommend_third_img.append(imgs)



    recommend_first_list = []

    for k in range(len(recommend_first_id)) :
        recommend_first = list(zip(recommend_first_id[k], recommend_first_title[k], recommend_first_img[k]))
        recommend_first_list.append(recommend_first)


    recommend_second_list = []

    for k in range(len(recommend_second_id)) :
        recommend_second = list(zip(recommend_second_id[k], recommend_second_title[k], recommend_second_img[k]))
        recommend_second_list.append(recommend_second)


    recommend_third_list = []

    for k in range(len(recommend_third_id)) :
        recommend_third = list(zip(recommend_third_id[k], recommend_third_title[k], recommend_third_img[k]))
        recommend_third_list.append(recommend_third)


    df = pd.DataFrame({'id' : xs, 'first_reco' : recommend_first_list, 'second_reco' : recommend_second_list, 'third_reco' : recommend_third_list})

    return df

def dummy_cafe(df) :
    food_df = df[df['kind_big'] == '맛집'].reset_index(drop = True)
    cafe_df = df[df['kind_big'] == '카페'].reset_index(drop = True)
    drink_df = df[df['kind_big'] == '술집'].reset_index(drop = True)
    
    xs = list(cafe_df['id'].unique())

    id_subway = []
    for i in range(len(xs)) :
        subway = list(cafe_df[cafe_df['id'] == xs[i]]['subway'])[0]
        id_subway.append(subway)

    for i in range(len(id_subway)) :
        if id_subway[i] not in ["성수역", "뚝섬역", "서울숲역"] : id_subway[i] = "성수역"



    # 근처 혼밥하기 좋은 맛집 추천
    random.seed(121)

    recommend_first_id = []
    recommend_first_title = []
    recommend_first_img = []

    for i in range(len(xs)) :
        x_df = food_df[food_df['subway'] == id_subway[i]]
        x_id = list(x_df['id'].unique())
        recommend_first_id.append(random.sample(x_id, 10))

    for i in range(len(recommend_first_id)) :
        titles = []
        imgs = []
        for k in range(len(recommend_first_id[i])) :
            id = recommend_first_id[i][k]
            x_df = food_df[food_df['id'] == id]
            title = list(x_df['title'])[0]
            img = list(x_df['image_place'])[0]
            titles.append(title)
            imgs.append(img)
        recommend_first_title.append(titles)
        recommend_first_img.append(imgs)



    # 근처 단체모임하기 좋은 맛집 추천
    random.seed(42)

    recommend_second_id = []
    recommend_second_title = []
    recommend_second_img = []

    for i in range(len(xs)) :
        x_df = food_df[food_df['subway'] == id_subway[i]]
        x_id = list(x_df['id'].unique())
        recommend_second_id.append(random.sample(x_id, 10))

    for i in range(len(recommend_second_id)) :
        titles = []
        imgs = []
        for k in range(len(recommend_second_id[i])) :
            id = recommend_second_id[i][k]
            x_df = food_df[food_df['id'] == id]
            title = list(x_df['title'])[0]
            img = list(x_df['image_place'])[0]
            titles.append(title)
            imgs.append(img)
        recommend_second_title.append(titles)
        recommend_second_img.append(imgs)



    # 근처 술집 추천
    recommend_third_id = []
    recommend_third_title = []
    recommend_third_img = []

    for i in range(len(xs)) :
        x_df = drink_df[drink_df['subway'] == id_subway[i]]
        x_id = list(x_df['id'].unique())
        recommend_third_id.append(random.sample(x_id, 10))

    for i in range(len(recommend_third_id)) :
        titles = []
        imgs = []
        for k in range(len(recommend_third_id[i])) :
            id = recommend_third_id[i][k]
            x_df = drink_df[drink_df['id'] == id]
            title = list(x_df['title'])[0]
            img = list(x_df['image_place'])[0]
            titles.append(title)
            imgs.append(img)
        recommend_third_title.append(titles)
        recommend_third_img.append(imgs)


    recommend_first_list = []

    for k in range(len(recommend_first_id)) :
        recommend_first = list(zip(recommend_first_id[k], recommend_first_title[k], recommend_first_img[k]))
        recommend_first_list.append(recommend_first)


    recommend_second_list = []

    for k in range(len(recommend_second_id)) :
        recommend_second = list(zip(recommend_second_id[k], recommend_second_title[k], recommend_second_img[k]))
        recommend_second_list.append(recommend_second)


    recommend_third_list = []

    for k in range(len(recommend_third_id)) :
        recommend_third = list(zip(recommend_third_id[k], recommend_third_title[k], recommend_third_img[k]))
        recommend_third_list.append(recommend_third)


    df = pd.DataFrame({'id' : xs, 'first_reco' : recommend_first_list, 'second_reco' : recommend_second_list, 'third_reco' : recommend_third_list})

    return df

def dummy_drink(df) :
    food_df = df[df['kind_big'] == '맛집'].reset_index(drop = True)
    cafe_df = df[df['kind_big'] == '카페'].reset_index(drop = True)
    drink_df = df[df['kind_big'] == '술집'].reset_index(drop = True)

    xs = list(drink_df['id'].unique())

    id_subway = []
    for i in range(len(xs)) :
        subway = list(drink_df[drink_df['id'] == xs[i]]['subway'])[0]
        id_subway.append(subway)

    for i in range(len(id_subway)) :
        if id_subway[i] not in ["성수역", "뚝섬역", "서울숲역"] : id_subway[i] = "성수역"

    id_kind = []
    for i in range(len(xs)) :
        kind = list(drink_df[drink_df['id'] == xs[i]]['kind_small'])[0]
        id_kind.append(kind)
    

    # 비슷한 가격대 술집 추천
    recommend_first_id = []
    recommend_first_title = []
    recommend_first_img = []

    for i in range(len(xs)) :
        ys = xs.copy()
        y = ys[i]
        ys.remove(ys[i])
        recommend_first_id.append(random.sample(ys, 10))

    for i in range(len(recommend_first_id)) :
        titles = []
        imgs = []
        for k in range(len(recommend_first_id[i])) :
            id = recommend_first_id[i][k]
            x_df = drink_df[drink_df['id'] == id]
            title = list(x_df['title'])[0]
            img = list(x_df['image_place'])[0]
            titles.append(title)
            imgs.append(img)
        recommend_first_title.append(titles)
        recommend_first_img.append(imgs)


    # 근처 단체 모임하기 좋은 맛집 추천
    recommend_second_id = []
    recommend_second_title = []
    recommend_second_img = []

    for i in range(len(xs)) :
        x_df = food_df[food_df['subway'] == id_subway[i]]
        x_id = list(x_df['id'].unique())
        recommend_second_id.append(random.sample(x_id, 10))

    for i in range(len(recommend_second_id)) :
        titles = []
        imgs = []
        for k in range(len(recommend_second_id[i])) :
            id = recommend_second_id[i][k]
            x_df = food_df[food_df['id'] == id]
            title = list(x_df['title'])[0]
            img = list(x_df['image_place'])[0]
            titles.append(title)
            imgs.append(img)
        recommend_second_title.append(titles)
        recommend_second_img.append(imgs)


    # 주종이 비슷한 술집 추천
    recommend_third_id = []
    recommend_third_title = []
    recommend_third_img = []

    for i in range(len(xs)) :
        x_df = drink_df[drink_df['kind_small'] == id_kind[i]]
        x_id = list(x_df['id'].unique())
        recommend_third_id.append(random.sample(x_id, 10))

    for i in range(len(recommend_third_id)) :
        titles = []
        imgs = []
        for k in range(len(recommend_third_id[i])) :
            id = recommend_third_id[i][k]
            x_df = drink_df[drink_df['id'] == id]
            title = list(x_df['title'])[0]
            img = list(x_df['image_place'])[0]
            titles.append(title)
            imgs.append(img)
        recommend_third_title.append(titles)
        recommend_third_img.append(imgs)


    recommend_first_list = []

    for k in range(len(recommend_first_id)) :
        recommend_first = list(zip(recommend_first_id[k], recommend_first_title[k], recommend_first_img[k]))
        recommend_first_list.append(recommend_first)


    recommend_second_list = []

    for k in range(len(recommend_second_id)) :
        recommend_second = list(zip(recommend_second_id[k], recommend_second_title[k], recommend_second_img[k]))
        recommend_second_list.append(recommend_second)


    recommend_third_list = []

    for k in range(len(recommend_third_id)) :
        recommend_third = list(zip(recommend_third_id[k], recommend_third_title[k], recommend_third_img[k]))
        recommend_third_list.append(recommend_third)


    df = pd.DataFrame({'id' : xs, 'first_reco' : recommend_first_list, 'second_reco' : recommend_second_list, 'third_reco' : recommend_third_list})

    return df

def dummy_func() :
    df = dummy_df()

    df0 = dummy_food(df)
    df1 = dummy_cafe(df)
    df2 = dummy_drink(df)

    dummy = pd.concat([df0, df1, df2], axis = 0).reset_index(drop = True)

    return dummy

