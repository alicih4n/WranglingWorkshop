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


def create_tables(conn):
    """Creates the departments and employees tables with FK relationship."""
    commands = (
        """
        DROP TABLE IF EXISTS employees;
        DROP TABLE IF EXISTS departments;
        """,
        """
        CREATE TABLE departments (
            dept_id SERIAL PRIMARY KEY,
            dept_name VARCHAR(255) UNIQUE NOT NULL,
            location VARCHAR(255),
            budget FLOAT
        )
        """,
        """
        CREATE TABLE employees (
            employee_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            position VARCHAR(255),
            start_date DATE,
            salary FLOAT,
            dept_id INTEGER,
            FOREIGN KEY (dept_id) REFERENCES departments (dept_id)
        )
        """
    )
    try:
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        cur.close()
        print("Tables 'departments' and 'employees' created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

def generate_departments():
    """Generates static department data."""
    depts = [
        ("Engineering", "Building A", 5000000.00),
        ("Data Science", "Building B", 3500000.00),
        ("Product", "Building A", 2000000.00),
        ("Sales", "Building C", 4500000.00),
        ("HR", "Building D", 1500000.00)
    ]
    return depts # Returns list of tuples (name, loc, budget)

def generate_employees(num_records, dirty_prob):
    """Generates synthetic employee data linked to departments."""
    data = []
    
    positions_list = [
        "Software Engineer", "Data Scientist", "Project Manager", 
        "HR Specialist", "Marketing Manager", "Sales Associate",
        "Product Owner", "DevOps Engineer", "QA Analyst", "System Admin"
    ]
    
    # Map positions to likely departments for realism (optional, but good)
    # dept_ids are 1 to 5 based on insertion order above
    
    for _ in range(num_records):
        is_dirty = random.random() < dirty_prob
        
        # Basic fields
        name = fake.name()
        position = random.choice(positions_list)
        # Fix date generation to strictly align with notebook's 2024 analysis year
        start_date = fake.date_between(start_date='-9y', end_date=datetime.date(2024, 12, 31))
        salary = round(random.uniform(50000, 150000), 2)
        dept_id = random.randint(1, 5) # Randomly assign to one of the 5 depts
        
        if is_dirty:
            dirty_choice = random.choice(['missing_name', 'missing_salary', 'bad_casing', 'logic_error'])
            
            if dirty_choice == 'missing_name':
                name = None 
            elif dirty_choice == 'missing_salary':
                salary = None 
            elif dirty_choice == 'bad_casing':
                if random.random() > 0.5:
                    position = position.lower()
                else:
                    position = position.upper()
            elif dirty_choice == 'logic_error':
                if random.random() > 0.5:
                     start_date = fake.date_between(start_date='-20y', end_date='-11y') 
                else:
                     start_date = fake.date_between(start_date='+1y', end_date='+2y') 
        
        data.append((name, position, start_date, salary, dept_id))
        
    return data

def insert_data(conn, depts, employees):
    """Inserts generated data into both tables."""
    insert_dept = "INSERT INTO departments (dept_name, location, budget) VALUES (%s, %s, %s)"
    insert_emp = "INSERT INTO employees (name, position, start_date, salary, dept_id) VALUES (%s, %s, %s, %s, %s)"
    
    try:
        cur = conn.cursor()
        # Insert Departments first (Parent table)
        cur.executemany(insert_dept, depts)
        conn.commit()
        print(f"Successfully inserted {len(depts)} departments.")
        
        # Insert Employees (Child table with FK)
        cur.executemany(insert_emp, employees)
        conn.commit()
        print(f"Successfully inserted {len(employees)} employees.")
        
        cur.close()
    except Exception as e:
        print(f"Error inserting data: {e}")

def main():
    print("--- Starting Lab 3 Data Generation (Multi-Table) ---")
    
    conn = get_db_connection()
    if not conn: return
        
    create_tables(conn)
    
    print("Generating schema data...")
    depts = generate_departments()
    emp_data = generate_employees(NUM_RECORDS, DIRTY_PERCENTAGE)
    
    insert_data(conn, depts, emp_data)
    
    conn.close()
    print("--- Data Generation Complete ---")

if __name__ == "__main__":
    main()
