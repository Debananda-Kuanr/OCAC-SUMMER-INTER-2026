from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import subprocess
import sys
import os


# ============================================================
# FILE:
# ACCOUNTANT/accountant_dashboard.py
# ============================================================


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
# ACCOUNTANT MODULE PATHS
# ============================================================

STUDENT_FEES_FILE = os.path.join(
    CURRENT_DIR,
    "student_fees_page.py"
)

ASSIGN_FEES_FILE = os.path.join(
    CURRENT_DIR,
    "assign_fees_page.py"
)


PAYMENTS_FILE = os.path.join(
    CURRENT_DIR,
    "payments_page.py"
)


REPORTS_FILE = os.path.join(
    CURRENT_DIR,
    "reports_page.py"
)

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

try:
    from student_fees_page import show_student_fees_page
except Exception as error:
    show_student_fees_page = None
    print(
        "Student Fees Import Error:",
        error
    )

try:
    from assign_fees_page import open_assign_fees_page
except Exception as error:
    open_assign_fees_page = None
    ASSIGN_FEES_IMPORT_ERROR = str(error)

    print(
        "Assign Fees Import Error:",
        error
    )
else:
    ASSIGN_FEES_IMPORT_ERROR = ""


try:
    from payments_page import open_payments_page
except Exception as error:
    open_payments_page = None
    PAYMENTS_IMPORT_ERROR = str(error)

    print(
        "Payments Import Error:",
        error
    )
else:
    PAYMENTS_IMPORT_ERROR = ""


try:
    from reports_page import open_reports_page
except Exception as error:
    open_reports_page = None
    REPORTS_IMPORT_ERROR = str(error)
    print("Reports Import Error:", error)
else:
    REPORTS_IMPORT_ERROR = ""


# ============================================================
# COLORS
# ============================================================

SIDEBAR = "#0F172A"
TOPBAR_BLUE = "#DBEAFE"
TOPBAR_BORDER = "#BFDBFE"
TOPBAR_TEXT = "#1E3A8A"
TOPBAR_MUTED = "#475569"
SIDEBAR_HOVER = "#1E293B"
SIDEBAR_TEXT = "#CBD5E1"
SIDEBAR_MUTED = "#64748B"

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

INDIGO = "#4F46E5"
LIGHT_INDIGO = "#EEF2FF"

YELLOW = "#FACC15"

WHITE = "#FFFFFF"
BG = "#F8FAFC"

TEXT = "#0F172A"
GRAY = "#64748B"

BORDER = "#E2E8F0"


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
# LOGGED-IN ACCOUNTANT
#
# Supported:
#
# 1.
# accountant_dashboard.py "Name" "Username"
#
# 2.
# accountant_dashboard.py "Registration_No" "Name" "Username"
#
# ============================================================

ACCOUNTANT_REGISTRATION_NO = ""
ACCOUNTANT_NAME = ""
ACCOUNTANT_USERNAME = ""


if len(sys.argv) >= 4:

    ACCOUNTANT_REGISTRATION_NO = (
        sys.argv[1].strip()
    )

    ACCOUNTANT_NAME = (
        sys.argv[2].strip()
    )

    ACCOUNTANT_USERNAME = (
        sys.argv[3].strip()
    )


elif len(sys.argv) >= 3:

    ACCOUNTANT_NAME = (
        sys.argv[1].strip()
    )

    ACCOUNTANT_USERNAME = (
        sys.argv[2].strip()
    )


elif len(sys.argv) >= 2:

    ACCOUNTANT_USERNAME = (
        sys.argv[1].strip()
    )


# ============================================================
# LOAD ACCOUNTANT DETAILS FROM DATABASE
#
# This makes the dashboard safer.
# Even if only Username is passed, the actual Name is loaded.
# ============================================================

def load_logged_in_accountant():

    global ACCOUNTANT_REGISTRATION_NO
    global ACCOUNTANT_NAME
    global ACCOUNTANT_USERNAME


    # --------------------------------------------------------
    # IF USERNAME EXISTS, LOAD USER FROM DATABASE
    # --------------------------------------------------------

    if ACCOUNTANT_USERNAME:

        con = None
        cursor = None

        try:

            con = get_connection()

            cursor = con.cursor()


            cursor.execute(
                """
                SELECT
                    Registration_No,
                    Name,
                    Username,
                    Role

                FROM registration

                WHERE Username = %s

                LIMIT 1
                """,
                (
                    ACCOUNTANT_USERNAME,
                )
            )


            result = cursor.fetchone()


            if result:

                ACCOUNTANT_REGISTRATION_NO = str(
                    result[0]
                ).strip()

                ACCOUNTANT_NAME = str(
                    result[1]
                ).strip()

                ACCOUNTANT_USERNAME = str(
                    result[2]
                ).strip()


        except mysql.connector.Error:

            # Keep the values received from login.py
            pass


        finally:

            if cursor is not None:

                cursor.close()


            if (
                con is not None
                and con.is_connected()
            ):

                con.close()


    # --------------------------------------------------------
    # FINAL FALLBACK
    # --------------------------------------------------------

    if not ACCOUNTANT_NAME:

        ACCOUNTANT_NAME = "Accountant"


load_logged_in_accountant()


# ============================================================
# MAIN WINDOW
# ============================================================

window = Tk()

window.title(
    "Accountant Dashboard - Fee Status Management System"
)

window.geometry(
    "1536x864"
)

window.minsize(
    1200,
    700
)

window.configure(
    bg=BG
)


try:

    window.state(
        "zoomed"
    )

except TclError:

    pass


# ============================================================
# SIDEBAR BUTTON STORAGE
# ============================================================

sidebar_buttons = {}


# ============================================================
# MAIN LAYOUT
# ============================================================

sidebar = Frame(
    window,
    bg=SIDEBAR,
    width=235
)

sidebar.pack(
    side=LEFT,
    fill=Y
)

sidebar.pack_propagate(
    False
)


main_area = Frame(
    window,
    bg=BG
)

main_area.pack(
    side=RIGHT,
    fill=BOTH,
    expand=True
)


# ============================================================
# SIDEBAR BRAND
# ============================================================

brand_frame = Frame(
    sidebar,
    bg=SIDEBAR,
    height=115
)

brand_frame.pack(
    fill=X
)

brand_frame.pack_propagate(
    False
)


logo_box = Frame(
    brand_frame,
    bg=BLUE,
    width=42,
    height=42
)

logo_box.place(
    x=20,
    y=27
)

logo_box.pack_propagate(
    False
)


Label(
    logo_box,
    text="₹",
    bg=BLUE,
    fg=WHITE,
    font=(
        "Helvetica",
        21,
        "bold"
    )
).pack(
    expand=True
)


Label(
    brand_frame,
    text="FEE STATUS",
    bg=SIDEBAR,
    fg=WHITE,
    font=(
        "Helvetica",
        13,
        "bold"
    )
).place(
    x=76,
    y=29
)


Label(
    brand_frame,
    text="MANAGEMENT SYSTEM",
    bg=SIDEBAR,
    fg="#93C5FD",
    font=(
        "Helvetica",
        7
    )
).place(
    x=76,
    y=53
)


Frame(
    sidebar,
    bg="#1E293B",
    height=1
).pack(
    fill=X,
    padx=18
)


# ============================================================
# ACCOUNTANT PANEL LABEL
# ============================================================

Label(
    sidebar,
    text="ACCOUNTANT PANEL",
    bg=SIDEBAR,
    fg=SIDEBAR_MUTED,
    font=(
        "Helvetica",
        8,
        "bold"
    )
).pack(
    anchor="w",
    padx=28,
    pady=(22, 12)
)


# ============================================================
# TOPBAR
# ============================================================

topbar = Frame(
    main_area,
    bg=TOPBAR_BLUE,
    height=86,
    highlightbackground=TOPBAR_BORDER,
    highlightthickness=1
)

topbar.pack(
    fill=X
)

topbar.pack_propagate(
    False
)


# ============================================================
# PAGE TITLE VARIABLES
# ============================================================

page_title_var = StringVar(
    value="Dashboard"
)

page_subtitle_var = StringVar(
    value=(
        "Overview of fee collection "
        "and student payment status."
    )
)


# ============================================================
# TOPBAR TITLE
# ============================================================

Label(
    topbar,
    textvariable=page_title_var,
    bg=TOPBAR_BLUE,
    fg=TOPBAR_TEXT,
    font=(
        "Helvetica",
        19,
        "bold"
    )
).place(
    x=30,
    y=17
)


Label(
    topbar,
    textvariable=page_subtitle_var,
    bg=TOPBAR_BLUE,
    fg=TOPBAR_MUTED,
    font=(
        "Helvetica",
        9
    )
).place(
    x=30,
    y=50
)


# ============================================================
# PROFILE AREA
# ============================================================

profile_frame = Frame(
    topbar,
    bg=TOPBAR_BLUE
)

profile_frame.pack(
    side=RIGHT,
    padx=30,
    pady=16
)


profile_initial = (
    ACCOUNTANT_NAME[0].upper()
    if ACCOUNTANT_NAME
    else "A"
)


Label(
    profile_frame,
    text=profile_initial,
    bg=BLUE,
    fg=WHITE,
    font=(
        "Helvetica",
        12,
        "bold"
    ),
    width=3,
    height=2
).pack(
    side=LEFT,
    padx=(0, 10)
)


profile_text = Frame(
    profile_frame,
    bg=TOPBAR_BLUE
)

profile_text.pack(
    side=LEFT
)


Label(
    profile_text,
    text=ACCOUNTANT_NAME,
    bg=TOPBAR_BLUE,
    fg="#0F172A",
    font=(
        "Helvetica",
        10,
        "bold"
    )
).pack(
    anchor="w"
)


Label(
    profile_text,
    text="Accountant",
    bg=TOPBAR_BLUE,
    fg="#64748B",
    font=(
        "Helvetica",
        8
    )
).pack(
    anchor="w",
    pady=(2, 0)
)


# ============================================================
# DYNAMIC CONTENT PANEL
# ============================================================

content = Frame(
    main_area,
    bg=BG
)

content.pack(
    fill=BOTH,
    expand=True
)


# ============================================================
# CLEAR MAIN CONTENT
# ============================================================

def clear_content():

    for widget in content.winfo_children():

        widget.destroy()


# ============================================================
# SET ACTIVE SIDEBAR BUTTON
# ============================================================

def set_active_button(
    active_name
):

    for (
        button_name,
        button
    ) in sidebar_buttons.items():

        if button_name == active_name:

            button.config(
                bg=BLUE,
                fg=WHITE,
                activebackground=BLUE,
                activeforeground=WHITE
            )

        else:

            button.config(
                bg=SIDEBAR,
                fg=SIDEBAR_TEXT,
                activebackground=SIDEBAR_HOVER,
                activeforeground=WHITE
            )


# ============================================================
# MONEY FORMAT
# ============================================================

def money(
    value
):

    try:

        return (
            f"₹{float(value):,.2f}"
        )

    except (
        TypeError,
        ValueError
    ):

        return "₹0.00"


# ============================================================
# GET DASHBOARD DATA
# ============================================================

def get_dashboard_data():

    data = {

        "student_fees":
            0,

        "total_assigned":
            0,

        "total_collected":
            0,

        "total_due":
            0,

        "paid_students":
            0,

        "partial_students":
            0,

        "unpaid_students":
            0
    }


    con = None
    cursor = None


    try:

        con = get_connection()

        cursor = con.cursor(
            dictionary=True
        )


        # ----------------------------------------------------
        # TOTAL FEE DATA
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT

                COUNT(*)
                    AS Student_Fees,

                COALESCE(
                    SUM(Total_Fee),
                    0
                )
                    AS Total_Assigned,

                COALESCE(
                    SUM(Amount_Paid),
                    0
                )
                    AS Total_Collected,

                COALESCE(
                    SUM(Due_Amount),
                    0
                )
                    AS Total_Due

            FROM student_fees
            """
        )


        result = cursor.fetchone()


        if result:

            data[
                "student_fees"
            ] = (
                result[
                    "Student_Fees"
                ]
                or 0
            )


            data[
                "total_assigned"
            ] = (
                result[
                    "Total_Assigned"
                ]
                or 0
            )


            data[
                "total_collected"
            ] = (
                result[
                    "Total_Collected"
                ]
                or 0
            )


            data[
                "total_due"
            ] = (
                result[
                    "Total_Due"
                ]
                or 0
            )


        # ----------------------------------------------------
        # STATUS COUNTS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT

                COALESCE(
                    SUM(
                        CASE

                            WHEN LOWER(
                                TRIM(
                                    Payment_Status
                                )
                            ) = 'paid'

                            THEN 1

                            ELSE 0

                        END
                    ),
                    0
                )
                    AS Paid_Students,


                COALESCE(
                    SUM(
                        CASE

                            WHEN LOWER(
                                TRIM(
                                    Payment_Status
                                )
                            ) = 'partial'

                            THEN 1

                            ELSE 0

                        END
                    ),
                    0
                )
                    AS Partial_Students,


                COALESCE(
                    SUM(
                        CASE

                            WHEN LOWER(
                                TRIM(
                                    Payment_Status
                                )
                            ) = 'unpaid'

                            THEN 1

                            ELSE 0

                        END
                    ),
                    0
                )
                    AS Unpaid_Students

            FROM student_fees
            """
        )


        status_result = (
            cursor.fetchone()
        )


        if status_result:

            data[
                "paid_students"
            ] = (
                status_result[
                    "Paid_Students"
                ]
                or 0
            )


            data[
                "partial_students"
            ] = (
                status_result[
                    "Partial_Students"
                ]
                or 0
            )


            data[
                "unpaid_students"
            ] = (
                status_result[
                    "Unpaid_Students"
                ]
                or 0
            )


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            (
                "Could not load dashboard data."
                f"\n\n{error}"
            ),
            parent=window
        )


    finally:

        if cursor is not None:

            cursor.close()


        if (
            con is not None
            and con.is_connected()
        ):

            con.close()


    return data


# ============================================================
# TEMPORARY PAGE
# ============================================================

def show_temporary_page(
    page_name,
    subtitle
):

    clear_content()


    page_title_var.set(
        page_name
    )


    page_subtitle_var.set(
        subtitle
    )


    set_active_button(
        page_name
    )


    page_wrapper = Frame(
        content,
        bg=BG
    )

    page_wrapper.pack(
        fill=BOTH,
        expand=True
    )


    center_card = Frame(
        page_wrapper,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1,
        width=500,
        height=260
    )

    center_card.place(
        relx=0.5,
        rely=0.45,
        anchor=CENTER
    )

    center_card.pack_propagate(
        False
    )


    Label(
        center_card,
        text=page_name,
        bg=WHITE,
        fg=TEXT,
        font=(
            "Helvetica",
            22,
            "bold"
        )
    ).pack(
        pady=(55, 10)
    )


    Label(
        center_card,
        text=(
            f"{page_name} page will load "
            "inside this main panel."
        ),
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            10
        )
    ).pack()


    Button(
        center_card,
        text="BACK TO DASHBOARD",
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
        command=show_dashboard
    ).pack(
        pady=30,
        ipadx=20,
        ipady=8
    )


# ============================================================
# STUDENT FEES PAGE
# ============================================================

def show_student_fees(
    status_filter="All"
):

    if show_student_fees_page is None:

        messagebox.showerror(
            "Student Fees Module Error",
            (
                "Unable to load student_fees_page.py."
                "\n\n"
                "Make sure this file exists:"
                f"\n{STUDENT_FEES_FILE}"
            ),
            parent=window
        )

        return


    clear_content()


    page_title_var.set(
        "Student Fees"
    )


    page_subtitle_var.set(
        (
            "Search students, view assigned fees, "
            "check payment status and record payments."
        )
    )


    set_active_button(
        "Student Fees"
    )


    try:

        show_student_fees_page(
            parent=content,
            status_filter=status_filter,
            refresh_dashboard_callback=None
        )


    except TypeError:

        show_student_fees_page(
            parent=content,
            status_filter=status_filter
        )


    except Exception as error:

        messagebox.showerror(
            "Student Fees Error",
            (
                "Unable to open the Student Fees page."
                f"\n\n{error}"
            ),
            parent=window
        )


        show_dashboard()


# ============================================================
# ASSIGN FEES PAGE
# ============================================================

def show_assign_fees():

    # --------------------------------------------------------
    # CHECK WHETHER MODULE LOADED SUCCESSFULLY
    # --------------------------------------------------------

    if open_assign_fees_page is None:

        messagebox.showerror(
            "Assign Fees Module Error",
            (
                "Unable to load assign_fees_page.py."
                "\n\n"
                "Make sure this file exists:"
                f"\n{ASSIGN_FEES_FILE}"
                "\n\n"
                "Import error:"
                f"\n{ASSIGN_FEES_IMPORT_ERROR}"
            ),
            parent=window
        )

        return


    # --------------------------------------------------------
    # CLEAR ONLY THE DASHBOARD CONTENT AREA
    # --------------------------------------------------------

    clear_content()


    # --------------------------------------------------------
    # UPDATE TOPBAR
    # --------------------------------------------------------

    page_title_var.set(
        "Assign Fees"
    )


    page_subtitle_var.set(
        (
            "Search a student and assign "
            "semester-wise fee structures."
        )
    )


    # --------------------------------------------------------
    # ACTIVE SIDEBAR BUTTON
    # --------------------------------------------------------

    set_active_button(
        "Assign Fees"
    )


    # --------------------------------------------------------
    # OPEN ASSIGN FEES INSIDE DASHBOARD CONTENT FRAME
    # --------------------------------------------------------

    try:

        open_assign_fees_page(
            parent=content,
            user_role="Accountant",
            current_user_name=ACCOUNTANT_NAME,
            current_user_id=ACCOUNTANT_REGISTRATION_NO
        )


    except Exception as error:

        messagebox.showerror(
            "Assign Fees Error",
            (
                "Unable to open the Assign Fees page."
                "\n\n"
                f"{type(error).__name__}: {error}"
            ),
            parent=window
        )

        show_dashboard()


# ============================================================
# PAYMENTS PAGE
# ============================================================

def show_payments():

    if open_payments_page is None:

        messagebox.showerror(
            "Payments Module Error",
            (
                "Unable to load payments_page.py."
                "\n\n"
                "Make sure this file exists:"
                f"\n{PAYMENTS_FILE}"
                "\n\n"
                "Import error:"
                f"\n{PAYMENTS_IMPORT_ERROR}"
            ),
            parent=window
        )

        return


    clear_content()


    page_title_var.set(
        "Payments"
    )


    page_subtitle_var.set(
        (
            "View your collection history, "
            "search transactions and check payment details."
        )
    )


    set_active_button(
        "Payments"
    )


    try:

        open_payments_page(
            parent=content,
            current_user_name=ACCOUNTANT_NAME,
            current_user_id=ACCOUNTANT_REGISTRATION_NO,
            current_username=ACCOUNTANT_USERNAME,
            user_role="Accountant",
            back_command=show_dashboard
        )


    except Exception as error:

        messagebox.showerror(
            "Payments Error",
            (
                "Unable to open the Payments page."
                "\n\n"
                f"{type(error).__name__}: {error}"
            ),
            parent=window
        )

        show_dashboard()


# ============================================================
# REPORTS PAGE PLACEHOLDER
# ============================================================

def show_reports():

    if open_reports_page is None:
        messagebox.showerror(
            "Reports Module Error",
            (
                "Unable to load reports_page.py."
                "\n\n"
                f"Expected file: {REPORTS_FILE}"
                "\n\n"
                f"Import error: {REPORTS_IMPORT_ERROR}"
            ),
            parent=window
        )
        return

    clear_content()

    page_title_var.set("Reports")
    page_subtitle_var.set(
        "Generate and export your personal collection report."
    )

    set_active_button("Reports")

    try:
        open_reports_page(
            parent=content,
            current_user_name=ACCOUNTANT_NAME,
            current_user_id=ACCOUNTANT_REGISTRATION_NO,
            current_username=ACCOUNTANT_USERNAME,
            user_role="Accountant",
            back_command=show_dashboard
        )

    except Exception as error:
        messagebox.showerror(
            "Reports Error",
            (
                "Unable to open the Reports page."
                "\n\n"
                f"{type(error).__name__}: {error}"
            ),
            parent=window
        )
        show_dashboard()


def create_dashboard_card(
    parent,
    title,
    value,
    footer,
    accent_bg,
    accent_fg,
    command,
    column,
    icon_text
):

    card = Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1,
        cursor="hand2"
    )

    card.grid(
        row=0,
        column=column,
        sticky="nsew",
        padx=5
    )


    # --------------------------------------------------------
    # TOP ACCENT
    # --------------------------------------------------------

    accent = Frame(
        card,
        bg=accent_fg,
        height=4
    )

    accent.pack(
        fill=X
    )


    # --------------------------------------------------------
    # CARD BODY
    # --------------------------------------------------------

    card_body = Frame(
        card,
        bg=WHITE,
        cursor="hand2"
    )

    card_body.pack(
        fill=BOTH,
        expand=True,
        padx=13,
        pady=12
    )


    # --------------------------------------------------------
    # ICON BOX
    # --------------------------------------------------------

    icon_box = Label(
        card_body,
        text=icon_text,
        bg=accent_bg,
        fg=accent_fg,
        font=(
            "Helvetica",
            10,
            "bold"
        ),
        width=4,
        height=1,
        cursor="hand2"
    )

    icon_box.pack(
        anchor="w"
    )


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title_label = Label(
        card_body,
        text=title,
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            7,
            "bold"
        ),
        anchor="w",
        justify=LEFT,
        cursor="hand2"
    )

    title_label.pack(
        anchor="w",
        pady=(10, 5)
    )


    # --------------------------------------------------------
    # VALUE
    # --------------------------------------------------------

    value_label = Label(
        card_body,
        text=value,
        bg=WHITE,
        fg=TEXT,
        font=(
            "Helvetica",
            13,
            "bold"
        ),
        anchor="w",
        cursor="hand2"
    )

    value_label.pack(
        anchor="w"
    )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    footer_label = Label(
        card_body,
        text=footer,
        bg=WHITE,
        fg=accent_fg,
        font=(
            "Helvetica",
            7,
            "bold"
        ),
        anchor="w",
        cursor="hand2"
    )

    footer_label.pack(
        anchor="w",
        pady=(12, 0)
    )


    # --------------------------------------------------------
    # CLICK EVENT
    #
    # Entire card remains clickable.
    # No hover bindings.
    # --------------------------------------------------------

    clickable_widgets = [

        card,
        accent,
        card_body,
        icon_box,
        title_label,
        value_label,
        footer_label
    ]


    for widget in clickable_widgets:

        widget.bind(
            "<Button-1>",
            lambda event,
            action=command:
            action()
        )


# ============================================================
# LOAD RECENT PAYMENTS
# ============================================================

def load_recent_payments(
    tree
):

    for item in tree.get_children():

        tree.delete(
            item
        )


    con = None
    cursor = None


    try:

        con = get_connection()

        cursor = con.cursor()


        cursor.execute(
            """
            SELECT

                fp.Payment_ID,

                r.Name,

                sf.Registration_No,

                fp.Amount,

                fp.Payment_Mode,

                fp.Payment_Date

            FROM fee_payments fp

            INNER JOIN student_fees sf

                ON sf.Student_Fee_ID
                =
                fp.Student_Fee_ID

            INNER JOIN registration r

                ON r.Registration_No
                =
                sf.Registration_No

            ORDER BY
                fp.Payment_ID DESC

            LIMIT 8
            """
        )


        records = cursor.fetchall()


        for record in records:

            payment_id = (
                f"PAY-{int(record[0]):06d}"
            )


            tree.insert(
                "",
                END,
                values=(
                    payment_id,
                    record[1],
                    record[2],
                    money(
                        record[3]
                    ),
                    record[4],
                    record[5]
                )
            )


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            (
                "Could not load recent payments."
                f"\n\n{error}"
            ),
            parent=window
        )


    finally:

        if cursor is not None:

            cursor.close()


        if (
            con is not None
            and con.is_connected()
        ):

            con.close()


# ============================================================
# SHOW DASHBOARD
# ============================================================

def show_dashboard():

    # --------------------------------------------------------
    # CLEAR CURRENT PAGE
    # --------------------------------------------------------

    clear_content()


    # --------------------------------------------------------
    # PAGE INFORMATION
    # --------------------------------------------------------

    page_title_var.set(
        "Dashboard"
    )


    page_subtitle_var.set(
        (
            "Overview of fee collection "
            "and student payment status."
        )
    )


    set_active_button(
        "Dashboard"
    )


    # --------------------------------------------------------
    # GET DATABASE DATA
    # --------------------------------------------------------

    dashboard_data = (
        get_dashboard_data()
    )


    # ========================================================
    # MAIN DASHBOARD WRAPPER
    # ========================================================

    wrapper = Frame(
        content,
        bg=BG
    )

    wrapper.pack(
        fill=BOTH,
        expand=True,
        padx=24,
        pady=20
    )


    # ========================================================
    # WELCOME SECTION
    # ========================================================

    welcome = Frame(
        wrapper,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    welcome.pack(
        fill=X,
        pady=(0, 16)
    )


    welcome_left = Frame(
        welcome,
        bg=WHITE
    )

    welcome_left.pack(
        side=LEFT,
        padx=22,
        pady=16
    )


    Label(
        welcome_left,
        text=(
            f"Welcome back, "
            f"{ACCOUNTANT_NAME}"
        ),
        bg=WHITE,
        fg=TEXT,
        font=(
            "Helvetica",
            17,
            "bold"
        )
    ).pack(
        anchor="w"
    )


    Label(
        welcome_left,
        text=(
            "Manage student fees, "
            "collect payments and "
            "track outstanding dues."
        ),
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            9
        )
    ).pack(
        anchor="w",
        pady=(5, 0)
    )


    # ========================================================
    # FEE OVERVIEW HEADER
    # ========================================================

    overview_header = Frame(
        wrapper,
        bg=BG
    )

    overview_header.pack(
        fill=X,
        pady=(0, 8)
    )


    Label(
        overview_header,
        text="FEE OVERVIEW",
        bg=BG,
        fg=TEXT,
        font=(
            "Helvetica",
            10,
            "bold"
        )
    ).pack(
        side=LEFT
    )


    Label(
        overview_header,
        text=(
            "Click any card to open "
            "the related section"
        ),
        bg=BG,
        fg=GRAY,
        font=(
            "Helvetica",
            8
        )
    ).pack(
        side=LEFT,
        padx=12
    )


    # ========================================================
    # 7 DASHBOARD CARDS IN ONE ROW
    # ========================================================

    cards_frame = Frame(
        wrapper,
        bg=BG
    )

    cards_frame.pack(
        fill=X,
        pady=(0, 18)
    )


    for column in range(7):

        cards_frame.grid_columnconfigure(
            column,
            weight=1,
            uniform="dashboard_cards"
        )


    # --------------------------------------------------------
    # CARD 1 - STUDENT FEES
    # --------------------------------------------------------

    create_dashboard_card(
        cards_frame,
        "STUDENT FEES",
        str(
            dashboard_data[
                "student_fees"
            ]
        ),
        "View Students  →",
        LIGHT_BLUE,
        BLUE,
        lambda:
        show_student_fees(
            "All"
        ),
        0,
        "ST"
    )


    # --------------------------------------------------------
    # CARD 2 - TOTAL ASSIGNED
    # --------------------------------------------------------

    create_dashboard_card(
        cards_frame,
        "TOTAL ASSIGNED",
        money(
            dashboard_data[
                "total_assigned"
            ]
        ),
        "View Fees  →",
        LIGHT_INDIGO,
        INDIGO,
        lambda:
        show_student_fees(
            "All"
        ),
        1,
        "₹"
    )


    # --------------------------------------------------------
    # CARD 3 - TOTAL COLLECTED
    # --------------------------------------------------------

    create_dashboard_card(
        cards_frame,
        "TOTAL COLLECTED",
        money(
            dashboard_data[
                "total_collected"
            ]
        ),
        "View Payments  →",
        LIGHT_GREEN,
        GREEN,
        show_payments,
        2,
        "₹"
    )


    # --------------------------------------------------------
    # CARD 4 - TOTAL DUE
    # --------------------------------------------------------

    create_dashboard_card(
        cards_frame,
        "TOTAL DUE",
        money(
            dashboard_data[
                "total_due"
            ]
        ),
        "View Due Fees  →",
        LIGHT_ORANGE,
        ORANGE,
        lambda:
        show_student_fees(
            "Due"
        ),
        3,
        "₹"
    )


    # --------------------------------------------------------
    # CARD 5 - PAID STUDENTS
    # --------------------------------------------------------

    create_dashboard_card(
        cards_frame,
        "PAID STUDENTS",
        str(
            dashboard_data[
                "paid_students"
            ]
        ),
        "View Paid  →",
        LIGHT_GREEN,
        GREEN,
        lambda:
        show_student_fees(
            "Paid"
        ),
        4,
        "P"
    )


    # --------------------------------------------------------
    # CARD 6 - PARTIAL STUDENTS
    # --------------------------------------------------------

    create_dashboard_card(
        cards_frame,
        "PARTIAL STUDENTS",
        str(
            dashboard_data[
                "partial_students"
            ]
        ),
        "View Partial  →",
        LIGHT_PURPLE,
        PURPLE,
        lambda:
        show_student_fees(
            "Partial"
        ),
        5,
        "PT"
    )


    # --------------------------------------------------------
    # CARD 7 - UNPAID STUDENTS
    # --------------------------------------------------------

    create_dashboard_card(
        cards_frame,
        "UNPAID STUDENTS",
        str(
            dashboard_data[
                "unpaid_students"
            ]
        ),
        "View Unpaid  →",
        LIGHT_RED,
        RED,
        lambda:
        show_student_fees(
            "Unpaid"
        ),
        6,
        "U"
    )


    # ========================================================
    # RECENT PAYMENTS CARD
    # ========================================================

    recent_card = Frame(
        wrapper,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    recent_card.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # RECENT PAYMENTS HEADER
    # ========================================================

    recent_header = Frame(
        recent_card,
        bg=WHITE
    )

    recent_header.pack(
        fill=X,
        padx=20,
        pady=(16, 12)
    )


    recent_header_left = Frame(
        recent_header,
        bg=WHITE
    )

    recent_header_left.pack(
        side=LEFT
    )


    Label(
        recent_header_left,
        text="Recent Payments",
        bg=WHITE,
        fg=TEXT,
        font=(
            "Helvetica",
            13,
            "bold"
        )
    ).pack(
        anchor="w"
    )


    Label(
        recent_header_left,
        text=(
            "Latest student fee payments "
            "recorded in the system."
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


    Button(
        recent_header,
        text="VIEW ALL PAYMENTS",
        bg=LIGHT_BLUE,
        fg=BLUE,
        activebackground=LIGHT_BLUE,
        activeforeground=BLUE,
        bd=0,
        relief=FLAT,
        cursor="hand2",
        font=(
            "Helvetica",
            8,
            "bold"
        ),
        command=show_payments
    ).pack(
        side=RIGHT,
        ipadx=12,
        ipady=7
    )


    # ========================================================
    # TREEVIEW STYLE
    # ========================================================

    style = ttk.Style()


    try:

        style.theme_use(
            "clam"
        )

    except TclError:

        pass


    style.configure(
        "Accountant.Treeview",
        background=WHITE,
        foreground=TEXT,
        fieldbackground=WHITE,
        rowheight=38,
        borderwidth=0,
        font=(
            "Helvetica",
            9
        )
    )


    style.configure(
        "Accountant.Treeview.Heading",
        background="#F8FAFC",
        foreground=GRAY,
        borderwidth=0,
        relief=FLAT,
        font=(
            "Helvetica",
            8,
            "bold"
        )
    )


    style.map(
        "Accountant.Treeview",
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

    table_frame = Frame(
        recent_card,
        bg=WHITE
    )

    table_frame.pack(
        fill=BOTH,
        expand=True,
        padx=20,
        pady=(0, 18)
    )


    columns = (

        "payment_id",

        "student",

        "registration",

        "amount",

        "mode",

        "date"
    )


    payment_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Accountant.Treeview"
    )


    # --------------------------------------------------------
    # HEADINGS
    # --------------------------------------------------------

    payment_tree.heading(
        "payment_id",
        text="PAYMENT ID"
    )


    payment_tree.heading(
        "student",
        text="STUDENT"
    )


    payment_tree.heading(
        "registration",
        text="REGISTRATION NO."
    )


    payment_tree.heading(
        "amount",
        text="AMOUNT"
    )


    payment_tree.heading(
        "mode",
        text="PAYMENT MODE"
    )


    payment_tree.heading(
        "date",
        text="PAYMENT DATE"
    )


    # --------------------------------------------------------
    # COLUMNS
    # --------------------------------------------------------

    payment_tree.column(
        "payment_id",
        width=125,
        minwidth=100,
        anchor=CENTER
    )


    payment_tree.column(
        "student",
        width=220,
        minwidth=160,
        anchor=W
    )


    payment_tree.column(
        "registration",
        width=170,
        minwidth=140,
        anchor=CENTER
    )


    payment_tree.column(
        "amount",
        width=150,
        minwidth=120,
        anchor=E
    )


    payment_tree.column(
        "mode",
        width=150,
        minwidth=120,
        anchor=CENTER
    )


    payment_tree.column(
        "date",
        width=150,
        minwidth=120,
        anchor=CENTER
    )


    # --------------------------------------------------------
    # SCROLLBAR
    # --------------------------------------------------------

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient=VERTICAL,
        command=payment_tree.yview
    )


    payment_tree.configure(
        yscrollcommand=scrollbar.set
    )


    payment_tree.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )


    scrollbar.pack(
        side=RIGHT,
        fill=Y
    )


    # --------------------------------------------------------
    # LOAD DATABASE DATA
    # --------------------------------------------------------

    load_recent_payments(
        payment_tree
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
                "Change Password file "
                "was not found."
                f"\n\n{CHANGE_PASSWORD_FILE}"
            ),
            parent=window
        )

        return


    try:

        command = [

            sys.executable,

            CHANGE_PASSWORD_FILE
        ]


        if ACCOUNTANT_USERNAME:

            command.append(
                ACCOUNTANT_USERNAME
            )


        subprocess.Popen(
            command,
            cwd=PROJECT_DIR
        )


    except Exception as error:

        messagebox.showerror(
            "Open Error",
            (
                "Unable to open "
                "Change Password."
                f"\n\n{error}"
            ),
            parent=window
        )


# ============================================================
# LOGOUT
# ============================================================

def logout():

    confirm = messagebox.askyesno(
        "Logout",
        (
            "Are you sure you want "
            "to logout?"
        ),
        parent=window
    )


    if not confirm:

        return


    try:

        window.destroy()


        if os.path.exists(
            LOGIN_FILE
        ):

            subprocess.Popen(
                [
                    sys.executable,
                    LOGIN_FILE
                ],
                cwd=PROJECT_DIR
            )


    except Exception as error:

        messagebox.showerror(
            "Logout Error",
            str(
                error
            )
        )


# ============================================================
# CREATE SIDEBAR BUTTON
# ============================================================

def create_sidebar_button(
    name,
    command
):

    button = Button(
        sidebar,
        text=name,
        bg=SIDEBAR,
        fg=SIDEBAR_TEXT,
        activebackground=SIDEBAR_HOVER,
        activeforeground=WHITE,
        bd=0,
        relief=FLAT,
        anchor="w",
        padx=22,
        cursor="hand2",
        font=(
            "Helvetica",
            9
        ),
        command=command
    )


    button.pack(
        fill=X,
        padx=14,
        pady=3,
        ipady=9
    )


    sidebar_buttons[
        name
    ] = button


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

create_sidebar_button(
    "Dashboard",
    show_dashboard
)


create_sidebar_button(
    "Student Fees",
    lambda:
    show_student_fees(
        "All"
    )
)


create_sidebar_button(
    "Assign Fees",
    show_assign_fees
)


create_sidebar_button(
    "Payments",
    show_payments
)


create_sidebar_button(
    "Reports",
    show_reports
)


# ============================================================
# SIDEBAR BOTTOM ACTIONS
# ============================================================

bottom_frame = Frame(
    sidebar,
    bg=SIDEBAR
)

bottom_frame.pack(
    side=BOTTOM,
    fill=X,
    padx=14,
    pady=14
)


# ============================================================
# LOGGED-IN ACCOUNTANT INFO
# ============================================================

account_info = Frame(
    bottom_frame,
    bg="#1E293B"
)

account_info.pack(
    fill=X,
    pady=(0, 10)
)


Label(
    account_info,
    text=ACCOUNTANT_NAME,
    bg="#1E293B",
    fg=WHITE,
    font=(
        "Helvetica",
        9,
        "bold"
    ),
    wraplength=175,
    justify=LEFT
).pack(
    anchor="w",
    padx=12,
    pady=(10, 2)
)


Label(
    account_info,
    text=(
        ACCOUNTANT_USERNAME
        if ACCOUNTANT_USERNAME
        else "Accountant"
    ),
    bg="#1E293B",
    fg="#94A3B8",
    font=(
        "Helvetica",
        8
    )
).pack(
    anchor="w",
    padx=12,
    pady=(0, 10)
)


# ============================================================
# CHANGE PASSWORD BUTTON
# ============================================================

Button(
    bottom_frame,
    text="Change Password",
    bg=YELLOW,
    fg="#111827",
    activebackground=YELLOW,
    activeforeground="#111827",
    bd=0,
    relief=FLAT,
    cursor="hand2",
    font=(
        "Helvetica",
        9,
        "bold"
    ),
    command=change_password
).pack(
    fill=X,
    ipady=9,
    pady=(0, 7)
)


# ============================================================
# LOGOUT BUTTON
# ============================================================

Button(
    bottom_frame,
    text="Logout",
    bg="#EF4444",
    fg=WHITE,
    activebackground="#EF4444",
    activeforeground=WHITE,
    bd=0,
    relief=FLAT,
    cursor="hand2",
    font=(
        "Helvetica",
        9,
        "bold"
    ),
    command=logout
).pack(
    fill=X,
    ipady=9
)


# ============================================================
# INITIAL PAGE
# ============================================================

show_dashboard()


# ============================================================
# MAIN LOOP
# ============================================================

window.mainloop()