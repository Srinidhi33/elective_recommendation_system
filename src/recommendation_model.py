import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_data(file_path):
    df = pd.read_excel(file_path)
    print("Data loaded successfully.")
    return df

def preprocess_data(df):
    pivot_table = df.pivot_table(values='Marks (200)', index='RollNumber', columns='Course Code', fill_value=0)
    print("Pivot table created:")
    print(pivot_table.head())

    # Normalize the pivot table to account for differences in scales
    pivot_table = pivot_table.div(pivot_table.sum(axis=1), axis=0)
    print("Normalized pivot table:")
    print(pivot_table.head())
    return pivot_table

def compute_similarity(pivot_table):
    similarity_matrix = cosine_similarity(pivot_table)
    print("Similarity matrix computed:")
    print(similarity_matrix)
    return similarity_matrix

def recommend_courses(student_id, pivot_table, similarity_matrix, previous_recommendations=None, n_recommendations=5):
    if student_id not in pivot_table.index:
        print(f"Student ID {student_id} not found in data.")
        return []

    student_index = pivot_table.index.get_loc(student_id)
    student_similarities = similarity_matrix[student_index]

    print(f"Similarity scores for student {student_id}: {student_similarities}")

    similar_students = student_similarities.argsort()[::-1][1:11]
    print(f"Top similar students for {student_id}: {similar_students}")

    recommendations = {}
    for course in pivot_table.columns:
        if pivot_table.iloc[student_index][course] > 0:
            continue

        if previous_recommendations and course in previous_recommendations:
            continue

        course_scores = pivot_table.iloc[similar_students][course]
        weights = student_similarities[similar_students]
        if weights.sum() > 0:  # Avoid division by zero
            weighted_avg = np.average(course_scores, weights=weights)
        else:
            weighted_avg = 0

        print(f"Course: {course}, Scores: {course_scores.tolist()}, Weights: {weights.tolist()}, Weighted Average: {weighted_avg}")

        recommendations[course] = weighted_avg

    # Sort recommendations
    top_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
    
    # Randomize among ties if necessary
    if len(top_recommendations) > 1:
        import random
        scores = [score for course, score in top_recommendations]
        unique_scores = set(scores)
        if len(unique_scores) < len(scores):
            random.shuffle(top_recommendations)

    print(f"Top recommendations for {student_id}: {top_recommendations}")

    return [course for course, score in top_recommendations]
