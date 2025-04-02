import sqlite3
# This function will take in a dictionary, golfer id, points, and will return another dictionary, golfer_id, money
def get_skins_money(scores):
    money = {}
    skins_total = 0

    for _, skins in scores.items():
        skins_total += skins

    for golfer_id, skins in scores.items():
        money[golfer_id] = skins // skins_total
    
    return money