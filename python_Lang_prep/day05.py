#Pandas 🐼
#If NumPy is mainly for numerical arrays, Pandas is mainly for working with structured/tabular data like CSV, Excel, SQL results, JSON, etc.


#pip install pandas    #install pandas if you haven't already
import pandas as pd
#two main data structures in pandas are Series and DataFrame.

#Series

marks = pd.Series([80, 75, 90, 65])  #one dimensional labeled array
print(marks)     # 0    80
                 # 1    75
                 # 2    90
                 # 3    65
                 # dtype: int64


#DataFrame
data = {
    "name": ["Rahul", "Aman", "Priya"],
    "age": [21, 22, 20],
    "marks": [85, 90, 78]
}

df = pd.DataFrame(data)    #a dataframe is a two-dimensional labeled data structure with columns of potentially different types. It is similar to a spreadsheet or SQL table, or a dict of Series objects.
print(df)     #output:
#     name  age  marks
# 0   Rahul   21     85
# 1    Aman   22     90
# 2   Priya   20     78


#Reading a CSV
df = pd.read_csv("students.csv")
print(df)

#pandas automatically converts the CSV data into a DataFrame, making it easy to manipulate and analyze the data.


#Inspecting Your Data
#After loading a dataset, don't immediately start modifying it. First inspect it to understand its structure and contents. This will help you make informed decisions about how to clean, transform, and analyze the data.

print(df.head())   #you can even pass a number to head() to see that many rows from the top. For example, df.head(10) will show the first 10 rows.
print(df.tail())   #you can even pass a number to tail() to see that many rows from the bottom. For example, df.tail(10) will show the last 10 rows.
print(df.shape)    #prints the dimensions of the DataFrame (rows, columns)
print(df.columns)  #prints the column names
print(df.dtypes)   #prints the data types of each column
print(df.info())   #prints a concise summary of the DataFrame, including the number of non-null entries in each column and the data types.

#for numerical columns, you can also use the describe() method to get a quick overview of the distribution of values in each column.
print(df.describe())  #prints summary statistics for numerical columns, including count, mean, standard deviation, minimum, maximum, and quartiles. This can help you quickly identify potential outliers or unusual values in your data.


#Selecting Columns
print(df["name"])     #select a single column by name
print(df[["name"]])   #select a single column by name (returns a DataFrame)

df["marks"]        # one column
df[["name", "marks"]]   # multiple columns, also notice the double brackets [[]] when selecting multiple columns. This is because you are passing a list of column names to the DataFrame, and the list itself is enclosed in brackets.


#Selecting Rows
#You can select rows in a DataFrame using the loc and iloc indexers.

# The iloc indexer is integer position-based, meaning that you have to specify the index of the row or column that you want to select.
print(df.iloc[0])     #select a single row by index
print(df.iloc[0:2])    #select multiple rows by index range (0 to 1, 2 is excluded)
#output:
#     name  age  marks
# 0  Rahul   21     85
# 1   Aman   22     90

#specific rows and columns
print(df.iloc[1, 2])  #output: 90 (row 1, column 2)


# The loc indexer is label-based, meaning that you have to specify the name of the row or column that you want to select.
print(df.loc[0, "name"])  #output: Rahul (row 0, column "name")
print(df.loc[1, "marks"])  #output: 90 (row 1, column "marks")

#onr more thing to note is that loc can also be used to select rows and columns by their labels, while iloc can only be used to select rows and columns by their integer positions.
print(df.iloc[0:2])    #select multiple rows by index range (0 to 1, 2 is excluded)
#output:
#     name  age  marks
# 0  Rahul   21     85
# 1   Aman   22     90

print(df.loc[0:2])   #select multiple rows by label range (0 to 2, 2 is included)
#output:
#     name  age  marks
# 0  Rahul   21     85
# 1   Aman   22     90
# 2  Priya   20     78



#Filtering Data

#suppose you want to filter the DataFrame to only include students who scored more than 80 marks. You can do this using boolean indexing.
df = pd.DataFrame({
    "name": ["Rahul", "Aman", "Priya", "Neha"],
    "marks": [85, 90, 78, 88]
})

result = df[df["marks"] > 80]
print(result)    
#output:
#     name  marks
# 0  Rahul     85
# 1   Aman     90
# 3   Neha     88

#the important thing to note here is that the condition df["marks"] > 80 returns a boolean Series, which is then used to filter the DataFrame. This is a powerful feature of pandas that allows you to easily filter data based on complex conditions.
#Then Pandas keeps only True rows.


#Multiple Conditions
df = pd.DataFrame({
    "name": ["Rahul", "Aman", "Priya", "Neha"],
    "age": [21, 22, 20, 21],
    "marks": [85, 90, 78, 88]
})

result = df[ (df["marks"] > 80) & (df["age"] > 20) ]
print(result)
#output:
#     name  age  marks
# 0  Rahul   21     85
# 1   Aman   22     90
# 3   Neha   21     88


#important thing to note here is that when using multiple conditions, you need to use parentheses around each condition and use the & operator for "and", the | operator for "or" and ~ operator for "not". This is because the & and | operators have a higher precedence than the comparison operators, so you need to use parentheses to ensure that the conditions are evaluated correctly.
#don't use pythons and, or, not keywords for multiple conditions in pandas. Use &, |, ~ instead.


#Adding a New Column
df["grade"] = ["A" if marks >= 85 else "B" for marks in df["marks"]]
print(df)
#output:
#     name  age  marks grade
# 0  Rahul   21     85     A
# 1   Aman   22     90     A
# 2  Priya   20     78     B
# 3   Neha   21     88     A


#Sorting
df = df.sort_values(by="marks", ascending=False)  # Sort by marks in descending order
print(df)
#output:
#     name  age  marks grade
# 1   Aman   22     90     A
# 3   Neha   21     88     A
# 0  Rahul   21     85     A
# 2  Priya   20     78     B

df = df.sort_values(by=["marks", "age"], ascending=[False, True])  # Sort by marks in descending order and age in ascending order
print(df)
#output:
#     name  age  marks grade
# 1   Aman   22     90     A
# 3   Neha   21     88     A
# 0  Rahul   21     85     A
# 2  Priya   20     78     B


#Missing Values
#Real-world datasets almost always have missing values.

df = pd.DataFrame({
    "name": ["Rahul", "Aman", "Priya"],
    "marks": [85, None, 78]
})

print(df.isnull())   # Check for missing values in the DataFrame

print(df.isnull().sum())   # Count of missing values in each column
#output:
# name     0
# marks    1         #means marks has one missing value
# dtype: int64


#Filling Missing Values

df["marks"] = df["marks"].fillna(0)    #filling missing values with 0
df["marks"] = df["marks"].fillna(df["marks"].mean())    #filling missing values with mean


#Removing Missing Rows

df = df.dropna()     #This removes rows containing missing values.
#But don't blindly use dropna() in real projects. Sometimes missing values contain useful information and should be filled instead.


#Removing Duplicate Rows

print(df.duplicated())    #check duplicates
df = df.drop_duplicates()    #remove duplicates


#GroupBy
#This is one of the most important Pandas concepts for Data Engineering.

df = pd.DataFrame({
    "department": ["CSE", "CSE", "ECE", "ECE", "CSE"],
    "student": ["A", "B", "C", "D", "E"],
    "marks": [80, 90, 70, 85, 95]
})

result = df.groupby("department")["marks"].mean()
print(result)
#output:
# department
# CSE    88.333333
# ECE    77.500000


#Pandas and SQL Similar functions
# Pandas                  SQL

# groupby()        ↔      GROUP BY
# mean()           ↔      AVG()
# sum()            ↔      SUM()
# count()          ↔      COUNT()
# min()            ↔      MIN()
# max()            ↔      MAX()


#Reading JSON
#panda can diretly read json
df = pd.read_json("students.json")   #read
df.to_json("output.json")    #write


df.to_csv("output.csv", index=False)    #writing csv
#why index = false, otherwise panda may write
# 0,Rahul,21,85
# 1,Aman,22,90

