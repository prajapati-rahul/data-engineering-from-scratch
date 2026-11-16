#Day 10: Relational Databases & SQL Integration with Python 🗄️⚡

#In Data Engineering, reading from and loading into relational databases (PostgreSQL, MySQL, SQLite, Snowflake, Redshift)
#is one of the most common daily tasks.
#Python has a standard Database API specification (PEP 249). The built-in `sqlite3` module follows this exact standard,
#so the concepts you learn here apply identically to PostgreSQL (psycopg2), Snowflake (snowflake-connector), and MySQL!

#Today we cover:
# 1. Connecting to a Database & Understanding Cursors
# 2. Creating Tables with Schemas & Constraints
# 3. Safe Data Ingestion (Parameterized Queries & Bulk Ingestion with executemany)
# 4. Querying & Fetching Data (fetchone, fetchall)
# 5. Transaction Management (Commit & Rollback for Pipeline Reliability)
# 6. Pandas + SQL Integration (pd.read_sql & df.to_sql)
# 7. End-to-End ETL Pipeline: CSV/Records → Transform → SQLite Warehouse
# 8. Practice Questions with Solutions


import sqlite3
import pandas as pd


# 1. Connecting to a Database & Cursors

# sqlite3.connect("database_name.db") creates or opens a local database file.
# You can also use ":memory:" for a lightning-fast temporary database in RAM (great for testing!).

conn = sqlite3.connect(":memory:") # Using in-memory database for quick local experimentation
cursor = conn.cursor()             # A cursor is used to execute SQL queries and fetch results.

print("Database connected successfully!")



# 2. Creating Tables with Schemas

# In Data Engineering, explicit schemas with primary keys and constraints ensure data quality.
create_table_query = """
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    city TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

cursor.execute(create_table_query)
conn.commit() # Saves changes to database
print("Table 'dim_customers' created.")



# 3. Safe Data Ingestion (Parameterized Queries & executemany)

# DANGER: NEVER format SQL queries using f-strings like this:
# bad_query = f"INSERT INTO dim_customers VALUES (1, '{user_input}', ...)"
# This causes SQL Injection vulnerabilities and crashes when names have quotes (e.g. O'Connor)!

# ALWAYS use parameterized queries with '?' placeholders:
# Python's database driver automatically sanitizes values.

# Single Insert:
single_insert_query = """
INSERT INTO dim_customers (customer_id, name, email, city)
VALUES (?, ?, ?, ?);
"""
cursor.execute(single_insert_query, (1, "Rahul Prajapati", "rahul@example.com", "Ghaziabad"))
conn.commit()


# Bulk Insert (High-Performance Ingestion with executemany):
# In production, never insert 10,000 rows one-by-one in a loop.
# Use cursor.executemany() for batch insertion!
customers_batch = [
    (2, "Aman Sharma", "aman@example.com", "Delhi"),
    (3, "Priya Verma", "priya@example.com", "Noida"),
    (4, "Sneha Patel", "sneha@example.com", "Mumbai"),
    (5, "Rohit Kumar", "rohit@example.com", "Bengaluru")
]

cursor.executemany(single_insert_query, customers_batch)
conn.commit()
print(f"Inserted {cursor.rowcount} records in batch.")



# 4. Querying & Fetching Data

# Executing a SELECT query:
cursor.execute("SELECT customer_id, name, city FROM dim_customers WHERE city = ?", ("Delhi",))

# fetchone() → Returns the next single row as a tuple (or None)
first_row = cursor.fetchone()
print("First row from Delhi:", first_row) # (2, 'Aman Sharma', 'Delhi')


# fetchall() → Returns all matching rows as a list of tuples
cursor.execute("SELECT customer_id, name, city FROM dim_customers ORDER BY name ASC")
all_customers = cursor.fetchall()

print("--- All Customers ---")
for row in all_customers:
    print(f"ID: {row[0]}, Name: {row[1]}, City: {row[2]}")


# Converting Rows to Dictionaries (Common in API/JSON pipelines):
# You can set row_factory on the connection:
conn.row_factory = sqlite3.Row
dict_cursor = conn.cursor()
dict_cursor.execute("SELECT customer_id, name FROM dim_customers LIMIT 2")
for r in dict_cursor.fetchall():
    print(dict(r)) # {'customer_id': 1, 'name': 'Rahul Prajapati'}



# 5. Transaction Management (Commit & Rollback)

# In Data Engineering, ACID transactions are essential:
# Either ALL records in a batch get loaded, or NONE do. Partial loads ruin data integrity.

# Let's create an accounts table:
cursor.execute("""
CREATE TABLE IF NOT EXISTS bank_accounts (
    acc_id INTEGER PRIMARY KEY,
    holder TEXT,
    balance REAL
);
""")
cursor.executemany("INSERT INTO bank_accounts VALUES (?, ?, ?)", [
    (101, "Rahul", 5000.0),
    (102, "Aman", 3000.0)
])
conn.commit()

# Simulating a safe financial transfer transaction:
# Transfer ₹1000 from Rahul to Aman
try:
    transfer_amount = 1000.0

    # Deduct from Rahul
    cursor.execute("UPDATE bank_accounts SET balance = balance - ? WHERE acc_id = ?", (transfer_amount, 101))

    # Suppose an unexpected pipeline failure happens here!
    # raise Exception("Network connection dropped while updating recipient!")

    # Add to Aman
    cursor.execute("UPDATE bank_accounts SET balance = balance + ? WHERE acc_id = ?", (transfer_amount, 102))

    # Commit only if both updates succeeded:
    conn.commit()
    print("Transaction successful! Both accounts updated.")

except Exception as err:
    # If anything failed, undo all changes in this transaction!
    conn.rollback()
    print(f"Transaction failed ({err}). Rolled back to safe state.")



# 6. Pandas + SQL Integration (The Power Combo 🚀)

# In real data workflows, you query SQL directly into a Pandas DataFrame for analysis,
# or save transformed DataFrames directly into a database table.

# A. pd.read_sql_query() (SQL → DataFrame)
query = """
SELECT customer_id, name, city 
FROM dim_customers 
WHERE city IN ('Delhi', 'Ghaziabad', 'Mumbai')
"""
df_customers = pd.read_sql_query(query, conn)
print("--- Loaded into Pandas DataFrame from SQL ---")
print(df_customers)


# B. df.to_sql() (DataFrame → SQL Table)
# Create a transformed summary table and save it back into SQL:
orders_data = pd.DataFrame({
    "order_id": [1001, 1002, 1003, 1004],
    "customer_id": [1, 2, 1, 3],
    "amount": [450.0, 1200.0, 850.0, 3000.0],
    "status": ["DELIVERED", "DELIVERED", "CANCELLED", "DELIVERED"]
})

# if_exists options:
# - 'fail'    : Raise ValueError if table already exists (default)
# - 'replace' : Drop existing table and create new one
# - 'append'  : Insert new records into existing table
orders_data.to_sql("fct_orders", conn, if_exists="replace", index=False)

# Verify table was created in SQLite:
check_df = pd.read_sql_query("SELECT * FROM fct_orders WHERE status = 'DELIVERED'", conn)
print("--- Querying fct_orders Table Created by Pandas ---")
print(check_df)



# 7. Complete Mini ETL Pipeline: CSV/Dict → Transform → SQLite Warehouse

# Pipeline Architecture:
# Raw Data (Dict/CSV)
#       ↓
# Extract & Validate
#       ↓
# Transform (Calculate tax & total)
#       ↓
# Load into SQLite Table (fct_daily_sales)

raw_sales = [
    {"txn_id": "T1", "item": "Laptop", "price": 60000, "qty": 1},
    {"txn_id": "T2", "item": "Mouse", "price": 800, "qty": 3},
    {"txn_id": "T3", "item": "Monitor", "price": 12000, "qty": 2}
]

def run_sales_etl(records, db_connection):
    print("--- Running Sales ETL Pipeline ---")

    # Step 1: Extract into DataFrame
    df = pd.DataFrame(records)

    # Step 2: Transform
    df["subtotal"] = df["price"] * df["qty"]
    df["tax"] = df["subtotal"] * 0.18
    df["total_amount"] = df["subtotal"] + df["tax"]

    # Step 3: Load into SQLite
    df.to_sql("fct_daily_sales", db_connection, if_exists="replace", index=False)
    print(f"Successfully loaded {len(df)} records into warehouse table 'fct_daily_sales'!")

run_sales_etl(raw_sales, conn)

# Read back and inspect:
print(pd.read_sql_query("SELECT item, qty, total_amount FROM fct_daily_sales", conn))



#Practice Questions

#Q1: Create a table named `inventory` in SQLite with columns:
#    item_id (INTEGER PRIMARY KEY), item_name (TEXT), stock (INTEGER), price (REAL).
#    Insert 3 records using `executemany()`.
#    Query and print all items where stock is less than 10.

#solution:
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL,
    stock INTEGER NOT NULL,
    price REAL NOT NULL
);
""")

sample_items = [
    (1, "SSD 1TB", 15, 6500.0),
    (2, "RAM 16GB", 4, 3200.0),
    (3, "HDMI Cable", 8, 450.0)
]
cursor.executemany("INSERT OR REPLACE INTO inventory VALUES (?, ?, ?, ?)", sample_items)
conn.commit()

cursor.execute("SELECT item_name, stock FROM inventory WHERE stock < 10")
low_stock_items = cursor.fetchall()
print("Low Stock Items:")
for item in low_stock_items:
    print(f"- {item[0]}: {item[1]} units remaining")

#output:
# Low Stock Items:
# - RAM 16GB: 4 units remaining
# - HDMI Cable: 8 units remaining


#Q2: Write a Python function `safe_execute_transaction(conn, query_list)` that takes a list
#    of SQL queries, executes all of them sequentially, and commits only if ALL queries pass.
#    If any query raises an exception, roll back the transaction and return False.

#solution:
def safe_execute_transaction(connection, queries):
    cur = connection.cursor()
    try:
        for sql in queries:
            cur.execute(sql)
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Transaction aborted: {e}")
        return False

# Test valid transaction:
valid_queries = [
    "UPDATE inventory SET stock = stock - 1 WHERE item_id = 1",
    "UPDATE inventory SET stock = stock - 2 WHERE item_id = 3"
]
success = safe_execute_transaction(conn, valid_queries)
print("Transaction succeeded:", success)


#Q3: Using Pandas and SQL together:
#    Write a SQL query that joins `fct_orders` and `dim_customers` on `customer_id`
#    to compute total spending per customer. Load the result into a DataFrame and print it.

#solution:
analytics_query = """
SELECT 
    c.name AS customer_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.amount) AS total_spent
FROM dim_customers c
JOIN fct_orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
"""

customer_spending = pd.read_sql_query(analytics_query, conn)
print("--- Customer Spending Analytics ---")
print(customer_spending)

# Closing database connection cleanly at the end
conn.close()
