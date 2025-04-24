import os
import numpy as np
import face_recognition
import pandas as pd
from datetime import datetime

# Configuration Variables
KNOWN_FACES_DIR = "known_faces"         
CAPTURED_IMAGE = "captured_image.jpg"     
ATTENDANCE_FILE = "attendance.xlsx"       

def load_known_faces(known_faces_dir=KNOWN_FACES_DIR):
    
    # Loads images from the folder and computes their face encodings.
  
    known_face_encodings = []
    known_face_names = []
    
    for filename in os.listdir(known_faces_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])
            else:
                print(f"Warning: No face found in {filename}")
    
    return known_face_encodings, known_face_names

def recognize_face(image_path, known_face_encodings, known_face_names, tolerance=0.6):

    # Detects and recognizes faces in the provided image.
    image = face_recognition.load_image_file(image_path)
    
    face_locations = face_recognition.face_locations(image, model="cnn")
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    recognized_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if face_distances.size > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
        recognized_names.append(name)
    return recognized_names

def record_attendance_by_date(recognized_names):

    # Updates the master attendance Excel file using a date-as-column layout.
    today = datetime.now().strftime("%Y-%m-%d")

    # Open the pre-populated master attendance file.
    if os.path.exists(ATTENDANCE_FILE):
        df = pd.read_excel(ATTENDANCE_FILE, dtype={'Attendance': str, 'Timestamp': str, 'Date': str})
    else:
        print(f"Error: {ATTENDANCE_FILE} not found. Please create the master file with fixed columns.")
        return

    # If today's column doesn't exist, add it with blank values.
    if today not in df.columns:
        df[today] = pd.Series([""] * len(df), dtype="str")
        print(f"Added new column for {today}.")

    # For each recognized student (skip "Unknown"), update their cell under today's column.
    for recognized in recognized_names:
        if recognized == "Unknown":
            continue
        
        mask = df["ImageName"] == recognized
        if mask.any():
            df.loc[mask, today] = "Present"
            print(f"Marked attendance for {recognized} on {today}.")
        else:
            print(f"Warning: No record found for ImageName '{recognized}' in the master file.")
    
    # Save the updated file.
    df.to_excel(ATTENDANCE_FILE, index=False)
    print("Attendance updated successfully in", ATTENDANCE_FILE)

def main():
    # Step 1: Load known faces.
    print("Loading known faces from folder:", KNOWN_FACES_DIR)
    known_face_encodings, known_face_names = load_known_faces()
    print("Known faces loaded:", known_face_names)
    
    # Step 2: Check if the captured image exists.
    if not os.path.exists(CAPTURED_IMAGE):
        print(f"Error: The image '{CAPTURED_IMAGE}' does not exist. Please ensure it is present.")
        return
    
    # Step 3: Recognize faces in the captured image.
    recognized_names = recognize_face(CAPTURED_IMAGE, known_face_encodings, known_face_names)
    print("Recognized names from the image:", recognized_names)
    
    # Step 4: Record attendance in the master Excel file using today's date as a column header.
    record_attendance_by_date(recognized_names)

if __name__ == "__main__":
    main()
