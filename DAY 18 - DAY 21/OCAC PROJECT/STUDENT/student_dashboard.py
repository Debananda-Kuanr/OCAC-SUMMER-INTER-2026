from tkinter import *
from tkinter import ttk, messagebox
import json
import mysql.connector
import sys
import os
import subprocess
from datetime import date

# ============================================================
# FILE: STUDENT/student_dashboard.py
# ============================================================

REGISTRATION_NO = sys.argv[1].strip() if len(sys.argv) > 1 else ""
STUDENT_NAME = sys.argv[2].strip() if len(sys.argv) > 2 else "Student"
LOGIN_USERNAME = sys.argv[3].strip() if len(sys.argv) > 3 else ""

if not REGISTRATION_NO:
    raise SystemExit("Registration number is required.")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
LOGIN_FILE = os.path.join(PROJECT_DIR, "COMMON GUI", "login.py")

# Separate STUDENT modules are kept in the same folder as this file.
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

try:
    import student_fees
except ImportError:
    student_fees = None

try:
    import student_payment_history
except ImportError:
    student_payment_history = None

try:
    import student_profile
except ImportError:
    student_profile = None

DB = {
    "host": "localhost",
    "user": "root",
    "password": "9439",
    "database": "OCAC_GROUP2"
}

BLUE = "#2563EB"
DARK_BLUE = "#1E40AF"
SIDEBAR = "#0F172A"
SIDEBAR_HOVER = "#1E293B"
TOPBAR = "#DBEAFE"
TOPBAR_BORDER = "#BFDBFE"
TOPBAR_TEXT = "#1E3A8A"
BG = "#F8FAFC"
WHITE = "#FFFFFF"
TEXT = "#0F172A"
MUTED = "#64748B"
BORDER = "#E2E8F0"
GREEN = "#16A34A"
RED = "#DC2626"
AMBER = "#D97706"
AMBER_BG = "#FEF3C7"

def connection():
    return mysql.connector.connect(**DB)

def fetch_one(sql, values=()):
    con = connection()
    cur = con.cursor(dictionary=True)
    try:
        cur.execute(sql, values)
        return cur.fetchone()
    finally:
        cur.close()
        con.close()

def fetch_all(sql, values=()):
    con = connection()
    cur = con.cursor(dictionary=True)
    try:
        cur.execute(sql, values)
        return cur.fetchall()
    finally:
        cur.close()
        con.close()

def execute(sql, values=()):
    con = connection()
    cur = con.cursor()
    try:
        cur.execute(sql, values)
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        cur.close()
        con.close()

def ensure_student_approval_table():
    con = connection()
    cur = con.cursor()
    try:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS student_approval_requests (
                Request_ID INT AUTO_INCREMENT PRIMARY KEY,
                Registration_No VARCHAR(50) NOT NULL,
                Request_Type VARCHAR(30) NOT NULL,
                Student_Name VARCHAR(255) NOT NULL,
                Username VARCHAR(255) NOT NULL,
                Previous_Data LONGTEXT NOT NULL,
                Proposed_Data LONGTEXT NOT NULL,
                Status VARCHAR(20) NOT NULL DEFAULT 'Pending',
                Requested_At DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                Reviewed_At DATETIME NULL,
                Reviewed_By VARCHAR(255) NULL,
                Remarks TEXT NULL,
                INDEX idx_student_approval_status (Status),
                INDEX idx_student_approval_regno (Registration_No)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        )
        con.commit()
    finally:
        cur.close()
        con.close()

def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def money(value):
    return f"Rs. {float(value or 0):,.2f}"

def get_details():
    return fetch_one(
        """
        SELECT *
        FROM student_details
        WHERE Registration_No = %s
        LIMIT 1
        """,
        (REGISTRATION_NO,)
    )

def complete(details):
    if not details:
        return False

    fields = [
        details.get("Course"),
        details.get("Semester"),
        details.get("Admission_Year"),
        details.get("Email"),
        details.get("Age"),
        details.get("Gender"),
        details.get("Phone")
    ]

    return all(
        value is not None and str(value).strip() != ""
        for value in fields
    )

def admission_is_year():
    row = fetch_one(
        """
        SELECT DATA_TYPE
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s
          AND TABLE_NAME = 'student_details'
          AND COLUMN_NAME = 'Admission_Year'
        """,
        (DB["database"],)
    )
    return bool(row and str(row["DATA_TYPE"]).lower() == "year")

def session_list():
    current = date.today().year
    return [
        f"{year}-{str(year + 1)[-2:]}"
        for year in range(current - 10, current + 1)
    ]

def session_for_display(value):
    if value is None:
        return ""

    text = str(value)

    if "-" in text:
        return text

    try:
        year = int(text)
        return f"{year}-{str(year + 1)[-2:]}"
    except Exception:
        return text

def session_for_database(value):
    if admission_is_year():
        return int(value[:4])
    return value

root = Tk()
root.title("Student Panel - Fee Status Management System")
root.minsize(1100, 680)
root.state("zoomed")
root.configure(bg=BG)

def logout():
    if not messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?",
        parent=root
    ):
        return

    if os.path.exists(LOGIN_FILE):
        subprocess.Popen(
            [sys.executable, LOGIN_FILE],
            cwd=PROJECT_DIR
        )

    root.destroy()

# ============================================================
# COMPLETE PROFILE SCREEN
# ============================================================

def show_profile_setup():
    clear(root)

    header = Frame(
        root,
        bg=TOPBAR,
        height=86,
        highlightbackground=TOPBAR_BORDER,
        highlightthickness=1
    )
    header.pack(fill=X)
    header.pack_propagate(False)

    Label(
        header,
        text="FEE STATUS MANAGEMENT SYSTEM",
        bg=TOPBAR,
        fg=TOPBAR_TEXT,
        font=("Helvetica", 17, "bold")
    ).pack(side=LEFT, padx=35)

    Label(
        header,
        text="STUDENT PROFILE SETUP",
        bg=TOPBAR,
        fg=MUTED,
        font=("Helvetica", 10, "bold")
    ).pack(side=RIGHT, padx=35)

    body = Frame(root, bg=BG)
    body.pack(fill=BOTH, expand=True)

    card = Frame(
        body,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.place(
        relx=0.5,
        rely=0.5,
        anchor=CENTER,
        width=820,
        height=575
    )

    Label(
        card,
        text="Complete Your Profile",
        bg=WHITE,
        fg=TEXT,
        font=("Helvetica", 22, "bold")
    ).pack(pady=(24, 4))

    Label(
        card,
        text="Complete all required information before continuing.",
        bg=WHITE,
        fg=MUTED,
        font=("Helvetica", 10)
    ).pack()

    form = Frame(card, bg=WHITE)
    form.pack(
        fill=BOTH,
        expand=True,
        padx=40,
        pady=18
    )

    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)

    details = get_details() or {}

    course_var = StringVar(
        value=str(details.get("Course") or "")
    )

    semester_var = StringVar(
        value=(
            f"Semester {details.get('Semester')}"
            if details.get("Semester")
            else ""
        )
    )

    admission_var = StringVar(
        value=session_for_display(
            details.get("Admission_Year")
        )
    )

    email_var = StringVar(
        value=str(details.get("Email") or "")
    )

    age_var = StringVar(
        value=str(details.get("Age") or "")
    )

    gender_var = StringVar(
        value=str(details.get("Gender") or "")
    )

    phone_var = StringVar(
        value=str(details.get("Phone") or "")
    )

    # Fetch course names without assuming only one column name.
    courses = []

    try:
        columns = fetch_all("DESC courses")
        column_names = [row["Field"] for row in columns]

        preferred = None

        for name in [
            "Course_Name",
            "Course",
            "Name",
            "course_name"
        ]:
            if name in column_names:
                preferred = name
                break

        if preferred:
            rows = fetch_all(
                f"""
                SELECT DISTINCT `{preferred}` AS Course_Name
                FROM courses
                WHERE `{preferred}` IS NOT NULL
                  AND TRIM(`{preferred}`) <> ''
                ORDER BY `{preferred}`
                """
            )

            courses = [
                str(row["Course_Name"])
                for row in rows
            ]

    except Exception:
        courses = []

    def label(text, row, col):
        Label(
            form,
            text=text,
            bg=WHITE,
            fg=TEXT,
            font=("Helvetica", 9, "bold")
        ).grid(
            row=row,
            column=col,
            sticky="w",
            pady=(7, 5)
        )

    def locked(value, row, col):
        entry = Entry(
            form,
            font=("Helvetica", 10),
            bg="#F1F5F9",
            fg=MUTED,
            relief=SOLID,
            bd=1
        )

        entry.insert(0, value)
        entry.config(state="readonly")

        entry.grid(
            row=row,
            column=col,
            sticky="ew",
            padx=(0, 18) if col == 0 else (18, 0),
            ipady=8
        )

    label("REGISTRATION NO.", 0, 0)
    label("STUDENT STUDENT_NAME", 0, 1)

    locked(REGISTRATION_NO, 1, 0)
    locked(STUDENT_NAME, 1, 1)

    label("COURSE", 2, 0)
    label("SEMESTER", 2, 1)

    ttk.Combobox(
        form,
        textvariable=course_var,
        values=courses,
        state="readonly",
        font=("Helvetica", 10)
    ).grid(
        row=3,
        column=0,
        sticky="ew",
        padx=(0, 18),
        ipady=7
    )

    ttk.Combobox(
        form,
        textvariable=semester_var,
        values=[
            f"Semester {number}"
            for number in range(1, 13)
        ],
        state="readonly",
        font=("Helvetica", 10)
    ).grid(
        row=3,
        column=1,
        sticky="ew",
        padx=(18, 0),
        ipady=7
    )

    label("ADMISSION SESSION", 4, 0)
    label("GENDER", 4, 1)

    ttk.Combobox(
        form,
        textvariable=admission_var,
        values=session_list(),
        state="readonly",
        font=("Helvetica", 10)
    ).grid(
        row=5,
        column=0,
        sticky="ew",
        padx=(0, 18),
        ipady=7
    )

    ttk.Combobox(
        form,
        textvariable=gender_var,
        values=["Male", "Female", "Other"],
        state="readonly",
        font=("Helvetica", 10)
    ).grid(
        row=5,
        column=1,
        sticky="ew",
        padx=(18, 0),
        ipady=7
    )

    label("EMAIL", 6, 0)
    label("PHONE NUMBER", 6, 1)

    Entry(
        form,
        textvariable=email_var,
        font=("Helvetica", 10),
        relief=SOLID,
        bd=1
    ).grid(
        row=7,
        column=0,
        sticky="ew",
        padx=(0, 18),
        ipady=8
    )

    Entry(
        form,
        textvariable=phone_var,
        font=("Helvetica", 10),
        relief=SOLID,
        bd=1
    ).grid(
        row=7,
        column=1,
        sticky="ew",
        padx=(18, 0),
        ipady=8
    )

    label("AGE", 8, 0)

    Entry(
        form,
        textvariable=age_var,
        font=("Helvetica", 10),
        relief=SOLID,
        bd=1
    ).grid(
        row=9,
        column=0,
        sticky="ew",
        padx=(0, 18),
        ipady=8
    )

    def save_profile():
        course = course_var.get().strip()
        semester_text = semester_var.get().strip()
        admission = admission_var.get().strip()
        email = email_var.get().strip()
        age = age_var.get().strip()
        gender = gender_var.get().strip()
        phone = phone_var.get().strip()

        if not all([
            course,
            semester_text,
            admission,
            email,
            age,
            gender,
            phone
        ]):
            messagebox.showwarning(
                "Required Fields",
                "Please complete all fields.",
                parent=root
            )
            return

        if (
            "@" not in email
            or
            "." not in email.split("@")[-1]
        ):
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address.",
                parent=root
            )
            return

        if (
            not age.isdigit()
            or
            not 15 <= int(age) <= 100
        ):
            messagebox.showwarning(
                "Invalid Age",
                "Age must be between 15 and 100.",
                parent=root
            )
            return

        phone_digits = "".join(
            character
            for character in phone
            if character.isdigit()
        )

        if len(phone_digits) != 10:
            messagebox.showwarning(
                "Invalid Phone",
                "Phone number must contain 10 digits.",
                parent=root
            )
            return

        semester = int(
            semester_text
            .replace("Semester", "")
            .strip()
        )

        admission_db = session_for_database(
            admission
        )

        try:
            existing = get_details() or {}
            ensure_student_approval_table()
            request_type = "profile_update" if existing else "new_student"

            previous_data = {
                "Course": str(existing.get("Course") or ""),
                "Semester": str(existing.get("Semester") or ""),
                "Admission_Year": str(existing.get("Admission_Year") or ""),
                "Email": str(existing.get("Email") or ""),
                "Age": str(existing.get("Age") or ""),
                "Gender": str(existing.get("Gender") or ""),
                "Phone": str(existing.get("Phone") or ""),
                "Status": str(existing.get("Status") or "Inactive"),
            }

            proposed_data = {
                "Course": course,
                "Semester": semester,
                "Admission_Year": admission_db,
                "Email": email,
                "Age": int(age),
                "Gender": gender,
                "Phone": phone_digits,
                "Status": "Pending Approval",
            }

            execute(
                """
                INSERT INTO student_approval_requests
                (
                    Registration_No,
                    Request_Type,
                    Student_Name,
                    Username,
                    Previous_Data,
                    Proposed_Data,
                    Status
                )
                VALUES
                (
                    %s, %s, %s, %s, %s, %s, 'Pending'
                )
                """,
                (
                    REGISTRATION_NO,
                    request_type,
                    STUDENT_NAME,
                    LOGIN_USERNAME,
                    json.dumps(previous_data, ensure_ascii=True),
                    json.dumps(proposed_data, ensure_ascii=True)
                )
            )

            if existing:
                execute(
                    """
                    UPDATE student_details
                    SET
                        Status = 'Pending Approval'
                    WHERE Registration_No = %s
                    """,
                    (REGISTRATION_NO,)
                )
            else:
                execute(
                    """
                    INSERT INTO student_details
                    (
                        Registration_No,
                        Course,
                        Semester,
                        Admission_Year,
                        Email,
                        Age,
                        Gender,
                        Phone,
                        Status
                    )
                    VALUES
                    (
                        %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        'Pending Approval'
                    )
                    """,
                    (
                        REGISTRATION_NO,
                        course,
                        semester,
                        admission_db,
                        email,
                        int(age),
                        gender,
                        phone_digits
                    )
                )

            messagebox.showinfo(
                "Profile Submitted",
                (
                    "Your profile change request was submitted successfully."
                    "\n\nStatus: PENDING APPROVAL"
                    "\n\nAdministrator approval is required "
                    "before the update becomes active."
                ),
                parent=root
            )

            show_inactive()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error),
                parent=root
            )

    Label(
        form,
        text=(
            "After saving, your status becomes Inactive "
            "until an administrator approves the profile."
        ),
        bg=WHITE,
        fg=MUTED,
        font=("Helvetica", 8),
        wraplength=450,
        justify=LEFT
    ).grid(
        row=10,
        column=0,
        sticky="w",
        pady=(22, 0)
    )

    Button(
        form,
        text="SAVE & CONTINUE",
        bg=BLUE,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        font=("Helvetica", 10, "bold"),
        command=save_profile
    ).grid(
        row=10,
        column=1,
        sticky="e",
        pady=(22, 0),
        ipadx=20,
        ipady=10
    )

    def close_incomplete():
        if messagebox.askyesno(
            "Profile Completion Required",
            (
                "You cannot access the Student Dashboard "
                "until your profile is complete."
                "\n\nLogout now?"
            ),
            parent=root
        ):
            logout()

    root.protocol(
        "WM_DELETE_WINDOW",
        close_incomplete
    )

# ============================================================
# INACTIVE SCREEN
# ============================================================

def show_inactive():
    clear(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    header = Frame(
        root,
        bg=TOPBAR,
        height=86,
        highlightbackground=TOPBAR_BORDER,
        highlightthickness=1
    )
    header.pack(fill=X)
    header.pack_propagate(False)

    Label(
        header,
        text="FEE STATUS MANAGEMENT SYSTEM",
        bg=TOPBAR,
        fg=TOPBAR_TEXT,
        font=("Helvetica", 17, "bold")
    ).pack(side=LEFT, padx=35)

    body = Frame(root, bg=BG)
    body.pack(fill=BOTH, expand=True)

    card = Frame(
        body,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.place(
        relx=0.5,
        rely=0.5,
        anchor=CENTER,
        width=620,
        height=390
    )

    Label(
        card,
        text="PROFILE UNDER REVIEW",
        bg=WHITE,
        fg=TEXT,
        font=("Helvetica", 22, "bold")
    ).pack(pady=(55, 10))

    Label(
        card,
        text=(
            "Your profile change request has been submitted.\n"
            "Administrator approval is required before "
            "the update becomes active."
        ),
        bg=WHITE,
        fg=MUTED,
        font=("Helvetica", 11),
        justify=CENTER
    ).pack(pady=8)

    info = Frame(card, bg="#F8FAFC")
    info.pack(fill=X, padx=55, pady=22)

    Label(
        info,
        text=f"Registration No: {REGISTRATION_NO}",
        bg="#F8FAFC",
        fg=TEXT,
        font=("Helvetica", 10, "bold")
    ).pack(pady=(14, 5))

    Label(
        info,
        text="Status: PENDING APPROVAL",
        bg="#F8FAFC",
        fg=AMBER,
        font=("Helvetica", 10, "bold")
    ).pack(pady=(5, 14))

    Button(
        card,
        text="LOGOUT",
        bg=RED,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        font=("Helvetica", 10, "bold"),
        command=logout
    ).pack(
        ipadx=30,
        ipady=10
    )

# ============================================================
# ACTIVE DASHBOARD
# ============================================================

sidebar = None
content = None
page_title = StringVar(value="Dashboard")
page_subtitle = StringVar(
    value="View your fee status, payments and outstanding dues."
)
nav = {}

def set_nav(name):
    for key, button in nav.items():
        button.config(
            bg=BLUE if key == name else SIDEBAR,
            fg=WHITE if key == name else "#CBD5E1"
        )

def new_page(title, subtitle):
    page_title.set(title)
    page_subtitle.set(subtitle)
    clear(content)

def fee_summary():
    row = fetch_one(
        """
        SELECT
            COALESCE(SUM(Total_Fee), 0) AS Total_Assigned,
            COALESCE(SUM(Amount_Paid), 0) AS Total_Paid,
            COALESCE(SUM(Due_Amount), 0) AS Total_Due
        FROM student_fees
        WHERE Registration_No = %s
        """,
        (REGISTRATION_NO,)
    ) or {}

    return (
        float(row.get("Total_Assigned") or 0),
        float(row.get("Total_Paid") or 0),
        float(row.get("Total_Due") or 0)
    )


def semester_fees():
    return fetch_all(
        """
        SELECT
            fs.Semester,
            COALESCE(SUM(sf.Total_Fee), 0) AS Total_Assigned,
            COALESCE(SUM(sf.Amount_Paid), 0) AS Total_Paid,
            COALESCE(SUM(sf.Due_Amount), 0) AS Total_Due
        FROM student_fees sf
        INNER JOIN fee_structures fs
            ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
        WHERE sf.Registration_No = %s
        GROUP BY fs.Semester
        ORDER BY fs.Semester
        """,
        (REGISTRATION_NO,)
    )


def show_dashboard():

    set_nav("Dashboard")
    new_page(
        "Dashboard",
        "View your fee status, payments and outstanding dues."
    )

    page = content

    details = get_details() or {}

    student_name = STUDENT_NAME or "Student"
    registration_no = details.get("Registration_No") or REGISTRATION_NO
    course = details.get("Course") or "Not Assigned"
    current_semester = int(details.get("Semester") or 0)
    admission_year = details.get("Admission_Year") or "-"

    total_fee, total_paid, total_due = fee_summary()

    if total_fee <= 0:
        fee_status = "NOT ASSIGNED"
        fee_status_color = MUTED
    elif total_due <= 0:
        fee_status = "PAID"
        fee_status_color = GREEN
    elif total_paid > 0:
        fee_status = "PARTIAL"
        fee_status_color = AMBER
    else:
        fee_status = "UNPAID"
        fee_status_color = RED

    semester_rows = semester_fees()

    previous_total = 0.0
    previous_paid = 0.0
    previous_due = 0.0
    current_total = 0.0
    current_paid = 0.0
    current_due = 0.0

    for row in semester_rows:

        semester_no = int(row.get("Semester") or 0)
        row_total = float(row.get("Total_Assigned") or 0)
        row_paid = float(row.get("Total_Paid") or 0)
        row_due = float(row.get("Total_Due") or 0)

        if semester_no < current_semester:
            previous_total += row_total
            previous_paid += row_paid
            previous_due += row_due

        elif semester_no == current_semester:
            current_total += row_total
            current_paid += row_paid
            current_due += row_due

    recent_rows = fetch_all(
        """
        SELECT
            fp.Payment_ID,
            fp.Payment_Date,
            fs.Semester,
            fp.Payment_Mode,
            fp.Amount
        FROM fee_payments fp
        INNER JOIN student_fees sf
            ON sf.Student_Fee_ID = fp.Student_Fee_ID
        INNER JOIN fee_structures fs
            ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
        WHERE sf.Registration_No = %s
        ORDER BY fp.Payment_Date DESC, fp.Payment_ID DESC
        LIMIT 5
        """,
        (REGISTRATION_NO,)
    )

    # ========================================================
    # SCROLLABLE DASHBOARD
    # ========================================================

    outer = Frame(page, bg=BG)
    outer.pack(fill=BOTH, expand=True)

    canvas = Canvas(
        outer,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        outer,
        orient=VERTICAL,
        command=canvas.yview
    )

    body = Frame(canvas, bg=BG)

    body_window = canvas.create_window(
        (0, 0),
        window=body,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )

    scrollbar.pack(
        side=RIGHT,
        fill=Y
    )

    body.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(
            body_window,
            width=event.width
        )
    )

    scroll_state = {
        "target": 0.0,
        "job": None
    }

    def scroll_metrics():
        bbox = canvas.bbox("all")

        if not bbox:
            return 1.0, 0.0

        content_height = max(
            1.0,
            float(bbox[3] - bbox[1])
        )

        viewport_height = max(
            1.0,
            float(canvas.winfo_height())
        )

        max_scroll = max(
            0.0,
            content_height - viewport_height
        )

        return content_height, max_scroll

    def current_scroll_pixels():
        content_height, _ = scroll_metrics()

        return (
            canvas.yview()[0]
            * content_height
        )

    def animate_scroll():
        content_height, max_scroll = scroll_metrics()

        target = max(
            0.0,
            min(
                scroll_state["target"],
                max_scroll
            )
        )

        current = current_scroll_pixels()
        difference = target - current

        if abs(difference) < 0.8:
            canvas.yview_moveto(
                target / content_height
            )

            scroll_state["job"] = None
            return

        next_position = current + (
            difference * 0.24
        )

        canvas.yview_moveto(
            next_position / content_height
        )

        scroll_state["job"] = root.after(
            10,
            animate_scroll
        )

    def dashboard_scroll(event):
        _, max_scroll = scroll_metrics()

        if max_scroll <= 0:
            return "break"

        direction = (
            -1
            if event.delta > 0
            else 1
        )

        scroll_state["target"] = max(
            0.0,
            min(
                current_scroll_pixels()
                + direction * 120,
                max_scroll
            )
        )

        if scroll_state["job"] is None:
            animate_scroll()

        return "break"

    def enable_dashboard_scroll(event=None):
        scroll_state["target"] = (
            current_scroll_pixels()
        )

        canvas.bind_all(
            "<MouseWheel>",
            dashboard_scroll
        )

    def disable_dashboard_scroll(event=None):
        canvas.unbind_all(
            "<MouseWheel>"
        )

        if scroll_state["job"] is not None:
            try:
                root.after_cancel(
                    scroll_state["job"]
                )
            except Exception:
                pass

            scroll_state["job"] = None

    canvas.bind(
        "<Enter>",
        enable_dashboard_scroll
    )

    body.bind(
        "<Enter>",
        enable_dashboard_scroll
    )

    canvas.bind(
        "<Leave>",
        disable_dashboard_scroll
    )

    # ========================================================
    # WELCOME
    # ========================================================

    welcome = Frame(body, bg=BG)
    welcome.pack(
        fill=X,
        padx=25,
        pady=(22, 15)
    )

    Label(
        welcome,
        text=f"Welcome back, {student_name}",
        bg=BG,
        fg=TEXT,
        font=("Helvetica", 20, "bold")
    ).pack(anchor="w")

    Label(
        welcome,
        text=(
            f"{registration_no}  •  "
            f"{course}  •  "
            f"Semester {current_semester}"
        ),
        bg=BG,
        fg=MUTED,
        font=("Helvetica", 10)
    ).pack(
        anchor="w",
        pady=(7, 0)
    )

    # ========================================================
    # SUMMARY CARDS
    # ========================================================

    summary = Frame(body, bg=BG)
    summary.pack(
        fill=X,
        padx=25,
        pady=(0, 18)
    )

    for column in range(4):
        summary.grid_columnconfigure(
            column,
            weight=1,
            uniform="summary"
        )

    def make_summary_card(
        column,
        title,
        value,
        value_color
    ):

        card = Frame(
            summary,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(
                0 if column == 0 else 6,
                0 if column == 3 else 6
            )
        )

        Label(
            card,
            text=title,
            bg=WHITE,
            fg=MUTED,
            font=("Helvetica", 9, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 8)
        )

        Label(
            card,
            text=value,
            bg=WHITE,
            fg=value_color,
            font=("Helvetica", 17, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

    make_summary_card(
        0,
        "TOTAL FEES",
        money(total_fee),
        BLUE
    )

    make_summary_card(
        1,
        "TOTAL PAID",
        money(total_paid),
        GREEN
    )

    make_summary_card(
        2,
        "TOTAL DUE",
        money(total_due),
        RED
    )

    make_summary_card(
        3,
        "FEE STATUS",
        fee_status,
        fee_status_color
    )

    # ========================================================
    # PREVIOUS SEMESTER OUTSTANDING
    # ========================================================

    if previous_due > 0:

        warning = Frame(
            body,
            bg="#FFF7D6",
            highlightbackground="#F3C94F",
            highlightthickness=1
        )

        warning.pack(
            fill=X,
            padx=25,
            pady=(0, 18)
        )

        Label(
            warning,
            text="PREVIOUS SEMESTER OUTSTANDING",
            bg="#FFF7D6",
            fg=AMBER,
            font=("Helvetica", 10, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        warning_box = Frame(
            warning,
            bg=WHITE,
            highlightbackground="#F0D77B",
            highlightthickness=1
        )

        warning_box.pack(
            fill=X,
            padx=20,
            pady=(0, 18)
        )

        info = Frame(
            warning_box,
            bg=WHITE
        )

        info.pack(
            side=LEFT,
            fill=X,
            expand=True,
            padx=20,
            pady=16
        )

        Label(
            info,
            text=f"Semester {max(current_semester - 1, 1)}",
            bg=WHITE,
            fg=TEXT,
            font=("Helvetica", 11, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 45)
        )

        Label(
            info,
            text=f"Total  {money(previous_total)}",
            bg=WHITE,
            fg=TEXT,
            font=("Helvetica", 10)
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(0, 45)
        )

        Label(
            info,
            text=f"Paid  {money(previous_paid)}",
            bg=WHITE,
            fg=TEXT,
            font=("Helvetica", 10)
        ).grid(
            row=0,
            column=2,
            sticky="w"
        )

        Label(
            info,
            text="Outstanding",
            bg=WHITE,
            fg=MUTED,
            font=("Helvetica", 9, "bold")
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(12, 0)
        )

        Label(
            info,
            text=money(previous_due),
            bg=WHITE,
            fg=RED,
            font=("Helvetica", 14, "bold")
        ).grid(
            row=1,
            column=1,
            columnspan=2,
            sticky="w",
            pady=(12, 0)
        )

        Button(
            warning_box,
            text="VIEW DETAILS",
            command=show_fees,
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            font=("Helvetica", 9, "bold"),
            padx=18,
            pady=9
        ).pack(
            side=RIGHT,
            padx=20,
            pady=20
        )

    # ========================================================
    # CURRENT SEMESTER FEE
    # ========================================================

    Label(
        body,
        text="CURRENT SEMESTER FEE",
        bg=BG,
        fg=TEXT,
        font=("Helvetica", 11, "bold")
    ).pack(
        anchor="w",
        padx=25,
        pady=(0, 10)
    )

    middle = Frame(body, bg=BG)
    middle.pack(
        fill=X,
        padx=25,
        pady=(0, 18)
    )

    middle.grid_columnconfigure(
        0,
        weight=2
    )

    middle.grid_columnconfigure(
        1,
        weight=1
    )

    current_card = Frame(
        middle,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    current_card.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 8)
    )

    Label(
        current_card,
        text=f"Semester {current_semester}",
        bg=WHITE,
        fg=TEXT,
        font=("Helvetica", 15, "bold")
    ).pack(
        anchor="w",
        padx=22,
        pady=(20, 16)
    )

    current_info = Frame(
        current_card,
        bg=WHITE
    )

    current_info.pack(
        fill=X,
        padx=22
    )

    def current_fee_row(
        row_number,
        title,
        value,
        value_color=TEXT
    ):

        Label(
            current_info,
            text=title,
            bg=WHITE,
            fg=MUTED,
            font=("Helvetica", 10)
        ).grid(
            row=row_number,
            column=0,
            sticky="w",
            pady=5
        )

        Label(
            current_info,
            text=value,
            bg=WHITE,
            fg=value_color,
            font=("Helvetica", 10, "bold")
        ).grid(
            row=row_number,
            column=1,
            sticky="w",
            padx=(35, 0),
            pady=5
        )

    current_fee_row(
        0,
        "Total Fee",
        money(current_total)
    )

    current_fee_row(
        1,
        "Paid",
        money(current_paid),
        GREEN
    )

    current_fee_row(
        2,
        "Due",
        money(current_due),
        RED
    )

    if current_total > 0:
        progress_percent = min(
            100,
            max(
                0,
                int(
                    current_paid
                    / current_total
                    * 100
                )
            )
        )
    else:
        progress_percent = 0

    progress_row = Frame(
        current_card,
        bg=WHITE
    )

    progress_row.pack(
        fill=X,
        padx=22,
        pady=(18, 8)
    )

    progress_track = Frame(
        progress_row,
        bg="#E7EDF5",
        height=12
    )

    progress_track.pack(
        side=LEFT,
        fill=X,
        expand=True
    )

    progress_track.pack_propagate(False)

    def draw_progress(event=None):

        for child in progress_track.winfo_children():
            child.destroy()

        track_width = progress_track.winfo_width()

        fill_width = int(
            track_width
            * progress_percent
            / 100
        )

        if fill_width > 0:

            Frame(
                progress_track,
                bg=GREEN,
                width=fill_width,
                height=12
            ).place(
                x=0,
                y=0
            )

    progress_track.bind(
        "<Configure>",
        draw_progress
    )

    Label(
        progress_row,
        text=f"{progress_percent}%",
        bg=WHITE,
        fg=MUTED,
        font=("Helvetica", 9, "bold")
    ).pack(
        side=LEFT,
        padx=(10, 0)
    )

    Button(
        current_card,
        text="VIEW MY FEES",
        command=show_fees,
        bg=BLUE,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        relief=FLAT,
        bd=0,
        cursor="hand2",
        font=("Helvetica", 9, "bold"),
        padx=18,
        pady=9
    ).pack(
        anchor="e",
        padx=22,
        pady=(10, 20)
    )

    # ========================================================
    # MY PROFILE CARD
    # ========================================================

    profile_card = Frame(
        middle,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    profile_card.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(8, 0)
    )

    Label(
        profile_card,
        text="MY PROFILE",
        bg=WHITE,
        fg=TEXT,
        font=("Helvetica", 13, "bold")
    ).pack(
        anchor="w",
        padx=22,
        pady=(20, 18)
    )

    profile_items = [
        ("REG NO.", registration_no),
        ("COURSE", course),
        ("BATCH", str(admission_year)),
        ("SEMESTER", str(current_semester))
    ]

    for label_text, value_text in profile_items:

        Label(
            profile_card,
            text=label_text,
            bg=WHITE,
            fg=MUTED,
            font=("Helvetica", 8, "bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(4, 2)
        )

        Label(
            profile_card,
            text=value_text,
            bg=WHITE,
            fg=TEXT,
            font=("Helvetica", 10, "bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 7)
        )

    Button(
        profile_card,
        text="MY PROFILE",
        command=show_profile,
        bg="#EAF2FF",
        fg=BLUE,
        activebackground="#DCEAFF",
        activeforeground=BLUE,
        relief=FLAT,
        bd=0,
        cursor="hand2",
        font=("Helvetica", 9, "bold"),
        padx=18,
        pady=9
    ).pack(
        anchor="e",
        padx=22,
        pady=(10, 20)
    )

    # ========================================================
    # RECENT PAYMENTS
    # ========================================================

    recent_card = Frame(
        body,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    recent_card.pack(
        fill=X,
        padx=25,
        pady=(0, 25)
    )

    recent_header = Frame(
        recent_card,
        bg=WHITE
    )

    recent_header.pack(
        fill=X,
        padx=20,
        pady=(18, 12)
    )

    Label(
        recent_header,
        text="RECENT PAYMENTS",
        bg=WHITE,
        fg=TEXT,
        font=("Helvetica", 12, "bold")
    ).pack(side=LEFT)

    Button(
        recent_header,
        text="VIEW ALL PAYMENTS",
        command=show_payments,
        bg=BLUE,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        relief=FLAT,
        bd=0,
        cursor="hand2",
        font=("Helvetica", 9, "bold"),
        padx=16,
        pady=8
    ).pack(side=RIGHT)

    table = Frame(
        recent_card,
        bg=WHITE
    )

    table.pack(
        fill=X,
        padx=20,
        pady=(0, 20)
    )

    headers = [
        "PAYMENT ID",
        "DATE",
        "SEMESTER",
        "MODE",
        "AMOUNT"
    ]

    for column, header in enumerate(headers):

        table.grid_columnconfigure(
            column,
            weight=1
        )

        Label(
            table,
            text=header,
            bg="#F4F7FB",
            fg=MUTED,
            font=("Helvetica", 9, "bold"),
            anchor="w",
            padx=12,
            pady=10
        ).grid(
            row=0,
            column=column,
            sticky="nsew"
        )

    if recent_rows:

        for row_number, row in enumerate(
            recent_rows,
            start=1
        ):

            payment_date = row["Payment_Date"]

            if hasattr(
                payment_date,
                "strftime"
            ):
                payment_date = payment_date.strftime(
                    "%d-%m-%Y"
                )

            values = [
                f"PAY-{int(row['Payment_ID']):06d}",
                str(payment_date),
                f"Semester {row['Semester']}",
                row["Payment_Mode"],
                money(
                    float(
                        row["Amount"]
                        or 0
                    )
                )
            ]

            for column, value in enumerate(values):

                Label(
                    table,
                    text=value,
                    bg=WHITE,
                    fg=TEXT,
                    font=("Helvetica", 9),
                    anchor="w",
                    padx=12,
                    pady=9
                ).grid(
                    row=row_number,
                    column=column,
                    sticky="nsew"
                )

    else:

        Label(
            table,
            text="No payment records found.",
            bg=WHITE,
            fg=MUTED,
            font=("Helvetica", 10),
            pady=25
        ).grid(
            row=1,
            column=0,
            columnspan=5,
            sticky="ew"
        )




# ============================================================
# FUTURE STUDENT MODULES
# These three screens will be designed in separate Python files.
# ============================================================

def show_fees():
    set_nav("My Fees")

    new_page(
        "My Fees",
        "View your semester-wise assigned fees and outstanding dues."
    )

    # Use the same database configuration as the dashboard.
    student_fees.DB_CONFIG.clear()
    student_fees.DB_CONFIG.update(DB)

    # My Fees remains completely inside student_fees.py.
    student_fees.show_student_fees(
        parent=content,
        registration_no=REGISTRATION_NO,
        student_name=STUDENT_NAME,
        colors={
            "BG": BG,
            "WHITE": WHITE,
            "TEXT": TEXT,
            "MUTED": MUTED,
            "BLUE": BLUE,
            "GREEN": GREEN,
            "RED": RED,
            "AMBER": AMBER,
            "BORDER": BORDER
        }
    )

def show_payments():
    set_nav("Payment History")

    new_page(
        "Payment History",
        "View all your fee payment transactions."
    )

    if student_payment_history is None:
        messagebox.showerror(
            "Module Missing",
            "student_payment_history.py could not be loaded.",
            parent=root
        )
        return

    student_payment_history.DB_CONFIG.clear()
    student_payment_history.DB_CONFIG.update(DB)

    student_payment_history.show_student_payment_history(
        parent=content,
        registration_no=REGISTRATION_NO,
        student_name=STUDENT_NAME,
        colors={
            "BG": BG,
            "WHITE": WHITE,
            "TEXT": TEXT,
            "MUTED": MUTED,
            "BLUE": BLUE,
            "GREEN": GREEN,
            "RED": RED,
            "AMBER": AMBER,
            "BORDER": BORDER,
            "SOFT_BLUE": "#EFF6FF",
            "SOFT_GREEN": "#F0FDF4",
            "SOFT_RED": "#FEF2F2",
            "SOFT_AMBER": "#FFFBEB",
            "SIDEBAR": SIDEBAR,
            "SIDEBAR_HOVER": SIDEBAR_HOVER
        }
    )


def show_profile():
    set_nav("My Profile")

    new_page(
        "My Profile",
        "View your personal and academic information."
    )

    if student_profile is None:
        messagebox.showerror(
            "Module Missing",
            "student_profile.py could not be loaded.",
            parent=root
        )
        return

    student_profile.DB_CONFIG.clear()
    student_profile.DB_CONFIG.update(DB)

    student_profile.show_student_profile(
        parent=content,
        registration_no=REGISTRATION_NO,
        student_name=STUDENT_NAME,
        login_username=LOGIN_USERNAME,
        colors={
            "BG": BG,
            "WHITE": WHITE,
            "TEXT": TEXT,
            "MUTED": MUTED,
            "BLUE": BLUE,
            "GREEN": GREEN,
            "RED": RED,
            "AMBER": AMBER,
            "BORDER": BORDER,
            "SOFT_BLUE": "#EFF6FF",
            "SOFT_GREEN": "#F0FDF4",
            "SOFT_RED": "#FEF2F2",
            "SOFT_AMBER": "#FFFBEB",
            "SIDEBAR": SIDEBAR,
            "SIDEBAR_HOVER": SIDEBAR_HOVER,
            "TOP": TOPBAR,
            "TOP_BORDER": TOPBAR_BORDER,
            "TOP_TEXT": TOPBAR_TEXT
        }
    )



def create_dashboard():
    global sidebar
    global content

    clear(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        root.destroy
    )

    sidebar = Frame(
        root,
        bg=SIDEBAR,
        width=245
    )

    sidebar.pack(
        side=LEFT,
        fill=Y
    )

    sidebar.pack_propagate(False)

    main = Frame(root, bg=BG)
    main.pack(
        side=RIGHT,
        fill=BOTH,
        expand=True
    )

    brand = Frame(
        sidebar,
        bg=SIDEBAR,
        height=105
    )

    brand.pack(fill=X)
    brand.pack_propagate(False)

    Label(
        brand,
        text="FEE STATUS\nMANAGEMENT SYSTEM",
        bg=SIDEBAR,
        fg=WHITE,
        font=("Helvetica", 12, "bold"),
        justify=LEFT,
        anchor="w"
    ).pack(
        side=LEFT,
        padx=25,
        pady=25
    )

    Label(
        sidebar,
        text="STUDENT PANEL",
        bg=SIDEBAR,
        fg="#94A3B8",
        font=("Helvetica", 8, "bold"),
        anchor="w"
    ).pack(
        fill=X,
        padx=20,
        pady=(15, 8)
    )

    def add_nav(name, command):
        button = Button(
            sidebar,
            text=name,
            bg=SIDEBAR,
            fg="#CBD5E1",
            activebackground=SIDEBAR_HOVER,
            activeforeground=WHITE,
            bd=0,
            anchor="w",
            padx=22,
            pady=12,
            cursor="hand2",
            font=("Helvetica", 10, "bold"),
            command=command
        )

        button.pack(
            fill=X,
            padx=8,
            pady=2
        )

        nav[name] = button

    add_nav("Dashboard", show_dashboard)
    add_nav("My Fees", show_fees)
    add_nav("Payment History", show_payments)
    add_nav("My Profile", show_profile)

    bottom = Frame(
        sidebar,
        bg=SIDEBAR
    )

    bottom.pack(
        side=BOTTOM,
        fill=X,
        padx=16,
        pady=18
    )

    Label(
        bottom,
        text=STUDENT_NAME,
        bg=SIDEBAR,
        fg=WHITE,
        font=("Helvetica", 10, "bold"),
        anchor="w"
    ).pack(fill=X)

    Label(
        bottom,
        text=REGISTRATION_NO,
        bg=SIDEBAR,
        fg="#94A3B8",
        font=("Helvetica", 8),
        anchor="w"
    ).pack(
        fill=X,
        pady=(2, 12)
    )

    Button(
        bottom,
        text="LOGOUT",
        bg=RED,
        fg=WHITE,
        activebackground="#334155",
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        font=("Helvetica", 9, "bold"),
        command=logout
    ).pack(
        fill=X,
        ipady=8
    )

    topbar = Frame(
        main,
        bg=TOPBAR,
        height=86,
        highlightbackground=TOPBAR_BORDER,
        highlightthickness=1
    )

    topbar.pack(fill=X)
    topbar.pack_propagate(False)

    title_box = Frame(
        topbar,
        bg=TOPBAR
    )

    title_box.pack(
        side=LEFT,
        padx=30,
        pady=16
    )

    Label(
        title_box,
        textvariable=page_title,
        bg=TOPBAR,
        fg=TOPBAR_TEXT,
        font=("Helvetica", 17, "bold")
    ).pack(anchor="w")

    Label(
        title_box,
        textvariable=page_subtitle,
        bg=TOPBAR,
        fg=MUTED,
        font=("Helvetica", 9)
    ).pack(
        anchor="w",
        pady=(3, 0)
    )

    profile = Frame(
        topbar,
        bg=TOPBAR
    )

    profile.pack(
        side=RIGHT,
        padx=30,
        pady=16
    )

    Label(
        profile,
        text=STUDENT_NAME[:1].upper(),
        bg=BLUE,
        fg=WHITE,
        font=("Helvetica", 11, "bold"),
        width=3,
        height=2
    ).pack(
        side=LEFT,
        padx=(0, 10)
    )

    profile_text = Frame(
        profile,
        bg=TOPBAR
    )

    profile_text.pack(side=LEFT)

    Label(
        profile_text,
        text=STUDENT_NAME,
        bg=TOPBAR,
        fg=TEXT,
        font=("Helvetica", 10, "bold")
    ).pack(anchor="w")

    Label(
        profile_text,
        text="Student",
        bg=TOPBAR,
        fg=MUTED,
        font=("Helvetica", 8)
    ).pack(anchor="w")

    content = Frame(
        main,
        bg=BG
    )

    content.pack(
        fill=BOTH,
        expand=True
    )

    show_dashboard()

# ============================================================
# ROUTE STUDENT BY STATUS
# ============================================================

def route():
    try:
        details = get_details()

        if (
            not details
            or
            not complete(details)
        ):
            show_profile_setup()
            return

        status = str(
            details.get("Status")
            or "Incomplete"
        ).strip().lower()

        if status == "active":
            create_dashboard()

        elif status in ("inactive", "pending approval"):
            show_inactive()

        else:
            show_profile_setup()

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error),
            parent=root
        )

        root.destroy()

route()
root.mainloop()
