import streamlit as st
import firebase_admin
from firebase_admin import firestore, credentials
import pandas as pd
from datetime import datetime

# Setup
cred = credentials.Certificate("timetable-7078c-84ae453a37d8.json")

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def app():
    if 'db' not in st.session_state:
        st.session_state.db = db

    st.header('Schedule Timetable')

    try:
        # Integrated timetable app logic

        st.header('Batch and Subjects Selection')

        # Select a batch from the dropdown menu
        selected_batch = st.selectbox("Select Batch", get_batches(st.session_state.db))

        # Retrieve subjects for the selected batch
        selected_batch_subjects = get_subjects_for_batch(st.session_state.db, selected_batch)

        # Display selected subjects for the batch
        st.write(f"Subjects for {selected_batch}: {', '.join(selected_batch_subjects)}")

        # Input field for the number of days for the batch
        no_of_days = st.number_input("No. of Days for the Batch This Week", min_value=0)

        # Input field for preferred days for the batch
        preferred_days = st.multiselect("Preferred Days for the Batch", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        # Input fields for the number of classes for each subject
        no_of_classes_list = []
        for subject in selected_batch_subjects:
            no_of_classes_list.append(st.number_input(f"No. of Classes for {subject} This Week", min_value=0))

        # Save data button
        if st.button('Save Data', use_container_width=True):
            # Save subject-wise classes to the database
            for i, subject in enumerate(selected_batch_subjects):
                no_of_classes = no_of_classes_list[i]
                save_subject_classes(st.session_state.db, selected_batch, subject, no_of_classes, no_of_days, preferred_days)

            st.success("Data saved successfully!")

        # Display batch-wise and subject-wise classes information in the table after saving
        subject_classes_docs = st.session_state.db.collection('SubjectClasses').document(selected_batch).collection('Subjects').get()

        # Create a DataFrame to hold batch-wise and subject-wise classes data
        data = {
            "Batch Name": [],
            "Subject": [],
            "No. of Classes": [],
            "No. of Days": [],
            "Preferred Days": []
        }

        for subject_doc in subject_classes_docs:
            subject_data = subject_doc.to_dict()
            data["Batch Name"].append(selected_batch)
            data["Subject"].append(subject_doc.id)
            data["No. of Classes"].append(subject_data.get('NoOfClasses', ""))
            data["No. of Days"].append(subject_data.get('NoOfDays', ""))
            data["Preferred Days"].append(subject_data.get('PreferredDays', ""))

        df = pd.DataFrame(data)

        # Display the table
        st.table(df)

        # Delete Data button
        if st.button('Delete Data', use_container_width=True):
            delete_subject_classes(st.session_state.db, selected_batch)
            st.success("Data deleted successfully!")

        # Generate Time Table button
        if st.button('Generate Time Table', use_container_width=True):
            # Your logic for generating the time table goes here
            # You can access selected_batch, selected_batch_subjects, no_of_classes_list, and no_of_days to get user inputs
            pass

    except Exception as e:
        print(f"Error: {e}")
        if st.session_state.username == '':
            st.text('Please Login first')

# Function to save subject-wise classes
def save_subject_classes(db, batch_name, subject, no_of_classes, no_of_days, preferred_days):
    # Create a document reference for the subject's data
    subject_doc_ref = db.collection('SubjectClasses').document(batch_name).collection('Subjects').document(subject)

    # Set the subject data
    subject_data = {
        'NoOfClasses': no_of_classes,
        'NoOfDays': no_of_days,
        'PreferredDays': preferred_days
    }

    # Update the subject's data in the database
    subject_doc_ref.set(subject_data)

# Function to delete subject-wise classes for a batch
def delete_subject_classes(db, batch_name):
    # Reference to the batch's document in Firestore
    batch_doc_ref = db.collection('SubjectClasses').document(batch_name)

    # Retrieve all documents in the batch's subjects collection
    subjects_collection = batch_doc_ref.collection('Subjects')
    subjects_docs = subjects_collection.stream()

    # Delete each subject document
    for doc in subjects_docs:
        doc.reference.delete()

# Function to get batches
def get_batches(db):
    batch_docs = db.collection('Batches').get()
    batches = [batch.id for batch in batch_docs]
    return batches

# Function to get subjects for a batch
def get_subjects_for_batch(db, batch_name):
    batch_doc = db.collection('Batches').document(batch_name).get()
    batch_data = batch_doc.to_dict()
    subjects = batch_data.get('Subjects', [])
    return subjects

if __name__ == "__main__":
    app()
