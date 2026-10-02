# filter() keeps elements satisfying a condition.

numbers = [1, 2, 3, 4, 5, 6]
even = filter(lambda x: x % 2 == 0, numbers)
print(list(even))



#Suppose:
prices = [100, 500, 1200, 300, 2000]

#First select prices > 500:
filtered = filter(lambda x: x > 500, prices)

#Then add 18% tax:
result = map(lambda x: x * 1.18, filtered)

#Finally:
print(list(result))  #Output: [1416.0, 2360.0]


#But Comprehension Is Often Cleaner
result = [x * 1.18 for x in prices if x > 500]
print(result)  #Output: [1416.0, 2360.0]



#Function Returning Multiple Values
def calculate(a, b):
    total = a + b
    difference = a - b

    return total, difference

total, difference = calculate(10, 5)

print(total)
print(difference)



#Scope
x = 100

def test():
    x = 50
    print(x)  # Prints 50

test()

print(x)  # Prints 100



#A Very Important Data Engineering Pattern
def clean_data(data):
    # cleaning
    return data


def transform_data(data):
    # transformation
    return data


def validate_data(data):
    # validation
    return True

#practical example of a data engineering pipeline using the above functions:
name = [" rahul ", " AMAN", "Priya ", "  rohit"]

result = [name.strip().title() for name in name if validate_data(name)]
print(result)  #Output: ['Rahul', 'Aman', 'Priya', 'Rohit']



#File Handling for Data Engineering



file = open("students.txt", "r")   #r stands for read mode
data = file.read()
print(data)
file.close()


#but there is a better way to handle files using the with statement, which automatically closes the file after the block of code is executed:
with open("students.txt", "r") as file:
    data = file.read()
    print(data)


#reading a file line by line using a for loop:
with open("students.txt", "r") as file:
    for line in file:
        print(line.strip())  #strip() removes the newline character at the end of each line


#read() method reads the entire file and returns it as a string:
with open("students.txt", "r") as file:
    data = file.read()
    print(data)

#readline() method reads the file line by line and returns a string of the current line:
with open("students.txt", "r") as file:
    line = file.readline()
    print(line.strip())

#readlines() method reads the file line by line and returns a list of lines:
with open("students.txt", "r") as file:
    lines = file.readlines()
    print(lines)  #Output: ['Rahul\n', 'Aman\n', 'Priya\n', 'Rohit\n']


#writing to a file using the write() method:
with open("output.txt", "w") as file:  #w stands for write mode
    file.write("Hello World\n")
    file.write("This is a test file.\n")

#if the file already exists, it will be overwritten. If the file does not exist, it will be created.

#appending to a file using the append() method:
with open("output.txt", "a") as file:  #a stands for append mode
    file.write("This line will be appended to the file.\n")



#CSV Files for Data Engineering, Comma-Separated Values files are a common format for storing tabular data. Python provides a built-in module called csv for reading and writing CSV files.
import csv
with open("students.csv", "r") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)


#output:
# ['id', 'name', 'age', 'marks']
# ['1', 'Rahul', '21', '85']
# ['2', 'Aman', '22', '90']
# ['3', 'Priya', '20', '88']

#notice that the first row is the header row, which contains the names of the columns. The subsequent rows contain the data.
#and everything is read as a string, so you may need to convert the data to the appropriate type (e.g., int, float) before using it in calculations or comparisons.


#CSV as a Dictionary for Data Engineering, Python's csv module also provides a DictReader class that allows you to read CSV files as dictionaries, where the keys are the column names and the values are the corresponding data for each row.
import csv
with open("student.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)

#output:
# {'id': '1', 'name': 'Rahul', 'age': '21', 'marks': '85'}



#Writing to a CSV File for Data Engineering, Python's csv module also provides a writer class that allows you to write data to a CSV file.
import csv

with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name", "age", "marks"])
    writer.writerow(["1", "Rahul", "21", "85"])
    writer.writerow(["2", "Aman", "22", "90"])
    writer.writerow(["3", "Priya", "20", "88"])



#json Files for Data Engineering, JSON (JavaScript Object Notation) is a lightweight data interchange format that is easy for humans to read and write, and easy for machines to parse and generate. Python provides a built-in module called json for working with JSON data.



import json
with open("students.json", "r") as file:
    data = json.load(file)
    print(data)

#output:
# [{'id': '1', 'name': 'Rahul', 'age': '21', 'marks': '85'}, {'id': '2', 'name': 'Aman', 'age': '22', 'marks': '90'}, {'id': '3', 'name': 'Priya', 'age': '20', 'marks': '88'}]


#writing to a JSON file for Data Engineering, Python's json module also provides a dump() method that allows you to write data to a JSON file.
import json

student = {
    "name": "Rahul",
    "age": 21,
    "skills": ["Python", "AWS", "SQL"]
}

with open("student.json", "w") as file:
    json.dump(student, file, indent=4)   #indent=4 is used to pretty-print the JSON data with an indentation of 4 spaces, making it more readable. If you omit the indent parameter, the JSON data will be written in a compact format without any extra whitespace.


#json.dump() vs json.dumps(), The json.dump() method is used to write JSON data to a file, while the json.dumps() method is used to convert a Python object to a JSON-formatted string. The "s" in dumps stands for "string".
