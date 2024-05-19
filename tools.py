import os
from difflib import SequenceMatcher


def count_average(query):
    summary = 0
    counter = 0
    for i in query:
        summary += i.rating
        counter += 1
    return round(summary / counter, 2)


def similar(p1, p2):
    return SequenceMatcher(None, p1, p2).ratio()


def get_photos_from_id(id, mode):
    try:
        arr = os.listdir(f'static/photos/{mode}/{id}')
        arr = list(map(lambda x: f'static/photos/{mode}/{id}/{x}', arr))
        return arr
    except Exception as ex:
        return []
