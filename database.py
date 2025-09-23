import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'a4p')
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Database connection established successfully")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            # Try to create database if it doesn't exist
            self.create_database()

    def create_database(self):
        try:
            # Connect without specifying database
            temp_conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = temp_conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS a4p")
            print("Database 'a4p' created or already exists")
            cursor.close()
            temp_conn.close()
            
            # Reconnect to the specific database
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.create_tables()
        except Error as e:
            print(f"Error creating database: {e}")

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            
            # Create property_claims table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS property_claims (
                    policy_num VARCHAR(20) PRIMARY KEY,
                    ph_num BIGINT,
                    staff_id VARCHAR(20),
                    inc_date DATE,
                    inc_time TIME,
                    address VARCHAR(50),
                    property_type VARCHAR(20),
                    damage_type VARCHAR(20),
                    country VARCHAR(20),
                    emg_cont BIGINT,
                    descr VARCHAR(100),
                    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create motor_claims table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS motor_claims (
                    policy_num VARCHAR(20) PRIMARY KEY,
                    ph_num BIGINT,
                    staff_id VARCHAR(20),
                    inc_date DATE,
                    inc_time TIME,
                    plate_no VARCHAR(10),
                    colour VARCHAR(10),
                    engine_no BIGINT,
                    chasis_no VARCHAR(17),
                    km_reading BIGINT,
                    variant_year VARCHAR(30),
                    address VARCHAR(50),
                    country VARCHAR(20),
                    descr VARCHAR(100),
                    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create new_users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS new_users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    _name_ VARCHAR(30),
                    email VARCHAR(30) UNIQUE,
                    ph_no BIGINT,
                    country VARCHAR(20),
                    address VARCHAR(50),
                    pwd VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.connection.commit()
            print("Tables created successfully")
            cursor.close()
            
        except Error as e:
            print(f"Error creating tables: {e}")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().lower().startswith('select'):
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.lastrowid
            
            cursor.close()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

# Global database instance
db = Database()
