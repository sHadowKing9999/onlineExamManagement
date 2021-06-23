from datetime import date
today = date.today()
print("Today's date:", today,today.day,today.month,today.year)
"""Imports the datetime package from the Python library"""
from datetime import datetime

"""Sets the variable now to the current date and time"""
now = datetime.now()

"""The variable current_time contains the string values of the current time"""
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
dic={'2':34424,'5':4234}
for i in dic.keys():
    print(i)
print(current_time[current_time.index(':')+1:current_time.rindex(':')])
