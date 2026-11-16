#Day 07: Production Error Handling, Logging & Context Managers for Data Engineering 🚀

#In Day 06 we saw basic try/except. In production data pipelines, pipelines run on schedules (e.g., Airflow, Cron) without humans watching them.
#If a pipeline fails silently or crashes without clear logs, troubleshooting becomes a nightmare.
#Today we learn:
# 1. Advanced Exception Handling (else, finally, raise)
# 2. Custom Exceptions for Data Quality Checks
# 3. Python Logging Module (Replacing print in production)
# 4. Context Managers (with statement & custom resource managers)
# 5. Production Pipeline Pattern with Logging & Error Handling


# 1. The else and finally blocks

# try     → Runs code that might fail
# except  → Runs if an error occurs
# else    → Runs ONLY if no error occurred in try block
# finally → ALWAYS runs, no matter what (even if an error occurred or return was called)

def process_file(file_path):
    try:
        print(f"Opening file: {file_path}")
        file = open(file_path, "r")
        data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' was not found!")
    else:
        print(f"Success! Read {len(data)} characters.")
    finally:
        print("Cleanup: This block always executes (e.g., closing database connections, cleaning temporary files).")

# Testing with a non-existent file
process_file("missing_orders.csv")

# Why finally is critical in Data Engineering:
# When working with databases, network sockets, or locked files:
# db_connection = open_connection()
# try:
#     load_data(db_connection)
# finally:
#     db_connection.close()  # Ensures connection is NEVER left open even if loading crashes!



# 2. Raising Exceptions & Data Quality Checks

# In data engineering, dirty data is very common (negative age, missing IDs, future order dates).
# You can deliberately raise exceptions using the 'raise' keyword to stop bad data from corrupting your data warehouse.

def validate_transaction(record):
    if record["amount"] <= 0:
        raise ValueError(f"Invalid amount: {record['amount']}. Amount must be greater than zero.")
    if not record["customer_id"]:
        raise ValueError("Missing customer_id! Transaction cannot be processed.")
    return True

try:
    bad_record = {"transaction_id": 101, "customer_id": "CUST12", "amount": -500}
    validate_transaction(bad_record)
except ValueError as e:
    print(f"Validation Failed: {e}")

#output: Validation Failed: Invalid amount: -500. Amount must be greater than zero.



# 3. Custom Exceptions for Data Pipelines

# Python lets you create your own exception classes by inheriting from Exception.
# Custom exceptions make debugging large pipelines much easier.

class DataValidationError(Exception):
    """Raised when incoming data violates business validation rules."""
    pass

class SchemaMismatchError(Exception):
    """Raised when columns in incoming file do not match expected schema."""
    pass

def check_schema(df_columns, expected_columns):
    missing_cols = set(expected_columns) - set(df_columns)
    if missing_cols:
        raise SchemaMismatchError(f"Incoming data is missing required columns: {missing_cols}")

expected = ["order_id", "customer_id", "amount", "date"]
incoming = ["order_id", "amount"]

try:
    check_schema(incoming, expected)
except SchemaMismatchError as err:
    print(f"Pipeline Stopped: {err}")

#output: Pipeline Stopped: Incoming data is missing required columns: {'date', 'customer_id'}



# 4. Python Logging Module (Production Data Engineering)

# NEVER use print() in production data pipelines!
# Why print() is bad for Data Engineering:
# 1. print() only outputs to console; it cannot be categorized by severity.
# 2. print() doesn't include timestamps, line numbers, or module names.
# 3. print() cannot easily write simultaneously to file, stdout, and cloud monitoring tools (like AWS CloudWatch, Datadog).

# Python provides the built-in 'logging' module.
import logging

# Standard Log Levels (from lowest to highest severity):
# DEBUG    → Detailed diagnostic information (used during development)
# INFO     → Confirmation that pipeline steps are working as expected
# WARNING  → Something unexpected happened, but pipeline can continue
# ERROR    → A serious problem occurred; a step failed
# CRITICAL → Fatal error; the entire pipeline must abort

# Configuring logging:
logging.basicConfig(
    level=logging.INFO, # Sets minimum level to log
    format="%(asctime)s [%(levelname)s] - %(message)s", # Timestamp, level, and message
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("ETL_Pipeline")

logger.info("Pipeline started.")
logger.debug("Connecting to staging storage...")  # Won't print because level is INFO
logger.warning("Record 45 has missing email; defaulting to null.")
logger.error("Failed to load table 'dim_users'.")
logger.critical("Database connection timed out! Aborting job.")

# Logging Exceptions with Stack Trace:
# In an except block, use logger.error(..., exc_info=True) or logger.exception(...)
try:
    res = 100 / 0
except ZeroDivisionError:
    logger.exception("Calculation failed in pipeline step!")



# 5. Context Managers (with Statement)

# You already used 'with open(...) as file:'.
# A context manager guarantees that resources are properly set up before and cleaned up after a code block,
# even if an unexpected error occurs.

# Under the hood, any context manager implements two methods:
# 1. __enter__() → Runs when entering the 'with' block
# 2. __exit__()  → Runs when exiting the 'with' block (handles cleanup)

# Example: Custom Pipeline Timer Context Manager
import time

class PipelineTimer:
    def __init__(self, step_name):
        self.step_name = step_name

    def __enter__(self):
        self.start_time = time.time()
        print(f"--- Starting: {self.step_name} ---")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = round(time.time() - self.start_time, 4)
        print(f"--- Completed: {self.step_name} in {duration} seconds ---")
        # Returning False allows any exception to propagate normally
        return False

# Usage:
with PipelineTimer("Data Transformation Step"):
    total = sum([i * i for i in range(1000000)])
    print("Done math calculation.")

#output:
# --- Starting: Data Transformation Step ---
# Done math calculation.
# --- Completed: Data Transformation Step in 0.0521 seconds ---


# Alternative: Creating Context Managers using contextlib
from contextlib import contextmanager

@contextmanager
def managed_database_session(db_name):
    print(f"[DB] Connected to database '{db_name}'")
    try:
        yield f"Connection({db_name})"
    finally:
        print(f"[DB] Closed connection to database '{db_name}' safely.")

with managed_database_session("analytics_dw") as conn:
    print(f"Executing queries using {conn}...")



# 6. Complete Data Engineering Mini Pipeline with Logging & Validation

import csv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
pipeline_logger = logging.getLogger("OrderETL")

raw_orders = [
    {"order_id": "101", "product": "Mouse", "price": "500", "qty": "2"},
    {"order_id": "102", "product": "Keyboard", "price": "invalid_price", "qty": "1"}, # bad record
    {"order_id": "103", "product": "Monitor", "price": "15000", "qty": "1"},
    {"order_id": "104", "product": "Desk", "price": "-2000", "qty": "1"},              # negative price
]

def transform_order_records(records):
    pipeline_logger.info(f"Starting transformation for {len(records)} records.")
    valid_records = []
    skipped_count = 0

    for record in records:
        try:
            order_id = int(record["order_id"])
            price = float(record["price"])
            qty = int(record["qty"])

            if price <= 0 or qty <= 0:
                raise ValueError("Price and quantity must be positive.")

            total_amount = price * qty
            valid_records.append({
                "order_id": order_id,
                "product": record["product"],
                "total_amount": total_amount
            })

        except (ValueError, KeyError) as e:
            pipeline_logger.warning(f"Skipping bad record (order_id={record.get('order_id')}): {e}")
            skipped_count += 1
            continue

    pipeline_logger.info(f"Transformation complete. Valid: {len(valid_records)}, Skipped: {skipped_count}")
    return valid_records

processed_orders = transform_order_records(raw_orders)
print("Processed Orders:", processed_orders)



#Practice Questions

#Q1: Create a custom exception called `NegativeSalaryError`. Write a function `calculate_net_salary(gross, deductions)`
#    that calculates net salary (gross - deductions). If either gross is negative or deductions > gross, raise `NegativeSalaryError`.
#    Handle the error using try/except.

#solution:
class NegativeSalaryError(Exception):
    pass

def calculate_net_salary(gross, deductions):
    if gross < 0:
        raise NegativeSalaryError("Gross salary cannot be negative.")
    if deductions > gross:
        raise NegativeSalaryError("Deductions cannot exceed gross salary.")
    return gross - deductions

try:
    net = calculate_net_salary(50000, 60000)
    print("Net Salary:", net)
except NegativeSalaryError as e:
    print(f"Error caught: {e}")

#output: Error caught: Deductions cannot exceed gross salary.


#Q2: Write a pipeline logger that writes logs to a file named 'pipeline.log' with level INFO.
#    Process a list of user dictionaries:
#    users = [
#        {"id": 1, "email": "rahul@gmail.com"},
#        {"id": 2, "email": None},
#        {"id": 3, "email": "aman@yahoo.com"}
#    ]
#    For valid emails, log an INFO message. For missing/None emails, log a WARNING message.

#solution:
import logging

file_logger = logging.getLogger("UserValidator")
handler = logging.FileHandler("pipeline.log", mode="w")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
file_logger.addHandler(handler)
file_logger.setLevel(logging.INFO)

users = [
    {"id": 1, "email": "rahul@gmail.com"},
    {"id": 2, "email": None},
    {"id": 3, "email": "aman@yahoo.com"}
]

for user in users:
    if user.get("email"):
        file_logger.info(f"User {user['id']} has valid email: {user['email']}")
    else:
        file_logger.warning(f"User {user['id']} is missing email address!")


#Q3: Implement a context manager `PipelineAudit` using `@contextmanager`.
#    When entering, it prints: "[AUDIT] Pipeline run started".
#    Inside the with block, simulate processing records.
#    When exiting, it prints: "[AUDIT] Pipeline run finished successfully" if no error occurred,
#    or "[AUDIT] Pipeline failed with error: <error_message>" if an error occurred.

#solution:
from contextlib import contextmanager

@contextmanager
def pipeline_audit(pipeline_name):
    print(f"[AUDIT] Pipeline '{pipeline_name}' started.")
    try:
        yield
        print(f"[AUDIT] Pipeline '{pipeline_name}' finished successfully.")
    except Exception as e:
        print(f"[AUDIT] Pipeline '{pipeline_name}' failed with error: {e}")
        raise # re-raise exception so caller is notified

try:
    with pipeline_audit("Daily_Sales_Sync"):
        print("Transforming sales records...")
        # Simulating work
        records = [10, 20, 30]
        print(f"Loaded {len(records)} records.")
except Exception:
    pass
