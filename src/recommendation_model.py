import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_data(file_path):
    df = pd.read_excel(file_path)
    print("Data loaded successfully.")
    return df

def preprocess_data(df):
    # Creating a pivot table for student course marks
    pivot_table = df.pivot_table(values='Marks (200)', index='RollNumber', columns='Course Code', fill_value=0)
    return pivot_table

def compute_similarity(pivot_table):
    # Calculating the cosine similarity matrix
    similarity_matrix = cosine_similarity(pivot_table)
    return similarity_matrix

def recommend_courses(student_id, pivot_table, similarity_matrix, previous_recommendations=None, n_recommendations=5):
    # Check if student_id exists in pivot_table
    if student_id not in pivot_table.index:
        return []

    # Getting the index of the student
    student_index = pivot_table.index.get_loc(student_id)
    student_similarities = similarity_matrix[student_index]

    # Finding the top 10 most similar students
    similar_students = student_similarities.argsort()[::-1][1:11]

    recommendations = {}
    
    for course in pivot_table.columns:
        if pivot_table.iloc[student_index][course] == 0:  # Student hasn't taken this course
            # Skip previously recommended courses if provided
            if previous_recommendations and course in previous_recommendations:
                continue
            
            # Calculating the average score for the course from similar students
            course_scores = pivot_table.iloc[similar_students][course]
            recommendations[course] = course_scores.mean()

    # Sorting the recommendations by score and selecting the top ones
    top_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
    
    return [course for course, score in top_recommendations]