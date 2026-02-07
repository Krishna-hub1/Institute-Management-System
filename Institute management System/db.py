"""
Database Layer for Student Management System
Handles all database operations with PyMySQL
"""

import pymysql
from config import DB_CONFIG
import os

class Database:
    """Database handler class for all database operations"""

    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = pymysql.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            print(f"Connection Error: {e}")
            return False

    def create_database(self):
        """Create database if it doesn't exist"""
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            self.cursor.execute(f"USE {DB_CONFIG['database']}")
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Database Creation Error: {e}")
            return False

    def create_tables(self):
        """Create all required tables if they don't exist"""
        try:
            # Students Table
            students_table = """
            CREATE TABLE IF NOT EXISTS students (
                student_id VARCHAR(20) PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                gender ENUM('Male', 'Female', 'Other') NOT NULL,
                dob DATE NOT NULL,
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(15),
                address TEXT,
                course_id INT,
                admission_date DATE NOT NULL,
                photo_path VARCHAR(255),
                status ENUM('Active', 'Inactive', 'Graduated') DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
            )
            """

            # Courses Table
            courses_table = """
            CREATE TABLE IF NOT EXISTS courses (
                course_id INT AUTO_INCREMENT PRIMARY KEY,
                course_name VARCHAR(100) NOT NULL UNIQUE,
                course_code VARCHAR(20) NOT NULL UNIQUE,
                description TEXT,
                duration_months INT,
                fees DECIMAL(10, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """

            # Attendance Table
            attendance_table = """
            CREATE TABLE IF NOT EXISTS attendance (
                attendance_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(20) NOT NULL,
                course_id INT NOT NULL,
                attendance_date DATE NOT NULL,
                status ENUM('Present', 'Absent') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                UNIQUE KEY unique_attendance (student_id, attendance_date)
            )
            """

            # Users Table (for login)
            users_table = """
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                role ENUM('Admin', 'Staff') DEFAULT 'Staff',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """

            # Execute table creation - courses first due to foreign key
            self.cursor.execute(courses_table)
            self.cursor.execute(students_table)
            self.cursor.execute(attendance_table)
            self.cursor.execute(users_table)

            self.connection.commit()
            print("✓ All tables created successfully")
            return True

        except Exception as e:
            print(f"Table Creation Error: {e}")
            return False

    def initialize_database(self):
        """Initialize the complete database"""
        if self.connect():
            if self.create_database():
                if self.create_tables():
                    # Create assets directories
                    os.makedirs("assets/photos", exist_ok=True)
                    os.makedirs("assets/icons", exist_ok=True)
                    return True
        return False

    # CRUD Operations for Students
    def add_student(self, student_data):
        """Add a new student - parameterized query"""
        try:
            query = """
            INSERT INTO students 
            (student_id, first_name, last_name, gender, dob, email, phone, 
             address, course_id, admission_date, photo_path, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, student_data)
            self.connection.commit()
            return True, "Student added successfully!"
        except pymysql.IntegrityError as e:
            return False, f"Duplicate entry: {str(e)}"
        except Exception as e:
            return False, f"Error adding student: {str(e)}"

    def update_student(self, student_id, student_data):
        """Update existing student - parameterized query"""
        try:
            query = """
            UPDATE students SET 
                first_name=%s, last_name=%s, gender=%s, dob=%s, email=%s, 
                phone=%s, address=%s, course_id=%s, admission_date=%s, 
                photo_path=%s, status=%s
            WHERE student_id=%s
            """
            data = student_data + (student_id,)
            self.cursor.execute(query, data)
            self.connection.commit()
            return True, "Student updated successfully!"
        except Exception as e:
            return False, f"Error updating student: {str(e)}"

    def delete_student(self, student_id):
        """Delete a student - parameterized query"""
        try:
            query = "DELETE FROM students WHERE student_id=%s"
            self.cursor.execute(query, (student_id,))
            self.connection.commit()
            return True, "Student deleted successfully!"
        except Exception as e:
            return False, f"Error deleting student: {str(e)}"

    def get_all_students(self):
        """Get all students"""
        try:
            query = """
            SELECT s.*, c.course_name 
            FROM students s 
            LEFT JOIN courses c ON s.course_id = c.course_id
            ORDER BY s.admission_date DESC
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching students: {e}")
            return []

    def search_students(self, search_term, filter_by="all"):
        """Search students - parameterized query"""
        try:
            if filter_by == "all":
                query = """
                SELECT s.*, c.course_name 
                FROM students s 
                LEFT JOIN courses c ON s.course_id = c.course_id
                WHERE s.student_id LIKE %s OR s.first_name LIKE %s 
                   OR s.last_name LIKE %s OR s.email LIKE %s
                """
                search_param = f"%{search_term}%"
                self.cursor.execute(query, (search_param, search_param, search_param, search_param))
            else:
                query = f"""
                SELECT s.*, c.course_name 
                FROM students s 
                LEFT JOIN courses c ON s.course_id = c.course_id
                WHERE {filter_by} LIKE %s
                """
                self.cursor.execute(query, (f"%{search_term}%",))

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Search Error: {e}")
            return []

    def get_student_by_id(self, student_id):
        """Get student by ID - parameterized query"""
        try:
            query = """
            SELECT s.*, c.course_name 
            FROM students s 
            LEFT JOIN courses c ON s.course_id = c.course_id
            WHERE s.student_id = %s
            """
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def generate_student_id(self):
        """Generate unique student ID in format STU-YYYY0001"""
        try:
            from datetime import datetime
            year = datetime.now().year

            query = "SELECT student_id FROM students WHERE student_id LIKE %s ORDER BY student_id DESC LIMIT 1"
            self.cursor.execute(query, (f"STU-{year}%",))
            result = self.cursor.fetchone()

            if result:
                last_id = result['student_id']
                number = int(last_id.split('-')[1][4:]) + 1
            else:
                number = 1

            new_id = f"STU-{year}{number:04d}"
            return new_id
        except Exception as e:
            print(f"ID Generation Error: {e}")
            return f"STU-{datetime.now().year}0001"

    # CRUD Operations for Courses
    def add_course(self, course_data):
        """Add new course - parameterized query"""
        try:
            query = """
            INSERT INTO courses (course_name, course_code, description, duration_months, fees)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, course_data)
            self.connection.commit()
            return True, "Course added successfully!"
        except pymysql.IntegrityError:
            return False, "Course already exists!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def update_course(self, course_id, course_data):
        """Update course - parameterized query"""
        try:
            query = """
            UPDATE courses SET 
                course_name=%s, course_code=%s, description=%s, 
                duration_months=%s, fees=%s
            WHERE course_id=%s
            """
            data = course_data + (course_id,)
            self.cursor.execute(query, data)
            self.connection.commit()
            return True, "Course updated successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def delete_course(self, course_id):
        """Delete course - parameterized query"""
        try:
            query = "DELETE FROM courses WHERE course_id=%s"
            self.cursor.execute(query, (course_id,))
            self.connection.commit()
            return True, "Course deleted successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def get_all_courses(self):
        """Get all courses with student count"""
        try:
            query = """
            SELECT c.*, COUNT(s.student_id) as student_count
            FROM courses c
            LEFT JOIN students s ON c.course_id = s.course_id
            GROUP BY c.course_id
            ORDER BY c.course_name
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []

    # Attendance Operations
    def mark_attendance(self, attendance_data):
        """Mark attendance for students - parameterized query"""
        try:
            query = """
            INSERT INTO attendance (student_id, course_id, attendance_date, status, remarks)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE status=%s, remarks=%s
            """
            data = attendance_data + (attendance_data[3], attendance_data[4])
            self.cursor.execute(query, data)
            self.connection.commit()
            return True, "Attendance marked successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def get_attendance_by_date(self, date, course_id=None):
        """Get attendance records by date - parameterized query"""
        try:
            if course_id:
                query = """
                SELECT a.*, s.first_name, s.last_name, c.course_name
                FROM attendance a
                JOIN students s ON a.student_id = s.student_id
                JOIN courses c ON a.course_id = c.course_id
                WHERE a.attendance_date = %s AND a.course_id = %s
                """
                self.cursor.execute(query, (date, course_id))
            else:
                query = """
                SELECT a.*, s.first_name, s.last_name, c.course_name
                FROM attendance a
                JOIN students s ON a.student_id = s.student_id
                JOIN courses c ON a.course_id = c.course_id
                WHERE a.attendance_date = %s
                """
                self.cursor.execute(query, (date,))

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_student_attendance(self, student_id):
        """Get attendance percentage for a student - parameterized query"""
        try:
            query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present
            FROM attendance
            WHERE student_id = %s
            """
            self.cursor.execute(query, (student_id,))
            result = self.cursor.fetchone()

            if result and result['total'] > 0:
                percentage = (result['present'] / result['total']) * 100
                return percentage
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 0

    def get_course_attendance(self, course_id):
        """Get attendance statistics for a course - parameterized query"""
        try:
            query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present
            FROM attendance
            WHERE course_id = %s
            """
            self.cursor.execute(query, (course_id,))
            result = self.cursor.fetchone()

            if result and result['total'] > 0:
                percentage = (result['present'] / result['total']) * 100
                return percentage
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 0

    def get_attendance_full_by_date_range(self, start_date, end_date):
        """
        Get attendance records between start_date and end_date (inclusive)
        with full data: Student Name, Course Name, etc.
        """
        try:
            query = """
                SELECT 
                    a.student_id,
                    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
                    c.course_name,
                    a.attendance_date,
                    a.status,
                    a.remarks
                FROM attendance a
                JOIN students s ON a.student_id = s.student_id
                JOIN courses c ON a.course_id = c.course_id
                WHERE a.attendance_date BETWEEN %s AND %s
                ORDER BY a.attendance_date, a.student_id
            """
            self.cursor.execute(query, (start_date, end_date))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching full attendance by date range: {e}")
            return []

    # Dashboard Statistics
    def get_dashboard_stats(self):
        """Get statistics for dashboard"""
        try:
            stats = {}

            # Total students
            self.cursor.execute("SELECT COUNT(*) as count FROM students")
            stats['total_students'] = self.cursor.fetchone()['count']

            # Total courses
            self.cursor.execute("SELECT COUNT(*) as count FROM courses")
            stats['total_courses'] = self.cursor.fetchone()['count']

            # Active students
            self.cursor.execute("SELECT COUNT(*) as count FROM students WHERE status='Active'")
            stats['active_students'] = self.cursor.fetchone()['count']

            # Overall attendance rate
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present
                FROM attendance
            """)
            result = self.cursor.fetchone()
            if result and result['total'] > 0:
                stats['attendance_rate'] = round((result['present'] / result['total']) * 100, 2)
            else:
                stats['attendance_rate'] = 0

            # Students by course
            self.cursor.execute("""
                SELECT c.course_name, COUNT(s.student_id) as count
                FROM courses c
                LEFT JOIN students s ON c.course_id = s.course_id
                GROUP BY c.course_id, c.course_name
            """)
            stats['students_by_course'] = self.cursor.fetchall()

            # Monthly admissions
            self.cursor.execute("""
                SELECT 
                    DATE_FORMAT(admission_date, '%Y-%m') as month,
                    COUNT(*) as count
                FROM students
                WHERE admission_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
                GROUP BY month
                ORDER BY month
            """)
            stats['monthly_admissions'] = self.cursor.fetchall()

            return stats
        except Exception as e:
            print(f"Stats Error: {e}")
            return {}

    # User Authentication
    def add_user(self, user_data):
        """Add new user - parameterized query"""
        try:
            query = """
            INSERT INTO users (username, email, password_hash, full_name, role)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, user_data)
            self.connection.commit()
            return True, "User registered successfully!"
        except pymysql.IntegrityError:
            return False, "Username or email already exists!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def authenticate_user(self, username, password_hash):
        """Authenticate user - parameterized query"""
        try:
            query = "SELECT * FROM users WHERE (username=%s OR email=%s) AND password_hash=%s"
            self.cursor.execute(query, (username, username, password_hash))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Auth Error: {e}")
            return None

    def get_user_by_email(self, email):
        """Get user by email - parameterized query"""
        try:
            query = "SELECT * FROM users WHERE email=%s"
            self.cursor.execute(query, (email,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def update_password(self, email, new_password_hash):
        """Update user password - parameterized query"""
        try:
            query = "UPDATE users SET password_hash=%s WHERE email=%s"
            self.cursor.execute(query, (new_password_hash, email))
            self.connection.commit()
            return True, "Password updated successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
