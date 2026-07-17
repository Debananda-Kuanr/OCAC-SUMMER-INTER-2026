from tkinter import *
from tkinter import messagebox
import mysql.connector
import subprocess
import sys
import os


# ============================================================
# IMPORT MODULES
# ============================================================

from accountant_management import show_accountant_page
from student_management import show_student_page
from student_approvals import show_student_approval_page
from course_management import show_course_page
from fee_structure_management import show_fee_structure_page
from student_fee_management import open_student_fee_management
from reports_management import open_reports_management


# ============================================================
# PROJECT PATHS
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(
    CURRENT_DIR
)

COMMON_GUI_DIR = os.path.join(
    PROJECT_DIR,
    "COMMON GUI"
)

LOGIN_FILE = os.path.join(
    COMMON_GUI_DIR,
    "login.py"
)


CHANGE_PASSWORD_FILE = os.path.join(
    COMMON_GUI_DIR,
    "change_password.py"
)


# ============================================================
# MAIN WINDOW
# ============================================================

window = Tk()

window.title(
    "Admin Dashboard - Fee Status Management System"
)

window.state(
    "zoomed"
)

window.minsize(
    1100,
    650
)

window.configure(
    bg="#F8FAFC"
)


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
DARK_BLUE = "#1E40AF"
LIGHT_BLUE = "#EFF6FF"

SIDEBAR_BG = "#0F172A"
SIDEBAR_HOVER = "#1E293B"
SIDEBAR_TEXT = "#CBD5E1"

WHITE = "#FFFFFF"
BACKGROUND = "#F8FAFC"

TEXT_COLOR = "#1E293B"
GRAY = "#64748B"
LIGHT_GRAY = "#94A3B8"
BORDER_COLOR = "#E2E8F0"

GREEN = "#16A34A"
LIGHT_GREEN = "#F0FDF4"

ORANGE = "#F97316"
LIGHT_ORANGE = "#FFF7ED"

PURPLE = "#7C3AED"
LIGHT_PURPLE = "#F5F3FF"

RED = "#DC2626"


# ============================================================
# DATABASE CONNECTION
# ============================================================

con = None
cursor = None


def connect_database():

    global con
    global cursor

    try:

        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="9439",
            database="OCAC_GROUP2"
        )

        cursor = con.cursor()

        return True

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            (
                "Unable to connect to database."
                f"\n\n{error}"
            )
        )

        return False


if not connect_database():

    window.destroy()

    sys.exit()


# ============================================================
# ENSURE DATABASE CONNECTION
# ============================================================

def ensure_connection():

    global con
    global cursor

    try:

        if (
            con is None
            or
            not con.is_connected()
        ):

            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="9439",
                database="OCAC_GROUP2"
            )

            cursor = con.cursor()

        return True

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            (
                "Could not reconnect "
                "to the database."
                f"\n\n{error}"
            )
        )

        return False


# ============================================================
# GET TOTAL STUDENTS
# ============================================================

def get_total_students():

    try:

        if not ensure_connection():
            return 0

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM registration

            WHERE
                LOWER(TRIM(Role)) = 'student'
            """
        )

        result = cursor.fetchone()

        return (
            result[0]
            if result
            else 0
        )

    except mysql.connector.Error:

        return 0


# ============================================================
# GET TOTAL ACCOUNTANTS
# ============================================================

def get_total_accountants():

    try:

        if not ensure_connection():
            return 0

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM registration

            WHERE
                LOWER(TRIM(Role)) = 'accountant'
            """
        )

        result = cursor.fetchone()

        return (
            result[0]
            if result
            else 0
        )

    except mysql.connector.Error:

        return 0


# ============================================================
# GET TOTAL COLLECTION
# ============================================================

def get_total_collection():

    try:

        if not ensure_connection():
            return 0.00

        cursor.execute(
            """
            SELECT
                COALESCE(
                    SUM(Amount_Paid),
                    0
                )

            FROM student_fees
            """
        )

        result = cursor.fetchone()

        return float(
            result[0] or 0
        )

    except mysql.connector.Error:

        return 0.00


# ============================================================
# GET PENDING FEES
# ============================================================

def get_pending_fees():

    try:

        if not ensure_connection():
            return 0.00

        cursor.execute(
            """
            SELECT
                COALESCE(
                    SUM(Due_Amount),
                    0
                )

            FROM student_fees
            """
        )

        result = cursor.fetchone()

        return float(
            result[0] or 0
        )

    except mysql.connector.Error:

        return 0.00


# ============================================================
# GET RECENT PAYMENTS
# ============================================================

def get_recent_payments():

    try:

        if not ensure_connection():
            return []

        cursor.execute(
            """
            SELECT
                fp.Payment_ID,
                r.Name,
                sf.Registration_No,
                fp.Amount,
                fp.Payment_Date,
                sf.Payment_Status

            FROM fee_payments fp

            INNER JOIN student_fees sf
                ON
                    sf.Student_Fee_ID
                    =
                    fp.Student_Fee_ID

            INNER JOIN registration r
                ON
                    r.Registration_No
                    =
                    sf.Registration_No

            ORDER BY
                fp.Payment_ID DESC

            LIMIT 5
            """
        )

        return cursor.fetchall()

    except mysql.connector.Error:

        return []


# ============================================================
# CLOSE DATABASE
# ============================================================

def close_database():

    global con
    global cursor

    try:

        if cursor is not None:

            cursor.close()

    except:

        pass

    try:

        if (
            con is not None
            and
            con.is_connected()
        ):

            con.close()

    except:

        pass


# ============================================================
# LOGOUT
# ============================================================

def logout():

    answer = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if not answer:

        return

    if not os.path.exists(
        LOGIN_FILE
    ):

        messagebox.showerror(
            "File Not Found",
            (
                "Login file not found:"
                f"\n\n{LOGIN_FILE}"
            )
        )

        return

    close_database()

    window.destroy()

    subprocess.Popen(
        [
            sys.executable,
            LOGIN_FILE
        ],
        cwd=PROJECT_DIR
    )


# ============================================================
# CLOSE SOFTWARE
# ============================================================

def close_software():

    answer = messagebox.askyesno(
        "Exit Software",
        (
            "Are you sure you want "
            "to close the software?"
        )
    )

    if answer:

        close_database()

        window.destroy()


# ============================================================
# CLEAR CONTENT AREA
# ============================================================

def clear_content():

    for widget in (
        content_frame.winfo_children()
    ):

        widget.destroy()


# ============================================================
# SIDEBAR BUTTON LIST
# ============================================================

sidebar_buttons = []


# ============================================================
# SET ACTIVE SIDEBAR BUTTON
# ============================================================

def set_active_button(
    active_button
):

    for button in sidebar_buttons:

        button.config(
            bg=SIDEBAR_BG,
            fg=SIDEBAR_TEXT,
            font=(
                "Helvetica",
                10
            )
        )

    active_button.config(
        bg=BLUE,
        fg=WHITE,
        font=(
            "Helvetica",
            10,
            "bold"
        )
    )


# ============================================================
# CREATE STAT CARD
# ============================================================

def create_stat_card(
    parent,
    x_position,
    icon_text,
    icon_bg,
    icon_fg,
    title,
    value,
    command
):

    card = Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1,
        cursor="hand2"
    )

    card.place(
        relx=x_position,
        y=120,
        relwidth=0.225,
        height=155
    )


    # --------------------------------------------------------
    # ICON BOX
    # --------------------------------------------------------

    icon_box = Label(
        card,
        text=icon_text,
        bg=icon_bg,
        fg=icon_fg,
        font=(
            "Helvetica",
            13,
            "bold"
        )
    )

    icon_box.place(
        x=20,
        y=18,
        width=42,
        height=42
    )


    # --------------------------------------------------------
    # CARD TITLE
    # --------------------------------------------------------

    title_label = Label(
        card,
        text=title,
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            8,
            "bold"
        ),
        anchor="w"
    )

    title_label.place(
        x=20,
        y=78
    )


    # --------------------------------------------------------
    # CARD VALUE
    # --------------------------------------------------------

    value_label = Label(
        card,
        text=value,
        bg=WHITE,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            18,
            "bold"
        ),
        anchor="w"
    )

    value_label.place(
        x=20,
        y=102
    )


    # --------------------------------------------------------
    # VIEW DETAILS BUTTON
    # --------------------------------------------------------

    details_button = Button(
        card,
        text="View Details  →",
        bg=WHITE,
        fg=BLUE,
        activebackground=WHITE,
        activeforeground=DARK_BLUE,
        font=(
            "Helvetica",
            8,
            "bold"
        ),
        bd=0,
        cursor="hand2",
        command=command
    )

    details_button.place(
        relx=0.62,
        y=105
    )


    # --------------------------------------------------------
    # MAKE CARD CLICKABLE
    # --------------------------------------------------------

    card.bind(
        "<Button-1>",
        lambda event: command()
    )

    icon_box.bind(
        "<Button-1>",
        lambda event: command()
    )

    title_label.bind(
        "<Button-1>",
        lambda event: command()
    )

    value_label.bind(
        "<Button-1>",
        lambda event: command()
    )


# ============================================================
# SHOW DASHBOARD
# ============================================================

def show_dashboard():

    set_active_button(
        dashboard_button
    )

    top_title.config(
        text="Dashboard"
    )

    clear_content()


    # --------------------------------------------------------
    # GET DASHBOARD DATA
    # --------------------------------------------------------

    total_students = (
        get_total_students()
    )

    total_accountants = (
        get_total_accountants()
    )

    total_collection = (
        get_total_collection()
    )

    pending_fees = (
        get_pending_fees()
    )

    recent_payments = (
        get_recent_payments()
    )


    # ========================================================
    # WELCOME TITLE
    # ========================================================

    welcome_title = Label(
        content_frame,
        text=(
            "Welcome back, Administrator"
        ),
        bg=BACKGROUND,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            22,
            "bold"
        )
    )

    welcome_title.place(
        x=35,
        y=30
    )


    # ========================================================
    # WELCOME SUBTITLE
    # ========================================================

    welcome_subtitle = Label(
        content_frame,
        text=(
            "Monitor students, accountants, "
            "fees and payments."
        ),
        bg=BACKGROUND,
        fg=GRAY,
        font=(
            "Helvetica",
            10
        )
    )

    welcome_subtitle.place(
        x=36,
        y=70
    )


    # ========================================================
    # STUDENTS CARD
    # ========================================================

    create_stat_card(
        parent=content_frame,
        x_position=0.03,
        icon_text="ST",
        icon_bg=LIGHT_BLUE,
        icon_fg=BLUE,
        title="TOTAL STUDENTS",
        value=str(
            total_students
        ),
        command=show_students
    )


    # ========================================================
    # ACCOUNTANTS CARD
    # ========================================================

    create_stat_card(
        parent=content_frame,
        x_position=0.265,
        icon_text="AC",
        icon_bg=LIGHT_PURPLE,
        icon_fg=PURPLE,
        title="ACCOUNTANTS",
        value=str(
            total_accountants
        ),
        command=show_accountants
    )


    # ========================================================
    # TOTAL COLLECTION CARD
    # ========================================================

    create_stat_card(
        parent=content_frame,
        x_position=0.50,
        icon_text="₹",
        icon_bg=LIGHT_GREEN,
        icon_fg=GREEN,
        title="TOTAL COLLECTION",
        value=(
            f"₹{total_collection:,.2f}"
        ),
        command=show_student_fees
    )


    # ========================================================
    # PENDING FEES CARD
    # ========================================================

    create_stat_card(
        parent=content_frame,
        x_position=0.735,
        icon_text="!",
        icon_bg=LIGHT_ORANGE,
        icon_fg=ORANGE,
        title="PENDING FEES",
        value=(
            f"₹{pending_fees:,.2f}"
        ),
        command=show_student_fees
    )


    # ========================================================
    # RECENT PAYMENTS TITLE
    # ========================================================

    recent_title = Label(
        content_frame,
        text="Recent Payments",
        bg=BACKGROUND,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            16,
            "bold"
        )
    )

    recent_title.place(
        x=35,
        y=320
    )


    recent_subtitle = Label(
        content_frame,
        text=(
            "Latest student fee transactions"
        ),
        bg=BACKGROUND,
        fg=GRAY,
        font=(
            "Helvetica",
            9
        )
    )

    recent_subtitle.place(
        x=36,
        y=355
    )


    # ========================================================
    # RECENT PAYMENTS CARD
    # ========================================================

    payment_card = Frame(
        content_frame,
        bg=WHITE,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    payment_card.place(
        x=35,
        y=395,
        relwidth=0.94,
        relheight=0.38
    )


    # ========================================================
    # TABLE HEADER
    # ========================================================

    table_header = Frame(
        payment_card,
        bg=BACKGROUND,
        height=50
    )

    table_header.pack(
        fill=X
    )

    table_header.pack_propagate(
        False
    )


    headers = [
        (
            "RECEIPT ID",
            0.03
        ),
        (
            "STUDENT",
            0.20
        ),
        (
            "REGISTRATION NO.",
            0.40
        ),
        (
            "AMOUNT",
            0.60
        ),
        (
            "DATE",
            0.75
        ),
        (
            "STATUS",
            0.88
        )
    ]


    for (
        text,
        x_position
    ) in headers:

        header_label = Label(
            table_header,
            text=text,
            bg=BACKGROUND,
            fg=GRAY,
            font=(
                "Helvetica",
                8,
                "bold"
            )
        )

        header_label.place(
            relx=x_position,
            rely=0.5,
            anchor="w"
        )


    # ========================================================
    # EMPTY PAYMENT STATE
    # ========================================================

    if not recent_payments:

        empty_icon = Label(
            payment_card,
            text="₹",
            bg=LIGHT_BLUE,
            fg=BLUE,
            font=(
                "Helvetica",
                17,
                "bold"
            )
        )

        empty_icon.place(
            relx=0.50,
            rely=0.48,
            anchor="center",
            width=48,
            height=48
        )


        empty_title = Label(
            payment_card,
            text=(
                "No payment records available"
            ),
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                10,
                "bold"
            )
        )

        empty_title.place(
            relx=0.50,
            rely=0.68,
            anchor="center"
        )


        empty_subtitle = Label(
            payment_card,
            text=(
                "Recent transactions will "
                "appear here after payments "
                "are recorded."
            ),
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                9
            )
        )

        empty_subtitle.place(
            relx=0.50,
            rely=0.80,
            anchor="center"
        )


    # ========================================================
    # DISPLAY RECENT PAYMENTS
    # ========================================================

    else:

        rows_container = Frame(
            payment_card,
            bg=WHITE
        )

        rows_container.pack(
            fill=BOTH,
            expand=True
        )


        for index, record in enumerate(
            recent_payments
        ):

            (
                payment_id,
                student_name,
                registration_no,
                amount,
                payment_date,
                payment_status
            ) = record


            row = Frame(
                rows_container,
                bg=WHITE,
                height=48
            )

            row.pack(
                fill=X
            )

            row.pack_propagate(
                False
            )


            values = [
                (
                    f"PAY{int(payment_id):05d}",
                    0.03,
                    TEXT_COLOR
                ),
                (
                    str(student_name),
                    0.20,
                    TEXT_COLOR
                ),
                (
                    str(registration_no),
                    0.40,
                    BLUE
                ),
                (
                    f"₹{float(amount):,.2f}",
                    0.60,
                    GREEN
                ),
                (
                    str(payment_date),
                    0.75,
                    TEXT_COLOR
                ),
                (
                    str(payment_status),
                    0.88,
                    GREEN
                )
            ]


            for (
                value,
                x_position,
                color
            ) in values:

                Label(
                    row,
                    text=value,
                    bg=WHITE,
                    fg=color,
                    font=(
                        "Helvetica",
                        9,
                        (
                            "bold"
                            if x_position in [
                                0.03,
                                0.60
                            ]
                            else "normal"
                        )
                    )
                ).place(
                    relx=x_position,
                    rely=0.5,
                    anchor="w"
                )


            if (
                index
                <
                len(recent_payments) - 1
            ):

                Frame(
                    rows_container,
                    bg=BORDER_COLOR,
                    height=1
                ).pack(
                    fill=X
                )


# ============================================================
# SHOW ACCOUNTANTS
# ============================================================

def show_accountants():

    set_active_button(
        accountants_button
    )

    top_title.config(
        text="Accountants"
    )

    clear_content()

    show_accountant_page(
        content_frame
    )


# ============================================================
# SHOW STUDENTS
# ============================================================

def show_students():

    set_active_button(
        students_button
    )

    top_title.config(
        text="Students"
    )

    clear_content()

    show_student_page(
        content_frame
    )


# ============================================================
# SHOW REQUESTS
# ============================================================

def show_requests():

    set_active_button(
        requests_button
    )

    top_title.config(
        text="Requests"
    )

    clear_content()

    show_student_approval_page(
        content_frame
    )


# ============================================================
# SHOW COURSES
# ============================================================

def show_courses():

    set_active_button(
        courses_button
    )

    top_title.config(
        text="Courses"
    )

    clear_content()

    show_course_page(
        content_frame
    )


# ============================================================
# SHOW FEE STRUCTURE
# ============================================================

def show_fee_structure():

    set_active_button(
        fee_structure_button
    )

    top_title.config(
        text="Fee Structure"
    )

    clear_content()

    show_fee_structure_page(
        content_frame
    )


# ============================================================
# SHOW STUDENT FEES
# ADMIN VIEW ONLY
# ============================================================

def show_student_fees():

    set_active_button(
        student_fees_button
    )

    top_title.config(
        text="Student Fees"
    )

    clear_content()

    # --------------------------------------------------------
    # ADMIN ROLE
    #
    # Admin can:
    # - View fee records
    # - Search
    # - Filter
    # - View details
    # - View fee components
    # - View payment history
    #
    # Admin cannot:
    # - Assign fee
    # - Record payment
    # --------------------------------------------------------

    open_student_fee_management(
        content_frame,
        user_role="Admin"
    )


# ============================================================
# SHOW REPORTS
# ADMIN VIEW ONLY
# ============================================================

def show_reports():

    set_active_button(
        reports_button
    )

    top_title.config(
        text="Reports"
    )

    clear_content()

    # Open the complete reports page inside the admin content area.
    open_reports_management(
        content_frame,
        current_role="Admin"
    )


# ============================================================
# CHANGE PASSWORD
# ============================================================

def change_password():

    if not os.path.exists(
        CHANGE_PASSWORD_FILE
    ):

        messagebox.showerror(
            "File Not Found",
            (
                "Change Password file not found:"
                f"\n\n{CHANGE_PASSWORD_FILE}"
            ),
            parent=window
        )

        return

    try:

        subprocess.Popen(
            [
                sys.executable,
                CHANGE_PASSWORD_FILE
            ],
            cwd=PROJECT_DIR
        )

    except Exception as error:

        messagebox.showerror(
            "Open Error",
            (
                "Unable to open Change Password."
                f"\n\n{error}"
            ),
            parent=window
        )


# ============================================================
# MAIN LAYOUT
# ============================================================


# ============================================================
# SIDEBAR
# ============================================================

sidebar = Frame(
    window,
    bg=SIDEBAR_BG,
    width=245
)

sidebar.pack(
    side=LEFT,
    fill=Y
)

sidebar.pack_propagate(
    False
)


# ============================================================
# SIDEBAR HEADER
# ============================================================

sidebar_header = Frame(
    sidebar,
    bg=SIDEBAR_BG,
    height=110
)

sidebar_header.pack(
    fill=X
)

sidebar_header.pack_propagate(
    False
)


# ============================================================
# LOGO BOX
# ============================================================

logo_box = Label(
    sidebar_header,
    text="₹",
    bg=BLUE,
    fg=WHITE,
    font=(
        "Helvetica",
        19,
        "bold"
    )
)

logo_box.place(
    x=22,
    y=28,
    width=45,
    height=45
)


# ============================================================
# PROJECT NAME
# ============================================================

project_name = Label(
    sidebar_header,
    text="FEE STATUS",
    bg=SIDEBAR_BG,
    fg=WHITE,
    font=(
        "Helvetica",
        11,
        "bold"
    ),
    anchor="w"
)

project_name.place(
    x=80,
    y=29
)


project_name_2 = Label(
    sidebar_header,
    text="MANAGEMENT SYSTEM",
    bg=SIDEBAR_BG,
    fg=LIGHT_GRAY,
    font=(
        "Helvetica",
        8
    ),
    anchor="w"
)

project_name_2.place(
    x=80,
    y=53
)


# ============================================================
# SIDEBAR SEPARATOR
# ============================================================

separator = Frame(
    sidebar,
    bg="#334155",
    height=1
)

separator.pack(
    fill=X,
    padx=20
)


# ============================================================
# ADMIN PANEL LABEL
# ============================================================

admin_panel_label = Label(
    sidebar,
    text="ADMIN PANEL",
    bg=SIDEBAR_BG,
    fg="#64748B",
    font=(
        "Helvetica",
        8,
        "bold"
    ),
    anchor="w"
)

admin_panel_label.pack(
    fill=X,
    padx=28,
    pady=(
        25,
        12
    )
)


# ============================================================
# DASHBOARD BUTTON
# ============================================================

dashboard_button = Button(
    sidebar,
    text="   Dashboard",
    bg=SIDEBAR_BG,
    fg=SIDEBAR_TEXT,
    activebackground=SIDEBAR_HOVER,
    activeforeground=WHITE,
    font=(
        "Helvetica",
        10
    ),
    bd=0,
    anchor="w",
    cursor="hand2",
    command=show_dashboard
)

dashboard_button.pack(
    fill=X,
    padx=15,
    pady=4,
    ipady=11
)


# ============================================================
# ACCOUNTANTS BUTTON
# ============================================================

accountants_button = Button(
    sidebar,
    text="   Accountants",
    bg=SIDEBAR_BG,
    fg=SIDEBAR_TEXT,
    activebackground=SIDEBAR_HOVER,
    activeforeground=WHITE,
    font=(
        "Helvetica",
        10
    ),
    bd=0,
    anchor="w",
    cursor="hand2",
    command=show_accountants
)

accountants_button.pack(
    fill=X,
    padx=15,
    pady=4,
    ipady=11
)


# ============================================================
# STUDENTS BUTTON
# ============================================================

students_button = Button(
    sidebar,
    text="   Students",
    bg=SIDEBAR_BG,
    fg=SIDEBAR_TEXT,
    activebackground=SIDEBAR_HOVER,
    activeforeground=WHITE,
    font=(
        "Helvetica",
        10
    ),
    bd=0,
    anchor="w",
    cursor="hand2",
    command=show_students
)

students_button.pack(
    fill=X,
    padx=15,
    pady=4,
    ipady=11
)


# ============================================================
# COURSES BUTTON
# ============================================================

courses_button = Button(
    sidebar,
    text="   Courses",
    bg=SIDEBAR_BG,
    fg=SIDEBAR_TEXT,
    activebackground=SIDEBAR_HOVER,
    activeforeground=WHITE,
    font=(
        "Helvetica",
        10
    ),
    bd=0,
    anchor="w",
    cursor="hand2",
    command=show_courses
)

courses_button.pack(
    fill=X,
    padx=15,
    pady=4,
    ipady=11
)


# ============================================================
# REQUESTS BUTTON
# ============================================================

requests_button = Button(
    sidebar,
    text="   Requests",
    bg=SIDEBAR_BG,
    fg=SIDEBAR_TEXT,
    activebackground=SIDEBAR_HOVER,
    activeforeground=WHITE,
    font=(
        "Helvetica",
        10
    ),
    bd=0,
    anchor="w",
    cursor="hand2",
    command=show_requests
)

requests_button.pack(
    fill=X,
    padx=15,
    pady=4,
    ipady=11
)


# ============================================================
# FEE STRUCTURE BUTTON
# ============================================================

fee_structure_button = Button(
    sidebar,
    text="   Fee Structure",
    bg=SIDEBAR_BG,
    fg=SIDEBAR_TEXT,
    activebackground=SIDEBAR_HOVER,
    activeforeground=WHITE,
    font=(
        "Helvetica",
        10
    ),
    bd=0,
    anchor="w",
    cursor="hand2",
    command=show_fee_structure
)

fee_structure_button.pack(
    fill=X,
    padx=15,
    pady=4,
    ipady=11
)


# ============================================================
# STUDENT FEES BUTTON
# ============================================================

student_fees_button = Button(
    sidebar,
    text="   Student Fees",
    bg=SIDEBAR_BG,
    fg=SIDEBAR_TEXT,
    activebackground=SIDEBAR_HOVER,
    activeforeground=WHITE,
    font=(
        "Helvetica",
        10
    ),
    bd=0,
    anchor="w",
    cursor="hand2",
    command=show_student_fees
)

student_fees_button.pack(
    fill=X,
    padx=15,
    pady=4,
    ipady=11
)


# ============================================================
# REPORTS BUTTON
# ============================================================

reports_button = Button(
    sidebar,
    text="   Reports",
    bg=SIDEBAR_BG,
    fg=SIDEBAR_TEXT,
    activebackground=SIDEBAR_HOVER,
    activeforeground=WHITE,
    font=(
        "Helvetica",
        10
    ),
    bd=0,
    anchor="w",
    cursor="hand2",
    command=show_reports
)

reports_button.pack(
    fill=X,
    padx=15,
    pady=4,
    ipady=11
)


# ============================================================
# ADD SIDEBAR BUTTONS TO LIST
# ============================================================

sidebar_buttons.extend(
    [
        dashboard_button,
        accountants_button,
        students_button,
        requests_button,
        courses_button,
        fee_structure_button,
        student_fees_button,
        reports_button
    ]
)


# ============================================================
# SIDEBAR BOTTOM AREA
# ============================================================

bottom_area = Frame(
    sidebar,
    bg=SIDEBAR_BG
)

bottom_area.pack(
    side=BOTTOM,
    fill=X,
    padx=15,
    pady=15
)


# ============================================================
# CHANGE PASSWORD BUTTON
# ============================================================

change_password_button = Button(
    bottom_area,
    text="Change Password",
    bg="yellow",
    fg="black",
    activebackground="#FACC15",
    activeforeground="black",
    font=(
        "Helvetica",
        10,
        "bold"
    ),
    bd=0,
    cursor="hand2",
    command=change_password
)

change_password_button.pack(
    fill=X,
    ipady=10
)


# ============================================================
# LOGOUT BUTTON
# ============================================================

logout_button = Button(
    bottom_area,
    text="Logout",
    bg=RED,
    fg=WHITE,
    activebackground="#B91C1C",
    activeforeground=WHITE,
    font=(
        "Helvetica",
        10,
        "bold"
    ),
    bd=0,
    cursor="hand2",
    command=logout
)

logout_button.pack(
    fill=X,
    pady=(
        10,
        0
    ),
    ipady=8
)


# ============================================================
# RIGHT AREA
# ============================================================

right_area = Frame(
    window,
    bg=BACKGROUND
)

right_area.pack(
    side=LEFT,
    fill=BOTH,
    expand=True
)


# ============================================================
# TOP BAR
# ACCOUNTANT-PANEL STYLE
# ============================================================

TOP_NAV_BG = "#DBEAFE"
TOP_NAV_BORDER = "#BFDBFE"
TOP_NAV_TEXT = "#1E3A8A"
TOP_NAV_MUTED = "#475569"

top_bar = Frame(
    right_area,
    bg=TOP_NAV_BG,
    height=78,
    highlightbackground=TOP_NAV_BORDER,
    highlightthickness=1
)

top_bar.pack(
    fill=X
)

top_bar.pack_propagate(
    False
)


# ============================================================
# TOP BAR LEFT AREA
# ============================================================

top_left_area = Frame(
    top_bar,
    bg=TOP_NAV_BG
)

top_left_area.pack(
    side=LEFT,
    fill=Y,
    padx=35
)


top_title = Label(
    top_left_area,
    text="Dashboard",
    bg=TOP_NAV_BG,
    fg=TOP_NAV_TEXT,
    font=(
        "Helvetica",
        18,
        "bold"
    ),
    anchor="w"
)

top_title.pack(
    side=LEFT
)


# ============================================================
# TOP BAR RIGHT PROFILE AREA
# ============================================================

top_profile_frame = Frame(
    top_bar,
    bg=TOP_NAV_BG
)

top_profile_frame.pack(
    side=RIGHT,
    fill=Y,
    padx=35
)


top_profile_icon = Label(
    top_profile_frame,
    text="A",
    bg=BLUE,
    fg=WHITE,
    font=(
        "Helvetica",
        11,
        "bold"
    ),
    width=3,
    height=1
)

top_profile_icon.pack(
    side=LEFT,
    padx=(
        0,
        12
    ),
    ipadx=4,
    ipady=8
)


top_profile_text = Frame(
    top_profile_frame,
    bg=TOP_NAV_BG
)

top_profile_text.pack(
    side=LEFT
)


top_profile_name = Label(
    top_profile_text,
    text="Administrator",
    bg=TOP_NAV_BG,
    fg=TOP_NAV_TEXT,
    font=(
        "Helvetica",
        10,
        "bold"
    ),
    anchor="w"
)

top_profile_name.pack(
    anchor="w"
)


top_profile_role = Label(
    top_profile_text,
    text="ADMIN",
    bg=TOP_NAV_BG,
    fg=TOP_NAV_MUTED,
    font=(
        "Helvetica",
        8
    ),
    anchor="w"
)

top_profile_role.pack(
    anchor="w",
    pady=(
        2,
        0
    )
)


# ============================================================
# CHANGEABLE CONTENT FRAME
# ============================================================

content_frame = Frame(
    right_area,
    bg=BACKGROUND
)

content_frame.pack(
    fill=BOTH,
    expand=True
)


# ============================================================
# SHOW DASHBOARD WHEN SOFTWARE STARTS
# ============================================================

show_dashboard()


# ============================================================
# WINDOW CLOSE EVENT
# ============================================================

window.protocol(
    "WM_DELETE_WINDOW",
    close_software
)


# ============================================================
# MAIN LOOP
# ============================================================

window.mainloop()
