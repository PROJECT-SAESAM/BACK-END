from enum import Enum



class schemaconfig(Enum) :
    downloadschemaname = ["merged", "keyword", "recommend"]



class parseconfig(Enum) :
    parselist = ["info", "kind", "dist", "menu", "review"]



class analyticsconfig(Enum) :
    keywordlist = ["saesamkeyword", "naverkeyword"]
    recommendlist = []


class recommendtextconfig(Enum) :
    rest = {
        'first_reco' : '비슷한 가격대의 맛집',
        'second_reco' : '식사 후 방문하기 좋은 근처 카페', 
        'third_reco' : '2차로 가기 좋은 근처 술집'}
    cafe = {
        'first_reco' : '혼밥하기 좋은 근처 맛집', 
        'second_reco' : '단체 모임하기 좋은 근처 맛집', 
        'third_reco' : '단체 모임하기 좋은 근처 술집'
    }
    drink = {
        'first_reco' : '비슷한 가격대의 술집',
        'second_reco' : '1차로 가기 좋은 근처 맛집',
        'thrid_reco' : '주종이 비슷한 술집'
    }