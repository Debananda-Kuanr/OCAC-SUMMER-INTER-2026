from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
import json
import mysql.connector
import os
import sys
from types import SimpleNamespace


# ============================================================
# DATABASE CONFIGURATION
# Updated from student_dashboard.py at runtime.
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ocac_group2"
}


# ============================================================
# DEFAULT COLORS
# ============================================================

DEFAULT_COLORS = {
    "BG": "#F4F7FB",
    "WHITE": "#FFFFFF",
    "TEXT": "#0F172A",
    "MUTED": "#64748B",
    "BLUE": "#2563EB",
    "GREEN": "#16A34A",
    "RED": "#DC2626",
    "AMBER": "#D97706",
    "BORDER": "#DCE3EC",
    "SOFT_BLUE": "#EFF6FF",
    "SOFT_GREEN": "#F0FDF4",
    "SOFT_RED": "#FEF2F2",
    "SOFT_AMBER": "#FFFBEB",
    "SIDEBAR": "#0F172A",
    "SIDEBAR_HOVER": "#1E293B",
    "TOP": "#DBEAFE",
    "TOP_BORDER": "#BFDBFE",
    "TOP_TEXT": "#1E3A8A",
}


# ============================================================
# DATABASE HELPERS
# ============================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_one(query, params=()):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchone()
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def execute(query, params=()):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as error:
        if connection is not None:
            try:
                connection.rollback()
            except Exception:
                pass
        raise error
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def ensure_student_approval_table(connection, cursor):
    cursor.execute(
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


# ============================================================
# FORMAT HELPERS
# ============================================================

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def safe_text(value, fallback="-"):
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


def money(value):
    try:
        amount = Decimal(str(value or 0))
    except (InvalidOperation, TypeError, ValueError):
        amount = Decimal("0.00")
    return f"Rs. {amount:,.2f}"


def format_date(value):
    if value is None:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%d %b %Y")
    if isinstance(value, date):
        return value.strftime("%d %b %Y")
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").strftime("%d %b %Y")
    except Exception:
        return str(value)


def normalize_text(value):
    return str(value or "").strip()


def format_admission_session(value):
    text = normalize_text(value)
    if not text:
        return ""
    if "-" in text:
        return text
    try:
        year = int(text)
        return f"{year}-{str(year + 1)[-2:]}"
    except Exception:
        return text


def load_course_options(existing_value=None):
    rows = fetch_one(
        """
        SELECT COUNT(*) AS Total
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
          AND table_name = 'courses'
        """
    ) or {}

    if int(rows.get("Total") or 0) == 0:
        return [safe_text(existing_value, "")] if existing_value else []

    records = fetch_one(
        """
        SELECT GROUP_CONCAT(DISTINCT Course_Name ORDER BY Course_Name ASC SEPARATOR '||') AS Course_List
        FROM courses
        WHERE Course_Name IS NOT NULL
          AND TRIM(Course_Name) <> ''
        """
    ) or {}

    options = []
    raw = records.get("Course_List")
    if raw:
        options = [item.strip() for item in str(raw).split("||") if item.strip()]

    if existing_value and existing_value not in options:
        options.insert(0, existing_value)

    return options


def load_course_semester_map(existing_course=None):
    records = fetch_one(
        """
        SELECT
            GROUP_CONCAT(
                DISTINCT CONCAT(Course_Name, '||', Total_Semesters)
                ORDER BY Course_Name ASC
                SEPARATOR '##'
            ) AS Course_List
        FROM courses
        WHERE Course_Name IS NOT NULL
          AND TRIM(Course_Name) <> ''
        """
    ) or {}

    course_map = {}
    raw = records.get("Course_List")
    if raw:
        for item in str(raw).split("##"):
            if "||" not in item:
                continue
            course_name, total_semesters = item.split("||", 1)
            course_name = course_name.strip()
            try:
                semester_count = int(str(total_semesters).strip())
            except Exception:
                semester_count = 0
            if course_name:
                course_map[course_name] = max(semester_count, 0)

    if existing_course and existing_course not in course_map:
        existing_row = fetch_one(
            """
            SELECT Course_Name, Total_Semesters
            FROM courses
            WHERE Course_Name = %s
            LIMIT 1
            """,
            (existing_course,)
        ) or {}
        if existing_row.get("Course_Name"):
            try:
                course_map[str(existing_row["Course_Name"]).strip()] = int(existing_row.get("Total_Semesters") or 0)
            except Exception:
                course_map[str(existing_row["Course_Name"]).strip()] = 0

    return course_map


def load_admission_year_options(existing_value=None):
    current_year = date.today().year
    options = [
        f"{year}-{str(year + 1)[-2:]}"
        for year in range(current_year - 10, current_year + 1)
    ]

    if existing_value and existing_value not in options:
        options.insert(0, existing_value)

    return options


def semester_options_for_course(course_name, course_semester_map, existing_value=None):
    course_name = safe_text(course_name, "")
    count = int(course_semester_map.get(course_name) or 0)
    options = [f"Semester {index}" for index in range(1, count + 1)]

    if existing_value:
        existing_text = safe_text(existing_value)
        if existing_text and existing_text not in options:
            options.insert(0, existing_text)

    return options


_ACTIVE_MOUSEWHEEL_HANDLER = None
_ACTIVE_MOUSEWHEEL_ROOT = None


def _dispatch_mousewheel(event):
    if _ACTIVE_MOUSEWHEEL_HANDLER is None:
        return "break"
    return _ACTIVE_MOUSEWHEEL_HANDLER(event)


def _set_mousewheel_handler(root, handler):
    global _ACTIVE_MOUSEWHEEL_HANDLER
    global _ACTIVE_MOUSEWHEEL_ROOT

    _ACTIVE_MOUSEWHEEL_HANDLER = handler
    _ACTIVE_MOUSEWHEEL_ROOT = root

    try:
        root.bind_all("<MouseWheel>", _dispatch_mousewheel)
        root.bind_all("<Button-4>", lambda event: _dispatch_mousewheel(SimpleNamespace(delta=120)))
        root.bind_all("<Button-5>", lambda event: _dispatch_mousewheel(SimpleNamespace(delta=-120)))
    except Exception:
        pass


# ============================================================
# MAIN PROFILE PAGE
# ============================================================

class StudentProfilePage:
    def __init__(
        self,
        parent,
        registration_no,
        student_name="Student",
        login_username="",
        colors=None,
        on_dashboard=None
    ):
        self.parent = parent
        self.registration_no = normalize_text(registration_no)
        self.student_name = normalize_text(student_name) or "Student"
        self.login_username = normalize_text(login_username)
        self.on_dashboard = on_dashboard

        palette = DEFAULT_COLORS.copy()
        if colors:
            palette.update(colors)

        self.BG = palette["BG"]
        self.WHITE = palette["WHITE"]
        self.TEXT = palette["TEXT"]
        self.MUTED = palette["MUTED"]
        self.BLUE = palette["BLUE"]
        self.GREEN = palette["GREEN"]
        self.RED = palette["RED"]
        self.AMBER = palette["AMBER"]
        self.BORDER = palette["BORDER"]
        self.SOFT_BLUE = palette["SOFT_BLUE"]
        self.SOFT_GREEN = palette["SOFT_GREEN"]
        self.SOFT_RED = palette["SOFT_RED"]
        self.SOFT_AMBER = palette["SOFT_AMBER"]
        self.SIDEBAR = palette["SIDEBAR"]
        self.SIDEBAR_HOVER = palette["SIDEBAR_HOVER"]
        self.TOP = palette["TOP"]
        self.TOP_BORDER = palette["TOP_BORDER"]
        self.TOP_TEXT = palette["TOP_TEXT"]

        self.details = {}

        clear_frame(self.parent)
        self.load_profile()
        self.build_ui()

    # --------------------------------------------------------
    # HELPERS
    # --------------------------------------------------------

    def button(self, parent, text, command, bg, fg, active_bg=None, width=16):
        return Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active_bg or bg,
            activeforeground=fg,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=("Helvetica", 9, "bold"),
            padx=14,
            pady=9,
            width=width
        )

    def pill(self, parent, text, bg, fg):
        return Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=("Helvetica", 8, "bold"),
            padx=10,
            pady=5
        )

    def avatar_letter(self):
        source = self.details.get("Name") or self.student_name or "S"
        return str(source).strip()[:1].upper() or "S"

    def load_profile(self):
        row = fetch_one(
            """
            SELECT
                r.Registration_No,
                r.Name,
                r.Username,
                r.Password,
                r.Security_Question,
                r.Security_Answer,
                r.Role,
                sd.Course,
                sd.Semester,
                sd.Admission_Year,
                sd.Email,
                sd.Age,
                sd.Gender,
                sd.Phone,
                sd.Status
            FROM registration r
            LEFT JOIN student_details sd
                ON sd.Registration_No = r.Registration_No
            WHERE r.Registration_No = %s
            LIMIT 1
            """,
            (self.registration_no,)
        ) or {}

        self.details = row
        self.details["Name"] = row.get("Name") or self.student_name

        self.payment_summary = fetch_one(
            """
            SELECT
                COUNT(fp.Payment_ID) AS Payment_Count,
                COALESCE(SUM(fp.Amount), 0) AS Total_Paid,
                MAX(fp.Payment_Date) AS Last_Payment_Date
            FROM fee_payments fp
            INNER JOIN student_fees sf
                ON sf.Student_Fee_ID = fp.Student_Fee_ID
            WHERE sf.Registration_No = %s
            """,
            (self.registration_no,)
        ) or {}

        self.fee_summary = fetch_one(
            """
            SELECT
                COALESCE(SUM(Total_Fee), 0) AS Total_Assigned,
                COALESCE(SUM(Amount_Paid), 0) AS Total_Paid,
                COALESCE(SUM(Due_Amount), 0) AS Total_Due
            FROM student_fees
            WHERE Registration_No = %s
            """,
            (self.registration_no,)
        ) or {}

    def status_color(self):
        status = normalize_text(self.details.get("Status") or "Inactive").lower()
        if status == "active":
            return self.SOFT_GREEN, self.GREEN, "Active"
        if status == "inactive":
            return self.SOFT_AMBER, self.AMBER, "Inactive"
        return self.SOFT_RED, self.RED, safe_text(self.details.get("Status"), "Unknown")

    def profile_stat(self, title, value, subtitle, accent):
        card = Frame(
            self.stats,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        card.grid(
            row=0,
            column=self.stat_index,
            sticky="nsew",
            padx=(0 if self.stat_index == 0 else 8, 0 if self.stat_index == 3 else 8)
        )
        self.stat_index += 1

        Label(
            card,
            text=title,
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Helvetica", 8, "bold")
        ).pack(anchor="w", padx=18, pady=(16, 6))

        Label(
            card,
            text=value,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Helvetica", 17, "bold")
        ).pack(anchor="w", padx=18)

        Label(
            card,
            text=subtitle,
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Helvetica", 8)
        ).pack(anchor="w", padx=18, pady=(6, 14))

        Frame(card, bg=accent, height=3).pack(fill=X, padx=18, pady=(0, 14))

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def build_ui(self):
        outer = Frame(self.parent, bg=self.BG)
        outer.pack(fill=BOTH, expand=True)

        canvas = Canvas(outer, bg=self.BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient=VERTICAL, command=canvas.yview)
        content = Frame(canvas, bg=self.BG)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def fit_body_width(event):
            canvas.itemconfigure(window_id, width=event.width)

        scroll_state = {"target": 0.0, "job": None}

        def current_scroll_pixels():
            bbox = canvas.bbox("all")
            if not bbox:
                return 0.0, 0.0

            content_height = max(1.0, float(bbox[3] - bbox[1]))
            viewport_height = max(1.0, float(canvas.winfo_height()))
            max_scroll = max(0.0, content_height - viewport_height)
            return content_height, max_scroll

        def animate_scroll():
            content_height, max_scroll = current_scroll_pixels()
            target = max(0.0, min(scroll_state["target"], max_scroll))
            current = canvas.yview()[0] * content_height
            delta = target - current

            if abs(delta) < 1.0:
                canvas.yview_moveto(target / content_height)
                scroll_state["job"] = None
                return

            next_position = current + delta * 0.22
            canvas.yview_moveto(next_position / content_height)
            scroll_state["job"] = self.parent.after(10, animate_scroll)

        def scroll_by_delta(delta):
            content_height, max_scroll = current_scroll_pixels()
            if max_scroll <= 0:
                return "break"

            direction = -1 if delta > 0 else 1
            scroll_state["target"] = max(
                0.0,
                min(
                    canvas.yview()[0] * content_height + direction * 120,
                    max_scroll
                )
            )

            if scroll_state["job"] is None:
                animate_scroll()

            return "break"

        def mouse_wheel(event):
            return scroll_by_delta(event.delta)

        content.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", fit_body_width)
        scroll_state["target"] = current_scroll_pixels()[0]
        self.page_mousewheel_handler = mouse_wheel
        _set_mousewheel_handler(self.parent.winfo_toplevel(), mouse_wheel)

        self.build_header(content)
        self.build_summary(content)
        self.build_personal_section(content)
        self.build_academic_section(content)
        self.build_account_section(content)
        self.build_activity_section(content)

    def build_header(self, parent):
        header = Frame(parent, bg=self.BG)
        header.pack(fill=X, padx=28, pady=(24, 16))

        left = Frame(header, bg=self.BG)
        left.pack(side=LEFT, fill=BOTH, expand=True)

        Label(
            left,
            text="My Profile",
            bg=self.BG,
            fg=self.TEXT,
            font=("Helvetica", 22, "bold")
        ).pack(anchor="w")

        Label(
            left,
            text="View your personal and academic information.",
            bg=self.BG,
            fg=self.MUTED,
            font=("Helvetica", 10)
        ).pack(anchor="w", pady=(5, 0))

        right = Frame(header, bg=self.BG)
        right.pack(side=RIGHT)

        avatar = Label(
            right,
            text=self.avatar_letter(),
            bg=self.BLUE,
            fg=self.WHITE,
            font=("Helvetica", 13, "bold"),
            width=3,
            height=2
        )
        avatar.pack(side=LEFT, padx=(0, 12))

        profile_text = Frame(right, bg=self.BG)
        profile_text.pack(side=LEFT)

        Label(
            profile_text,
            text=self.details.get("Name") or self.student_name,
            bg=self.BG,
            fg=self.TEXT,
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w")

        Label(
            profile_text,
            text=f"Registration No: {self.registration_no}",
            bg=self.BG,
            fg=self.MUTED,
            font=("Helvetica", 8)
        ).pack(anchor="w", pady=(3, 0))

        self.button(
            right,
            "Edit Profile",
            self.open_edit_profile,
            self.BLUE,
            self.WHITE,
            active_bg="#1D4ED8",
            width=14
        ).pack(side=RIGHT, padx=(10, 0))

        self.button(
            right,
            "Change Password",
            self.open_change_password,
            self.SIDEBAR,
            self.WHITE,
            active_bg=self.SIDEBAR_HOVER,
            width=16
        ).pack(side=RIGHT, padx=(10, 0))

    def build_summary(self, parent):
        summary = Frame(parent, bg=self.BG)
        summary.pack(fill=X, padx=28, pady=(0, 18))

        for column in range(4):
            summary.grid_columnconfigure(column, weight=1, uniform="profile_stats")

        self.stats = summary
        self.stat_index = 0

        status_bg, status_fg, status_text = self.status_color()
        self.profile_stat(
            "Account Status",
            status_text,
            "Profile verification state",
            self.GREEN if status_text == "Active" else self.AMBER
        )
        self.profile_stat(
            "Payment Count",
            str(int(self.payment_summary.get("Payment_Count") or 0)),
            "Recorded fee payments",
            self.BLUE
        )
        self.profile_stat(
            "Total Paid",
            money(self.payment_summary.get("Total_Paid")),
            "Across all semesters",
            self.GREEN
        )
        self.profile_stat(
            "Due Balance",
            money(self.fee_summary.get("Total_Due")),
            "Outstanding amount",
            self.RED
        )

        badge_row = Frame(parent, bg=self.BG)
        badge_row.pack(fill=X, padx=28, pady=(0, 18))

        card = Frame(
            badge_row,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        card.pack(fill=X)

        inner = Frame(card, bg=self.WHITE)
        inner.pack(fill=X, padx=18, pady=16)

        left = Frame(inner, bg=self.WHITE)
        left.pack(side=LEFT, fill=X, expand=True)

        Label(
            left,
            text=self.details.get("Name") or self.student_name,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Helvetica", 14, "bold")
        ).pack(anchor="w")

        Label(
            left,
            text=f"Username: {safe_text(self.details.get('Username'))}",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Helvetica", 9)
        ).pack(anchor="w", pady=(4, 0))

        right = Frame(inner, bg=self.WHITE)
        right.pack(side=RIGHT)

        self.pill(
            right,
            status_text.upper(),
            status_bg,
            status_fg
        ).pack(anchor="e")

    def build_personal_section(self, parent):
        section = Frame(parent, bg=self.BG)
        section.pack(fill=X, padx=28, pady=(0, 18))

        Label(
            section,
            text="PERSONAL INFORMATION",
            bg=self.BG,
            fg=self.TEXT,
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w", pady=(0, 10))

        card = Frame(section, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(fill=X)

        grid = Frame(card, bg=self.WHITE)
        grid.pack(fill=X, padx=20, pady=18)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        items = [
            ("Full Name", self.details.get("Name") or self.student_name),
            ("Email", safe_text(self.details.get("Email"))),
            ("Phone Number", safe_text(self.details.get("Phone"))),
            ("Gender", safe_text(self.details.get("Gender"))),
            ("Age", safe_text(self.details.get("Age"))),
            ("Status", safe_text(self.details.get("Status"), "Inactive")),
        ]

        for index, (label, value) in enumerate(items):
            column = index % 2
            row = index // 2
            slot = Frame(grid, bg=self.WHITE)
            slot.grid(row=row, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 0), pady=8)

            Label(
                slot,
                text=label,
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 8, "bold")
            ).pack(anchor="w")

            Label(
                slot,
                text=value,
                bg=self.WHITE,
                fg=self.TEXT,
                font=("Helvetica", 10, "bold"),
                wraplength=320,
                justify=LEFT
            ).pack(anchor="w", pady=(4, 0))

    def build_academic_section(self, parent):
        section = Frame(parent, bg=self.BG)
        section.pack(fill=X, padx=28, pady=(0, 18))

        Label(
            section,
            text="ACADEMIC INFORMATION",
            bg=self.BG,
            fg=self.TEXT,
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w", pady=(0, 10))

        card = Frame(section, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(fill=X)

        grid = Frame(card, bg=self.WHITE)
        grid.pack(fill=X, padx=20, pady=18)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        admission = self.details.get("Admission_Year")
        if admission is None or str(admission).strip() == "":
            admission_text = "-"
        else:
            admission_text = str(admission)
            if admission_text.isdigit() and len(admission_text) == 4:
                admission_text = f"{admission_text}-{str(int(admission_text) + 1)[-2:]}"

        semester = self.details.get("Semester")
        semester_text = f"Semester {semester}" if semester not in (None, "") else "-"

        items = [
            ("Course", safe_text(self.details.get("Course"))),
            ("Semester", semester_text),
            ("Admission Year", admission_text),
            ("Registration Number", self.registration_no),
            ("Role", safe_text(self.details.get("Role"), "Student")),
            ("Last Payment", format_date(self.payment_summary.get("Last_Payment_Date"))),
        ]

        for index, (label, value) in enumerate(items):
            column = index % 2
            row = index // 2
            slot = Frame(grid, bg=self.WHITE)
            slot.grid(row=row, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 0), pady=8)

            Label(
                slot,
                text=label,
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 8, "bold")
            ).pack(anchor="w")

            Label(
                slot,
                text=value,
                bg=self.WHITE,
                fg=self.TEXT,
                font=("Helvetica", 10, "bold")
            ).pack(anchor="w", pady=(4, 0))

    def build_account_section(self, parent):
        section = Frame(parent, bg=self.BG)
        section.pack(fill=X, padx=28, pady=(0, 18))

        Label(
            section,
            text="ACCOUNT SECURITY",
            bg=self.BG,
            fg=self.TEXT,
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w", pady=(0, 10))

        card = Frame(section, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(fill=X)

        grid = Frame(card, bg=self.WHITE)
        grid.pack(fill=X, padx=20, pady=18)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        password_mask = "•" * 12
        answer_mask = "•" * max(8, min(len(safe_text(self.details.get("Security_Answer"), "")), 12))

        items = [
            ("Username", safe_text(self.details.get("Username"))),
            ("Security Question", safe_text(self.details.get("Security_Question"))),
            ("Security Answer", answer_mask),
            ("Password", password_mask),
        ]

        for index, (label, value) in enumerate(items):
            column = index % 2
            row = index // 2
            slot = Frame(grid, bg=self.WHITE)
            slot.grid(row=row, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 0), pady=8)

            Label(
                slot,
                text=label,
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 8, "bold")
            ).pack(anchor="w")

            Label(
                slot,
                text=value,
                bg=self.WHITE,
                fg=self.TEXT,
                font=("Helvetica", 10, "bold"),
                wraplength=320,
                justify=LEFT
            ).pack(anchor="w", pady=(4, 0))

    def build_activity_section(self, parent):
        section = Frame(parent, bg=self.BG)
        section.pack(fill=X, padx=28, pady=(0, 28))

        Label(
            section,
            text="PROFILE ACTIVITY",
            bg=self.BG,
            fg=self.TEXT,
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w", pady=(0, 10))

        card = Frame(section, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(fill=X)

        grid = Frame(card, bg=self.WHITE)
        grid.pack(fill=X, padx=20, pady=18)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        items = [
            ("Account Created", "-"),
            ("Last Profile Update", "-"),
            ("Profile Verification", safe_text(self.details.get("Status"), "Inactive")),
            ("Current Status", safe_text(self.details.get("Status"), "Inactive")),
        ]

        for index, (label, value) in enumerate(items):
            column = index % 2
            row = index // 2
            slot = Frame(grid, bg=self.WHITE)
            slot.grid(row=row, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 0), pady=8)

            Label(
                slot,
                text=label,
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 8, "bold")
            ).pack(anchor="w")

            Label(
                slot,
                text=value,
                bg=self.WHITE,
                fg=self.TEXT,
                font=("Helvetica", 10, "bold")
            ).pack(anchor="w", pady=(4, 0))

        credits = Frame(parent, bg=self.BG)
        credits.pack(fill=X, padx=28, pady=(0, 20))

        credit_card = Frame(
            credits,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        credit_card.pack(fill=X)

        Label(
            credit_card,
            text="Developed by Debananda",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w", padx=18, pady=(14, 2))

        Label(
            credit_card,
            text="Mail: debanandakuanr89@gmail.com  |  Website: www.codenextlab.com",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Helvetica", 8)
        ).pack(anchor="w", padx=18, pady=(0, 14))

    # --------------------------------------------------------
    # ACTIONS
    # --------------------------------------------------------

    def open_change_password(self):
        try:
            from COMMON_GUI import change_password
        except Exception:
            change_password = None

        if change_password is None:
            alt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "COMMON GUI")
            if alt_path not in sys.path:
                sys.path.insert(0, alt_path)
            try:
                import change_password
            except Exception as error:
                messagebox.showerror("Module Error", str(error), parent=self.parent)
                return

        change_password.open_change_password(
            parent=self.parent.winfo_toplevel(),
            current_registration_no=self.registration_no
        )

    def open_edit_profile(self):
        window = Toplevel(self.parent.winfo_toplevel())
        window.title("Edit Profile")
        window.configure(bg=self.BG)
        window.resizable(False, False)

        width = 800
        height = 720
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = max(10, int((screen_width - width) / 2))
        y = max(20, int((screen_height - height) / 2) - 20)
        window.geometry(f"{width}x{height}+{x}+{y}")

        try:
            window.transient(self.parent.winfo_toplevel())
            window.grab_set()
        except TclError:
            pass

        def close_window():
            try:
                window.grab_release()
            except TclError:
                pass
            if hasattr(self, "page_mousewheel_handler"):
                _set_mousewheel_handler(self.parent.winfo_toplevel(), self.page_mousewheel_handler)
            window.destroy()

        header = Frame(window, bg=self.BLUE, height=92)
        header.pack(fill=X)
        header.pack_propagate(False)

        Label(
            header,
            text="EDIT PROFILE",
            bg=self.BLUE,
            fg=self.WHITE,
            font=("Helvetica", 20, "bold")
        ).place(x=28, y=22)

        Label(
            header,
            text="Update your personal and academic details.",
            bg=self.BLUE,
            fg="#DBEAFE",
            font=("Helvetica", 9)
        ).place(x=28, y=58)

        body = Frame(window, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        body.pack(fill=BOTH, expand=True, padx=20, pady=(18, 0))

        form_shell = Frame(body, bg=self.WHITE)
        form_shell.pack(fill=BOTH, expand=True)

        canvas = Canvas(form_shell, bg=self.WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_shell, orient=VERTICAL, command=canvas.yview)
        content = Frame(canvas, bg=self.WHITE)
        body_window = canvas.create_window((0, 0), window=content, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=(22, 0), pady=18)
        scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 12), pady=18)

        scroll_state = {"target": 0.0, "job": None}

        def scroll_metrics():
            bbox = canvas.bbox("all")
            if not bbox:
                return 1.0, 0.0
            content_height = max(1.0, float(bbox[3] - bbox[1]))
            viewport_height = max(1.0, float(canvas.winfo_height()))
            max_scroll = max(0.0, content_height - viewport_height)
            return content_height, max_scroll

        def current_scroll_pixels():
            content_height, _ = scroll_metrics()
            return canvas.yview()[0] * content_height

        def animate_scroll():
            content_height, max_scroll = scroll_metrics()
            target = max(0.0, min(scroll_state["target"], max_scroll))
            current = current_scroll_pixels()
            delta = target - current

            if abs(delta) < 1.0:
                canvas.yview_moveto(target / content_height)
                scroll_state["job"] = None
                return

            next_position = current + delta * 0.22
            canvas.yview_moveto(next_position / content_height)
            scroll_state["job"] = window.after(10, animate_scroll)

        def mouse_wheel(event):
            return scroll_by_delta(event.delta)

        def scroll_by_delta(delta):
            content_height, max_scroll = scroll_metrics()
            if max_scroll <= 0:
                return "break"

            direction = -1 if delta > 0 else 1
            scroll_state["target"] = max(
                0.0,
                min(current_scroll_pixels() + direction * 120, max_scroll)
            )
            if scroll_state["job"] is None:
                animate_scroll()
            return "break"

        def refresh_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            scroll_state["target"] = current_scroll_pixels()

        def fit_width(event):
            canvas.itemconfigure(body_window, width=event.width)

        def enable_scroll(event=None):
            scroll_state["target"] = current_scroll_pixels()

        content.bind("<Configure>", refresh_scroll_region)
        canvas.bind("<Configure>", fit_width)
        enable_scroll()
        _set_mousewheel_handler(window, mouse_wheel)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        fields = {
            "Name": StringVar(value=safe_text(self.details.get("Name"), "")),
            "Email": StringVar(value=safe_text(self.details.get("Email"), "")),
            "Phone": StringVar(value=safe_text(self.details.get("Phone"), "")),
            "Age": StringVar(value=safe_text(self.details.get("Age"), "")),
            "Gender": StringVar(value=safe_text(self.details.get("Gender"), "Male")),
            "Course": StringVar(value=safe_text(self.details.get("Course"), "")),
            "Semester": StringVar(value=safe_text(self.details.get("Semester"), "")),
            "Admission_Year": StringVar(value=format_admission_session(self.details.get("Admission_Year"))),
            "Username": StringVar(value=safe_text(self.details.get("Username"), "")),
            "Security_Question": StringVar(value=safe_text(self.details.get("Security_Question"), "")),
            "Security_Answer": StringVar(value=safe_text(self.details.get("Security_Answer"), "")),
        }

        course_semester_map = load_course_semester_map(fields["Course"].get())

        def add_field(row, column, label_text, var, width=28):
            slot = Frame(content, bg=self.WHITE)
            slot.grid(row=row, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 0), pady=8)

            Label(
                slot,
                text=label_text,
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 8, "bold")
            ).pack(anchor="w", pady=(0, 6))

            Entry(
                slot,
                textvariable=var,
                bg=self.WHITE,
                fg=self.TEXT,
                relief=SOLID,
                bd=1,
                highlightthickness=1,
                highlightbackground=self.BORDER,
                highlightcolor=self.BLUE,
                font=("Helvetica", 10),
                width=width
            ).pack(fill=X)

        def add_combo_field(row, column, label_text, var, values, width=28):
            slot = Frame(content, bg=self.WHITE)
            slot.grid(row=row, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 0), pady=8)

            Label(
                slot,
                text=label_text,
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 8, "bold")
            ).pack(anchor="w", pady=(0, 6))

            combo = ttk.Combobox(
                slot,
                textvariable=var,
                state="readonly",
                values=values,
                font=("Helvetica", 10),
                width=width
            )
            combo.pack(fill=X)
            return combo

        add_field(0, 0, "Full Name", fields["Name"])
        add_field(0, 1, "Email", fields["Email"])
        add_field(1, 0, "Phone Number", fields["Phone"])
        add_field(1, 1, "Age", fields["Age"])
        course_options = load_course_options(fields["Course"].get())
        if not course_options:
            course_options = [fields["Course"].get() or ""]
        add_combo_field(2, 0, "Course", fields["Course"], course_options)
        semester_combo = add_combo_field(
            2,
            1,
            "Semester",
            fields["Semester"],
            semester_options_for_course(
                fields["Course"].get(),
                course_semester_map,
                fields["Semester"].get()
            )
        )
        admission_options = load_admission_year_options(fields["Admission_Year"].get())
        if not admission_options:
            admission_options = [fields["Admission_Year"].get() or ""]
        add_combo_field(3, 0, "Admission Year", fields["Admission_Year"], admission_options)
        add_field(3, 1, "Username", fields["Username"])
        security_questions = [
            "What is your favorite color?",
            "What is your father's name?",
            "What is your mother's name?",
            "What is the name of your first school?",
            "What is your pet name?",
            "What is your birth city?",
            "What is your favorite food?",
            "What is your favorite teacher's name?",
            "What is your childhood nickname?",
            "What is your favorite subject?",
        ]
        add_combo_field(4, 0, "Security Question", fields["Security_Question"], security_questions, width=38)
        add_field(4, 1, "Security Answer", fields["Security_Answer"])

        gender_holder = Frame(content, bg=self.WHITE)
        gender_holder.grid(row=5, column=0, columnspan=2, sticky="we", pady=(8, 4))

        Label(
            gender_holder,
            text="Gender",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Helvetica", 8, "bold")
        ).pack(anchor="w", pady=(0, 6))

        gender_combo = ttk.Combobox(
            gender_holder,
            state="readonly",
            values=["Male", "Female", "Other"],
            textvariable=fields["Gender"],
            font=("Helvetica", 10)
        )
        gender_combo.pack(fill=X)

        def refresh_semester_options(*args):
            options = semester_options_for_course(
                fields["Course"].get(),
                course_semester_map,
                fields["Semester"].get()
            )
            semester_combo["values"] = options
            current_value = fields["Semester"].get().strip()
            if current_value not in options and options:
                fields["Semester"].set(options[0])

        fields["Course"].trace_add("write", refresh_semester_options)
        refresh_semester_options()

        notes = Label(
            content,
            text=(
                "Saving changes will set your account status to Inactive "
                "until an administrator reviews the update."
            ),
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Helvetica", 8),
            wraplength=650,
            justify=LEFT
        )
        notes.grid(row=6, column=0, columnspan=2, sticky="w", pady=(14, 18))

        action_bar = Frame(window, bg=self.WHITE, height=72, highlightbackground=self.BORDER, highlightthickness=1)
        action_bar.pack(side=BOTTOM, fill=X)
        action_bar.pack_propagate(False)

        def save_changes():
            name = fields["Name"].get().strip()
            email = fields["Email"].get().strip()
            phone = fields["Phone"].get().strip()
            age = fields["Age"].get().strip()
            gender = fields["Gender"].get().strip()
            course = fields["Course"].get().strip()
            semester = fields["Semester"].get().strip()
            admission_year = fields["Admission_Year"].get().strip()
            username = fields["Username"].get().strip()
            security_question = fields["Security_Question"].get().strip()
            security_answer = fields["Security_Answer"].get().strip()

            if not name:
                messagebox.showwarning("Invalid Name", "Please enter your full name.", parent=window)
                return
            if "@" not in email or "." not in email.split("@")[-1]:
                messagebox.showwarning("Invalid Email", "Please enter a valid email address.", parent=window)
                return
            phone_digits = "".join(ch for ch in phone if ch.isdigit())
            if len(phone_digits) != 10:
                messagebox.showwarning("Invalid Phone", "Phone number must contain 10 digits.", parent=window)
                return
            if not age.isdigit() or not 15 <= int(age) <= 100:
                messagebox.showwarning("Invalid Age", "Age must be between 15 and 100.", parent=window)
                return
            if not course:
                messagebox.showwarning("Invalid Course", "Please select or enter a course.", parent=window)
                return
            semester_digits = "".join(ch for ch in semester if ch.isdigit())
            if not semester_digits:
                messagebox.showwarning("Invalid Semester", "Please enter a valid semester number.", parent=window)
                return
            if not admission_year.strip():
                messagebox.showwarning("Invalid Admission Year", "Please enter an admission year.", parent=window)
                return

            current_snapshot = fetch_one(
                """
                SELECT
                    r.Name,
                    r.Username,
                    r.Password,
                    r.Security_Question,
                    r.Security_Answer,
                    s.Course,
                    s.Semester,
                    s.Admission_Year,
                    s.Email,
                    s.Age,
                    s.Gender,
                    s.Phone,
                    s.Status

                FROM registration r

                LEFT JOIN student_details s
                    ON r.Registration_No = s.Registration_No

                WHERE r.Registration_No = %s

                LIMIT 1
                """,
                (self.registration_no,)
            ) or {}

            try:
                semester_value = int(semester_digits)
                admission_value = admission_year[:4] if len(admission_year) >= 4 else admission_year
                if admission_value.isdigit():
                    admission_value = int(admission_value)

                previous_data = {
                    "Name": safe_text(current_snapshot.get("Name"), ""),
                    "Username": safe_text(current_snapshot.get("Username"), ""),
                    "Password": safe_text(current_snapshot.get("Password"), ""),
                    "Security_Question": safe_text(current_snapshot.get("Security_Question"), ""),
                    "Security_Answer": safe_text(current_snapshot.get("Security_Answer"), ""),
                    "Course": safe_text(current_snapshot.get("Course"), ""),
                    "Semester": safe_text(current_snapshot.get("Semester"), ""),
                    "Admission_Year": safe_text(current_snapshot.get("Admission_Year"), ""),
                    "Email": safe_text(current_snapshot.get("Email"), ""),
                    "Age": safe_text(current_snapshot.get("Age"), ""),
                    "Gender": safe_text(current_snapshot.get("Gender"), ""),
                    "Phone": safe_text(current_snapshot.get("Phone"), ""),
                    "Status": safe_text(current_snapshot.get("Status"), "Inactive"),
                }

                proposed_data = {
                    "Name": name,
                    "Username": username,
                    "Password": safe_text(current_snapshot.get("Password"), ""),
                    "Security_Question": security_question,
                    "Security_Answer": security_answer,
                    "Course": course,
                    "Semester": semester_value,
                    "Admission_Year": admission_value,
                    "Email": email,
                    "Age": int(age),
                    "Gender": gender,
                    "Phone": phone_digits,
                    "Status": "Inactive",
                }

                connection = get_connection()
                cursor = connection.cursor()

                try:
                    connection.start_transaction()

                    ensure_student_approval_table(
                        connection,
                        cursor
                    )

                    cursor.execute(
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
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            'Pending'
                        )
                        """,
                        (
                            self.registration_no,
                            "profile_update",
                            name,
                            username,
                            json.dumps(previous_data, ensure_ascii=True),
                            json.dumps(proposed_data, ensure_ascii=True)
                        )
                    )

                    cursor.execute(
                        """
                        UPDATE student_details
                        SET
                            Status = 'Pending Approval'
                        WHERE Registration_No = %s
                        """,
                        (
                            self.registration_no,
                        )
                    )

                    connection.commit()
                except Exception:
                    connection.rollback()
                    raise
                finally:
                    cursor.close()
                    connection.close()

                messagebox.showinfo(
                    "Profile Updated",
                    "Profile updated successfully.\n\nYour profile has been sent for admin approval.",
                    parent=window
                )

                close_window()
                self.load_profile()
                clear_frame(self.parent)
                self.build_ui()
            except mysql.connector.Error as error:
                messagebox.showerror("Database Error", str(error), parent=window)

        self.button(
            action_bar,
            "Save Changes",
            save_changes,
            self.BLUE,
            self.WHITE,
            active_bg="#1D4ED8",
            width=15
        ).pack(side=RIGHT, padx=(8, 22), pady=14)

        self.button(
            action_bar,
            "Cancel",
            close_window,
            self.RED,
            self.WHITE,
            active_bg="#B91C1C",
            width=12
        ).pack(side=RIGHT, pady=14)

        window.update_idletasks()
        window.lift()
        window.focus_force()

    def refresh(self):
        self.load_profile()
        clear_frame(self.parent)
        self.build_ui()


def show_student_profile(
    parent,
    registration_no,
    student_name="Student",
    login_username="",
    colors=None,
    on_dashboard=None
):
    StudentProfilePage(
        parent=parent,
        registration_no=registration_no,
        student_name=student_name,
        login_username=login_username,
        colors=colors,
        on_dashboard=on_dashboard
    )
