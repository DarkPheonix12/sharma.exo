import streamlit as st
from firebase_admin import firestore
import pandas as pd
import numpy as np

def load_teacher_details_table(db):
    teacher_docs = db.collection('Teachers').get()
    teacher_details_table = pd.DataFrame(columns=["Teacher's Name", "Teacher's Code", "Subject Taught"])

    for idx, teacher_doc in enumerate(teacher_docs):
        teacher_data = teacher_doc.to_dict()
        subject_taught = teacher_data.get('SubjectTaught', '')

        new_row = pd.DataFrame({
            "Teacher's Name": [teacher_data['TeacherName']],
            "Teacher's Code": [teacher_data['TeacherCode']],
            "Subject Taught": [subject_taught]
        })
        teacher_details_table = pd.concat([teacher_details_table, new_row], ignore_index=True)

    return teacher_details_table

def display_teacher_details_table(teacher_details_table, db):
    if teacher_details_table is not None and not teacher_details_table.empty:
        teacher_details_table.index = np.arange(1, len(teacher_details_table) + 1)
        st.header(' :violet[Teacher Details Table]')
        st.table(teacher_details_table)

        for index, row in teacher_details_table.iterrows():
            teacher_name = row["Teacher's Name"]
            teacher_code = row["Teacher's Code"]
            subject_taught = row["Subject Taught"]

            row_data = [
                f"{teacher_name}",
                f"{teacher_code}",
                f"{subject_taught}",
                f"Delete {teacher_code}",
            ]

            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

            # Display the row in the table
            with col1:
                st.write(row_data[0])
            with col2:
                st.write(row_data[1])
            with col3:
                st.write(row_data[2])

            # Handle delete action
            with col4:
                if st.button(f"Delete {teacher_code}"):
                    db.collection('Teachers').document(teacher_code).delete()
                    st.success(f"Teacher {teacher_code} deleted successfully!")

            st.markdown("---")  # Separator between teacher entries

def app():
    if 'db' not in st.session_state:
        st.session_state.db = ''

    db = firestore.client()
    st.session_state.db = db
    
    teacher_name = st.text_input("Teacher's Name")
    teacher_code = st.text_input("Teacher's Code")
    subject_taught = st.selectbox("Select Subject Taught", ["Maths", "Physics", "Chemistry", "Biology", "MAT", "SST", "English"])

    if st.button('Save Teacher Info', use_container_width=20):
        if teacher_name != '' and teacher_code != '' and subject_taught != '':
            # Save new teacher information to the database
            teacher_info = {
                'TeacherName': teacher_name,
                'TeacherCode': teacher_code,
                'SubjectTaught': subject_taught
            }
            db.collection('Teachers').document(teacher_code).set(teacher_info)
            st.success('Teacher information saved successfully!')
        else:
            st.error("Please enter Teacher's Name, Teacher's Code, and Select Subject Taught.")

    st.header(' :violet[Teacher Information] ')
    teacher_details_table = load_teacher_details_table(db)
    display_teacher_details_table(teacher_details_table, db)

# Uncomment the line below to run the Streamlit app
# app()
