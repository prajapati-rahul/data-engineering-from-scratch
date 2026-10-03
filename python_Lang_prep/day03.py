#Real API Example

#suppose api returns a json response like this:
response = '''
{
    "users": [
        {"id": 1, "name": "Rahul"},
        {"id": 2, "name": "Aman"}
    ]
}
'''

#Convert JSON string:
import json

data = json.loads(response)

for user in data["users"]:
    print(user["name"])

#output:
# Rahul
# Aman



#Parquet
#parquet is a columnar storage file format that is optimized for use with big data processing frameworks like Apache Spark and Apache Hadoop. It is designed to be efficient in terms of both storage and query performance, making it a popular choice for storing large datasets. 

#csv
#csv (Comma-Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database. Each line in a CSV file represents a row in the table, and the values in each row are separated by commas.

#Pandas + Parquet
# We'll properly learn pandas shortly.
#for now, let's see how to read a parquet file using pandas. Pandas is a powerful data manipulation library in Python that provides data structures and functions needed to work with structured data seamlessly.

import pandas as pd
df = pd.read_parquet("data.parquet")

#or

import pandas as pd
df = pd.read_csv("students.csv")
df.to_parquet("students.parquet")

#why parquet instead of csv

# imagine you have a dataset with
# 100 million rows
# 20 columns

# but you ony need
# name
# salary

#csv
# Row 1 → all columns
# Row 2 → all columns
# Row 3 → all columns

 #parquet
# Column: ID
# Column: Name
# Column: Age
# Column: Salary
# ...
# Parquet is a columnar storage format, which means it stores data in columns rather than rows. This makes it more efficient for analytical queries that involve reading only specific columns or filtering data based on column values. Additionally, parquet files are compressed, which reduces storage space and improves I/O performance when reading large datasets.


#File Paths
#you should always use relative paths instead of absolute paths. Absolute paths are specific to a particular machine and may not work on other machines or environments. Relative paths, on the other hand, are based on the current working directory and are more portable.
# istead of using an absolute path like this:
file = open("data/students.csv")

# you can use pathlib to create a relative path like this:
from pathlib import Path
file_path = Path("data") / "students.csv"

print(file_path)      #output: data/students.csv

#check if the file exists
if file_path.exists():
    print("File exists")

#get extension of the file
print(file_path.suffix)        #output: .csv



#Encoding

#Encoding is the process of converting data from one format to another. In the context of text files, encoding refers to the way characters are represented in bytes. Different encodings can represent the same characters using different byte sequences. Common encodings include UTF-8, ASCII, and ISO-8859-1.
#you can specify the encoding when reading or writing files in Python. For example, when reading a CSV file with pandas, you can specify the encoding like this:    
with open("students.csv", "r", encoding="utf-8") as file:
    data = file.read()

#utf-8 is a widely used encoding that can represent all characters in the Unicode standard. It is backward compatible with ASCII and is the default encoding for many programming languages and platforms. Using UTF-8 ensures that your text files can handle a wide range of characters from different languages and scripts.


#Mini ETL Example
#Let's combine what you've learned.

# Suppose students.csv contains:
# name,marks
# Rahul,85
# Aman,92
# Priya,67
# Rohit,74

# We want:
# CSV
#  ↓
# Read
#  ↓
# Filter marks >= 75
#  ↓
# Save JSON

import csv
import json

students = []

with open("students.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if int(row["marks"]) >= 75:
            students.append(row)

with open("top_students.json", "w", encoding="utf-8") as file:
    json.dump(students, file, indent=4)


#the resulting top_students.json will contain:
# [
#     {
#         "name": "Rahul",
#         "marks": "85"
#     },
#     {
#         "name": "Aman",
#         "marks": "92"
#     }
# ]

#Important Things to Remember
#csv
csv.reader()     # Read rows as lists
csv.DictReader() # Read rows as dictionaries
csv.writer()     # Write rows as lists

#json
json.load()      #Read JSON from a file
json.loads()     #Read JSON from a string

json.dump()      #Write JSON to a file
json.dumps()     #Write JSON to a string

#parquet
pd.read_parquet()    #Read parquet file into a DataFrame
df.to_parquet()      #Write DataFrame to a parquet file


#practice , dont skip this
#Q1 create a file "numbers.txt" that contains the numbers 10, 20, 30, 40, and 50, each on a new line. Then write a Python script that reads the numbers from the file, calculates their sum, and prints the result.

#solution:
with open("numbers.txt", "r") as file:
    numbers = [int(line.strip()) for line in file]

total = sum(numbers)
print("The sum of the numbers is:", total)     #output: The sum of the numbers is: 150


#Q2 read this csv file and print only the names of the students who are older than 20. csv file content:
# name,age,city
# Rahul,21,Ghaziabad
# Aman,22,Delhi
# Priya,20,Noida

#solution:
import csv
with open ("students.csv","r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if int(row["age"]) > 20:
            print(row["name"]) 

#output: Rahul
#        Aman  


#Q3 create a Json file conataining "name", "age", "skill" and "collage" of 3 students. Then write a Python script that reads the JSON file and prints the names of the students who have "Python" as a skill.
import json
# Create a JSON file with student data
students_data = [
    {"name": "Rahul", "age": 21, "skill": "Python", "college": "XYZ University"},
    {"name": "Aman", "age": 22, "skill": "Java", "college": "ABC College"},
    {"name": "Priya", "age": 20, "skill": "Python", "college": "LMN Institute"}
]
with open("students.json", "w") as file:
    json.dump(students_data, file, indent=4)

# Read the JSON file and print names of students with Python skill
with open("students.json", "r") as file:
    data =json.load(file)
    for student in data:
        if student["skill"] == "Python":
            print(student["name"])

#output: Rahul
#        Priya

#q4 Mini ETL Example, create a CSV file conataining the below data and read this csv file and create a Json file conataining only the products with total_price. total_price = price * quantity. csv file content:
# product,price,quantity
# Laptop,50000,2
# Mouse,500,5
# Keyboard,1000,3
# Monitor,15000,2

#solution:
import csv
import json
products = []
with open ("products.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_price = int(row["price"]) * int(row["quantity"])
        products.append({
            "product": row["product"],
            "total_price": total_price
        })
    
with open("products.json", "w") as file:
    json.dump(products, file, indent=4)