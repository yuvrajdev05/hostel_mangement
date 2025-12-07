import mysql.connector
from mysql.connector import Error

def create_database():
    """Create the hostel_management database"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS hostel_management")
            print("Database 'hostel_management' created successfully!")
            
            # Use the database
            cursor.execute("USE hostel_management")
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role ENUM('admin', 'student') NOT NULL
                )
            """)
            
            # Create students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    phone VARCHAR(20),
                    room_number VARCHAR(10),
                    check_in_date DATE,
                    check_out_date DATE,
                    status ENUM('active', 'inactive') DEFAULT 'active'
                )
            """)
            
            # Create rooms table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    room_number VARCHAR(10) UNIQUE NOT NULL,
                    capacity INT NOT NULL,
                    room_type VARCHAR(50),
                    occupied INT DEFAULT 0
                )
            """)
            
            # Insert default admin user
            cursor.execute("""
                INSERT IGNORE INTO users (username, password, role) 
                VALUES ('admin', 'admin123', 'admin')
            """)
            
            # Insert sample student user
            cursor.execute("""
                INSERT IGNORE INTO users (username, password, role) 
                VALUES ('student1', 'student123', 'student')
            """)
            
            connection.commit()
            print("Tables created successfully!")
            print("Default admin user: username='admin', password='admin123'")
            print("Default student user: username='student1', password='student123'")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()