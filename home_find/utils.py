import numpy as np
from home_find.constants import EARTH_RADIUS


# 获取中心点右上角以及左下角经纬度坐标
def get_position(center, distance):
    lat, lng = center

    # 转换经纬度为弧度
    lat, lng = np.radians(lat), np.radians(lng)

    # 计算对角线距离（公里）
    diagonal_distance = distance

    # 计算纬度和经度的偏移量（单位：弧度）
    lat_offset = diagonal_distance / EARTH_RADIUS
    lng_offset = diagonal_distance / (EARTH_RADIUS * np.cos(lat))

    # 计算右上角和左下角经纬度（弧度）
    upper_right_lat = lat + lat_offset
    upper_right_lng = lng + lng_offset
    lower_left_lat = lat - lat_offset
    lower_left_lng = lng - lng_offset

    # 转换结果为角度
    return [
        float(np.degrees(upper_right_lat)),  # 右上角纬度
        float(np.degrees(upper_right_lng)),  # 右上角经度
        float(np.degrees(lower_left_lat)),  # 左下角纬度
        float(np.degrees(lower_left_lng)),  # 左下角经度
    ]


# 计算距离
def distance_to_center(center, latitude, longitude):
    lat1 = np.radians(center[0])
    lon1 = np.radians(center[1])
    lat2 = np.radians(latitude)
    lon2 = np.radians(longitude)

    # 哈弗辛公式
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        np.sin(delta_lat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2) ** 2
    )
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    # 计算距离（单位：公里）
    distance = EARTH_RADIUS * c

    return float(distance * 1000)  # 单位：米
