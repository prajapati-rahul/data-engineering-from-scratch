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

