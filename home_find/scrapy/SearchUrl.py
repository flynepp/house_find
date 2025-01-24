import requests
import re
import json

from bs4 import BeautifulSoup
from urllib.parse import urlencode
from home_find import get_position
from home_find import constants, conditions


class SearchUrl:

    def __init__(self):
        # 基础url
        self.BASE_URL = constants.BASE_URL
        self.BASE_CONDITION = constants.BASE_CONDITION

        # 搜索条件
        self.conditions = {
            key: getattr(conditions, key)
            for key in dir(conditions)
            if not key.startswith("__")
        }
        self.conditions.update(
            {"LTLG": [constants.COMPANY_LATITUDE, constants.COMPANY_LONGITUDE]}
        )

        # 请求头
        self.headers = constants.HEADERS

    def get_url(self, condition):
        # 基础条件拼接
        api = self.get_base_condition()
        self.BASE_CONDITION = {**self.BASE_CONDITION, **api}

        query_string = urlencode(self.BASE_CONDITION)
        url = f"{self.BASE_URL}{query_string}"

        # 位置条件处理，从中心坐标+距离计算出对角线坐标
        condition = condition or self.conditions
        [KUKEIPT1LT, KUKEIPT1LG, KUKEIPT2LT, KUKEIPT2LG] = get_position(
            condition["LTLG"], condition["DISTANCE"]
        )
        condition.update(
            {
                "KUKEIPT1LT": KUKEIPT1LT,
                "KUKEIPT1LG": KUKEIPT1LG,
                "KUKEIPT2LT": KUKEIPT2LT,
                "KUKEIPT2LG": KUKEIPT2LG,
            }
        )

        # 全局变量更新
        conditions.DISTANCE = condition["DISTANCE"]
        constants.COMPANY_LATITUDE = condition["LTLG"][0]
        constants.COMPANY_LONGITUDE = condition["LTLG"][1]

        # 搜索条件更新
        condition.pop("LTLG")
        condition.pop("DISTANCE")

        # 搜索条件拼接
        query_string = urlencode(condition, doseq=True)
        url = f"{url}&{query_string}"

        return url

    # 获取UID, STMP, ATT
    def get_base_condition(self):
        url = "https://suumo.jp/map/tokyo/sc_nakano/"

        response = requests.get(url, headers=self.headers)
        text = response.text
        soup = BeautifulSoup(text, "html.parser")
        scripts = soup.find_all("script")

        for script in scripts:
            if "suumo.ApiParam" in script.text:
                text = script.text

        match = re.search(r"suumo\.ApiParam\s*=\s*(\{.*?\});", text, re.DOTALL)
        api_param = match.group(1)
        api_param = json.loads(api_param.replace("'", '"'))
        api = api_param["bkApi"]
        api.pop("url")

        return api
