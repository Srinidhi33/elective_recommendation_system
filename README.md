# Elective Course Recommendation System

## Overview

This project provides an interactive system to recommend elective courses to students based on their past performance and preferences. The system allows students to view course recommendations, check course details, and enroll in courses directly via a user-friendly interface built with Streamlit. The backend leverages SQLite for enrollment management and a machine learning-based recommendation model to suggest relevant courses.

---

## Team Details


| Sl. No. | Roll Number     | Student Name        |
|---------|-----------------|---------------------|
| 1       | 20211CSD0108    | SAHANA R           |
| 2       | 20201CSD0130    | AKASH KARTHIK RAO  |
| 3       | 20211CSD0019    | PRATHIKSHA M       |
| 4       | 20211CSD0114    | SRINIDHI S         |
| 5       | 20211CSD0110    | AMPANA J           |

---

## Under the Guidance of:
**Dr. Marimuthu K**  
School of Computer Science,  
Presidency University, Bengaluru  

---

## Features

- Personalized course recommendations using a machine learning-based recommendation model.
- Real-time enrollment updates and seat availability checks.
- Easy enrollment via an interactive Streamlit-based user interface.
- Backend powered by SQLite for managing student and course data.

---
## Steps to run this Project
### 1. Clone this repository to your local machine:
git clone https://github.com/your-repo/elective_course_recommendation.git

cd elective_course_recommendation
---
### 2. Install Dependencies
pip install -r requirements.txt
---
### 3. Initialize the Database
python -c "from database import init_db; init_db()"
---
### 4. Add Required Data Files
- dataset for ml recommendation system for elective.xlsx (student grades and performance data)
- course details.xlsx (course metadata such as course name, description, objectives, and instructor details)
### 5. Run the Application
streamlit run student_interface.py
---
---



