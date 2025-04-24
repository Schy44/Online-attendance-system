import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration Variables for the Excel file and fixed columns.
ATTENDANCE_FILE = "attendance.xlsx"
FIXED_COLUMNS = ["Name", "ID", "ImageName", "Email"]

# Gmail SMTP settings:
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_LOGIN = "growwitharup@gmail.com"           
EMAIL_PASSWORD = "fovsycgosevwoopv"               

def send_email(recipient, subject, body, student_id=None):
   
    msg = MIMEMultipart()
    msg['From'] = EMAIL_LOGIN
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        server.sendmail(EMAIL_LOGIN, recipient, msg.as_string())
        server.quit()
        print(f"Email successfully sent to {recipient}.")
    except Exception as e:
        if student_id:
            print(f"Error sending Email for student ID {student_id}.")
        else:
            print(f"Error sending Email to: {recipient}")

def check_and_send_absence_emails():

    # Checks the attendance Excel file for students with three consecutive absent days.
    try:
        df = pd.read_excel(ATTENDANCE_FILE)
    except FileNotFoundError:
        print(f"Error: {ATTENDANCE_FILE} not found.")
        return

    # Identify date columns: any column not in FIXED_COLUMNS and not "Attendance Percentage".
    date_columns = [col for col in df.columns if col not in FIXED_COLUMNS and col != "Attendance Percentage"]
    if len(date_columns) < 3:
        print("Not enough date columns (need at least 3) to check for consecutive absences.")
        return

    # Sort date columns (assumes headers are formatted as YYYY-MM-DD) and get the last three.
    date_columns.sort()
    last_three = date_columns[-3:]
    print(f"Checking absences for the last 3 dates: {last_three}")

    # Email content.
    subject = "Attendance Alert: 3 Consecutive Absences"
    email_body = (
        "We have noticed that you have been absent from your classes for the past three consecutive days. "
        "If there is a valid reason for your absence, we kindly request that you inform the academic office "
        "or your department advisor at your earliest convenience.\n\n"
        "If you are facing any difficulties or require assistance, please do not hesitate to reach out to us.\n\n"
        "Best regards,\nDept of SWE\nMetropolitan University"
    )

    # Process each student row.
    for idx, row in df.iterrows():
        student_id = row.get("ID", "Unknown ID")
        student_email = str(row.get("Email", "")).strip()
        originally_blank = []
        for day in last_three:
            cell_val = row.get(day, "")
            # Check if cell_val is NaN or, when converted to string, is empty.
            if pd.isna(cell_val):
                originally_blank.append(True)
            else:
                # Convert explicitly to string
                cell_str = str(cell_val)
                if cell_str.strip() == "":
                    originally_blank.append(True)
                else:
                    originally_blank.append(False)
        # Fill any blank cell with "Absent".
        for day in last_three:
            cell_val = row.get(day, "")
            if pd.isna(cell_val) or str(cell_val).strip() == "":
                df.at[idx, day] = "Absent"
        # Only send email if all last three cells were originally blank.
        if all(originally_blank):
            if student_email and student_email.lower() != "nan":
                send_email(student_email, subject, email_body, student_id=student_id)
            else:
                print(f"Email not sent for student ID {student_id}: Email address not available.")
    # Save the updated attendance file.
    df.to_excel(ATTENDANCE_FILE, index=False)
    print(f"Attendance updated successfully in {ATTENDANCE_FILE}")

if __name__ == "__main__":
    check_and_send_absence_emails()
