# Presence Detection 0x00 0x18
import base64
import requests
import json
from loguru import logger

heat_map_url_pre =  "http://localhost:8080"
import struct


def bytes_to_float(bytes):
    return struct.unpack('>f', bytes)[0]  # 大端序，单精度


def bytes_to_int(bytes):
    return struct.unpack('>i', bytes)[0]  # 大端序，单精度


def read_http_person_List_new(rangeBinStepList):
    """"
    presenceTag_data: int类型数据的人存
    presenceRange_data：float类型数据的距离
    presenceEn_data：float类型的能量
    rangeBinStep：200个值
    [0]:200个值
    [1]:人存
    [2]:距离
    [3]:能量
    """
    rangeBinMap_list = []
    rangeBinPerson_list = []
    rangeBinRange_list = []
    rangeBinEn_list = []
    for n in rangeBinStepList:
        rawData = base64.b64decode(n['data'])
        rangeBinMap = []
        presenceTag = rawData[0:4]  # int
        presenceRange = rawData[4:8]  # float
        presenceEn = rawData[8:12]  # float
        presenceTag_data = bytes_to_int(presenceTag)
        presenceRange_data = bytes_to_float(presenceRange)
        presenceEn_data = bytes_to_float(presenceEn)
        rangeBinStep = rawData[12:]
        for d in rangeBinStep:
            rangeBinMap.append(int(d))
        rangeBinMap_list.append(rangeBinMap)
        rangeBinPerson_list.append(presenceTag_data)
        rangeBinRange_list.append(presenceRange_data)
        rangeBinEn_list.append(presenceEn_data)
    return rangeBinMap_list, rangeBinPerson_list, rangeBinRange_list, rangeBinEn_list


def get_person_data(radar_uuid, start_time, end_time):
    """
       获取人存数据
       :return:
       [
           {radarUuid,radarType},
           {radarUuid,radarType},
           {radarUuid,radarType},
           {radarUuid,radarType},
           {radarUuid,radarType},
       ]
       """
    try:
        url = heat_map_url_pre + "/common/listPresenceDetectionByRange/" + radar_uuid + "/" + start_time + "/" + end_time
        req = requests.get(url, timeout=(30, 120))
        result = json.loads(req.content)
        if len(result) > 0:
            # 成功
            return result
        else:
            return []
    except Exception as error:
        logger.error("获取雷达列表:" + str(url) + "错误信息" + str(error))
        return []



if __name__ == "__main__":
    rangeBinStepList = get_person_data("000000000000000000000000", "20231123140000", "20231124220000")  #
    rangeBinMap_list, rangeBinPerson_list, rangeBinRange_list, rangeBinEn_list = read_http_person_List_new(rangeBinStepList)
