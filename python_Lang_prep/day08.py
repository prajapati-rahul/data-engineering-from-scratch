#Day 08: Advanced Pandas for Data Engineering 🐼🚀

#In Day 05 we learned basic Pandas (DataFrames, filtering, sorting, basic groupby).
#In real-world Data Engineering, data rarely comes in a single clean table.
#Data is scattered across multiple tables, files, and partitions that you need to join, reshape, and clean at scale.

#Today we cover:
# 1. Merging & Joining DataFrames (SQL JOIN equivalents)
# 2. Concatenation (SQL UNION ALL equivalent)
# 3. Data Transformations: apply(), map(), np.where()
# 4. Reshaping Data: melt() and pivot_table()
# 5. String Manipulation with the .str Accessor
# 6. Window-like Operations: cumsum(), shift(), rank()
# 7. Practice Questions with Solutions


import pandas as pd
import numpy as np


# 1. Merging & Joining (SQL JOINs in Pandas)

# In SQL, you use JOIN to combine tables using a common key.
# In Pandas, we use pd.merge().

customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4],
    "name": ["Rahul", "Aman", "Priya", "Sneha"],
    "city": ["Ghaziabad", "Delhi", "Noida", "Mumbai"]
})

orders = pd.DataFrame({
    "order_id": [101, 102, 103, 105],
    "customer_id": [1, 2, 1, 5],    # Note: customer 5 does not exist in customers table
    "amount": [5000, 1200, 3500, 8000]
})

# Inner Join (Default: how="inner")
# Returns only rows where the key exists in BOTH DataFrames.
# SQL: SELECT * FROM orders INNER JOIN customers ON orders.customer_id = customers.customer_id
inner_df = pd.merge(orders, customers, on="customer_id", how="inner")
print("--- Inner Join ---")
print(inner_df)
#output:
#    order_id  customer_id  amount   name       city
# 0       101            1    5000  Rahul  Ghaziabad
# 1       103            1    3500  Rahul  Ghaziabad
# 2       102            2    1200   Aman      Delhi


# Left Join (how="left")
# Keeps all rows from left table (orders). If no match in right table, fills with NaN.
# SQL: SELECT * FROM orders LEFT JOIN customers ON orders.customer_id = customers.customer_id
left_df = pd.merge(orders, customers, on="customer_id", how="left")
print("--- Left Join ---")
print(left_df)
# Customer 5 has NaN for name and city because they don't exist in customers table.


# Right Join (how="right")
# Keeps all rows from right table (customers). Customers with no orders will have NaN for order columns.
right_df = pd.merge(orders, customers, on="customer_id", how="right")
print("--- Right Join ---")
print(right_df)
# Priya and Sneha have NaN for order_id and amount because they haven't placed orders yet.


# Outer Join (how="outer" / Full Outer Join)
# Keeps all rows from BOTH tables. Missing data filled with NaN.
outer_df = pd.merge(orders, customers, on="customer_id", how="outer")
print("--- Outer Join ---")
print(outer_df)


# Merging on different column names:
# Suppose orders has 'cust_id' instead of 'customer_id':
orders_alt = orders.rename(columns={"customer_id": "cust_id"})
merged_diff_keys = pd.merge(orders_alt, customers, left_on="cust_id", right_on="customer_id", how="inner")

# Handling Column Name Collisions (suffixes):
# If both tables share a column name (e.g., 'date'), specify suffixes:
# pd.merge(df1, df2, on="id", suffixes=('_order', '_payment'))



# 2. Concatenation (SQL UNION ALL in Pandas)

# In Data Engineering, daily pipeline dumps often arrive as separate files:
# jan_sales.csv, feb_sales.csv, mar_sales.csv
# To combine them vertically, use pd.concat().

jan_sales = pd.DataFrame({
    "order_id": [1, 2],
    "amount": [1000, 2000]
})

feb_sales = pd.DataFrame({
    "order_id": [3, 4],
    "amount": [1500, 3000]
})

# Stacking rows (axis=0 is default)
# Always set ignore_index=True to avoid duplicate index labels (0, 1, 0, 1)
all_sales = pd.concat([jan_sales, feb_sales], ignore_index=True)
print("--- Concatenated Sales ---")
print(all_sales)
#output:
#    order_id  amount
# 0         1    1000
# 1         2    2000
# 2         3    1500
# 3         4    3000



# 3. Data Transformations: apply(), map(), and np.where()

df = pd.DataFrame({
    "employee": ["Rahul", "Priya", "Aman", "Rohan"],
    "salary": [45000, 85000, 60000, 30000],
    "department": ["IT", "HR", "IT", "Sales"],
    "status_code": ["A", "I", "A", "A"] # A = Active, I = Inactive
})

# A. .map() on a Series
# Ideal for simple dictionary lookups / mapping categorical codes
status_mapping = {"A": "Active", "I": "Inactive"}
df["status_name"] = df["status_code"].map(status_mapping)


# B. .apply() with custom function
# Use apply when logic is more complex:
def calculate_tax(salary):
    if salary >= 75000:
        return salary * 0.20
    elif salary >= 50000:
        return salary * 0.10
    else:
        return 0

df["tax"] = df["salary"].apply(calculate_tax)


# Row-wise apply (axis=1): when calculation depends on multiple columns
def bonus_calculator(row):
    if row["department"] == "IT" and row["salary"] < 50000:
        return 10000
    return 5000

df["bonus"] = df.apply(bonus_calculator, axis=1)


# C. Fast Vectorized Logic with np.where()
# In huge datasets, apply() can be slow because it acts like a Python loop.
# np.where(condition, value_if_true, value_if_false) is vectorized and 10x-50x faster!
df["salary_band"] = np.where(df["salary"] >= 60000, "High", "Standard")

print("--- Transformed DataFrame ---")
print(df[["employee", "salary", "status_name", "tax", "bonus", "salary_band"]])



# 4. Reshaping Data: melt() and pivot_table()

# A. pd.melt() (Unpivoting: Wide format → Long format)
# In Data Engineering, source reports often arrive in wide format (e.g., quarterly columns).
# Analytical databases (Snowflake, BigQuery) prefer tall/long normalized rows.

wide_sales = pd.DataFrame({
    "store": ["Delhi", "Mumbai"],
    "Q1": [10000, 15000],
    "Q2": [12000, 18000],
    "Q3": [11000, 16000],
    "Q4": [14000, 20000]
})
print("--- Wide Format ---")
print(wide_sales)

# Melting into Long Format:
long_sales = pd.melt(
    wide_sales,
    id_vars=["store"],                # Column to keep as identifier
    value_vars=["Q1", "Q2", "Q3", "Q4"], # Columns to unpivot
    var_name="quarter",              # Name for unpivoted header column
    value_name="revenue"             # Name for values column
)
print("--- Long Format (Melted) ---")
print(long_sales)
#output:
#     store quarter  revenue
# 0   Delhi      Q1    10000
# 1  Mumbai      Q1    15000
# 2   Delhi      Q2    12000
# ...


# B. pivot_table() (Long format → Summary table)
# Groups and aggregates data across rows and columns.
pivot_summary = long_sales.pivot_table(
    index="store",
    columns="quarter",
    values="revenue",
    aggfunc="sum"
)
print("--- Pivot Table ---")
print(pivot_summary)



# 5. String Manipulation (.str Accessor)

# Raw data from CSV or web scrapers usually has whitespace, mixed cases, or embedded codes.
messy_data = pd.DataFrame({
    "raw_name": ["  RAHUL sharma  ", "priya VERMA", " aman GUPTA "],
    "contact": ["DEL-9876543210", "MUM-9123456789", "BLR-9988776655"]
})

# Cleaning names:
messy_data["clean_name"] = messy_data["raw_name"].str.strip().str.title()

# Checking if string contains a substring:
delhi_mask = messy_data["contact"].str.contains("DEL")
print("Delhi Contacts:", messy_data[delhi_mask])

# Splitting string into multiple columns:
# expand=True returns a DataFrame with separate columns
messy_data[["city_code", "phone"]] = messy_data["contact"].str.split("-", expand=True)

print("--- Cleaned String Data ---")
print(messy_data[["clean_name", "city_code", "phone"]])



# 6. Window-like Operations (cumsum, shift, rank)

# In SQL, you use window functions: SUM() OVER (...), LAG(), RANK().
# Pandas has direct built-in equivalents.

sales_trend = pd.DataFrame({
    "date": pd.date_range(start="2026-03-01", periods=5),
    "daily_revenue": [1000, 1500, 1200, 2000, 1800]
})

# Running Total (SQL: SUM(daily_revenue) OVER (ORDER BY date))
sales_trend["running_total"] = sales_trend["daily_revenue"].cumsum()

# Previous Day's Revenue (SQL: LAG(daily_revenue, 1) OVER (ORDER BY date))
sales_trend["prev_day_revenue"] = sales_trend["daily_revenue"].shift(1)

# Day-over-Day Revenue Change:
sales_trend["dod_change"] = sales_trend["daily_revenue"] - sales_trend["prev_day_revenue"]

# Ranking (SQL: RANK() OVER (ORDER BY daily_revenue DESC))
sales_trend["rank"] = sales_trend["daily_revenue"].rank(ascending=False, method="min")

print("--- Window Functions in Pandas ---")
print(sales_trend)



#Practice Questions

#Q1: (Anti-Join Pattern)
#    Given `all_customers` and `purchased_customers`, find the names of customers who have NOT purchased anything yet.
#    Use a Left Join with `indicator=True` or check for nulls.

#solution:
all_cust = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "name": ["Rahul", "Aman", "Priya", "Sneha", "Vikram"]
})

purchased_cust = pd.DataFrame({
    "customer_id": [1, 3, 4],
    "order_id": [101, 102, 103]
})

merged = pd.merge(all_cust, purchased_cust, on="customer_id", how="left")
non_purchasers = merged[merged["order_id"].isna()]["name"].tolist()
print("Customers with zero orders:", non_purchasers)
#output: Customers with zero orders: ['Aman', 'Vikram']


#Q2: (Unpivoting with Melt)
#    You have employee monthly sales data in wide format:
#    Emp_ID, Jan, Feb, Mar
#    E1, 500, 600, 700
#    E2, 800, 750, 900
#    Transform this into long format with columns: Emp_ID, Month, Sales.

#solution:
wide_emp = pd.DataFrame({
    "Emp_ID": ["E1", "E2"],
    "Jan": [500, 800],
    "Feb": [600, 750],
    "Mar": [700, 900]
})

long_emp = pd.melt(
    wide_emp,
    id_vars=["Emp_ID"],
    value_vars=["Jan", "Feb", "Mar"],
    var_name="Month",
    value_name="Sales"
)
print("Long Format Employees:")
print(long_emp)


#Q3: (Vectorized Data Transformation)
#    Create a DataFrame with columns 'product' and 'stock'.
#    If stock == 0 → status = "Out of Stock"
#    If stock < 10 → status = "Low Stock"
#    Otherwise      → status = "In Stock"
#    Use np.select() for clean multi-condition vectorized logic.

#solution:
inventory = pd.DataFrame({
    "product": ["Keyboard", "Mouse", "Monitor", "Webcam"],
    "stock": [0, 5, 25, 8]
})

conditions = [
    inventory["stock"] == 0,
    inventory["stock"] < 10
]
choices = ["Out of Stock", "Low Stock"]

inventory["status"] = np.select(conditions, choices, default="In Stock")
print("Inventory Status:")
print(inventory)
