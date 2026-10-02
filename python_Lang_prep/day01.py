from doctest import Example


amount = 1000
tax = amount * 0.18
print(amount + tax)

def calculate_total(amount):
    return amount * 1.18

total = calculate_total(1000)

print(total)


# Multiple parameters
def calculate_total(price, tax):
    return price + (price * tax)

print(calculate_total(1000, 0.18))

# Why functions matter in Data Engineering
# Imagine a pipeline:

# CSV
#  ↓
# Read Data
#  ↓
# Clean Data
#  ↓
# Transform Data
#  ↓
# Validate Data
#  ↓
# Save Data

# Instead of putting everything into one giant script:

def read_data():
    pass

def clean_data():
    pass

def transform_data():
    pass

def validate_data():
    pass

def save_data():
    pass

#Then you can call these functions in order to create a clean and organized pipeline:

data = read_data()
data = clean_data(data)
data = transform_data(data)

validate_data(data)
save_data(data)



# Lists
# A list stores multiple values.

numbers = [10, 20, 30, 40]
print(numbers[0])  # accessing the first element of the list
print(numbers[-1])  # accessing the last element of the list
numbers.append(50)  # adding an element to the end of the list
numbers.remove(20)  # removing an element from the list
len(numbers)  # getting the length of the list

# we have learned about slicing in basics.py, we can also slice lists in a similar way:
print(numbers[1:3])  # prints elements from index 1 to 2



# Dictionaries
# Dictionary = key-value pairs.
student = {
    "name": "Rahul",
    "age": 21,
    "marks": 85
}


print(student["name"])  # accessing the value associated with the key "name"
student["city"] = "Ghaziabad"  # adding a new key-value pair to the dictionary
del student["age"]  # removing a key-value pair from the dictionary
student["marks"] = 90  # updating the value associated with the key "marks"
print(student.keys())  # getting all the keys in the dictionary
print(student.values())  # getting all the values in the dictionary

# Why dictionaries are extremely important
# JSON data looks almost exactly like Python dictionaries.
# {
#     "name": "Rahul",
#     "age": 21,
#     "skills": ["Python", "AWS", "SQL"]
# }



# List of Dictionaries
employees = [
    {"id": 1, "name": "Rahul", "salary": 50000},
    {"id": 2, "name": "Aman", "salary": 60000},
    {"id": 3, "name": "Priya", "salary": 55000}
]

for employee in employees:
    print(employee["name"])
# Rahul
# Aman
# Priya

for employee in employees:
    if employee["salary"] > 55000:
        print(employee["name"])
# Aman
# Priya


# Tuples
# Tuple is similar to a list but generally treated as immutable.
point = (10, 20)
print(point[0])
# Use tuples when values should be treated as fixed.



# Sets
# Set is an unordered collection of unique elements.
unique_numbers = {1, 2, 3, 4, 5}
unique_numbers.add(6)  # adding an element to the set
unique_numbers.remove(3)  # removing an element from the set
print(unique_numbers)  # {1, 2, 4, 5, 6}

# Very useful for removing duplicates:
emails = [
    "a@gmail.com",
    "b@gmail.com",
    "a@gmail.com"
]

unique_emails = set(emails)

print(unique_emails)



# Comprehensions
# Python's compact way of creating collections.
numbers = [1, 2, 3, 4, 5]

squares = []

# Instead of:
# for n in numbers:
#     squares.append(n * n)

#you can use a list comprehension:

squares = [n * n for n in numbers]

even = [n for n in numbers if n % 2 == 0]


# Dictionary comprehension
student = {
    "name": "Rahul",
    "age": 21,
    "marks": 85
}

# Create a new dictionary with only the keys we want
student_info = {key: value for key, value in student.items() if key in ["name", "marks"]}

print(student_info)  # {'name': 'Rahul', 'marks': 85}

# Functions for Data Engineering

def add(a, b):
    return a + b

# Parameters vs Arguments
def greet(name):       # name = parameter
    print("Hello", name)

greet("Rahul")         # "Rahul" = argument

# Multiple parameters
def calculate_total(price, tax):
    return price + price * tax

result = calculate_total(1000, 0.18)
print(result)

# Default Arguments
def greet(name, greeting="Hello"):
    print(greeting, name)

greet("Rahul")  # Output: Hello Rahul
greet("Rahul", "Hi")  # Output: Hi Rahul


#example of a function with a default argument that is useful in data engineering:
def read_data(file_path, encoding="utf-8"):
    print(f"Reading {file_path} using {encoding}")

# Keyword Arguments
#instead of passing arguments in order, you can specify them by name:
def employee(name, age, salary):
    print(name, age, salary)

employee("Rahul", 21, 50000)

#you can also call the function using keyword arguments:
employee(
    name="Rahul",
    age=21,
    salary=50000
)
#this is more readable and allows you to pass arguments in any order.

#args
#suppose you want to create a function that can accept any number of arguments. You can use *args for this:
def calculate_sum(*numbers):
    total = 0

    for number in numbers:
        total += number

    return total

print(calculate_sum(10, 20))  # 30
print(calculate_sum(10, 20, 30, 40))  #100
# *args collects arguments into a tuple.


# **kwargs
# kwargs is used for multiple keyword arguments.
def show_details(**details):
    print(details)

show_details(
    name="Rahul",
    age=21,
    city="Ghaziabad"
)

# Remember this:

# Syntax	    Stores	            Example
# *args	        tuple	            (10, 20, 30)
# **kwargs	    dictionary	        {"name": "Rahul"}


# Lambda Functions
square = lambda x: x * x
print(square(5))  # 25

# Lambda functions are useful for short, simple operations.
# They are often used with functions like map(), filter(), and sorted().