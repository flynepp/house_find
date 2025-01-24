from django.core.management.base import BaseCommand
from home_find.scrapy.scrapy_main import ScrapyMain
from home_find.panda.ToExcel import ToExcel
from home_find import distance_to_center


class Command(BaseCommand):
    help = "导出房源信息为xlsx文件"

    def handle(self, *args, **options):

        print("")

        print("")
        setting = input("是否采用默认设置(参考conditions.py)? (y/n)\n")

        if setting == "y":
            print("采用默认设置")
            conditions = None

        elif setting == "n":
            print("自定义设置")

            print("\n请输入租房中心点 (必填):")
            LTLG = self.get_required_input(
                "(经纬度, 以逗号分隔, 精度: 高一点, googlemap 右键可以复制坐标, 如: 31.23456,121.456789)\n",
                lambda x: [float(i) for i in x.split(",")],
                "输入不能为空，请重新输入",
            )
            print("中心点坐标:", LTLG)

            DISTANCE = self.get_required_input(
                "\n请输入距中心点距离 (必填, 单位: km):\n",
                float,
                "输入不能为空，请重新输入",
            )
            print("距离:", DISTANCE)

            CJOKEN = self.get_optional_input(
                "\n请输入租房条件 (以逗号分隔, 可选条件有 1:包含管理费, 2:包含停车费, 3:无礼金, 4:无保证金, 5:无其余初期费用, 不填则默认无条件)\n",
                lambda x: [i for i in x.split(",") if i in {"1", "2", "3", "4", "5"}],
            )
            print("条件:", CJOKEN or "无条件")

            FR_SENYUMENMIN = self.get_optional_input(
                "\n面积不低于 (单位: 平米, 最高100, 最低20, 间隔5, 不填则默认无面积限制):\n",
                int,
            )
            print("面积不低于:", FR_SENYUMENMIN or "无面积限制")

            FR_SENYUMENMAX = self.get_optional_input(
                "\n面积不高于 (单位: 平米, 最高100, 最低20, 间隔5, 不填则默认无面积限制):\n",
                int,
            )
            print("面积不高于:", FR_SENYUMENMAX or "无面积限制")

            TSHURUI = self.get_optional_input(
                "\n建筑类型 (1:公寓, 2:别墅, 3:普通住宅, 不填则默认无建筑类型限制):\n",
                lambda x: [i for i in x.split(",") if i in {"1", "2", "3"}],
            )
            print("建筑类型:", TSHURUI or "无建筑类型限制")

            CINCN = self.get_optional_input(
                "\n年限 (请输入 0, 1, 3, 5, 10, 15, 20, 30, 不填则不指定):\n", int
            )
            print("年限:", CINCN or "无年限限制")

            CHINRYOMAX = self.get_optional_input(
                "\n月租金不高于 (单位: 万, 最高40, 最低3, 间隔0.5, 不填则默认无价格限制):\n",
                float,
            )
            print("月租金不高于:", CHINRYOMAX or "无价格限制")

            CHINRYOMIN = self.get_optional_input(
                "\n月租金不低于 (单位: 万, 最高40, 最低3, 间隔0.5, 不填则默认无价格限制):\n",
                float,
            )
            print("月租金不低于:", CHINRYOMIN or "无价格限制")

            conditions = {
                "LTLG": LTLG,
                "DISTANCE": float(DISTANCE),
                "CJOKEN": CJOKEN,
                "FR_SENYUMENMIN": FR_SENYUMENMIN,
                "FR_SENYUMENMAX": FR_SENYUMENMAX,
                "TSHURUI": TSHURUI,
                "CINCN": CINCN,
                "CHINRYOMIN": CHINRYOMIN,
                "CHINRYOMAX": CHINRYOMAX,
            }

            conditions = {key: value for key, value in conditions.items() if value}

        else:
            print("输入错误，请重新输入")
            return

        print("")

        scrapy_main = ScrapyMain()
        home_infos = scrapy_main.run(conditions)

        if not home_infos:
            print("未找到房源信息")
            return

        ToExcel.export_excel(home_infos, True)
        print("导出成功")

    def get_required_input(prompt: str, parse_fn: callable, error_message: str) -> any:
        """
        获取用户输入，确保不为空，并使用指定的解析函数解析。

        :param prompt: 提示信息
        :param parse_fn: 解析函数
        :param error_message: 出错时的提示信息
        :return: 解析后的输入值
        """
        while True:
            user_input = input(prompt)
            if not user_input:
                print(error_message)
                continue
            try:
                return parse_fn(user_input)
            except Exception as e:
                print(f"输入无效: {e}")

    def get_optional_input(prompt: str, parse_fn: callable=None) -> any:
        """
        获取用户输入，如果为空则返回 None。

        :param prompt: 提示信息
        :param parse_fn: 解析函数（可选）
        :return: 解析后的输入值或 None
        """
        user_input = input(prompt)
        if not user_input:
            return None
        return parse_fn(user_input) if parse_fn else user_input
