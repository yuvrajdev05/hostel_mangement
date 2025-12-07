import os
import csv
import pandas as pd
from datetime import datetime
import json

class StorageManager:
    def __init__(self):
        self.use_mysql = False
        self.connection = None
        self.data_dir = "data"
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Try to connect to MySQL first
        self._try_mysql_connection()
        
        if not self.use_mysql:
            print("MySQL not available. Using CSV files for data storage.")
            self._initialize_csv_files()
    
    def _try_mysql_connection(self):
        try:
            import mysql.connector
            from mysql.connector import Error
            
            # Try to connect to MySQL
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root'
            )
            
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                # Create database if it doesn't exist
                cursor.execute("CREATE DATABASE IF NOT EXISTS hostel_management")
                cursor.execute("USE hostel_management")
                
                # Create tables
                self._create_mysql_tables(cursor)
                self.connection.commit()
                cursor.close()
                
                self.use_mysql = True
                print("Connected to MySQL database successfully!")
                
        except Exception as e:
            print(f"MySQL connection failed: {e}")
            self.use_mysql = False
            if self.connection:
                self.connection.close()
    
    def _create_mysql_tables(self, cursor):
        # Users table
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
        
        # Insert default users
        cursor.execute("""
            INSERT IGNORE INTO users (username, password, role) 
            VALUES ('admin', 'admin123', 'admin')
        """)
        cursor.execute("""
            INSERT IGNORE INTO users (username, password, role) 
            VALUES ('student1', 'student123', 'student')
        """)
    
    def _initialize_csv_files(self):
        # Initialize CSV files with headers if they don't exist
        files_config = {
            'users.csv': ['id', 'username', 'password', 'role'],
            'students.csv': ['id', 'name', 'email', 'phone', 'room_number', 'check_in_date', 'check_out_date', 'status'],
            'rooms.csv': ['id', 'room_number', 'capacity', 'room_type', 'occupied']
        }
        
        for filename, headers in files_config.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
        
        # Add default users if users.csv is empty
        users_file = os.path.join(self.data_dir, 'users.csv')
        if os.path.getsize(users_file) <= len(','.join(files_config['users.csv'])) + 1:
            with open(users_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([1, 'admin', 'admin123', 'admin'])
                writer.writerow([2, 'student1', 'student123', 'student'])
    
    def _get_next_id(self, filename):
        filepath = os.path.join(self.data_dir, filename)
        try:
            df = pd.read_csv(filepath)
            return df['id'].max() + 1 if not df.empty else 1
        except:
            return 1
    
    # Authentication
    def authenticate_user(self, username, password):
        if self.use_mysql:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            cursor.close()
            return result['role'] if result else None
        else:
            try:
                df = pd.read_csv(os.path.join(self.data_dir, 'users.csv'))
                user = df[(df['username'] == username) & (df['password'] == password)]
                return user.iloc[0]['role'] if not user.empty else None
            except:
                return None
    
    # Students operations
    def get_students(self):
        if self.use_mysql:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students")
            results = cursor.fetchall()
            cursor.close()
            return results
        else:
            try:
                df = pd.read_csv(os.path.join(self.data_dir, 'students.csv'))
                return df.to_dict('records')
            except:
                return []
    
    def add_student(self, name, email, phone, room_number):
        if self.use_mysql:
            cursor = self.connection.cursor()
            try:
                cursor.execute("""
                    INSERT INTO students (name, email, phone, room_number, check_in_date, status)
                    VALUES (%s, %s, %s, %s, %s, 'active')
                """, (name, email, phone, room_number, datetime.now().date()))
                cursor.execute("UPDATE rooms SET occupied = occupied + 1 WHERE room_number = %s", (room_number,))
                self.connection.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error adding student: {e}")
                self.connection.rollback()
                cursor.close()
                return False
        else:
            try:
                new_id = self._get_next_id('students.csv')
                with open(os.path.join(self.data_dir, 'students.csv'), 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([new_id, name, email, phone, room_number, datetime.now().date(), '', 'active'])
                
                # Update room occupancy
                self._update_room_occupancy(room_number, 1)
                return True
            except Exception as e:
                print(f"Error adding student: {e}")
                return False
    
    def update_student(self, student_id, name, email, phone, room_number, status):
        if self.use_mysql:
            cursor = self.connection.cursor()
            try:
                cursor.execute("""
                    UPDATE students SET name = %s, email = %s, phone = %s, room_number = %s, status = %s
                    WHERE id = %s
                """, (name, email, phone, room_number, status, student_id))
                self.connection.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error updating student: {e}")
                cursor.close()
                return False
        else:
            try:
                df = pd.read_csv(os.path.join(self.data_dir, 'students.csv'))
                df.loc[df['id'] == student_id, ['name', 'email', 'phone', 'room_number', 'status']] = [name, email, phone, room_number, status]
                df.to_csv(os.path.join(self.data_dir, 'students.csv'), index=False)
                return True
            except Exception as e:
                print(f"Error updating student: {e}")
                return False
    
    def delete_student(self, student_id):
        if self.use_mysql:
            cursor = self.connection.cursor()
            try:
                cursor.execute("SELECT room_number FROM students WHERE id = %s", (student_id,))
                room = cursor.fetchone()
                if room:
                    cursor.execute("UPDATE rooms SET occupied = occupied - 1 WHERE room_number = %s", (room[0],))
                cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
                self.connection.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error deleting student: {e}")
                cursor.close()
                return False
        else:
            try:
                df = pd.read_csv(os.path.join(self.data_dir, 'students.csv'))
                student = df[df['id'] == student_id]
                if not student.empty:
                    room_number = student.iloc[0]['room_number']
                    self._update_room_occupancy(room_number, -1)
                df = df[df['id'] != student_id]
                df.to_csv(os.path.join(self.data_dir, 'students.csv'), index=False)
                return True
            except Exception as e:
                print(f"Error deleting student: {e}")
                return False
    
    # Rooms operations
    def get_rooms(self):
        if self.use_mysql:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM rooms")
            results = cursor.fetchall()
            cursor.close()
            return results
        else:
            try:
                df = pd.read_csv(os.path.join(self.data_dir, 'rooms.csv'))
                return df.to_dict('records')
            except:
                return []
    
    def add_room(self, room_number, capacity, room_type):
        if self.use_mysql:
            cursor = self.connection.cursor()
            try:
                cursor.execute("""
                    INSERT INTO rooms (room_number, capacity, room_type)
                    VALUES (%s, %s, %s)
                """, (room_number, capacity, room_type))
                self.connection.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error adding room: {e}")
                cursor.close()
                return False
        else:
            try:
                new_id = self._get_next_id('rooms.csv')
                with open(os.path.join(self.data_dir, 'rooms.csv'), 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([new_id, room_number, capacity, room_type, 0])
                return True
            except Exception as e:
                print(f"Error adding room: {e}")
                return False
    
    def _update_room_occupancy(self, room_number, change):
        if not self.use_mysql:
            try:
                df = pd.read_csv(os.path.join(self.data_dir, 'rooms.csv'))
                df.loc[df['room_number'] == room_number, 'occupied'] += change
                df.to_csv(os.path.join(self.data_dir, 'rooms.csv'), index=False)
            except Exception as e:
                print(f"Error updating room occupancy: {e}")
    
    # Dashboard data
    def get_dashboard_data(self):
        if self.use_mysql:
            cursor = self.connection.cursor(dictionary=True)
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
            return data
        else:
            try:
                students_df = pd.read_csv(os.path.join(self.data_dir, 'students.csv'))
                rooms_df = pd.read_csv(os.path.join(self.data_dir, 'rooms.csv'))
                
                data = {
                    'total_students': len(students_df[students_df['status'] == 'active']),
                    'total_rooms': len(rooms_df),
                    'occupied_rooms': len(rooms_df[rooms_df['occupied'] > 0]),
                    'available_beds': (rooms_df['capacity'] - rooms_df['occupied']).sum()
                }
                return data
            except:
                return {'total_students': 0, 'total_rooms': 0, 'occupied_rooms': 0, 'available_beds': 0}
    
    # Export functions
    def export_students_to_csv(self):
        students = self.get_students()
        df = pd.DataFrame(students)
        filename = f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        return filename
    
    def export_rooms_to_csv(self):
        rooms = self.get_rooms()
        df = pd.DataFrame(rooms)
        filename = f"rooms_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        return filename
    
    def export_students_to_pdf(self):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            
            students = self.get_students()
            filename = f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            c.drawString(100, height - 50, "Students Report")
            y = height - 100
            for student in students:
                c.drawString(50, y, f"ID: {student['id']}, Name: {student['name']}, Email: {student['email']}, Room: {student.get('room_number', 'N/A')}")
                y -= 20
                if y < 50:
                    c.showPage()
                    y = height - 50
            c.save()
            return filename
        except ImportError:
            print("ReportLab not available. Cannot export to PDF.")
            return None
    
    def export_rooms_to_pdf(self):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            
            rooms = self.get_rooms()
            filename = f"rooms_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            c.drawString(100, height - 50, "Rooms Report")
            y = height - 100
            for room in rooms:
                c.drawString(50, y, f"Room: {room['room_number']}, Capacity: {room['capacity']}, Type: {room.get('room_type', 'N/A')}, Occupied: {room.get('occupied', 0)}")
                y -= 20
                if y < 50:
                    c.showPage()
                    y = height - 50
            c.save()
            return filename
        except ImportError:
            print("ReportLab not available. Cannot export to PDF.")
            return None