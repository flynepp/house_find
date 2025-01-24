import threading

from django.core.management.base import BaseCommand
from home_find.centralDispatch import main


class Command(BaseCommand):
    help = "this is entrance"

    def handle(self, *args, **options):

        house_info_process = main.Main()
        house_info_process_thread = threading.Thread(target=house_info_process.run)
        house_info_process_thread.daemon = True
        house_info_process_thread.start()
