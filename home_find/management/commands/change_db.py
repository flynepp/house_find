import re
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "change database"
    pattern = r"(?P<start>###---database_config).*?(?P<end>###---database_config)"

    def handle(self, *args, **options):
        print("")
        print("change database")
        print("")
        database = input(
            "Enter the name of the database you want to change to(sqlite/mysql): \n"
        )
        print("")
        if database == "sqlite":
            print("changing to sqlite")

            text = """
            database_config = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }
            """
            self.replace_text(text)

        elif database == "mysql":
            print("changing to mysql")
            host = input("Enter the host name: \n")
            port = input("Enter the port number: \n")
            user = input("Enter the user name: \n")
            password = input("Enter the password: \n")
            database_name = input("Enter the name of the database: \n")

            text = f"""
            database_config = {{
                'default': {{
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': '{database_name}',
                    'USER': '{user}',
                    'PASSWORD': '{password}',
                    'HOST': '{host}',
                    'PORT': '{port}',
                }}
            }}
            """
            self.replace_text(text)

        else:
            print("Invalid input")
            return 0

    def replace_text(self, replace_text: str) -> int:
        with open("home_find/constants.py", "r+") as f:
            content = f.read()
            result = re.sub(
                self.pattern,
                rf"\1\n{replace_text.strip()}\n\2",
                content,
                flags=re.DOTALL,
            )
            f.seek(0)
            f.write(result)
            f.truncate()

        return 1
