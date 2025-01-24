import time
import schedule
import requests
import datetime

import home_find.models.HouseInfo as HouseInfo
import home_find.constants as constants

from requests.exceptions import Timeout
from django.db import connection


class Main:

    check_queue = None

    def __init__(self):
        pass

    def run(self) -> None:
        """
        run the main program.
        
                
        Returns:
            None
        """
        schedule.every().day.at("00:00").do(
            self.cron_callable, call=self.house_info_store, task_name="HouseInfo Store"
        )
        schedule.every().day.at("01:00").do(
            self.cron_callable, call=self.check_effective, task_name="Check Effective"
        )

        while True:
            schedule.run_pending()
            time.sleep(1)

    def cron_callable(self, call: callable, task_name: str) -> None:
        """
        running a task with a specific name.
        
        Args:
            call (callable): The function to run.
            task_name (str): The name of the task.
        
        Returns:
            None
        """
        try:
            self.printTime()
            print(f"{task_name} is running...")

            call()

            self.printTime()
            print(f"{task_name} is done.")
        except Exception as e:
            print(f"Error occurred during {task_name}: {e}")
        finally:
            connection.close()
            print("Database connection closed.")

    def house_info_store(self) -> None:
        """
        store house information from suumo.jp
        
                
        Returns:
            None
        """
        print("Scrapy is running...")

        scrapy = scrapy.ScrapyMain()
        house_results = scrapy.run()

        for house in house_results:
            if not house.is_in_db():
                house.save()

        print("Scrapy is done.")

    def check_effective(self) -> None:
        """
        check effective houses.
        
                
        Returns:
            None
        """
        print("Checking effective...")
        self.check_queue = list(HouseInfo.objects.filter(deleted_at__isnull=True))

        for _ in range(3):
            for house in self.check_queue:
                url = house.website
                print(f"Checking {url}...")

                self.check_queue.pop(house)
                self.check(url, house)

            time.sleep(30)

        self.printTime()
        print("Checking effective is done.")

        for house in self.check_queue:
            house.delete()

        self.printTime()
        print("Deleted uneffective houses.")

    def check(self, url: str, house: HouseInfo) -> None:
        """
        check a specific house.
        
        Args:
            url (str): The URL of the house to check.
            house (HouseInfo): The HouseInfo object to check.
        
        Returns:
            None
        """
        try:
            response = requests.get(url, headers=constants.HEADERS, timeout=2)

            if response.status_code == 400:
                self.check_queue.append(house)
            elif response.status_code == 301:
                self.check_queue.append(house)
            elif response.status_code == 200:
                pass

        except Timeout:

            print(f"Request to {url} timed out.")
            self.check_queue.append(house)

        except requests.RequestException as e:

            print(f"An error occurred: {e}")
            self.check_queue.append(house)

    def printTime(self) -> None:
        """
        print the current time.
        
                
        Returns:
            None
        """
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
