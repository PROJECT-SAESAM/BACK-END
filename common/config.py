from enum import Enum



class schemaconfig(Enum) :
    downloadschemaname = ["merged", "keyword", "recommend"]



class parseconfig(Enum) :
    parselist = ["info", "kind", "dist", "menu", "review"]



class analyticsconfig(Enum) :
    keywordlist = ["saesamkeyword", "naverkeyword"]
    recommendlist = []