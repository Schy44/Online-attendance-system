import fetch_image
import attendance_system
import absence_email
import calculate_attendance_percentage

def main():
    # Step 1: Fetch the image.
    print("=== Step 1: Fetching image from ESP32 ===")
    # fetch_image.main()  # assuming fetch_image.py defines a main() to fetch the image
    input("Step 1 complete. Press Enter to continue to Attendance System...")

    # Step 2: Update attendance.
    print("\n=== Step 2: Updating Attendance ===")
    attendance_system.main()  # assuming attendance_system.py defines a main() for attendance update
    input("Step 2 complete. Press Enter to continue to Absence Email Check...")

    # Step 3: Check for absence and send emails.
    print("\n=== Step 3: Checking and Sending Absence Emails ===")
    absence_email.check_and_send_absence_emails()  # directly call the function from absence_email.py
    input("Step 3 complete. Press Enter to continue to Calculate Attendance Percentage...")

    # Step 4: Calculate attendance percentage.
    print("\n=== Step 4: Calculating Attendance Percentage ===")
    calculate_attendance_percentage.calculate_attendance_percentage()  # assuming calculate_attendance_percentage.py defines a main() function
    print("\nAll processes completed successfully.")

if __name__ == "__main__":
    main()
