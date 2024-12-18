import streamlit as st
import pandas as pd
from datetime import date
from recommendation_model import load_data, preprocess_data, compute_similarity, recommend_courses
from database import init_db, get_course_enrollment, enroll_student, get_student_enrollments

def load_course_details(file_path):
    return pd.read_excel(file_path)

def main():
    st.title("Elective Course Recommendation System")

    init_db()

    # Load data only once
    grade_data = load_data("dataset for ml recommendation system for elective.xlsx")
    course_details = load_course_details("course details.xlsx")

    # Initialize variables for session state
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []

    pivot_table = preprocess_data(grade_data)
    similarity_matrix = compute_similarity(pivot_table)

    # Error handling for empty roll number input
    student_id = st.text_input("Enter your Roll Number:")
    
    if student_id:
        if student_id not in pivot_table.index:
            st.error("Invalid Roll Number. Please enter a valid roll number.")
            return

        if student_id in pivot_table.index:
            st.success(f"Welcome, Student {student_id}!")

            # Check if the student has already registered for any course
            existing_enrollments = get_student_enrollments(student_id)
            if existing_enrollments:
                st.error("You have already registered for a course. Multiple registrations are not allowed.")
            else:
                # Generate recommendations only once when the student ID is entered
                if not st.session_state.recommendations:
                    st.session_state.recommendations = recommend_courses(student_id, pivot_table, similarity_matrix)

                st.subheader("Recommended Courses:")
                for course in st.session_state.recommendations:
                    course_info = course_details[course_details['course_code'] == course].iloc[0]
                    current_enrolled = get_course_enrollment(course)

                    if current_enrolled < 60:
                        st.write(f"\nCourse Code: {course}")
                        st.write(f"Course Name: {course_info['course_name']}")
                        st.write(f"Description: {course_info['description']}")
                        st.write(f"Objective: {course_info['objective']}")
                        st.write(f"Instructors: {course_info['instructors']}")
                        st.write(f"Available Seats: {60 - current_enrolled}")

                        # Enroll button will only show if the student hasn't enrolled yet
                        if st.button(f"Enroll in {course}"):
                            success = enroll_student(student_id, course, str(date.today()))
                            if success:
                                st.success(f"Successfully enrolled in {course}")
                            else:
                                st.error("Enrollment failed. Please try again.")
                    else:
                        st.warning(f"Course {course} is full and not available for enrollment.")
                    st.write("-" * 50)

if __name__ == "__main__":
    main()