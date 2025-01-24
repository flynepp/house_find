import requests
import json

from datetime import datetime

from home_find.scrapy.SearchUrl import SearchUrl
from home_find.scrapy.SearchHouseInfo import SearchHouseInfo
from home_find import constants, conditions
from home_find.models import HouseInfo


class ScrapyMain:

    def __init__(self):
        return

    def run(self, condition=None):
        # 房屋信息爬取,时间记录
        startTime = datetime.now()
        print("")
        print("------------------------start scrapy------------------------")
        print("start time:", startTime)

        search_url = SearchUrl()
        url = search_url.get_url(condition)

        response = requests.get(url, headers=constants.HEADERS)
        if response.status_code == 200:
            temp = json.loads(response.text)

            if temp["smatch"]["resultset"]["hits"] == 0:
                print(f"no houses found")
                return False

        else:
            print(f"data catch failed, status code: {response.status_code}")
            return False

        print(f"data catch success, total: {temp['smatch']['resultset']['hits']}")
        results = temp["smatch"]["resultset"]["item"]
        home_result = []

        for result in results:
            house_info = HouseInfo()

            # 获取详细信息
            info = SearchHouseInfo.get_house_info(result["link"])

            data = {
                "house_id": result["bukken_cd"],
                "name": result["bukken_nm"],
                "address": result["jusho"],
                "price": int(float(result["kakaku"].replace("万円", "")) * 10000)
                + (
                    0
                    if result["kanrihi"].replace("円", "") == "-"
                    else int(result["kanrihi"].replace("円", "").replace(",", ""))
                ),
                "area": result["menseki"].replace("平米", ""),
                "type": result["madori"],
                "age": result["chikugonensu"].replace("年", ""),
                "latitude": result["lt"],
                "longitude": result["lg"],
                "website": result["link"],
                "reikin": (
                    0
                    if result["reikin"] == "-"
                    else int(float(result["kakaku"].replace("万円", "")) * 10000)
                ),
                "shikikin": (
                    0
                    if result["shikikin"] == "-"
                    else int(float(result["kakaku"].replace("万円", "")) * 10000)
                ),
            }

            data.update(info)

            house_info.fill(data)

            if house_info.distance > (conditions.DISTANCE * 1000):
                pass

            home_result.append(house_info)

        endTime = datetime.now()
        print("end time:", endTime)
        print("total time:", endTime - startTime)
        print("------------------------end scrapy------------------------")

        return home_result
