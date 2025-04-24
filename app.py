from flask import Flask, render_template, redirect, url_for, flash, request
import os
import fetch_image
import attendance_system
import absence_email
import calculate_attendance_percentage
from werkzeug.utils import secure_filename
import pandas as pd


app = Flask(__name__)
app.secret_key = "supersecretkey"  

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = "known_faces"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch")
def fetch():
    try:
        fetch_image.fetch_image_from_esp32("192.168.122.80")
        flash("✅ Image fetched successfully!")
    except Exception as e:
        flash(f"❌ Error fetching image: {e}")
    return redirect(url_for("index"))

@app.route("/attendance")
def attendance():
    try:
        attendance_system.main()
        flash("✅ Attendance updated successfully!")
    except Exception as e:
        flash(f"❌ Error updating attendance: {e}")
    return redirect(url_for("index"))

@app.route("/absence")
def absence():
    try:
        absence_email.check_and_send_absence_emails()
        flash("✅ Absence emails checked/sent.")
    except Exception as e:
        flash(f"❌ Error during absence check/email: {e}")
    return redirect(url_for("index"))

@app.route("/calculate")
def calculate():
    try:
        calculate_attendance_percentage.calculate_attendance_percentage()
        flash("✅ Attendance percentage calculated!")
    except Exception as e:
        flash(f"❌ Error calculating percentage: {e}")
    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_student", methods=["POST"])
def register_student():
    name = request.form.get("name").strip()
    student_id = request.form.get("student_id").strip()
    email = request.form.get("email").strip()
    image_name = request.form.get("image_name").strip()
    image_file = request.files.get("image_file")

    if not all([name, student_id, email, image_name]):
        flash("⚠️ All fields except image upload are required.")
        return redirect(url_for("register"))

    # Save image if uploaded
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_name + os.path.splitext(image_file.filename)[1])
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)
        flash(f"✅ Image saved as {filename}.")
    else:
        flash("ℹ️ No image uploaded or invalid format. Upload jpg/png/jpeg.")

    # Append student to Excel
    if os.path.exists("attendance.xlsx"):
        df = pd.read_excel("attendance.xlsx")
    else:
        df = pd.DataFrame(columns=["Name", "ID", "ImageName", "Email"])

    new_row = {
        "Name": name,
        "ID": student_id,
        "ImageName": image_name,
        "Email": email
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel("attendance.xlsx", index=False)

    flash(f"✅ Student {name} (ID: {student_id}) added successfully.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
