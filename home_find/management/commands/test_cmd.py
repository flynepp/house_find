# home_find/management/commands/test_cmd.py
import requests
import json

import home_find.mail.sendMail as SendMail

from django.core.management.base import BaseCommand
from home_find.scrapy.scrapy_main import ScrapyMain
from home_find import constants, conditions
from home_find.models import HouseInfo
from home_find.centralDispatch import main



class Command(BaseCommand):
    help = "打印测试命令"

    def handle(self, *args, **options):

        print("")

        mail = SendMail.SendMail()
        mail.send()

        print(1)
