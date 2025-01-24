

# 搜索中心点
COMPANY_LONGITUDE = 139.682125122186
COMPANY_LATITUDE = 35.696714545066214

# km
EARTH_RADIUS = 6371

# 补助相关
USEALLOWANCE = True
ALLOWANCE_LEVEL_1_DISTANCE = 1500
ALLOWANCE_LEVEL_1 = 40000
ALLOWANCE_LEVEL_2 = 20000

# 初期费用系数
INITIAL_FEE_RATE = 2.5

BASE_CONDITION = {
    "FORMAT": "1",
    "CALLBACL": "SUUMO.CALLBACK.FUNCTION",
    "P": "1",
    "CNT": "1998",
    "GAZO": "2",
    "PROT": "1",
    "SE": "040",
}

BASE_URL = "https://suumo.jp/jj/JJ903FC020/?"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

###---database_config
database_config = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "home_find",
        "USER": "Elaina",
        "PASSWORD": "Elaina",
        "HOST": "192.168.1.175",
        "PORT": "42356",
    }
}
###---database_config

EMAIL="z861092684@gmail.com"
MAILPASS = "rcrdbuojyoufpjbk"
