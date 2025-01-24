import requests

from home_find import constants
from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout, ReadTimeout


class SearchHouseInfo:
    def __init__(self):
        return

    @staticmethod
    def get_house_info(url):
        data = {}

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=constants.HEADERS, timeout=2)
                break
            except (ConnectTimeout, ReadTimeout):
                print(f"Attempt {attempt + 1} failed. Retrying...")
        else:
            # 此物件被归档，标记为失败
            print("All retries failed.")
            data["success"] = False
            return data

        if response.status_code == 200:
            # 页面正常，开始解析
            soup = BeautifulSoup(response.text, "html.parser")

            data["success"] = True

            # 详细信息提取
            items = soup.find_all("div", class_="property_data")
            for item in items:
                if "向き" in item.text:
                    soup = BeautifulSoup(str(item), "html.parser")
                    data["direction"] = soup.find(
                        "div", class_="property_data-body"
                    ).text.strip()

                if "建物種別" in item.text:
                    soup = BeautifulSoup(str(item), "html.parser")
                    data["type"] = soup.find(
                        "div", class_="property_data-body"
                    ).text.strip()

        elif response.status_code == 404:
            #  此物件被删除，标记为失败
            data["success"] = False

        return data
