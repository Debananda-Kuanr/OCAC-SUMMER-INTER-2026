from tkinter import *
from tkinter import messagebox
import mysql.connector


# ============================================================
# DATABASE CONFIGURATION
# ============================================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "9439",
    "database": "OCAC"
}


# ============================================================
# COLORS
# ============================================================
NAVY = "#071A33"
NAVY_2 = "#0D2B4D"
NAVY_3 = "#12385F"

BLUE = "#2563EB"
BLUE_HOVER = "#1D4ED8"

GREEN = "#16A34A"
GREEN_HOVER = "#15803D"

RED = "#DC2626"
RED_HOVER = "#B91C1C"

AMBER = "#F59E0B"

SLATE = "#64748B"
SLATE_HOVER = "#475569"

PURPLE = "#8B5CF6"

BG = "#F1F5F9"
CARD = "#FFFFFF"

TEXT = "#0F172A"
MUTED = "#64748B"

BORDER = "#DCE5F0"

LIGHT_BLUE = "#EFF6FF"
LIGHT_GREEN = "#DCFCE7"
LIGHT_AMBER = "#FEF3C7"


# ============================================================
# MAIN WINDOW
# ============================================================
window = Tk()

window.title(
    "OCAC - Student Management Portal"
)

window.geometry(
    "1400x850"
)

window.minsize(
    1100,
    700
)

window.configure(
    bg=BG
)


# Open maximized
try:
    window.state(
        "zoomed"
    )

except TclError:
    pass


# F11 = Fullscreen
window.bind(
    "<F11>",
    lambda event: window.attributes(
        "-fullscreen",
        True
    )
)


# Escape = Exit fullscreen
window.bind(
    "<Escape>",
    lambda event: window.attributes(
        "-fullscreen",
        False
    )
)


# ============================================================
# DATABASE CONNECTION
# ============================================================
try:

    con = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

    cursor = con.cursor()


except mysql.connector.Error as error:

    messagebox.showerror(
        "Database Error",
        f"Database connection failed:\n\n"
        f"{error}\n\n"
        f"Please check MySQL and your database configuration."
    )

    window.destroy()

    raise SystemExit


# ============================================================
# GLOBAL VARIABLES
# ============================================================
password_visible = False

current_student = None


# ============================================================
# HOVER EFFECT
# ============================================================
def add_hover(
    button,
    normal_color,
    hover_color
):

    button.bind(
        "<Enter>",
        lambda event: button.config(
            bg=hover_color
        )
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(
            bg=normal_color
        )
    )


# ============================================================
# SHOW / HIDE PASSWORD
# ============================================================
def toggle_password():

    global password_visible

    password_visible = not password_visible


    if password_visible:

        password_entry.config(
            show=""
        )

        show_button.config(
            text="HIDE"
        )


    else:

        password_entry.config(
            show="*"
        )

        show_button.config(
            text="SHOW"
        )


# ============================================================
# CLEAR LOGIN FORM
# ============================================================
def clear_login():

    username_entry.delete(
        0,
        END
    )

    password_entry.delete(
        0,
        END
    )

    login_status.config(
        text=""
    )

    username_entry.focus()


# ============================================================
# STUDENT LOGIN
# ============================================================
def student_login():

    global current_student

    username = username_entry.get().strip()

    password = password_entry.get().strip()


    # Check username
    if username == "":

        login_status.config(
            text="Please enter your username.",
            fg=RED
        )

        username_entry.focus()

        return


    # Check password
    if password == "":

        login_status.config(
            text="Please enter your password.",
            fg=RED
        )

        password_entry.focus()

        return


    try:

        sql = """
        SELECT
            Roll_No,
            Name,
            Username
        FROM registration
        WHERE
            Username = %s
            AND Password = %s
        """


        cursor.execute(
            sql,
            (
                username,
                password
            )
        )


        result = cursor.fetchone()


        # Login successful
        if result:

            current_student = result

            login_status.config(
                text="Login successful.",
                fg=GREEN
            )

            open_student_dashboard(
                result
            )


        # Login failed
        else:

            login_status.config(
                text="Invalid username or password.",
                fg=RED
            )

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

            password_entry.delete(
                0,
                END
            )

            password_entry.focus()


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ============================================================
# OPEN STUDENT DASHBOARD
# ============================================================
def open_student_dashboard(
    student
):

    roll_no = student[0]

    name = student[1]

    username = student[2]


    # Hide login page
    login_page.pack_forget()


    # Update student information
    welcome_label.config(
        text=f"Welcome, {name}"
    )

    student_name_value.config(
        text=name
    )

    roll_value.config(
        text=str(roll_no)
    )

    profile_name_value.config(
        text=name
    )

    profile_roll_value.config(
        text=str(roll_no)
    )

    profile_username_value.config(
        text=username
    )


    # Demo transaction ID based on roll number
    transaction_value.config(
        text=f"OCAC2026{roll_no}"
    )


    # Show dashboard
    dashboard_frame.pack(
        fill=BOTH,
        expand=True
    )


# ============================================================
# LOGOUT
# ============================================================
def logout():

    global current_student

    confirm = messagebox.askyesno(
        "Logout",
        "Do you want to logout from your student account?"
    )


    if not confirm:
        return


    current_student = None


    # Hide dashboard
    dashboard_frame.pack_forget()


    # Clear login form
    clear_login()


    # Show login page
    login_page.pack(
        fill=BOTH,
        expand=True
    )


    username_entry.focus()


# ============================================================
# CLOSE APPLICATION
# ============================================================
def close_app():

    confirm = messagebox.askyesno(
        "Exit",
        "Do you want to close the OCAC Student Portal?"
    )


    if not confirm:
        return


    try:

        cursor.close()

        con.close()

    except:
        pass


    window.destroy()


# ============================================================
# LOGIN PAGE
# ============================================================
login_page = Frame(
    window,
    bg=BG
)

login_page.pack(
    fill=BOTH,
    expand=True
)


# ============================================================
# LOGIN PAGE HEADER
# ============================================================
header = Frame(
    login_page,
    bg=NAVY,
    height=75
)

header.pack(
    fill=X
)

header.pack_propagate(
    False
)


# ============================================================
# LOGIN HEADER BRAND
# ============================================================
brand_frame = Frame(
    header,
    bg=NAVY
)

brand_frame.pack(
    side=LEFT,
    padx=35
)


Label(
    brand_frame,
    text="OCAC",
    bg=NAVY,
    fg="white",
    font=(
        "Segoe UI",
        25,
        "bold"
    )
).pack(
    side=LEFT,
    pady=16
)


Frame(
    brand_frame,
    bg="#52677F",
    width=1,
    height=30
).pack(
    side=LEFT,
    padx=18
)


Label(
    brand_frame,
    text="Student Management Portal",
    bg=NAVY,
    fg="#C8D6E5",
    font=(
        "Segoe UI",
        12
    )
).pack(
    side=LEFT
)


# ============================================================
# LOGIN HEADER RIGHT
# ============================================================
Label(
    header,
    text="STUDENT LOGIN",
    bg=NAVY_2,
    fg="#DCE8F5",
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    padx=18,
    pady=9
).pack(
    side=RIGHT,
    padx=35
)


# ============================================================
# LOGIN BODY
# ============================================================
login_body = Frame(
    login_page,
    bg=BG
)

login_body.pack(
    fill=BOTH,
    expand=True
)


# ============================================================
# LEFT EDUCATION PANEL
# ============================================================
education_panel = Frame(
    login_body,
    bg=NAVY_2
)

education_panel.pack(
    side=LEFT,
    fill=BOTH,
    expand=True
)


education_content = Frame(
    education_panel,
    bg=NAVY_2
)

education_content.place(
    relx=0.5,
    rely=0.5,
    anchor=CENTER
)


# ============================================================
# EDUCATION ICON
# ============================================================
Label(
    education_content,
    text="🎓",
    bg=NAVY_2,
    fg="white",
    font=(
        "Segoe UI Emoji",
        70
    )
).pack(
    pady=(0, 20)
)


# ============================================================
# OCAC TITLE
# ============================================================
Label(
    education_content,
    text="OCAC",
    bg=NAVY_2,
    fg="white",
    font=(
        "Segoe UI",
        42,
        "bold"
    )
).pack()


# ============================================================
# PORTAL TITLE
# ============================================================
Label(
    education_content,
    text="Student Management Portal",
    bg=NAVY_2,
    fg="#D7E6F5",
    font=(
        "Segoe UI",
        18
    )
).pack(
    pady=(8, 15)
)


# ============================================================
# DESCRIPTION
# ============================================================
Label(
    education_content,
    text=(
        "Access your student account securely\n"
        "using your registered username and password."
    ),
    bg=NAVY_2,
    fg="#AFC6DC",
    justify=CENTER,
    font=(
        "Segoe UI",
        11
    )
).pack()


# ============================================================
# DECORATIVE LINE
# ============================================================
Frame(
    education_content,
    bg=BLUE,
    width=100,
    height=4
).pack(
    pady=30
)


# ============================================================
# TAGLINE
# ============================================================
Label(
    education_content,
    text="LEARN  •  GROW  •  SUCCEED",
    bg=NAVY_2,
    fg="#8EABC7",
    font=(
        "Segoe UI",
        9,
        "bold"
    )
).pack()


# ============================================================
# RIGHT LOGIN SECTION
# ============================================================
login_section = Frame(
    login_body,
    bg=BG
)

login_section.pack(
    side=RIGHT,
    fill=BOTH,
    expand=True
)


# ============================================================
# LOGIN CARD
# ============================================================
login_card = Frame(
    login_section,
    bg=CARD,
    width=440,
    height=520,
    highlightbackground=BORDER,
    highlightthickness=1
)

login_card.place(
    relx=0.5,
    rely=0.5,
    anchor=CENTER
)

login_card.pack_propagate(
    False
)


# ============================================================
# LOGIN CARD HEADER
# ============================================================
card_header = Frame(
    login_card,
    bg=CARD
)

card_header.pack(
    fill=X,
    padx=45,
    pady=(45, 30)
)


Label(
    card_header,
    text="Welcome Back",
    bg=CARD,
    fg=TEXT,
    font=(
        "Segoe UI",
        27,
        "bold"
    )
).pack(
    anchor=W
)


Label(
    card_header,
    text="Sign in to access your student account.",
    bg=CARD,
    fg=MUTED,
    font=(
        "Segoe UI",
        10
    )
).pack(
    anchor=W,
    pady=(7, 0)
)


# ============================================================
# LOGIN FORM
# ============================================================
login_form = Frame(
    login_card,
    bg=CARD
)

login_form.pack(
    fill=X,
    padx=45
)


# ============================================================
# USERNAME
# ============================================================
Label(
    login_form,
    text="USERNAME",
    bg=CARD,
    fg=MUTED,
    font=(
        "Segoe UI",
        9,
        "bold"
    )
).pack(
    anchor=W,
    pady=(0, 7)
)


username_border = Frame(
    login_form,
    bg=BORDER,
    padx=1,
    pady=1
)

username_border.pack(
    fill=X,
    pady=(0, 20)
)


username_entry = Entry(
    username_border,
    font=(
        "Segoe UI",
        12
    ),
    bg="white",
    fg=TEXT,
    insertbackground=TEXT,
    bd=0
)

username_entry.pack(
    fill=X,
    ipady=11,
    padx=12
)


# ============================================================
# PASSWORD
# ============================================================
Label(
    login_form,
    text="PASSWORD",
    bg=CARD,
    fg=MUTED,
    font=(
        "Segoe UI",
        9,
        "bold"
    )
).pack(
    anchor=W,
    pady=(0, 7)
)


password_row = Frame(
    login_form,
    bg=CARD
)

password_row.pack(
    fill=X,
    pady=(0, 12)
)


password_border = Frame(
    password_row,
    bg=BORDER,
    padx=1,
    pady=1
)

password_border.pack(
    side=LEFT,
    fill=X,
    expand=True
)


password_entry = Entry(
    password_border,
    font=(
        "Segoe UI",
        12
    ),
    bg="white",
    fg=TEXT,
    insertbackground=TEXT,
    show="*",
    bd=0
)

password_entry.pack(
    fill=X,
    ipady=11,
    padx=12
)


# ============================================================
# SHOW PASSWORD BUTTON
# ============================================================
show_button = Button(
    password_row,
    text="SHOW",
    command=toggle_password,
    bg=SLATE,
    fg="white",
    activebackground=SLATE_HOVER,
    activeforeground="white",
    font=(
        "Segoe UI",
        8,
        "bold"
    ),
    bd=0,
    cursor="hand2",
    padx=12,
    pady=12
)

show_button.pack(
    side=LEFT,
    padx=(7, 0)
)


add_hover(
    show_button,
    SLATE,
    SLATE_HOVER
)


# ============================================================
# LOGIN STATUS
# ============================================================
login_status = Label(
    login_form,
    text="",
    bg=CARD,
    fg=RED,
    font=(
        "Segoe UI",
        9,
        "bold"
    )
)

login_status.pack(
    anchor=W,
    pady=(0, 10)
)


# ============================================================
# LOGIN BUTTON
# ============================================================
login_button = Button(
    login_form,
    text="LOGIN TO STUDENT PORTAL",
    command=student_login,
    bg=BLUE,
    fg="white",
    activebackground=BLUE_HOVER,
    activeforeground="white",
    font=(
        "Segoe UI",
        11,
        "bold"
    ),
    bd=0,
    cursor="hand2",
    pady=12
)

login_button.pack(
    fill=X,
    pady=(5, 10)
)


add_hover(
    login_button,
    BLUE,
    BLUE_HOVER
)


# ============================================================
# CLEAR BUTTON
# ============================================================
clear_button = Button(
    login_form,
    text="CLEAR",
    command=clear_login,
    bg="#E2E8F0",
    fg=TEXT,
    activebackground="#CBD5E1",
    activeforeground=TEXT,
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    bd=0,
    cursor="hand2",
    pady=10
)

clear_button.pack(
    fill=X
)


add_hover(
    clear_button,
    "#E2E8F0",
    "#CBD5E1"
)


# ============================================================
# LOGIN FOOTER
# ============================================================
Label(
    login_card,
    text=(
        "Use the username and password "
        "provided by the administrator."
    ),
    bg=CARD,
    fg=MUTED,
    font=(
        "Segoe UI",
        8
    )
).pack(
    side=BOTTOM,
    pady=25
)


# ============================================================
# ENTER KEY LOGIN
# ============================================================
username_entry.bind(
    "<Return>",
    lambda event: password_entry.focus()
)


password_entry.bind(
    "<Return>",
    lambda event: student_login()
)


# ============================================================
# STUDENT DASHBOARD
# Initially hidden
# ============================================================
dashboard_frame = Frame(
    window,
    bg=BG
)


# ============================================================
# DASHBOARD HEADER
# ============================================================
dashboard_header = Frame(
    dashboard_frame,
    bg=NAVY,
    height=70
)

dashboard_header.pack(
    fill=X
)

dashboard_header.pack_propagate(
    False
)


# ============================================================
# DASHBOARD BRAND
# ============================================================
dashboard_brand = Frame(
    dashboard_header,
    bg=NAVY
)

dashboard_brand.pack(
    side=LEFT,
    padx=30
)


Label(
    dashboard_brand,
    text="OCAC",
    bg=NAVY,
    fg="white",
    font=(
        "Segoe UI",
        23,
        "bold"
    )
).pack(
    side=LEFT,
    pady=14
)


Frame(
    dashboard_brand,
    bg="#52677F",
    width=1,
    height=28
).pack(
    side=LEFT,
    padx=17
)


Label(
    dashboard_brand,
    text="Student Dashboard",
    bg=NAVY,
    fg="#C8D6E5",
    font=(
        "Segoe UI",
        11
    )
).pack(
    side=LEFT
)


# ============================================================
# LOGOUT BUTTON
# ============================================================
logout_button = Button(
    dashboard_header,
    text="LOGOUT",
    command=logout,
    bg=RED,
    fg="white",
    activebackground=RED_HOVER,
    activeforeground="white",
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    bd=0,
    cursor="hand2",
    padx=22,
    pady=8
)

logout_button.pack(
    side=RIGHT,
    padx=30
)


add_hover(
    logout_button,
    RED,
    RED_HOVER
)


# ============================================================
# ACTIVE STUDENT STATUS
# ============================================================
Label(
    dashboard_header,
    text="● ACTIVE STUDENT",
    bg=NAVY_2,
    fg="#86EFAC",
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    padx=16,
    pady=8
).pack(
    side=RIGHT
)


# ============================================================
# DASHBOARD CONTENT
# ============================================================
dashboard_content = Frame(
    dashboard_frame,
    bg=BG
)

dashboard_content.pack(
    fill=BOTH,
    expand=True,
    padx=28,
    pady=18
)


# ============================================================
# WELCOME CARD
# ============================================================
welcome_card = Frame(
    dashboard_content,
    bg=NAVY_2,
    height=125
)

welcome_card.pack(
    fill=X
)

welcome_card.pack_propagate(
    False
)


# ============================================================
# WELCOME LEFT
# ============================================================
welcome_content = Frame(
    welcome_card,
    bg=NAVY_2
)

welcome_content.pack(
    side=LEFT,
    padx=30,
    pady=20
)


Label(
    welcome_content,
    text="STUDENT PORTAL",
    bg=NAVY_2,
    fg="#8FB5D9",
    font=(
        "Segoe UI",
        8,
        "bold"
    )
).pack(
    anchor=W
)


welcome_label = Label(
    welcome_content,
    text="Welcome, Student",
    bg=NAVY_2,
    fg="white",
    font=(
        "Segoe UI",
        25,
        "bold"
    )
)

welcome_label.pack(
    anchor=W,
    pady=(4, 2)
)


Label(
    welcome_content,
    text=(
        "Here is an overview of your "
        "OCAC training account."
    ),
    bg=NAVY_2,
    fg="#C8D9E8",
    font=(
        "Segoe UI",
        9
    )
).pack(
    anchor=W
)


# ============================================================
# CURRENT PROGRAM
# ============================================================
course_info = Frame(
    welcome_card,
    bg=NAVY_3
)

course_info.pack(
    side=RIGHT,
    padx=30,
    pady=20
)


Label(
    course_info,
    text="CURRENT PROGRAM",
    bg=NAVY_3,
    fg="#8FB5D9",
    font=(
        "Segoe UI",
        8,
        "bold"
    )
).pack(
    anchor=W,
    padx=20,
    pady=(10, 2)
)


Label(
    course_info,
    text="Python & MySQL Training",
    bg=NAVY_3,
    fg="white",
    font=(
        "Segoe UI",
        14,
        "bold"
    )
).pack(
    anchor=W,
    padx=20
)


Label(
    course_info,
    text="Summer Internship 2026",
    bg=NAVY_3,
    fg="#C8D9E8",
    font=(
        "Segoe UI",
        8
    )
).pack(
    anchor=W,
    padx=20,
    pady=(2, 10)
)


# ============================================================
# SUMMARY CARDS
# ============================================================
summary_frame = Frame(
    dashboard_content,
    bg=BG
)

summary_frame.pack(
    fill=X,
    pady=(15, 12)
)


# ============================================================
# CREATE SUMMARY CARD
# ============================================================
def create_summary_card(
    parent,
    title,
    value,
    subtitle,
    color
):

    card = Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.pack(
        side=LEFT,
        fill=X,
        expand=True,
        padx=(0, 10)
    )


    Frame(
        card,
        bg=color,
        height=4
    ).pack(
        fill=X
    )


    content = Frame(
        card,
        bg=CARD
    )

    content.pack(
        fill=BOTH,
        expand=True,
        padx=15,
        pady=10
    )


    Label(
        content,
        text=title,
        bg=CARD,
        fg=MUTED,
        font=(
            "Segoe UI",
            7,
            "bold"
        )
    ).pack(
        anchor=W
    )


    value_label = Label(
        content,
        text=value,
        bg=CARD,
        fg=TEXT,
        font=(
            "Segoe UI",
            16,
            "bold"
        )
    )

    value_label.pack(
        anchor=W,
        pady=(2, 1)
    )


    Label(
        content,
        text=subtitle,
        bg=CARD,
        fg=MUTED,
        font=(
            "Segoe UI",
            7
        )
    ).pack(
        anchor=W
    )


    return value_label


# ============================================================
# STUDENT NAME CARD
# ============================================================
student_name_value = create_summary_card(
    summary_frame,
    "STUDENT NAME",
    "-",
    "Registered student",
    BLUE
)


# ============================================================
# ROLL NUMBER CARD
# ============================================================
roll_value = create_summary_card(
    summary_frame,
    "ROLL NUMBER",
    "-",
    "Student identification",
    GREEN
)


# ============================================================
# ATTENDANCE CARD
# ============================================================
attendance_value = create_summary_card(
    summary_frame,
    "ATTENDANCE",
    "92%",
    "Excellent attendance",
    PURPLE
)


# ============================================================
# PAYMENT STATUS CARD
# ============================================================
payment_status_value = create_summary_card(
    summary_frame,
    "PAYMENT STATUS",
    "PAID",
    "No pending payment",
    GREEN
)


# ============================================================
# MAIN INFORMATION AREA
# ============================================================
info_area = Frame(
    dashboard_content,
    bg=BG
)

info_area.pack(
    fill=BOTH,
    expand=True
)


# ============================================================
# LEFT COLUMN
# ============================================================
left_column = Frame(
    info_area,
    bg=BG
)

left_column.pack(
    side=LEFT,
    fill=BOTH,
    expand=True,
    padx=(0, 7)
)


# ============================================================
# RIGHT COLUMN
# ============================================================
right_column = Frame(
    info_area,
    bg=BG,
    width=390
)

right_column.pack(
    side=RIGHT,
    fill=Y,
    padx=(7, 0)
)

right_column.pack_propagate(
    False
)


# ============================================================
# DETAIL ROW FUNCTION
# ============================================================
def create_detail_row(
    parent,
    title,
    value,
    value_color=TEXT
):

    row = Frame(
        parent,
        bg=CARD
    )

    row.pack(
        fill=X,
        pady=4
    )


    Label(
        row,
        text=title,
        bg=CARD,
        fg=MUTED,
        font=(
            "Segoe UI",
            8
        )
    ).pack(
        side=LEFT
    )


    value_label = Label(
        row,
        text=value,
        bg=CARD,
        fg=value_color,
        font=(
            "Segoe UI",
            8,
            "bold"
        )
    )

    value_label.pack(
        side=RIGHT
    )


    return value_label


# ============================================================
# PAYMENT DETAILS CARD
# ============================================================
payment_card = Frame(
    left_column,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

payment_card.pack(
    fill=X,
    pady=(0, 12)
)


# Payment Header
payment_header = Frame(
    payment_card,
    bg=CARD
)

payment_header.pack(
    fill=X,
    padx=20,
    pady=(15, 10)
)


Label(
    payment_header,
    text="Payment Details",
    bg=CARD,
    fg=TEXT,
    font=(
        "Segoe UI",
        15,
        "bold"
    )
).pack(
    side=LEFT
)


Label(
    payment_header,
    text="PAID",
    bg=LIGHT_GREEN,
    fg=GREEN_HOVER,
    font=(
        "Segoe UI",
        8,
        "bold"
    ),
    padx=12,
    pady=4
).pack(
    side=RIGHT
)


# Separator
Frame(
    payment_card,
    bg=BORDER,
    height=1
).pack(
    fill=X
)


payment_details = Frame(
    payment_card,
    bg=CARD
)

payment_details.pack(
    fill=X,
    padx=20,
    pady=12
)


create_detail_row(
    payment_details,
    "Total Course Fee",
    "₹5,000"
)


create_detail_row(
    payment_details,
    "Amount Paid",
    "₹5,000",
    GREEN
)


create_detail_row(
    payment_details,
    "Pending Amount",
    "₹0",
    GREEN
)


transaction_value = create_detail_row(
    payment_details,
    "Transaction ID",
    "OCAC2026DEMO"
)


create_detail_row(
    payment_details,
    "Payment Date",
    "10 July 2026"
)


create_detail_row(
    payment_details,
    "Payment Method",
    "UPI"
)


# ============================================================
# TRAINING PROGRESS CARD
# ============================================================
progress_card = Frame(
    left_column,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

progress_card.pack(
    fill=BOTH,
    expand=True
)


Label(
    progress_card,
    text="Training Progress",
    bg=CARD,
    fg=TEXT,
    font=(
        "Segoe UI",
        15,
        "bold"
    )
).pack(
    anchor=W,
    padx=20,
    pady=(15, 3)
)


Label(
    progress_card,
    text=(
        "Your current internship "
        "learning progress"
    ),
    bg=CARD,
    fg=MUTED,
    font=(
        "Segoe UI",
        8
    )
).pack(
    anchor=W,
    padx=20,
    pady=(0, 10)
)


progress_content = Frame(
    progress_card,
    bg=CARD
)

progress_content.pack(
    fill=X,
    padx=20,
    pady=(0, 15)
)


# ============================================================
# CREATE PROGRESS ITEM
# ============================================================
def create_progress_item(
    parent,
    module,
    status,
    status_bg,
    status_fg
):

    row = Frame(
        parent,
        bg="#F8FAFC"
    )

    row.pack(
        fill=X,
        pady=3
    )


    Label(
        row,
        text=module,
        bg="#F8FAFC",
        fg=TEXT,
        font=(
            "Segoe UI",
            8,
            "bold"
        )
    ).pack(
        side=LEFT,
        padx=10,
        pady=7
    )


    Label(
        row,
        text=status,
        bg=status_bg,
        fg=status_fg,
        font=(
            "Segoe UI",
            7,
            "bold"
        ),
        padx=9,
        pady=3
    ).pack(
        side=RIGHT,
        padx=8
    )


# Progress items
create_progress_item(
    progress_content,
    "Python Programming Basics",
    "COMPLETED",
    LIGHT_GREEN,
    GREEN_HOVER
)


create_progress_item(
    progress_content,
    "Python Data Structures",
    "COMPLETED",
    LIGHT_GREEN,
    GREEN_HOVER
)


create_progress_item(
    progress_content,
    "MySQL Database",
    "IN PROGRESS",
    "#DBEAFE",
    BLUE_HOVER
)


create_progress_item(
    progress_content,
    "Final Internship Project",
    "PENDING",
    LIGHT_AMBER,
    "#B45309"
)


# ============================================================
# PROFILE INFORMATION CARD
# ============================================================
profile_card = Frame(
    right_column,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

profile_card.pack(
    fill=X,
    pady=(0, 10)
)


Label(
    profile_card,
    text="My Profile",
    bg=CARD,
    fg=TEXT,
    font=(
        "Segoe UI",
        14,
        "bold"
    )
).pack(
    anchor=W,
    padx=18,
    pady=(14, 10)
)


profile_details = Frame(
    profile_card,
    bg=CARD
)

profile_details.pack(
    fill=X,
    padx=18,
    pady=(0, 14)
)


profile_name_value = create_detail_row(
    profile_details,
    "Student Name",
    "-"
)


profile_roll_value = create_detail_row(
    profile_details,
    "Roll Number",
    "-"
)


profile_username_value = create_detail_row(
    profile_details,
    "Username",
    "-"
)


# ============================================================
# COURSE INFORMATION CARD
# ============================================================
course_card = Frame(
    right_column,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

course_card.pack(
    fill=X,
    pady=(0, 10)
)


Label(
    course_card,
    text="Course Information",
    bg=CARD,
    fg=TEXT,
    font=(
        "Segoe UI",
        14,
        "bold"
    )
).pack(
    anchor=W,
    padx=18,
    pady=(14, 10)
)


course_details = Frame(
    course_card,
    bg=CARD
)

course_details.pack(
    fill=X,
    padx=18,
    pady=(0, 14)
)


create_detail_row(
    course_details,
    "Program",
    "Summer Internship"
)


create_detail_row(
    course_details,
    "Technology",
    "Python + MySQL"
)


create_detail_row(
    course_details,
    "Batch",
    "2026"
)


create_detail_row(
    course_details,
    "Duration",
    "4 Weeks"
)


create_detail_row(
    course_details,
    "Status",
    "ACTIVE",
    GREEN
)


# ============================================================
# RECENT ACTIVITY CARD
# ============================================================
activity_card = Frame(
    right_column,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

activity_card.pack(
    fill=X,
    pady=(0, 10)
)


Label(
    activity_card,
    text="Recent Activity",
    bg=CARD,
    fg=TEXT,
    font=(
        "Segoe UI",
        14,
        "bold"
    )
).pack(
    anchor=W,
    padx=18,
    pady=(14, 8)
)


activities = [
    "Logged into Student Portal",
    "Completed Python Assignment",
    "Attendance record updated",
    "Course payment verified"
]


for activity in activities:

    activity_row = Frame(
        activity_card,
        bg=CARD
    )

    activity_row.pack(
        fill=X,
        padx=18,
        pady=3
    )


    Label(
        activity_row,
        text="●",
        bg=CARD,
        fg=BLUE,
        font=(
            "Segoe UI",
            7
        )
    ).pack(
        side=LEFT,
        padx=(0, 7)
    )


    Label(
        activity_row,
        text=activity,
        bg=CARD,
        fg=TEXT,
        font=(
            "Segoe UI",
            8
        )
    ).pack(
        side=LEFT
    )


Frame(
    activity_card,
    bg=CARD,
    height=10
).pack()


# ============================================================
# ANNOUNCEMENT CARD
# ============================================================
announcement_card = Frame(
    right_column,
    bg=LIGHT_BLUE,
    highlightbackground="#BFDBFE",
    highlightthickness=1
)

announcement_card.pack(
    fill=BOTH,
    expand=True
)


Label(
    announcement_card,
    text="Announcements",
    bg=LIGHT_BLUE,
    fg="#1E3A8A",
    font=(
        "Segoe UI",
        14,
        "bold"
    )
).pack(
    anchor=W,
    padx=18,
    pady=(14, 8)
)


Label(
    announcement_card,
    text=(
        "• Submit your final internship project "
        "before the deadline.\n\n"
        "• Maintain a minimum of 75% attendance.\n\n"
        "• Contact your mentor for "
        "project-related queries."
    ),
    bg=LIGHT_BLUE,
    fg="#334155",
    justify=LEFT,
    wraplength=340,
    font=(
        "Segoe UI",
        8
    )
).pack(
    anchor=W,
    padx=18,
    pady=(0, 14)
)


# ============================================================
# WINDOW CLOSE EVENT
# ============================================================
window.protocol(
    "WM_DELETE_WINDOW",
    close_app
)


# ============================================================
# INITIAL FOCUS
# ============================================================
username_entry.focus()


# ============================================================
# START APPLICATION
# ============================================================
window.mainloop()