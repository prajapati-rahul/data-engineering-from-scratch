#Python's datetime module
from datetime import datetime, date, time

today = date.today()
now = datetime.now()

print(today)    #prints current date
print(now)      #prints current data along with time


# Creating dates and timestamps
dt = datetime(2026, 10, 9, 14, 30, 0)

print(dt)     #2026-10-09 14:30:00
print(dt.year)      #2026
print(dt.month)     #10
print(dt.day)       #9
print(dt.hour)      #14
print(dt.minute)    #30


#Convert strings into dates using strptime()
from datetime import datetime

date_string = "09-10-2026"
dt = datetime.strptime(date_string, "%d-%m-%Y")    #strptime() means string parse time: convert a string into a datetime object.

print(dt)     #2026-10-09 00:00:00
print(type(dt))    #<class 'datetime.datetime'>


#Common format Codes
# Code	Meaning	Example

# %Y	Four-digit year	2026
# %y	Two-digit year	26
# %m	Month	10
# %d	Day	09
# %H	Hour (24-hour)	14
# %M	Minute	30
# %S	Second	45

dt = datetime.strptime("2026/10/09", "%Y/%m/%d")


#Convert dates into strings using strftime()
from datetime import datetime

dt = datetime(2026, 10, 9, 14, 30)
formatted = dt.strftime("%d-%m-%Y")

print(formatted)      #09-10-2026

# Remember:
# - strptime() → string to datetime
# - strftime() → datetime to formatted string


#Date arithmetic using timedelta
# Suppose you need to calculate a delivery date three days after an order.
from datetime import date, timedelta

order_date = date(2026, 10, 9)
delivery_date = order_date + timedelta(days=3)

print(delivery_date)    #2026-10-12


#Subtract Dates:
previous_date = order_date - timedelta(days=7)
print(previous_date)

#You can also calculate the difference between two dates:
from datetime import date

start = date(2026, 10, 1)
end = date(2026, 10, 9)

difference = end - start
print(difference.days)      #8


#Working with dates in Pandas
