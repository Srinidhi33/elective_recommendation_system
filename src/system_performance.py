import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import get_all_enrollments
from recommendation_model import load_data, preprocess_data, compute_similarity, recommend_courses

def evaluate_recommendations(student_id, enrolled_courses, recommendations):
    hit_count = len(set(enrolled_courses) & set(recommendations))
    precision = hit_count / len(recommendations) if recommendations else 0
    recall = hit_count / len(enrolled_courses) if enrolled_courses else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1_score

def main():
    st.title("Recommendation System Performance")

    grade_data = load_data("dataset for ml recommendation system for elective.xlsx")
    pivot_table = preprocess_data(grade_data)
    similarity_matrix = compute_similarity(pivot_table)

    enrollments = get_all_enrollments()
    
    performance_data = []
    for student_id in enrollments['student_id'].unique():
        if student_id in pivot_table.index:
            enrolled_courses = enrollments[enrollments['student_id'] == student_id]['course_code'].tolist()
            recommendations = recommend_courses(student_id, pivot_table, similarity_matrix)
            precision, recall, f1_score = evaluate_recommendations(student_id, enrolled_courses, recommendations)
            performance_data.append({
                'student_id': student_id,
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score
            })
    
    performance_df = pd.DataFrame(performance_data)
    
    if not performance_df.empty:
        st.subheader("Overall System Performance")
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Precision", f"{performance_df['precision'].mean():.2f}")
        col2.metric("Average Recall", f"{performance_df['recall'].mean():.2f}")
        col3.metric("Average F1 Score", f"{performance_df['f1_score'].mean():.2f}")

        st.subheader("Performance Distribution")
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.histplot(performance_df['precision'], kde=True, ax=axes[0])
        axes[0].set_title("Precision Distribution")
        sns.histplot(performance_df['recall'], kde=True, ax=axes[1])
        axes[1].set_title("Recall Distribution")
        sns.histplot(performance_df['f1_score'], kde=True, ax=axes[2])
        axes[2].set_title("F1 Score Distribution")
        st.pyplot(fig)

        st.subheader("Performance by Student")
        st.dataframe(performance_df)

        st.subheader("Performance Correlation")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(performance_df[['precision', 'recall', 'f1_score']].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No performance data available. Make sure students have enrolled in courses and received recommendations.")

if __name__ == "__main__":
    main()
