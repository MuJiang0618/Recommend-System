import os
import math

def getUserClick(rating_file):
    """
    Return:  用户喜欢的电影集合
    a dict: Key userId Value [movieId, movieId]
    """

    if not os.path.exists(rating_file):
        return {}

    fp = open(rating_file)
    num = 0
    user_click = {}
    for line in fp:
        if num == 0:
            num += 1
            continue

        item = line.strip().split(',')
        
        if len(item) < 4:  #信息不全的条目直接丢弃
            continue

        if float(item[2]) < 3.0:
            continue         #用户评分<3则丢弃

        if item[0] not in user_click.keys():  #如果该用户还未被添加
            user_click[item[0]] = []

        user_click[item[0]].append(item[1])

    fp.close()

    return user_click

def getItemInfo(item_file):
    """
    Return:每一部电影的类型
        a dict:key itemid, value:[title, genres]
    """

    if not os.path.exists(item_file):
        return {}

    num = 0
    fp = open(item_file)
    itemInfo = {}
    for line in fp:
        if num == 0:
            num += 1
            continue

        itemList = line.strip().split(',')
        print(itemList)
        if len(itemList) < 3:
            continue
        
        if len(itemList) == 3:
            [itemid_i, title, genres] = itemList

        elif len(itemList) > 3:
            itemid_i = itemList[0]
            genres = itemList[-1]
            title = ''.join(itemList[1:-1])

        if itemid_i not in itemInfo:
            itemInfo[itemid_i] = [title, genres]

    fp.close()
    return itemInfo

def calItemSim(user_click):
    #得到电影之间的相似度
    #这里电影之间的相似度根据两部电影被多少用户同时喜欢
    co_appear = {}      #同时喜欢电影i,j的用户数
    item_user_click_times = {}
    for user, itemList in user_click.items():
        for index_i in range(0, len(itemList)):
            itemid_i = itemList[index_i]
            item_user_click_times.setdefault(itemid_i, 0)
            item_user_click_times[itemid_i] += 1   #记录喜欢电影i的用户数

            for index_j in range(index_i + 1, len(itemList)):
                itemid_j = itemList[index_j]

                co_appear.setdefault(itemid_i, {})
                co_appear[itemid_i].setdefault(itemid_j, 0)
                co_appear[itemid_i][itemid_j] += 1

                co_appear.setdefault(itemid_j, {})
                co_appear[itemid_j].setdefault(itemid_i, 0)
                co_appear[itemid_j][itemid_i] += 1

    item_sim_score = {}; item_sim_score_sorted = {}
    for itemid_i, relate_item in co_appear.items():
        for itemid_j, co_time in relate_item.items():
            sim_score = co_time / math.sqrt(item_user_click_times[itemid_i] + item_user_click_times[itemid_j])
            item_sim_score.setdefault(itemid_i, {})
            item_sim_score[itemid_i].setdefault(itemid_j, 0)
            item_sim_score[itemid_i][itemid_j] = sim_score

    for itemid in item_sim_score:
        item_sim_score_sorted[itemid] = sorted(item_sim_score[itemid].items(), key = \
            lambda x:x[1], reverse = True)

    return item_sim_score_sorted

def result(sim_info, user_click):
    topN = 5
    recom_info = {}
    for user in user_click:
        click_list = user_click[user]
        recom_info.setdefault(user, {})
        for itemid in click_list[: 3]:
            if itemid not in sim_info:
                continue

            for itemsimzuhe in sim_info[itemid][:topN]:
                itemsimid = itemsimzuhe[0]
                itemsimscore = itemsimzuhe[1]
                recom_info[user][itemsimid] = itemsimscore

    return recom_info

if __name__ == '__main__':
    user_click = getUserClick(r'D:\dataSet\movielens\ratings.csv')
    sim_info = calItemSim(user_click)
    recom_result = result(sim_info, user_click)
    print(recom_result['1'])