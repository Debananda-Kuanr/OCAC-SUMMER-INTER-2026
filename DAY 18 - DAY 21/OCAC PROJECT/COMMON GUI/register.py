from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
import subprocess
import sys
import os


# ============================================================
# FILE PATH
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(
    CURRENT_DIR
)


# ============================================================
# MAIN WINDOW
# ============================================================

window = Tk()

window.title(
    "Register - Fee Status Management System"
)

window.geometry(
    "1000x620+250+70"
)

window.resizable(
    False,
    False
)

window.configure(
    bg="white"
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
READONLY_BG = "#F8FAFC"


# ============================================================
# SECURITY QUESTIONS
# ============================================================

SECURITY_QUESTIONS = [

    "What is your favorite color?",

    "What is the name of your first school?",

    "What is your favorite food?",

    "What is the name of your childhood best friend?",

    "What is your favorite book?",

    "What is your favorite movie?",

    "What is the name of your hometown?",

    "What is your favorite sport?",

    "What is your dream travel destination?",

    "What was the name of your first teacher?"

]


DEFAULT_SECURITY_QUESTION = (
    "Select a security question"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

try:

    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="9439",
        database="OCAC_GROUP2"
    )

    cursor = con.cursor()


except mysql.connector.Error as error:

    messagebox.showerror(
        "Database Error",
        (
            "Unable to connect to database."
            "\n\n"
            f"{error}"
        )
    )

    window.destroy()

    sys.exit()


# ============================================================
# GENERATE STUDENT ID
# ============================================================

def generate_student_id():

    try:

        # ----------------------------------------------------
        # GET THE HIGHEST EXISTING STUDENT ID
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT Registration_No

            FROM registration

            WHERE
                Role = 'Student'

                AND Registration_No
                REGEXP '^STU[0-9]+$'

            ORDER BY
                CAST(
                    SUBSTRING(
                        Registration_No,
                        4
                    )
                    AS UNSIGNED
                ) DESC

            LIMIT 1
            """
        )


        result = cursor.fetchone()


        # ----------------------------------------------------
        # FIRST STUDENT
        # ----------------------------------------------------

        if result is None:

            return "STU00001"


        # ----------------------------------------------------
        # GET LAST STUDENT ID
        # ----------------------------------------------------

        last_student_id = result[0]


        # Example:
        #
        # STU00025
        #
        # becomes:
        #
        # 00025

        last_number = int(
            last_student_id[3:]
        )


        # ----------------------------------------------------
        # CREATE NEXT NUMBER
        # ----------------------------------------------------

        next_number = (
            last_number + 1
        )


        # ----------------------------------------------------
        # RETURN NEW ID
        # ----------------------------------------------------

        return (
            f"STU{next_number:05d}"
        )


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            (
                "Unable to generate "
                "Student ID."
                "\n\n"
                f"{error}"
            )
        )

        return ""


# ============================================================
# SET STUDENT ID
# ============================================================

def set_student_id():

    student_id = (
        generate_student_id()
    )


    registration_no.config(
        state=NORMAL
    )


    registration_no.delete(
        0,
        END
    )


    registration_no.insert(
        0,
        student_id
    )


    registration_no.config(
        state="readonly"
    )


# ============================================================
# REGISTER FUNCTION
# ============================================================

def register_new():

    # --------------------------------------------------------
    # GET FORM VALUES
    # --------------------------------------------------------

    r = (
        registration_no
        .get()
        .strip()
    )


    n = (
        name
        .get()
        .strip()
    )


    u = (
        username
        .get()
        .strip()
    )


    p = password.get()


    q = (
        security_question
        .get()
        .strip()
    )


    a = (
        security_answer
        .get()
        .strip()
    )


    # ========================================================
    # CHECK EMPTY FIELDS
    # ========================================================

    if (
        r == ""
        or n == ""
        or u == ""
        or p == ""
        or q == ""
        or q == DEFAULT_SECURITY_QUESTION
        or a == ""
    ):

        messagebox.showwarning(
            "Warning",
            (
                "All fields must be filled "
                "and a security question "
                "must be selected."
            )
        )

        return


    # ========================================================
    # INSERT STUDENT ACCOUNT
    # ========================================================

    try:

        sql = """
        INSERT INTO registration
        (
            Registration_No,
            Name,
            Username,
            Password,
            Security_Question,
            Security_Answer,
            Role
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
        """


        values = (
            r,
            n,
            u,
            p,
            q,
            a,
            "Student"
        )


        cursor.execute(
            sql,
            values
        )


        con.commit()


        # ====================================================
        # SUCCESS MESSAGE
        # ====================================================

        messagebox.showinfo(
            "Registration Successful",
            (
                "Your account has been "
                "registered successfully."
                "\n\n"
                f"Student ID: {r}"
                "\n\n"
                "Please remember your Student ID."
            )
        )


        # ====================================================
        # OPEN LOGIN PAGE
        # ====================================================

        open_login()


    # ========================================================
    # DUPLICATE VALUE
    # ========================================================

    except mysql.connector.IntegrityError as error:

        try:

            con.rollback()

        except:

            pass


        error_text = str(
            error
        )


        # ----------------------------------------------------
        # DUPLICATE STUDENT ID
        # ----------------------------------------------------

        if (
            "Registration_No"
            in error_text
            or r in error_text
        ):

            messagebox.showerror(
                "Registration Failed",
                (
                    "The generated Student ID "
                    "already exists."
                    "\n\n"
                    "A new Student ID will "
                    "be generated."
                )
            )


            set_student_id()


        # ----------------------------------------------------
        # DUPLICATE USERNAME
        # ----------------------------------------------------

        else:

            messagebox.showerror(
                "Registration Failed",
                (
                    "Username already exists."
                    "\n\n"
                    "Please choose another username."
                )
            )


    # ========================================================
    # DATABASE ERROR
    # ========================================================

    except mysql.connector.Error as error:

        try:

            con.rollback()

        except:

            pass


        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ============================================================
# PASSWORD VISIBILITY
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
    # EYE SHAPE
    # --------------------------------------------------------

    eye_canvas.create_oval(
        6,
        10,
        32,
        24,
        outline=GRAY,
        width=2
    )


    # --------------------------------------------------------
    # PASSWORD VISIBLE
    # --------------------------------------------------------

    if visible:

        eye_canvas.create_oval(
            15,
            14,
            23,
            22,
            fill=GRAY,
            outline=GRAY
        )


    # --------------------------------------------------------
    # PASSWORD HIDDEN
    # --------------------------------------------------------

    else:

        eye_canvas.create_line(
            7,
            9,
            32,
            25,
            fill=GRAY,
            width=2
        )


# ============================================================
# TOGGLE PASSWORD
# ============================================================

def toggle_password():

    global password_visible


    if password_visible:

        password.config(
            show="*"
        )


        draw_eye_icon(
            False
        )


        password_visible = False


    else:

        password.config(
            show=""
        )


        draw_eye_icon(
            True
        )


        password_visible = True


# ============================================================
# OPEN LOGIN PAGE
# ============================================================

def open_login():

    login_file = os.path.join(
        CURRENT_DIR,
        "login.py"
    )


    # --------------------------------------------------------
    # CLOSE DATABASE
    # --------------------------------------------------------

    try:

        cursor.close()


        if con.is_connected():

            con.close()


    except:

        pass


    # --------------------------------------------------------
    # CLOSE REGISTRATION PAGE
    # --------------------------------------------------------

    window.destroy()


    # --------------------------------------------------------
    # OPEN LOGIN PAGE
    # --------------------------------------------------------

    subprocess.Popen(
        [
            sys.executable,
            login_file
        ],
        cwd=PROJECT_DIR
    )


# ============================================================
# CLOSE WINDOW
# ============================================================

def close_window():

    try:

        cursor.close()


        if con.is_connected():

            con.close()


    except:

        pass


    window.destroy()


# ============================================================
# LEFT PANEL
# ============================================================

left_panel = Frame(
    window,
    bg=LIGHT_BLUE,
    width=420,
    height=620
)

left_panel.place(
    x=0,
    y=0
)


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
        20,
        "bold"
    ),
    justify="center"
)

project_title.place(
    x=65,
    y=45
)


# ============================================================
# REGISTER IMAGE
# ============================================================

register_image_path = os.path.join(
    PROJECT_DIR,
    "IMAGES",
    "registration.png"
)


try:

    register_image = PhotoImage(
        file=register_image_path
    )


    register_image = (
        register_image.subsample(
            2,
            2
        )
    )


    image_label = Label(
        left_panel,
        image=register_image,
        bg=LIGHT_BLUE
    )


    image_label.place(
        x=10,
        y=130,
        width=400,
        height=350
    )


except TclError:

    image_label = Label(
        left_panel,
        text=(
            "STUDENT\n"
            "REGISTRATION"
        ),
        bg=LIGHT_BLUE,
        fg=BLUE,
        font=(
            "Helvetica",
            24,
            "bold"
        ),
        justify=CENTER
    )


    image_label.place(
        x=10,
        y=130,
        width=400,
        height=350
    )


# ============================================================
# LEFT DESCRIPTION
# ============================================================

project_description = Label(
    left_panel,
    text=(
        "Create your account "
        "and get started"
    ),
    bg=LIGHT_BLUE,
    fg=GRAY,
    font=(
        "Helvetica",
        12
    )
)

project_description.place(
    x=75,
    y=520
)


# ============================================================
# RIGHT PANEL
# ============================================================

right_panel = Frame(
    window,
    bg=WHITE,
    width=580,
    height=620
)

right_panel.place(
    x=420,
    y=0
)


# ============================================================
# FORM FRAME
# ============================================================

form_frame = Frame(
    right_panel,
    bg=WHITE,
    width=460,
    height=570
)

form_frame.place(
    x=60,
    y=25
)


# ============================================================
# TITLE
# ============================================================

register_title = Label(
    form_frame,
    text="Create Student Account",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        26,
        "bold"
    )
)

register_title.place(
    x=0,
    y=0
)


# ============================================================
# SUBTITLE
# ============================================================

register_subtitle = Label(
    form_frame,
    text=(
        "Enter your details to "
        "create a student account"
    ),
    bg=WHITE,
    fg=GRAY,
    font=(
        "Helvetica",
        10
    )
)

register_subtitle.place(
    x=0,
    y=42
)


# ============================================================
# STUDENT ID LABEL
# ============================================================

registration_label = Label(
    form_frame,
    text="Student ID",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        10,
        "bold"
    )
)

registration_label.place(
    x=0,
    y=85
)


# ============================================================
# STUDENT ID
# AUTO GENERATED + READ ONLY
# ============================================================

registration_no = Entry(
    form_frame,
    font=(
        "Helvetica",
        11,
        "bold"
    ),
    fg=BLUE,
    bg=READONLY_BG,
    readonlybackground=READONLY_BG,
    bd=1,
    relief="solid",
    state="readonly"
)

registration_no.place(
    x=0,
    y=110,
    width=215,
    height=38
)


# ============================================================
# FULL NAME
# ============================================================

name_label = Label(
    form_frame,
    text="Full Name",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        10,
        "bold"
    )
)

name_label.place(
    x=245,
    y=85
)


name = Entry(
    form_frame,
    font=(
        "Helvetica",
        11
    ),
    fg=TEXT_COLOR,
    bg=WHITE,
    bd=1,
    relief="solid"
)

name.place(
    x=245,
    y=110,
    width=215,
    height=38
)


# ============================================================
# USERNAME
# ============================================================

username_label = Label(
    form_frame,
    text="Username",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        10,
        "bold"
    )
)

username_label.place(
    x=0,
    y=170
)


username = Entry(
    form_frame,
    font=(
        "Helvetica",
        11
    ),
    fg=TEXT_COLOR,
    bg=WHITE,
    bd=1,
    relief="solid"
)

username.place(
    x=0,
    y=195,
    width=215,
    height=38
)


# ============================================================
# PASSWORD
# ============================================================

password_label = Label(
    form_frame,
    text="Password",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        10,
        "bold"
    )
)

password_label.place(
    x=245,
    y=170
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
    x=245,
    y=195,
    width=215,
    height=38
)


# ============================================================
# PASSWORD ENTRY
# ============================================================

password = Entry(
    password_frame,
    font=(
        "Helvetica",
        11
    ),
    fg=TEXT_COLOR,
    bg=WHITE,
    bd=0,
    show="*"
)

password.place(
    x=10,
    y=2,
    width=160,
    height=32
)


# ============================================================
# EYE ICON
# ============================================================

eye_canvas = Canvas(
    password_frame,
    bg=WHITE,
    highlightthickness=0,
    cursor="hand2"
)

eye_canvas.place(
    x=174,
    y=1,
    width=38,
    height=34
)


draw_eye_icon(
    False
)


eye_canvas.bind(
    "<Button-1>",
    lambda event: toggle_password()
)


# ============================================================
# SECURITY QUESTION LABEL
# ============================================================

question_label = Label(
    form_frame,
    text="Security Question",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        10,
        "bold"
    )
)

question_label.place(
    x=0,
    y=255
)


# ============================================================
# COMBOBOX STYLE
# ============================================================

style = ttk.Style()


try:

    style.theme_use(
        "clam"
    )

except TclError:

    pass


style.configure(
    "Security.TCombobox",
    fieldbackground=WHITE,
    background=WHITE,
    foreground=TEXT_COLOR,
    bordercolor=BORDER_COLOR,
    lightcolor=BORDER_COLOR,
    darkcolor=BORDER_COLOR,
    arrowcolor=GRAY,
    padding=8
)


style.map(
    "Security.TCombobox",

    fieldbackground=[
        (
            "readonly",
            WHITE
        )
    ],

    foreground=[
        (
            "readonly",
            TEXT_COLOR
        )
    ],

    selectbackground=[
        (
            "readonly",
            WHITE
        )
    ],

    selectforeground=[
        (
            "readonly",
            TEXT_COLOR
        )
    ]
)


# ============================================================
# SECURITY QUESTION DROPDOWN
# ============================================================

security_question = ttk.Combobox(
    form_frame,
    values=SECURITY_QUESTIONS,
    state="readonly",
    style="Security.TCombobox",
    font=(
        "Helvetica",
        10
    )
)

security_question.place(
    x=0,
    y=280,
    width=460,
    height=38
)


# ============================================================
# DEFAULT SECURITY QUESTION TEXT
# ============================================================

security_question.set(
    DEFAULT_SECURITY_QUESTION
)


# ============================================================
# SECURITY ANSWER
# ============================================================

answer_label = Label(
    form_frame,
    text="Security Answer",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        10,
        "bold"
    )
)

answer_label.place(
    x=0,
    y=340
)


security_answer = Entry(
    form_frame,
    font=(
        "Helvetica",
        11
    ),
    fg=TEXT_COLOR,
    bg=WHITE,
    bd=1,
    relief="solid"
)

security_answer.place(
    x=0,
    y=365,
    width=460,
    height=38
)


# ============================================================
# REGISTER BUTTON
# ============================================================

register_button = Button(
    form_frame,
    text="REGISTER ACCOUNT",
    bg=BLUE,
    fg=WHITE,
    activebackground=DARK_BLUE,
    activeforeground=WHITE,
    font=(
        "Helvetica",
        11,
        "bold"
    ),
    bd=0,
    cursor="hand2",
    command=register_new
)

register_button.place(
    x=0,
    y=435,
    width=460,
    height=45
)


# ============================================================
# LOGIN SECTION
# ============================================================

login_text = Label(
    form_frame,
    text="Already have an account?",
    bg=WHITE,
    fg=GRAY,
    font=(
        "Helvetica",
        10
    )
)

login_text.place(
    x=120,
    y=510
)


login_button = Button(
    form_frame,
    text="Login",
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
    command=open_login
)

login_button.place(
    x=280,
    y=508
)


# ============================================================
# GENERATE STUDENT ID WHEN PAGE OPENS
# ============================================================

set_student_id()


# ============================================================
# FOCUS ON NAME FIELD
# ============================================================

name.focus_set()


# ============================================================
# PRESS ENTER TO REGISTER
# ============================================================

window.bind(
    "<Return>",
    lambda event: register_new()
)


# ============================================================
# WINDOW CLOSE
# ============================================================

window.protocol(
    "WM_DELETE_WINDOW",
    close_window
)


# ============================================================
# MAIN LOOP
# ============================================================

window.mainloop()