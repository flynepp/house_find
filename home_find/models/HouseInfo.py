import home_find.constants
import json
from django.db import models
from home_find import distance_to_center


class HouseInfo(models.Model):
    house_id = models.BigIntegerField(null=True, help_text="网站id")
    name = models.CharField(max_length=100, null=True, help_text="名称")
    address = models.CharField(max_length=100, null=True, help_text="地址")
    price = models.IntegerField(null=True, help_text="租金")
    price_cal = models.IntegerField(null=True, help_text="租金(补贴后)")
    area = models.FloatField(null=True, help_text="面积")
    type = models.CharField(max_length=8, null=True, help_text="户型")
    direction = models.CharField(max_length=8, null=True, help_text="朝向")
    floor = models.IntegerField(null=True, help_text="楼层")
    age = models.IntegerField(null=True, help_text="年代")
    latitude = models.FloatField(null=True, help_text="纬度")
    longitude = models.FloatField(null=True, help_text="经度")
    distance = models.FloatField(null=True, help_text="距离")
    website = models.CharField(max_length=100, null=True, help_text="网站")
    reikin = models.IntegerField(null=True, help_text="礼金")
    shikikin = models.IntegerField(null=True, help_text="保证金")
    first_money = models.IntegerField(null=True, help_text="首付")
    comment = models.CharField(max_length=200, null=True, help_text="评论")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新时间")
    deleted_at = models.DateTimeField(null=True, help_text="删除时间")

    # 重写__str__方法，返回房源信息的json字符串
    def __str__(self):
        house_info_dict = {}

        for field in self._meta.fields:
            field_name = field.name
            field_value = getattr(self, field_name)

            if field_value is None:
                house_info_dict[field_name] = None
            else:
                house_info_dict[field_name] = field_value

        return json.dumps(house_info_dict, indent=4, default=str, ensure_ascii=False)

    # 填充房源信息
    def fill(self, data):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")

        # 距离计算
        center = [
            home_find.constants.COMPANY_LATITUDE,
            home_find.constants.COMPANY_LONGITUDE,
        ]
        distance = distance_to_center(center, data["latitude"], data["longitude"])
        data["distance"] = distance

        # 补贴计算
        if home_find.constants.USEALLOWANCE:
            if distance < home_find.constants.ALLOWANCE_LEVEL_1_DISTANCE:
                data["price_cal"] = data["price"] - home_find.constants.ALLOWANCE_LEVEL_1
            else:
                data["price_cal"] = data["price"] - home_find.constants.ALLOWANCE_LEVEL_2

        # 初期费用估算
        data["first_money"] = (
            data["price"] * home_find.constants.INITIAL_FEE_RATE
            + data["reikin"]
            + data["shikikin"]
        )

        for key, value in data.items():
            setattr(self, key, value)

        print(f"house_id: {self.house_id} got")

    # 保存房源信息
    def save(self, *args, **kwargs):
        """
        save house info to database
        
        Args:
            *args:
            **kwargs:
        
        Returns:
            None
        """
        super(HouseInfo, self).save(*args, **kwargs)
        print(f"house_id: {self.house_id} saved")

    # 查询房源信息
    def query_by_id(self, house_id):
        return self.objects.filter(house_id=house_id).first()

    # 删除房源信息
    def delete_by_id(self, house_id):
        return self.objects.filter(house_id=house_id).delete()

    def is_in_db(self):
        """
        判断当前 house_id 是否已存在于数据库
        """
        if not self.house_id:
            raise ValueError("house_id is required for this check.")
        return type(self).objects.filter(house_id=self.house_id).exists()
