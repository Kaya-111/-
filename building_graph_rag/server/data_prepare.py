import pandas as pd
import glob

# 数据1：宫廷典制_故宫博物院
d1 = pd.read_csv("docs/宫廷典制_故宫博物院.csv", encoding="gb18030")
d1 = d1[["名称", "介绍"]]

# 数据2：宫廷世系_故宫博物院
d2 = pd.read_csv("docs/宫廷世系_故宫博物院.csv", encoding="gb18030")
d2 = d2[["人物", "介绍", "关键词", "事件"]]

# 数据3: 宫俗文化_故宫博物院
d3 = pd.read_csv("docs/宫俗文化_故宫博物院.csv", encoding="gb18030")
d3 = d3[["名称", "介绍"]]

# 数据4: 建筑_故宫博物院
d4 = pd.read_csv("docs/建筑_故宫博物院.csv", encoding="gb18030")
d4 = d4[["建筑名称", "年代", "分类.1", "区域"]]

# 数据5: 宫廷人物_故宫博物院
d5 = pd.read_csv("docs/宫廷人物_故宫博物院.csv", encoding="gb18030")
d5 = d5[["人物", "介绍"]]

# 数据6：宫廷事件_故宫博物院
d6 = pd.read_csv("docs/宫廷事件_故宫博物院.csv", encoding="gb18030")
d6 = d6[["事件名称", "介绍", "关键词"]]

# 数据7：藏品_故宫博物院
d7 = pd.read_csv("docs/藏品_故宫博物院.csv", encoding="gb18030")
d7 = d7[["文物分类", "名称", "介绍", "关键词"]]

# 数据8：古籍
d8 = pd.read_csv("docs/古籍.csv", encoding="gb18030")

with open("docs/raw_data.txt", "w", encoding="utf-8") as f:
    for _, row in d1.iterrows():
        f.write(row["名称"] + "。" + row["介绍"] + "\n")
    
    for _, row in d2.iterrows():
        f.write(str(row["人物"]) + "," + str(row["介绍"]) + "," + str(row["关键词"]) + "," + str(row["事件"]) + "\n")

    for _, row in d3.iterrows():
        f.write(str(row["名称"]) + "," + str(row["介绍"]) + "\n")
    
    for _, row in d4.iterrows():
        f.write(str(row["建筑名称"]) + "," + str(row["年代"]) + "," + str(row["分类.1"]) + "," + str(row["区域"]) + "\n")
    
    for _, row in d5.iterrows():
        f.write(str(row["人物"]) + "," + str(row["介绍"]) + "\n")
    
    for _, row in d6.iterrows():
        f.write(str(row["事件名称"]) + "," + str(row["介绍"]) + "," + str(row["关键词"]) + "\n")

    for _, row in d7.iterrows():
        f.write(str(row["文物分类"]) + "," + str(row["名称"]) + "," + str(row["介绍"]) + "," + str(row["关键词"]) + "\n")
    
    for _, row in d8.iterrows():
        f.write(str(row["古籍类型"]) + "," + str(row["古籍名称"]) + "," + str(row["古籍介绍"]) + "," + str(row["古籍关键词"]) + "\n")

