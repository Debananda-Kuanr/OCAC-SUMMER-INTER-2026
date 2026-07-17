from tkinter import *
from tkinter import messagebox
import mysql.connector
import subprocess
import sys
import os


# ============================================================
# PROJECT PATHS
# ============================================================

# Current Folder:
# OCAC PROJECT/COMMON_GUI

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# Main Project Folder:
# OCAC PROJECT

PROJECT_DIR = os.path.dirname(
    CURRENT_DIR
)

# Images Folder:
# OCAC PROJECT/IMAGES

IMAGES_DIR = os.path.join(
    PROJECT_DIR,
    "IMAGES"
)


# ============================================================
# MAIN WINDOW
# ============================================================

window = Tk()

window.title(
    "Forgot Password - Fee Status Management System"
)

window.geometry(
    "900x550+300+100"
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
GREEN = "#16A34A"


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
        f"Unable to connect to database.\n\n{error}"
    )

    window.destroy()


# ============================================================
# STORE USER DATA
# ============================================================

user_data = {

    "name": "",

    "username": "",

    "password": "",

    "question": "",

    "answer": ""

}


# ============================================================
# OPEN LOGIN PAGE
# ============================================================

def open_login():

    login_file = os.path.join(
        CURRENT_DIR,
        "login.py"
    )

    window.destroy()

    subprocess.Popen(
        [
            sys.executable,
            login_file
        ],
        cwd=PROJECT_DIR
    )


# ============================================================
# VERIFY USERNAME
# ============================================================

def verify_username():

    u = username.get().strip()


    # --------------------------------------------------------
    # CHECK EMPTY USERNAME
    # --------------------------------------------------------

    if u == "":

        messagebox.showwarning(
            "Warning",
            "Please enter your Username"
        )

        return


    try:

        # ----------------------------------------------------
        # SEARCH USER IN DATABASE
        # ----------------------------------------------------

        sql = """
        SELECT
            Name,
            Username,
            Password,
            Security_Question,
            Security_Answer

        FROM registration

        WHERE BINARY Username = BINARY %s
        """


        cursor.execute(
            sql,
            (u,)
        )


        result = cursor.fetchone()


        # ----------------------------------------------------
        # USER NOT FOUND
        # ----------------------------------------------------

        if result is None:

            messagebox.showerror(
                "Account Not Found",
                "No account found with this Username"
            )

            username.delete(
                0,
                END
            )

            username.focus_set()

            return


        # ----------------------------------------------------
        # SAVE USER INFORMATION
        # ----------------------------------------------------

        user_data["name"] = result[0]

        user_data["username"] = result[1]

        user_data["password"] = result[2]

        user_data["question"] = result[3]

        user_data["answer"] = result[4]


        # ----------------------------------------------------
        # DISPLAY SECURITY QUESTION
        # ----------------------------------------------------

        question_display.config(
            text=user_data["question"]
        )


        # ----------------------------------------------------
        # HIDE USERNAME SECTION
        # ----------------------------------------------------

        username_section.place_forget()


        # ----------------------------------------------------
        # SHOW SECURITY SECTION
        # ----------------------------------------------------

        security_section.place(
            x=80,
            y=65
        )


        security_answer.focus_set()


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ============================================================
# VERIFY SECURITY ANSWER
# ============================================================

def verify_answer():

    entered_answer = security_answer.get().strip()


    # --------------------------------------------------------
    # CHECK EMPTY ANSWER
    # --------------------------------------------------------

    if entered_answer == "":

        messagebox.showwarning(
            "Warning",
            "Please enter your Security Answer"
        )

        return


    # --------------------------------------------------------
    # CHECK SECURITY ANSWER
    # --------------------------------------------------------

    if entered_answer == user_data["answer"].strip():

        # Hide Security Section

        security_section.place_forget()


        # Update Welcome Message

        welcome_label.config(
            text=f"Welcome Back,\n{user_data['name']}!"
        )


        # Display Username

        recovered_username.config(
            text=user_data["username"]
        )


        # Display Password

        recovered_password.config(
            text=user_data["password"]
        )


        # Show Result Section

        result_section.place(
            x=80,
            y=55
        )


    else:

        messagebox.showerror(
            "Incorrect Answer",
            "The Security Answer is incorrect"
        )

        security_answer.delete(
            0,
            END
        )

        security_answer.focus_set()


# ============================================================
# GO BACK TO USERNAME SECTION
# ============================================================

def back_to_username():

    security_section.place_forget()

    security_answer.delete(
        0,
        END
    )

    username_section.place(
        x=80,
        y=80
    )

    username.focus_set()


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
# PROJECT TITLE
# ============================================================

project_title = Label(
    left_panel,
    text="FEE STATUS\nMANAGEMENT SYSTEM",
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
# FORGOT PASSWORD IMAGE
# ============================================================

forgot_image_path = os.path.join(
    IMAGES_DIR,
    "forgot.png"
)


# If forgot_password.png exists, show it.
# Otherwise show simple recovery text.

if os.path.exists(forgot_image_path):

    forgot_image = PhotoImage(
        file=forgot_image_path
    )

    forgot_image = forgot_image.subsample(
        2,
        2
    )

    image_label = Label(
        left_panel,
        image=forgot_image,
        bg=LIGHT_BLUE
    )

    image_label.place(
        x=0,
        y=110,
        width=400,
        height=550
    )


else:

    image_label = Label(
        left_panel,
        text="ACCOUNT\nRECOVERY",
        bg=LIGHT_BLUE,
        fg=BLUE,
        font=(
            "Helvetica",
            26,
            "bold"
        ),
        justify="center"
    )

    image_label.place(
        x=0,
        y=120,
        width=400,
        height=350
    )


# ============================================================
# PROJECT DESCRIPTION
# ============================================================

project_description = Label(
    left_panel,
    text="Recover your account securely",
    bg=LIGHT_BLUE,
    fg=GRAY,
    font=(
        "Helvetica",
        12
    )
)

project_description.place(
    x=90,
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
# STAGE 1 - USERNAME SECTION
# ============================================================

username_section = Frame(
    right_panel,
    bg=WHITE,
    width=340,
    height=420
)

username_section.place(
    x=80,
    y=80
)


# ============================================================
# FORGOT PASSWORD TITLE
# ============================================================

forgot_title = Label(
    username_section,
    text="Forgot Password?",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        27,
        "bold"
    )
)

forgot_title.place(
    x=0,
    y=0
)


# ============================================================
# SUBTITLE
# ============================================================

forgot_subtitle = Label(
    username_section,
    text="Let's find your account",
    bg=WHITE,
    fg=GRAY,
    font=(
        "Helvetica",
        11
    )
)

forgot_subtitle.place(
    x=0,
    y=48
)


# ============================================================
# USERNAME LABEL
# ============================================================

username_label = Label(
    username_section,
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
    y=120
)


# ============================================================
# USERNAME ENTRY
# ============================================================

username = Entry(
    username_section,
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
# VERIFY USERNAME BUTTON
# ============================================================

verify_username_button = Button(
    username_section,
    text="VERIFY USERNAME",
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
    command=verify_username
)

verify_username_button.place(
    x=0,
    y=230,
    width=340,
    height=45
)


# ============================================================
# BACK TO LOGIN BUTTON
# ============================================================

back_login_button = Button(
    username_section,
    text="←  Back to Login",
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

back_login_button.place(
    x=105,
    y=310
)


# ============================================================
# STAGE 2 - SECURITY QUESTION SECTION
# ============================================================

security_section = Frame(
    right_panel,
    bg=WHITE,
    width=340,
    height=450
)


# IMPORTANT:
# Do not place this section initially.
# It will appear after Username verification.


# ============================================================
# SECURITY TITLE
# ============================================================

security_title = Label(
    security_section,
    text="Verify Your Identity",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        25,
        "bold"
    )
)

security_title.place(
    x=0,
    y=0
)


# ============================================================
# SECURITY SUBTITLE
# ============================================================

security_subtitle = Label(
    security_section,
    text="Answer your security question",
    bg=WHITE,
    fg=GRAY,
    font=(
        "Helvetica",
        11
    )
)

security_subtitle.place(
    x=0,
    y=45
)


# ============================================================
# SECURITY QUESTION LABEL
# ============================================================

question_label = Label(
    security_section,
    text="Security Question",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        11,
        "bold"
    )
)

question_label.place(
    x=0,
    y=100
)


# ============================================================
# SECURITY QUESTION DISPLAY
# ============================================================

question_box = Frame(
    security_section,
    bg=LIGHT_BLUE,
    width=340,
    height=65
)

question_box.place(
    x=0,
    y=130
)


question_display = Label(
    question_box,
    text="Security question will appear here",
    bg=LIGHT_BLUE,
    fg=DARK_BLUE,
    font=(
        "Helvetica",
        11,
        "bold"
    ),
    wraplength=300,
    justify="left"
)

question_display.place(
    x=15,
    y=10,
    width=310,
    height=45
)


# ============================================================
# SECURITY ANSWER LABEL
# ============================================================

answer_label = Label(
    security_section,
    text="Security Answer",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        11,
        "bold"
    )
)

answer_label.place(
    x=0,
    y=225
)


# ============================================================
# SECURITY ANSWER ENTRY
# ============================================================

security_answer = Entry(
    security_section,
    font=(
        "Helvetica",
        12
    ),
    fg=TEXT_COLOR,
    bg=WHITE,
    bd=1,
    relief="solid"
)

security_answer.place(
    x=0,
    y=260,
    width=340,
    height=42
)


# ============================================================
# VERIFY ANSWER BUTTON
# ============================================================

verify_answer_button = Button(
    security_section,
    text="VERIFY ANSWER",
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
    command=verify_answer
)

verify_answer_button.place(
    x=0,
    y=335,
    width=340,
    height=45
)


# ============================================================
# BACK BUTTON
# ============================================================

back_button = Button(
    security_section,
    text="←  Change Username",
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
    command=back_to_username
)

back_button.place(
    x=100,
    y=405
)


# ============================================================
# STAGE 3 - RESULT SECTION
# ============================================================

result_section = Frame(
    right_panel,
    bg=WHITE,
    width=340,
    height=450
)


# IMPORTANT:
# Do not place this section initially.
# It will appear after Security Answer verification.


# ============================================================
# SUCCESS ICON
# ============================================================

success_icon = Label(
    result_section,
    text="✓",
    bg=GREEN,
    fg=WHITE,
    font=(
        "Helvetica",
        20,
        "bold"
    )
)

success_icon.place(
    x=120,
    y=0,
    width=30,
    height=30
)


# ============================================================
# WELCOME LABEL
# ============================================================

welcome_label = Label(
    result_section,
    text="Welcome Back!",
    bg=WHITE,
    fg=TEXT_COLOR,
    font=(
        "Helvetica",
        23,
        "bold"
    ),
    justify="left"
)

welcome_label.place(
    x=0,
    y=40
)


# ============================================================
# SUCCESS MESSAGE
# ============================================================

success_message = Label(
    result_section,
    text="Your account has been verified successfully.",
    bg=WHITE,
    fg=GRAY,
    font=(
        "Helvetica",
        10
    )
)

success_message.place(
    x=0,
    y=145
)


# ============================================================
# USERNAME LABEL
# ============================================================

recovered_username_label = Label(
    result_section,
    text="Username",
    bg=WHITE,
    fg=GRAY,
    font=(
        "Helvetica",
        10,
        "bold"
    )
)

recovered_username_label.place(
    x=0,
    y=190
)


# ============================================================
# USERNAME DISPLAY BOX
# ============================================================

username_result_box = Frame(
    result_section,
    bg=LIGHT_BLUE,
    width=340,
    height=45
)

username_result_box.place(
    x=0,
    y=215
)


recovered_username = Label(
    username_result_box,
    text="Username",
    bg=LIGHT_BLUE,
    fg=DARK_BLUE,
    font=(
        "Helvetica",
        12,
        "bold"
    ),
    anchor="w"
)

recovered_username.place(
    x=15,
    y=0,
    width=310,
    height=45
)


# ============================================================
# PASSWORD LABEL
# ============================================================

recovered_password_label = Label(
    result_section,
    text="Password",
    bg=WHITE,
    fg=GRAY,
    font=(
        "Helvetica",
        10,
        "bold"
    )
)

recovered_password_label.place(
    x=0,
    y=285
)


# ============================================================
# PASSWORD DISPLAY BOX
# ============================================================

password_result_box = Frame(
    result_section,
    bg=LIGHT_BLUE,
    width=340,
    height=45
)

password_result_box.place(
    x=0,
    y=310
)


recovered_password = Label(
    password_result_box,
    text="Password",
    bg=LIGHT_BLUE,
    fg=DARK_BLUE,
    font=(
        "Helvetica",
        12,
        "bold"
    ),
    anchor="w"
)

recovered_password.place(
    x=15,
    y=0,
    width=310,
    height=45
)


# ============================================================
# BACK TO LOGIN BUTTON
# ============================================================

result_login_button = Button(
    result_section,
    text="BACK TO LOGIN",
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
    command=open_login
)

result_login_button.place(
    x=0,
    y=395,
    width=340,
    height=45
)


# ============================================================
# PRESS ENTER
# ============================================================

def enter_key(event):

    # If Username Section is Visible

    if username_section.winfo_ismapped():

        verify_username()


    # If Security Section is Visible

    elif security_section.winfo_ismapped():

        verify_answer()


window.bind(
    "<Return>",
    enter_key
)


# ============================================================
# MAIN LOOP
# ============================================================

window.mainloop()
