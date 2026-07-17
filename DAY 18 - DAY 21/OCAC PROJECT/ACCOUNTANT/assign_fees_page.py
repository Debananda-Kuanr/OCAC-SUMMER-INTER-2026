# ============================================================
# assign_fees_page.py
# Accountant Panel - Assign / View / Delete Student Fees
#
# Exact database model used:
#   registration
#   student_details
#   courses
#   fee_structures
#   fee_structure_components
#   student_fees
#   fee_payments
#
# IMPORTANT:
#   - There is NO "students" table in this file.
#   - Opens inside accountant dashboard's content frame.
#   - One student may have multiple semester fee assignments.
#   - Previous semester dues remain unchanged.
#   - Same Fee_Structure_ID cannot be assigned twice to the
#     same Registration_No.
#   - Delete is allowed only when no payment history exists
#     and Amount_Paid is 0.
# ============================================================

from tkinter import *
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation
import mysql.connector


# ============================================================
# DATABASE CONFIGURATION
# Change password only if your MySQL password is different.
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "9439",
    "database": "OCAC_GROUP2"
}


# ============================================================
# COLORS
# ============================================================

BG = "#F8FAFC"
WHITE = "#FFFFFF"
TEXT = "#0F172A"
TEXT_2 = "#334155"
GRAY = "#64748B"
LIGHT_GRAY = "#F1F5F9"
BORDER = "#E2E8F0"
BORDER_DARK = "#CBD5E1"

BLUE = "#2563EB"
DARK_BLUE = "#1D4ED8"
LIGHT_BLUE = "#EFF6FF"

GREEN = "#16A34A"
DARK_GREEN = "#15803D"
LIGHT_GREEN = "#F0FDF4"

RED = "#DC2626"
DARK_RED = "#B91C1C"
LIGHT_RED = "#FEF2F2"

ORANGE = "#EA580C"
LIGHT_ORANGE = "#FFF7ED"

PURPLE = "#7C3AED"
LIGHT_PURPLE = "#F5F3FF"

FONT = "Helvetica"


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# HELPERS
# ============================================================

def decimal_value(value):
    try:
        return Decimal(str(value if value is not None else 0))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal("0.00")


def money(value):
    return "₹" + format(decimal_value(value), ",.2f")


def clear_widgets(parent):
    for widget in parent.winfo_children():
        widget.destroy()


def center_message_parent(parent):
    try:
        return parent.winfo_toplevel()
    except Exception:
        return parent


# ============================================================
# MAIN PAGE
# ============================================================

class AssignFeesPage:

    def __init__(
        self,
        parent,
        user_role="Accountant",
        current_user_name="",
        current_user_id=""
    ):
        self.parent = parent
        self.user_role = user_role or "Accountant"
        self.current_user_name = current_user_name or "Accountant"
        self.current_user_id = current_user_id or ""

        self.selected_student = None
        self.selected_fee_structure = None
        self.selected_components = []

        self.student_map = {}
        self.assigned_fee_map = {}
        self.structure_map = {}

        self.search_var = StringVar()
        self.student_count_var = StringVar(value="0 Students")

        self.configure_styles()

        # Dashboard already clears content, but this also makes the
        # module safe if called directly.
        clear_widgets(self.parent)

        self.page = Frame(self.parent, bg=BG)
        self.page.pack(fill=BOTH, expand=True)

        self.show_assign_mode()


    # ========================================================
    # STYLE
    # ========================================================

    def configure_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Assign.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            borderwidth=0,
            relief=FLAT,
            rowheight=42,
            font=(FONT, 10)
        )

        style.configure(
            "Assign.Treeview.Heading",
            background=LIGHT_GRAY,
            foreground=TEXT_2,
            borderwidth=0,
            relief=FLAT,
            padding=(10, 10),
            font=(FONT, 9, "bold")
        )

        style.map(
            "Assign.Treeview",
            background=[("selected", LIGHT_BLUE)],
            foreground=[("selected", TEXT)]
        )


    # ========================================================
    # PAGE HELPERS
    # ========================================================

    def clear_page(self):
        clear_widgets(self.page)


    def accountant_text(self):
        if self.current_user_id:
            return f"{self.current_user_name} - {self.current_user_id}"
        return self.current_user_name


    def make_button(
        self,
        parent,
        text,
        command,
        kind="primary",
        width=18
    ):
        palettes = {
            "primary": ("#2563EB", WHITE, "#1D4ED8"),
            "success": ("#16A34A", WHITE, "#15803D"),
            "danger": ("#DC2626", WHITE, "#B91C1C"),
            "warning": ("#F59E0B", WHITE, "#D97706"),
            "secondary": ("#475569", WHITE, "#334155")
        }

        bg, fg, active_bg = palettes.get(
            kind,
            palettes["secondary"]
        )

        return Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=WHITE,
            disabledforeground="#CBD5E1",
            bd=0,
            relief=FLAT,
            cursor="hand2",
            width=width,
            pady=10,
            font=(FONT, 9, "bold")
        )

    def page_header(
        self,
        title,
        subtitle,
        step,
        back_command=None,
        show_progress=True
    ):
        header = Frame(self.page, bg=WHITE, height=92)
        header.pack(fill=X)
        header.pack_propagate(False)

        left = Frame(header, bg=WHITE)
        left.pack(side=LEFT, fill=BOTH, expand=True, padx=28)

        if back_command:
            Button(
                left,
                text="←  BACK",
                command=back_command,
                bg=WHITE,
                fg=BLUE,
                activebackground=WHITE,
                activeforeground=DARK_BLUE,
                bd=0,
                relief=FLAT,
                cursor="hand2",
                font=(FONT, 8, "bold")
            ).pack(anchor=W, pady=(10, 2))

            title_pad = 0
        else:
            title_pad = 18

        Label(
            left,
            text=title,
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 20, "bold")
        ).pack(anchor=W, pady=(title_pad, 0))

        Label(
            left,
            text=subtitle,
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 9)
        ).pack(anchor=W, pady=(4, 0))

        right = Frame(header, bg=WHITE)
        right.pack(side=RIGHT, padx=28)

        Label(
            right,
            text=f"STEP {step} OF 4",
            bg=LIGHT_BLUE,
            fg=BLUE,
            padx=14,
            pady=7,
            font=(FONT, 8, "bold")
        ).pack(pady=25)

        if show_progress:
            self.progress(step)


    def progress(self, active_step):
        progress = Frame(self.page, bg=BG)
        progress.pack(fill=X, padx=28, pady=(14, 14))

        names = [
            "Select Student",
            "Assigned Fees",
            "Fee Structure",
            "Review"
        ]

        for index, name in enumerate(names, start=1):
            item = Frame(progress, bg=BG)
            item.pack(side=LEFT, fill=X, expand=True)

            active = index <= active_step

            Label(
                item,
                text=str(index),
                bg=BLUE if active else WHITE,
                fg=WHITE if active else GRAY,
                width=3,
                pady=5,
                highlightbackground=BLUE if active else BORDER_DARK,
                highlightthickness=1,
                font=(FONT, 8, "bold")
            ).pack(side=LEFT)

            Label(
                item,
                text=name,
                bg=BG,
                fg=TEXT if active else GRAY,
                font=(FONT, 8, "bold" if active else "normal")
            ).pack(side=LEFT, padx=(7, 8))

            if index < 4:
                Frame(
                    item,
                    bg=BLUE if index < active_step else BORDER,
                    height=2
                ).pack(
                    side=LEFT,
                    fill=X,
                    expand=True,
                    padx=(0, 8)
                )


    # ========================================================
    # SCREEN 1 - SELECT STUDENT
    # ========================================================

    def show_select_student(self):
        self.clear_page()

        self.selected_student = None
        self.selected_fee_structure = None
        self.selected_components = []
        self.student_map.clear()

        self.page_header(
            "Assign Fees",
            "Search and select a student to manage semester-wise fee assignments.",
            1,
            self.show_assign_mode,
            show_progress=False
        )

        card = Frame(
            self.page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill=BOTH, expand=True, padx=28, pady=(0, 24))

        top = Frame(card, bg=WHITE)
        top.pack(fill=X, padx=22, pady=(18, 12))

        Label(
            top,
            text="SELECT STUDENT",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 12, "bold")
        ).pack(side=LEFT)

        Label(
            top,
            textvariable=self.student_count_var,
            bg=LIGHT_BLUE,
            fg=BLUE,
            padx=12,
            pady=5,
            font=(FONT, 8, "bold")
        ).pack(side=RIGHT)

        search_row = Frame(card, bg=WHITE)
        search_row.pack(fill=X, padx=22, pady=(0, 14))

        self.search_entry = Entry(
            search_row,
            textvariable=self.search_var,
            bg=WHITE,
            fg=TEXT,
            relief=SOLID,
            bd=1,
            font=(FONT, 10)
        )
        self.search_entry.pack(side=LEFT, fill=X, expand=True, ipady=10)

        self.search_entry.bind(
            "<Return>",
            lambda event: self.load_students()
        )

        self.make_button(
            search_row,
            "SEARCH",
            self.load_students,
            "primary",
            13
        ).pack(side=LEFT, padx=(10, 0))

        self.make_button(
            search_row,
            "CLEAR",
            self.clear_student_search,
            "secondary",
            10
        ).pack(side=LEFT, padx=(8, 0))

        table_holder = Frame(card, bg=WHITE)
        table_holder.pack(fill=BOTH, expand=True, padx=22, pady=(0, 14))

        columns = (
            "registration",
            "name",
            "course",
            "semester",
            "admission_year",
            "status"
        )

        self.student_tree = ttk.Treeview(
            table_holder,
            columns=columns,
            show="headings",
            style="Assign.Treeview"
        )

        headings = {
            "registration": "REGISTRATION NO.",
            "name": "STUDENT NAME",
            "course": "COURSE",
            "semester": "CURRENT SEMESTER",
            "admission_year": "ADMISSION YEAR",
            "status": "PROFILE STATUS"
        }

        widths = {
            "registration": 150,
            "name": 210,
            "course": 230,
            "semester": 130,
            "admission_year": 130,
            "status": 120
        }

        for col in columns:
            self.student_tree.heading(col, text=headings[col])
            self.student_tree.column(
                col,
                width=widths[col],
                anchor=W if col in ("registration", "name", "course") else CENTER
            )

        y_scroll = Scrollbar(
            table_holder,
            orient=VERTICAL,
            command=self.student_tree.yview
        )

        self.student_tree.configure(yscrollcommand=y_scroll.set)

        self.student_tree.pack(side=LEFT, fill=BOTH, expand=True)
        y_scroll.pack(side=RIGHT, fill=Y)

        self.student_tree.bind(
            "<Double-1>",
            lambda event: self.select_student_and_continue()
        )

        footer = Frame(card, bg=WHITE)
        footer.pack(fill=X, padx=22, pady=(0, 18))

        Label(
            footer,
            text="Select one student. Existing semester fees will be shown on the next screen.",
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8)
        ).pack(side=LEFT)

        self.make_button(
            footer,
            "CONTINUE  →",
            self.select_student_and_continue,
            "primary",
            18
        ).pack(side=RIGHT)

        self.load_students()


    def clear_student_search(self):
        self.search_var.set("")
        self.load_students()


    def load_students(self):
        self.student_map.clear()

        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        keyword = self.search_var.get().strip()

        sql = """
            SELECT
                r.Registration_No,
                r.Name,
                sd.Course,
                sd.Semester,
                sd.Admission_Year,
                sd.Email,
                sd.Phone,
                sd.Status
            FROM registration AS r
            INNER JOIN student_details AS sd
                ON r.Registration_No = sd.Registration_No
            WHERE LOWER(TRIM(r.Role)) = 'student'
        """

        params = []

        if keyword:
            sql += """
                AND (
                    r.Registration_No LIKE %s
                    OR r.Name LIKE %s
                    OR sd.Course LIKE %s
                    OR CAST(sd.Semester AS CHAR) LIKE %s
                )
            """

            like = f"%{keyword}%"
            params.extend([like, like, like, like])

        sql += """
            ORDER BY
                r.Name ASC,
                r.Registration_No ASC
        """

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()

            for row in rows:
                item_id = self.student_tree.insert(
                    "",
                    END,
                    values=(
                        row["Registration_No"],
                        row["Name"],
                        row["Course"] or "-",
                        f"Semester {row['Semester']}" if row["Semester"] else "-",
                        row["Admission_Year"] or "-",
                        row["Status"] or "-"
                    )
                )

                self.student_map[item_id] = {
                    "Registration_No": str(row["Registration_No"]),
                    "Name": str(row["Name"]),
                    "Course": str(row["Course"] or ""),
                    "Semester": int(row["Semester"] or 0),
                    "Admission_Year": str(row["Admission_Year"] or ""),
                    "Email": str(row["Email"] or ""),
                    "Phone": str(row["Phone"] or ""),
                    "Status": str(row["Status"] or "")
                }

            count = len(rows)
            self.student_count_var.set(
                f"{count} Student" if count == 1 else f"{count} Students"
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Student Load Error",
                (
                    "Unable to load students from registration and student_details.\n\n"
                    f"{error}"
                ),
                parent=center_message_parent(self.parent)
            )

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()


    def select_student_and_continue(self):
        selection = self.student_tree.selection()

        if not selection:
            messagebox.showwarning(
                "Select Student",
                "Please select one student first.",
                parent=center_message_parent(self.parent)
            )
            return

        self.selected_student = self.student_map.get(selection[0])

        if self.selected_student is None:
            return

        self.show_assigned_fees()


    # ========================================================
    # SCREEN 2 - EXISTING ASSIGNED FEES + DELETE
    # ========================================================

    def show_assigned_fees(self):
        if self.selected_student is None:
            self.show_select_student()
            return

        self.clear_page()
        self.assigned_fee_map.clear()

        self.page_header(
            "Student Fee Assignments",
            "Review all semester fees already assigned to the selected student.",
            2,
            self.show_select_student
        )

        wrapper = Frame(self.page, bg=BG)
        wrapper.pack(fill=BOTH, expand=True, padx=28, pady=(0, 24))

        student_card = Frame(
            wrapper,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        student_card.pack(fill=X, pady=(0, 12))

        left = Frame(student_card, bg=WHITE)
        left.pack(side=LEFT, fill=X, expand=True, padx=20, pady=16)

        Label(
            left,
            text="SELECTED STUDENT",
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8, "bold")
        ).pack(anchor=W)

        Label(
            left,
            text=self.selected_student["Name"],
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 16, "bold")
        ).pack(anchor=W, pady=(4, 2))

        Label(
            left,
            text=self.selected_student["Registration_No"],
            bg=WHITE,
            fg=BLUE,
            font=(FONT, 9, "bold")
        ).pack(anchor=W)

        right = Frame(student_card, bg=WHITE)
        right.pack(side=RIGHT, padx=20, pady=16)

        info1 = Frame(right, bg=WHITE)
        info1.pack(side=LEFT, padx=18)

        Label(
            info1,
            text="COURSE",
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8, "bold")
        ).pack(anchor=W)

        Label(
            info1,
            text=self.selected_student["Course"],
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(anchor=W, pady=(4, 0))

        info2 = Frame(right, bg=WHITE)
        info2.pack(side=LEFT, padx=18)

        Label(
            info2,
            text="CURRENT SEMESTER",
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8, "bold")
        ).pack(anchor=W)

        Label(
            info2,
            text=f"Semester {self.selected_student['Semester']}",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(anchor=W, pady=(4, 0))

        totals = self.get_student_fee_totals()

        summary = Frame(wrapper, bg=BG)
        summary.pack(fill=X, pady=(0, 12))

        self.create_summary_card(
            summary,
            "TOTAL ASSIGNED",
            money(totals["Total_Assigned"]),
            BLUE,
            LIGHT_BLUE
        ).pack(side=LEFT, fill=X, expand=True, padx=(0, 6))

        self.create_summary_card(
            summary,
            "TOTAL PAID",
            money(totals["Total_Paid"]),
            GREEN,
            LIGHT_GREEN
        ).pack(side=LEFT, fill=X, expand=True, padx=6)

        self.create_summary_card(
            summary,
            "TOTAL DUE",
            money(totals["Total_Due"]),
            RED,
            LIGHT_RED
        ).pack(side=LEFT, fill=X, expand=True, padx=(6, 0))

        card = Frame(
            wrapper,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill=BOTH, expand=True)

        head = Frame(card, bg=WHITE)
        head.pack(fill=X, padx=20, pady=(16, 8))

        Label(
            head,
            text="EXISTING ASSIGNED FEES",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 11, "bold")
        ).pack(side=LEFT)

        self.assigned_count_label = Label(
            head,
            text="0 Assigned",
            bg=LIGHT_GRAY,
            fg=TEXT_2,
            padx=10,
            pady=5,
            font=(FONT, 8, "bold")
        )
        self.assigned_count_label.pack(side=RIGHT)

        Label(
            card,
            text=(
                "Each semester fee is stored separately. "
                "A paid or partially paid assignment cannot be deleted."
            ),
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8)
        ).pack(anchor=W, padx=20, pady=(0, 10))

        # ----------------------------------------------------
        # ALWAYS-VISIBLE ACTION BAR
        # The previous buttons were at the bottom of the card
        # and could go below the visible dashboard area.
        # ----------------------------------------------------

        action_bar = Frame(
            card,
            bg=LIGHT_GRAY,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        action_bar.pack(fill=X, padx=20, pady=(0, 12))

        Label(
            action_bar,
            text=(
                "Select an existing row to delete it, "
                "or continue to assign a new semester fee."
            ),
            bg=LIGHT_GRAY,
            fg=GRAY,
            font=(FONT, 8)
        ).pack(side=LEFT, padx=12, pady=10)

        self.make_button(
            action_bar,
            "DELETE SELECTED",
            self.delete_selected_assignment,
            "danger",
            18
        ).pack(side=RIGHT, padx=(8, 10), pady=7)

        self.make_button(
            action_bar,
            "ASSIGN NEW FEE  →",
            self.show_fee_structures,
            "primary",
            20
        ).pack(side=RIGHT, pady=7)

        table_holder = Frame(card, bg=WHITE)
        table_holder.pack(fill=BOTH, expand=True, padx=20, pady=(0, 12))

        columns = (
            "fee_id",
            "academic_year",
            "semester",
            "total",
            "paid",
            "due",
            "status",
            "payments"
        )

        self.assigned_tree = ttk.Treeview(
            table_holder,
            columns=columns,
            show="headings",
            style="Assign.Treeview",
            height=7
        )

        headings = {
            "fee_id": "FEE ID",
            "academic_year": "ACADEMIC YEAR",
            "semester": "SEMESTER",
            "total": "TOTAL FEE",
            "paid": "PAID",
            "due": "DUE",
            "status": "STATUS",
            "payments": "PAYMENTS"
        }

        widths = {
            "fee_id": 80,
            "academic_year": 130,
            "semester": 110,
            "total": 125,
            "paid": 125,
            "due": 125,
            "status": 100,
            "payments": 90
        }

        for col in columns:
            self.assigned_tree.heading(col, text=headings[col])
            self.assigned_tree.column(col, width=widths[col], anchor=CENTER)

        y_scroll = Scrollbar(
            table_holder,
            orient=VERTICAL,
            command=self.assigned_tree.yview
        )

        self.assigned_tree.configure(yscrollcommand=y_scroll.set)

        self.assigned_tree.pack(side=LEFT, fill=BOTH, expand=True)
        y_scroll.pack(side=RIGHT, fill=Y)

        # Double-clicking an assigned fee row opens the next step
        # for assigning another semester fee.
        self.assigned_tree.bind(
            "<Double-1>",
            lambda event: self.show_fee_structures()
        )

        note = Frame(
            card,
            bg=LIGHT_ORANGE,
            highlightbackground="#FED7AA",
            highlightthickness=1
        )
        note.pack(fill=X, padx=20, pady=(0, 12))

        Label(
            note,
            text=(
                f"Current total outstanding due: {money(totals['Total_Due'])}. "
                "Assigning a new semester fee will not change old semester dues."
            ),
            bg=LIGHT_ORANGE,
            fg=ORANGE,
            font=(FONT, 8, "bold")
        ).pack(anchor=W, padx=12, pady=10)

        footer = Frame(card, bg=WHITE)
        footer.pack(fill=X, padx=20, pady=(0, 16))

        self.make_button(
            footer,
            "←  CHANGE STUDENT",
            self.show_select_student,
            "secondary",
            19
        ).pack(side=LEFT)

        Label(
            footer,
            text=(
                "Use ASSIGN NEW FEE above to continue to Step 3."
            ),
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8)
        ).pack(side=RIGHT, pady=10)

        self.load_assigned_fees()


    def create_summary_card(
        self,
        parent,
        title,
        value,
        value_color,
        background
    ):
        card = Frame(
            parent,
            bg=background,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        Label(
            card,
            text=title,
            bg=background,
            fg=GRAY,
            font=(FONT, 8, "bold")
        ).pack(anchor=W, padx=16, pady=(12, 3))

        Label(
            card,
            text=value,
            bg=background,
            fg=value_color,
            font=(FONT, 15, "bold")
        ).pack(anchor=W, padx=16, pady=(0, 12))

        return card


    def get_student_fee_totals(self):
        result = {
            "Total_Assigned": Decimal("0.00"),
            "Total_Paid": Decimal("0.00"),
            "Total_Due": Decimal("0.00")
        }

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    COALESCE(SUM(Total_Fee), 0) AS Total_Assigned,
                    COALESCE(SUM(Amount_Paid), 0) AS Total_Paid,
                    COALESCE(SUM(Due_Amount), 0) AS Total_Due
                FROM student_fees
                WHERE Registration_No = %s
                """,
                (self.selected_student["Registration_No"],)
            )

            row = cursor.fetchone() or {}

            result["Total_Assigned"] = decimal_value(row.get("Total_Assigned"))
            result["Total_Paid"] = decimal_value(row.get("Total_Paid"))
            result["Total_Due"] = decimal_value(row.get("Total_Due"))

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Fee Summary Error",
                str(error),
                parent=center_message_parent(self.parent)
            )

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()

        return result


    def load_assigned_fees(self):
        self.assigned_fee_map.clear()

        for item in self.assigned_tree.get_children():
            self.assigned_tree.delete(item)

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    sf.Student_Fee_ID,
                    sf.Registration_No,
                    sf.Fee_Structure_ID,
                    fs.Academic_Year,
                    fs.Semester,
                    c.Course_ID,
                    c.Course_Name,
                    sf.Total_Fee,
                    sf.Amount_Paid,
                    sf.Due_Amount,
                    sf.Payment_Status,
                    sf.Assigned_At,
                    COUNT(fp.Payment_ID) AS Payment_Count
                FROM student_fees AS sf
                INNER JOIN fee_structures AS fs
                    ON sf.Fee_Structure_ID = fs.Fee_Structure_ID
                INNER JOIN courses AS c
                    ON fs.Course_ID = c.Course_ID
                LEFT JOIN fee_payments AS fp
                    ON sf.Student_Fee_ID = fp.Student_Fee_ID
                WHERE sf.Registration_No = %s
                GROUP BY
                    sf.Student_Fee_ID,
                    sf.Registration_No,
                    sf.Fee_Structure_ID,
                    fs.Academic_Year,
                    fs.Semester,
                    c.Course_ID,
                    c.Course_Name,
                    sf.Total_Fee,
                    sf.Amount_Paid,
                    sf.Due_Amount,
                    sf.Payment_Status,
                    sf.Assigned_At
                ORDER BY
                    fs.Academic_Year ASC,
                    fs.Semester ASC,
                    sf.Student_Fee_ID ASC
                """,
                (self.selected_student["Registration_No"],)
            )

            rows = cursor.fetchall()

            for row in rows:
                item_id = self.assigned_tree.insert(
                    "",
                    END,
                    values=(
                        row["Student_Fee_ID"],
                        row["Academic_Year"],
                        f"Semester {row['Semester']}",
                        money(row["Total_Fee"]),
                        money(row["Amount_Paid"]),
                        money(row["Due_Amount"]),
                        row["Payment_Status"],
                        row["Payment_Count"]
                    )
                )

                self.assigned_fee_map[item_id] = {
                    "Student_Fee_ID": int(row["Student_Fee_ID"]),
                    "Registration_No": str(row["Registration_No"]),
                    "Fee_Structure_ID": int(row["Fee_Structure_ID"]),
                    "Academic_Year": str(row["Academic_Year"]),
                    "Semester": int(row["Semester"]),
                    "Course_ID": str(row["Course_ID"]),
                    "Course_Name": str(row["Course_Name"]),
                    "Total_Fee": decimal_value(row["Total_Fee"]),
                    "Amount_Paid": decimal_value(row["Amount_Paid"]),
                    "Due_Amount": decimal_value(row["Due_Amount"]),
                    "Payment_Status": str(row["Payment_Status"]),
                    "Payment_Count": int(row["Payment_Count"] or 0)
                }

            self.assigned_count_label.config(
                text=f"{len(rows)} Assigned"
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Assigned Fees Error",
                (
                    "Unable to load assigned fees.\n\n"
                    f"{error}"
                ),
                parent=center_message_parent(self.parent)
            )

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()


    # ========================================================
    # DELETE ASSIGNMENT
    # ========================================================

    def delete_selected_assignment(self):
        selection = self.assigned_tree.selection()

        if not selection:
            messagebox.showwarning(
                "Select Assigned Fee",
                "Please select one assigned fee from the table.",
                parent=center_message_parent(self.parent)
            )
            return

        selected = self.assigned_fee_map.get(selection[0])

        if selected is None:
            return

        student_fee_id = selected["Student_Fee_ID"]

        connection = None
        cursor = None

        try:
            connection = get_connection()
            connection.start_transaction()

            cursor = connection.cursor(dictionary=True)

            # Lock the assignment while validating deletion.
            cursor.execute(
                """
                SELECT
                    Student_Fee_ID,
                    Registration_No,
                    Fee_Structure_ID,
                    Total_Fee,
                    Amount_Paid,
                    Due_Amount,
                    Payment_Status
                FROM student_fees
                WHERE Student_Fee_ID = %s
                FOR UPDATE
                """,
                (student_fee_id,)
            )

            current_fee = cursor.fetchone()

            if current_fee is None:
                connection.rollback()

                messagebox.showwarning(
                    "Assignment Not Found",
                    "The selected fee assignment no longer exists.",
                    parent=center_message_parent(self.parent)
                )

                self.show_assigned_fees()
                return

            cursor.execute(
                """
                SELECT
                    COUNT(*) AS Payment_Count,
                    COALESCE(SUM(Amount), 0) AS Payment_Total
                FROM fee_payments
                WHERE Student_Fee_ID = %s
                """,
                (student_fee_id,)
            )

            payment_data = cursor.fetchone() or {}

            payment_count = int(payment_data.get("Payment_Count") or 0)
            payment_total = decimal_value(payment_data.get("Payment_Total"))
            amount_paid = decimal_value(current_fee["Amount_Paid"])

            if (
                amount_paid > 0
                or payment_count > 0
                or payment_total > 0
            ):
                connection.rollback()

                messagebox.showerror(
                    "Delete Not Allowed",
                    (
                        "This fee assignment cannot be deleted because "
                        "financial payment history exists.\n\n"
                        f"Student Fee ID: {student_fee_id}\n"
                        f"Amount Paid: {money(amount_paid)}\n"
                        f"Payment Records: {payment_count}\n\n"
                        "Paid and partially paid fee assignments must be preserved."
                    ),
                    parent=center_message_parent(self.parent)
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                (
                    "Delete this unused fee assignment?\n\n"
                    f"Student: {self.selected_student['Name']}\n"
                    f"Registration No.: {self.selected_student['Registration_No']}\n"
                    f"Student Fee ID: {student_fee_id}\n"
                    f"Academic Year: {selected['Academic_Year']}\n"
                    f"Semester: {selected['Semester']}\n"
                    f"Total Fee: {money(selected['Total_Fee'])}\n\n"
                    "This action cannot be undone."
                ),
                parent=center_message_parent(self.parent)
            )

            if not confirm:
                connection.rollback()
                return

            # Final safe delete. If a payment appeared after the
            # previous check, NOT EXISTS prevents deletion.
            cursor.execute(
                """
                DELETE FROM student_fees
                WHERE Student_Fee_ID = %s
                  AND Amount_Paid = 0
                  AND NOT EXISTS (
                      SELECT 1
                      FROM fee_payments
                      WHERE fee_payments.Student_Fee_ID
                            = student_fees.Student_Fee_ID
                  )
                """,
                (student_fee_id,)
            )

            if cursor.rowcount != 1:
                connection.rollback()

                messagebox.showerror(
                    "Delete Failed",
                    (
                        "The assignment was not deleted. "
                        "It may now contain payment history."
                    ),
                    parent=center_message_parent(self.parent)
                )
                return

            connection.commit()

            messagebox.showinfo(
                "Fee Assignment Deleted",
                (
                    "The unused fee assignment was deleted successfully.\n\n"
                    f"Student Fee ID: {student_fee_id}"
                ),
                parent=center_message_parent(self.parent)
            )

            self.show_assigned_fees()

        except mysql.connector.Error as error:
            if connection is not None:
                try:
                    connection.rollback()
                except Exception:
                    pass

            messagebox.showerror(
                "Delete Fee Error",
                str(error),
                parent=center_message_parent(self.parent)
            )

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()


    # ========================================================
    # SCREEN 3 - AVAILABLE FEE STRUCTURES
    # ========================================================

    def show_fee_structures(self):
        self.clear_page()

        if not self.selected_student:
            messagebox.showwarning(
                "Student Required",
                "Please select a student first.",
                parent=center_message_parent(self.parent)
            )
            self.show_select_student()
            return

        self.page_header(
            "Select Fee Structure",
            "Only the selected student's current-semester fee structure can be added.",
            3,
            self.show_assigned_fees,
            show_progress=True
        )

        registration_no = str(
            self.selected_student.get("Registration_No", "")
        ).strip()
        student_name = str(
            self.selected_student.get("Name", "")
        ).strip()
        student_course = str(
            self.selected_student.get("Course", "")
        ).strip()

        try:
            current_semester = int(
                self.selected_student.get("Semester", 0)
            )
        except (TypeError, ValueError):
            current_semester = 0

        # Refresh the student's current course and semester directly from DB.
        # This prevents stale values when the student has moved to a new semester.
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    r.Registration_No,
                    r.Name,
                    sd.Course,
                    sd.Semester,
                    sd.Admission_Year,
                    sd.Status
                FROM registration AS r
                INNER JOIN student_details AS sd
                    ON sd.Registration_No = r.Registration_No
                WHERE r.Registration_No = %s
                  AND LOWER(TRIM(r.Role)) = 'student'
                LIMIT 1
                """,
                (registration_no,)
            )

            fresh_student = cursor.fetchone()

            if fresh_student:
                student_name = str(fresh_student.get("Name") or "").strip()
                student_course = str(fresh_student.get("Course") or "").strip()

                try:
                    current_semester = int(
                        fresh_student.get("Semester") or 0
                    )
                except (TypeError, ValueError):
                    current_semester = 0

                self.selected_student.update(fresh_student)

            # IMPORTANT:
            # Match the student's Course text against courses.Course_Name.
            # Do not assume student_details.Course contains Course_ID.
            cursor.execute(
                """
                SELECT
                    fs.Fee_Structure_ID,
                    c.Course_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year,
                    COUNT(fsc.Component_ID) AS Component_Count,
                    COALESCE(SUM(fsc.Amount), 0) AS Total_Fee
                FROM fee_structures AS fs
                INNER JOIN courses AS c
                    ON c.Course_ID = fs.Course_ID
                LEFT JOIN fee_structure_components AS fsc
                    ON fsc.Fee_Structure_ID = fs.Fee_Structure_ID
                WHERE LOWER(TRIM(c.Course_Name)) = LOWER(TRIM(%s))
                  AND fs.Semester = %s
                  AND (
                        fs.Status IS NULL
                        OR LOWER(TRIM(fs.Status)) = 'active'
                      )
                  AND NOT EXISTS (
                        SELECT 1
                        FROM student_fees AS sf
                        WHERE sf.Registration_No = %s
                          AND sf.Fee_Structure_ID = fs.Fee_Structure_ID
                  )
                GROUP BY
                    fs.Fee_Structure_ID,
                    c.Course_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year
                ORDER BY
                    fs.Academic_Year DESC,
                    fs.Fee_Structure_ID DESC
                """,
                (
                    student_course,
                    current_semester,
                    registration_no
                )
            )

            rows = cursor.fetchall()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                "Unable to load fee structures.\n\n"
                f"{error}",
                parent=center_message_parent(self.parent)
            )
            return

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

        # Selected student information strip.
        info = Frame(
            self.page,
            bg="#EFF6FF",
            highlightbackground="#BFDBFE",
            highlightthickness=1
        )
        info.pack(fill=X, padx=28, pady=(10, 12))

        Label(
            info,
            text=(
                f"{student_name}   •   {registration_no}   •   "
                f"{student_course}   •   Current Semester {current_semester}"
            ),
            bg="#EFF6FF",
            fg=BLUE,
            font=(FONT, 10, "bold"),
            anchor="w"
        ).pack(fill=X, padx=18, pady=14)

        card = Frame(
            self.page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill=BOTH, expand=True, padx=28, pady=(0, 18))

        top = Frame(card, bg=WHITE)
        top.pack(fill=X, padx=20, pady=(18, 8))

        Label(
            top,
            text="AVAILABLE FEE STRUCTURES",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 11, "bold")
        ).pack(side=LEFT)

        Label(
            top,
            text=f"{len(rows)} Available",
            bg="#EFF6FF",
            fg=BLUE,
            font=(FONT, 9, "bold"),
            padx=12,
            pady=7
        ).pack(side=RIGHT)

        Label(
            card,
            text=(
                "Only active fee structures for the student's exact current "
                "course and semester are shown. Already assigned structures are hidden."
            ),
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 9),
            anchor="w"
        ).pack(fill=X, padx=20, pady=(0, 12))

        action_bar = Frame(card, bg="#F1F5F9")
        action_bar.pack(fill=X, padx=20, pady=(0, 10))

        Label(
            action_bar,
            text=(
                f"Current Semester: {current_semester}  •  "
                "Select one matching fee structure, then click ADD SELECTED FEE."
            ),
            bg="#F1F5F9",
            fg=TEXT,
            font=(FONT, 9, "bold"),
            anchor="w"
        ).pack(side=LEFT, fill=X, expand=True, padx=14, pady=12)

        add_button = self.make_button(
            action_bar,
            "ADD SELECTED FEE  →",
            self.review_selected_structure,
            "primary",
            20
        )
        add_button.pack(side=RIGHT, padx=10, pady=8)

        table_frame = Frame(card, bg=WHITE)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 18))

        columns = (
            "Fee_Structure_ID",
            "Course",
            "Semester",
            "Academic_Year",
            "Components",
            "Total_Fee"
        )

        self.fee_structure_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "Fee_Structure_ID": "STRUCTURE ID",
            "Course": "COURSE",
            "Semester": "SEMESTER",
            "Academic_Year": "ACADEMIC YEAR",
            "Components": "COMPONENTS",
            "Total_Fee": "TOTAL FEE"
        }

        widths = {
            "Fee_Structure_ID": 120,
            "Course": 250,
            "Semester": 110,
            "Academic_Year": 150,
            "Components": 120,
            "Total_Fee": 160
        }

        for column in columns:
            self.fee_structure_tree.heading(
                column,
                text=headings[column]
            )
            self.fee_structure_tree.column(
                column,
                width=widths[column],
                anchor=CENTER
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=VERTICAL,
            command=self.fee_structure_tree.yview
        )
        self.fee_structure_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.fee_structure_tree.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )
        scrollbar.pack(
            side=RIGHT,
            fill=Y
        )

        self.available_fee_structures = {}

        for row in rows:
            structure_id = int(row["Fee_Structure_ID"])
            total_fee = float(row["Total_Fee"] or 0)

            self.available_fee_structures[structure_id] = row

            self.fee_structure_tree.insert(
                "",
                END,
                iid=str(structure_id),
                values=(
                    structure_id,
                    row["Course_Name"],
                    f"Semester {row['Semester']}",
                    row["Academic_Year"],
                    row["Component_Count"],
                    f"₹{total_fee:,.2f}"
                )
            )

        self.fee_structure_tree.bind(
            "<Double-1>",
            lambda event: self.review_selected_structure()
        )

        if not rows:
            Label(
                table_frame,
                text=(
                    "No unassigned active fee structure was found for:\n"
                    f"{student_course} • Semester {current_semester}\n\n"
                    "Create/activate a matching fee structure, or check whether "
                    "it is already assigned to this student."
                ),
                bg=WHITE,
                fg=GRAY,
                font=(FONT, 10),
                justify=CENTER
            ).place(relx=0.5, rely=0.45, anchor=CENTER)


    def open_selected_fee_review(self):
        if not hasattr(self, "fee_structure_tree"):
            return

        selected = self.fee_structure_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Fee Structure",
                "Please select one fee structure first.",
                parent=center_message_parent(self.parent)
            )
            return

        structure_id = int(selected[0])

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    fs.Fee_Structure_ID,
                    c.Course_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year,
                    fsc.Component_ID,
                    fsc.Fee_Type,
                    fsc.Amount
                FROM fee_structures AS fs
                INNER JOIN courses AS c
                    ON c.Course_ID = fs.Course_ID
                LEFT JOIN fee_structure_components AS fsc
                    ON fsc.Fee_Structure_ID = fs.Fee_Structure_ID
                WHERE fs.Fee_Structure_ID = %s
                ORDER BY fsc.Component_ID
                """,
                (structure_id,)
            )

            component_rows = cursor.fetchall()

            if not component_rows:
                messagebox.showerror(
                    "Fee Structure Error",
                    "The selected fee structure could not be loaded.",
                    parent=center_message_parent(self.parent)
                )
                return

            first = component_rows[0]

            self.selected_fee_structure = {
                "Fee_Structure_ID": first["Fee_Structure_ID"],
                "Course_ID": first["Course_ID"],
                "Course_Name": first["Course_Name"],
                "Semester": first["Semester"],
                "Academic_Year": first["Academic_Year"],
                "Components": [],
                "Total_Fee": 0.0
            }

            total = 0.0

            for row in component_rows:
                if row["Component_ID"] is None:
                    continue

                amount = float(row["Amount"] or 0)
                total += amount

                self.selected_fee_structure["Components"].append(
                    {
                        "Component_ID": row["Component_ID"],
                        "Fee_Type": row["Fee_Type"],
                        "Amount": amount
                    }
                )

            self.selected_fee_structure["Total_Fee"] = total

            self.show_review_assignment()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                "Unable to prepare the fee assignment review.\n\n"
                f"{error}",
                parent=center_message_parent(self.parent)
            )

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()


    def get_student_course(self):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            # student_details.Course contains the course name.
            # fee_structures stores Course_ID.
            cursor.execute(
                """
                SELECT
                    Course_ID,
                    Course_Name,
                    Duration_Years,
                    Total_Semesters,
                    Status
                FROM courses
                WHERE LOWER(TRIM(Course_Name))
                      = LOWER(TRIM(%s))
                LIMIT 1
                """,
                (self.selected_student["Course"],)
            )

            return cursor.fetchone()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Course Match Error",
                str(error),
                parent=center_message_parent(self.parent)
            )
            return None

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()


    def load_available_fee_structures(self):
        course = self.get_student_course()

        if course is None:
            messagebox.showerror(
                "Course Not Found",
                (
                    "The student's course could not be matched with courses.Course_Name.\n\n"
                    f"Student course: {self.selected_student['Course']}\n\n"
                    "Make sure student_details.Course and courses.Course_Name contain "
                    "the same course name."
                ),
                parent=center_message_parent(self.parent)
            )
            return

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    fs.Fee_Structure_ID,
                    fs.Course_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year,
                    fs.Status,
                    COUNT(fsc.Component_ID) AS Component_Count,
                    COALESCE(SUM(fsc.Amount), 0) AS Total_Fee
                FROM fee_structures AS fs
                INNER JOIN courses AS c
                    ON fs.Course_ID = c.Course_ID
                LEFT JOIN fee_structure_components AS fsc
                    ON fs.Fee_Structure_ID = fsc.Fee_Structure_ID
                WHERE fs.Course_ID = %s
                  AND LOWER(TRIM(fs.Status)) = 'active'
                  AND fs.Semester = %s
                  AND NOT EXISTS (
                      SELECT 1
                      FROM student_fees AS sf
                      WHERE sf.Registration_No = %s
                        AND sf.Fee_Structure_ID = fs.Fee_Structure_ID
                  )
                GROUP BY
                    fs.Fee_Structure_ID,
                    fs.Course_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year,
                    fs.Status
                ORDER BY
                    fs.Semester ASC,
                    fs.Academic_Year ASC,
                    fs.Fee_Structure_ID ASC
                """,
                (
                    course["Course_ID"],
                    self.selected_student["Semester"],
                    self.selected_student["Registration_No"]
                )
            )

            rows = cursor.fetchall()

            for row in rows:
                item_id = self.structure_tree.insert(
                    "",
                    END,
                    values=(
                        row["Fee_Structure_ID"],
                        row["Course_Name"],
                        f"Semester {row['Semester']}",
                        row["Academic_Year"],
                        row["Component_Count"],
                        money(row["Total_Fee"])
                    )
                )

                self.structure_map[item_id] = {
                    "Fee_Structure_ID": int(row["Fee_Structure_ID"]),
                    "Course_ID": str(row["Course_ID"]),
                    "Course_Name": str(row["Course_Name"]),
                    "Semester": int(row["Semester"]),
                    "Academic_Year": str(row["Academic_Year"]),
                    "Status": str(row["Status"]),
                    "Component_Count": int(row["Component_Count"] or 0),
                    "Total_Fee": decimal_value(row["Total_Fee"])
                }

            self.available_count_label.config(
                text=f"{len(rows)} Available"
            )

            if not rows:
                clear_widgets(self.component_preview)

                Label(
                    self.component_preview,
                    text=(
                        "No new fee structures are currently available for this student. "
                        "The matching structures may already be assigned."
                    ),
                    bg=LIGHT_RED,
                    fg=RED,
                    font=(FONT, 8, "bold")
                ).pack(fill=X, padx=12, pady=11)

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Fee Structure Error",
                (
                    "Unable to load fee structures.\n\n"
                    f"{error}"
                ),
                parent=center_message_parent(self.parent)
            )

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()


    def on_structure_selected(self, event=None):
        selection = self.structure_tree.selection()

        if not selection:
            self.selected_fee_structure = None
            self.selected_components = []
            self.review_button.config(state=DISABLED, cursor="arrow")
            if hasattr(self, "top_add_button"):
                self.top_add_button.config(state=DISABLED, cursor="arrow")
            return

        self.selected_fee_structure = self.structure_map.get(selection[0])

        if self.selected_fee_structure is None:
            return

        self.selected_components = self.load_fee_components(
            self.selected_fee_structure["Fee_Structure_ID"]
        )

        clear_widgets(self.component_preview)

        header = Frame(self.component_preview, bg=LIGHT_GRAY)
        header.pack(fill=X, padx=12, pady=(10, 6))

        Label(
            header,
            text=(
                f"{self.selected_fee_structure['Course_Name']}  •  "
                f"Semester {self.selected_fee_structure['Semester']}  •  "
                f"{self.selected_fee_structure['Academic_Year']}"
            ),
            bg=LIGHT_GRAY,
            fg=TEXT,
            font=(FONT, 9, "bold")
        ).pack(side=LEFT)

        total = Decimal("0.00")

        component_area = Frame(self.component_preview, bg=LIGHT_GRAY)
        component_area.pack(fill=X, padx=12, pady=(0, 10))

        if not self.selected_components:
            Label(
                component_area,
                text="No fee components exist for this structure.",
                bg=LIGHT_GRAY,
                fg=RED,
                font=(FONT, 8, "bold")
            ).pack(anchor=W)

            self.review_button.config(state=DISABLED, cursor="arrow")
            if hasattr(self, "top_add_button"):
                self.top_add_button.config(state=DISABLED, cursor="arrow")
            return

        for component in self.selected_components:
            amount = decimal_value(component["Amount"])
            total += amount

            row = Frame(component_area, bg=LIGHT_GRAY)
            row.pack(fill=X, pady=2)

            Label(
                row,
                text=component["Fee_Type"],
                bg=LIGHT_GRAY,
                fg=TEXT_2,
                font=(FONT, 8)
            ).pack(side=LEFT)

            Label(
                row,
                text=money(amount),
                bg=LIGHT_GRAY,
                fg=TEXT,
                font=(FONT, 8, "bold")
            ).pack(side=RIGHT)

        self.selected_fee_structure["Total_Fee"] = total

        Label(
            header,
            text=money(total),
            bg=LIGHT_GRAY,
            fg=BLUE,
            font=(FONT, 11, "bold")
        ).pack(side=RIGHT)

        self.review_button.config(state=NORMAL, cursor="hand2")
        if hasattr(self, "top_add_button"):
            self.top_add_button.config(state=NORMAL, cursor="hand2")


    def load_fee_components(self, fee_structure_id):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    Component_ID,
                    Fee_Structure_ID,
                    Fee_Type,
                    Amount
                FROM fee_structure_components
                WHERE Fee_Structure_ID = %s
                ORDER BY Component_ID ASC
                """,
                (fee_structure_id,)
            )

            return cursor.fetchall()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Fee Component Error",
                str(error),
                parent=center_message_parent(self.parent)
            )
            return []

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()


    def review_selected_structure(self):
        # Step 3 uses self.fee_structure_tree. Read the selection from that exact
        # Treeview instead of an older Treeview attribute from the previous UI.
        tree = getattr(self, "fee_structure_tree", None)

        if tree is None:
            messagebox.showerror(
                "Fee Structure Error",
                "The fee structure table is not available.",
                parent=center_message_parent(self.parent)
            )
            return

        selected = tree.selection()

        # On some Tk/Windows themes a row can have focus but selection() may be
        # temporarily empty. Use the focused row as a safe fallback.
        if not selected:
            focused = tree.focus()
            if focused:
                selected = (focused,)

        if not selected:
            messagebox.showwarning(
                "Select Fee Structure",
                "Please select one fee structure first.",
                parent=center_message_parent(self.parent)
            )
            return

        item_id = selected[0]
        item = tree.item(item_id)
        values = item.get("values", ())

        # The Step 3 table stores Fee_Structure_ID in the first column and also
        # uses the structure ID as the Treeview iid.
        try:
            if values:
                structure_id = int(values[0])
            else:
                structure_id = int(item_id)
        except (TypeError, ValueError, IndexError):
            messagebox.showerror(
                "Selection Error",
                "Unable to read the selected fee structure ID.",
                parent=center_message_parent(self.parent)
            )
            return

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    fs.Fee_Structure_ID,
                    fs.Course_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year,
                    fs.Status
                FROM fee_structures AS fs
                INNER JOIN courses AS c
                    ON c.Course_ID = fs.Course_ID
                WHERE fs.Fee_Structure_ID = %s
                LIMIT 1
                """,
                (structure_id,)
            )

            structure = cursor.fetchone()

            if not structure:
                messagebox.showerror(
                    "Fee Structure Error",
                    "The selected fee structure no longer exists.",
                    parent=center_message_parent(self.parent)
                )
                return

            cursor.execute(
                """
                SELECT
                    Component_ID,
                    Fee_Type,
                    Amount
                FROM fee_structure_components
                WHERE Fee_Structure_ID = %s
                ORDER BY Component_ID
                """,
                (structure_id,)
            )

            components = cursor.fetchall()

            total_fee = sum(
                float(row.get("Amount") or 0)
                for row in components
            )

            # Store both the dictionary expected by the newer UI and the common
            # scalar attributes used by older review code.
            self.selected_fee_structure = {
                "Fee_Structure_ID": structure["Fee_Structure_ID"],
                "Course_ID": structure["Course_ID"],
                "Course_Name": structure["Course_Name"],
                "Semester": structure["Semester"],
                "Academic_Year": structure["Academic_Year"],
                "Status": structure["Status"],
                "Components": components,
                "Total_Fee": total_fee
            }

            self.selected_structure_id = structure_id
            self.selected_structure = self.selected_fee_structure

            # Use the existing review page in this class.
            self.show_review()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                "Unable to load the selected fee structure.\n\n"
                f"{error}",
                parent=center_message_parent(self.parent)
            )

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

    def show_review(self):
        if self.selected_student is None:
            self.show_select_student()
            return

        if self.selected_fee_structure is None:
            self.show_fee_structures()
            return

        self.clear_page()

        self.page_header(
            "Review Fee Assignment",
            "Verify the student, semester and fee breakdown before confirming.",
            4,
            self.show_fee_structures
        )

        # IMPORTANT:
        # The action bar is packed FIRST at the bottom of the page.
        # Therefore it always remains visible even when the review content is tall.
        fixed_action_bar = Frame(
            self.page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            height=72
        )
        fixed_action_bar.pack(side=BOTTOM, fill=X, padx=28, pady=(0, 16))
        fixed_action_bar.pack_propagate(False)

        self.make_button(
            fixed_action_bar,
            "←  BACK TO FEE STRUCTURE",
            self.show_fee_structures,
            "secondary",
            24
        ).pack(side=LEFT, padx=14, pady=14)

        self.make_button(
            fixed_action_bar,
            "CONFIRM & ASSIGN FEE",
            self.assign_fee,
            "success",
            24
        ).pack(side=RIGHT, padx=14, pady=14)

        # Review content gets only the remaining available space.
        wrapper = Frame(self.page, bg=BG)
        wrapper.pack(side=TOP, fill=BOTH, expand=True, padx=28, pady=(0, 10))

        card = Frame(
            wrapper,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill=BOTH, expand=True)

        Label(
            card,
            text="FEE ASSIGNMENT SUMMARY",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 12, "bold")
        ).pack(anchor=W, padx=24, pady=(14, 10))

        # Compact two-column summary so Step 4 fits on normal laptop screens.
        summary = Frame(card, bg=WHITE)
        summary.pack(fill=X, padx=24)

        left = Frame(summary, bg=WHITE)
        left.pack(side=LEFT, fill=X, expand=True)

        right = Frame(summary, bg=WHITE)
        right.pack(side=LEFT, fill=X, expand=True, padx=(30, 0))

        self.review_row(left, "Student", self.selected_student["Name"])
        self.review_row(
            left,
            "Registration No.",
            self.selected_student["Registration_No"]
        )
        self.review_row(
            left,
            "Course",
            self.selected_fee_structure["Course_Name"]
        )

        self.review_row(
            right,
            "Semester",
            f"Semester {self.selected_fee_structure['Semester']}"
        )
        self.review_row(
            right,
            "Academic Year",
            self.selected_fee_structure["Academic_Year"]
        )
        self.review_row(
            right,
            "Fee Structure ID",
            str(self.selected_fee_structure["Fee_Structure_ID"])
        )

        Frame(card, bg=BORDER, height=1).pack(fill=X, padx=24, pady=10)

        Label(
            card,
            text="FEE BREAKDOWN",
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8, "bold")
        ).pack(anchor=W, padx=24, pady=(0, 6))

        component_box = Frame(card, bg=WHITE)
        component_box.pack(fill=X, padx=24)

        total = Decimal("0.00")

        for component in self.selected_components:
            amount = decimal_value(component["Amount"])
            total += amount

            row = Frame(component_box, bg=WHITE)
            row.pack(fill=X, pady=2)

            Label(
                row,
                text=component["Fee_Type"],
                bg=WHITE,
                fg=TEXT_2,
                font=(FONT, 9)
            ).pack(side=LEFT)

            Label(
                row,
                text=money(amount),
                bg=WHITE,
                fg=TEXT,
                font=(FONT, 9, "bold")
            ).pack(side=RIGHT)

        self.selected_fee_structure["Total_Fee"] = total

        total_box = Frame(
            card,
            bg=LIGHT_BLUE,
            highlightbackground="#BFDBFE",
            highlightthickness=1
        )
        total_box.pack(fill=X, padx=24, pady=10)

        Label(
            total_box,
            text="TOTAL NEW FEE",
            bg=LIGHT_BLUE,
            fg=DARK_BLUE,
            font=(FONT, 9, "bold")
        ).pack(side=LEFT, padx=14, pady=10)

        Label(
            total_box,
            text=money(total),
            bg=LIGHT_BLUE,
            fg=BLUE,
            font=(FONT, 15, "bold")
        ).pack(side=RIGHT, padx=14, pady=10)

        old_totals = self.get_student_fee_totals()

        due_note = Frame(
            card,
            bg=LIGHT_ORANGE,
            highlightbackground="#FED7AA",
            highlightthickness=1
        )
        due_note.pack(fill=X, padx=24, pady=(0, 8))

        Label(
            due_note,
            text=(
                f"Existing outstanding due: {money(old_totals['Total_Due'])}. "
                "This amount remains unchanged. The new fee is stored as a separate semester assignment."
            ),
            bg=LIGHT_ORANGE,
            fg=ORANGE,
            font=(FONT, 8, "bold"),
            wraplength=900,
            justify=LEFT
        ).pack(anchor=W, padx=12, pady=8)

        accountant_box = Frame(card, bg=LIGHT_GRAY)
        accountant_box.pack(fill=X, padx=24, pady=(0, 10))

        Label(
            accountant_box,
            text=f"Current accountant: {self.accountant_text()}",
            bg=LIGHT_GRAY,
            fg=GRAY,
            font=(FONT, 8)
        ).pack(anchor=W, padx=12, pady=7)

    def review_row(self, parent, label_text, value):
        row = Frame(parent, bg=WHITE)
        row.pack(fill=X, pady=4)

        Label(
            row,
            text=label_text,
            bg=WHITE,
            fg=GRAY,
            width=20,
            anchor=W,
            font=(FONT, 8)
        ).pack(side=LEFT)

        Label(
            row,
            text=value,
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 9, "bold")
        ).pack(side=LEFT)


    # ========================================================
    # ASSIGN FEE
    # ========================================================

    def assign_fee(self):
        student = self.selected_student
        structure = self.selected_fee_structure

        if student is None or structure is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Fee Assignment",
            (
                "Assign this fee to the student?\n\n"
                f"Student: {student['Name']}\n"
                f"Registration No.: {student['Registration_No']}\n"
                f"Course: {structure['Course_Name']}\n"
                f"Semester: {structure['Semester']}\n"
                f"Academic Year: {structure['Academic_Year']}\n"
                f"Total Fee: {money(structure['Total_Fee'])}\n\n"
                "Existing semester dues will remain unchanged."
            ),
            parent=center_message_parent(self.parent)
        )

        if not confirm:
            return

        connection = None
        cursor = None

        try:
            connection = get_connection()
            connection.start_transaction()

            cursor = connection.cursor(dictionary=True)

            # Validate student still exists.
            cursor.execute(
                """
                SELECT
                    r.Registration_No,
                    r.Name
                FROM registration AS r
                INNER JOIN student_details AS sd
                    ON r.Registration_No = sd.Registration_No
                WHERE r.Registration_No = %s
                  AND LOWER(TRIM(r.Role)) = 'student'
                LIMIT 1
                FOR UPDATE
                """,
                (student["Registration_No"],)
            )

            if cursor.fetchone() is None:
                connection.rollback()

                messagebox.showerror(
                    "Student Not Found",
                    "The selected student no longer exists.",
                    parent=center_message_parent(self.parent)
                )
                return

            # Prevent duplicate assignment before insert.
            cursor.execute(
                """
                SELECT
                    Student_Fee_ID
                FROM student_fees
                WHERE Registration_No = %s
                  AND Fee_Structure_ID = %s
                LIMIT 1
                FOR UPDATE
                """,
                (
                    student["Registration_No"],
                    structure["Fee_Structure_ID"]
                )
            )

            duplicate = cursor.fetchone()

            if duplicate is not None:
                connection.rollback()

                messagebox.showwarning(
                    "Fee Already Assigned",
                    (
                        "This exact fee structure is already assigned "
                        "to the selected student.\n\n"
                        f"Existing Student Fee ID: {duplicate['Student_Fee_ID']}"
                    ),
                    parent=center_message_parent(self.parent)
                )

                self.show_assigned_fees()
                return

            # Recalculate total from the database at the moment
            # of assignment. Never trust only the UI value.
            cursor.execute(
                """
                SELECT
                    COUNT(*) AS Component_Count,
                    COALESCE(SUM(Amount), 0) AS Total_Fee
                FROM fee_structure_components
                WHERE Fee_Structure_ID = %s
                """,
                (structure["Fee_Structure_ID"],)
            )

            total_data = cursor.fetchone() or {}

            component_count = int(total_data.get("Component_Count") or 0)
            total_fee = decimal_value(total_data.get("Total_Fee"))

            if component_count == 0 or total_fee <= 0:
                connection.rollback()

                messagebox.showerror(
                    "Invalid Fee Structure",
                    (
                        "The selected fee structure does not contain "
                        "a valid fee component total."
                    ),
                    parent=center_message_parent(self.parent)
                )
                return

            # Exact INSERT for the actual student_fees schema.
            cursor.execute(
                """
                INSERT INTO student_fees
                (
                    Registration_No,
                    Fee_Structure_ID,
                    Total_Fee,
                    Amount_Paid,
                    Due_Amount,
                    Payment_Status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    0.00,
                    %s,
                    'Unpaid'
                )
                """,
                (
                    student["Registration_No"],
                    structure["Fee_Structure_ID"],
                    total_fee,
                    total_fee
                )
            )

            new_student_fee_id = cursor.lastrowid

            connection.commit()

            self.show_success(
                new_student_fee_id,
                total_fee
            )

        except mysql.connector.IntegrityError as error:
            if connection is not None:
                try:
                    connection.rollback()
                except Exception:
                    pass

            # Handles the unique key:
            # (Registration_No, Fee_Structure_ID)
            if getattr(error, "errno", None) == 1062:
                messagebox.showwarning(
                    "Fee Already Assigned",
                    (
                        "This fee structure is already assigned "
                        "to this student."
                    ),
                    parent=center_message_parent(self.parent)
                )

                self.show_assigned_fees()

            else:
                messagebox.showerror(
                    "Assignment Error",
                    str(error),
                    parent=center_message_parent(self.parent)
                )

        except mysql.connector.Error as error:
            if connection is not None:
                try:
                    connection.rollback()
                except Exception:
                    pass

            messagebox.showerror(
                "Assign Fee Error",
                (
                    "The fee could not be assigned.\n\n"
                    f"{error}"
                ),
                parent=center_message_parent(self.parent)
            )

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()


    # ========================================================
    # SUCCESS SCREEN
    # ========================================================

    def show_success(self, student_fee_id, total_fee):
        self.clear_page()

        outer = Frame(self.page, bg=BG)
        outer.pack(fill=BOTH, expand=True, padx=28, pady=28)

        card = Frame(
            outer,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.place(
            relx=0.5,
            rely=0.48,
            anchor=CENTER,
            width=650,
            height=450
        )

        Label(
            card,
            text="✓",
            bg=LIGHT_GREEN,
            fg=GREEN,
            width=3,
            pady=7,
            font=(FONT, 26, "bold")
        ).pack(pady=(38, 16))

        Label(
            card,
            text="FEE ASSIGNED SUCCESSFULLY",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 17, "bold")
        ).pack()

        Label(
            card,
            text=(
                f"Semester {self.selected_fee_structure['Semester']} fee "
                f"has been assigned to {self.selected_student['Name']}."
            ),
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 9)
        ).pack(pady=(8, 14))

        summary = Frame(card, bg=LIGHT_BLUE)
        summary.pack(fill=X, padx=55, pady=(0, 14))

        Label(
            summary,
            text=f"STUDENT FEE ID: {student_fee_id}",
            bg=LIGHT_BLUE,
            fg=GRAY,
            font=(FONT, 8, "bold")
        ).pack(pady=(11, 3))

        Label(
            summary,
            text=money(total_fee),
            bg=LIGHT_BLUE,
            fg=BLUE,
            font=(FONT, 17, "bold")
        ).pack(pady=(0, 11))

        Label(
            card,
            text=f"Assigned by: {self.accountant_text()}",
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8)
        ).pack(pady=(0, 16))

        buttons = Frame(card, bg=WHITE)
        buttons.pack()

        self.make_button(
            buttons,
            "SELECT ANOTHER STUDENT",
            self.show_select_student,
            "secondary",
            21
        ).pack(side=LEFT, padx=5)

        self.make_button(
            buttons,
            "VIEW ASSIGNED FEES",
            self.show_assigned_fees,
            "primary",
            20
        ).pack(side=LEFT, padx=5)


# ============================================================
# FUNCTION USED BY accountant_dashboard.py
# ============================================================


    # ========================================================
    # BULK / BATCH FEE ASSIGNMENT
    # ========================================================

    def bulk_step_indicator(self, parent, active_step):
        labels = ("Select Group", "Select Fee", "Review", "Complete")
        bar = Frame(parent, bg=LIGHT_GRAY)
        bar.pack(fill=X, pady=(0, 12))

        for index, label in enumerate(labels, start=1):
            cell = Frame(bar, bg=LIGHT_GRAY)
            cell.pack(side=LEFT, fill=X, expand=True, padx=4, pady=8)

            active = index <= active_step
            Label(
                cell,
                text=str(index),
                bg=BLUE if active else WHITE,
                fg=WHITE if active else GRAY,
                width=3,
                pady=6,
                font=(FONT, 9, "bold"),
                highlightbackground=BLUE if active else BORDER,
                highlightthickness=1
            ).pack(side=LEFT)

            Label(
                cell,
                text=label,
                bg=LIGHT_GRAY,
                fg=BLUE if index == active_step else (TEXT if index < active_step else GRAY),
                font=(FONT, 9, "bold" if index == active_step else "normal")
            ).pack(side=LEFT, padx=(8, 0))


    def show_assign_mode(self):
        self.clear_page()

        self.page_header(
            "Assign Fees",
            "Assign a fee to one student or to a complete course batch and semester.",
            1
        )

        wrapper = Frame(self.page, bg=BG)
        wrapper.pack(fill=BOTH, expand=True, padx=28, pady=(0, 24))

        Label(
            wrapper,
            text="CHOOSE ASSIGNMENT MODE",
            bg=BG,
            fg=TEXT,
            font=(FONT, 12, "bold")
        ).pack(anchor=W, pady=(8, 14))

        cards = Frame(wrapper, bg=BG)
        cards.pack(fill=X)

        single = Frame(cards, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        single.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 8))

        Label(
            single,
            text="SINGLE STUDENT",
            bg=WHITE,
            fg=BLUE,
            font=(FONT, 11, "bold")
        ).pack(anchor=W, padx=22, pady=(22, 8))

        Label(
            single,
            text="Search one student, review existing semester fees and assign a new fee structure.",
            bg=WHITE,
            fg=GRAY,
            justify=LEFT,
            wraplength=400,
            font=(FONT, 9)
        ).pack(anchor=W, padx=22)

        self.make_button(
            single,
            "OPEN SINGLE STUDENT ASSIGNMENT  →",
            self.show_select_student,
            "primary",
            32
        ).pack(anchor=W, padx=22, pady=22)

        bulk_card = Frame(cards, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        bulk_card.pack(side=LEFT, fill=BOTH, expand=True, padx=(8, 0))

        Label(
            bulk_card,
            text="BULK / BATCH ASSIGNMENT",
            bg=WHITE,
            fg=PURPLE,
            font=(FONT, 11, "bold")
        ).pack(anchor=W, padx=22, pady=(22, 8))

        Label(
            bulk_card,
            text="Select database-driven Course, Admission Batch and Current Semester, then assign one fee to selected matching students.",
            bg=WHITE,
            fg=GRAY,
            justify=LEFT,
            wraplength=400,
            font=(FONT, 9)
        ).pack(anchor=W, padx=22)

        self.make_button(
            bulk_card,
            "OPEN BULK ASSIGNMENT  →",
            self.show_bulk_target,
            "success",
            28
        ).pack(anchor=W, padx=22, pady=22)


    def show_bulk_target(self):
        self.clear_page()

        self.bulk_student_map = {}
        self.bulk_selected_students = []
        self.bulk_selected_structure = None
        self.bulk_selected_components = []

        self.bulk_course_var = StringVar(value="")
        self.bulk_batch_var = StringVar(value="")
        self.bulk_semester_var = StringVar(value="")
        self.bulk_count_var = StringVar(value="0 Students")

        self.page_header(
            "Bulk Assign Semester Fee",
            "Choose a student group from live database values.",
            1,
            self.show_assign_mode,
            show_progress=False
        )

        wrapper = Frame(self.page, bg=BG)
        wrapper.pack(fill=BOTH, expand=True, padx=28, pady=(0, 18))

        self.bulk_step_indicator(wrapper, 1)

        filter_card = Frame(wrapper, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        filter_card.pack(fill=X, pady=(0, 10))

        Label(
            filter_card,
            text="SELECT STUDENT GROUP",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 11, "bold")
        ).pack(anchor=W, padx=20, pady=(14, 10))

        filters = Frame(filter_card, bg=WHITE)
        filters.pack(fill=X, padx=20, pady=(0, 12))

        for col in range(3):
            filters.grid_columnconfigure(col, weight=1)

        def make_filter_box(column, title, variable):
            box = Frame(filters, bg=WHITE)
            box.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 8, 0 if column == 2 else 8))
            Label(
                box,
                text=title,
                bg=WHITE,
                fg=GRAY,
                font=(FONT, 8, "bold")
            ).pack(anchor=W, pady=(0, 5))
            combo = ttk.Combobox(
                box,
                textvariable=variable,
                state="readonly",
                font=(FONT, 9)
            )
            combo.pack(fill=X, ipady=6)
            return combo

        self.bulk_course_combo = make_filter_box(0, "COURSE", self.bulk_course_var)
        self.bulk_batch_combo = make_filter_box(1, "ADMISSION BATCH", self.bulk_batch_var)
        self.bulk_semester_combo = make_filter_box(2, "CURRENT SEMESTER", self.bulk_semester_var)

        self.bulk_course_combo.bind("<<ComboboxSelected>>", self.on_bulk_course_changed)
        self.bulk_batch_combo.bind("<<ComboboxSelected>>", self.on_bulk_batch_changed)
        self.bulk_semester_combo.bind("<<ComboboxSelected>>", self.on_bulk_semester_changed)

        action = Frame(filter_card, bg=WHITE)
        action.pack(fill=X, padx=20, pady=(0, 14))

        Label(
            action,
            text="Dropdown values are loaded from registration + student_details.",
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8)
        ).pack(side=LEFT)

        self.make_button(
            action,
            "LOAD MATCHING STUDENTS",
            self.load_bulk_students,
            "primary",
            24
        ).pack(side=RIGHT)

        table_card = Frame(wrapper, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        table_card.pack(fill=BOTH, expand=True)

        head = Frame(table_card, bg=WHITE)
        head.pack(fill=X, padx=20, pady=(12, 8))

        Label(
            head,
            text="MATCHING STUDENTS",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 11, "bold")
        ).pack(side=LEFT)

        self.make_button(
            head,
            "CONTINUE  →",
            self.bulk_continue_to_structure,
            "primary",
            16
        ).pack(side=RIGHT, padx=(10, 0))

        self.make_button(
            head,
            "CLEAR",
            self.bulk_clear_selection,
            "danger",
            10
        ).pack(side=RIGHT, padx=(8, 0))

        self.make_button(
            head,
            "SELECT ALL",
            self.bulk_select_all,
            "success",
            12
        ).pack(side=RIGHT, padx=(8, 0))

        Label(
            head,
            textvariable=self.bulk_count_var,
            bg=LIGHT_BLUE,
            fg=BLUE,
            padx=11,
            pady=5,
            font=(FONT, 8, "bold")
        ).pack(side=RIGHT)

        holder = Frame(table_card, bg=WHITE)
        holder.pack(fill=BOTH, expand=True, padx=20, pady=(0, 12))

        columns = ("registration", "name", "course", "semester", "batch", "status")
        self.bulk_student_tree = ttk.Treeview(
            holder,
            columns=columns,
            show="headings",
            style="Assign.Treeview",
            selectmode="extended",
            height=10
        )

        headings = {
            "registration": "REGISTRATION NO.",
            "name": "STUDENT NAME",
            "course": "COURSE",
            "semester": "CURRENT SEMESTER",
            "batch": "ADMISSION BATCH",
            "status": "PROFILE STATUS"
        }
        widths = {
            "registration": 145,
            "name": 200,
            "course": 220,
            "semester": 125,
            "batch": 125,
            "status": 110
        }

        for col in columns:
            self.bulk_student_tree.heading(col, text=headings[col])
            self.bulk_student_tree.column(
                col,
                width=widths[col],
                anchor=W if col in ("registration", "name", "course") else CENTER
            )

        scroll = Scrollbar(holder, orient=VERTICAL, command=self.bulk_student_tree.yview)
        self.bulk_student_tree.configure(yscrollcommand=scroll.set)
        self.bulk_student_tree.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)

        self.load_bulk_courses()


    def bulk_query_values(self, query, params=()):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params)
            return [row[0] for row in cursor.fetchall()]
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()


    def load_bulk_courses(self):
        try:
            # COURSE dropdown: all active courses from the master courses table.
            course_values = self.bulk_query_values(
                """
                SELECT Course_Name
                FROM courses
                WHERE Status IS NULL
                   OR LOWER(TRIM(Status)) = 'active'
                ORDER BY Course_Name
                """
            )
            self.bulk_course_combo["values"] = [str(v) for v in course_values]
            self.bulk_course_var.set("")

            # ADMISSION BATCH dropdown: all years that actually exist in student_details.
            batch_values = self.bulk_query_values(
                """
                SELECT DISTINCT Admission_Year
                FROM student_details
                WHERE Admission_Year IS NOT NULL
                ORDER BY Admission_Year DESC
                """
            )
            self.bulk_batch_combo["values"] = [str(v) for v in batch_values]
            self.bulk_batch_var.set("")

            self.bulk_semester_combo["values"] = ()
            self.bulk_semester_var.set("")

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Filter Load Error",
                str(error),
                parent=center_message_parent(self.parent)
            )

    def on_bulk_course_changed(self, event=None):
        # Admission Batch remains database-driven and fully available.
        # Semester is recalculated after Course + Batch are selected.
        self.bulk_semester_var.set("")
        self.bulk_semester_combo["values"] = ()
        self.clear_bulk_student_rows()

        if self.bulk_course_var.get().strip() and self.bulk_batch_var.get().strip():
            self.load_bulk_semesters_for_group()

    def on_bulk_batch_changed(self, event=None):
        self.bulk_semester_var.set("")
        self.bulk_semester_combo["values"] = ()
        self.clear_bulk_student_rows()

        if self.bulk_course_var.get().strip() and self.bulk_batch_var.get().strip():
            self.load_bulk_semesters_for_group()


    def load_bulk_semesters_for_group(self):
        course = self.bulk_course_var.get().strip()
        batch = self.bulk_batch_var.get().strip()

        if not course or not batch:
            self.bulk_semester_combo["values"] = ()
            return

        try:
            values = self.bulk_query_values(
                """
                SELECT DISTINCT sd.Semester
                FROM student_details AS sd
                INNER JOIN registration AS r
                    ON r.Registration_No = sd.Registration_No
                WHERE LOWER(TRIM(r.Role)) = 'student'
                  AND LOWER(TRIM(sd.Course)) = LOWER(TRIM(%s))
                  AND sd.Admission_Year = %s
                  AND sd.Semester IS NOT NULL
                ORDER BY sd.Semester
                """,
                (course, batch)
            )

            self.bulk_semester_combo["values"] = [
                f"Semester {int(v)}"
                for v in values
            ]

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Semester Load Error",
                str(error),
                parent=center_message_parent(self.parent)
            )

    def on_bulk_semester_changed(self, event=None):
        self.clear_bulk_student_rows()


    def clear_bulk_student_rows(self):
        if hasattr(self, "bulk_student_tree"):
            for item in self.bulk_student_tree.get_children():
                self.bulk_student_tree.delete(item)
        self.bulk_student_map = {}
        if hasattr(self, "bulk_count_var"):
            self.bulk_count_var.set("0 Students")


    def load_bulk_students(self):
        course = self.bulk_course_var.get().strip()
        batch = self.bulk_batch_var.get().strip()
        semester_text = self.bulk_semester_var.get().strip()

        if not course or not batch or not semester_text:
            messagebox.showwarning(
                "Select Student Group",
                "Please select Course, Admission Batch and Current Semester.",
                parent=center_message_parent(self.parent)
            )
            return

        try:
            semester = int(semester_text.replace("Semester", "").strip())
        except ValueError:
            return

        self.clear_bulk_student_rows()

        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT
                    r.Registration_No,
                    r.Name,
                    sd.Course,
                    sd.Semester,
                    sd.Admission_Year,
                    sd.Status
                FROM registration AS r
                INNER JOIN student_details AS sd
                    ON r.Registration_No = sd.Registration_No
                WHERE LOWER(TRIM(r.Role)) = 'student'
                  AND LOWER(TRIM(sd.Course)) = LOWER(TRIM(%s))
                  AND sd.Admission_Year = %s
                  AND sd.Semester = %s
                ORDER BY r.Name, r.Registration_No
                """,
                (course, batch, semester)
            )
            rows = cursor.fetchall()

            for row in rows:
                item_id = self.bulk_student_tree.insert(
                    "",
                    END,
                    values=(
                        row["Registration_No"],
                        row["Name"],
                        row["Course"],
                        f"Semester {row['Semester']}",
                        row["Admission_Year"],
                        row["Status"]
                    )
                )
                self.bulk_student_map[item_id] = {
                    "Registration_No": str(row["Registration_No"]),
                    "Name": str(row["Name"]),
                    "Course": str(row["Course"]),
                    "Semester": int(row["Semester"]),
                    "Admission_Year": str(row["Admission_Year"]),
                    "Status": str(row["Status"] or "")
                }

            count = len(rows)
            self.bulk_count_var.set(f"{count} Student" if count == 1 else f"{count} Students")
            if not rows:
                messagebox.showinfo(
                    "No Students",
                    "No students match the selected Course, Admission Batch and Current Semester.",
                    parent=center_message_parent(self.parent)
                )
        except mysql.connector.Error as error:
            messagebox.showerror("Student Load Error", str(error), parent=center_message_parent(self.parent))
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()


    def bulk_select_all(self):
        items = self.bulk_student_tree.get_children()
        if items:
            self.bulk_student_tree.selection_set(items)


    def bulk_clear_selection(self):
        self.bulk_student_tree.selection_remove(self.bulk_student_tree.selection())


    def bulk_continue_to_structure(self):
        selections = self.bulk_student_tree.selection()
        if not selections:
            messagebox.showwarning(
                "Select Students",
                "Please select at least one student.",
                parent=center_message_parent(self.parent)
            )
            return

        self.bulk_selected_students = [
            self.bulk_student_map[item]
            for item in selections
            if item in self.bulk_student_map
        ]
        if self.bulk_selected_students:
            self.show_bulk_fee_structures()


    def show_bulk_fee_structures(self):
        self.clear_page()

        self.bulk_selected_structure = None
        self.bulk_selected_components = []
        self.bulk_structure_map = {}
        self.bulk_structure_display_map = {}
        self.bulk_structure_var = StringVar(value="")

        self.page_header(
            "Select Bulk Fee Structure",
            "Choose one active fee structure matching the selected course and current semester.",
            2,
            self.show_bulk_target,
            show_progress=False
        )

        wrapper = Frame(self.page, bg=BG)
        wrapper.pack(fill=BOTH, expand=True, padx=28, pady=(0, 18))

        self.bulk_step_indicator(wrapper, 2)

        first = self.bulk_selected_students[0]

        strip = Frame(wrapper, bg=LIGHT_BLUE, highlightbackground="#BFDBFE", highlightthickness=1)
        strip.pack(fill=X, pady=(0, 10))

        Label(
            strip,
            text=(
                f"{first['Course']}   •   Admission Batch {first['Admission_Year']}   •   "
                f"Current Semester {first['Semester']}   •   {len(self.bulk_selected_students)} Selected Students"
            ),
            bg=LIGHT_BLUE,
            fg=DARK_BLUE,
            font=(FONT, 9, "bold")
        ).pack(anchor=W, padx=16, pady=11)

        card = Frame(wrapper, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill=BOTH, expand=True)

        top = Frame(card, bg=WHITE)
        top.pack(fill=X, padx=22, pady=(16, 10))

        Label(
            top,
            text="SELECT FEE STRUCTURE",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 11, "bold")
        ).pack(anchor=W)

        Label(
            top,
            text="Only active fee structures for the selected course and current semester are loaded from the database.",
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8)
        ).pack(anchor=W, pady=(4, 8))

        self.bulk_structure_combo = ttk.Combobox(
            top,
            textvariable=self.bulk_structure_var,
            state="readonly",
            font=(FONT, 10)
        )
        self.bulk_structure_combo.pack(fill=X, ipady=7)
        self.bulk_structure_combo.bind("<<ComboboxSelected>>", self.on_bulk_structure_combo_selected)

        self.bulk_detail_area = Frame(card, bg=WHITE)
        self.bulk_detail_area.pack(fill=BOTH, expand=True, padx=22, pady=(2, 10))

        placeholder = Frame(
            self.bulk_detail_area,
            bg=LIGHT_GRAY,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        placeholder.pack(fill=X)

        Label(
            placeholder,
            text="Select a fee structure from the dropdown to view its complete database fee breakdown.",
            bg=LIGHT_GRAY,
            fg=GRAY,
            font=(FONT, 9)
        ).pack(anchor=W, padx=16, pady=18)

        footer = Frame(card, bg=WHITE)
        footer.pack(fill=X, padx=22, pady=(0, 16))

        self.make_button(
            footer,
            "←  BACK TO STUDENTS",
            self.show_bulk_target,
            "secondary",
            20
        ).pack(side=LEFT)

        self.bulk_review_button = self.make_button(
            footer,
            "REVIEW ASSIGNMENT  →",
            self.show_bulk_review,
            "primary",
            22
        )
        self.bulk_review_button.pack(side=RIGHT)
        self.bulk_review_button.config(state=DISABLED, cursor="arrow")

        self.load_bulk_fee_structure_dropdown()


    def load_bulk_fee_structure_dropdown(self):
        first = self.bulk_selected_students[0]
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT
                    fs.Fee_Structure_ID,
                    fs.Course_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year,
                    fs.Status,
                    COUNT(fsc.Component_ID) AS Component_Count,
                    COALESCE(SUM(fsc.Amount), 0) AS Total_Fee
                FROM fee_structures AS fs
                INNER JOIN courses AS c
                    ON fs.Course_ID = c.Course_ID
                LEFT JOIN fee_structure_components AS fsc
                    ON fs.Fee_Structure_ID = fsc.Fee_Structure_ID
                WHERE LOWER(TRIM(c.Course_Name)) = LOWER(TRIM(%s))
                  AND fs.Semester = %s
                  AND LOWER(TRIM(fs.Status)) = 'active'
                GROUP BY
                    fs.Fee_Structure_ID,
                    fs.Course_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year,
                    fs.Status
                ORDER BY fs.Academic_Year DESC, fs.Fee_Structure_ID DESC
                """,
                (first["Course"], first["Semester"])
            )
            rows = cursor.fetchall()

            display_values = []
            for row in rows:
                data = {
                    "Fee_Structure_ID": int(row["Fee_Structure_ID"]),
                    "Course_ID": str(row["Course_ID"]),
                    "Course_Name": str(row["Course_Name"]),
                    "Semester": int(row["Semester"]),
                    "Academic_Year": str(row["Academic_Year"]),
                    "Status": str(row["Status"]),
                    "Component_Count": int(row["Component_Count"] or 0),
                    "Total_Fee": decimal_value(row["Total_Fee"])
                }
                display = (
                    f"ID {data['Fee_Structure_ID']}  |  {data['Course_Name']}  |  "
                    f"Semester {data['Semester']}  |  {data['Academic_Year']}  |  "
                    f"{money(data['Total_Fee'])}"
                )
                display_values.append(display)
                self.bulk_structure_display_map[display] = data

            self.bulk_structure_combo["values"] = display_values

            if len(display_values) == 1:
                self.bulk_structure_var.set(display_values[0])
                self.on_bulk_structure_combo_selected()
            elif not display_values:
                messagebox.showinfo(
                    "No Fee Structure",
                    "No active fee structure exists for the selected course and current semester.",
                    parent=center_message_parent(self.parent)
                )
        except mysql.connector.Error as error:
            messagebox.showerror("Fee Structure Error", str(error), parent=center_message_parent(self.parent))
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()


    def on_bulk_structure_combo_selected(self, event=None):
        display = self.bulk_structure_var.get().strip()
        self.bulk_selected_structure = self.bulk_structure_display_map.get(display)

        if self.bulk_selected_structure is None:
            self.bulk_review_button.config(state=DISABLED, cursor="arrow")
            return

        self.bulk_selected_components = self.load_fee_components(
            self.bulk_selected_structure["Fee_Structure_ID"]
        )

        clear_widgets(self.bulk_detail_area)

        detail = Frame(
            self.bulk_detail_area,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        detail.pack(fill=X)

        structure = self.bulk_selected_structure

        info = Frame(detail, bg=WHITE)
        info.pack(fill=X, padx=18, pady=(14, 10))

        info_rows = (
            ("Structure ID", structure["Fee_Structure_ID"]),
            ("Course", structure["Course_Name"]),
            ("Semester", f"Semester {structure['Semester']}"),
            ("Academic Year", structure["Academic_Year"])
        )

        for label_text, value_text in info_rows:
            row = Frame(info, bg=WHITE)
            row.pack(fill=X, pady=3)
            Label(
                row,
                text=label_text,
                bg=WHITE,
                fg=GRAY,
                width=18,
                anchor=W,
                font=(FONT, 8, "bold")
            ).pack(side=LEFT)
            Label(
                row,
                text=str(value_text),
                bg=WHITE,
                fg=TEXT,
                font=(FONT, 9, "bold")
            ).pack(side=LEFT)

        Frame(detail, bg=BORDER, height=1).pack(fill=X, padx=18, pady=4)

        breakdown = Frame(detail, bg=WHITE)
        breakdown.pack(fill=X, padx=18, pady=(8, 8))

        Label(
            breakdown,
            text="FEE BREAKDOWN",
            bg=WHITE,
            fg=GRAY,
            font=(FONT, 8, "bold")
        ).pack(anchor=W, pady=(0, 6))

        total = Decimal("0.00")
        for component in self.bulk_selected_components:
            amount = decimal_value(component["Amount"])
            total += amount
            row = Frame(breakdown, bg=WHITE)
            row.pack(fill=X, pady=3)
            Label(
                row,
                text=component["Fee_Type"],
                bg=WHITE,
                fg=TEXT_2,
                font=(FONT, 9)
            ).pack(side=LEFT)
            Label(
                row,
                text=money(amount),
                bg=WHITE,
                fg=TEXT,
                font=(FONT, 9, "bold")
            ).pack(side=RIGHT)

        total_row = Frame(detail, bg=LIGHT_BLUE)
        total_row.pack(fill=X, padx=18, pady=(4, 14))
        Label(
            total_row,
            text="TOTAL FEE",
            bg=LIGHT_BLUE,
            fg=DARK_BLUE,
            font=(FONT, 10, "bold")
        ).pack(side=LEFT, padx=14, pady=12)
        Label(
            total_row,
            text=money(total),
            bg=LIGHT_BLUE,
            fg=BLUE,
            font=(FONT, 14, "bold")
        ).pack(side=RIGHT, padx=14, pady=10)

        structure["Total_Fee"] = total

        if self.bulk_selected_components and total > 0:
            self.bulk_review_button.config(state=NORMAL, cursor="hand2")
        else:
            self.bulk_review_button.config(state=DISABLED, cursor="arrow")


    def get_bulk_assignment_preview(self):
        preview = []
        structure_id = self.bulk_selected_structure["Fee_Structure_ID"]
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            for student in self.bulk_selected_students:
                cursor.execute(
                    """
                    SELECT Student_Fee_ID
                    FROM student_fees
                    WHERE Registration_No = %s
                      AND Fee_Structure_ID = %s
                    LIMIT 1
                    """,
                    (student["Registration_No"], structure_id)
                )
                existing = cursor.fetchone()
                item = dict(student)
                item["Already_Assigned"] = existing is not None
                item["Student_Fee_ID"] = int(existing["Student_Fee_ID"]) if existing else None
                preview.append(item)
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

        return preview


    def show_bulk_review(self):
        if self.bulk_selected_structure is None:
            return

        self.bulk_preview = self.get_bulk_assignment_preview()
        self.clear_page()

        self.page_header(
            "Review Bulk Assignment",
            "Verify the fee structure and every selected student before confirming.",
            3,
            self.show_bulk_fee_structures,
            show_progress=False
        )

        wrapper = Frame(self.page, bg=BG)
        wrapper.pack(fill=BOTH, expand=True, padx=28, pady=(0, 18))
        self.bulk_step_indicator(wrapper, 3)

        structure = self.bulk_selected_structure
        selected_count = len(self.bulk_preview)
        skipped_count = sum(1 for item in self.bulk_preview if item["Already_Assigned"])
        ready_count = selected_count - skipped_count

        summary = Frame(wrapper, bg=BG)
        summary.pack(fill=X, pady=(0, 10))

        self.create_summary_card(summary, "SELECTED", str(selected_count), BLUE, LIGHT_BLUE).pack(
            side=LEFT, fill=X, expand=True, padx=(0, 6)
        )
        self.create_summary_card(summary, "READY TO ASSIGN", str(ready_count), GREEN, LIGHT_GREEN).pack(
            side=LEFT, fill=X, expand=True, padx=6
        )
        self.create_summary_card(summary, "ALREADY ASSIGNED", str(skipped_count), ORANGE, LIGHT_ORANGE).pack(
            side=LEFT, fill=X, expand=True, padx=(6, 0)
        )

        card = Frame(wrapper, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill=BOTH, expand=True)

        header = Frame(card, bg=WHITE)
        header.pack(fill=X, padx=20, pady=(14, 8))

        Label(
            header,
            text=(
                f"{structure['Course_Name']}  •  Semester {structure['Semester']}  •  "
                f"{structure['Academic_Year']}  •  {money(structure['Total_Fee'])}"
            ),
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(side=LEFT)

        self.make_button(
            header,
            "CONFIRM BULK ASSIGNMENT",
            self.confirm_bulk_assignment,
            "success",
            25
        ).pack(side=RIGHT)

        holder = Frame(card, bg=WHITE)
        holder.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

        columns = ("registration", "name", "semester", "batch", "result")
        tree = ttk.Treeview(holder, columns=columns, show="headings", style="Assign.Treeview", height=10)

        headings = {
            "registration": "REGISTRATION NO.",
            "name": "STUDENT NAME",
            "semester": "CURRENT SEMESTER",
            "batch": "ADMISSION BATCH",
            "result": "RESULT"
        }
        widths = {
            "registration": 150,
            "name": 220,
            "semester": 130,
            "batch": 130,
            "result": 230
        }

        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, width=widths[col], anchor=W if col in ("registration", "name", "result") else CENTER)

        scroll = Scrollbar(holder, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)

        for student in self.bulk_preview:
            tree.insert(
                "",
                END,
                values=(
                    student["Registration_No"],
                    student["Name"],
                    f"Semester {student['Semester']}",
                    student["Admission_Year"],
                    "ALREADY ASSIGNED - WILL SKIP" if student["Already_Assigned"] else "READY TO ASSIGN"
                )
            )

        footer = Frame(card, bg=WHITE)
        footer.pack(fill=X, padx=20, pady=(0, 14))
        self.make_button(
            footer,
            "←  BACK TO FEE STRUCTURE",
            self.show_bulk_fee_structures,
            "secondary",
            24
        ).pack(side=LEFT)


    def confirm_bulk_assignment(self):
        structure = self.bulk_selected_structure
        total_fee = decimal_value(structure["Total_Fee"])

        if total_fee <= 0:
            messagebox.showerror(
                "Invalid Fee",
                "The selected fee structure total must be greater than zero.",
                parent=center_message_parent(self.parent)
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Bulk Assignment",
            (
                f"Assign this fee to eligible selected students?\n\n"
                f"Course: {structure['Course_Name']}\n"
                f"Semester: {structure['Semester']}\n"
                f"Academic Year: {structure['Academic_Year']}\n"
                f"Fee per Student: {money(total_fee)}\n"
                f"Selected Students: {len(self.bulk_selected_students)}\n\n"
                "Existing identical assignments will be skipped."
            ),
            parent=center_message_parent(self.parent)
        )
        if not confirm:
            return

        connection = None
        cursor = None
        assigned = []
        skipped = []

        try:
            connection = get_connection()
            connection.start_transaction()
            cursor = connection.cursor(dictionary=True)

            for student in self.bulk_selected_students:
                cursor.execute(
                    """
                    SELECT Student_Fee_ID
                    FROM student_fees
                    WHERE Registration_No = %s
                      AND Fee_Structure_ID = %s
                    LIMIT 1
                    FOR UPDATE
                    """,
                    (student["Registration_No"], structure["Fee_Structure_ID"])
                )
                existing = cursor.fetchone()

                if existing:
                    skipped.append({**student, "Reason": "Fee structure already assigned."})
                    continue

                cursor.execute(
                    """
                    INSERT INTO student_fees
                    (
                        Registration_No,
                        Fee_Structure_ID,
                        Total_Fee,
                        Amount_Paid,
                        Due_Amount,
                        Payment_Status
                    )
                    VALUES (%s, %s, %s, 0.00, %s, 'Unpaid')
                    """,
                    (
                        student["Registration_No"],
                        structure["Fee_Structure_ID"],
                        total_fee,
                        total_fee
                    )
                )
                assigned.append({**student, "Student_Fee_ID": cursor.lastrowid})

            connection.commit()

        except mysql.connector.Error as error:
            if connection is not None:
                try:
                    connection.rollback()
                except Exception:
                    pass
            messagebox.showerror("Bulk Assignment Error", str(error), parent=center_message_parent(self.parent))
            return
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

        self.bulk_result = {
            "Selected": len(self.bulk_selected_students),
            "Assigned": assigned,
            "Skipped": skipped
        }
        self.show_bulk_result()


    def show_bulk_result(self):
        self.clear_page()

        self.page_header(
            "Bulk Assignment Complete",
            "The semester fee assignment process has finished.",
            4,
            show_progress=False
        )

        wrapper = Frame(self.page, bg=BG)
        wrapper.pack(fill=BOTH, expand=True, padx=28, pady=(0, 18))
        self.bulk_step_indicator(wrapper, 4)

        result = self.bulk_result

        summary = Frame(wrapper, bg=BG)
        summary.pack(fill=X, pady=(0, 12))

        self.create_summary_card(summary, "SELECTED", str(result["Selected"]), BLUE, LIGHT_BLUE).pack(
            side=LEFT, fill=X, expand=True, padx=(0, 6)
        )
        self.create_summary_card(summary, "ASSIGNED", str(len(result["Assigned"])), GREEN, LIGHT_GREEN).pack(
            side=LEFT, fill=X, expand=True, padx=6
        )
        self.create_summary_card(summary, "SKIPPED", str(len(result["Skipped"])), ORANGE, LIGHT_ORANGE).pack(
            side=LEFT, fill=X, expand=True, padx=(6, 0)
        )

        card = Frame(wrapper, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill=BOTH, expand=True)

        Label(
            card,
            text="ASSIGNMENT COMPLETED SUCCESSFULLY",
            bg=WHITE,
            fg=GREEN,
            font=(FONT, 13, "bold")
        ).pack(anchor=W, padx=22, pady=(22, 8))

        Label(
            card,
            text=(
                f"{len(result['Assigned'])} new fee assignment(s) created. "
                f"{len(result['Skipped'])} existing assignment(s) skipped."
            ),
            bg=WHITE,
            fg=TEXT_2,
            font=(FONT, 9)
        ).pack(anchor=W, padx=22)

        footer = Frame(card, bg=WHITE)
        footer.pack(fill=X, padx=22, pady=22)

        self.make_button(
            footer,
            "ASSIGN ANOTHER BATCH",
            self.show_bulk_target,
            "primary",
            22
        ).pack(side=LEFT)

        self.make_button(
            footer,
            "BACK TO ASSIGN FEES",
            self.show_assign_mode,
            "secondary",
            20
        ).pack(side=RIGHT)

def open_assign_fees_page(
    parent,
    user_role="Accountant",
    current_user_name="",
    current_user_id=""
):
    return AssignFeesPage(
        parent=parent,
        user_role=user_role,
        current_user_name=current_user_name,
        current_user_id=current_user_id
    )


# Optional alias if another file uses this name.
def show_assign_fees_page(
    parent,
    user_role="Accountant",
    current_user_name="",
    current_user_id=""
):
    return open_assign_fees_page(
        parent=parent,
        user_role=user_role,
        current_user_name=current_user_name,
        current_user_id=current_user_id
    )


# ============================================================
# STANDALONE TEST
# This block does not run when imported by the dashboard.
# ============================================================

if __name__ == "__main__":
    root = Tk()
    root.title("Assign Fees - Standalone Test")
    root.geometry("1280x820+40+20")
    root.minsize(1050, 700)
    root.configure(bg=BG)

    open_assign_fees_page(
        parent=root,
        user_role="Accountant",
        current_user_name="Debananda Kuanr",
        current_user_id="ACC0001"
    )

    root.mainloop()
