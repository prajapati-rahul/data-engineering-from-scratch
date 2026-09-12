# printing
print("hello its my fresh start to data engineering")


#for next line inside the print statement we can use \n
print("hello its my fresh start to data engineering\n this is my second line")


# variable, Python determines the type automatically.
name = "Rahul"              # str
age = 21                    # int
percentage = 85.5           # float
is_student = True           # bool

marks = [85, 90, 78]        # list
student = {"name": "Rahul"} # dict
unique = {1, 2, 3}          # set
coordinates = (10, 20)      # tuple, For Data Engineering, list and dictionary are especially important.


# confirmation of variable types
print(type(name)) #you can check it.
print(type(age)) #you can check it.
print(type(percentage)) #you can check it.
print(type(is_student)) #you can check it.
print(type(marks)) #you can check it.
print(type(student)) #you can check it.
print(type(unique)) #you can check it.
print(type(coordinates)) #you can check it.
print("Hello, my name is " + name + " and I am " + str(age) + " years old.")
print(f"Hello, my name is {name} and I am {age} years old.")

x,y,z = 5, 10, 15
print(x,y,z)


#comments
# This is a single-line comment

'''
This is a multi-line comment.
and it can span multiple lines.
'''



#explicit type casting
x = 5
print(type(x))
x = str(x)
print(type(x))


#implicit type casting
x = 5
y = 2.5
z = x + y
print(type(z))

#and one Note, dont forget python is case sensitive, so be careful with variable names and function names.
#also make sure to use proper indentation, as it is crucial in Python for defining code blocks.



# Conditions
age = 21

if age >= 18:
    print("Adult")
else:
    print("Minor")

# Multiple conditions:
marks = 82

if marks >= 90:
    grade = "A"
elif marks >= 75:
    grade = "B"
elif marks >= 60:
    grade = "C"
else:
    grade = "D"

print(grade)



#basic string operations and slicing
name = "rahul prajapati"
print(name[0])  # prints the first character of the string
print(name[6])  # prints the seventh character of the string
print(name[-1]) # prints the last character of the string  
print(name[0:5])  # prints characters from index 0 to 4
print(name[6:])  # prints characters from index 6 to the end
print(name[:6])  # prints characters from the start to index 5
print(name[:])   # prints the entire string
print(name[::2])  # prints every second character of the string

#basic string methods
print(name.upper())  # converts the string to uppercase
print(name.lower())  # converts the string to lowercase
print(name.capitalize())  # capitalizes the first character of the string
print(name.title())  # capitalizes the first character of each word in the string
print(name.replace("rahul", "abhinav"))  # replaces "rahul" with "abhinav" in the string



#basic string methods continued
file = "raw_data.csv"
if(file.endswith(".csv")):
    print("This is a CSV file.")

if(file.startswith("raw")):
    print("This file starts with 'raw'.")



# Loops
# for loop
numbers = [10, 20, 30, 40]

for number in numbers:
    print(number)


# You can also use range()
for i in range(5):
    print(i)


# while loop
count = 0

while count < 5:
    print(count)
    count += 1