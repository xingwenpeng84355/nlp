import csv
import logging
import json
import os
from logtidueToCity import convert_lat_long_to_city, get_conn


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


#nameForSaving = "/first{}Output2020-01GeoInfo.json".format(maxiMum)
#nameForSaving = "/first{}Output2020-03.json".format(maxiMum)

def csvLoader(path, maxiMum, mode, GEOINFO):

    logger.info("Start loading csv files in %s with mode %s, geoinfo only?: %s", path, mode, GEOINFO)
    contentInCsv = []
    countNumberOfWbWithGeoInfo = 0
    count = 0
    with open(path, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            count = count + 1
            if count == maxiMum and mode == "limited":
                break
            rowDic = {}
            rowDic['geo_info'] = row[9]
            rowDic['_id'] = row[0]
            rowDic['user_id'] = row[1]
            rowDic['crawl_time'] = row[2]
            rowDic['created_at'] = row[3]
            rowDic['like_num'] = row[4]
            rowDic['repost_num'] = row[5]
            rowDic['comment_num'] = row[6]
            rowDic['content'] = row[7]
            rowDic['origin_weibo'] = row[8]


            if not GEOINFO:
                contentInCsv.append(rowDic)

            if len(rowDic['geo_info']) >= 2:
                countNumberOfWbWithGeoInfo = countNumberOfWbWithGeoInfo +1
                if GEOINFO:
                    contentInCsv.append(rowDic)


    logger.info("The total number of weibos in {} is {}, {} found with geoinfo({}%)".format(path, count, countNumberOfWbWithGeoInfo, countNumberOfWbWithGeoInfo/count*100))
    return contentInCsv



def saveDicToJson(sourceFile, name):

    logger.info("Start saving to Json: %s ", name)
    ouput = {}
    count = 0
    for row in sourceFile:
        ouput[count] = row
        count = count+1
    dir = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/Output"
    if not os.path.exists(dir):
        logger.info("Creating dir %s", dir)
        os.makedirs(dir)
    try:
        finalPath = dir + name
        logger.info("Final path to save is %s", finalPath)
        with open(finalPath, "w") as f:
            f.write(json.dumps(ouput))
    except FileNotFoundError as e:
        logger.error(e)

def loadJsonToDict(path):
    logger.info("Start transfering json file to csv")
    with open(path, 'r', encoding='utf8')as fp:
        dictData = json.load(fp)
        return dictData




def main():





    #contentInCsv = csvLoader(sourFilePath, maxiMum, UNLIMITED, GEOINFO)

    #saveDicToJson(contentInCsv, nameForSaving)

    #loadJsonToDict("/Users/xingwenpeng/PycharmProjects/nlp/Output/first1000Output2020-01.json")





    convert_lat_long_to_city(get_conn, lat, long)



if __name__ == "__main__":
    # execute only if run as a script
    main()