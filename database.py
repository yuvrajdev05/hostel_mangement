import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import pandas as pd
from datetime import datetime

def create_connection():
    """Create a database connection to the MySQL database"""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_tables():
    """Create tables if they don't exist"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        # Users table for authentication
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'student') NOT NULL
            )
        """)
        # Students table
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
        # Rooms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_number VARCHAR(10) UNIQUE NOT NULL,
                capacity INT NOT NULL,
                room_type VARCHAR(50),
                occupied INT DEFAULT 0
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()

def authenticate_user(username, password):
    """Authenticate user and return role"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result['role'] if result else None
    return None

def get_students():
    """Get all students"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    return []

def add_student(name, email, phone, room_number):
    """Add a new student"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO students (name, email, phone, room_number, check_in_date, status)
                VALUES (%s, %s, %s, %s, %s, 'active')
            """, (name, email, phone, room_number, datetime.now().date()))
            # Update room occupancy
            cursor.execute("UPDATE rooms SET occupied = occupied + 1 WHERE room_number = %s", (room_number,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error adding student: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    return False

def update_student(student_id, name, email, phone, room_number, status):
    """Update student details"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE students SET name = %s, email = %s, phone = %s, room_number = %s, status = %s
                WHERE id = %s
            """, (name, email, phone, room_number, status, student_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error updating student: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    return False

def delete_student(student_id):
    """Delete a student"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Get room number before deleting
            cursor.execute("SELECT room_number FROM students WHERE id = %s", (student_id,))
            room = cursor.fetchone()
            if room:
                cursor.execute("UPDATE rooms SET occupied = occupied - 1 WHERE room_number = %s", (room[0],))
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error deleting student: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    return False

def get_rooms():
    """Get all rooms"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rooms")
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    return []

def add_room(room_number, capacity, room_type):
    """Add a new room"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO rooms (room_number, capacity, room_type)
                VALUES (%s, %s, %s)
            """, (room_number, capacity, room_type))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error adding room: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    return False

def get_dashboard_data():
    """Get data for dashboard"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        data = {}
        cursor.execute("SELECT COUNT(*) as total_students FROM students WHERE status = 'active'")
        data['total_students'] = cursor.fetchone()['total_students']
        cursor.execute("SELECT COUNT(*) as total_rooms FROM rooms")
        data['total_rooms'] = cursor.fetchone()['total_rooms']
        cursor.execute("SELECT COUNT(*) as occupied_rooms FROM rooms WHERE occupied > 0")
        data['occupied_rooms'] = cursor.fetchone()['occupied_rooms']
        cursor.execute("SELECT SUM(capacity - occupied) as available_beds FROM rooms")
        available = cursor.fetchone()['available_beds']
        data['available_beds'] = available if available else 0
        cursor.close()
        connection.close()
        return data
    return {}

def export_students_to_csv():
    """Export students to CSV"""
    students = get_students()
    df = pd.DataFrame(students)
    filename = "students_export.csv"
    df.to_csv(filename, index=False)
    return filename

def export_rooms_to_csv():
    """Export rooms to CSV"""
    rooms = get_rooms()
    df = pd.DataFrame(rooms)
    filename = "rooms_export.csv"
    df.to_csv(filename, index=False)
    return filename

def export_students_to_pdf():
    """Export students to PDF"""
    students = get_students()
    filename = "students_export.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 50, "Students Report")
    y = height - 100
    for student in students:
        c.drawString(50, y, f"ID: {student['id']}, Name: {student['name']}, Email: {student['email']}, Room: {student['room_number']}")
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
    return filename

def export_rooms_to_pdf():
    """Export rooms to PDF"""
    rooms = get_rooms()
    filename = "rooms_export.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 50, "Rooms Report")
    y = height - 100
    for room in rooms:
        c.drawString(50, y, f"Room: {room['room_number']}, Capacity: {room['capacity']}, Type: {room['room_type']}, Occupied: {room['occupied']}")
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
    return filename
