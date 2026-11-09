from flask import Flask, request, redirect, url_for, session
from database import init_db, get_connection
from datetime import date


app = Flask(__name__)
app.secret_key = "school_secret_key"





def page(title, body, color="#1a73e8", bg="#e3f2fd"):
    html = """
    <html>
    <head>
        <title>""" + title + """</title>
        <style>
            * {
                box-sizing: border-box;
                font-family: Arial;
            }
            body {
                margin: 0;
                background: """ + bg + """;
            }
            .navbar {
                background: """ + color + """;
                color: white;
                padding: 18px;
                text-align: center;
            }
            .navbar h1 {
                margin: 0;
                font-size: 24px;
            }
            .container {
                max-width: 800px;
                margin: 30px auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 3px 12px rgba(0,0,0,0.15);
            }
            h1, h2 {
                color: """ + color + """;
            }
            input, select, textarea {
                width: 100%;
                padding: 12px;
                margin: 8px 0 16px 0;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 15px;
            }
            button {
                width: 100%;
                padding: 13px;
                background: """ + color + """;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 17px;
                cursor: pointer;
            }
            button:hover {
                opacity: 0.9;
            }
            .btn {
                display: block;
                background: """ + color + """;
                color: white;
                padding: 13px;
                margin: 12px 0;
                text-align: center;
                text-decoration: none;
                border-radius: 8px;
                font-size: 17px;
            }
            .btn:hover {
                opacity: 0.9;
            }
            .card {
                background: #f9f9f9;
                border-left: 6px solid """ + color + """;
                padding: 15px;
                margin: 15px 0;
                border-radius: 8px;
            }
            .message {
                background: #e8f5e9;
                color: #2e7d32;
                padding: 12px;
                border-radius: 8px;
                margin-bottom: 15px;
                font-weight: bold;
            }
            .back {
                display: inline-block;
                margin-top: 20px;
                color: """ + color + """;
                font-weight: bold;
                text-decoration: none;
            }
            .footer {
                text-align: center;
                color: #777;
                padding: 20px;
            }
        </style>
    </head>
    <body>

        <div class="navbar">
            <h1>School Parent Portal</h1>
        </div>

        <div class="container">
            """ + body + """
        </div>

        <div class="footer">
            © 2026 School Parent Portal
        </div>

    </body>
    </html>
    """
    return html


@app.route("/")
def home():
    body = """
        <h1>🏫 Welcome to School Parent Portal</h1>
        <p>📚 Manage students, teachers, homework, marks, attendance and activities.</p>

        <a class="btn" style="background:#1a73e8;" href="/admin/login">👩‍💼 Admin Login</a>
        <a class="btn" style="background:#2e7d32;" href="/teacher/login">👨‍🏫 Teacher Login</a>
        <a class="btn" style="background:#ef6c00;" href="/parent/login">👪 Parent Login</a>
    """
    return page("School Parent Portal", body)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM admins WHERE username = ? AND password = ?
        """, (request.form["username"], request.form["password"]))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session["admin"] = True
            session["admin_username"] = admin[1]
            return redirect(url_for("admin_dashboard"))

        body = """
            <h1>👩‍💼 Admin Login</h1>
            <p class="message" style="background:#ffebee;color:#c62828;">Invalid username or password</p>
            <form method="POST">
                <input name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button>Login</button>
            </form>
            
            <a class="back" href="/">← Back to Home</a>
        """
        return page("Admin Login", body)

    body = """
        <h1>👩‍💼 Admin Login</h1>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button>Login</button>
        </form>
        
        <a class="back" href="/">← Back to Home</a>
    """
    return page("Admin Login", body)


@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():
         
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admins WHERE username = ?", (username,))
        existing = cursor.fetchone()

        if existing:
            conn.close()
            body = """
                <h1>👩‍💼 Create Admin Account</h1>
                <p class="message" style="background:#ffebee;color:#c62828;">Username already exists</p>
                <form method="POST">
                    <input name="username" placeholder="Username" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button>Create Admin</button>
                </form>
                <a class="back" href="/admin/dashboard">← Back to Dashboard</a>
            """
            return page("Admin Register", body)

        cursor.execute("""
            INSERT INTO admins (username, password)
            VALUES (?, ?)
        """, (username, password))

        conn.commit()
        conn.close()

        body = """
            <h1>👩‍💼 Create Admin Account</h1>
            <p class="message">Admin account created successfully!</p>
            <a class="btn" href="/admin/dashboard">← Back to Dashboard</a>
        """
        return page("Admin Register", body)

    body = """
        <h1>👩‍💼 Create Admin Account</h1>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button>Create Admin</button>
        </form>
        <a class="back" href="/admin/dashboard">← Back to Dashboard</a>
    """
    return page("Admin Register", body)


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    body = """
        <h1>👩‍💼 Admin Dashboard</h1>
        <a class="btn" href="/admin/add_student">🎓 Add Student and Parent</a>
        <a class="btn" href="/admin/add_teacher">👨‍🏫 Add Teacher</a>
        <a class="btn" href="/admin/add_homework">📚 Add Homework</a>
        <a class="btn" href="/admin/add_attendance">✅ Add Attendance</a>
        <a class="btn" href="/admin/add_marks">📝 Add Marks</a>
        <a class="btn" href="/admin/add_notice">📢 Add Notice</a>
        <a class="btn" href="/admin/add_activity">🏆 Add Activity</a>
        <a class="btn" href="/admin/complaints">📩 View Complaints</a>
        <a class="btn" href="/admin/register">➕ Create New Admin</a>
        <a class="btn" style="background:#c62828;" href="/admin/logout">Logout</a>
    """
    return page("Admin Dashboard", body)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


@app.route("/admin/add_student", methods=["GET", "POST"])
def add_student():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    message = ""
    if request.method == "POST":
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students
                (student_id, student_name, class_name, section, parent_name, parent_phone, parent_password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                request.form["student_id"],
                request.form["student_name"],
                request.form["class_name"],
                request.form.get("section", ""),
                request.form["parent_name"],
                request.form["parent_phone"],
                request.form["parent_password"]
            ))
            conn.commit()
            conn.close()
            message = "Student and parent added successfully!"
        except:
            message = "Error: Student ID or parent phone already exists."

    body = f"""
        <h1>🎓 Add Student and Parent</h1>
        <p class="message">{message}</p>
        <form method="POST">
            <input name="student_id" placeholder="Student ID" required>
            <input name="student_name" placeholder="Student Name" required>
            <input name="class_name" placeholder="Class" required>
            <input name="section" placeholder="Section">
            <input name="parent_name" placeholder="Parent Name" required>
            <input name="parent_phone" placeholder="Parent Phone" required>
            <input type="password" name="parent_password" placeholder="Parent Password" required>
            <button>Add Student</button>
        </form>
        <a class="back" href="/admin/dashboard">← Back to Dashboard</a>
    """
    return page("Add Student", body)


@app.route("/admin/add_teacher", methods=["GET", "POST"])
def add_teacher():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    message = ""
    if request.method == "POST":
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teachers (teacher_name, username, password, subject)
                VALUES (?, ?, ?, ?)
            """, (
                request.form["teacher_name"],
                request.form["username"],
                request.form["password"],
                request.form["subject"]
            ))
            conn.commit()
            conn.close()
            message = "Teacher added successfully!"
        except:
            message = "Error: Username already exists."

    body = f"""
        <h1>👨‍🏫 Add Teacher</h1>
        <p class="message">{message}</p>
        <form method="POST">
            <input name="teacher_name" placeholder="Teacher Name" required>
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <input name="subject" placeholder="Subject" required>
            <button>Add Teacher</button>
        </form>
        <a class="back" href="/admin/dashboard">← Back to Dashboard</a>
    """
    return page("Add Teacher", body)


@app.route("/admin/add_homework", methods=["GET", "POST"])
def add_homework():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    message = ""
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO homework
            (class_name, section, homework_date, period, subject, homework_text)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            request.form["class_name"],
            request.form.get("section", ""),
            request.form["homework_date"],
            request.form["period"],
            request.form["subject"],
            request.form["homework_text"]
        ))
        conn.commit()
        conn.close()
        message = "Homework added successfully!"

    body = f"""
        <h1>📚 Add Homework</h1>
        <p class="message">{message}</p>
        <form method="POST">
            <input name="class_name" placeholder="Class" required>
            <input name="section" placeholder="Section">
            <input type="date" name="homework_date" required>
            <select name="period" required>
                <option value="">Select Period</option>
                <option value="1">Period 1</option>
                <option value="2">Period 2</option>
                <option value="3">Period 3</option>
                <option value="4">Period 4</option>
                <option value="5">Period 5</option>
                <option value="6">Period 6</option>
                <option value="7">Period 7</option>
            </select>
            <input name="subject" placeholder="Subject" required>
            <textarea name="homework_text" placeholder="Homework" required></textarea>
            <button>Add Homework</button>
        </form>
        <a class="back" href="/admin/dashboard">← Back to Dashboard</a>
    """
    return page("Add Homework", body)


@app.route("/admin/add_attendance", methods=["GET", "POST"])
def add_attendance():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    message = ""
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance (student_id, attendance_date, status)
            VALUES (?, ?, ?)
        """, (
            request.form["student_id"],
            request.form["attendance_date"],
            request.form["status"]
        ))
        conn.commit()
        conn.close()
        message = "Attendance added successfully!"

    body = f"""
        <h1>✅ Add Attendance</h1>
        <p class="message">{message}</p>
        <form method="POST">
            <input name="student_id" placeholder="Student ID" required>
            <input type="date" name="attendance_date" required>
            <select name="status" required>
                <option value="Present">Present</option>
                <option value="Absent">Absent</option>
            </select>
            <button>Add Attendance</button>
        </form>
        <a class="back" href="/admin/dashboard">← Back to Dashboard</a>
    """
    return page("Add Attendance", body)


@app.route("/admin/add_marks", methods=["GET", "POST"])
def add_marks():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    message = ""
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO marks (student_id, subject, exam_name, marks)
            VALUES (?, ?, ?, ?)
        """, (
            request.form["student_id"],
            request.form["subject"],
            request.form["exam_name"],
            request.form["marks"]
        ))
        conn.commit()
        conn.close()
        message = "Marks added successfully!"

    body = f"""
        <h1>📝 Add Marks</h1>
        <p class="message">{message}</p>
        <form method="POST">
            <input name="student_id" placeholder="Student ID" required>
            <input name="subject" placeholder="Subject" required>
            <input name="exam_name" placeholder="Exam Name" required>
            <input type="number" name="marks" placeholder="Marks" required>
            <button>Add Marks</button>
        </form>
        <a class="back" href="/admin/dashboard">← Back to Dashboard</a>
    """
    return page("Add Marks", body)


@app.route("/admin/add_notice", methods=["GET", "POST"])
def add_notice():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    message = ""
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notices (title, message, notice_date)
            VALUES (?, ?, ?)
        """, (
            request.form["title"],
            request.form["message"],
            request.form["notice_date"]
        ))
        conn.commit()
        conn.close()
        message = "Notice added successfully!"

    body = f"""
        <h1>📢 Add Notice</h1>
        <p class="message">{message}</p>
        <form method="POST">
            <input name="title" placeholder="Notice Title" required>
            <textarea name="message" placeholder="Notice Message" required></textarea>
            <input type="date" name="notice_date" required>
            <button>Add Notice</button>
        </form>
        <a class="back" href="/admin/dashboard">← Back to Dashboard</a>
    """
    return page("Add Notice", body)


@app.route("/admin/add_activity", methods=["GET", "POST"])
def add_activity():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    message = ""
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO activities (student_id, activity_text, activity_date)
            VALUES (?, ?, ?)
        """, (
            request.form["student_id"],
            request.form["activity_text"],
            request.form["activity_date"]
        ))
        conn.commit()
        conn.close()
        message = "Activity added successfully!"

    body = f"""
        <h1>🏆 Add Activity</h1>
        <p class="message">{message}</p>
        <form method="POST">
            <input name="student_id" placeholder="Student ID" required>
            <textarea name="activity_text" placeholder="Activity" required></textarea>
            <input type="date" name="activity_date" required>
            <button>Add Activity</button>
        </form>
        <a class="back" href="/admin/dashboard">← Back to Dashboard</a>
    """
    return page("Add Activity", body)


@app.route("/admin/complaints")
def admin_complaints():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints ORDER BY id DESC")
    complaints = cursor.fetchall()
    conn.close()

    body = "<h1>📩 Parent Complaints</h1>"

    if not complaints:
        body += "<div class='card'>No complaints yet.</div>"

    for c in complaints:
        body += f"""
        <div class="card">
            <b>Complaint ID:</b> {c[0]}<br>
            <b>Parent Phone:</b> {c[1]}<br>
            <b>Student ID:</b> {c[2]}<br>
            <b>Complaint:</b> {c[3]}<br>
            <b>Status:</b> {c[4]}<br><br>
            <a class="btn" style="background:#f9a825;" href="/admin/complaint/{c[0]}/In Progress">Mark In Progress</a>
            <a class="btn" style="background:#2e7d32;" href="/admin/complaint/{c[0]}/Resolved">Mark Resolved</a>
        </div>
        """

    body += "<a class='back' href='/admin/dashboard'>← Back to Dashboard</a>"
    return page("Complaints", body)


@app.route("/admin/complaint/<int:complaint_id>/<status>")
def update_complaint(complaint_id, status):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status = ? WHERE id = ?", (status, complaint_id))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_complaints"))


@app.route("/teacher/login", methods=["GET", "POST"])
def teacher_login():
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM teachers WHERE username = ? AND password = ?
        """, (request.form["username"], request.form["password"]))
        teacher = cursor.fetchone()
        conn.close()

        if teacher:
            session["teacher_id"] = teacher[0]
            session["teacher_name"] = teacher[1]
            session["teacher_subject"] = teacher[4]
            return redirect(url_for("teacher_dashboard"))

        body = """
            <h1>👨‍🏫 Teacher Login</h1>
            <p class="message" style="background:#ffebee;color:#c62828;">Invalid teacher username or password</p>
            <form method="POST">
                <input name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button>Login</button>
            </form>
        """
        return page("Teacher Login", body, "#2e7d32", "#e8f5e9")

    body = """
        <h1>👨‍🏫 Teacher Login</h1>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button>Login</button>
        </form>
        <a class="back" href="/">← Back to Home</a>
    """
    return page("Teacher Login", body, "#2e7d32", "#e8f5e9")


@app.route("/teacher/dashboard")
def teacher_dashboard():
    if not session.get("teacher_id"):
        return redirect(url_for("teacher_login"))

    body = f"""
        <h1>👨‍🏫 Teacher Dashboard</h1>
        <div class="card">
            <b>Welcome:</b> {session['teacher_name']}<br>
            <b>Subject:</b> {session['teacher_subject']}
        </div>
        <a class="btn" href="/teacher/add_homework">📚 Add Homework</a>
        <a class="btn" href="/teacher/add_marks">📝 Add Marks</a>
        <a class="btn" style="background:#c62828;" href="/teacher/logout">Logout</a>
    """
    return page("Teacher Dashboard", body, "#2e7d32", "#e8f5e9")


@app.route("/teacher/logout")
def teacher_logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/teacher/add_homework", methods=["GET", "POST"])
def teacher_add_homework():
    if not session.get("teacher_id"):
        return redirect(url_for("teacher_login"))

    message = ""
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO homework
            (class_name, section, homework_date, period, subject, homework_text)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            request.form["class_name"],
            request.form.get("section", ""),
            request.form["homework_date"],
            request.form["period"],
            session["teacher_subject"],
            request.form["homework_text"]
        ))
        conn.commit()
        conn.close()
        message = "Homework added successfully!"

    body = f"""
        <h1>📚 Add Homework - {session['teacher_subject']}</h1>
        <p class="message">{message}</p>
        <form method="POST">
            <input name="class_name" placeholder="Class" required>
            <input name="section" placeholder="Section">
            <input type="date" name="homework_date" required>
            <select name="period" required>
                <option value="">Select Period</option>
                <option value="1">Period 1</option>
                <option value="2">Period 2</option>
                <option value="3">Period 3</option>
                <option value="4">Period 4</option>
                <option value="5">Period 5</option>
                <option value="6">Period 6</option>
                <option value="7">Period 7</option>
            </select>
            <textarea name="homework_text" placeholder="Homework" required></textarea>
            <button>Add Homework</button>
        </form>
        <a class="back" href="/teacher/dashboard">← Back to Dashboard</a>
    """
    return page("Teacher Homework", body, "#2e7d32", "#e8f5e9")


@app.route("/teacher/add_marks", methods=["GET", "POST"])
def teacher_add_marks():
    if not session.get("teacher_id"):
        return redirect(url_for("teacher_login"))

    message = ""
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO marks (student_id, subject, exam_name, marks)
            VALUES (?, ?, ?, ?)
        """, (
            request.form["student_id"],
            session["teacher_subject"],
            request.form["exam_name"],
            request.form["marks"]
        ))
        conn.commit()
        conn.close()
        message = "Marks added successfully!"

    body = f"""
        <h1>📝 Add Marks - {session['teacher_subject']}</h1>
        <p class="message">{message}</p>
        <form method="POST">
            <input name="student_id" placeholder="Student ID" required>
            <input name="exam_name" placeholder="Exam Name" required>
            <input type="number" name="marks" placeholder="Marks" required>
            <button>Add Marks</button>
        </form>
        <a class="back" href="/teacher/dashboard">← Back to Dashboard</a>
    """
    return page("Teacher Marks", body, "#2e7d32", "#e8f5e9")


@app.route("/parent/login", methods=["GET", "POST"])
def parent_login():
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM students
            WHERE parent_phone = ? AND parent_password = ?
        """, (request.form["parent_phone"], request.form["parent_password"]))
        student = cursor.fetchone()
        conn.close()

        if student:
            session["parent_phone"] = student[5]
            return redirect(url_for("parent_dashboard"))

        body = """
            <h1>👪 Parent Login</h1>
            <p class="message" style="background:#ffebee;color:#c62828;">Invalid parent phone number or password</p>
            <form method="POST">
                <input name="parent_phone" placeholder="Parent Phone" required>
                <input type="password" name="parent_password" placeholder="Password" required>
                <button>Login</button>
            </form>
        """
        return page("Parent Login", body, "#ef6c00", "#fff3e0")

    body = """
        <h1>👪 Parent Login</h1>
        <form method="POST">
            <input name="parent_phone" placeholder="Parent Phone" required>
            <input type="password" name="parent_password" placeholder="Password" required>
            <button>Login</button>
        </form>
        <a class="back" href="/">← Back to Home</a>
    """
    return page("Parent Login", body, "#ef6c00", "#fff3e0")


@app.route("/parent/dashboard")
def parent_dashboard():
    if not session.get("parent_phone"):
        return redirect(url_for("parent_login"))

    phone = session["parent_phone"]
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE parent_phone = ?", (phone,))
    student = cursor.fetchone()

    cursor.execute("""
        SELECT period, subject, homework_text FROM homework
        WHERE class_name = ? AND section = ?
        ORDER BY period
    """, (student[2], student[3]))
    homework_list = cursor.fetchall()

    cursor.execute("""
        SELECT attendance_date, status FROM attendance
        WHERE student_id = ? ORDER BY attendance_date DESC
    """, (student[0],))
    attendance_list = cursor.fetchall()

    cursor.execute("""
        SELECT subject, exam_name, marks FROM marks
        WHERE student_id = ?
    """, (student[0],))
    marks_list = cursor.fetchall()

    cursor.execute("""
        SELECT title, message, notice_date FROM notices
        ORDER BY notice_date DESC
    """)
    notice_list = cursor.fetchall()

    cursor.execute("""
        SELECT activity_text, activity_date FROM activities
        WHERE student_id = ? ORDER BY activity_date DESC
    """, (student[0],))
    activity_list = cursor.fetchall()

    conn.close()

    homework_html = ""
    for h in homework_list:
        homework_html += f"<div class='card'><b>Period {h[0]} - {h[1]}:</b> {h[2]}</div>"

    attendance_html = ""
    for a in attendance_list:
        attendance_html += f"<div class='card'><b>{a[0]}:</b> {a[1]}</div>"

    marks_html = ""
    for m in marks_list:
        marks_html += f"<div class='card'><b>{m[0]} - {m[1]}:</b> {m[2]}</div>"

    notice_html = ""
    for n in notice_list:
        notice_html += f"<div class='card'><b>{n[0]}</b><br>{n[1]}<br><i>{n[2]}</i></div>"

    activity_html = ""
    for a in activity_list:
        activity_html += f"<div class='card'><b>{a[1]}:</b> {a[0]}</div>"

    if homework_html == "":
        homework_html = "<div class='card'>No homework yet.</div>"

    if attendance_html == "":
        attendance_html = "<div class='card'>No attendance yet.</div>"

    if marks_html == "":
        marks_html = "<div class='card'>No marks yet.</div>"

    if notice_html == "":
        notice_html = "<div class='card'>No notices yet.</div>"

    if activity_html == "":
        activity_html = "<div class='card'>No activities yet.</div>"

    body = f"""
        <h1>👪 Parent Dashboard</h1>

        <h2>🎓 Student Details</h2>
        <div class="card">
            <b>Student ID:</b> {student[0]}<br>
            <b>Name:</b> {student[1]}<br>
            <b>Class:</b> {student[2]}<br>
            <b>Section:</b> {student[3]}
        </div>

        <h2>📚 Homework</h2>
        {homework_html}

        <h2>✅ Attendance</h2>
        {attendance_html}

        <h2>📝 Marks</h2>
        {marks_html}

        <h2>📢 School Notices</h2>
        {notice_html}

        <h2>🏆 Activities</h2>
        {activity_html}

        <h2>📩 Send Complaint</h2>
        <form method="POST" action="/parent/complaint">
            <textarea name="complaint_text" placeholder="Write your complaint" required></textarea>
            <button>Send Complaint</button>
        </form>

        <a class="back" href="/parent/logout">Logout</a>
    """
    return page("Parent Dashboard", body, "#ef6c00", "#fff3e0")


@app.route("/parent/complaint", methods=["POST"])
def parent_complaint():
    if not session.get("parent_phone"):
        return redirect(url_for("parent_login"))

    phone = session["parent_phone"]
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT student_id FROM students WHERE parent_phone = ?", (phone,))
    student = cursor.fetchone()

    cursor.execute("""
        INSERT INTO complaints
        (parent_phone, student_id, complaint_text, complaint_date)
        VALUES (?, ?, ?, ?)
    """, (phone, student[0], request.form["complaint_text"], date.today().isoformat()))

    conn.commit()
    conn.close()

    return redirect(url_for("parent_dashboard"))


@app.route("/parent/logout")
def parent_logout():
    session.pop("parent_phone", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

   

    conn.commit()
    conn.close()

    app.run(debug=True)