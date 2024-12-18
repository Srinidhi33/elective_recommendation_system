import sqlite3
import pandas as pd

# Initialize the database and create the enrollments table if it doesn't exist
def init_db():
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS enrollments
                 (student_id TEXT, course_code TEXT, enrollment_date TEXT,
                  PRIMARY KEY (student_id, course_code))''')
    conn.commit()
    conn.close()

# Get the current number of students enrolled in a course
def get_course_enrollment(course_code):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM enrollments WHERE course_code = ?", (course_code,))
    count = c.fetchone()[0]
    conn.close()
    return count

# Check if the student is valid based on enrollment records
def is_valid_student(student_id):
    # Instead of checking the enrollments, consider checking the valid student IDs in the system
    # If you have a separate student table, this method needs to be implemented accordingly
    return True  # Temporary return; implement a proper check if needed

# Enroll a student into a course
def enroll_student(student_id, course_code, enrollment_date):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    if not is_valid_student(student_id):
        conn.close()
        return {"success": False, "message": "Invalid student ID. Please check and try again."}

    try:
        c.execute("INSERT INTO enrollments VALUES (?, ?, ?)", (student_id, course_code, enrollment_date))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Successfully enrolled in the course."}
    except sqlite3.IntegrityError:
        conn.close()
        return {"success": False, "message": "You are already enrolled in this course."}

# Remove enrollment for a student from a course
def delete_enrollment(student_id, course_code):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("DELETE FROM enrollments WHERE student_id = ? AND course_code = ?", (student_id, course_code))
    conn.commit()
    conn.close()

# Get all enrollments as a DataFrame
def get_all_enrollments():
    conn = sqlite3.connect('courses.db')
    df = pd.read_sql_query("SELECT * FROM enrollments", conn)
    conn.close()
    return df

# Check if a specific student is already enrolled in a course
def is_student_enrolled(student_id, course_code):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM enrollments WHERE student_id = ? AND course_code = ?", (student_id, course_code))
    count = c.fetchone()[0]
    conn.close()
    return count > 0

# Get all distinct course codes from the enrollments table
def get_all_courses():
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT course_code FROM enrollments")
    courses = [row[0] for row in c.fetchall()]
    conn.close()
    return courses

# Get a list of all courses a student is enrolled in
def get_student_enrollments(student_id):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("SELECT course_code FROM enrollments WHERE student_id = ?", (student_id,))
    enrollments = [row[0] for row in c.fetchall()]
    conn.close()
    return enrollments
