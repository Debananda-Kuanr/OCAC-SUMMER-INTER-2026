from tkinter import *
from tkinter import messagebox
from datetime import datetime
import json
import mysql.connector

from student_form import open_student_form


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
DARK_BLUE = "#1D4ED8"
WHITE = "#FFFFFF"
BACKGROUND = "#F8FAFC"
TEXT_COLOR = "#0F172A"
GRAY = "#64748B"
LIGHT_GRAY = "#94A3B8"
BORDER = "#E2E8F0"
CARD_BG = "#FFFFFF"
SOFT_BLUE = "#EFF6FF"
SOFT_AMBER = "#FFFBEB"
SOFT_GREEN = "#F0FDF4"
SOFT_RED = "#FEF2F2"
GREEN = "#16A34A"
AMBER = "#D97706"
RED = "#DC2626"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="9439",
        database="OCAC_GROUP2"
    )


def ensure_schema(cursor):
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


def safe_text(value, fallback="-"):
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


def format_timestamp(value):
    if value is None:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%d %b %Y, %I:%M %p")
    try:
        return datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return str(value)


def format_admission_session(value):
    text = safe_text(value, "")
    if not text:
        return ""
    if "-" in text:
        return text
    try:
        year = int(text)
        return f"{year}-{str(year + 1)[-2:]}"
    except Exception:
        return text


def parse_blob(value):
    if not value:
        return {}
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


ACCOUNT_FIELDS = (
    "Name",
    "Username",
    "Password",
    "Security_Question",
    "Security_Answer",
)

DETAIL_FIELDS = (
    "Course",
    "Semester",
    "Admission_Year",
    "Email",
    "Age",
    "Gender",
    "Phone",
)


def normalize_request_kind(request_type):
    request_type = safe_text(request_type, "").lower()
    if request_type in ("new_student", "new", "registration"):
        return "new_student"
    return "profile_update"


def load_items():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        ensure_schema(cursor)

        items = []

        cursor.execute(
            """
            SELECT
                Request_ID,
                Registration_No,
                Request_Type,
                Student_Name,
                Username,
                Previous_Data,
                Proposed_Data,
                Status,
                Requested_At

            FROM student_approval_requests

            WHERE LOWER(Status) = 'pending'

            ORDER BY Requested_At DESC, Request_ID DESC
            """
        )

        for row in cursor.fetchall():
            request_kind = normalize_request_kind(row["Request_Type"])
            items.append(
                {
                    "kind": request_kind,
                    "request_type": safe_text(row["Request_Type"], ""),
                    "request_id": row["Request_ID"],
                    "registration_no": safe_text(row["Registration_No"], ""),
                    "name": safe_text(row["Student_Name"], ""),
                    "username": safe_text(row["Username"], ""),
                    "requested_at": row["Requested_At"],
                    "previous_data": parse_blob(row["Previous_Data"]),
                    "proposed_data": parse_blob(row["Proposed_Data"]),
                    "status": safe_text(row["Status"], "Pending"),
                }
            )

        cursor.execute(
            """
            SELECT
                r.Registration_No,
                r.Name,
                r.Username,
                s.Course,
                s.Semester,
                s.Admission_Year,
                s.Email,
                s.Age,
                s.Gender,
                s.Phone,
                COALESCE(s.Status, 'Incomplete') AS Student_Status,
                CASE
                    WHEN s.Registration_No IS NULL THEN 0
                    ELSE 1
                END AS Has_Details

            FROM registration r

            LEFT JOIN student_details s
                ON r.Registration_No = s.Registration_No

            LEFT JOIN student_approval_requests ar
                ON ar.Registration_No = r.Registration_No
               AND LOWER(ar.Status) = 'pending'

            WHERE
                LOWER(TRIM(r.Role)) = 'student'

                AND ar.Request_ID IS NULL

                AND (
                    s.Registration_No IS NULL
                    OR LOWER(COALESCE(s.Status, '')) IN ('inactive', 'incomplete')
                )

                AND LOWER(COALESCE(s.Status, '')) <> 'pending approval'

            ORDER BY r.Name ASC
            """
        )

        for row in cursor.fetchall():
            details = {
                "Course": safe_text(row["Course"], ""),
                "Semester": safe_text(row["Semester"], ""),
                "Admission_Year": safe_text(row["Admission_Year"], ""),
                "Email": safe_text(row["Email"], ""),
                "Age": safe_text(row["Age"], ""),
                "Gender": safe_text(row["Gender"], ""),
                "Phone": safe_text(row["Phone"], ""),
                "Status": safe_text(row["Student_Status"], "Incomplete"),
            }

            items.append(
                {
                    "kind": "new_student",
                    "registration_no": safe_text(row["Registration_No"], ""),
                    "name": safe_text(row["Name"], ""),
                    "username": safe_text(row["Username"], ""),
                    "has_details": bool(row["Has_Details"]),
                    "details": details,
                    "status": safe_text(row["Student_Status"], "Incomplete"),
                }
            )

        return items

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))
        return []

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def show_student_approval_page(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    items_state = {"items": [], "selected": None}

    page = Frame(parent, bg=BACKGROUND)
    page.pack(fill=BOTH, expand=True)

    header = Frame(page, bg=BACKGROUND, height=92)
    header.pack(fill=X)
    header.pack_propagate(False)

    Label(
        header,
        text="Student Requests",
        bg=BACKGROUND,
        fg=TEXT_COLOR,
        font=("Helvetica", 22, "bold")
    ).place(x=28, y=18)

    Label(
        header,
        text="Review student profile updates and new student requests before activating the account.",
        bg=BACKGROUND,
        fg=GRAY,
        font=("Helvetica", 10)
    ).place(x=30, y=52)

    summary = Frame(page, bg=BACKGROUND)
    summary.pack(fill=X, padx=24)

    left_stat = Frame(summary, bg=WHITE, highlightbackground=BORDER, highlightthickness=1, width=240, height=82)
    left_stat.pack(side=LEFT, padx=(0, 14), pady=(0, 14))
    left_stat.pack_propagate(False)
    left_label = Label(left_stat, text="Profile Requests", bg=WHITE, fg=GRAY, font=("Helvetica", 9, "bold"))
    left_label.pack(anchor="w", padx=16, pady=(14, 2))
    left_value = Label(left_stat, text="0", bg=WHITE, fg=TEXT_COLOR, font=("Helvetica", 22, "bold"))
    left_value.pack(anchor="w", padx=16)

    right_stat = Frame(summary, bg=WHITE, highlightbackground=BORDER, highlightthickness=1, width=240, height=82)
    right_stat.pack(side=LEFT, pady=(0, 14))
    right_stat.pack_propagate(False)
    right_label = Label(right_stat, text="New Student Requests", bg=WHITE, fg=GRAY, font=("Helvetica", 9, "bold"))
    right_label.pack(anchor="w", padx=16, pady=(14, 2))
    right_value = Label(right_stat, text="0", bg=WHITE, fg=TEXT_COLOR, font=("Helvetica", 22, "bold"))
    right_value.pack(anchor="w", padx=16)

    body = Frame(page, bg=BACKGROUND)
    body.pack(fill=BOTH, expand=True, padx=24, pady=(0, 20))

    list_frame = Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1, width=360)
    list_frame.pack(side=LEFT, fill=Y, padx=(0, 14))
    list_frame.pack_propagate(False)

    detail_frame = Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
    detail_frame.pack(side=LEFT, fill=BOTH, expand=True)

    list_header = Frame(list_frame, bg=WHITE, height=70)
    list_header.pack(fill=X)
    list_header.pack_propagate(False)

    Label(
        list_header,
        text="Requests",
        bg=WHITE,
        fg=TEXT_COLOR,
        font=("Helvetica", 16, "bold")
    ).place(x=18, y=16)

    Label(
        list_header,
        text="Select a request to inspect details.",
        bg=WHITE,
        fg=GRAY,
        font=("Helvetica", 9)
    ).place(x=18, y=42)

    list_canvas = Canvas(list_frame, bg=WHITE, bd=0, highlightthickness=0)
    list_scroll = Scrollbar(list_frame, orient=VERTICAL, command=list_canvas.yview)
    list_inner = Frame(list_canvas, bg=WHITE)
    list_inner_id = list_canvas.create_window((0, 0), window=list_inner, anchor="nw")
    list_canvas.configure(yscrollcommand=list_scroll.set)
    list_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=(12, 0), pady=(0, 12))
    list_scroll.pack(side=RIGHT, fill=Y, pady=(0, 12))

    def update_list_scrollregion(event=None):
        list_canvas.configure(scrollregion=list_canvas.bbox("all"))

    def fit_list_width(event):
        list_canvas.itemconfigure(list_inner_id, width=event.width)

    def on_list_mousewheel(event):
        if list_canvas.winfo_exists():
            list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    list_inner.bind("<Configure>", update_list_scrollregion)
    list_canvas.bind("<Configure>", fit_list_width)
    list_canvas.bind("<Enter>", lambda event: list_canvas.bind_all("<MouseWheel>", on_list_mousewheel))
    list_canvas.bind("<Leave>", lambda event: list_canvas.unbind_all("<MouseWheel>"))

    detail_title = Label(detail_frame, text="Approval Details", bg=WHITE, fg=TEXT_COLOR, font=("Helvetica", 18, "bold"))
    detail_title.place(x=20, y=18)

    detail_subtitle = Label(detail_frame, text="No request selected.", bg=WHITE, fg=GRAY, font=("Helvetica", 10))
    detail_subtitle.place(x=20, y=48)

    detail_body = Frame(detail_frame, bg=WHITE)
    detail_body.place(x=20, y=85, relwidth=1.0, width=-40, relheight=1.0, height=-170)

    action_bar = Frame(detail_frame, bg=WHITE, height=70)
    action_bar.pack(side=BOTTOM, fill=X)
    action_bar.pack_propagate(False)

    refresh_button = Button(
        action_bar,
        text="Refresh",
        bg="#F1F5F9",
        fg=TEXT_COLOR,
        activebackground="#E2E8F0",
        activeforeground=TEXT_COLOR,
        font=("Helvetica", 10, "bold"),
        bd=0,
        cursor="hand2"
    )
    refresh_button.pack(side=RIGHT, padx=(8, 20), pady=14, ipadx=18, ipady=8)

    def open_selected_student():
        item = items_state["selected"]
        if not item:
            return
        open_student_form(
            parent,
            refresh_callback=lambda: show_student_approval_page(parent),
            student_id=item["registration_no"],
            mode="edit"
        )

    def draw_field(container, label_text, value_text, accent=TEXT_COLOR):
        field = Frame(container, bg=SOFT_BLUE if accent == BLUE else WHITE)
        field.pack(fill=X, pady=4)
        Label(field, text=label_text, bg=field["bg"], fg=GRAY, font=("Helvetica", 9, "bold")).pack(anchor="w")
        Label(
            field,
            text=value_text,
            bg=field["bg"],
            fg=accent,
            font=("Helvetica", 10, "bold"),
            wraplength=290,
            justify=LEFT,
            anchor="w"
            ).pack(anchor="w", pady=(2, 0))

    def create_detail_scroll_area():
        for widget in detail_body.winfo_children():
            widget.destroy()

        canvas = Canvas(detail_body, bg=WHITE, bd=0, highlightthickness=0)
        scrollbar = Scrollbar(detail_body, orient=VERTICAL, command=canvas.yview)
        inner = Frame(canvas, bg=WHITE)
        inner_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        def update_scrollregion(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def fit_width(event):
            canvas.itemconfigure(inner_window, width=event.width)

        def on_mousewheel(event):
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        inner.bind("<Configure>", update_scrollregion)
        canvas.bind("<Configure>", fit_width)
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        return canvas, inner, scrollbar

    def render_empty_state():
        for widget in detail_body.winfo_children():
            widget.destroy()

        Frame(detail_body, bg=SOFT_GREEN, highlightbackground="#BBF7D0", highlightthickness=1, height=120).pack(fill=X, pady=(0, 14))
        message = Label(
            detail_body,
            text="No pending approvals at the moment.",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 13, "bold")
        )
        message.pack(anchor="w", pady=(20, 6))
        Label(
            detail_body,
            text="Student profile updates and inactive new student records will appear here for review.",
            bg=WHITE,
            fg=GRAY,
            font=("Helvetica", 10),
            wraplength=620,
            justify=LEFT
        ).pack(anchor="w")

        approve_button.config(state=DISABLED)
        open_button.config(state=DISABLED)

    def render_profile_request(item):
        canvas, scroll_inner, scrollbar = create_detail_scroll_area()

        detail_subtitle.config(text=f"Profile update request for {item['name']} ({item['registration_no']})")

        top = Frame(scroll_inner, bg=SOFT_AMBER, highlightbackground="#FDE68A", highlightthickness=1)
        top.pack(fill=X, pady=(0, 14))
        Label(top, text="Pending Profile Change", bg=SOFT_AMBER, fg=AMBER, font=("Helvetica", 10, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
        Label(
            top,
            text=f"Submitted for {item['registration_no']} and waiting for admin approval.",
            bg=SOFT_AMBER,
            fg=TEXT_COLOR,
            font=("Helvetica", 10),
            wraplength=620,
            justify=LEFT
            ).pack(anchor="w", padx=14, pady=(0, 12))

        timestamp_row = Frame(scroll_inner, bg=WHITE)
        timestamp_row.pack(fill=X, pady=(0, 12))
        Label(
            timestamp_row,
            text="Requested At",
            bg=WHITE,
            fg=GRAY,
            font=("Helvetica", 9, "bold")
        ).pack(anchor="w")
        Label(
            timestamp_row,
            text=format_timestamp(item.get("requested_at")),
            bg=WHITE,
            fg=TEXT_COLOR,
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w", pady=(2, 0))

        compare = Frame(scroll_inner, bg=WHITE)
        compare.pack(fill=BOTH, expand=True)

        prev_panel = Frame(compare, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        prev_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        new_panel = Frame(compare, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        new_panel.pack(side=LEFT, fill=BOTH, expand=True)

        Label(prev_panel, text="Current Values", bg=WHITE, fg=TEXT_COLOR, font=("Helvetica", 12, "bold")).pack(anchor="w", padx=14, pady=(12, 8))
        Label(new_panel, text="Proposed Values", bg=WHITE, fg=TEXT_COLOR, font=("Helvetica", 12, "bold")).pack(anchor="w", padx=14, pady=(12, 8))

        fields = [
            ("Name", "Name"),
            ("Username", "Username"),
            ("Password", "Password"),
            ("Security Question", "Security_Question"),
            ("Security Answer", "Security_Answer"),
            ("Course", "Course"),
            ("Semester", "Semester"),
            ("Academic Year", "Admission_Year"),
            ("Email", "Email"),
            ("Age", "Age"),
            ("Gender", "Gender"),
            ("Phone", "Phone"),
        ]

        previous_data = item.get("previous_data", {})
        proposed_data = item.get("proposed_data", {})

        changed_fields = []

        for label_text, key in fields:
            if key == "Admission_Year":
                previous_value = format_admission_session(previous_data.get(key))
                proposed_value = format_admission_session(proposed_data.get(key))
            else:
                previous_value = safe_text(previous_data.get(key), "-")
                proposed_value = safe_text(proposed_data.get(key), "-")

            if previous_value != proposed_value:
                changed_fields.append((label_text, key, previous_value, proposed_value))

        if not changed_fields:
            Label(
                compare,
                text="No field-level differences were detected in this request.",
                bg=WHITE,
                fg=GRAY,
                font=("Helvetica", 10),
                wraplength=620,
                justify=LEFT
            ).pack(anchor="w", padx=4, pady=14)
        else:
            for label_text, _, previous_value, proposed_value in changed_fields:
                draw_field(prev_panel, label_text, previous_value)
                draw_field(new_panel, label_text, proposed_value, BLUE)

        approve_button.config(state=NORMAL)
        open_button.config(state=NORMAL)

        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def render_new_student(item):
        for widget in detail_body.winfo_children():
            widget.destroy()

        details = item.get("details", {})
        has_details = item.get("has_details", False)

        detail_subtitle.config(
            text=f"New student record for {item['name']} ({item['registration_no']})"
        )

        top = Frame(detail_body, bg=SOFT_GREEN, highlightbackground="#BBF7D0", highlightthickness=1)
        top.pack(fill=X, pady=(0, 14))
        Label(top, text="New Student", bg=SOFT_GREEN, fg=GREEN, font=("Helvetica", 10, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
        if has_details:
            notice = "Student details exist but the account is not active yet."
        else:
            notice = "Registration exists, but student details are not completed yet."
        Label(
            top,
            text=notice,
            bg=SOFT_GREEN,
            fg=TEXT_COLOR,
            font=("Helvetica", 10),
            wraplength=620,
            justify=LEFT
        ).pack(anchor="w", padx=14, pady=(0, 12))

        info = Frame(detail_body, bg=WHITE)
        info.pack(fill=BOTH, expand=True)

        left = Frame(info, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        right = Frame(info, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side=LEFT, fill=BOTH, expand=True)

        Label(left, text="Registration Info", bg=WHITE, fg=TEXT_COLOR, font=("Helvetica", 12, "bold")).pack(anchor="w", padx=14, pady=(12, 8))
        Label(right, text="Current Student Status", bg=WHITE, fg=TEXT_COLOR, font=("Helvetica", 12, "bold")).pack(anchor="w", padx=14, pady=(12, 8))

        draw_field(left, "Registration No", item["registration_no"])
        draw_field(left, "Name", item["name"])
        draw_field(left, "Username", item["username"])

        draw_field(right, "Course", safe_text(details.get("Course"), "-"))
        draw_field(right, "Semester", safe_text(details.get("Semester"), "-"))
        draw_field(right, "Admission Year", safe_text(details.get("Admission_Year"), "-"))
        draw_field(right, "Email", safe_text(details.get("Email"), "-"))
        draw_field(right, "Age", safe_text(details.get("Age"), "-"))
        draw_field(right, "Gender", safe_text(details.get("Gender"), "-"))
        draw_field(right, "Phone", safe_text(details.get("Phone"), "-"))
        draw_field(right, "Status", safe_text(details.get("Status"), "Incomplete"), BLUE if has_details else AMBER)

        approve_button.config(state=NORMAL if has_details else DISABLED)
        open_button.config(state=NORMAL)

    def render_detail(item):
        items_state["selected"] = item
        if item["kind"] == "profile_update":
            render_profile_request(item)
        else:
            render_new_student(item)

    def approve_selected():
        item = items_state["selected"]
        if not item:
            return

        if item["kind"] == "new_student" and not item.get("has_details"):
            messagebox.showwarning(
                "Profile Incomplete",
                "This student does not have a completed profile yet. Open Student Form to fill the details before approval.",
            )
            return

        confirm = messagebox.askyesno(
            "Approve Student",
            f"Approve the selected student record for {item['registration_no']}?"
        )
        if not confirm:
            return

        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            ensure_schema(cursor)
            connection.start_transaction()

            if item["kind"] == "profile_update":
                proposed = item.get("proposed_data", {})
                account_updates = [
                    (field, proposed[field])
                    for field in ACCOUNT_FIELDS
                    if field in proposed
                ]

                if account_updates:
                    set_clause = ", ".join(f"{field} = %s" for field, _ in account_updates)
                    values = [value for _, value in account_updates]
                    values.append(item["registration_no"])
                    cursor.execute(
                        f"""
                        UPDATE registration
                        SET {set_clause}
                        WHERE Registration_No = %s
                        """,
                        tuple(values)
                    )

                cursor.execute(
                    """
                    SELECT Registration_No
                    FROM student_details
                    WHERE Registration_No = %s
                    LIMIT 1
                    """,
                    (item["registration_no"],)
                )
                exists = cursor.fetchone()

                detail_updates = [
                    (field, proposed[field])
                    for field in DETAIL_FIELDS
                    if field in proposed
                ]

                if exists:
                    if detail_updates:
                        set_clause = ", ".join(f"{field} = %s" for field, _ in detail_updates)
                        values = [value for _, value in detail_updates]
                        values.extend(["Active", item["registration_no"]])
                        cursor.execute(
                            f"""
                            UPDATE student_details
                            SET {set_clause},
                                Status = %s
                            WHERE Registration_No = %s
                            """,
                            tuple(values)
                        )
                    else:
                        cursor.execute(
                            """
                            UPDATE student_details
                            SET Status = 'Active'
                            WHERE Registration_No = %s
                            """,
                            (item["registration_no"],)
                        )
                elif detail_updates:
                    insert_fields = ["Registration_No"] + [field for field, _ in detail_updates] + ["Status"]
                    placeholders = ", ".join(["%s"] * len(insert_fields))
                    values = [item["registration_no"]] + [value for _, value in detail_updates] + ["Active"]
                    cursor.execute(
                        f"""
                        INSERT INTO student_details
                        ({", ".join(insert_fields)})
                        VALUES
                        ({placeholders})
                        """,
                        tuple(values)
                    )

                cursor.execute(
                    """
                    UPDATE student_approval_requests
                    SET
                        Status = 'Approved',
                        Reviewed_At = NOW(),
                        Reviewed_By = %s
                    WHERE Request_ID = %s
                    """,
                    ("Admin", item["request_id"])
                )

            else:
                proposed = item.get("proposed_data", {})
                detail_updates = [
                    (field, proposed[field])
                    for field in DETAIL_FIELDS
                    if field in proposed
                ]

                cursor.execute(
                    """
                    SELECT Registration_No
                    FROM student_details
                    WHERE Registration_No = %s
                    LIMIT 1
                    """,
                    (item["registration_no"],)
                )
                exists = cursor.fetchone()

                if exists:
                    if detail_updates:
                        set_clause = ", ".join(f"{field} = %s" for field, _ in detail_updates)
                        values = [value for _, value in detail_updates]
                        values.extend(["Active", item["registration_no"]])
                        cursor.execute(
                            f"""
                            UPDATE student_details
                            SET {set_clause},
                                Status = %s
                            WHERE Registration_No = %s
                            """,
                            tuple(values)
                        )
                    else:
                        cursor.execute(
                            """
                            UPDATE student_details
                            SET Status = 'Active'
                            WHERE Registration_No = %s
                            """,
                            (item["registration_no"],)
                        )
                elif detail_updates:
                    insert_fields = ["Registration_No"] + [field for field, _ in detail_updates] + ["Status"]
                    placeholders = ", ".join(["%s"] * len(insert_fields))
                    values = [item["registration_no"]] + [value for _, value in detail_updates] + ["Active"]
                    cursor.execute(
                        f"""
                        INSERT INTO student_details
                        ({", ".join(insert_fields)})
                        VALUES
                        ({placeholders})
                        """,
                        tuple(values)
                    )

            connection.commit()
            messagebox.showinfo(
                "Approved",
                f"Student record approved for {item['registration_no']}."
            )
            show_student_approval_page(parent)

        except mysql.connector.Error as error:
            if connection is not None:
                try:
                    connection.rollback()
                except Exception:
                    pass
            messagebox.showerror("Database Error", str(error))

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

    def refresh_page():
        show_student_approval_page(parent)

    def render_cards():
        for widget in list_inner.winfo_children():
            widget.destroy()

        items = load_items()
        items_state["items"] = items

        profile_count = sum(1 for item in items if item["kind"] == "profile_update")
        new_count = sum(1 for item in items if item["kind"] == "new_student")

        left_value.config(text=str(profile_count))
        right_value.config(text=str(new_count))

        if not items:
            render_empty_state()
            return

        first_item = items[0]
        items_state["selected"] = first_item

        for index, item in enumerate(items):
            card_bg = SOFT_BLUE if item["kind"] == "profile_update" else SOFT_GREEN
            border_color = "#BFDBFE" if item["kind"] == "profile_update" else "#BBF7D0"
            card = Frame(list_inner, bg=card_bg, highlightbackground=border_color, highlightthickness=1)
            card.pack(fill=X, padx=6, pady=(0, 10))

            kind_text = "Profile Change" if item["kind"] == "profile_update" else "New Student"
            status_text = "Pending" if item["kind"] == "profile_update" else safe_text(item.get("status"), "Incomplete")

            Label(card, text=kind_text, bg=card_bg, fg=BLUE if item["kind"] == "profile_update" else GREEN, font=("Helvetica", 9, "bold")).pack(anchor="w", padx=12, pady=(10, 2))
            Label(card, text=item["name"], bg=card_bg, fg=TEXT_COLOR, font=("Helvetica", 11, "bold"), wraplength=300, justify=LEFT).pack(anchor="w", padx=12)
            Label(card, text=item["registration_no"], bg=card_bg, fg=GRAY, font=("Helvetica", 9)).pack(anchor="w", padx=12, pady=(2, 0))
            Label(card, text=status_text, bg=card_bg, fg=AMBER if item["kind"] == "profile_update" else GREEN, font=("Helvetica", 9, "bold")).pack(anchor="w", padx=12, pady=(2, 10))

            def make_select_handler(selected_item):
                return lambda event=None: render_detail(selected_item)

            card.bind("<Button-1>", make_select_handler(item))
            for child in card.winfo_children():
                child.bind("<Button-1>", make_select_handler(item))

        render_detail(first_item)

        list_inner.update_idletasks()
        list_canvas.configure(scrollregion=list_canvas.bbox("all"))

    approve_button = Button(
        action_bar,
        text="Approve Selected",
        bg=BLUE,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        font=("Helvetica", 10, "bold"),
        bd=0,
        cursor="hand2",
        command=approve_selected
    )
    approve_button.pack(side=RIGHT, padx=(0, 8), pady=14, ipadx=20, ipady=8)

    open_button = Button(
        action_bar,
        text="Open Student Form",
        bg="#F1F5F9",
        fg=TEXT_COLOR,
        activebackground="#E2E8F0",
        activeforeground=TEXT_COLOR,
        font=("Helvetica", 10, "bold"),
        bd=0,
        cursor="hand2",
        command=open_selected_student
    )
    open_button.pack(side=RIGHT, padx=(0, 8), pady=14, ipadx=16, ipady=8)

    refresh_button.config(command=refresh_page)

    render_cards()
