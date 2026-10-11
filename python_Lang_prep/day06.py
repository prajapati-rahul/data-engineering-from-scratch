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
import pandas as pd

df = pd.DataFrame({
    "order_id": [101, 102, 103, 104],
    "order_date": [
        "2026-10-01",
        "2026-10-03",
        "2026-10-07",
        "2026-10-09"
    ],
    "amount": [1000, 2500, 1500, 3000]
})

print(df.dtypes)
#Initially, order_date may be stored as object, which generally indicates string-like data. Convert it:

df["order_date"] = pd.to_datetime(df["order_date"])

print(df.dtypes)
#Now order_date has a datetime dtype, usually datetime64[ns].


#Extract year, month, and day
#Once converted, use the .dt accessor.
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["day"] = df["order_date"].dt.day
df["day_name"] = df["order_date"].dt.day_name()

print(df)
#Your DataFrame now contains additional columns for year, month, day, and weekday name.


#Other useful properties include:
df["order_date"].dt.dayofweek    #dayofweek uses Monday = 0 and Sunday = 6.
df["order_date"].dt.quarter
df["order_date"].dt.is_month_end
df["order_date"].dt.is_month_start


#Filter rows by date, Suppose you need orders placed on or after October 5.
df["order_date"] = pd.to_datetime(df["order_date"])
result = df[df["order_date"] >= "2026-10-05"]

print(result)

#For a date range:
start_date = "2026-10-03"
end_date = "2026-10-07"

result = df[df["order_date"].between(start_date, end_date)]
print(result)    #between() includes both endpoints by default.


#Handle invalid or missing dates, Consider messy data:
df = pd.DataFrame({
    "order_date": [
        "2026-10-01",
        "invalid-date",
        None,
        "2026-10-05"
    ]
})

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
print(df)      #Invalid values and missing dates become NaT (Not a Time).

print(df["order_date"].isna())
print(df["order_date"].isna().sum())

#Remove rows with missing dates:
df = df.dropna(subset=["order_date"])
#Or keep the rows and decide how to handle them based on your business requirements.


#Practical Data Engineering example. Imagine a CSV containing order dates and sales amounts. Your task is to calculate monthly sales.
import pandas as pd

df = pd.DataFrame({
    "order_date": [
        "2026-01-05",
        "2026-01-15",
        "2026-02-03",
        "2026-02-20",
        "2026-03-10"
    ],
    "amount": [1000, 2000, 1500, 3000, 2500]
})

df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.to_period("M")

monthly_sales = df.groupby("month")["amount"].sum()
print(monthly_sales)

# month
# 2026-01    3000
# 2026-02    4500
# 2026-03    2500
# Freq: M, Name: amount, dtype: int64


#Python Error Handling, Exceptions & Logging

#In Data Engineering, your pipeline may read thousands of rows from CSV files, connect to databases, or process API responses. Some records may be invalid, files may be missing, or conversions may fail.
#That's why you need error handling: to handle failures safely instead of letting your entire program crash unexpectedly.

#Errors vs exceptions
number = int("hello") #Python raises a ValueError because "hello" cannot be converted into an integer.

print(10 / 0)  #This raises a ZeroDivisionError.

# Common exceptions:
# Exception	                     When it occurs
# ValueError	            Value is invalid for an operation
# TypeError     	        Operation used with an inappropriate type
# FileNotFoundError	        File does not exist
# KeyError	                Dictionary key is missing
# IndexError	            List index is out of range
# ZeroDivisionError	        Division by zero
# PermissionError	        Access to a file or resource is denied

#An exception is a runtime problem that Python can raise and your program can handle.
# try and except, basic syntax:
try:
    # Code that might fail
    number = int(input("Enter a number: "))
    print(number * 2)
except ValueError:
    # What to do if that exception occurs
    print("Please enter a valid integer.")


#Handling multiple exceptions
try:
    a = int(input("Enter numerator: "))
    b = int(input("Enter denominator: "))

    result = a / b
    print(result)

except ValueError:
    print("Enter valid integers.")

except ZeroDivisionError:
    print("Denominator cannot be zero.")


