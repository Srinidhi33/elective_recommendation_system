import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import get_all_enrollments, delete_enrollment, get_all_courses

def main():
    st.title("HOD Course Enrollment Dashboard")

    # Fetch enrollments and all courses
    enrollments = get_all_enrollments()
    all_courses = get_all_courses()

    # Visualization: Number of enrollments per course
    st.subheader("Course Enrollment Visualization")
    fig, ax = plt.subplots(figsize=(12, 6))
    course_data = enrollments['course_code'].value_counts().reindex(all_courses, fill_value=0)
    sns.barplot(x=course_data.index, y=course_data.values, ax=ax)
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Number of Enrolled Students")
    ax.set_title("Course Enrollment")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Visualization: Enrollment percentage per course
    st.subheader("Course Enrollment Percentage")
    course_data = pd.DataFrame({'course_code': all_courses, 'enrolled': course_data.values, 'capacity': 60})
    course_data['enrollment_percentage'] = course_data['enrolled'] / course_data['capacity'] * 100
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='course_code', y='enrollment_percentage', data=course_data, ax=ax)
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Enrollment Percentage")
    ax.set_title("Course Enrollment Percentage")
    plt.xticks(rotation=45, ha='right')
    ax.set_ylim(0, 100)
    for i, v in enumerate(course_data['enrollment_percentage']):
        ax.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom')
    st.pyplot(fig)

    # Section: Student Enrollments
    st.subheader("Student Enrollments")

    # Iterate over all courses
    for course in all_courses:
        st.write(f"\nCourse: {course}")
        
        # Display all students enrolled in the course
        course_enrollments = enrollments[enrollments['course_code'] == course]
        
        # Search box for roll number only (no search option for section)
        search_term = st.text_input(f"Enter Roll Number to search in {course}", key=f"search_{course}")

        # Filter enrollments based on roll number search term
        if search_term:
            course_enrollments = course_enrollments[course_enrollments['student_id'].str.contains(search_term, case=False)]

        # Display student enrollments, even if there are none
        if not course_enrollments.empty:
            for _, enrollment in course_enrollments.iterrows():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                with col1:
                    st.write(f"Student: {enrollment['student_id']}")
                with col2:
                    st.write(f"Enrolled on: {enrollment['enrollment_date']}")
                with col3:
                    if st.button(f"Delete", key=f"{course}_{enrollment['student_id']}"):
                        delete_enrollment(enrollment['student_id'], course)
                        st.success(f"Deleted enrollment of student {enrollment['student_id']} from course {course}")
                        st.rerun()

        else:
            st.write(f"No enrollments found for {course}")

        # CSV Download button for course enrollments
        if st.button(f"Download CSV for {course}"):
            csv = course_enrollments.to_csv(index=False)
            st.download_button(
                label=f"Download {course} enrollments",
                data=csv,
                file_name=f"{course}_enrollments.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
