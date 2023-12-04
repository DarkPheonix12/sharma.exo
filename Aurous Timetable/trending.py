import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pandas as pd
import numpy as np

# Setup
cred = credentials.Certificate("timetable-7078c-84ae453a37d8.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def load_teacher_details(db):
    teacher_docs = db.collection('Teachers').get()
    teachers = [teacher.to_dict() for teacher in teacher_docs]
    return teachers

def get_subjects_for_teacher(teacher_name, teachers):
    for teacher in teachers:
        if teacher['TeacherName'] == teacher_name:
            subject_taught = teacher.get('SubjectTaught', "")
            return [subject_taught] if subject_taught else []
    return []

def save_batch_details(db, batch_info):
    db.collection('Batches').document(batch_info['BatchName']).set(batch_info)
    st.success('Batch information saved successfully!')

def delete_batch_entry(db, batch_name):
    db.collection('Batches').document(batch_name).delete()
    st.success(f'Batch entry {batch_name} deleted successfully!')

def app(db):
    if 'db' not in st.session_state:
        st.session_state.db = db

    st.header('Batch Details Form')

    # Input fields for Batch details
    batch_name = st.text_input("Enter Batch Name")

    # Dropdown menu for selecting teachers from the entered data
    teachers_data = load_teacher_details(db)
    teacher_options = [f"{teacher['TeacherName']} ({teacher.get('TeacherCode', '')})" for teacher in teachers_data]
    selected_teachers = st.multiselect("Select Batch Teachers", teacher_options)

    # Extract teacher names from the selected options
    selected_teacher_names = [teacher.split(' (')[0] for teacher in selected_teachers]

    # Dropdown menu for selecting subjects
    selected_subjects = []
    for selected_teacher in selected_teacher_names:
        subjects_for_teacher = get_subjects_for_teacher(selected_teacher, teachers_data)
        selected_subject = st.selectbox(f"Select Subject for {selected_teacher}", subjects_for_teacher)
        selected_subjects.append(selected_subject)

    # Dropdown menu for selecting time slots
    time_slots = [
        "10:40am - 11:45am", "11:55am - 01:10pm", "09:00am - 10:20am", "10:40am - 12:00pm",
        "12:10pm - 01:25pm", "05:00pm - 05:50pm", "06:00pm - 06:50pm", "07:00pm - 08:20pm",
        "12:15pm - 01:45pm", "02:00pm - 03:30pm", "04:00pm - 05:20pm",
        "05:30pm - 06:50pm", "10:15am - 11:45am","03:45pm - 04:50pm"
    ]

    selected_time_slots = st.multiselect("Select Time Slots for Classes", time_slots)

    if st.button('Save Batch Info', use_container_width=20):
        if batch_name != '' and selected_teacher_names and selected_subjects and selected_time_slots:
            # Save batch information to the database
            batch_info = {
                'BatchName': batch_name,
                'Teachers': selected_teacher_names,
                'Subjects': selected_subjects,
                'TimeSlots': selected_time_slots
            }
            save_batch_details(db, batch_info)
            st.success('Batch information saved successfully!')
        else:
            st.error("Please fill in all the required fields.")

    st.header('Batch Information')

    # Display batch information in the table
    batch_docs = db.collection('Batches').get()

    # Create a DataFrame to hold batch data
    data = {
        "Batch Name": [],
        "Teachers": [],
        "Subjects": [],
        "Time Slots": []
    }

    for batch_doc in batch_docs:
        batch_data = batch_doc.to_dict()
        data["Batch Name"].append(batch_data['BatchName'])
        data["Teachers"].append(', '.join(batch_data['Teachers']))
        data["Subjects"].append(', '.join(batch_data['Subjects']))
        data["Time Slots"].append(', '.join(batch_data.get('TimeSlots', [])))

    df = pd.DataFrame(data)

    # Display the table
    st.table(df)

    # Delete batch entries
    batch_to_delete = st.selectbox("Select Batch to Delete", data["Batch Name"])
    if st.button('Delete Batch Entry', use_container_width=20):
        delete_batch_entry(db, batch_to_delete)

# Uncomment the line below to run the Streamlit app
if __name__ == "__main__":
    db_instance = firestore.client()  # Initialize your Firestore client
    app(db_instance)
