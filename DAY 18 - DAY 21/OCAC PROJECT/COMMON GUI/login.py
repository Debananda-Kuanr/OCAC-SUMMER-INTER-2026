from tkinter import *
from tkinter import messagebox
import mysql.connector
import subprocess
import sys
import os


# ============================================================
# FILE:
# COMMON GUI/login.py
# ============================================================


# ============================================================
# FILE PATHS
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(
    CURRENT_DIR
)


# ============================================================
# DASHBOARD PATHS
# ============================================================

ADMIN_DASHBOARD_FILE = os.path.join(
    PROJECT_DIR,
    "ADMIN",
    "admin_dashboard.py"
)

ACCOUNTANT_DASHBOARD_FILE = os.path.join(
    PROJECT_DIR,
    "ACCOUNTANT",
    "accountant_dashboard.py"
)


STUDENT_DASHBOARD_FILE = os.path.join(
    PROJECT_DIR,
    "STUDENT",
    "student_dashboard.py"
)

FORGOT_PASSWORD_FILE = os.path.join(
    CURRENT_DIR,
    "forgot.py"
)

REGISTER_FILE = os.path.join(
    CURRENT_DIR,
    "register.py"
)

LOGIN_IMAGE_FILE = os.path.join(
    PROJECT_DIR,
    "IMAGES",
    "login.png"
)


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"

DARK_BLUE = "#1E40AF"

LIGHT_BLUE = "#EFF6FF"

TEXT_COLOR = "#1F2937"

GRAY = "#6B7280"

BORDER_COLOR = "#CBD5E1"

WHITE = "#FFFFFF"


# ============================================================
# MAIN WINDOW
# ============================================================

window = Tk()

window.title(
    "Fee Status Management System"
)

window.geometry(
    "900x550+300+100"
)

window.resizable(
    False,
    False
)

window.configure(
    bg=WHITE
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

con = None

cursor = None


# ============================================================
# CONNECT DATABASE
# ============================================================

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
            ),
            parent=window
        )


        return False


# ============================================================
# INITIAL DATABASE CONNECTION
# ============================================================

if not connect_database():

    window.destroy()

    sys.exit()


# ============================================================
# ENSURE DATABASE CONNECTION
#
# If the MySQL connection closes for any reason,
# this function reconnects automatically.
# ============================================================

def ensure_database_connection():

    global con
    global cursor


    try:

        if (
            con is None
            or
            not con.is_connected()
        ):

            return connect_database()


        return True


    except mysql.connector.Error:

        return connect_database()


# ============================================================
# CLOSE DATABASE CONNECTION
# ============================================================

def close_database():

    global cursor
    global con


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


    cursor = None

    con = None


# ============================================================
# OPEN NORMAL PYTHON FILE
#
# Used for pages that do not need logged-in user information.
# ============================================================

def open_python_file(
    file_path,
    page_name
):

    # --------------------------------------------------------
    # CHECK FILE EXISTS
    # --------------------------------------------------------

    if not os.path.exists(
        file_path
    ):

        messagebox.showerror(
            "File Not Found",
            (
                f"{page_name} file was not found."
                f"\n\n{file_path}"
            ),
            parent=window
        )


        return False


    # --------------------------------------------------------
    # OPEN FILE
    # --------------------------------------------------------

    try:

        subprocess.Popen(
            [
                sys.executable,
                file_path
            ],
            cwd=PROJECT_DIR
        )


        return True


    except Exception as error:

        messagebox.showerror(
            "Open Error",
            (
                f"Unable to open {page_name}."
                f"\n\n{error}"
            ),
            parent=window
        )


        return False


# ============================================================
# OPEN ACCOUNTANT DASHBOARD
#
# IMPORTANT:
#
# This function passes:
#
# sys.argv[1] = Registration_No
# sys.argv[2] = Name
# sys.argv[3] = Username
#
# to accountant_dashboard.py
# ============================================================

def open_accountant_dashboard(
    registration_no,
    user_name,
    login_username
):

    # --------------------------------------------------------
    # CHECK FILE EXISTS
    # --------------------------------------------------------

    if not os.path.exists(
        ACCOUNTANT_DASHBOARD_FILE
    ):

        messagebox.showerror(
            "File Not Found",
            (
                "Accountant Dashboard file "
                "was not found."
                f"\n\n{ACCOUNTANT_DASHBOARD_FILE}"
            ),
            parent=window
        )


        return False


    # --------------------------------------------------------
    # OPEN ACCOUNTANT DASHBOARD
    # --------------------------------------------------------

    try:

        subprocess.Popen(
            [
                sys.executable,

                ACCOUNTANT_DASHBOARD_FILE,

                str(
                    registration_no
                ),

                str(
                    user_name
                ),

                str(
                    login_username
                )
            ],
            cwd=PROJECT_DIR
        )


        return True


    except Exception as error:

        messagebox.showerror(
            "Open Error",
            (
                "Unable to open "
                "Accountant Dashboard."
                f"\n\n{error}"
            ),
            parent=window
        )


        return False


# ============================================================
# OPEN STUDENT DASHBOARD
# ============================================================

def open_student_dashboard(
    registration_no,
    user_name,
    login_username
):

    if not os.path.exists(STUDENT_DASHBOARD_FILE):

        messagebox.showerror(
            "File Not Found",
            (
                "Student Dashboard file was not found."
                f"\n\n{STUDENT_DASHBOARD_FILE}"
            ),
            parent=window
        )

        return False

    try:

        subprocess.Popen(
            [
                sys.executable,
                STUDENT_DASHBOARD_FILE,
                str(registration_no),
                str(user_name),
                str(login_username)
            ],
            cwd=PROJECT_DIR
        )

        return True

    except Exception as error:

        messagebox.showerror(
            "Open Error",
            (
                "Unable to open Student Dashboard."
                f"\n\n{error}"
            ),
            parent=window
        )

        return False


# ============================================================
# LOGIN FUNCTION
# ============================================================

def login():

    # --------------------------------------------------------
    # GET USERNAME AND PASSWORD
    # --------------------------------------------------------

    u = username.get().strip()

    p = password.get()


    # --------------------------------------------------------
    # CHECK EMPTY USERNAME
    # --------------------------------------------------------

    if u == "":

        messagebox.showwarning(
            "Username Required",
            "Please enter your Username.",
            parent=window
        )


        username.focus_set()


        return


    # --------------------------------------------------------
    # CHECK EMPTY PASSWORD
    # --------------------------------------------------------

    if p == "":

        messagebox.showwarning(
            "Password Required",
            "Please enter your Password.",
            parent=window
        )


        password.focus_set()


        return


    # --------------------------------------------------------
    # CHECK DATABASE CONNECTION
    # --------------------------------------------------------

    if not ensure_database_connection():

        messagebox.showerror(
            "Database Error",
            (
                "Unable to connect to database."
                "\n\nPlease try again."
            ),
            parent=window
        )


        return


    try:

        # ====================================================
        # SEARCH USER
        #
        # IMPORTANT:
        #
        # We now fetch:
        #
        # 1. Registration_No
        # 2. Name
        # 3. Username
        # 4. Role
        #
        # ====================================================

        sql = """
        SELECT

            Registration_No,

            Name,

            Username,

            Role

        FROM registration

        WHERE

            BINARY Username = BINARY %s

            AND

            BINARY Password = BINARY %s

        LIMIT 1
        """


        values = (
            u,
            p
        )


        cursor.execute(
            sql,
            values
        )


        result = cursor.fetchone()


        # ====================================================
        # INVALID LOGIN
        # ====================================================

        if result is None:

            messagebox.showerror(
                "Login Failed",
                (
                    "Invalid Username "
                    "or Password."
                ),
                parent=window
            )


            password.delete(
                0,
                END
            )


            password.focus_set()


            return


        # ====================================================
        # GET LOGGED-IN USER DETAILS
        # ====================================================

        registration_no = str(
            result[0]
        ).strip()


        user_name = str(
            result[1]
        ).strip()


        login_username = str(
            result[2]
        ).strip()


        user_role = str(
            result[3]
        ).strip()


        role_lower = (
            user_role.lower()
        )


        # ====================================================
        # ADMIN LOGIN
        # ====================================================

        if role_lower == "admin":

            opened = open_python_file(
                ADMIN_DASHBOARD_FILE,
                "Admin Dashboard"
            )


            if opened:

                close_database()


                window.destroy()


        # ====================================================
        # ACCOUNTANT LOGIN
        #
        # Pass actual logged-in user details.
        # ====================================================

        elif role_lower == "accountant":

            opened = open_accountant_dashboard(
                registration_no,
                user_name,
                login_username
            )


            if opened:

                close_database()


                window.destroy()


        # ====================================================
        # STUDENT LOGIN
        # ====================================================

        elif role_lower == "student":

            opened = open_student_dashboard(
                registration_no,
                user_name,
                login_username
            )

            if opened:

                close_database()

                window.destroy()
        # ====================================================
        # UNKNOWN ROLE
        # ====================================================

        else:

            messagebox.showerror(
                "Role Error",
                (
                    "Unknown User Role: "
                    f"{user_role}"
                ),
                parent=window
            )


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            (
                "An error occurred while "
                "checking login details."
                f"\n\n{error}"
            ),
            parent=window
        )


    except Exception as error:

        messagebox.showerror(
            "Login Error",
            (
                "An unexpected error occurred."
                f"\n\n{error}"
            ),
            parent=window
        )


# ============================================================
# SHOW / HIDE PASSWORD
# ============================================================

password_visible = False


# ============================================================
# DRAW EYE ICON
# ============================================================

def draw_eye_icon(
    visible
):

    eye_canvas.delete(
        "all"
    )


    # --------------------------------------------------------
    # OUTER EYE
    # --------------------------------------------------------

    eye_canvas.create_oval(
        6,
        10,
        34,
        26,
        outline=GRAY,
        width=2
    )


    # --------------------------------------------------------
    # PASSWORD VISIBLE
    # --------------------------------------------------------

    if visible:

        eye_canvas.create_oval(
            14,
            14,
            26,
            22,
            outline=GRAY,
            fill=GRAY
        )


    # --------------------------------------------------------
    # PASSWORD HIDDEN
    # --------------------------------------------------------

    else:

        eye_canvas.create_line(
            8,
            12,
            32,
            24,
            fill=GRAY,
            width=3,
            capstyle="round"
        )


# ============================================================
# TOGGLE PASSWORD
# ============================================================

def toggle_password():

    global password_visible


    # --------------------------------------------------------
    # HIDE PASSWORD
    # --------------------------------------------------------

    if password_visible:

        password.config(
            show="*"
        )


        draw_eye_icon(
            False
        )


        password_visible = False


    # --------------------------------------------------------
    # SHOW PASSWORD
    # --------------------------------------------------------

    else:

        password.config(
            show=""
        )


        draw_eye_icon(
            True
        )


        password_visible = True


# ============================================================
# FORGOT PASSWORD
# ============================================================

def forgot_password():

    # --------------------------------------------------------
    # CHECK FILE EXISTS
    # --------------------------------------------------------

    if not os.path.exists(
        FORGOT_PASSWORD_FILE
    ):

        messagebox.showerror(
            "File Not Found",
            (
                "Forgot Password file "
                "was not found."
                f"\n\n{FORGOT_PASSWORD_FILE}"
            ),
            parent=window
        )


        return


    # --------------------------------------------------------
    # OPEN FORGOT PASSWORD
    # --------------------------------------------------------

    try:

        subprocess.Popen(
            [
                sys.executable,
                FORGOT_PASSWORD_FILE
            ],
            cwd=PROJECT_DIR
        )


        close_database()


        window.destroy()


    except Exception as error:

        messagebox.showerror(
            "Open Error",
            (
                "Unable to open "
                "Forgot Password."
                f"\n\n{error}"
            ),
            parent=window
        )


# ============================================================
# OPEN REGISTER PAGE
# ============================================================

def open_register():

    # --------------------------------------------------------
    # CHECK FILE EXISTS
    # --------------------------------------------------------

    if not os.path.exists(
        REGISTER_FILE
    ):

        messagebox.showerror(
            "File Not Found",
            (
                "Register file was not found."
                f"\n\n{REGISTER_FILE}"
            ),
            parent=window
        )


        return


    # --------------------------------------------------------
    # OPEN REGISTER PAGE
    # --------------------------------------------------------

    try:

        subprocess.Popen(
            [
                sys.executable,
                REGISTER_FILE
            ],
            cwd=PROJECT_DIR
        )


        close_database()


        window.destroy()


    except Exception as error:

        messagebox.showerror(
            "Open Error",
            (
                "Unable to open Register page."
                f"\n\n{error}"
            ),
            parent=window
        )


# ============================================================
# CLOSE WINDOW
# ============================================================

def close_window():

    close_database()


    window.destroy()


window.protocol(
    "WM_DELETE_WINDOW",
    close_window
)


# ============================================================
# LEFT SIDE PANEL
# ============================================================

left_panel = Frame(
    window,
    bg=LIGHT_BLUE,
    width=400,
    height=550
)

left_panel.place(
    x=0,
    y=0
)


# ============================================================
# LOGIN IMAGE
# ============================================================

login_image = None


try:

    if os.path.exists(
        LOGIN_IMAGE_FILE
    ):

        login_image = PhotoImage(
            file=LOGIN_IMAGE_FILE
        )


        login_image = login_image.subsample(
            2,
            2
        )


        image_label = Label(
            left_panel,
            image=login_image,
            bg=LIGHT_BLUE
        )


        image_label.place(
            x=0,
            y=120,
            width=500,
            height=470
        )


except TclError:

    login_image = None


# ============================================================
# PROJECT TITLE
# ============================================================

project_title = Label(
    left_panel,
    text=(
        "FEE STATUS\n"
        "MANAGEMENT SYSTEM"
    ),
    bg=LIGHT_BLUE,
    fg=DARK_BLUE,
    font=(
        "Helvetica",
        18,
        "bold"
    ),
    justify="center"
)

project_title.place(
    x=65,
    y=55
)


# ============================================================
# PROJECT DESCRIPTION
# ============================================================

project_description = Label(
    left_panel,
    text=(
        "Manage student fees efficiently"
    ),
    bg=LIGHT_BLUE,
    fg=GRAY,
    font=(
        "Helvetica",
        12
    )
)

project_description.place(
    x=85,
    y=485
)


# ============================================================
# RIGHT SIDE PANEL
# ============================================================

right_panel = Frame(
    window,
    bg=WHITE,
    width=500,
    height=550
)

right_panel.place(
    x=400,
    y=0
)


# ============================================================
# LOGIN FORM FRAME
# ============================================================

form_frame = Frame(
    right_panel,
    bg=WHITE,
    width=340,
    height=450
)

form_frame.place(
    x=80,
    y=50
)


# ============================================================
# LOGIN TITLE
# ============================================================

login_title = Label(
    form_frame,
    text="Welcome Back",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        28,
        "bold"
    )
)

login_title.place(
    x=0,
    y=20
)


# ============================================================
# LOGIN SUBTITLE
# ============================================================

login_subtitle = Label(
    form_frame,
    text="Login to your account",
    bg=WHITE,
    fg=GRAY,
    font=(
        "Helvetica",
        12
    )
)

login_subtitle.place(
    x=0,
    y=65
)


# ============================================================
# USERNAME LABEL
# ============================================================

username_label = Label(
    form_frame,
    text="Username",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        11,
        "bold"
    )
)

username_label.place(
    x=0,
    y=125
)


# ============================================================
# USERNAME ENTRY
# ============================================================

username = Entry(
    form_frame,
    font=(
        "Helvetica",
        12
    ),
    fg=TEXT_COLOR,
    bg=WHITE,
    bd=1,
    relief="solid"
)

username.place(
    x=0,
    y=155,
    width=340,
    height=42
)

username.focus_set()


# ============================================================
# PASSWORD LABEL
# ============================================================

password_label = Label(
    form_frame,
    text="Password",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        11,
        "bold"
    )
)

password_label.place(
    x=0,
    y=225
)


# ============================================================
# PASSWORD CONTAINER
# ============================================================

password_frame = Frame(
    form_frame,
    bg=WHITE,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

password_frame.place(
    x=0,
    y=255,
    width=340,
    height=42
)


# ============================================================
# PASSWORD ENTRY
# ============================================================

password = Entry(
    password_frame,
    font=(
        "Helvetica",
        12
    ),
    fg=TEXT_COLOR,
    bg=WHITE,
    bd=0,
    show="*"
)

password.place(
    x=10,
    y=1,
    width=280,
    height=38
)


# ============================================================
# EYE CANVAS
# ============================================================

eye_canvas = Canvas(
    password_frame,
    bg=WHITE,
    highlightthickness=0,
    cursor="hand2",
    width=40,
    height=36
)

eye_canvas.place(
    x=295,
    y=2,
    width=40,
    height=36
)


# ============================================================
# DRAW CLOSED EYE INITIALLY
# ============================================================

draw_eye_icon(
    False
)


# ============================================================
# CLICK EYE TO SHOW / HIDE PASSWORD
# ============================================================

eye_canvas.bind(
    "<Button-1>",
    lambda event:
    toggle_password()
)


# ============================================================
# FORGOT PASSWORD BUTTON
# ============================================================

forgot_button = Button(
    form_frame,
    text="Forgot Password?",
    bg=WHITE,
    fg=BLUE,
    activebackground=WHITE,
    activeforeground=DARK_BLUE,
    font=(
        "Helvetica",
        10
    ),
    bd=0,
    cursor="hand2",
    command=forgot_password
)

forgot_button.place(
    x=220,
    y=310
)


# ============================================================
# LOGIN BUTTON
# ============================================================

login_button = Button(
    form_frame,
    text="LOGIN",
    bg=BLUE,
    fg=WHITE,
    activebackground=DARK_BLUE,
    activeforeground=WHITE,
    font=(
        "Helvetica",
        12,
        "bold"
    ),
    bd=0,
    cursor="hand2",
    command=login
)

login_button.place(
    x=0,
    y=355,
    width=340,
    height=45
)


# ============================================================
# REGISTER SECTION
# ============================================================

new_user_label = Label(
    form_frame,
    text="Don't Have an Account?",
    bg=WHITE,
    fg=GRAY,
    font=(
        "Helvetica",
        10
    )
)

new_user_label.place(
    x=70,
    y=420
)


register_button = Button(
    form_frame,
    text="Register",
    bg=WHITE,
    fg=BLUE,
    activebackground=WHITE,
    activeforeground=DARK_BLUE,
    font=(
        "Helvetica",
        10,
        "bold"
    ),
    bd=0,
    cursor="hand2",
    command=open_register
)

register_button.place(
    x=218,
    y=418
)


# ============================================================
# PRESS ENTER TO LOGIN
# ============================================================

window.bind(
    "<Return>",
    lambda event:
    login()
)


# ============================================================
# MAIN LOOP
# ============================================================

window.mainloop()
