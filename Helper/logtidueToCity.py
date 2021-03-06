# -*- coding: utf-8 -*-
import http.client
import json
import logging

from pip._vendor.retrying import retry

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_conn():

    conn = http.client.HTTPConnection("api.map.baidu.com")

    return conn



def update_city_info(dict, start, total, core_number, myDict, lock):
    i = (start-1)*total/core_number
    logger.info("%s 线程, 编号： %s", start, i)
    conn = get_conn()
    dicUpdated = []
    n = 0
    while (i < start*total/core_number):
        if i == 0:
            i = i + 1
            continue
        dicData = dict.get(str(int(i)))
        i = i+1
        n = n + 1
        long, lat = dicData.get('geo_info').split(",")
        city = convert_lat_long_to_city(conn, long, lat)
        dicData["city"] = city
        dicUpdated.append(dicData)

    logger.info("%s 线程, 进度： %s", start, n)
    lock.acquire()
    myDict.extend(dicUpdated)
    lock.release()
    conn.close()


def update_city_info_normal(dict, total):

    logger.info("start update city info without mp")
    conn = get_conn()
    dicUpdated = []
    n = 0
    i = 0
    while (i < total):
        if i == 0:
            i = i + 1
            continue
        dicData = dict.get(str(int(i)))
        i = i+1
        n = n + 1
        long, lat = dicData.get('geo_info').split(",")
        print(long, lat)
        print(i)
        try:
            city = convert_lat_long_to_city(conn, long, lat)
        except :
            logger.info("retry error")
            dicData["city"] = None
            dicUpdated.append(dicData)
            continue

        dicData["city"] = city
        dicUpdated.append(dicData)

    conn.close()
    return dicUpdated




def retry_if_result_none(result):
    return result is "Null"

@retry(retry_on_result=retry_if_result_none, stop_max_attempt_number=40)
def convert_lat_long_to_city(conn, long, lat):

    url = "/geocoder?output=json&location={},{}&key=1qwNjPIb8UmwZdA7owlopzgjNI0Sov7j".format(str(lat), str(long))
    conn.request("GET", url)
    res = conn.getresponse()
    data = res.read()
    try:
        dict = json.loads(data.decode("utf-8"))
    except json.decoder.JSONDecodeError as e:
        return "Null"

    city = dict.get('result').get('addressComponent').get('city')


    return city
