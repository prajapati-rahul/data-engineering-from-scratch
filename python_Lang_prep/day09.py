#Day 09: Memory Optimization, Iterators & Generators for Big Data Processing 🧠⚡

#In Data Engineering, you will often work with datasets that are 10GB, 50GB, or even 500GB in size.
#If your laptop or server has only 8GB or 16GB of RAM, running:
#    df = pd.read_csv("huge_file.csv")
#will crash your program with a MemoryError (Out Of Memory / OOM)!

#To solve this, Data Engineers use:
# 1. Iterators & Iterables
# 2. Generators & the yield keyword (Lazy Evaluation)
# 3. Processing Large Files in Chunks (Pandas chunksize)
# 4. Pandas Memory Optimization (Downcasting dtypes & categorical data)
# 5. Building a Streaming ETL Pipeline
# 6. Practice Questions with Solutions


import sys
import pandas as pd
import numpy as np


# 1. The Memory Problem: Lists vs Generators

# A list stores ALL elements in memory at the same time.
# A generator generates ONE element at a time on demand (Lazy Evaluation).

# Let's compare memory consumption:
list_data = [x for x in range(1000000)]       # 1 Million numbers stored in RAM
gen_data = (x for x in range(1000000))        # 1 Million numbers generated on the fly

print("--- Memory Comparison ---")
print(f"Memory used by List:      {sys.getsizeof(list_data)} bytes (~8 MB)")
print(f"Memory used by Generator: {sys.getsizeof(gen_data)} bytes (Only ~100 bytes!)")

# Notice: The generator takes almost ZERO memory regardless of whether there are 1,000 or 1,000,000,000 items!



# 2. Iterators & Iterables Under the Hood

# An Iterable is an object you can loop over (like list, tuple, string, dict).
# An Iterator is an object that remembers its current position during iteration.

fruits = ["Apple", "Banana", "Cherry"]

# Getting an iterator using iter()
fruit_iter = iter(fruits)

# Getting elements one by one using next()
print(next(fruit_iter))  # Apple
print(next(fruit_iter))  # Banana
print(next(fruit_iter))  # Cherry

# If you call next() after elements are exhausted, Python raises StopIteration:
# print(next(fruit_iter)) # Raises StopIteration!
# Python's for loop automatically handles StopIteration behind the scenes.



# 3. Generators and the 'yield' Keyword

# When a function contains the 'yield' keyword instead of 'return', it becomes a Generator Function.
# - 'return' terminates the function immediately and returns a single value.
# - 'yield' produces a value, PAUSES execution, and saves state for the next call.

def number_stream(n):
    for i in range(1, n + 1):
        print(f"[Generating number {i}]")
        yield i

gen = number_stream(3)
print(next(gen))  # Runs until first yield -> returns 1
print(next(gen))  # Resumes from paused state -> returns 2
print(next(gen))  # Resumes -> returns 3


# Real Data Engineering Use Case: Reading a massive log file line-by-line
def stream_log_file(file_path):
    """
    Streams a log file line by line without ever loading the full file into memory.
    Safe for 100GB+ files!
    """
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()

# Usage in pipeline:
# for log_entry in stream_log_file("server_logs.txt"):
#     if "ERROR" in log_entry:
#         process_error(log_entry)



# 4. Processing Massive Files in Chunks with Pandas

# Pandas provides the `chunksize` parameter in `read_csv()`.
# Instead of loading all rows at once, it returns an Iterator of smaller DataFrames (chunks)!

# Creating a simulated large dataset:
sales_data = pd.DataFrame({
    "order_id": range(1, 10001),
    "category": np.random.choice(["Electronics", "Clothing", "Home", "Books"], 10000),
    "amount": np.random.randint(100, 5000, 10000)
})
sales_data.to_csv("large_sales.csv", index=False)

# Processing chunk-by-chunk:
# Goal: Calculate total revenue and average order amount across 10,000 rows without loading all into memory at once!
chunk_size = 2000
total_revenue = 0
total_orders = 0

print("--- Processing in Chunks ---")
for chunk in pd.read_csv("large_sales.csv", chunksize=chunk_size):
    # 'chunk' is a normal DataFrame of 2000 rows
    total_revenue += chunk["amount"].sum()
    total_orders += len(chunk)
    print(f"Processed chunk of {len(chunk)} rows. Subtotal revenue so far: ₹{total_revenue}")

avg_order_value = round(total_revenue / total_orders, 2)
print(f"Final Total Orders: {total_orders}, Total Revenue: ₹{total_revenue}, Avg: ₹{avg_order_value}")



# 5. Memory Optimization in Pandas (Dtypes & Categorical Data)

# By default, Pandas assigns:
# - int64 (8 bytes per integer)
# - float64 (8 bytes per float)
# - object (very inefficient memory usage for repeated strings)

# In Data Engineering, optimizing dtypes can reduce memory usage by 70% to 90%!

sample_df = pd.DataFrame({
    "user_id": np.random.randint(1, 1000, 50000),             # values fit easily in int16 or int32
    "rating": np.random.choice([1, 2, 3, 4, 5], 50000),        # values 1 to 5 fit in int8 (-128 to 127)
    "city": np.random.choice(["Delhi", "Mumbai", "Bangalore", "Pune"], 50000) # Only 4 distinct strings repeated 50k times!
})

# Checking initial memory usage:
initial_memory = sample_df.memory_usage(deep=True).sum() / (1024 * 1024)
print(f"\nInitial DataFrame Memory Usage: {initial_memory:.2f} MB")

# Optimizing dtypes:
sample_df["user_id"] = sample_df["user_id"].astype("int32")
sample_df["rating"] = sample_df["rating"].astype("int8")

# Crucial for Data Engineering: Convert low-cardinality string columns to category!
sample_df["city"] = sample_df["city"].astype("category")

# Checking optimized memory usage:
optimized_memory = sample_df.memory_usage(deep=True).sum() / (1024 * 1024)
print(f"Optimized DataFrame Memory Usage: {optimized_memory:.2f} MB")
reduction = ((initial_memory - optimized_memory) / initial_memory) * 100
print(f"Memory Reduced by: {reduction:.1f}%! 🚀")



# 6. Streaming ETL Pipeline Pattern (Producer → Transformer → Consumer)

# Real production streaming architecture using Python generators:
# Memory complexity is O(1) because records flow one-by-one through the pipeline!

# Step 1: Producer (Generates or reads raw records)
def record_producer():
    raw_stream = [
        "101,Laptop,55000,COMPLETED",
        "102,Mouse,,FAILED",               # missing price
        "103,Keyboard,1500,COMPLETED",
        "104,Monitor,18000,COMPLETED",
        "105,Phone,25000,CANCELLED"
    ]
    for row in raw_stream:
        yield row

# Step 2: Transformer (Cleans and filters records)
def record_transformer(records):
    for raw in records:
        parts = raw.split(",")
        order_id, product, price, status = parts[0], parts[1], parts[2], parts[3]

        # Filter only COMPLETED orders with valid price
        if status == "COMPLETED" and price != "":
            yield {
                "order_id": int(order_id),
                "product": product,
                "price": float(price)
            }

# Step 3: Consumer (Loads or aggregates data)
def record_consumer(valid_stream):
    total = 0
    count = 0
    for record in valid_stream:
        print(f"Loaded into warehouse: {record}")
        total += record["price"]
        count += 1
    print(f"Summary: Ingested {count} orders. Total: ₹{total}")

# Connecting the pipeline stages:
# Notice how elegant this is: no lists or DataFrames stored in memory!
raw = record_producer()
clean = record_transformer(raw)
record_consumer(clean)



#Practice Questions

#Q1: Write a generator function `filter_errors(logs)` that takes a list of log strings
#    and yields only logs that start with "[ERROR]".
#    logs = [
#        "[INFO] System started",
#        "[ERROR] Database connection failed",
#        "[WARNING] Disk space low",
#        "[ERROR] Table orders not found"
#    ]

#solution:
def filter_errors(logs):
    for log in logs:
        if log.startswith("[ERROR]"):
            yield log

logs = [
    "[INFO] System started",
    "[ERROR] Database connection failed",
    "[WARNING] Disk space low",
    "[ERROR] Table orders not found"
]

for error in filter_errors(logs):
    print("Found Error:", error)


#Q2: Write a generator function `batch_generator(data, batch_size)` that splits a large list
#    into smaller batches of size `batch_size` and yields each batch as a list.
#    Test it with numbers 1 to 10 and batch_size = 3.

#solution:
def batch_generator(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

numbers = list(range(1, 11))
for batch in batch_generator(numbers, batch_size=3):
    print("Ingesting batch:", batch)
#output:
# Ingesting batch: [1, 2, 3]
# Ingesting batch: [4, 5, 6]
# Ingesting batch: [7, 8, 9]
# Ingesting batch: [10]


#Q3: Create a DataFrame with 10,000 rows containing columns: 'id', 'department', 'status'.
#    - 'id' from 1 to 10000
#    - 'department' chosen randomly from ['HR', 'Engineering', 'Finance', 'Sales']
#    - 'status' chosen randomly from ['Active', 'On Leave', 'Resigned']
#    Print memory usage, convert 'department' and 'status' to category dtype,
#    and print new memory usage with percentage reduction.

#solution:
df = pd.DataFrame({
    "id": range(1, 10001),
    "department": np.random.choice(["HR", "Engineering", "Finance", "Sales"], 10000),
    "status": np.random.choice(["Active", "On Leave", "Resigned"], 10000)
})

mem_before = df.memory_usage(deep=True).sum() / 1024 # in KB
df["department"] = df["department"].astype("category")
df["status"] = df["status"].astype("category")
mem_after = df.memory_usage(deep=True).sum() / 1024 # in KB

print(f"Memory before: {mem_before:.2f} KB")
print(f"Memory after:  {mem_after:.2f} KB")
print(f"Reduction:     {((mem_before - mem_after) / mem_before) * 100:.2f}%")
