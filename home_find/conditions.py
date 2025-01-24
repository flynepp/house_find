#     # 租金相关条件(string)
#     "CJOKEN": [         # 賃料条件(list)
#         "1",  # 包含管理费
#         "2",  # 包含停车费
#         "3",  # 无礼金
#         "4",  # 无保证金
#         "5",  # 无其余初期费用
#     ],
#     "SJOKEN": [         # 賃料条件2(list)
#         "040086",  # 租金可信用卡
#         "040085",  # 初期费用可信用卡
#     ],
#     "CHINRYOMIN": None, # 租金范围下限(单位：万, start:3, step:0.5) 不填则不指定
#     "CHINRYOMAX": None, # 租金范围上限(单位：万, end:40, step:0.5) 不填则不指定
#
#     # 搜索区域范围
#     "KUKEIPT1LT": None, # 搜索区域右上角 纬度
#     "KUKEIPT1LG": None, # 搜索区域右上角 经度
#     "KUKEIPT2LT": None, # 搜索区域左下角 纬度
#     "KUKEIPT2LG": None, # 搜索区域左下角 经度
#     "DISTANCE": 2,      # 搜索区域半径(单位：公里)
#
#     # 面积相关条件
#     "FR_SENYUMENMIN": None, # 面积范围下限(单位：平方米, start:20, step:5) 不填则不指定
#     "FR_SENYUMENMAX": None, # 面积范围上限(单位：平方米, end:100, step:5) 不填则不指定
#
#     # 年限条件
#     "CINCN": None,      # 年限: 0, 1, 3, 5 ,10, 15, 20, 30 不填则不指定
#
#     # 建筑类型
#     "TSHURUI": [        # 建筑类型(list)
#         "1",  # mansion
#         "2",  # apartment
#         "3",  # house
#     ],
#
#     # 户型条件
#     "CINM": [           # 户型(list)
#         "01", # "one_room",
#         "02", # "1K",
#         "03", # "1DK",
#         "04", # "1LDK",
#         "05", # "2K",
#         "06", # "2DK",
#         "07", # "2LDK",
#         "08", # "3K",
#         "09", # "3DK",
#         "10", # "3LDK",
#         "11", # "4K",
#         "12", # "4DK",
#         "13", # "4LDK",
#         "14", # "over5K",
#     ],

CJOKEN = ["1"]
DISTANCE = 2
CHINRYOMAX = "12"
FR_SENYUMENMIN = "25"
TSHURUI = ["1"]
