import pandas as pd

# Configuration Variables
ATTENDANCE_FILE = "attendance.xlsx"
FIXED_COLUMNS = ["Name", "ID", "ImageName", "Email"]

def calculate_attendance_percentage():
    ATTENDANCE_FILE = "attendance.xlsx"
    FIXED_COLUMNS = ["Name", "ID", "ImageName", "Email"]

    try:
        df = pd.read_excel(ATTENDANCE_FILE)
    except FileNotFoundError:
        print("Attendance file not found.")
        return

    # Remove the column if it already exists (to reinsert at the end)
    if "Attendance Percentage" in df.columns:
        df.drop(columns=["Attendance Percentage"], inplace=True)

    # Get date columns only
    date_columns = [col for col in df.columns if col not in FIXED_COLUMNS]

    # Count percentage
    percentage_list = []
    for idx, row in df.iterrows():
        total = len(date_columns)
        present = sum(1 for col in date_columns if str(row[col]).strip().lower() == "present")
        percent = round((present / total) * 100, 2) if total > 0 else 0
        percentage_list.append(f"{percent}%")

    # Append as last column
    df["Attendance Percentage"] = percentage_list

    # Save
    df.to_excel(ATTENDANCE_FILE, index=False)
    print("✅ Attendance percentage updated (always at the last column).")

if __name__ == "__main__":
    calculate_attendance_percentage()
