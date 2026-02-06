import psycopg2
from faker import Faker
import random
import numpy as np
import datetime

# --- Configuration ---
DB_URL = "postgresql://neondb_owner:npg_a2cfwEmDp5ig@ep-noisy-grass-ai9zgc4l-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
NUM_RECORDS = 500
DIRTY_PERCENTAGE = 0.20

fake = Faker()

def get_db_connection():
    """Establishes a connection to the Neon database."""
    try:
        conn = psycopg2.connect(DB_URL)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    """Creates the employees table if it doesn't exist."""
    create_table_query = """
    DROP TABLE IF EXISTS employees;
    CREATE TABLE employees (
        employee_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        position VARCHAR(255),
        start_date DATE,
        salary FLOAT
    );
    """
    try:
        cur = conn.cursor()
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        print("Table 'employees' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

def generate_data(num_records, dirty_prob):
    """Generates synthetic data with injected errors."""
    data = []
    
    positions_list = [
        "Software Engineer", "Data Scientist", "Project Manager", 
        "HR Specialist", "Marketing Manager", "Sales Associate",
        "Product Owner", "DevOps Engineer", "QA Analyst", "System Admin"
    ]
    
    for _ in range(num_records):
        is_dirty = random.random() < dirty_prob
        
        # Basic fields
        name = fake.name()
        position = random.choice(positions_list)
        start_date = fake.date_between(start_date='-10y', end_date='today')
        salary = round(random.uniform(50000, 150000), 2)
        
        if is_dirty:
            dirty_choice = random.choice(['missing_name', 'missing_salary', 'bad_casing', 'logic_error'])
            
            if dirty_choice == 'missing_name':
                name = None # Simulate missing name for SQL (will be NULL)
            
            elif dirty_choice == 'missing_salary':
                salary = None # Simulate missing salary
                
            elif dirty_choice == 'bad_casing':
                # Randomly lowercase or uppercase
                if random.random() > 0.5:
                    position = position.lower()
                else:
                    position = position.upper()
                    
            elif dirty_choice == 'logic_error':
                # invalid dates (prospectively in future or way past)
                # Note: modifying date to be outside reasonable range [2015-2024]
                # Lab requirement says: "dates before 2015 or after 2024"
                # To be safe with SQL DATE type, stick to valid calendar dates but outside the logic range.
                if random.random() > 0.5:
                     start_date = fake.date_between(start_date='-20y', end_date='-11y') # Before 2015
                else:
                     start_date = fake.date_between(start_date='+1y', end_date='+2y') # Future date
        
        data.append((name, position, start_date, salary))
        
    return data

def insert_data(conn, data):
    """Inserts generated data into the database."""
    insert_query = "INSERT INTO employees (name, position, start_date, salary) VALUES (%s, %s, %s, %s)"
    try:
        cur = conn.cursor()
        cur.executemany(insert_query, data)
        conn.commit()
        cur.close()
        print(f"Successfully inserted {len(data)} records.")
    except Exception as e:
        print(f"Error inserting data: {e}")

def main():
    print("--- Starting Lab 3 Data Generation ---")
    
    # 1. Connect
    conn = get_db_connection()
    if not conn:
        return
        
    # 2. Create Table
    create_table(conn)
    
    # 3. Generate Data
    print(f"Generating {NUM_RECORDS} records with {int(DIRTY_PERCENTAGE*100)}% dirty data probability...")
    dataset = generate_data(NUM_RECORDS, DIRTY_PERCENTAGE)
    
    # 4. Insert Data
    insert_data(conn, dataset)
    
    conn.close()
    print("--- Data Generation Complete ---")

if __name__ == "__main__":
    main()
