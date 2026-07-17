from tkinter import *
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import date
from PIL import Image, ImageDraw, ImageFont
import os
import sys
import shutil
import subprocess


# ============================================================
# FILE:
# ACCOUNTANT/student_fees_page.py
#
# PURPOSE:
# This module loads the Student Fees page inside the
# Accountant Dashboard content frame.
#
# It does NOT create another Tk() main window.
# ============================================================


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
DARK_BLUE = "#1D4ED8"
LIGHT_BLUE = "#EFF6FF"

GREEN = "#16A34A"
LIGHT_GREEN = "#F0FDF4"

ORANGE = "#EA580C"
LIGHT_ORANGE = "#FFF7ED"

RED = "#DC2626"
LIGHT_RED = "#FEF2F2"

PURPLE = "#7C3AED"
LIGHT_PURPLE = "#F5F3FF"

WHITE = "#FFFFFF"
BG = "#F8FAFC"

TEXT = "#0F172A"
GRAY = "#64748B"

BORDER = "#E2E8F0"
LIGHT_BORDER = "#F1F5F9"


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


# ============================================================
# MONEY FORMAT
# ============================================================

def money(value):

    try:

        return f"₹{float(value):,.2f}"

    except (
        TypeError,
        ValueError
    ):

        return "₹0.00"


# ============================================================
# STUDENT FEES PAGE CLASS
# ============================================================

class StudentFeesPage:

    def __init__(
        self,
        parent,
        status_filter="All",
        refresh_dashboard_callback=None,
        collector_name=None
    ):

        self.parent = parent

        self.initial_status_filter = (
            status_filter
            if status_filter
            else "All"
        )

        self.refresh_dashboard_callback = (
            refresh_dashboard_callback
        )

        # ====================================================
        # LOGGED-IN ACCOUNTANT / PAYMENT COLLECTOR
        #
        # Final database value:
        # Debananda Kuanr - ACC0001
        #
        # This page can receive either:
        # 1. collector_name="Debananda Kuanr - ACC0001"
        # 2. collector_name="Debananda Kuanr"
        # 3. collector_name="ACC0001"
        # 4. no collector_name, while accountant_dashboard.py
        #    was opened with:
        #       sys.argv[1] = Registration_No
        #       sys.argv[2] = Name
        #       sys.argv[3] = Username
        #
        # The code verifies the accountant from the
        # registration table before storing Collected_By.
        # ====================================================

        self.collector_name = (
            self.resolve_collector_name(
                collector_name
            )
        )

        self.search_var = StringVar()

        self.status_var = StringVar(
            value=self.initial_status_filter
        )

        self.course_var = StringVar(
            value="All Courses"
        )

        self.semester_var = StringVar(
            value="All Semesters"
        )

        self.record_count_var = StringVar(
            value="0 Records"
        )

        self.tree = None

        self.build_page()

        self.load_filter_values()

        self.load_student_fees()


    # ========================================================
    # RESOLVE LOGGED-IN ACCOUNTANT
    # ========================================================

    def resolve_collector_name(
        self,
        collector_name=None
    ):

        passed_value = (
            str(
                collector_name
            ).strip()
            if collector_name is not None
            else ""
        )


        argv_registration_no = ""
        argv_name = ""
        argv_username = ""


        if len(
            sys.argv
        ) >= 2:

            argv_registration_no = str(
                sys.argv[1]
            ).strip()


        if len(
            sys.argv
        ) >= 3:

            argv_name = str(
                sys.argv[2]
            ).strip()


        if len(
            sys.argv
        ) >= 4:

            argv_username = str(
                sys.argv[3]
            ).strip()


        # ----------------------------------------------------
        # If a complete "Name - ID" value was explicitly
        # passed, verify and normalize it when possible.
        # ----------------------------------------------------

        explicit_name = ""
        explicit_id = ""


        if (
            passed_value
            and
            " - " in passed_value
        ):

            parts = passed_value.rsplit(
                " - ",
                1
            )


            if len(
                parts
            ) == 2:

                explicit_name = (
                    parts[0].strip()
                )

                explicit_id = (
                    parts[1].strip()
                )


        # ----------------------------------------------------
        # BUILD SEARCH VALUES
        # ----------------------------------------------------

        registration_candidates = []


        for value in (
            explicit_id,
            argv_registration_no
        ):

            if (
                value
                and
                value.lower() != "accountant"
                and
                value not in registration_candidates
            ):

                registration_candidates.append(
                    value
                )


        username_candidates = []


        for value in (
            argv_username,
            passed_value
        ):

            if (
                value
                and
                value.lower() != "accountant"
                and
                " - " not in value
                and
                value not in username_candidates
            ):

                username_candidates.append(
                    value
                )


        name_candidates = []


        for value in (
            explicit_name,
            argv_name,
            passed_value
        ):

            if (
                value
                and
                value.lower() != "accountant"
                and
                " - " not in value
                and
                value not in name_candidates
            ):

                name_candidates.append(
                    value
                )


        # ----------------------------------------------------
        # VERIFY ACCOUNTANT FROM DATABASE
        # ----------------------------------------------------

        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor(
                dictionary=True
            )


            # Search first by Registration_No because it is
            # the unique accountant ID.
            for registration_no in registration_candidates:

                cursor.execute(
                    """
                    SELECT
                        Registration_No,
                        Name,
                        Username,
                        Role

                    FROM registration

                    WHERE
                        Registration_No = %s
                        AND
                        LOWER(TRIM(Role)) = 'accountant'

                    LIMIT 1
                    """,
                    (
                        registration_no,
                    )
                )


                row = cursor.fetchone()


                if row:

                    return (
                        f"{str(row['Name']).strip()} - "
                        f"{str(row['Registration_No']).strip()}"
                    )


            # Search by Username.
            for username in username_candidates:

                cursor.execute(
                    """
                    SELECT
                        Registration_No,
                        Name,
                        Username,
                        Role

                    FROM registration

                    WHERE
                        Username = %s
                        AND
                        LOWER(TRIM(Role)) = 'accountant'

                    LIMIT 1
                    """,
                    (
                        username,
                    )
                )


                row = cursor.fetchone()


                if row:

                    return (
                        f"{str(row['Name']).strip()} - "
                        f"{str(row['Registration_No']).strip()}"
                    )


            # Search by exact accountant Name.
            for accountant_name in name_candidates:

                cursor.execute(
                    """
                    SELECT
                        Registration_No,
                        Name,
                        Username,
                        Role

                    FROM registration

                    WHERE
                        Name = %s
                        AND
                        LOWER(TRIM(Role)) = 'accountant'

                    LIMIT 1
                    """,
                    (
                        accountant_name,
                    )
                )


                row = cursor.fetchone()


                if row:

                    return (
                        f"{str(row['Name']).strip()} - "
                        f"{str(row['Registration_No']).strip()}"
                    )


        except mysql.connector.Error:

            # Do not stop the Student Fees page only because
            # collector verification failed. Use the safe
            # fallback values below.
            pass


        finally:

            try:

                if cursor is not None:

                    cursor.close()

            except Exception:

                pass


            try:

                if (
                    con is not None
                    and
                    con.is_connected()
                ):

                    con.close()

            except Exception:

                pass


        # ----------------------------------------------------
        # SAFE FALLBACKS
        # ----------------------------------------------------

        if (
            explicit_name
            and
            explicit_id
        ):

            return (
                f"{explicit_name} - "
                f"{explicit_id}"
            )


        if (
            argv_name
            and
            argv_registration_no
        ):

            return (
                f"{argv_name} - "
                f"{argv_registration_no}"
            )


        if (
            passed_value
            and
            argv_registration_no
            and
            passed_value.lower() != "accountant"
        ):

            return (
                f"{passed_value} - "
                f"{argv_registration_no}"
            )


        if passed_value:

            return passed_value


        return "Accountant"


    # ========================================================
    # BUILD PAGE
    # ========================================================

    def build_page(self):

        # ----------------------------------------------------
        # MAIN WRAPPER
        # ----------------------------------------------------

        self.wrapper = Frame(
            self.parent,
            bg=BG
        )

        self.wrapper.pack(
            fill=BOTH,
            expand=True,
            padx=24,
            pady=20
        )


        # ====================================================
        # PAGE INTRODUCTION
        # ====================================================

        intro_frame = Frame(
            self.wrapper,
            bg=BG
        )

        intro_frame.pack(
            fill=X,
            pady=(0, 14)
        )


        Label(
            intro_frame,
            text="STUDENT FEE MANAGEMENT",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                15,
                "bold"
            )
        ).pack(
            anchor="w"
        )


        Label(
            intro_frame,
            text=(
                "Search students, view assigned fees, "
                "check payment status and record payments."
            ),
            bg=BG,
            fg=GRAY,
            font=(
                "Helvetica",
                9
            )
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


        # ====================================================
        # SEARCH AND FILTER CARD
        # ====================================================

        filter_card = Frame(
            self.wrapper,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        filter_card.pack(
            fill=X,
            pady=(0, 16)
        )


        # ----------------------------------------------------
        # FILTER TITLE
        # ----------------------------------------------------

        Label(
            filter_card,
            text="SEARCH & FILTER",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 10)
        )


        # ----------------------------------------------------
        # SEARCH ROW
        # ----------------------------------------------------

        search_row = Frame(
            filter_card,
            bg=WHITE
        )

        search_row.pack(
            fill=X,
            padx=18,
            pady=(0, 12)
        )


        search_entry = Entry(
            search_row,
            textvariable=self.search_var,
            bg=WHITE,
            fg=TEXT,
            insertbackground=TEXT,
            font=(
                "Helvetica",
                10
            ),
            relief=SOLID,
            bd=1
        )

        search_entry.pack(
            side=LEFT,
            fill=X,
            expand=True,
            ipady=9
        )


        Button(
            search_row,
            text="SEARCH",
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=self.load_student_fees
        ).pack(
            side=LEFT,
            padx=(10, 0),
            ipadx=22,
            ipady=9
        )


        search_entry.bind(
            "<Return>",
            lambda event:
            self.load_student_fees()
        )


        # ----------------------------------------------------
        # FILTER ROW
        # ----------------------------------------------------

        filter_row = Frame(
            filter_card,
            bg=WHITE
        )

        filter_row.pack(
            fill=X,
            padx=18,
            pady=(0, 16)
        )


        # ----------------------------------------------------
        # STATUS FILTER
        # ----------------------------------------------------

        status_group = Frame(
            filter_row,
            bg=WHITE
        )

        status_group.pack(
            side=LEFT,
            padx=(0, 14)
        )


        Label(
            status_group,
            text="Status",
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                8,
                "bold"
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )


        self.status_combo = ttk.Combobox(
            status_group,
            textvariable=self.status_var,
            state="readonly",
            values=(
                "All",
                "Paid",
                "Partial",
                "Unpaid",
                "Due"
            ),
            width=16
        )

        self.status_combo.pack(
            ipady=5
        )


        self.status_combo.bind(
            "<<ComboboxSelected>>",
            lambda event:
            self.load_student_fees()
        )


        # ----------------------------------------------------
        # COURSE FILTER
        # ----------------------------------------------------

        course_group = Frame(
            filter_row,
            bg=WHITE
        )

        course_group.pack(
            side=LEFT,
            padx=(0, 14)
        )


        Label(
            course_group,
            text="Course",
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                8,
                "bold"
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )


        self.course_combo = ttk.Combobox(
            course_group,
            textvariable=self.course_var,
            state="readonly",
            values=(
                "All Courses",
            ),
            width=28
        )

        self.course_combo.pack(
            ipady=5
        )


        self.course_combo.bind(
            "<<ComboboxSelected>>",
            lambda event:
            self.load_student_fees()
        )


        # ----------------------------------------------------
        # SEMESTER FILTER
        # ----------------------------------------------------

        semester_group = Frame(
            filter_row,
            bg=WHITE
        )

        semester_group.pack(
            side=LEFT
        )


        Label(
            semester_group,
            text="Semester",
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                8,
                "bold"
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )


        self.semester_combo = ttk.Combobox(
            semester_group,
            textvariable=self.semester_var,
            state="readonly",
            values=(
                "All Semesters",
            ),
            width=18
        )

        self.semester_combo.pack(
            ipady=5
        )


        self.semester_combo.bind(
            "<<ComboboxSelected>>",
            lambda event:
            self.load_student_fees()
        )


        # ----------------------------------------------------
        # CLEAR FILTER BUTTON
        # ----------------------------------------------------

        Button(
            filter_row,
            text="CLEAR FILTER",
            bg="#F1F5F9",
            fg=TEXT,
            activebackground="#E2E8F0",
            activeforeground=TEXT,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                8,
                "bold"
            ),
            command=self.clear_filters
        ).pack(
            side=RIGHT,
            pady=(20, 0),
            ipadx=15,
            ipady=8
        )


        # ====================================================
        # STUDENT RECORDS CARD
        # ====================================================

        records_card = Frame(
            self.wrapper,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        records_card.pack(
            fill=BOTH,
            expand=True
        )


        # ----------------------------------------------------
        # RECORDS HEADER
        # ----------------------------------------------------

        records_header = Frame(
            records_card,
            bg=WHITE
        )

        records_header.pack(
            fill=X,
            padx=18,
            pady=(15, 10)
        )


        header_left = Frame(
            records_header,
            bg=WHITE
        )

        header_left.pack(
            side=LEFT
        )


        Label(
            header_left,
            text="STUDENT FEE RECORDS",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                11,
                "bold"
            )
        ).pack(
            anchor="w"
        )


        Label(
            header_left,
            text=(
                "One row represents one student. Single-click to view "
                "all assigned semester fees together."
            ),
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                8
            )
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


        # ----------------------------------------------------
        # HEADER ACTIONS
        # ----------------------------------------------------

        header_actions = Frame(
            records_header,
            bg=WHITE
        )

        header_actions.pack(
            side=RIGHT
        )


        Button(
            header_actions,
            text="+ ADD PAYMENT",
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                8,
                "bold"
            ),
            command=self.record_payment_for_selected
        ).pack(
            side=LEFT,
            padx=(0, 10),
            ipadx=14,
            ipady=7
        )


        Label(
            header_actions,
            textvariable=self.record_count_var,
            bg=LIGHT_BLUE,
            fg=BLUE,
            font=(
                "Helvetica",
                8,
                "bold"
            ),
            padx=12,
            pady=6
        ).pack(
            side=LEFT
        )


        # ====================================================
        # TREEVIEW STYLE
        # ====================================================

        style = ttk.Style()


        try:

            style.theme_use(
                "clam"
            )

        except TclError:

            pass


        style.configure(
            "StudentFees.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=40,
            borderwidth=0,
            font=(
                "Helvetica",
                8
            )
        )


        style.configure(
            "StudentFees.Treeview.Heading",
            background="#F8FAFC",
            foreground=GRAY,
            borderwidth=0,
            relief=FLAT,
            font=(
                "Helvetica",
                7,
                "bold"
            )
        )


        style.map(
            "StudentFees.Treeview",
            background=[
                (
                    "selected",
                    LIGHT_BLUE
                )
            ],
            foreground=[
                (
                    "selected",
                    TEXT
                )
            ]
        )


        # ====================================================
        # TABLE
        # ====================================================

        table_frame = Frame(
            records_card,
            bg=WHITE
        )

        table_frame.pack(
            fill=BOTH,
            expand=True,
            padx=18,
            pady=(0, 16)
        )


        columns = (
            "registration",
            "student",
            "course",
            "semester",
            "total",
            "paid",
            "due",
            "status"
        )


        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="StudentFees.Treeview",
            selectmode="browse"
        )


        # ----------------------------------------------------
        # HEADINGS
        # ----------------------------------------------------

        self.tree.heading(
            "registration",
            text="REG. NO."
        )

        self.tree.heading(
            "student",
            text="STUDENT NAME"
        )

        self.tree.heading(
            "course",
            text="COURSE"
        )

        self.tree.heading(
            "semester",
            text="CURRENT SEM / FEES"
        )

        self.tree.heading(
            "total",
            text="TOTAL FEE"
        )

        self.tree.heading(
            "paid",
            text="PAID"
        )

        self.tree.heading(
            "due",
            text="DUE"
        )

        self.tree.heading(
            "status",
            text="STATUS"
        )


        # ----------------------------------------------------
        # COLUMN WIDTHS
        # ----------------------------------------------------

        self.tree.column(
            "registration",
            width=120,
            minwidth=100,
            anchor=CENTER
        )

        self.tree.column(
            "student",
            width=190,
            minwidth=150,
            anchor=W
        )

        self.tree.column(
            "course",
            width=210,
            minwidth=150,
            anchor=W
        )

        self.tree.column(
            "semester",
            width=125,
            minwidth=110,
            anchor=CENTER
        )

        self.tree.column(
            "total",
            width=125,
            minwidth=100,
            anchor=E
        )

        self.tree.column(
            "paid",
            width=125,
            minwidth=100,
            anchor=E
        )

        self.tree.column(
            "due",
            width=125,
            minwidth=100,
            anchor=E
        )

        self.tree.column(
            "status",
            width=100,
            minwidth=90,
            anchor=CENTER
        )


        # ----------------------------------------------------
        # SCROLLBARS
        # ----------------------------------------------------

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient=VERTICAL,
            command=self.tree.yview
        )


        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient=HORIZONTAL,
            command=self.tree.xview
        )


        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )


        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )


        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )


        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )


        table_frame.grid_rowconfigure(
            0,
            weight=1
        )


        table_frame.grid_columnconfigure(
            0,
            weight=1
        )


        # ----------------------------------------------------
        # SINGLE CLICK
        # ----------------------------------------------------

        self.tree.bind(
            "<ButtonRelease-1>",
            self.on_student_click
        )


    # ========================================================
    # LOAD FILTER VALUES
    # ========================================================

    def load_filter_values(self):

        con = None

        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()


            # ------------------------------------------------
            # COURSES
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT DISTINCT
                    Course

                FROM student_details

                WHERE
                    Course IS NOT NULL
                    AND
                    TRIM(Course) <> ''

                ORDER BY Course
                """
            )


            courses = [
                str(row[0]).strip()
                for row in cursor.fetchall()
                if row[0] is not None
            ]


            self.course_combo[
                "values"
            ] = (
                ["All Courses"]
                +
                courses
            )


            # ------------------------------------------------
            # SEMESTERS
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT DISTINCT
                    Semester

                FROM student_details

                WHERE
                    Semester IS NOT NULL

                ORDER BY Semester
                """
            )


            semesters = [
                str(row[0])
                for row in cursor.fetchall()
                if row[0] is not None
            ]


            self.semester_combo[
                "values"
            ] = (
                ["All Semesters"]
                +
                semesters
            )


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load filter values."
                    f"\n\n{error}"
                ),
                parent=self.parent.winfo_toplevel()
            )


        finally:

            if cursor is not None:

                cursor.close()


            if (
                con is not None
                and con.is_connected()
            ):

                con.close()


    # ========================================================
    # CLEAR FILTERS
    # ========================================================

    def clear_filters(self):

        self.search_var.set(
            ""
        )

        self.status_var.set(
            "All"
        )

        self.course_var.set(
            "All Courses"
        )

        self.semester_var.set(
            "All Semesters"
        )

        self.load_student_fees()


    # ========================================================
    # LOAD STUDENT FEES
    # ========================================================

    def load_student_fees(self):

        # One table row = one student.
        # All fee structures assigned to that student are aggregated here.
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = self.search_var.get().strip()
        status_filter = self.status_var.get().strip()
        course_filter = self.course_var.get().strip()
        semester_filter = self.semester_var.get().strip()

        con = None
        cursor = None

        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)

            query = """
            SELECT
                sf.Registration_No,
                r.Name,
                sd.Course,
                sd.Semester AS Current_Semester,
                COUNT(sf.Student_Fee_ID) AS Fee_Structure_Count,
                COALESCE(SUM(sf.Total_Fee), 0) AS Total_Fee,
                COALESCE(SUM(sf.Amount_Paid), 0) AS Amount_Paid,
                COALESCE(SUM(sf.Due_Amount), 0) AS Due_Amount,
                CASE
                    WHEN COALESCE(SUM(sf.Due_Amount), 0) <= 0 THEN 'Paid'
                    WHEN COALESCE(SUM(sf.Amount_Paid), 0) > 0 THEN 'Partial'
                    ELSE 'Unpaid'
                END AS Payment_Status
            FROM student_fees sf
            INNER JOIN registration r
                ON r.Registration_No = sf.Registration_No
            LEFT JOIN student_details sd
                ON sd.Registration_No = sf.Registration_No
            INNER JOIN fee_structures fs
                ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
            WHERE 1 = 1
            """

            values = []

            if search_text:
                query += """
                AND (
                    sf.Registration_No LIKE %s
                    OR r.Name LIKE %s
                    OR sd.Course LIKE %s
                )
                """
                search_value = f"%{search_text}%"
                values.extend([search_value, search_value, search_value])

            if course_filter and course_filter != "All Courses":
                query += " AND sd.Course = %s "
                values.append(course_filter)

            # Filter by the semester of the assigned fee structure,
            # not only by the student's current semester.
            if semester_filter and semester_filter != "All Semesters":
                query += " AND fs.Semester = %s "
                values.append(semester_filter)

            query += """
            GROUP BY
                sf.Registration_No,
                r.Name,
                sd.Course,
                sd.Semester
            """

            if status_filter == "Paid":
                query += " HAVING COALESCE(SUM(sf.Due_Amount), 0) <= 0 "
            elif status_filter == "Partial":
                query += """
                HAVING
                    COALESCE(SUM(sf.Amount_Paid), 0) > 0
                    AND COALESCE(SUM(sf.Due_Amount), 0) > 0
                """
            elif status_filter == "Unpaid":
                query += " HAVING COALESCE(SUM(sf.Amount_Paid), 0) <= 0 "
            elif status_filter == "Due":
                query += " HAVING COALESCE(SUM(sf.Due_Amount), 0) > 0 "

            query += " ORDER BY r.Name ASC "

            cursor.execute(query, tuple(values))
            records = cursor.fetchall()

            for record in records:
                reg_no = str(record["Registration_No"])

                # Keep the existing 8-column table layout.
                # The SEM column now shows current semester plus assignment count.
                semester_text = (
                    f"{record['Current_Semester']}  ({record['Fee_Structure_Count']} fees)"
                    if record["Current_Semester"] is not None
                    else f"-  ({record['Fee_Structure_Count']} fees)"
                )

                self.tree.insert(
                    "",
                    END,
                    iid=reg_no,
                    values=(
                        reg_no,
                        record["Name"],
                        record["Course"] or "-",
                        semester_text,
                        money(record["Total_Fee"]),
                        money(record["Amount_Paid"]),
                        money(record["Due_Amount"]),
                        record["Payment_Status"]
                    )
                )

            count = len(records)
            self.record_count_var.set(
                "1 Student" if count == 1 else f"{count} Students"
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load student fees.\n\n{error}",
                parent=self.parent.winfo_toplevel()
            )

        finally:
            if cursor is not None:
                cursor.close()

            if con is not None and con.is_connected():
                con.close()

    def record_payment_for_selected(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Student",
                "Please select a student from the table first.",
                parent=self.parent.winfo_toplevel()
            )
            return

        registration_no = str(selected[0]).strip()

        # Open the combined student fee panel.
        # The accountant can choose the exact semester/fee structure
        # and record payment against that assignment.
        self.open_student_fee_details(registration_no)

    def on_student_click(
        self,
        event
    ):

        region = self.tree.identify_region(event.x, event.y)

        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)

        if not row_id:
            return

        self.tree.selection_set(row_id)
        self.open_student_fee_details(str(row_id))

    def get_student_fee_details(
        self,
        student_fee_id
    ):

        # Kept for payment/receipt compatibility:
        # this method still returns one exact Student_Fee_ID.
        con = None
        cursor = None

        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    sf.Student_Fee_ID,
                    sf.Registration_No,
                    sf.Fee_Structure_ID,
                    sf.Total_Fee,
                    sf.Amount_Paid,
                    sf.Due_Amount,
                    sf.Payment_Status,
                    r.Name,
                    sd.Course,
                    sd.Semester,
                    fs.Semester AS Fee_Semester,
                    fs.Academic_Year
                FROM student_fees sf
                INNER JOIN registration r
                    ON r.Registration_No = sf.Registration_No
                LEFT JOIN student_details sd
                    ON sd.Registration_No = sf.Registration_No
                INNER JOIN fee_structures fs
                    ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
                WHERE sf.Student_Fee_ID = %s
                LIMIT 1
                """,
                (student_fee_id,)
            )

            return cursor.fetchone()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load student fee details.\n\n{error}",
                parent=self.parent.winfo_toplevel()
            )
            return None

        finally:
            if cursor is not None:
                cursor.close()

            if con is not None and con.is_connected():
                con.close()

    def get_all_student_fee_assignments(
        self,
        registration_no
    ):

        con = None
        cursor = None

        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    sf.Student_Fee_ID,
                    sf.Registration_No,
                    sf.Fee_Structure_ID,
                    sf.Total_Fee,
                    sf.Amount_Paid,
                    sf.Due_Amount,
                    sf.Payment_Status,
                    sf.Assigned_At,
                    r.Name,
                    sd.Course,
                    sd.Semester AS Current_Semester,
                    fs.Semester AS Fee_Semester,
                    fs.Academic_Year
                FROM student_fees sf
                INNER JOIN registration r
                    ON r.Registration_No = sf.Registration_No
                LEFT JOIN student_details sd
                    ON sd.Registration_No = sf.Registration_No
                INNER JOIN fee_structures fs
                    ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
                WHERE sf.Registration_No = %s
                ORDER BY
                    fs.Semester ASC,
                    fs.Academic_Year ASC,
                    sf.Student_Fee_ID ASC
                """,
                (registration_no,)
            )

            return cursor.fetchall()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load all assigned fees.\n\n{error}",
                parent=self.parent.winfo_toplevel()
            )
            return []

        finally:
            if cursor is not None:
                cursor.close()

            if con is not None and con.is_connected():
                con.close()

    def get_fee_components(
        self,
        fee_structure_id
    ):

        con = None

        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor(
                dictionary=True
            )


            cursor.execute(
                """
                SELECT

                    Fee_Type,

                    Amount

                FROM fee_structure_components

                WHERE
                    Fee_Structure_ID = %s

                ORDER BY
                    Component_ID ASC
                """,
                (
                    fee_structure_id,
                )
            )


            return cursor.fetchall()


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load fee components."
                    f"\n\n{error}"
                ),
                parent=self.parent.winfo_toplevel()
            )


            return []


        finally:

            if cursor is not None:

                cursor.close()


            if (
                con is not None
                and con.is_connected()
            ):

                con.close()


    # ========================================================
    # CENTER WINDOW
    # ========================================================

    def center_window(
        self,
        child,
        width,
        height
    ):

        child.update_idletasks()


        parent_window = (
            self.parent.winfo_toplevel()
        )


        parent_window.update_idletasks()


        parent_x = (
            parent_window.winfo_rootx()
        )

        parent_y = (
            parent_window.winfo_rooty()
        )

        parent_width = (
            parent_window.winfo_width()
        )

        parent_height = (
            parent_window.winfo_height()
        )


        x = (
            parent_x
            +
            (
                parent_width
                -
                width
            )
            //
            2
        )


        y = (
            parent_y
            +
            (
                parent_height
                -
                height
            )
            //
            2
        )


        child.geometry(
            f"{width}x{height}+{x}+{y}"
        )


    # ========================================================
    # CREATE SUMMARY BOX
    # ========================================================

    def create_summary_box(
        self,
        parent,
        title,
        value,
        background,
        foreground
    ):

        box = Frame(
            parent,
            bg=background,
            highlightbackground=BORDER,
            highlightthickness=1
        )


        Label(
            box,
            text=title,
            bg=background,
            fg=GRAY,
            font=(
                "Helvetica",
                8,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=14,
            pady=(12, 5)
        )


        Label(
            box,
            text=value,
            bg=background,
            fg=foreground,
            font=(
                "Helvetica",
                15,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=14,
            pady=(0, 13)
        )


        return box


    # ========================================================
    # OPEN STUDENT FEE DETAILS
    # ========================================================

    def open_student_fee_details(
        self,
        registration_no
    ):

        assignments = self.get_all_student_fee_assignments(
            registration_no
        )

        if not assignments:
            return

        first = assignments[0]

        total_fee = sum(float(row["Total_Fee"] or 0) for row in assignments)
        total_paid = sum(float(row["Amount_Paid"] or 0) for row in assignments)
        total_due = sum(float(row["Due_Amount"] or 0) for row in assignments)

        details_window = Toplevel(self.parent)
        details_window.title("Student Fee Details")
        details_window.configure(bg=BG)
        details_window.resizable(True, True)
        details_window.transient(self.parent.winfo_toplevel())
        details_window.grab_set()

        self.center_window(
            details_window,
            920,
            720
        )

        # ====================================================
        # HEADER
        # ====================================================

        header = Frame(
            details_window,
            bg=WHITE,
            height=78
        )
        header.pack(fill=X)
        header.pack_propagate(False)

        Label(
            header,
            text="STUDENT FEE DETAILS",
            bg=WHITE,
            fg=TEXT,
            font=("Helvetica", 15, "bold")
        ).place(x=22, y=15)

        Label(
            header,
            text=(
                "All assigned semester fee structures are shown "
                "together for this student."
            ),
            bg=WHITE,
            fg=GRAY,
            font=("Helvetica", 8)
        ).place(x=22, y=45)

        Button(
            header,
            text="CLOSE",
            bg=RED,
            fg=WHITE,
            activebackground="#B91C1C",
            activeforeground=WHITE,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=("Helvetica", 8, "bold"),
            command=details_window.destroy
        ).pack(
            side=RIGHT,
            padx=20,
            pady=20,
            ipadx=16,
            ipady=7
        )

        # ====================================================
        # SCROLLABLE BODY
        # ====================================================

        outer = Frame(details_window, bg=BG)
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

        body.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=body,
            anchor="nw"
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                canvas_window,
                width=event.width
            )
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # ====================================================
        # STUDENT INFO
        # ====================================================

        student_card = Frame(
            body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        student_card.pack(
            fill=X,
            padx=20,
            pady=(18, 12)
        )

        Label(
            student_card,
            text=first["Name"],
            bg=WHITE,
            fg=TEXT,
            font=("Helvetica", 15, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 3)
        )

        Label(
            student_card,
            text=(
                f"{first['Registration_No']}  •  "
                f"{first['Course'] or '-'}  •  "
                f"Current Semester {first['Current_Semester'] or '-'}  •  "
                f"{len(assignments)} Assigned Fee Structure"
                f"{'' if len(assignments) == 1 else 's'}"
            ),
            bg=WHITE,
            fg=GRAY,
            font=("Helvetica", 8)
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 14)
        )

        # ====================================================
        # COMBINED TOTALS
        # ====================================================

        summary_frame = Frame(body, bg=BG)
        summary_frame.pack(
            fill=X,
            padx=20,
            pady=(0, 12)
        )

        for column in range(3):
            summary_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="combined_summary"
            )

        total_box = self.create_summary_box(
            summary_frame,
            "TOTAL ASSIGNED FEE",
            money(total_fee),
            LIGHT_BLUE,
            BLUE
        )
        total_box.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )

        paid_box = self.create_summary_box(
            summary_frame,
            "TOTAL PAID",
            money(total_paid),
            LIGHT_GREEN,
            GREEN
        )
        paid_box.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=6
        )

        due_box = self.create_summary_box(
            summary_frame,
            "TOTAL DUE",
            money(total_due),
            LIGHT_RED,
            RED
        )
        due_box.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(6, 0)
        )

        # ====================================================
        # ALL FEE STRUCTURES IN THE SAME WINDOW / SAME PART
        # ====================================================

        section_header = Frame(body, bg=BG)
        section_header.pack(
            fill=X,
            padx=20,
            pady=(2, 8)
        )

        Label(
            section_header,
            text="ASSIGNED FEE STRUCTURES",
            bg=BG,
            fg=TEXT,
            font=("Helvetica", 11, "bold")
        ).pack(side=LEFT)

        Label(
            section_header,
            text=f"{len(assignments)} fee assignment(s)",
            bg=LIGHT_BLUE,
            fg=BLUE,
            font=("Helvetica", 8, "bold"),
            padx=10,
            pady=5
        ).pack(side=RIGHT)

        for index, fee in enumerate(assignments, start=1):

            components = self.get_fee_components(
                fee["Fee_Structure_ID"]
            )

            fee_card = Frame(
                body,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )
            fee_card.pack(
                fill=X,
                padx=20,
                pady=(0, 12)
            )

            # Top row
            top = Frame(fee_card, bg=WHITE)
            top.pack(
                fill=X,
                padx=16,
                pady=(14, 8)
            )

            Label(
                top,
                text=(
                    f"FEE {index}  •  SEMESTER {fee['Fee_Semester']}"
                ),
                bg=WHITE,
                fg=TEXT,
                font=("Helvetica", 10, "bold")
            ).pack(side=LEFT)

            status = str(fee["Payment_Status"] or "Unpaid").strip()

            if status.lower() == "paid":
                status_bg = LIGHT_GREEN
                status_fg = GREEN
            elif status.lower() == "partial":
                status_bg = LIGHT_ORANGE
                status_fg = ORANGE
            else:
                status_bg = LIGHT_RED
                status_fg = RED

            Label(
                top,
                text=status.upper(),
                bg=status_bg,
                fg=status_fg,
                font=("Helvetica", 8, "bold"),
                padx=12,
                pady=5
            ).pack(side=RIGHT)

            # Structure meta
            meta = Frame(fee_card, bg="#F8FAFC")
            meta.pack(
                fill=X,
                padx=16,
                pady=(0, 10)
            )

            Label(
                meta,
                text=(
                    f"Academic Year: {fee['Academic_Year'] or '-'}"
                    f"     •     Fee Structure ID: {fee['Fee_Structure_ID']}"
                    f"     •     Student Fee ID: {fee['Student_Fee_ID']}"
                ),
                bg="#F8FAFC",
                fg=GRAY,
                font=("Helvetica", 8)
            ).pack(
                anchor="w",
                padx=12,
                pady=8
            )

            # Per-fee totals
            amounts = Frame(fee_card, bg=WHITE)
            amounts.pack(
                fill=X,
                padx=16,
                pady=(0, 10)
            )

            for col in range(3):
                amounts.grid_columnconfigure(
                    col,
                    weight=1,
                    uniform=f"fee_{index}_amounts"
                )

            fee_total_box = self.create_summary_box(
                amounts,
                "FEE TOTAL",
                money(fee["Total_Fee"]),
                LIGHT_BLUE,
                BLUE
            )
            fee_total_box.grid(
                row=0,
                column=0,
                sticky="nsew",
                padx=(0, 5)
            )

            fee_paid_box = self.create_summary_box(
                amounts,
                "PAID",
                money(fee["Amount_Paid"]),
                LIGHT_GREEN,
                GREEN
            )
            fee_paid_box.grid(
                row=0,
                column=1,
                sticky="nsew",
                padx=5
            )

            fee_due_box = self.create_summary_box(
                amounts,
                "DUE",
                money(fee["Due_Amount"]),
                LIGHT_RED,
                RED
            )
            fee_due_box.grid(
                row=0,
                column=2,
                sticky="nsew",
                padx=(5, 0)
            )

            # Components in the same fee card
            component_area = Frame(fee_card, bg=WHITE)
            component_area.pack(
                fill=X,
                padx=16,
                pady=(0, 10)
            )

            Label(
                component_area,
                text="FEE COMPONENTS",
                bg=WHITE,
                fg=GRAY,
                font=("Helvetica", 8, "bold")
            ).pack(
                anchor="w",
                pady=(0, 6)
            )

            if components:
                for component in components:
                    component_row = Frame(
                        component_area,
                        bg=WHITE
                    )
                    component_row.pack(
                        fill=X,
                        pady=2
                    )

                    Label(
                        component_row,
                        text=component["Fee_Type"],
                        bg=WHITE,
                        fg=TEXT,
                        font=("Helvetica", 8)
                    ).pack(side=LEFT)

                    Label(
                        component_row,
                        text=money(component["Amount"]),
                        bg=WHITE,
                        fg=TEXT,
                        font=("Helvetica", 8, "bold")
                    ).pack(side=RIGHT)
            else:
                Label(
                    component_area,
                    text="No fee components found.",
                    bg=WHITE,
                    fg=GRAY,
                    font=("Helvetica", 8)
                ).pack(anchor="w")

            # Actions for this exact fee structure
            actions = Frame(
                fee_card,
                bg="#F8FAFC"
            )
            actions.pack(
                fill=X,
                padx=16,
                pady=(0, 14)
            )

            Button(
                actions,
                text="PAYMENT HISTORY",
                bg=WHITE,
                fg=BLUE,
                activebackground=LIGHT_BLUE,
                activeforeground=BLUE,
                highlightbackground=BLUE,
                highlightthickness=1,
                bd=0,
                relief=FLAT,
                cursor="hand2",
                font=("Helvetica", 8, "bold"),
                command=lambda fee_id=fee["Student_Fee_ID"]:
                    self.open_payment_history(fee_id)
            ).pack(
                side=LEFT,
                padx=10,
                pady=9,
                ipadx=14,
                ipady=7
            )

            payment_button = Button(
                actions,
                text="+ RECORD PAYMENT",
                bg=BLUE,
                fg=WHITE,
                activebackground=DARK_BLUE,
                activeforeground=WHITE,
                bd=0,
                relief=FLAT,
                cursor="hand2",
                font=("Helvetica", 8, "bold"),
                command=lambda fee_id=fee["Student_Fee_ID"]:
                    self.open_record_payment(
                        fee_id,
                        details_window
                    )
            )
            payment_button.pack(
                side=RIGHT,
                padx=10,
                pady=9,
                ipadx=14,
                ipady=7
            )

            if float(fee["Due_Amount"] or 0) <= 0:
                payment_button.config(
                    state=DISABLED,
                    bg="#CBD5E1",
                    fg="#64748B",
                    cursor=""
                )

        # Mouse wheel scrolling while pointer is over the combined details window.
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )
            except Exception:
                pass

        details_window.bind_all(
            "<MouseWheel>",
            _on_mousewheel
        )

        def _close_details():
            try:
                details_window.unbind_all("<MouseWheel>")
            except Exception:
                pass
            details_window.destroy()

        details_window.protocol(
            "WM_DELETE_WINDOW",
            _close_details
        )

    def open_record_payment(
        self,
        student_fee_id,
        details_window=None
    ):

        details = (
            self.get_student_fee_details(
                student_fee_id
            )
        )


        if not details:

            return


        current_due = float(
            details[
                "Due_Amount"
            ]
        )


        if current_due <= 0:

            messagebox.showinfo(
                "Fee Paid",
                (
                    "This student's fee "
                    "has already been fully paid."
                ),
                parent=self.parent.winfo_toplevel()
            )

            return


        # ====================================================
        # PAYMENT WINDOW
        # ====================================================

        payment_window = Toplevel(
            self.parent
        )

        payment_window.title(
            "Record Payment"
        )

        payment_window.configure(
            bg=BG
        )

        payment_window.resizable(
            False,
            False
        )

        payment_window.transient(
            self.parent.winfo_toplevel()
        )

        payment_window.grab_set()


        self.center_window(
            payment_window,
            540,
            650
        )


        # ====================================================
        # VARIABLES
        # ====================================================

        amount_var = StringVar()

        mode_var = StringVar(
            value="Cash"
        )

        reference_var = StringVar()

        payment_date_var = StringVar(
            value=date.today().isoformat()
        )

        remarks_var = StringVar()


        # ====================================================
        # HEADER
        # ====================================================

        header = Frame(
            payment_window,
            bg=WHITE,
            height=70
        )

        header.pack(
            fill=X
        )

        header.pack_propagate(
            False
        )


        Label(
            header,
            text="RECORD PAYMENT",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                15,
                "bold"
            )
        ).place(
            x=22,
            y=16
        )


        Label(
            header,
            text=(
                f"Add a new payment for "
                f"{details['Name']}."
            ),
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                8
            )
        ).place(
            x=22,
            y=45
        )


        # ====================================================
        # FORM
        # ====================================================

        # Fixed footer is created first so SAVE PAYMENT and
        # CANCEL always remain visible at the bottom.
        footer = Frame(
            payment_window,
            bg=WHITE,
            height=70,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        footer.pack(
            side=BOTTOM,
            fill=X
        )

        footer.pack_propagate(
            False
        )


        form = Frame(
            payment_window,
            bg=BG
        )

        form.pack(
            fill=BOTH,
            expand=True,
            padx=22,
            pady=16
        )


        # ====================================================
        # CURRENT DUE CARD
        # ====================================================

        due_card = Frame(
            form,
            bg=LIGHT_RED,
            highlightbackground="#FECACA",
            highlightthickness=1,
            height=72
        )

        due_card.pack(
            fill=X,
            pady=(0, 12)
        )

        due_card.pack_propagate(
            False
        )


        Label(
            due_card,
            text="CURRENT DUE",
            bg=LIGHT_RED,
            fg=GRAY,
            font=(
                "Helvetica",
                8,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=16,
            pady=(10, 2)
        )


        Label(
            due_card,
            text=money(
                current_due
            ),
            bg=LIGHT_RED,
            fg=RED,
            font=(
                "Helvetica",
                17,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=16
        )


        # ====================================================
        # TWO-COLUMN COMPACT FORM
        # ====================================================

        fields = Frame(
            form,
            bg=BG
        )

        fields.pack(
            fill=BOTH,
            expand=True
        )

        fields.grid_columnconfigure(
            0,
            weight=1
        )

        fields.grid_columnconfigure(
            1,
            weight=1
        )


        # ----------------------------------------------------
        # PAYMENT AMOUNT
        # ----------------------------------------------------

        Label(
            fields,
            text="Payment Amount *",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=(0, 5)
        )


        # ----------------------------------------------------
        # PAYMENT MODE
        # ----------------------------------------------------

        Label(
            fields,
            text="Payment Mode *",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(8, 0),
            pady=(0, 5)
        )


        amount_entry = Entry(
            fields,
            textvariable=amount_var,
            bg=WHITE,
            fg=TEXT,
            insertbackground=TEXT,
            font=(
                "Helvetica",
                10
            ),
            relief=SOLID,
            bd=1
        )

        amount_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 8),
            ipady=8,
            pady=(0, 12)
        )


        mode_combo = ttk.Combobox(
            fields,
            textvariable=mode_var,
            state="readonly",
            values=(
                "Cash",
                "UPI",
                "Card",
                "Bank Transfer",
                "Cheque"
            )
        )

        mode_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(8, 0),
            ipady=5,
            pady=(0, 12)
        )


        # ----------------------------------------------------
        # TRANSACTION REFERENCE
        # ----------------------------------------------------

        Label(
            fields,
            text="Transaction Reference",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 5)
        )


        Entry(
            fields,
            textvariable=reference_var,
            bg=WHITE,
            fg=TEXT,
            insertbackground=TEXT,
            font=(
                "Helvetica",
                10
            ),
            relief=SOLID,
            bd=1
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            ipady=8,
            pady=(0, 12)
        )


        # ----------------------------------------------------
        # PAYMENT DATE
        # ----------------------------------------------------

        Label(
            fields,
            text="Payment Date *  (YYYY-MM-DD)",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 5)
        )


        Entry(
            fields,
            textvariable=payment_date_var,
            bg=WHITE,
            fg=TEXT,
            insertbackground=TEXT,
            font=(
                "Helvetica",
                10
            ),
            relief=SOLID,
            bd=1
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            ipady=8,
            pady=(0, 12)
        )


        # ----------------------------------------------------
        # REMARKS
        # ----------------------------------------------------

        Label(
            fields,
            text="Remarks",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 5)
        )


        Entry(
            fields,
            textvariable=remarks_var,
            bg=WHITE,
            fg=TEXT,
            insertbackground=TEXT,
            font=(
                "Helvetica",
                10
            ),
            relief=SOLID,
            bd=1
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew",
            ipady=8
        )


        amount_entry.focus_set()


        # ====================================================
        # SAVE PAYMENT
        # ====================================================

        def save_payment():

            amount_text = (
                amount_var.get().strip()
            )

            payment_mode = (
                mode_var.get().strip()
            )

            transaction_reference = (
                reference_var.get().strip()
            )

            payment_date = (
                payment_date_var.get().strip()
            )

            remarks = (
                remarks_var.get().strip()
            )


            # ------------------------------------------------
            # AMOUNT REQUIRED
            # ------------------------------------------------

            if amount_text == "":

                messagebox.showwarning(
                    "Amount Required",
                    (
                        "Please enter "
                        "the payment amount."
                    ),
                    parent=payment_window
                )

                amount_entry.focus_set()

                return


            # ------------------------------------------------
            # VALID AMOUNT
            # ------------------------------------------------

            try:

                payment_amount = float(
                    amount_text
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Amount",
                    (
                        "Please enter a valid "
                        "numeric payment amount."
                    ),
                    parent=payment_window
                )

                amount_entry.focus_set()

                return


            # ------------------------------------------------
            # POSITIVE AMOUNT
            # ------------------------------------------------

            if payment_amount <= 0:

                messagebox.showwarning(
                    "Invalid Amount",
                    (
                        "Payment amount must "
                        "be greater than zero."
                    ),
                    parent=payment_window
                )

                return


            # ------------------------------------------------
            # CANNOT EXCEED DUE
            # ------------------------------------------------

            if payment_amount > current_due:

                messagebox.showwarning(
                    "Amount Exceeds Due",
                    (
                        "Payment amount cannot "
                        "be greater than the "
                        "current due amount."
                        "\n\n"
                        f"Current Due: "
                        f"{money(current_due)}"
                    ),
                    parent=payment_window
                )

                return


            # ------------------------------------------------
            # PAYMENT MODE REQUIRED
            # ------------------------------------------------

            if payment_mode == "":

                messagebox.showwarning(
                    "Payment Mode Required",
                    (
                        "Please select a "
                        "payment mode."
                    ),
                    parent=payment_window
                )

                return


            # ------------------------------------------------
            # PAYMENT DATE REQUIRED
            # ------------------------------------------------

            if payment_date == "":

                messagebox.showwarning(
                    "Payment Date Required",
                    (
                        "Please enter the "
                        "payment date."
                    ),
                    parent=payment_window
                )

                return


            # ------------------------------------------------
            # VALIDATE DATE
            # ------------------------------------------------

            try:

                entered_payment_date = date.fromisoformat(
                    payment_date
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Date",
                    (
                        "Payment Date must use "
                        "YYYY-MM-DD format."
                    ),
                    parent=payment_window
                )

                return


            # ------------------------------------------------
            # FUTURE PAYMENT DATE IS NOT ALLOWED
            # Maximum allowed date is today's system date.
            # ------------------------------------------------

            today_date = date.today()

            if entered_payment_date > today_date:

                messagebox.showerror(
                    "Future Date Not Allowed",
                    (
                        "Payment date cannot be after today's date."
                        "\n\n"
                        f"Today's Date: {today_date.isoformat()}"
                        "\n"
                        f"Entered Date: {entered_payment_date.isoformat()}"
                        "\n\n"
                        "Please enter today's date or an earlier date."
                    ),
                    parent=payment_window
                )

                payment_date_var.set(
                    today_date.isoformat()
                )

                return


            # =================================================
            # DATABASE TRANSACTION
            # =================================================

            con = None

            cursor = None


            try:

                con = get_connection()

                cursor = con.cursor()


                # --------------------------------------------
                # GET LATEST FEE DATA
                # --------------------------------------------

                cursor.execute(
                    """
                    SELECT

                        Total_Fee,

                        Amount_Paid,

                        Due_Amount

                    FROM student_fees

                    WHERE
                        Student_Fee_ID = %s

                    FOR UPDATE
                    """,
                    (
                        student_fee_id,
                    )
                )


                current_record = (
                    cursor.fetchone()
                )


                if current_record is None:

                    raise Exception(
                        "Student fee record was not found."
                    )


                total_fee = float(
                    current_record[0]
                )

                old_paid = float(
                    current_record[1]
                )

                latest_due = float(
                    current_record[2]
                )


                # --------------------------------------------
                # CHECK AGAINST LATEST DUE
                # --------------------------------------------

                if payment_amount > latest_due:

                    raise Exception(
                        (
                            "Payment amount is greater "
                            "than the latest due amount."
                        )
                    )


                # --------------------------------------------
                # CALCULATE NEW VALUES
                # --------------------------------------------

                new_paid = (
                    old_paid
                    +
                    payment_amount
                )


                new_due = (
                    total_fee
                    -
                    new_paid
                )


                if new_due < 0:

                    new_due = 0


                if new_due <= 0:

                    new_status = "Paid"


                elif new_paid > 0:

                    new_status = "Partial"


                else:

                    new_status = "Unpaid"


                # --------------------------------------------
                # INSERT PAYMENT
                # --------------------------------------------

                cursor.execute(
                    """
                    INSERT INTO fee_payments
                    (
                        Student_Fee_ID,

                        Amount,

                        Payment_Mode,

                        Transaction_Reference,

                        Remarks,

                        Payment_Date,

                        Collected_By
                    )

                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        student_fee_id,

                        payment_amount,

                        payment_mode,

                        (
                            transaction_reference
                            if
                            transaction_reference
                            else
                            None
                        ),

                        (
                            remarks
                            if
                            remarks
                            else
                            None
                        ),

                        payment_date,

                        self.collector_name
                    )
                )


                # --------------------------------------------
                # UPDATE STUDENT FEE
                # --------------------------------------------

                cursor.execute(
                    """
                    UPDATE student_fees

                    SET

                        Amount_Paid = %s,

                        Due_Amount = %s,

                        Payment_Status = %s

                    WHERE
                        Student_Fee_ID = %s
                    """,
                    (
                        new_paid,

                        new_due,

                        new_status,

                        student_fee_id
                    )
                )


                # --------------------------------------------
                # COMMIT
                # --------------------------------------------

                con.commit()


                messagebox.showinfo(
                    "Payment Saved",
                    (
                        "Payment recorded successfully."
                        "\n\n"
                        f"Amount: "
                        f"{money(payment_amount)}"
                        "\n"
                        f"Remaining Due: "
                        f"{money(new_due)}"
                        "\n"
                        f"Status: "
                        f"{new_status}"
                    ),
                    parent=payment_window
                )


                # --------------------------------------------
                # CLOSE PAYMENT WINDOW
                # --------------------------------------------

                payment_window.destroy()


                # --------------------------------------------
                # CLOSE OLD DETAILS WINDOW
                # --------------------------------------------

                if (
                    details_window is not None
                    and
                    details_window.winfo_exists()
                ):

                    details_window.destroy()


                # --------------------------------------------
                # REFRESH STUDENT FEE TABLE
                # --------------------------------------------

                self.load_student_fees()


                # --------------------------------------------
                # REFRESH DASHBOARD IF CALLBACK EXISTS
                # --------------------------------------------

                if (
                    self.refresh_dashboard_callback
                    is not None
                ):

                    try:

                        self.refresh_dashboard_callback()

                    except Exception:

                        pass


                # --------------------------------------------
                # REOPEN UPDATED DETAILS
                # --------------------------------------------

                self.open_student_fee_details(
                    student_fee_id
                )


            except (
                mysql.connector.Error,
                Exception
            ) as error:

                if (
                    con is not None
                    and
                    con.is_connected()
                ):

                    con.rollback()


                messagebox.showerror(
                    "Payment Error",
                    (
                        "Unable to record payment."
                        f"\n\n{error}"
                    ),
                    parent=payment_window
                )


            finally:

                if cursor is not None:

                    cursor.close()


                if (
                    con is not None
                    and
                    con.is_connected()
                ):

                    con.close()


        # ====================================================
        # FIXED FOOTER BUTTONS
        # ====================================================

        Button(
            footer,
            text="CANCEL",
            bg="#E2E8F0",
            fg=TEXT,
            activebackground="#CBD5E1",
            activeforeground=TEXT,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=payment_window.destroy
        ).pack(
            side=RIGHT,
            padx=(10, 18),
            pady=14,
            ipadx=20,
            ipady=9
        )


        Button(
            footer,
            text="SAVE PAYMENT",
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=save_payment
        ).pack(
            side=RIGHT,
            pady=14,
            ipadx=22,
            ipady=9
        )


    # ========================================================
    # PAYMENT HISTORY
    # ========================================================

    def open_payment_history(
        self,
        student_fee_id
    ):

        details = self.get_student_fee_details(
            student_fee_id
        )

        if not details:
            return


        history_window = Toplevel(
            self.parent
        )

        history_window.title(
            "Payment History"
        )

        history_window.configure(
            bg=BG
        )

        history_window.resizable(
            False,
            False
        )

        history_window.transient(
            self.parent.winfo_toplevel()
        )

        history_window.grab_set()


        self.center_window(
            history_window,
            980,
            520
        )


        # ====================================================
        # HEADER
        # ====================================================

        header = Frame(
            history_window,
            bg=WHITE,
            height=92
        )

        header.pack(
            fill=X
        )

        header.pack_propagate(
            False
        )


        Label(
            header,
            text=(
                f"PAYMENT HISTORY — "
                f"{details['Name']}"
            ),
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                15,
                "bold"
            )
        ).place(
            x=22,
            y=16
        )


        Label(
            header,
            text=(
                f"{details['Registration_No']}  •  "
                "Single-click any payment row to open its receipt."
            ),
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                9
            )
        ).place(
            x=22,
            y=50
        )


        # ====================================================
        # BODY
        # ====================================================

        body = Frame(
            history_window,
            bg=BG
        )

        body.pack(
            fill=BOTH,
            expand=True,
            padx=20,
            pady=18
        )


        table_card = Frame(
            body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        table_card.pack(
            fill=BOTH,
            expand=True
        )


        columns = (
            "payment_id",
            "date",
            "amount",
            "mode",
            "reference",
            "collector",
            "remarks"
        )


        history_tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            style="StudentFees.Treeview",
            selectmode="browse"
        )


        headings = {
            "payment_id": "PAYMENT ID",
            "date": "DATE",
            "amount": "AMOUNT",
            "mode": "MODE",
            "reference": "REFERENCE",
            "collector": "COLLECTED BY",
            "remarks": "REMARKS"
        }


        for column, heading in headings.items():

            history_tree.heading(
                column,
                text=heading
            )


        history_tree.column(
            "payment_id",
            width=105,
            anchor=CENTER
        )

        history_tree.column(
            "date",
            width=100,
            anchor=CENTER
        )

        history_tree.column(
            "amount",
            width=115,
            anchor=E
        )

        history_tree.column(
            "mode",
            width=100,
            anchor=CENTER
        )

        history_tree.column(
            "reference",
            width=135,
            anchor=CENTER
        )

        history_tree.column(
            "collector",
            width=150,
            anchor=W
        )

        history_tree.column(
            "remarks",
            width=170,
            anchor=W
        )


        scrollbar = ttk.Scrollbar(
            table_card,
            orient=VERTICAL,
            command=history_tree.yview
        )


        history_tree.configure(
            yscrollcommand=scrollbar.set
        )


        history_tree.pack(
            side=LEFT,
            fill=BOTH,
            expand=True,
            padx=(12, 0),
            pady=12
        )


        scrollbar.pack(
            side=RIGHT,
            fill=Y,
            padx=(0, 12),
            pady=12
        )


        # ====================================================
        # LOAD PAYMENT HISTORY
        # ====================================================

        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor(
                dictionary=True
            )


            cursor.execute(
                """
                SELECT

                    Payment_ID,

                    Payment_Date,

                    Amount,

                    Payment_Mode,

                    Transaction_Reference,

                    Remarks,

                    Collected_By,

                    Created_At

                FROM fee_payments

                WHERE
                    Student_Fee_ID = %s

                ORDER BY
                    Payment_Date DESC,
                    Payment_ID DESC
                """,
                (
                    student_fee_id,
                )
            )


            records = cursor.fetchall()


            for record in records:

                payment_id = int(
                    record["Payment_ID"]
                )


                history_tree.insert(
                    "",
                    END,
                    iid=str(payment_id),
                    values=(
                        f"PAY-{payment_id:06d}",

                        record["Payment_Date"],

                        money(
                            record["Amount"]
                        ),

                        record["Payment_Mode"],

                        (
                            record["Transaction_Reference"]
                            or
                            "-"
                        ),

                        (
                            record["Collected_By"]
                            or
                            "-"
                        ),

                        (
                            record["Remarks"]
                            or
                            "-"
                        )
                    )
                )


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load payment history."
                    f"\n\n{error}"
                ),
                parent=history_window
            )


        finally:

            if cursor is not None:
                cursor.close()


            if (
                con is not None
                and
                con.is_connected()
            ):
                con.close()


        # ====================================================
        # SINGLE-CLICK PAYMENT -> RECEIPT
        # ====================================================

        def open_selected_receipt(
            event
        ):

            region = history_tree.identify_region(
                event.x,
                event.y
            )


            if region != "cell":
                return


            row_id = history_tree.identify_row(
                event.y
            )


            if not row_id:
                return


            history_tree.selection_set(
                row_id
            )


            try:
                history_window.grab_release()
            except TclError:
                pass

            self.open_payment_receipt(
                int(row_id),
                owner_window=history_window
            )


        history_tree.bind(
            "<ButtonRelease-1>",
            open_selected_receipt
        )

        history_tree.bind(
            "<Double-1>",
            open_selected_receipt
        )

        def open_receipt_with_enter(event=None):

            selected = history_tree.selection()

            if not selected:
                return

            try:
                try:
                    history_window.grab_release()
                except TclError:
                    pass

                self.open_payment_receipt(
                    int(selected[0]),
                    owner_window=history_window
                )

            except (
                TypeError,
                ValueError
            ):
                return


        history_tree.bind(
            "<Return>",
            open_receipt_with_enter
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        summary = Frame(
            body,
            bg=BG
        )

        summary.pack(
            fill=X,
            pady=(12, 0)
        )


        Label(
            summary,
            text=(
                "Total Paid: "
                f"{money(details['Amount_Paid'])}"
            ),
            bg=BG,
            fg=GREEN,
            font=(
                "Helvetica",
                10,
                "bold"
            )
        ).pack(
            side=LEFT
        )


        Label(
            summary,
            text=(
                "Remaining Due: "
                f"{money(details['Due_Amount'])}"
            ),
            bg=BG,
            fg=RED,
            font=(
                "Helvetica",
                10,
                "bold"
            )
        ).pack(
            side=RIGHT
        )


        # ====================================================
        # EXPLICIT OPEN RECEIPT BUTTON
        # ====================================================

        def open_selected_payment_receipt():

            selected = history_tree.selection()


            if not selected:

                messagebox.showwarning(
                    "Select Payment",
                    (
                        "Please select a payment record "
                        "from the payment history first."
                    ),
                    parent=history_window
                )

                return


            try:

                selected_payment_id = int(
                    selected[0]
                )

            except (
                TypeError,
                ValueError
            ):

                messagebox.showerror(
                    "Receipt Error",
                    "Invalid payment record selected.",
                    parent=history_window
                )

                return


            try:
                history_window.grab_release()
            except TclError:
                pass

            self.open_payment_receipt(
                selected_payment_id,
                owner_window=history_window
            )


        Button(
            summary,
            text="OPEN RECEIPT",
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=open_selected_payment_receipt
        ).pack(
            side=RIGHT,
            padx=(0, 22),
            ipadx=16,
            ipady=7
        )


    # ========================================================
    # GET ONE PAYMENT RECEIPT
    # ========================================================

    def get_payment_receipt(
        self,
        payment_id
    ):

        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor(
                dictionary=True
            )


            cursor.execute(
                """
                SELECT

                    fp.Payment_ID,
                    fp.Amount,
                    fp.Payment_Mode,
                    fp.Transaction_Reference,
                    fp.Remarks,
                    fp.Payment_Date,
                    fp.Collected_By,
                    fp.Created_At,

                    sf.Student_Fee_ID,
                    sf.Total_Fee,
                    sf.Amount_Paid,
                    sf.Due_Amount,
                    sf.Payment_Status,
                    sf.Registration_No,

                    r.Name,

                    sd.Course,
                    sd.Semester,

                    fs.Academic_Year

                FROM fee_payments fp

                INNER JOIN student_fees sf
                    ON sf.Student_Fee_ID = fp.Student_Fee_ID

                INNER JOIN registration r
                    ON r.Registration_No = sf.Registration_No

                LEFT JOIN student_details sd
                    ON sd.Registration_No = sf.Registration_No

                INNER JOIN fee_structures fs
                    ON fs.Fee_Structure_ID = sf.Fee_Structure_ID

                WHERE
                    fp.Payment_ID = %s

                LIMIT 1
                """,
                (
                    payment_id,
                )
            )


            return cursor.fetchone()


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load payment receipt."
                    f"\n\n{error}"
                ),
                parent=self.parent.winfo_toplevel()
            )

            return None


        finally:

            if cursor is not None:
                cursor.close()


            if (
                con is not None
                and
                con.is_connected()
            ):
                con.close()


    # ========================================================
    # RECEIPT IMAGE HELPERS
    # ========================================================

    def _receipt_font(
        self,
        size,
        bold=False
    ):

        font_candidates = []

        if os.name == "nt":

            if bold:

                font_candidates.extend(
                    [
                        r"C:\Windows\Fonts\arialbd.ttf",
                        r"C:\Windows\Fonts\segoeuib.ttf"
                    ]
                )

            else:

                font_candidates.extend(
                    [
                        r"C:\Windows\Fonts\arial.ttf",
                        r"C:\Windows\Fonts\segoeui.ttf"
                    ]
                )


        for font_path in font_candidates:

            if os.path.exists(
                font_path
            ):

                try:

                    return ImageFont.truetype(
                        font_path,
                        size
                    )

                except Exception:

                    pass


        return ImageFont.load_default()


    def create_receipt_image(
        self,
        receipt,
        output_path
    ):

        width = 900
        height = 1120

        image = Image.new(
            "RGB",
            (
                width,
                height
            ),
            "white"
        )

        draw = ImageDraw.Draw(
            image
        )


        blue = "#2563EB"
        dark = "#0F172A"
        gray = "#64748B"
        green = "#16A34A"
        red = "#DC2626"
        orange = "#EA580C"
        border = "#E2E8F0"
        light_green = "#F0FDF4"


        title_font = self._receipt_font(
            38,
            True
        )

        subtitle_font = self._receipt_font(
            20,
            False
        )

        label_font = self._receipt_font(
            20,
            True
        )

        value_font = self._receipt_font(
            21,
            True
        )

        amount_label_font = self._receipt_font(
            20,
            True
        )

        amount_font = self._receipt_font(
            42,
            True
        )

        footer_font = self._receipt_font(
            17,
            False
        )


        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        draw.rectangle(
            (
                0,
                0,
                width,
                170
            ),
            fill=blue
        )


        draw.text(
            (
                55,
                42
            ),
            "FEE PAYMENT RECEIPT",
            fill="white",
            font=title_font
        )


        draw.text(
            (
                55,
                108
            ),
            (
                f"Receipt No: "
                f"PAY-{int(receipt['Payment_ID']):06d}"
            ),
            fill="#DBEAFE",
            font=subtitle_font
        )


        # ----------------------------------------------------
        # INFORMATION CARD
        # ----------------------------------------------------

        card_left = 55
        card_top = 210
        card_right = width - 55
        card_bottom = 760


        draw.rounded_rectangle(
            (
                card_left,
                card_top,
                card_right,
                card_bottom
            ),
            radius=10,
            fill="white",
            outline=border,
            width=2
        )


        rows = (
            (
                "Student",
                receipt["Name"]
            ),
            (
                "Registration No.",
                receipt["Registration_No"]
            ),
            (
                "Course",
                receipt["Course"] or "-"
            ),
            (
                "Semester",
                receipt["Semester"] or "-"
            ),
            (
                "Academic Year",
                receipt["Academic_Year"] or "-"
            ),
            (
                "Payment Date",
                receipt["Payment_Date"]
            ),
            (
                "Payment Mode",
                receipt["Payment_Mode"]
            ),
            (
                "Transaction Reference",
                receipt["Transaction_Reference"] or "-"
            ),
            (
                "Collected By",
                receipt["Collected_By"] or "-"
            )
        )


        y = 245


        for label_text, value_text in rows:

            draw.text(
                (
                    95,
                    y
                ),
                str(label_text),
                fill=gray,
                font=label_font
            )


            draw.text(
                (
                    390,
                    y
                ),
                str(value_text),
                fill=dark,
                font=value_font
            )


            y += 52


        # ----------------------------------------------------
        # AMOUNT PAID
        # ----------------------------------------------------

        draw.rounded_rectangle(
            (
                85,
                790,
                width - 85,
                920
            ),
            radius=8,
            fill=light_green,
            outline="#BBF7D0",
            width=2
        )


        draw.text(
            (
                120,
                818
            ),
            "AMOUNT PAID",
            fill=gray,
            font=amount_label_font
        )


        draw.text(
            (
                120,
                858
            ),
            money(
                receipt["Amount"]
            ),
            fill=green,
            font=amount_font
        )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        status_text = str(
            receipt["Payment_Status"]
        )


        if status_text.lower() == "paid":

            status_color = green

        elif status_text.lower() == "partial":

            status_color = orange

        else:

            status_color = red


        summary_rows = (
            (
                "Total Fee",
                money(
                    receipt["Total_Fee"]
                ),
                dark
            ),
            (
                "Total Paid",
                money(
                    receipt["Amount_Paid"]
                ),
                green
            ),
            (
                "Due Amount",
                money(
                    receipt["Due_Amount"]
                ),
                red
            ),
            (
                "Status",
                status_text,
                status_color
            )
        )


        y = 950


        for label_text, value_text, value_color in summary_rows:

            draw.text(
                (
                    90,
                    y
                ),
                label_text,
                fill=gray,
                font=label_font
            )


            right_box = draw.textbbox(
                (
                    0,
                    0
                ),
                str(value_text),
                font=value_font
            )


            value_width = (
                right_box[2]
                -
                right_box[0]
            )


            draw.text(
                (
                    width
                    -
                    90
                    -
                    value_width,
                    y
                ),
                str(value_text),
                fill=value_color,
                font=value_font
            )


            y += 42


        draw.text(
            (
                55,
                height - 35
            ),
            "Fee Status Management System",
            fill=gray,
            font=footer_font
        )


        image.save(
            output_path,
            "PNG"
        )


        return output_path


    def save_receipt_image(
        self,
        receipt,
        parent_window
    ):

        default_name = (
            f"PAY-{int(receipt['Payment_ID']):06d}_"
            f"{receipt['Registration_No']}.png"
        )


        file_path = filedialog.asksaveasfilename(
            parent=parent_window,
            title="Save Payment Receipt",
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[
                (
                    "PNG Image",
                    "*.png"
                )
            ]
        )


        if not file_path:
            return


        try:

            self.create_receipt_image(
                receipt,
                file_path
            )


            messagebox.showinfo(
                "Receipt Saved",
                (
                    "Payment receipt saved successfully."
                    f"\n\n{file_path}"
                ),
                parent=parent_window
            )


        except Exception as error:

            messagebox.showerror(
                "Save Error",
                (
                    "Unable to save the payment receipt."
                    f"\n\n{error}"
                ),
                parent=parent_window
            )


    def share_receipt_image(
        self,
        receipt,
        parent_window
    ):

        bills_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(
                        __file__
                    )
                )
            ),
            "BILLS"
        )


        try:

            os.makedirs(
                bills_dir,
                exist_ok=True
            )


            file_name = (
                f"PAY-{int(receipt['Payment_ID']):06d}_"
                f"{receipt['Registration_No']}.png"
            )


            file_path = os.path.join(
                bills_dir,
                file_name
            )


            self.create_receipt_image(
                receipt,
                file_path
            )


            # On Windows, open Explorer with the receipt selected.
            # The user can then use Windows Share / WhatsApp / Email.
            if os.name == "nt":

                subprocess.Popen(
                    [
                        "explorer",
                        "/select,",
                        os.path.normpath(
                            file_path
                        )
                    ]
                )

            else:

                subprocess.Popen(
                    [
                        "xdg-open",
                        bills_dir
                    ]
                )


            messagebox.showinfo(
                "Receipt Ready to Share",
                (
                    "The receipt image has been created and "
                    "selected in the BILLS folder."
                    "\n\n"
                    f"{file_path}"
                ),
                parent=parent_window
            )


        except Exception as error:

            messagebox.showerror(
                "Share Error",
                (
                    "Unable to prepare the receipt for sharing."
                    f"\n\n{error}"
                ),
                parent=parent_window
            )


    # ========================================================
    # OPEN PAYMENT RECEIPT
    # ========================================================

    def open_payment_receipt(
        self,
        payment_id,
        owner_window=None
    ):

        try:

            payment_id = int(
                payment_id
            )

        except (
            TypeError,
            ValueError
        ):

            messagebox.showerror(
                "Receipt Error",
                "Invalid payment record.",
                parent=self.parent.winfo_toplevel()
            )

            return


        receipt = self.get_payment_receipt(
            payment_id
        )


        if not receipt:

            messagebox.showerror(
                "Receipt Error",
                (
                    "Payment receipt data was not found "
                    "for this payment."
                ),
                parent=self.parent.winfo_toplevel()
            )

            return


        receipt_parent = (
            owner_window
            if owner_window is not None
            and owner_window.winfo_exists()
            else self.parent.winfo_toplevel()
        )

        receipt_window = Toplevel(
            receipt_parent
        )

        receipt_window.title(
            "Payment Receipt"
        )

        receipt_window.configure(
            bg=BG
        )

        receipt_window.resizable(
            False,
            False
        )

        receipt_window.transient(
            receipt_parent
        )


        self.center_window(
            receipt_window,
            590,
            690
        )


        # ====================================================
        # HEADER
        # ====================================================

        header = Frame(
            receipt_window,
            bg=BLUE,
            height=105
        )

        header.pack(
            fill=X
        )

        header.pack_propagate(
            False
        )


        Label(
            header,
            text="FEE PAYMENT RECEIPT",
            bg=BLUE,
            fg=WHITE,
            font=(
                "Helvetica",
                20,
                "bold"
            )
        ).place(
            x=28,
            y=20
        )


        Label(
            header,
            text=(
                f"Receipt No: "
                f"PAY-{int(receipt['Payment_ID']):06d}"
            ),
            bg=BLUE,
            fg="#DBEAFE",
            font=(
                "Helvetica",
                9
            )
        ).place(
            x=28,
            y=65
        )


        # ====================================================
        # CLOSE RECEIPT AND RESTORE PAYMENT HISTORY
        # ====================================================

        def close_receipt():

            try:
                receipt_window.grab_release()
            except TclError:
                pass

            receipt_window.destroy()

            if (
                owner_window is not None
                and owner_window.winfo_exists()
            ):

                owner_window.lift()
                owner_window.focus_force()

                try:
                    owner_window.grab_set()
                except TclError:
                    pass


        receipt_window.protocol(
            "WM_DELETE_WINDOW",
            close_receipt
        )


        # ====================================================
        # FIXED FOOTER WITH SHARE / SAVE / CLOSE
        # ====================================================

        footer = Frame(
            receipt_window,
            bg=WHITE,
            height=68,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        footer.pack(
            side=BOTTOM,
            fill=X
        )

        footer.pack_propagate(
            False
        )


        Button(
            footer,
            text="CLOSE",
            bg="#E2E8F0",
            fg=TEXT,
            activebackground="#CBD5E1",
            activeforeground=TEXT,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=close_receipt
        ).pack(
            side=RIGHT,
            padx=(8, 16),
            pady=14,
            ipadx=15,
            ipady=8
        )


        Button(
            footer,
            text="SAVE IMAGE",
            bg=WHITE,
            fg=BLUE,
            activebackground=LIGHT_BLUE,
            activeforeground=BLUE,
            highlightbackground=BLUE,
            highlightthickness=1,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=lambda:
            self.save_receipt_image(
                receipt,
                receipt_window
            )
        ).pack(
            side=RIGHT,
            padx=4,
            pady=14,
            ipadx=14,
            ipady=7
        )


        Button(
            footer,
            text="SHARE",
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=lambda:
            self.share_receipt_image(
                receipt,
                receipt_window
            )
        ).pack(
            side=RIGHT,
            padx=4,
            pady=14,
            ipadx=18,
            ipady=8
        )


        # ====================================================
        # RECEIPT CARD
        # ====================================================

        outer = Frame(
            receipt_window,
            bg=BG
        )

        outer.pack(
            fill=BOTH,
            expand=True,
            padx=20,
            pady=16
        )


        card = Frame(
            outer,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill=BOTH,
            expand=True
        )


        # ====================================================
        # INFORMATION
        # ====================================================

        info = Frame(
            card,
            bg=WHITE
        )

        info.pack(
            fill=X,
            padx=24,
            pady=(14, 8)
        )


        info.grid_columnconfigure(
            0,
            minsize=165
        )

        info.grid_columnconfigure(
            1,
            weight=1
        )


        rows = (
            (
                "Student",
                receipt["Name"]
            ),
            (
                "Registration No.",
                receipt["Registration_No"]
            ),
            (
                "Course",
                receipt["Course"] or "-"
            ),
            (
                "Semester",
                receipt["Semester"] or "-"
            ),
            (
                "Academic Year",
                receipt["Academic_Year"] or "-"
            ),
            (
                "Payment Date",
                receipt["Payment_Date"]
            ),
            (
                "Payment Mode",
                receipt["Payment_Mode"]
            ),
            (
                "Transaction Reference",
                receipt["Transaction_Reference"] or "-"
            ),
            (
                "Collected By",
                receipt["Collected_By"] or "-"
            )
        )


        for row_index, (
            label_text,
            value_text
        ) in enumerate(rows):

            Label(
                info,
                text=label_text,
                bg=WHITE,
                fg=GRAY,
                font=(
                    "Helvetica",
                    8,
                    "bold"
                )
            ).grid(
                row=row_index,
                column=0,
                sticky="w",
                pady=4
            )


            Label(
                info,
                text=str(value_text),
                bg=WHITE,
                fg=TEXT,
                font=(
                    "Helvetica",
                    8,
                    "bold"
                ),
                anchor="w"
            ).grid(
                row=row_index,
                column=1,
                sticky="w",
                pady=4
            )


        Frame(
            card,
            bg=BORDER,
            height=1
        ).pack(
            fill=X,
            padx=24,
            pady=(4, 10)
        )


        # ====================================================
        # AMOUNT PAID
        # ====================================================

        amount_box = Frame(
            card,
            bg=LIGHT_GREEN,
            highlightbackground="#BBF7D0",
            highlightthickness=1,
            height=82
        )

        amount_box.pack(
            fill=X,
            padx=24,
            pady=(0, 12)
        )

        amount_box.pack_propagate(
            False
        )


        Label(
            amount_box,
            text="AMOUNT PAID",
            bg=LIGHT_GREEN,
            fg=GRAY,
            font=(
                "Helvetica",
                8,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(11, 2)
        )


        Label(
            amount_box,
            text=money(
                receipt["Amount"]
            ),
            bg=LIGHT_GREEN,
            fg=GREEN,
            font=(
                "Helvetica",
                18,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=18
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        summary = Frame(
            card,
            bg=WHITE
        )

        summary.pack(
            fill=X,
            padx=24,
            pady=(0, 10)
        )


        status_text = str(
            receipt["Payment_Status"]
        )


        if status_text.lower() == "paid":

            status_color = GREEN

        elif status_text.lower() == "partial":

            status_color = ORANGE

        else:

            status_color = RED


        summary_rows = (
            (
                "Total Fee",
                money(
                    receipt["Total_Fee"]
                ),
                TEXT
            ),
            (
                "Total Paid",
                money(
                    receipt["Amount_Paid"]
                ),
                GREEN
            ),
            (
                "Due Amount",
                money(
                    receipt["Due_Amount"]
                ),
                RED
            ),
            (
                "Status",
                status_text,
                status_color
            )
        )


        for (
            label_text,
            value_text,
            value_color
        ) in summary_rows:

            row = Frame(
                summary,
                bg=WHITE,
                height=24
            )

            row.pack(
                fill=X
            )

            row.pack_propagate(
                False
            )


            Label(
                row,
                text=label_text,
                bg=WHITE,
                fg=GRAY,
                font=(
                    "Helvetica",
                    8
                )
            ).pack(
                side=LEFT
            )


            Label(
                row,
                text=str(value_text),
                bg=WHITE,
                fg=value_color,
                font=(
                    "Helvetica",
                    8,
                    "bold"
                )
            ).pack(
                side=RIGHT
            )


        receipt_window.update_idletasks()
        receipt_window.deiconify()
        receipt_window.lift()
        receipt_window.attributes("-topmost", True)
        receipt_window.after(
            150,
            lambda:
            receipt_window.attributes(
                "-topmost",
                False
            )
        )
        receipt_window.focus_force()

        try:
            receipt_window.grab_set()
        except TclError:
            pass


# ============================================================
# PUBLIC FUNCTION
#
# accountant_dashboard.py will call this function.
# ============================================================

def show_student_fees_page(
    parent,
    status_filter="All",
    refresh_dashboard_callback=None,
    collector_name=None
):

    return StudentFeesPage(
        parent=parent,
        status_filter=status_filter,
        refresh_dashboard_callback=refresh_dashboard_callback,
        collector_name=collector_name
    )