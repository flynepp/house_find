import openpyxl
import mysqlclient
import black

openpyxl.load_workbook("output.xlsx")
mysqlclient.connect()
black.format_file("temp.py")