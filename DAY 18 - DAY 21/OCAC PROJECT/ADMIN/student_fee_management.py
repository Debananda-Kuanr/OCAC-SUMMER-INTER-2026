from tkinter import *
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import date, datetime
import os


BILL_FOLDER = r"C:\Users\deban\Desktop\OCAC PROJECT\BILLS"
os.makedirs(BILL_FOLDER, exist_ok=True)
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
DARK_BLUE = "#1D4ED8"

PURPLE = "#7C3AED"
DARK_PURPLE = "#6D28D9"

GREEN = "#16A34A"
DARK_GREEN = "#15803D"

ORANGE = "#EA580C"

RED = "#DC2626"

WHITE = "#FFFFFF"
BG = "#F8FAFC"

TEXT = "#0F172A"
GRAY = "#64748B"

BORDER = "#CBD5E1"
LIGHT_BORDER = "#E2E8F0"

LIGHT_BLUE = "#EFF6FF"
LIGHT_GREEN = "#F0FDF4"
LIGHT_ORANGE = "#FFF7ED"
LIGHT_RED = "#FEF2F2"


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
# CENTER POPUP WINDOW
# ============================================================

def center_window(window, width, height, parent=None):
    window.update_idletasks()
    try:
        owner = parent.winfo_toplevel() if parent is not None else None
        if owner is not None:
            owner.update_idletasks()
            x = owner.winfo_rootx() + max(0, (owner.winfo_width() - width) // 2)
            y = owner.winfo_rooty() + max(0, (owner.winfo_height() - height) // 2)
        else:
            x = (window.winfo_screenwidth() - width) // 2
            y = (window.winfo_screenheight() - height) // 2
    except TclError:
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


# ============================================================
# MAIN STUDENT FEE MANAGEMENT PAGE
# ============================================================

def open_student_fee_management(
    parent,
    user_role="Admin"
):

    # ========================================================
    # ROLE
    # ========================================================

    role = str(
        user_role
    ).strip().lower()

    is_accountant = (
        role == "accountant"
    )


    # ========================================================
    # CLEAR PARENT
    # ========================================================

    for widget in parent.winfo_children():

        widget.destroy()


    parent.configure(
        bg=BG
    )


    # ========================================================
    # VARIABLES
    # ========================================================

    search_var = StringVar()

    course_filter_var = StringVar(
        value="All Courses"
    )

    semester_filter_var = StringVar(
        value="All Semesters"
    )

    status_filter_var = StringVar(
        value="All Status"
    )


    total_assigned_var = StringVar(
        value="₹0.00"
    )

    total_collected_var = StringVar(
        value="₹0.00"
    )

    total_due_var = StringVar(
        value="₹0.00"
    )

    paid_students_var = StringVar(
        value="0"
    )


    # ========================================================
    # MAIN CONTAINER
    # ========================================================

    main_container = Frame(
        parent,
        bg=BG
    )

    main_container.pack(
        fill=BOTH,
        expand=True,
        padx=28,
        pady=22
    )


    # ========================================================
    # HEADER
    # ========================================================

    header = Frame(
        main_container,
        bg=BG
    )

    header.pack(
        fill=X,
        pady=(0, 18)
    )


    header_left = Frame(
        header,
        bg=BG
    )

    header_left.pack(
        side=LEFT
    )


    Label(
        header_left,
        text="Student Fees",
        bg=BG,
        fg=TEXT,
        font=(
            "Helvetica",
            22,
            "bold"
        )
    ).pack(
        anchor="w"
    )


    Label(
        header_left,
        text=(
            "View each student once and manage all assigned fee structures together."
        ),
        bg=BG,
        fg=GRAY,
        font=(
            "Helvetica",
            10
        )
    ).pack(
        anchor="w",
        pady=(4, 0)
    )


    # ========================================================
    # SUMMARY CARDS
    # ========================================================

    summary_frame = Frame(
        main_container,
        bg=BG
    )

    summary_frame.pack(
        fill=X,
        pady=(0, 18)
    )


    for column in range(4):

        summary_frame.grid_columnconfigure(
            column,
            weight=1,
            uniform="summary"
        )


    # ========================================================
    # CREATE SUMMARY CARD
    # ========================================================

    def create_summary_card(
        column,
        title,
        variable,
        value_color
    ):

        card = Frame(
            summary_frame,
            bg=WHITE,
            highlightbackground=LIGHT_BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=(
                0 if column == 0 else 7,
                0 if column == 3 else 7
            )
        )


        Label(
            card,
            text=title,
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 7)
        )


        Label(
            card,
            textvariable=variable,
            bg=WHITE,
            fg=value_color,
            font=(
                "Helvetica",
                18,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )


    create_summary_card(
        0,
        "TOTAL ASSIGNED",
        total_assigned_var,
        BLUE
    )


    create_summary_card(
        1,
        "TOTAL COLLECTED",
        total_collected_var,
        GREEN
    )


    create_summary_card(
        2,
        "TOTAL DUE",
        total_due_var,
        RED
    )


    create_summary_card(
        3,
        "PAID STUDENTS",
        paid_students_var,
        PURPLE
    )


    # ========================================================
    # FILTER CARD
    # ========================================================

    filter_card = Frame(
        main_container,
        bg=WHITE,
        highlightbackground=LIGHT_BORDER,
        highlightthickness=1
    )

    filter_card.pack(
        fill=X,
        pady=(0, 15)
    )


    filter_inner = Frame(
        filter_card,
        bg=WHITE
    )

    filter_inner.pack(
        fill=X,
        padx=18,
        pady=15
    )


    # ========================================================
    # SEARCH
    # ========================================================

    search_entry = Entry(
        filter_inner,
        textvariable=search_var,
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
        ipady=8
    )


    # ========================================================
    # COURSE FILTER
    # ========================================================

    course_filter = ttk.Combobox(
        filter_inner,
        textvariable=course_filter_var,
        state="readonly",
        width=20,
        font=(
            "Helvetica",
            9
        )
    )

    course_filter.pack(
        side=LEFT,
        padx=(10, 0),
        ipady=5
    )


    # ========================================================
    # SEMESTER FILTER
    # ========================================================

    semester_filter = ttk.Combobox(
        filter_inner,
        textvariable=semester_filter_var,
        values=[
            "All Semesters",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8"
        ],
        state="readonly",
        width=14,
        font=(
            "Helvetica",
            9
        )
    )

    semester_filter.pack(
        side=LEFT,
        padx=(10, 0),
        ipady=5
    )


    # ========================================================
    # STATUS FILTER
    # ========================================================

    status_filter = ttk.Combobox(
        filter_inner,
        textvariable=status_filter_var,
        values=[
            "All Status",
            "Unpaid",
            "Partial",
            "Paid"
        ],
        state="readonly",
        width=13,
        font=(
            "Helvetica",
            9
        )
    )

    status_filter.pack(
        side=LEFT,
        padx=(10, 0),
        ipady=5
    )


    # ========================================================
    # TABLE CARD
    # ========================================================

    table_card = Frame(
        main_container,
        bg=WHITE,
        highlightbackground=LIGHT_BORDER,
        highlightthickness=1
    )

    table_card.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # TABLE HEADER
    # ========================================================

    table_top = Frame(
        table_card,
        bg=WHITE
    )

    table_top.pack(
        fill=X,
        padx=18,
        pady=(15, 12)
    )


    table_title_frame = Frame(
        table_top,
        bg=WHITE
    )

    table_title_frame.pack(
        side=LEFT
    )


    Label(
        table_title_frame,
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


    record_count_var = StringVar(
        value="0 records"
    )


    Label(
        table_title_frame,
        textvariable=record_count_var,
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            9
        )
    ).pack(
        anchor="w",
        pady=(3, 0)
    )


    # ========================================================
    # TREEVIEW STYLE
    # ========================================================

    style = ttk.Style()

    style.configure(
        "StudentFee.Treeview",
        background=WHITE,
        foreground=TEXT,
        rowheight=42,
        fieldbackground=WHITE,
        borderwidth=0,
        font=(
            "Helvetica",
            9
        )
    )


    style.configure(
        "StudentFee.Treeview.Heading",
        background=BG,
        foreground=GRAY,
        font=(
            "Helvetica",
            8,
            "bold"
        ),
        relief=FLAT
    )


    style.map(
        "StudentFee.Treeview",
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


    # ========================================================
    # TABLE CONTAINER
    # ========================================================

    tree_container = Frame(
        table_card,
        bg=WHITE
    )

    tree_container.pack(
        fill=BOTH,
        expand=True,
        padx=18,
        pady=(0, 10)
    )


    columns = (
        "registration_no",
        "name",
        "course",
        "semester",
        "fee_count",
        "academic_year",
        "total_fee",
        "paid",
        "due",
        "status"
    )


    fee_tree = ttk.Treeview(
        tree_container,
        columns=columns,
        show="headings",
        style="StudentFee.Treeview"
    )


    # ========================================================
    # HEADINGS
    # ========================================================

    fee_tree.heading(
        "registration_no",
        text="STUDENT ID"
    )

    fee_tree.heading(
        "name",
        text="STUDENT NAME"
    )

    fee_tree.heading(
        "course",
        text="COURSE"
    )

    fee_tree.heading(
        "semester",
        text="CURRENT SEM"
    )

    fee_tree.heading(
        "fee_count",
        text="FEES"
    )

    fee_tree.heading(
        "academic_year",
        text="ACADEMIC YEAR(S)"
    )

    fee_tree.heading(
        "total_fee",
        text="TOTAL FEE"
    )

    fee_tree.heading(
        "paid",
        text="PAID"
    )

    fee_tree.heading(
        "due",
        text="DUE"
    )

    fee_tree.heading(
        "status",
        text="STATUS"
    )


    # ========================================================
    # COLUMN WIDTHS
    # ========================================================

    fee_tree.column(
        "registration_no",
        width=100,
        minwidth=90,
        anchor=W
    )

    fee_tree.column(
        "name",
        width=150,
        minwidth=120,
        anchor=W
    )

    fee_tree.column(
        "course",
        width=160,
        minwidth=130,
        anchor=W
    )

    fee_tree.column(
        "semester",
        width=85,
        minwidth=75,
        anchor=CENTER
    )

    fee_tree.column(
        "fee_count",
        width=60,
        minwidth=55,
        anchor=CENTER
    )

    fee_tree.column(
        "academic_year",
        width=100,
        minwidth=90,
        anchor=CENTER
    )

    fee_tree.column(
        "total_fee",
        width=100,
        minwidth=90,
        anchor=E
    )

    fee_tree.column(
        "paid",
        width=100,
        minwidth=90,
        anchor=E
    )

    fee_tree.column(
        "due",
        width=100,
        minwidth=90,
        anchor=E
    )

    fee_tree.column(
        "status",
        width=85,
        minwidth=80,
        anchor=CENTER
    )


    # ========================================================
    # SCROLLBARS
    # ========================================================

    vertical_scrollbar = ttk.Scrollbar(
        tree_container,
        orient=VERTICAL,
        command=fee_tree.yview
    )


    horizontal_scrollbar = ttk.Scrollbar(
        tree_container,
        orient=HORIZONTAL,
        command=fee_tree.xview
    )


    fee_tree.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set
    )


    fee_tree.grid(
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


    tree_container.grid_rowconfigure(
        0,
        weight=1
    )


    tree_container.grid_columnconfigure(
        0,
        weight=1
    )


    # ========================================================
    # BOTTOM ACTION BAR
    # ========================================================

    action_bar = Frame(
        table_card,
        bg=WHITE
    )

    action_bar.pack(
        fill=X,
        padx=18,
        pady=(0, 15)
    )


    selected_record_var = StringVar(
        value="Select a student to view all assigned fee structures."
    )


    Label(
        action_bar,
        textvariable=selected_record_var,
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            9
        )
    ).pack(
        side=LEFT
    )


    # ========================================================
    # GET SELECTED STUDENT FEE ID
    # ========================================================

    def get_selected_registration_no():

        selected_items = fee_tree.selection()

        if not selected_items:

            messagebox.showwarning(
                "No Selection",
                "Please select a student first.",
                parent=parent
            )

            return None

        item = selected_items[0]

        values = fee_tree.item(
            item,
            "values"
        )

        if not values:

            return None

        return str(
            values[0]
        ).strip()

    def on_tree_select(
        event=None
    ):

        selected_items = (
            fee_tree.selection()
        )


        if not selected_items:

            selected_record_var.set(
                "Select a student to view all assigned fee structures."
            )

            return


        values = fee_tree.item(
            selected_items[0],
            "values"
        )


        if values:

            selected_record_var.set(
                (
                    f"Selected: "
                    f"{values[0]} - {values[1]}"
                )
            )


    fee_tree.bind(
        "<<TreeviewSelect>>",
        on_tree_select
    )


    # ========================================================
    # LOAD COURSE FILTER
    # ========================================================

    def load_course_filter():

        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()


            cursor.execute(
                """
                SELECT
                    Course_Name

                FROM courses

                WHERE
                    LOWER(TRIM(Status)) = 'active'

                ORDER BY
                    Course_Name
                """
            )


            records = (
                cursor.fetchall()
            )


            courses = [
                "All Courses"
            ]


            for record in records:

                courses.append(
                    str(record[0])
                )


            course_filter[
                "values"
            ] = courses


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load courses."
                    f"\n\n{error}"
                ),
                parent=parent
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
    # LOAD SUMMARY
    # ========================================================

    def load_summary():

        con = None
        cursor = None

        try:

            con = get_connection()
            cursor = con.cursor()

            cursor.execute(
                """
                SELECT
                    COALESCE(SUM(Total_Fee), 0),
                    COALESCE(SUM(Amount_Paid), 0),
                    COALESCE(SUM(Due_Amount), 0)
                FROM student_fees
                """
            )

            record = cursor.fetchone()

            # The first three values are assignment totals.
            # Count paid students separately to avoid counting the same
            # student once for every fee structure.
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM (
                    SELECT
                        Registration_No
                    FROM student_fees
                    GROUP BY Registration_No
                    HAVING COALESCE(SUM(Due_Amount), 0) <= 0
                ) paid_student_list
                """
            )

            paid_record = cursor.fetchone()

            if record:

                total_assigned = float(record[0] or 0)
                total_collected = float(record[1] or 0)
                total_due = float(record[2] or 0)
                paid_students = int(
                    paid_record[0] if paid_record else 0
                )

                total_assigned_var.set(
                    f"₹{total_assigned:,.2f}"
                )

                total_collected_var.set(
                    f"₹{total_collected:,.2f}"
                )

                total_due_var.set(
                    f"₹{total_due:,.2f}"
                )

                paid_students_var.set(
                    str(paid_students)
                )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load fee summary."
                    f"\n\n{error}"
                ),
                parent=parent
            )

        finally:

            if cursor is not None:
                cursor.close()

            if (
                con is not None
                and con.is_connected()
            ):
                con.close()

    def load_student_fees(
        event=None
    ):

        # One table row represents one student.
        # Multiple fee structures are aggregated into that same row.
        for item in fee_tree.get_children():

            fee_tree.delete(
                item
            )

        keyword = search_var.get().strip()
        course_value = course_filter_var.get().strip()
        semester_value = semester_filter_var.get().strip()
        status_value = status_filter_var.get().strip()
        search_pattern = f"%{keyword}%"

        con = None
        cursor = None

        try:

            con = get_connection()
            cursor = con.cursor()

            query = """
                SELECT
                    sf.Registration_No,
                    r.Name,
                    sd.Course,
                    sd.Semester AS Current_Semester,
                    COUNT(sf.Student_Fee_ID) AS Fee_Count,
                    GROUP_CONCAT(
                        DISTINCT fs.Academic_Year
                        ORDER BY fs.Academic_Year
                        SEPARATOR ', '
                    ) AS Academic_Years,
                    COALESCE(SUM(sf.Total_Fee), 0) AS Total_Fee,
                    COALESCE(SUM(sf.Amount_Paid), 0) AS Amount_Paid,
                    COALESCE(SUM(sf.Due_Amount), 0) AS Due_Amount,
                    CASE
                        WHEN COALESCE(SUM(sf.Due_Amount), 0) <= 0
                            THEN 'Paid'
                        WHEN COALESCE(SUM(sf.Amount_Paid), 0) > 0
                            THEN 'Partial'
                        ELSE 'Unpaid'
                    END AS Combined_Status
                FROM student_fees sf
                INNER JOIN registration r
                    ON r.Registration_No = sf.Registration_No
                INNER JOIN student_details sd
                    ON sd.Registration_No = sf.Registration_No
                INNER JOIN fee_structures fs
                    ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
                WHERE
                (
                    %s = ''
                    OR sf.Registration_No LIKE %s
                    OR r.Name LIKE %s
                    OR sd.Course LIKE %s
                )
            """

            parameters = [
                keyword,
                search_pattern,
                search_pattern,
                search_pattern
            ]

            if (
                course_value
                and
                course_value != "All Courses"
            ):

                query += """
                    AND sd.Course = %s
                """

                parameters.append(
                    course_value
                )

            # Semester filter checks assigned fee structures.
            # This means a student with Sem 1 and Sem 2 fees still appears
            # when either assigned semester is selected.
            if (
                semester_value
                and
                semester_value != "All Semesters"
            ):

                query += """
                    AND fs.Semester = %s
                """

                parameters.append(
                    int(semester_value)
                )

            query += """
                GROUP BY
                    sf.Registration_No,
                    r.Name,
                    sd.Course,
                    sd.Semester
            """

            if (
                status_value
                and
                status_value != "All Status"
            ):

                if status_value == "Paid":
                    query += """
                        HAVING COALESCE(SUM(sf.Due_Amount), 0) <= 0
                    """

                elif status_value == "Partial":
                    query += """
                        HAVING
                            COALESCE(SUM(sf.Amount_Paid), 0) > 0
                            AND COALESCE(SUM(sf.Due_Amount), 0) > 0
                    """

                elif status_value == "Unpaid":
                    query += """
                        HAVING COALESCE(SUM(sf.Amount_Paid), 0) <= 0
                    """

            query += """
                ORDER BY r.Name ASC
            """

            cursor.execute(
                query,
                tuple(parameters)
            )

            records = cursor.fetchall()

            for record in records:

                registration_no = record[0]
                student_name = record[1]
                course = record[2]
                current_semester = record[3]
                fee_count = int(record[4] or 0)
                academic_years = record[5] or "-"
                total_fee = float(record[6] or 0)
                amount_paid = float(record[7] or 0)
                due_amount = float(record[8] or 0)
                payment_status = record[9]

                fee_tree.insert(
                    "",
                    END,
                    iid=str(registration_no),
                    values=(
                        registration_no,
                        student_name,
                        course,
                        current_semester,
                        fee_count,
                        academic_years,
                        f"₹{total_fee:,.2f}",
                        f"₹{amount_paid:,.2f}",
                        f"₹{due_amount:,.2f}",
                        payment_status
                    )
                )

            count = len(records)

            record_count_var.set(
                (
                    "1 student"
                    if count == 1
                    else f"{count} students"
                )
            )

            selected_record_var.set(
                "Select a student to view all assigned fee structures."
            )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load student fees."
                    f"\n\n{error}"
                ),
                parent=parent
            )

        finally:

            if cursor is not None:
                cursor.close()

            if (
                con is not None
                and con.is_connected()
            ):
                con.close()

    def refresh_page():

        load_summary()

        load_student_fees()


    # ========================================================
    # CLEAR FILTERS
    # ========================================================

    def clear_filters():

        search_var.set("")

        course_filter_var.set(
            "All Courses"
        )

        semester_filter_var.set(
            "All Semesters"
        )

        status_filter_var.set(
            "All Status"
        )

        load_student_fees()


    # ========================================================
    # PAYMENT RECEIPT / BILL
    # ========================================================

    def load_payment_receipt(payment_id):

        con = None
        cursor = None

        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    fp.Payment_ID,
                    fp.Amount,
                    fp.Payment_Mode,
                    fp.Transaction_Reference,
                    fp.Remarks,
                fp.Collected_By,
                    fp.Payment_Date,
                    sf.Registration_No,
                    sf.Total_Fee,
                    sf.Amount_Paid,
                    sf.Due_Amount,
                    sf.Payment_Status,
                    r.Name,
                    sd.Course,
                    sd.Semester,
                    fs.Academic_Year
                FROM fee_payments fp
                INNER JOIN student_fees sf
                    ON sf.Student_Fee_ID = fp.Student_Fee_ID
                INNER JOIN registration r
                    ON r.Registration_No = sf.Registration_No
                INNER JOIN student_details sd
                    ON sd.Registration_No = sf.Registration_No
                INNER JOIN fee_structures fs
                    ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
                WHERE fp.Payment_ID = %s
                """,
                (payment_id,)
            )

            return cursor.fetchone()

        finally:
            if cursor is not None:
                cursor.close()

            if con is not None and con.is_connected():
                con.close()


    def generate_receipt_image(receipt, output_path):

        if not PIL_AVAILABLE:
            raise RuntimeError(
                "Pillow is required for image generation. Run: pip install pillow"
            )

        width = 1100
        height = 1450

        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        def get_font(size, bold=False):
            paths = (
                ["C:/Windows/Fonts/arialbd.ttf", "DejaVuSans-Bold.ttf"]
                if bold
                else ["C:/Windows/Fonts/arial.ttf", "DejaVuSans.ttf"]
            )

            for font_path in paths:
                try:
                    return ImageFont.truetype(font_path, size)
                except Exception:
                    pass

            return ImageFont.load_default()

        title_font = get_font(48, True)
        subtitle_font = get_font(24)
        section_font = get_font(25, True)
        label_font = get_font(21)
        value_font = get_font(23, True)
        amount_font = get_font(44, True)
        small_font = get_font(18)

        margin = 70

        draw.rectangle((0, 0, width, 185), fill="#2563EB")
        draw.text((margin, 48), "FEE PAYMENT RECEIPT", fill="white", font=title_font)
        draw.text((margin, 118), "Fee Status Management System", fill="white", font=subtitle_font)

        y = 235
        draw.text(
            (margin, y),
            f"Receipt No: PAY-{int(receipt['Payment_ID']):06d}",
            fill="#0F172A",
            font=section_font
        )
        draw.text(
            (width - 390, y),
            f"Date: {receipt['Payment_Date']}",
            fill="#0F172A",
            font=section_font
        )

        y += 75
        draw.line((margin, y, width - margin, y), fill="#CBD5E1", width=2)
        y += 45
        draw.text((margin, y), "STUDENT INFORMATION", fill="#2563EB", font=section_font)
        y += 55

        student_rows = [
            ("Student Name", receipt["Name"]),
            ("Registration No.", receipt["Registration_No"]),
            ("Course", receipt["Course"]),
            ("Semester", receipt["Semester"]),
            ("Academic Year", receipt["Academic_Year"])
        ]

        for label, value in student_rows:
            draw.text((margin, y), str(label), fill="#64748B", font=label_font)
            draw.text((400, y), str(value), fill="#0F172A", font=value_font)
            y += 55

        y += 20
        draw.line((margin, y, width - margin, y), fill="#CBD5E1", width=2)
        y += 45
        draw.text((margin, y), "PAYMENT DETAILS", fill="#2563EB", font=section_font)
        y += 55

        payment_rows = [
            ("Payment ID", f"PAY-{int(receipt['Payment_ID']):06d}"),
            ("Payment Mode", receipt["Payment_Mode"]),
            ("Transaction Reference", receipt["Transaction_Reference"] or "-"),
            ("Collected By", receipt.get("Collected_By") or "-"),
            ("Remarks", receipt["Remarks"] or "-")
        ]

        for label, value in payment_rows:
            draw.text((margin, y), str(label), fill="#64748B", font=label_font)
            draw.text((400, y), str(value), fill="#0F172A", font=value_font)
            y += 55

        y += 25
        draw.rounded_rectangle(
            (margin, y, width - margin, y + 155),
            radius=18,
            fill="#EFF6FF",
            outline="#BFDBFE",
            width=2
        )
        draw.text((margin + 35, y + 28), "AMOUNT PAID", fill="#64748B", font=section_font)
        draw.text(
            (margin + 35, y + 72),
            f"Rs. {float(receipt['Amount']):,.2f}",
            fill="#16A34A",
            font=amount_font
        )

        y += 205
        draw.line((margin, y, width - margin, y), fill="#CBD5E1", width=2)
        y += 45
        draw.text((margin, y), "CURRENT FEE SUMMARY", fill="#2563EB", font=section_font)
        y += 60

        summary_rows = [
            ("Total Fee", f"Rs. {float(receipt['Total_Fee']):,.2f}"),
            ("Total Paid", f"Rs. {float(receipt['Amount_Paid']):,.2f}"),
            ("Due Amount", f"Rs. {float(receipt['Due_Amount']):,.2f}"),
            ("Payment Status", receipt["Payment_Status"])
        ]

        for label, value in summary_rows:
            draw.text((margin, y), str(label), fill="#64748B", font=label_font)
            draw.text((650, y), str(value), fill="#0F172A", font=value_font)
            y += 55

        draw.text(
            (margin, height - 120),
            "This is a computer-generated payment receipt.",
            fill="#64748B",
            font=small_font
        )
        draw.text(
            (margin, height - 80),
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            fill="#64748B",
            font=small_font
        )

        image.save(output_path, "PNG")


    def open_payment_receipt(
        payment_id,
        owner_window
    ):

        receipt = load_payment_receipt(
            payment_id
        )


        if receipt is None:

            messagebox.showerror(
                "Receipt Error",
                "Payment receipt data was not found.",
                parent=owner_window
            )

            return


        receipt_window = Toplevel(
            owner_window
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
            owner_window
        )


        # ----------------------------------------------------
        # SMALLER RECEIPT + FIXED HIGHER Y POSITION
        # ----------------------------------------------------

        receipt_width = 600
        receipt_height = 690

        screen_width = (
            receipt_window.winfo_screenwidth()
        )

        receipt_x = max(
            10,
            int(
                (
                    screen_width
                    -
                    receipt_width
                )
                /
                2
            )
        )

        receipt_y = 25


        receipt_window.geometry(
            f"{receipt_width}x{receipt_height}"
            f"+{receipt_x}+{receipt_y}"
        )


        try:

            owner_window.grab_release()

        except TclError:

            pass


        def close_receipt():

            try:

                receipt_window.grab_release()

            except TclError:

                pass


            receipt_window.destroy()


            if (
                owner_window is not None
                and
                owner_window.winfo_exists()
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
        # HEADER
        # ====================================================

        receipt_header = Frame(
            receipt_window,
            bg=BLUE,
            height=105
        )

        receipt_header.pack(
            fill=X
        )

        receipt_header.pack_propagate(
            False
        )


        Label(
            receipt_header,
            text="FEE PAYMENT RECEIPT",
            bg=BLUE,
            fg=WHITE,
            font=(
                "Helvetica",
                21,
                "bold"
            )
        ).place(
            x=28,
            y=22
        )


        Label(
            receipt_header,
            text=(
                "Receipt No: "
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
            y=67
        )


        # ====================================================
        # BOTTOM ACTION BAR - ALWAYS VISIBLE
        # ====================================================

        receipt_actions = Frame(
            receipt_window,
            bg=WHITE,
            height=72,
            highlightbackground=LIGHT_BORDER,
            highlightthickness=1
        )

        receipt_actions.pack(
            side=BOTTOM,
            fill=X
        )

        receipt_actions.pack_propagate(
            False
        )

        Button(
            receipt_actions,
            text="CLOSE",
            bg=RED,
            fg=WHITE,
            activebackground="#B91C1C",
            activeforeground=WHITE,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=close_receipt
        ).pack(
            side=RIGHT,
            padx=(
                6,
                24
            ),
            pady=14,
            ipadx=22,
            ipady=8
        )


        # ====================================================
        # RECEIPT BODY
        # ====================================================

        receipt_body = Frame(
            receipt_window,
            bg=WHITE,
            highlightbackground=LIGHT_BORDER,
            highlightthickness=1
        )

        receipt_body.pack(
            fill=BOTH,
            expand=True,
            padx=24,
            pady=(
                18,
                14
            )
        )


        info_frame = Frame(
            receipt_body,
            bg=WHITE
        )

        info_frame.pack(
            fill=X,
            padx=24,
            pady=(
                15,
                6
            )
        )


        def receipt_row(
            label_text,
            value_text
        ):

            row = Frame(
                info_frame,
                bg=WHITE,
                height=28
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
                    8,
                    "bold"
                ),
                anchor=W
            ).place(
                x=0,
                y=5,
                width=155
            )


            Label(
                row,
                text=str(
                    value_text
                ),
                bg=WHITE,
                fg=TEXT,
                font=(
                    "Helvetica",
                    9,
                    "bold"
                ),
                anchor=W
            ).place(
                x=165,
                y=4,
                width=320
            )


        receipt_row(
            "Student",
            receipt["Name"]
        )

        receipt_row(
            "Registration No.",
            receipt["Registration_No"]
        )

        receipt_row(
            "Course",
            receipt["Course"]
        )

        receipt_row(
            "Semester",
            receipt["Semester"]
        )

        receipt_row(
            "Academic Year",
            receipt["Academic_Year"]
        )

        receipt_row(
            "Payment Date",
            receipt["Payment_Date"]
        )

        receipt_row(
            "Payment Mode",
            receipt["Payment_Mode"]
        )

        receipt_row(
            "Transaction Reference",
            receipt["Transaction_Reference"]
            or "-"
        )

        receipt_row(
            "Collected By",
            receipt.get(
                "Collected_By"
            )
            or "-"
        )


        Frame(
            receipt_body,
            bg=LIGHT_BORDER,
            height=1
        ).pack(
            fill=X,
            padx=24,
            pady=(
                3,
                9
            )
        )


        # ====================================================
        # AMOUNT PAID
        # ====================================================

        amount_box = Frame(
            receipt_body,
            bg=LIGHT_GREEN,
            highlightbackground="#BBF7D0",
            highlightthickness=1,
            height=80
        )

        amount_box.pack(
            fill=X,
            padx=24
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
        ).place(
            x=20,
            y=13
        )


        Label(
            amount_box,
            text=(
                f"₹"
                f"{float(receipt['Amount']):,.2f}"
            ),
            bg=LIGHT_GREEN,
            fg=GREEN,
            font=(
                "Helvetica",
                20,
                "bold"
            )
        ).place(
            x=20,
            y=35
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        summary_frame = Frame(
            receipt_body,
            bg=WHITE
        )

        summary_frame.pack(
            fill=X,
            padx=24,
            pady=(
                10,
                4
            )
        )


        def summary_row(
            label_text,
            value_text,
            value_color=TEXT
        ):

            row = Frame(
                summary_frame,
                bg=WHITE,
                height=26
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
                    8,
                    "bold"
                ),
                anchor=W
            ).pack(
                side=LEFT
            )


            Label(
                row,
                text=value_text,
                bg=WHITE,
                fg=value_color,
                font=(
                    "Helvetica",
                    9,
                    "bold"
                ),
                anchor=E
            ).pack(
                side=RIGHT
            )


        summary_row(
            "Total Fee",
            f"₹{float(receipt['Total_Fee']):,.2f}"
        )

        summary_row(
            "Total Paid",
            f"₹{float(receipt['Amount_Paid']):,.2f}",
            GREEN
        )

        summary_row(
            "Due Amount",
            f"₹{float(receipt['Due_Amount']):,.2f}",
            RED
        )

        summary_row(
            "Status",
            receipt["Payment_Status"],
            (
                GREEN
                if
                str(
                    receipt["Payment_Status"]
                ).lower()
                ==
                "paid"
                else
                ORANGE
            )
        )


        receipt_window.update_idletasks()

        receipt_window.lift()

        receipt_window.focus_force()


        try:

            receipt_window.grab_set()

        except TclError:

            pass


    def view_student_fee():

        registration_no = (
            get_selected_registration_no()
        )

        if registration_no is None:
            return

        con = None
        cursor = None

        try:

            con = get_connection()
            cursor = con.cursor(
                dictionary=True
            )

            # Load every fee assignment for the selected student.
            cursor.execute(
                """
                SELECT
                    sf.Student_Fee_ID,
                    sf.Registration_No,
                    r.Name,
                    sd.Course,
                    sd.Semester AS Current_Semester,
                    fs.Semester AS Fee_Semester,
                    fs.Academic_Year,
                    sf.Fee_Structure_ID,
                    sf.Total_Fee,
                    sf.Amount_Paid,
                    sf.Due_Amount,
                    sf.Payment_Status,
                    sf.Assigned_At
                FROM student_fees sf
                INNER JOIN registration r
                    ON r.Registration_No = sf.Registration_No
                INNER JOIN student_details sd
                    ON sd.Registration_No = sf.Registration_No
                INNER JOIN fee_structures fs
                    ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
                WHERE sf.Registration_No = %s
                ORDER BY
                    fs.Semester ASC,
                    fs.Academic_Year ASC,
                    sf.Student_Fee_ID ASC
                """,
                (
                    registration_no,
                )
            )

            fee_records = cursor.fetchall()

            if not fee_records:

                messagebox.showerror(
                    "Not Found",
                    "No fee assignments were found for this student.",
                    parent=parent
                )

                return

            for fee_record in fee_records:

                cursor.execute(
                    """
                    SELECT
                        Fee_Type,
                        Amount
                    FROM fee_structure_components
                    WHERE Fee_Structure_ID = %s
                    ORDER BY Component_ID
                    """,
                    (
                        fee_record["Fee_Structure_ID"],
                    )
                )

                fee_record["Components"] = cursor.fetchall()

                cursor.execute(
                    """
                    SELECT
                        Payment_ID,
                        Amount,
                        Payment_Mode,
                        Transaction_Reference,
                        Remarks,
                        Collected_By,
                        Payment_Date,
                        Created_At
                    FROM fee_payments
                    WHERE Student_Fee_ID = %s
                    ORDER BY
                        Payment_Date DESC,
                        Payment_ID DESC
                    """,
                    (
                        fee_record["Student_Fee_ID"],
                    )
                )

                fee_record["Payments"] = cursor.fetchall()

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load fee details."
                    f"\n\n{error}"
                ),
                parent=parent
            )

            return

        finally:

            if cursor is not None:
                cursor.close()

            if (
                con is not None
                and con.is_connected()
            ):
                con.close()

        first = fee_records[0]

        combined_total = sum(
            float(record["Total_Fee"] or 0)
            for record in fee_records
        )

        combined_paid = sum(
            float(record["Amount_Paid"] or 0)
            for record in fee_records
        )

        combined_due = sum(
            float(record["Due_Amount"] or 0)
            for record in fee_records
        )

        details_window = Toplevel(
            parent
        )

        details_window.title(
            "Student Fee Details"
        )

        center_window(
            details_window,
            980,
            720,
            parent
        )

        details_window.minsize(
            860,
            620
        )

        details_window.configure(
            bg=BG
        )

        details_window.transient(
            parent.winfo_toplevel()
        )

        details_window.grab_set()

        # Header
        details_header = Frame(
            details_window,
            bg=BG
        )

        details_header.pack(
            fill=X,
            padx=30,
            pady=(20, 12)
        )

        Label(
            details_header,
            text="Student Fee Details",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                20,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        Label(
            details_header,
            text=(
                f"{first['Registration_No']}  •  "
                f"{first['Name']}  •  "
                f"{len(fee_records)} assigned fee structure"
                f"{'' if len(fee_records) == 1 else 's'}"
            ),
            bg=BG,
            fg=GRAY,
            font=(
                "Helvetica",
                10
            )
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        # Combined summary
        combined_card = Frame(
            details_window,
            bg=WHITE,
            highlightbackground=LIGHT_BORDER,
            highlightthickness=1
        )

        combined_card.pack(
            fill=X,
            padx=30,
            pady=(0, 12)
        )

        student_info = Frame(
            combined_card,
            bg=WHITE
        )

        student_info.pack(
            fill=X,
            padx=20,
            pady=(14, 8)
        )

        Label(
            student_info,
            text=(
                f"Course: {first['Course']}     "
                f"Current Semester: {first['Current_Semester']}"
            ),
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                10,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        combined_summary = Frame(
            combined_card,
            bg=LIGHT_BLUE,
            highlightbackground="#BFDBFE",
            highlightthickness=1
        )

        combined_summary.pack(
            fill=X,
            padx=20,
            pady=(4, 16)
        )

        combined_values = [
            (
                "TOTAL ASSIGNED",
                combined_total,
                BLUE
            ),
            (
                "TOTAL PAID",
                combined_paid,
                GREEN
            ),
            (
                "TOTAL DUE",
                combined_due,
                RED
            )
        ]

        for column in range(3):
            combined_summary.grid_columnconfigure(
                column,
                weight=1
            )

        for index, (
            title,
            value,
            value_color
        ) in enumerate(combined_values):

            item = Frame(
                combined_summary,
                bg=LIGHT_BLUE
            )

            item.grid(
                row=0,
                column=index,
                sticky="ew",
                padx=18,
                pady=13
            )

            Label(
                item,
                text=title,
                bg=LIGHT_BLUE,
                fg=GRAY,
                font=(
                    "Helvetica",
                    8,
                    "bold"
                )
            ).pack(
                anchor="w"
            )

            Label(
                item,
                text=f"₹{value:,.2f}",
                bg=LIGHT_BLUE,
                fg=value_color,
                font=(
                    "Helvetica",
                    15,
                    "bold"
                )
            ).pack(
                anchor="w",
                pady=(5, 0)
            )

        # Scrollable area containing all fee structures.
        content_outer = Frame(
            details_window,
            bg=BG
        )

        content_outer.pack(
            fill=BOTH,
            expand=True,
            padx=30,
            pady=(0, 12)
        )

        details_canvas = Canvas(
            content_outer,
            bg=BG,
            highlightthickness=0
        )

        details_scrollbar = ttk.Scrollbar(
            content_outer,
            orient=VERTICAL,
            command=details_canvas.yview
        )

        fees_container = Frame(
            details_canvas,
            bg=BG
        )

        fees_container.bind(
            "<Configure>",
            lambda event: details_canvas.configure(
                scrollregion=details_canvas.bbox("all")
            )
        )

        canvas_window = details_canvas.create_window(
            (0, 0),
            window=fees_container,
            anchor="nw"
        )

        details_canvas.bind(
            "<Configure>",
            lambda event: details_canvas.itemconfigure(
                canvas_window,
                width=event.width
            )
        )

        details_canvas.configure(
            yscrollcommand=details_scrollbar.set
        )

        details_canvas.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        details_scrollbar.pack(
            side=RIGHT,
            fill=Y
        )

        # Every fee structure is displayed in this same details window.
        for index, fee_record in enumerate(
            fee_records,
            start=1
        ):

            fee_card = Frame(
                fees_container,
                bg=WHITE,
                highlightbackground=LIGHT_BORDER,
                highlightthickness=1
            )

            fee_card.pack(
                fill=X,
                pady=(0, 12)
            )

            fee_header = Frame(
                fee_card,
                bg=WHITE
            )

            fee_header.pack(
                fill=X,
                padx=20,
                pady=(14, 8)
            )

            Label(
                fee_header,
                text=(
                    f"FEE {index}  •  "
                    f"SEMESTER {fee_record['Fee_Semester']}  •  "
                    f"{fee_record['Academic_Year']}"
                ),
                bg=WHITE,
                fg=TEXT,
                font=(
                    "Helvetica",
                    11,
                    "bold"
                )
            ).pack(
                side=LEFT
            )

            status_text = str(
                fee_record["Payment_Status"] or "Unpaid"
            )

            if status_text.lower() == "paid":
                status_bg = LIGHT_GREEN
                status_fg = GREEN

            elif status_text.lower() == "partial":
                status_bg = LIGHT_ORANGE
                status_fg = ORANGE

            else:
                status_bg = LIGHT_RED
                status_fg = RED

            Label(
                fee_header,
                text=status_text.upper(),
                bg=status_bg,
                fg=status_fg,
                font=(
                    "Helvetica",
                    8,
                    "bold"
                ),
                padx=12,
                pady=5
            ).pack(
                side=RIGHT
            )

            fee_summary = Frame(
                fee_card,
                bg="#F8FAFC"
            )

            fee_summary.pack(
                fill=X,
                padx=20,
                pady=(0, 10)
            )

            fee_amounts = [
                (
                    "TOTAL FEE",
                    float(fee_record["Total_Fee"] or 0)
                ),
                (
                    "AMOUNT PAID",
                    float(fee_record["Amount_Paid"] or 0)
                ),
                (
                    "DUE AMOUNT",
                    float(fee_record["Due_Amount"] or 0)
                )
            ]

            for column in range(3):
                fee_summary.grid_columnconfigure(
                    column,
                    weight=1
                )

            for amount_index, (
                amount_title,
                amount_value
            ) in enumerate(fee_amounts):

                amount_frame = Frame(
                    fee_summary,
                    bg="#F8FAFC"
                )

                amount_frame.grid(
                    row=0,
                    column=amount_index,
                    sticky="ew",
                    padx=14,
                    pady=10
                )

                Label(
                    amount_frame,
                    text=amount_title,
                    bg="#F8FAFC",
                    fg=GRAY,
                    font=(
                        "Helvetica",
                        8,
                        "bold"
                    )
                ).pack(
                    anchor="w"
                )

                Label(
                    amount_frame,
                    text=f"₹{amount_value:,.2f}",
                    bg="#F8FAFC",
                    fg=TEXT,
                    font=(
                        "Helvetica",
                        12,
                        "bold"
                    )
                ).pack(
                    anchor="w",
                    pady=(4, 0)
                )

            # Fee components
            components_frame = Frame(
                fee_card,
                bg=WHITE
            )

            components_frame.pack(
                fill=X,
                padx=20,
                pady=(0, 10)
            )

            Label(
                components_frame,
                text="FEE COMPONENTS",
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

            components = fee_record.get(
                "Components",
                []
            )

            if components:

                for component in components:

                    component_row = Frame(
                        components_frame,
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
                        font=(
                            "Helvetica",
                            9
                        )
                    ).pack(
                        side=LEFT
                    )

                    Label(
                        component_row,
                        text=(
                            f"₹"
                            f"{float(component['Amount'] or 0):,.2f}"
                        ),
                        bg=WHITE,
                        fg=TEXT,
                        font=(
                            "Helvetica",
                            9,
                            "bold"
                        )
                    ).pack(
                        side=RIGHT
                    )

            else:

                Label(
                    components_frame,
                    text="No fee components found.",
                    bg=WHITE,
                    fg=GRAY,
                    font=(
                        "Helvetica",
                        9
                    )
                ).pack(
                    anchor="w"
                )

            # Payment history for this exact fee assignment.
            payments_frame = Frame(
                fee_card,
                bg=WHITE
            )

            payments_frame.pack(
                fill=X,
                padx=20,
                pady=(0, 14)
            )

            Label(
                payments_frame,
                text="PAYMENT HISTORY",
                bg=WHITE,
                fg=GRAY,
                font=(
                    "Helvetica",
                    8,
                    "bold"
                )
            ).pack(
                anchor="w",
                pady=(0, 6)
            )

            payments = fee_record.get(
                "Payments",
                []
            )

            if payments:

                payment_tree = ttk.Treeview(
                    payments_frame,
                    columns=(
                        "payment_id",
                        "date",
                        "amount",
                        "mode",
                        "collector"
                    ),
                    show="headings",
                    height=min(
                        4,
                        len(payments)
                    )
                )

                payment_tree.heading(
                    "payment_id",
                    text="PAYMENT ID"
                )

                payment_tree.heading(
                    "date",
                    text="DATE"
                )

                payment_tree.heading(
                    "amount",
                    text="AMOUNT"
                )

                payment_tree.heading(
                    "mode",
                    text="MODE"
                )

                payment_tree.heading(
                    "collector",
                    text="COLLECTED BY"
                )

                payment_tree.column(
                    "payment_id",
                    width=90,
                    anchor=CENTER
                )

                payment_tree.column(
                    "date",
                    width=130,
                    anchor=CENTER
                )

                payment_tree.column(
                    "amount",
                    width=120,
                    anchor=E
                )

                payment_tree.column(
                    "mode",
                    width=110,
                    anchor=CENTER
                )

                payment_tree.column(
                    "collector",
                    width=150,
                    anchor=W
                )

                for payment in payments:

                    payment_tree.insert(
                        "",
                        END,
                        values=(
                            payment["Payment_ID"],
                            payment["Payment_Date"],
                            (
                                f"₹"
                                f"{float(payment['Amount'] or 0):,.2f}"
                            ),
                            payment["Payment_Mode"],
                            payment["Collected_By"] or "-"
                        )
                    )

                payment_tree.pack(
                    fill=X
                )

                def open_selected_receipt(
                    event=None,
                    tree=payment_tree
                ):

                    selected_payment = tree.selection()

                    if not selected_payment:
                        return

                    payment_values = tree.item(
                        selected_payment[0],
                        "values"
                    )

                    if payment_values:

                        open_payment_receipt(
                            int(payment_values[0]),
                            details_window
                        )

                payment_tree.bind(
                    "<Double-1>",
                    open_selected_receipt
                )

            else:

                Label(
                    payments_frame,
                    text="No payments recorded for this fee structure.",
                    bg=WHITE,
                    fg=GRAY,
                    font=(
                        "Helvetica",
                        9
                    )
                ).pack(
                    anchor="w"
                )

        bottom_bar = Frame(
            details_window,
            bg=WHITE,
            height=65,
            highlightbackground=LIGHT_BORDER,
            highlightthickness=1
        )

        bottom_bar.pack(
            side=BOTTOM,
            fill=X
        )

        bottom_bar.pack_propagate(
            False
        )

        Button(
            bottom_bar,
            text="CLOSE",
            bg=RED,
            fg=WHITE,
            activebackground="#B91C1C",
            activeforeground=WHITE,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=details_window.destroy
        ).pack(
            side=RIGHT,
            padx=25,
            pady=13,
            ipadx=22,
            ipady=7
        )

        def scroll_details(event):

            try:
                details_canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )
            except Exception:
                pass

        details_window.bind(
            "<MouseWheel>",
            scroll_details
        )


    def open_student_on_row_click(
        event
    ):

        # Open the combined student fee details when the user
        # single-clicks anywhere on a valid student row.
        region = fee_tree.identify_region(
            event.x,
            event.y
        )

        if region != "cell":
            return

        row_id = fee_tree.identify_row(
            event.y
        )

        if not row_id:
            return

        fee_tree.selection_set(
            row_id
        )

        fee_tree.focus(
            row_id
        )

        on_tree_select()

        view_student_fee()


    def open_assign_fee_form():

        if not is_accountant:

            messagebox.showwarning(
                "Access Denied",
                (
                    "Only an Accountant can "
                    "assign fees to students."
                ),
                parent=parent
            )

            return


        assign_window = Toplevel(
            parent
        )

        assign_window.title(
            "Assign Fee to Student"
        )

        center_window(
            assign_window,
            700,
            650,
            parent
        )

        assign_window.minsize(
            650,
            580
        )

        assign_window.configure(
            bg=BG
        )

        assign_window.transient(
            parent.winfo_toplevel()
        )

        assign_window.grab_set()


        # ====================================================
        # VARIABLES
        # ====================================================

        student_var = StringVar()

        academic_year_var = StringVar(
            value=str(
                date.today().year
            )
        )


        student_map = {}


        selected_student_info_var = StringVar(
            value=(
                "Select an active student "
                "to preview the fee structure."
            )
        )


        fee_structure_info_var = StringVar(
            value="No fee structure selected."
        )


        total_preview_var = StringVar(
            value="TOTAL FEE: ₹0.00"
        )


        current_fee_structure_id = [
            None
        ]


        # ====================================================
        # HEADER
        # ====================================================

        Label(
            assign_window,
            text="Assign Fee to Student",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                20,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(22, 4)
        )


        Label(
            assign_window,
            text=(
                "Select an active student. "
                "The matching fee structure "
                "will be loaded automatically."
            ),
            bg=BG,
            fg=GRAY,
            font=(
                "Helvetica",
                9
            )
        ).pack(
            anchor="w",
            padx=30
        )


        # ====================================================
        # CARD
        # ====================================================

        assign_card = Frame(
            assign_window,
            bg=WHITE,
            highlightbackground=LIGHT_BORDER,
            highlightthickness=1
        )

        assign_card.pack(
            fill=BOTH,
            expand=True,
            padx=30,
            pady=(18, 20)
        )


        # ====================================================
        # STUDENT
        # ====================================================

        Label(
            assign_card,
            text="Student",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 7)
        )


        student_combo = ttk.Combobox(
            assign_card,
            textvariable=student_var,
            state="readonly",
            font=(
                "Helvetica",
                10
            )
        )

        student_combo.pack(
            fill=X,
            padx=22,
            ipady=6
        )


        # ====================================================
        # STUDENT INFORMATION
        # ====================================================

        Label(
            assign_card,
            textvariable=selected_student_info_var,
            bg=LIGHT_BLUE,
            fg=TEXT,
            font=(
                "Helvetica",
                9
            ),
            justify=LEFT,
            anchor="w"
        ).pack(
            fill=X,
            padx=22,
            pady=(12, 5),
            ipady=10
        )


        # ====================================================
        # ACADEMIC YEAR
        # ====================================================

        Label(
            assign_card,
            text="Academic Year",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(12, 7)
        )


        academic_year_entry = Entry(
            assign_card,
            textvariable=academic_year_var,
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

        academic_year_entry.pack(
            fill=X,
            padx=22,
            ipady=7
        )


        # ====================================================
        # LOAD FEE STRUCTURE BUTTON
        # ====================================================

        load_fee_button = Button(
            assign_card,
            text="LOAD FEE STRUCTURE",
            bg=PURPLE,
            fg=WHITE,
            activebackground=DARK_PURPLE,
            activeforeground=WHITE,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            )
        )

        load_fee_button.pack(
            anchor="e",
            padx=22,
            pady=(12, 10),
            ipadx=16,
            ipady=8
        )


        # ====================================================
        # FEE STRUCTURE INFO
        # ====================================================

        Label(
            assign_card,
            textvariable=fee_structure_info_var,
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(5, 7)
        )


        # ====================================================
        # COMPONENT PREVIEW
        # ====================================================

        preview_tree = ttk.Treeview(
            assign_card,
            columns=(
                "fee_type",
                "amount"
            ),
            show="headings",
            height=6
        )


        preview_tree.heading(
            "fee_type",
            text="FEE TYPE"
        )


        preview_tree.heading(
            "amount",
            text="AMOUNT"
        )


        preview_tree.column(
            "fee_type",
            width=400,
            anchor=W
        )


        preview_tree.column(
            "amount",
            width=180,
            anchor=E
        )


        preview_tree.pack(
            fill=BOTH,
            expand=True,
            padx=22,
            pady=(0, 10)
        )


        # ====================================================
        # TOTAL PREVIEW
        # ====================================================

        Label(
            assign_card,
            textvariable=total_preview_var,
            bg=LIGHT_GREEN,
            fg=GREEN,
            font=(
                "Helvetica",
                12,
                "bold"
            ),
            anchor="e"
        ).pack(
            fill=X,
            padx=22,
            pady=(0, 15),
            ipady=10
        )


        # ====================================================
        # LOAD STUDENTS
        # ====================================================

        def load_active_students():

            con = None
            cursor = None


            try:

                con = get_connection()

                cursor = con.cursor()


                cursor.execute(
                    """
                    SELECT
                        r.Registration_No,
                        r.Name,
                        sd.Course,
                        sd.Semester

                    FROM registration r

                    INNER JOIN student_details sd
                        ON
                            sd.Registration_No
                            =
                            r.Registration_No

                    WHERE
                        LOWER(
                            TRIM(
                                sd.Status
                            )
                        )
                        =
                        'active'

                    ORDER BY
                        r.Name
                    """
                )


                records = (
                    cursor.fetchall()
                )


                student_map.clear()

                display_values = []


                for (
                    registration_no,
                    student_name,
                    course,
                    semester
                ) in records:

                    display_text = (
                        f"{registration_no} - "
                        f"{student_name}"
                    )


                    student_map[
                        display_text
                    ] = {

                        "registration_no":
                            registration_no,

                        "name":
                            student_name,

                        "course":
                            course,

                        "semester":
                            semester
                    }


                    display_values.append(
                        display_text
                    )


                student_combo[
                    "values"
                ] = display_values


            except mysql.connector.Error as error:

                messagebox.showerror(
                    "Database Error",
                    (
                        "Could not load students."
                        f"\n\n{error}"
                    ),
                    parent=assign_window
                )


            finally:

                if cursor is not None:

                    cursor.close()


                if (
                    con is not None
                    and con.is_connected()
                ):

                    con.close()


        # ====================================================
        # STUDENT SELECTED
        # ====================================================

        def on_student_selected(
            event=None
        ):

            selected = (
                student_var
                .get()
                .strip()
            )


            if selected not in student_map:

                return


            student = (
                student_map[
                    selected
                ]
            )


            selected_student_info_var.set(
                (
                    f"Student ID: "
                    f"{student['registration_no']}     "
                    f"Course: {student['course']}     "
                    f"Semester: {student['semester']}"
                )
            )


            # Clear old preview
            current_fee_structure_id[0] = None

            fee_structure_info_var.set(
                "Click LOAD FEE STRUCTURE to preview."
            )

            total_preview_var.set(
                "TOTAL FEE: ₹0.00"
            )


            for item in (
                preview_tree
                .get_children()
            ):

                preview_tree.delete(
                    item
                )


        student_combo.bind(
            "<<ComboboxSelected>>",
            on_student_selected
        )


        # ====================================================
        # LOAD MATCHING FEE STRUCTURE
        # ====================================================

        def load_matching_fee_structure():

            selected = (
                student_var
                .get()
                .strip()
            )


            if selected not in student_map:

                messagebox.showwarning(
                    "Required Field",
                    (
                        "Please select "
                        "an active student."
                    ),
                    parent=assign_window
                )

                return


            academic_year = (
                academic_year_var
                .get()
                .strip()
            )


            if not academic_year:

                messagebox.showwarning(
                    "Required Field",
                    (
                        "Please enter the "
                        "Academic Year."
                    ),
                    parent=assign_window
                )

                return


            student = (
                student_map[
                    selected
                ]
            )


            con = None
            cursor = None


            try:

                con = get_connection()

                cursor = con.cursor(
                    dictionary=True
                )


                # ---------------------------------------------
                # MATCH:
                #
                # student_details.Course
                #        =
                # courses.Course_Name
                #
                # then use Course_ID
                # ---------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        fs.Fee_Structure_ID

                    FROM fee_structures fs

                    INNER JOIN courses c
                        ON
                            c.Course_ID
                            =
                            fs.Course_ID

                    WHERE
                        c.Course_Name = %s

                    AND
                        fs.Semester = %s

                    AND
                        fs.Academic_Year = %s

                    AND
                        LOWER(
                            TRIM(
                                fs.Status
                            )
                        )
                        =
                        'active'

                    ORDER BY
                        fs.Fee_Structure_ID DESC

                    LIMIT 1
                    """,
                    (
                        student["course"],
                        student["semester"],
                        academic_year
                    )
                )


                structure = (
                    cursor.fetchone()
                )


                if not structure:

                    current_fee_structure_id[
                        0
                    ] = None


                    fee_structure_info_var.set(
                        (
                            "No active fee structure found "
                            "for this Course, Semester "
                            "and Academic Year."
                        )
                    )


                    total_preview_var.set(
                        "TOTAL FEE: ₹0.00"
                    )


                    for item in (
                        preview_tree
                        .get_children()
                    ):

                        preview_tree.delete(
                            item
                        )


                    return


                fee_structure_id = (
                    structure[
                        "Fee_Structure_ID"
                    ]
                )


                current_fee_structure_id[
                    0
                ] = fee_structure_id


                # ---------------------------------------------
                # LOAD COMPONENTS
                # ---------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        Fee_Type,
                        Amount

                    FROM
                        fee_structure_components

                    WHERE
                        Fee_Structure_ID = %s

                    ORDER BY
                        Component_ID
                    """,
                    (
                        fee_structure_id,
                    )
                )


                components = (
                    cursor.fetchall()
                )


                # ---------------------------------------------
                # CLEAR PREVIEW
                # ---------------------------------------------

                for item in (
                    preview_tree
                    .get_children()
                ):

                    preview_tree.delete(
                        item
                    )


                # ---------------------------------------------
                # INSERT COMPONENTS
                # ---------------------------------------------

                total_fee = 0.0


                for component in components:

                    amount = float(
                        component[
                            "Amount"
                        ]
                    )


                    total_fee += amount


                    preview_tree.insert(
                        "",
                        END,
                        values=(
                            component[
                                "Fee_Type"
                            ],

                            f"₹{amount:,.2f}"
                        )
                    )


                fee_structure_info_var.set(
                    (
                        f"Fee Structure ID: "
                        f"{fee_structure_id}"
                    )
                )


                total_preview_var.set(
                    (
                        f"TOTAL FEE: "
                        f"₹{total_fee:,.2f}"
                    )
                )


            except mysql.connector.Error as error:

                messagebox.showerror(
                    "Database Error",
                    (
                        "Could not load the "
                        "matching fee structure."
                        f"\n\n{error}"
                    ),
                    parent=assign_window
                )


            finally:

                if cursor is not None:

                    cursor.close()


                if (
                    con is not None
                    and con.is_connected()
                ):

                    con.close()


        load_fee_button.config(
            command=load_matching_fee_structure
        )


        # ====================================================
        # ASSIGN FEE
        # ====================================================

        def assign_fee():

            selected = (
                student_var
                .get()
                .strip()
            )


            if selected not in student_map:

                messagebox.showwarning(
                    "Required Field",
                    (
                        "Please select "
                        "an active student."
                    ),
                    parent=assign_window
                )

                return


            fee_structure_id = (
                current_fee_structure_id[
                    0
                ]
            )


            if fee_structure_id is None:

                messagebox.showwarning(
                    "No Fee Structure",
                    (
                        "Please load a valid "
                        "fee structure first."
                    ),
                    parent=assign_window
                )

                return


            student = (
                student_map[
                    selected
                ]
            )


            registration_no = (
                student[
                    "registration_no"
                ]
            )


            con = None
            cursor = None


            try:

                con = get_connection()

                cursor = con.cursor()


                # ---------------------------------------------
                # CHECK DUPLICATE
                # ---------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        Student_Fee_ID

                    FROM student_fees

                    WHERE
                        Registration_No = %s

                    AND
                        Fee_Structure_ID = %s
                    """,
                    (
                        registration_no,
                        fee_structure_id
                    )
                )


                duplicate = (
                    cursor.fetchone()
                )


                if duplicate:

                    messagebox.showwarning(
                        "Already Assigned",
                        (
                            "This fee structure has "
                            "already been assigned "
                            "to the selected student."
                        ),
                        parent=assign_window
                    )

                    return


                # ---------------------------------------------
                # CALCULATE TOTAL FROM DATABASE
                # ---------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        COALESCE(
                            SUM(Amount),
                            0
                        )

                    FROM
                        fee_structure_components

                    WHERE
                        Fee_Structure_ID = %s
                    """,
                    (
                        fee_structure_id,
                    )
                )


                total_record = (
                    cursor.fetchone()
                )


                total_fee = float(
                    total_record[0] or 0
                )


                if total_fee <= 0:

                    messagebox.showwarning(
                        "Invalid Fee Structure",
                        (
                            "The selected fee structure "
                            "does not contain any valid "
                            "fee components."
                        ),
                        parent=assign_window
                    )

                    return


                # ---------------------------------------------
                # INSERT STUDENT FEE
                # ---------------------------------------------

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
                        registration_no,
                        fee_structure_id,
                        total_fee,
                        total_fee
                    )
                )


                con.commit()


                messagebox.showinfo(
                    "Success",
                    (
                        "Fee assigned successfully."
                        "\n\n"
                        f"Student: "
                        f"{registration_no}"
                        "\n"
                        f"Total Fee: "
                        f"₹{total_fee:,.2f}"
                    ),
                    parent=assign_window
                )


                assign_window.destroy()

                refresh_page()


            except mysql.connector.Error as error:

                if con is not None:

                    try:
                        con.rollback()
                    except Exception:
                        pass


                messagebox.showerror(
                    "Database Error",
                    (
                        "Could not assign the fee."
                        f"\n\n{error}"
                    ),
                    parent=assign_window
                )


            finally:

                if cursor is not None:

                    cursor.close()


                if (
                    con is not None
                    and con.is_connected()
                ):

                    con.close()


        # ====================================================
        # BOTTOM ACTIONS
        # ====================================================

        assign_actions = Frame(
            assign_window,
            bg=BG
        )

        assign_actions.pack(
            fill=X,
            padx=30,
            pady=(0, 20)
        )


        Button(
            assign_actions,
            text="CANCEL",
            bg=WHITE,
            fg=TEXT,
            activebackground="#F1F5F9",
            activeforeground=TEXT,
            relief=SOLID,
            bd=1,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=assign_window.destroy
        ).pack(
            side=RIGHT,
            ipadx=18,
            ipady=8
        )


        Button(
            assign_actions,
            text="ASSIGN FEE",
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
            command=assign_fee
        ).pack(
            side=RIGHT,
            padx=10,
            ipadx=20,
            ipady=9
        )


        load_active_students()


    # ========================================================
    # RECORD PAYMENT
    # ACCOUNTANT ONLY
    # ========================================================

    def open_payment_form():

        if not is_accountant:

            messagebox.showwarning(
                "Access Denied",
                (
                    "Only an Accountant can "
                    "record student payments."
                ),
                parent=parent
            )

            return


        student_fee_id = (
            get_selected_registration_no()
        )


        if student_fee_id is None:

            return


        # ====================================================
        # LOAD FEE RECORD
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
                    sf.Student_Fee_ID,
                    sf.Registration_No,
                    r.Name,
                    sf.Total_Fee,
                    sf.Amount_Paid,
                    sf.Due_Amount,
                    sf.Payment_Status

                FROM student_fees sf

                INNER JOIN registration r
                    ON
                        r.Registration_No
                        =
                        sf.Registration_No

                WHERE
                    sf.Student_Fee_ID = %s
                """,
                (
                    student_fee_id,
                )
            )


            fee_record = (
                cursor.fetchone()
            )


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load "
                    "the student fee."
                    f"\n\n{error}"
                ),
                parent=parent
            )

            return


        finally:

            if cursor is not None:

                cursor.close()


            if (
                con is not None
                and con.is_connected()
            ):

                con.close()


        if not fee_record:

            messagebox.showerror(
                "Not Found",
                (
                    "The selected student "
                    "fee was not found."
                ),
                parent=parent
            )

            return


        due_amount = float(
            fee_record[
                "Due_Amount"
            ]
        )


        if due_amount <= 0:

            messagebox.showinfo(
                "Already Paid",
                (
                    "This student's fee "
                    "has already been paid in full."
                ),
                parent=parent
            )

            return


        # ====================================================
        # PAYMENT WINDOW
        # ====================================================

        payment_window = Toplevel(
            parent
        )

        payment_window.title(
            "Record Payment"
        )

        center_window(
            payment_window,
            620,
            610,
            parent
        )

        payment_window.resizable(
            False,
            False
        )

        payment_window.configure(
            bg=BG
        )

        payment_window.transient(
            parent.winfo_toplevel()
        )

        payment_window.grab_set()


        # ====================================================
        # VARIABLES
        # ====================================================

        payment_amount_var = StringVar()

        payment_mode_var = StringVar(
            value="Cash"
        )

        transaction_reference_var = StringVar()

        payment_date_var = StringVar(
            value=date.today().strftime(
                "%Y-%m-%d"
            )
        )


        # ====================================================
        # HEADER
        # ====================================================

        Label(
            payment_window,
            text="Record Payment",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                20,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(22, 4)
        )


        Label(
            payment_window,
            text=(
                f"{fee_record['Registration_No']}  •  "
                f"{fee_record['Name']}"
            ),
            bg=BG,
            fg=GRAY,
            font=(
                "Helvetica",
                10
            )
        ).pack(
            anchor="w",
            padx=30
        )


        # ====================================================
        # CARD
        # ====================================================

        payment_card = Frame(
            payment_window,
            bg=WHITE,
            highlightbackground=LIGHT_BORDER,
            highlightthickness=1
        )

        payment_card.pack(
            fill=BOTH,
            expand=True,
            padx=30,
            pady=(18, 15)
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        payment_summary = Frame(
            payment_card,
            bg=LIGHT_BLUE
        )

        payment_summary.pack(
            fill=X,
            padx=22,
            pady=(20, 15)
        )


        payment_summary.grid_columnconfigure(
            0,
            weight=1
        )

        payment_summary.grid_columnconfigure(
            1,
            weight=1
        )

        payment_summary.grid_columnconfigure(
            2,
            weight=1
        )


        summary_data = [

            (
                "TOTAL FEE",
                float(
                    fee_record[
                        "Total_Fee"
                    ]
                )
            ),

            (
                "PAID",
                float(
                    fee_record[
                        "Amount_Paid"
                    ]
                )
            ),

            (
                "DUE",
                due_amount
            )
        ]


        for index, (
            title,
            value
        ) in enumerate(
            summary_data
        ):

            summary_item = Frame(
                payment_summary,
                bg=LIGHT_BLUE
            )

            summary_item.grid(
                row=0,
                column=index,
                sticky="ew",
                padx=12,
                pady=14
            )


            Label(
                summary_item,
                text=title,
                bg=LIGHT_BLUE,
                fg=GRAY,
                font=(
                    "Helvetica",
                    8,
                    "bold"
                )
            ).pack(
                anchor="w"
            )


            Label(
                summary_item,
                text=f"₹{value:,.2f}",
                bg=LIGHT_BLUE,
                fg=TEXT,
                font=(
                    "Helvetica",
                    12,
                    "bold"
                )
            ).pack(
                anchor="w",
                pady=(5, 0)
            )


        # ====================================================
        # PAYMENT AMOUNT
        # ====================================================

        Label(
            payment_card,
            text="Payment Amount (₹)",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(5, 6)
        )


        payment_amount_entry = Entry(
            payment_card,
            textvariable=payment_amount_var,
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

        payment_amount_entry.pack(
            fill=X,
            padx=22,
            ipady=7
        )


        # ====================================================
        # PAYMENT MODE
        # ====================================================

        Label(
            payment_card,
            text="Payment Mode",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(13, 6)
        )


        payment_mode_combo = ttk.Combobox(
            payment_card,
            textvariable=payment_mode_var,
            values=[
                "Cash",
                "UPI",
                "Card",
                "Bank Transfer"
            ],
            state="readonly",
            font=(
                "Helvetica",
                10
            )
        )

        payment_mode_combo.pack(
            fill=X,
            padx=22,
            ipady=5
        )


        # ====================================================
        # TRANSACTION REFERENCE
        # ====================================================

        Label(
            payment_card,
            text="Transaction Reference",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(13, 6)
        )


        transaction_reference_entry = Entry(
            payment_card,
            textvariable=transaction_reference_var,
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

        transaction_reference_entry.pack(
            fill=X,
            padx=22,
            ipady=7
        )


        # ====================================================
        # PAYMENT DATE
        # ====================================================

        Label(
            payment_card,
            text="Payment Date (YYYY-MM-DD)",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(13, 6)
        )


        payment_date_entry = Entry(
            payment_card,
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
        )

        payment_date_entry.pack(
            fill=X,
            padx=22,
            ipady=7
        )


        # ====================================================
        # REMARKS
        # ====================================================

        Label(
            payment_card,
            text="Remarks",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(13, 6)
        )


        remarks_text = Text(
            payment_card,
            height=3,
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

        remarks_text.pack(
            fill=X,
            padx=22,
            pady=(0, 18)
        )


        # ====================================================
        # SAVE PAYMENT
        # ====================================================

        def save_payment():

            amount_text = (
                payment_amount_var
                .get()
                .strip()
            )


            # ---------------------------------------------
            # AMOUNT VALIDATION
            # ---------------------------------------------

            try:

                payment_amount = float(
                    amount_text
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Amount",
                    (
                        "Please enter a valid "
                        "payment amount."
                    ),
                    parent=payment_window
                )

                payment_amount_entry.focus_set()

                return


            if payment_amount <= 0:

                messagebox.showwarning(
                    "Invalid Amount",
                    (
                        "Payment amount must "
                        "be greater than 0."
                    ),
                    parent=payment_window
                )

                return


            if payment_amount > due_amount:

                messagebox.showwarning(
                    "Amount Exceeds Due",
                    (
                        "Payment amount cannot "
                        "be greater than the "
                        "remaining due amount."
                        "\n\n"
                        f"Remaining Due: "
                        f"₹{due_amount:,.2f}"
                    ),
                    parent=payment_window
                )

                return


            # ---------------------------------------------
            # DATE VALIDATION
            # ---------------------------------------------

            payment_date_text = (
                payment_date_var
                .get()
                .strip()
            )


            try:

                datetime.strptime(
                    payment_date_text,
                    "%Y-%m-%d"
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Date",
                    (
                        "Please enter the payment "
                        "date in YYYY-MM-DD format."
                    ),
                    parent=payment_window
                )

                payment_date_entry.focus_set()

                return


            # ---------------------------------------------
            # PAYMENT MODE
            # ---------------------------------------------

            payment_mode = (
                payment_mode_var
                .get()
                .strip()
            )


            if not payment_mode:

                messagebox.showwarning(
                    "Required Field",
                    (
                        "Please select a "
                        "Payment Mode."
                    ),
                    parent=payment_window
                )

                return


            # ---------------------------------------------
            # DATA
            # ---------------------------------------------

            transaction_reference = (
                transaction_reference_var
                .get()
                .strip()
            )


            remarks = (
                remarks_text
                .get(
                    "1.0",
                    END
                )
                .strip()
            )


            con = None
            cursor = None


            try:

                con = get_connection()

                cursor = con.cursor()


                # -----------------------------------------
                # GET CURRENT VALUES AGAIN
                # -----------------------------------------

                cursor.execute(
                    """
                    SELECT
                        Total_Fee,
                        Amount_Paid,
                        Due_Amount

                    FROM student_fees

                    WHERE
                        Student_Fee_ID = %s
                    """,
                    (
                        student_fee_id,
                    )
                )


                current_record = (
                    cursor.fetchone()
                )


                if not current_record:

                    messagebox.showerror(
                        "Not Found",
                        (
                            "The student fee "
                            "record no longer exists."
                        ),
                        parent=payment_window
                    )

                    return


                current_total = float(
                    current_record[0]
                )

                current_paid = float(
                    current_record[1]
                )

                current_due = float(
                    current_record[2]
                )


                if payment_amount > current_due:

                    messagebox.showwarning(
                        "Amount Exceeds Due",
                        (
                            "The current due amount "
                            "has changed."
                            "\n\n"
                            f"Current Due: "
                            f"₹{current_due:,.2f}"
                        ),
                        parent=payment_window
                    )

                    return


                # -----------------------------------------
                # INSERT PAYMENT
                # -----------------------------------------

                cursor.execute(
                    """
                    INSERT INTO fee_payments
                    (
                        Student_Fee_ID,
                        Amount,
                        Payment_Mode,
                        Transaction_Reference,
                        Remarks,
                        Payment_Date
                    )

                    VALUES
                    (
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
                            if transaction_reference
                            else None
                        ),
                        (
                            remarks
                            if remarks
                            else None
                        ),
                        payment_date_text
                    )
                )


                # -----------------------------------------
                # CALCULATE NEW VALUES
                # -----------------------------------------

                new_paid = (
                    current_paid
                    +
                    payment_amount
                )


                new_due = (
                    current_total
                    -
                    new_paid
                )


                # Prevent tiny floating point value
                if abs(new_due) < 0.005:

                    new_due = 0.0


                if new_paid <= 0:

                    new_status = (
                        "Unpaid"
                    )

                elif new_due > 0:

                    new_status = (
                        "Partial"
                    )

                else:

                    new_status = (
                        "Paid"
                    )


                # -----------------------------------------
                # UPDATE STUDENT FEE
                # -----------------------------------------

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


                con.commit()


                messagebox.showinfo(
                    "Payment Recorded",
                    (
                        "Payment recorded successfully."
                        "\n\n"
                        f"Amount Paid: "
                        f"₹{payment_amount:,.2f}"
                        "\n"
                        f"Remaining Due: "
                        f"₹{new_due:,.2f}"
                        "\n"
                        f"Status: "
                        f"{new_status}"
                    ),
                    parent=payment_window
                )


                payment_window.destroy()

                refresh_page()


            except mysql.connector.Error as error:

                if con is not None:

                    try:
                        con.rollback()
                    except Exception:
                        pass


                messagebox.showerror(
                    "Database Error",
                    (
                        "Could not record "
                        "the payment."
                        f"\n\n{error}"
                    ),
                    parent=payment_window
                )


            finally:

                if cursor is not None:

                    cursor.close()


                if (
                    con is not None
                    and con.is_connected()
                ):

                    con.close()


        # ====================================================
        # PAYMENT ACTIONS
        # ====================================================

        payment_actions = Frame(
            payment_window,
            bg=BG
        )

        payment_actions.pack(
            fill=X,
            padx=30,
            pady=(0, 20)
        )


        Button(
            payment_actions,
            text="CANCEL",
            bg=WHITE,
            fg=TEXT,
            activebackground="#F1F5F9",
            activeforeground=TEXT,
            relief=SOLID,
            bd=1,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=payment_window.destroy
        ).pack(
            side=RIGHT,
            ipadx=18,
            ipady=8
        )


        Button(
            payment_actions,
            text="RECORD PAYMENT",
            bg=GREEN,
            fg=WHITE,
            activebackground=DARK_GREEN,
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
            padx=10,
            ipadx=18,
            ipady=9
        )


        payment_amount_entry.focus_set()


    # ========================================================
    # SEARCH BUTTON
    # ========================================================

    Button(
        filter_inner,
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
            8,
            "bold"
        ),
        command=load_student_fees
    ).pack(
        side=LEFT,
        padx=(10, 0),
        ipadx=14,
        ipady=8
    )


    # ========================================================
    # CLEAR BUTTON
    # ========================================================

    Button(
        filter_inner,
        text="CLEAR",
        bg=WHITE,
        fg=TEXT,
        activebackground="#F1F5F9",
        activeforeground=TEXT,
        relief=SOLID,
        bd=1,
        cursor="hand2",
        font=(
            "Helvetica",
            8,
            "bold"
        ),
        command=clear_filters
    ).pack(
        side=LEFT,
        padx=(8, 0),
        ipadx=13,
        ipady=7
    )


    # ========================================================
    # VIEW BUTTON
    # ADMIN + ACCOUNTANT
    # ========================================================

    Button(
        action_bar,
        text="VIEW DETAILS",
        bg=WHITE,
        fg=BLUE,
        activebackground=LIGHT_BLUE,
        activeforeground=DARK_BLUE,
        relief=SOLID,
        bd=1,
        cursor="hand2",
        font=(
            "Helvetica",
            8,
            "bold"
        ),
        command=view_student_fee
    ).pack(
        side=RIGHT,
        ipadx=14,
        ipady=7
    )


    # ========================================================
    # ACCOUNTANT ONLY BUTTONS
    # ========================================================

    if is_accountant:

        # ----------------------------------------------------
        # RECORD PAYMENT
        # ----------------------------------------------------

        Button(
            action_bar,
            text="RECORD PAYMENT",
            bg=GREEN,
            fg=WHITE,
            activebackground=DARK_GREEN,
            activeforeground=WHITE,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                8,
                "bold"
            ),
            command=open_payment_form
        ).pack(
            side=RIGHT,
            padx=(0, 8),
            ipadx=14,
            ipady=8
        )


        # ----------------------------------------------------
        # ASSIGN FEE
        # ----------------------------------------------------

        Button(
            header,
            text="+ ASSIGN FEE",
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
            command=open_assign_fee_form
        ).pack(
            side=RIGHT,
            ipadx=17,
            ipady=9
        )


    # ========================================================
    # EVENTS
    # ========================================================

    search_entry.bind(
        "<Return>",
        load_student_fees
    )


    course_filter.bind(
        "<<ComboboxSelected>>",
        load_student_fees
    )


    semester_filter.bind(
        "<<ComboboxSelected>>",
        load_student_fees
    )


    status_filter.bind(
        "<<ComboboxSelected>>",
        load_student_fees
    )


    def on_student_name_single_click(event):

        region = fee_tree.identify_region(
            event.x,
            event.y
        )

        row_id = fee_tree.identify_row(
            event.y
        )

        column_id = fee_tree.identify_column(
            event.x
        )

        if region != "cell" or not row_id:
            return

        fee_tree.selection_set(row_id)
        fee_tree.focus(row_id)

        # Column #3 is STUDENT NAME.
        # Open details with ONE click only on the student name.
        if column_id == "#3":
            fee_tree.after(
                80,
                view_student_fee
            )


    fee_tree.bind(
        "<ButtonRelease-1>",
        on_student_name_single_click
    )


    # ========================================================
    # INITIALIZE PAGE
    # ========================================================


    # ========================================================
    # OPEN STUDENT DETAILS ON SINGLE ROW CLICK
    # ========================================================

    fee_tree.bind(
        "<ButtonRelease-1>",
        open_student_on_row_click,
        add="+"
    )


    load_course_filter()

    refresh_page()