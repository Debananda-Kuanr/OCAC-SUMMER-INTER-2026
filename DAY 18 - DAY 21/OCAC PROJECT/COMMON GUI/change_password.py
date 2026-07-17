from tkinter import *
from tkinter import messagebox
import mysql.connector
import os


# ============================================================
# FILE NAME: change_password.py
# LOCATION : COMMON GUI/change_password.py
#
# FLOW:
#   1. Enter Username
#   2. Enter Current Password
#   3. Verify Account
#   4. Enter New Password
#   5. Confirm New Password
#   6. Update Password
#
# USED BY:
#   - Admin
#   - Accountant
#   - Student
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

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="9439",
        database="OCAC_GROUP2"
    )


# ============================================================
# MAIN CHANGE PASSWORD WINDOW
# ============================================================

def open_change_password(
    parent=None,
    current_registration_no=None
):

    # ========================================================
    # CREATE WINDOW
    # ========================================================

    if parent is None:

        window = Tk()

    else:

        window = Toplevel(
            parent
        )


    window.title(
        "Change Password"
    )

    window.configure(
        bg=WHITE
    )

    window.resizable(
        False,
        False
    )


    # ========================================================
    # WINDOW SIZE
    # ========================================================

    window_width = 900
    window_height = 550


    # ========================================================
    # CENTER WINDOW
    # ========================================================

    window.update_idletasks()

    screen_width = (
        window.winfo_screenwidth()
    )

    screen_height = (
        window.winfo_screenheight()
    )

    x = (
        screen_width
        - window_width
    ) // 2

    y = (
        screen_height
        - window_height
    ) // 2

    # Move slightly upward
    y = max(
        20,
        y - 25
    )

    window.geometry(
        f"{window_width}x"
        f"{window_height}+"
        f"{x}+{y}"
    )


    # ========================================================
    # MODAL WINDOW
    # ========================================================

    if parent is not None:

        try:

            window.transient(
                parent.winfo_toplevel()
            )

            window.grab_set()

        except TclError:

            pass


    # ========================================================
    # VARIABLES
    # ========================================================

    username_var = StringVar()

    current_password_var = StringVar()

    new_password_var = StringVar()

    confirm_password_var = StringVar()


    # ========================================================
    # VERIFIED USER INFORMATION
    # ========================================================

    verified_user = {

        "registration_no":
            None,

        "name":
            None,

        "username":
            None,

        "role":
            None
    }


    # ========================================================
    # PASSWORD VISIBILITY
    # ========================================================

    current_password_visible = False

    new_password_visible = False

    confirm_password_visible = False


    # ========================================================
    # CLOSE WINDOW
    # ========================================================

    def close_window():

        try:

            window.grab_release()

        except TclError:

            pass

        window.destroy()


    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )


    # ========================================================
    # LEFT PANEL
    # ========================================================

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


    # ========================================================
    # PROJECT TITLE
    # ========================================================

    Label(
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
        justify=CENTER
    ).place(
        x=65,
        y=45
    )


    # ========================================================
    # IMAGE AREA
    # ========================================================

    image_label = Label(
        left_panel,
        bg=LIGHT_BLUE
    )

    image_label.place(
        x=0,
        y=100,
        width=400,
        height=450
    )


    # ========================================================
    # IMAGE PATHS
    # ========================================================

    image_paths = [

        # COMMON GUI/IMAGES/change_password.png
        os.path.join(
            CURRENT_DIR,
            "IMAGES",
            "change_password.png"
        ),

        # PROJECT/IMAGES/change_password.png
        os.path.join(
            PROJECT_DIR,
            "IMAGES",
            "change_password.png"
        ),

        # COMMON GUI/change_password.png
        os.path.join(
            CURRENT_DIR,
            "change_password.png"
        )
    ]


    change_password_image = None


    # ========================================================
    # LOAD IMAGE
    # ========================================================

    for image_path in image_paths:

        if os.path.exists(
            image_path
        ):

            try:

                change_password_image = PhotoImage(
                    file=image_path
                )

                # Reduce large image size
                change_password_image = (
                    change_password_image
                    .subsample(
                        2,
                        2
                    )
                )

                break

            except TclError:

                change_password_image = None


    # ========================================================
    # DISPLAY IMAGE
    # ========================================================

    if change_password_image is not None:

        image_label.config(
            image=change_password_image
        )

        # Keep reference
        image_label.image = (
            change_password_image
        )

    else:

        # ----------------------------------------------------
        # FALLBACK TEXT IF IMAGE NOT FOUND
        # ----------------------------------------------------

        image_label.config(
            text=(
                "CHANGE\n"
                "PASSWORD"
            ),
            fg=BLUE,
            bg=LIGHT_BLUE,
            font=(
                "Helvetica",
                28,
                "bold"
            ),
            justify=CENTER
        )


    # ========================================================
    # LEFT PANEL DESCRIPTION
    # ========================================================

    Label(
        left_panel,
        text="Keep your account secure",
        bg=LIGHT_BLUE,
        fg=GRAY,
        font=(
            "Helvetica",
            12
        )
    ).place(
        x=95,
        y=485
    )


    # ========================================================
    # RIGHT PANEL
    # ========================================================

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


    # ========================================================
    # FORM FRAME
    # ========================================================

    form_frame = Frame(
        right_panel,
        bg=WHITE,
        width=340,
        height=470
    )

    form_frame.place(
        x=80,
        y=40
    )


    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form():

        for widget in (
            form_frame
            .winfo_children()
        ):

            widget.destroy()


    # ========================================================
    # DRAW EYE ICON
    # ========================================================

    def draw_eye_icon(
        canvas,
        visible
    ):

        canvas.delete(
            "all"
        )


        # ----------------------------------------------------
        # OUTER EYE
        # ----------------------------------------------------

        canvas.create_oval(
            6,
            10,
            34,
            26,
            outline=GRAY,
            width=2
        )


        if visible:

            # ------------------------------------------------
            # PUPIL
            # ------------------------------------------------

            canvas.create_oval(
                14,
                14,
                26,
                22,
                outline=GRAY,
                fill=GRAY
            )

        else:

            # ------------------------------------------------
            # SLASH
            # ------------------------------------------------

            canvas.create_line(
                8,
                12,
                32,
                24,
                fill=GRAY,
                width=3,
                capstyle=ROUND
            )


    # ========================================================
    # CREATE NORMAL ENTRY
    # ========================================================

    def create_normal_entry(
        y_position,
        variable
    ):

        entry = Entry(
            form_frame,
            textvariable=variable,
            font=(
                "Helvetica",
                12
            ),
            fg=TEXT_COLOR,
            bg=WHITE,
            insertbackground=TEXT_COLOR,
            bd=1,
            relief=SOLID
        )

        entry.place(
            x=0,
            y=y_position,
            width=340,
            height=42
        )

        return entry


    # ========================================================
    # CREATE PASSWORD ENTRY
    # ========================================================

    def create_password_entry(
        y_position,
        variable,
        visibility_type
    ):

        # ----------------------------------------------------
        # PASSWORD FRAME
        # ----------------------------------------------------

        password_frame = Frame(
            form_frame,
            bg=WHITE,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        password_frame.place(
            x=0,
            y=y_position,
            width=340,
            height=42
        )


        # ----------------------------------------------------
        # PASSWORD ENTRY
        # ----------------------------------------------------

        password_entry = Entry(
            password_frame,
            textvariable=variable,
            font=(
                "Helvetica",
                12
            ),
            fg=TEXT_COLOR,
            bg=WHITE,
            insertbackground=TEXT_COLOR,
            bd=0,
            show="*"
        )

        password_entry.place(
            x=10,
            y=1,
            width=280,
            height=38
        )


        # ----------------------------------------------------
        # EYE CANVAS
        # ----------------------------------------------------

        eye_canvas = Canvas(
            password_frame,
            bg=WHITE,
            highlightthickness=0,
            cursor="hand2"
        )

        eye_canvas.place(
            x=295,
            y=2,
            width=40,
            height=36
        )


        # ----------------------------------------------------
        # INITIAL EYE
        # ----------------------------------------------------

        draw_eye_icon(
            eye_canvas,
            False
        )


        # ====================================================
        # TOGGLE PASSWORD
        # ====================================================

        def toggle_password():

            # CORRECT NONLOCAL SYNTAX
            nonlocal current_password_visible
            nonlocal new_password_visible
            nonlocal confirm_password_visible


            # ================================================
            # CURRENT PASSWORD
            # ================================================

            if visibility_type == "current":

                current_password_visible = (
                    not current_password_visible
                )

                if current_password_visible:

                    password_entry.config(
                        show=""
                    )

                    draw_eye_icon(
                        eye_canvas,
                        True
                    )

                else:

                    password_entry.config(
                        show="*"
                    )

                    draw_eye_icon(
                        eye_canvas,
                        False
                    )


            # ================================================
            # NEW PASSWORD
            # ================================================

            elif visibility_type == "new":

                new_password_visible = (
                    not new_password_visible
                )

                if new_password_visible:

                    password_entry.config(
                        show=""
                    )

                    draw_eye_icon(
                        eye_canvas,
                        True
                    )

                else:

                    password_entry.config(
                        show="*"
                    )

                    draw_eye_icon(
                        eye_canvas,
                        False
                    )


            # ================================================
            # CONFIRM PASSWORD
            # ================================================

            elif visibility_type == "confirm":

                confirm_password_visible = (
                    not confirm_password_visible
                )

                if confirm_password_visible:

                    password_entry.config(
                        show=""
                    )

                    draw_eye_icon(
                        eye_canvas,
                        True
                    )

                else:

                    password_entry.config(
                        show="*"
                    )

                    draw_eye_icon(
                        eye_canvas,
                        False
                    )


        # ----------------------------------------------------
        # EYE CLICK EVENT
        # ----------------------------------------------------

        eye_canvas.bind(
            "<Button-1>",
            lambda event:
            toggle_password()
        )


        return password_entry


    # ========================================================
    # VERIFY ACCOUNT
    # ========================================================

    def verify_account():

        username = (
            username_var
            .get()
            .strip()
        )

        current_password = (
            current_password_var
            .get()
        )


        # ----------------------------------------------------
        # VALIDATE USERNAME
        # ----------------------------------------------------

        if username == "":

            messagebox.showwarning(
                "Warning",
                "Please enter your Username",
                parent=window
            )

            return


        # ----------------------------------------------------
        # VALIDATE CURRENT PASSWORD
        # ----------------------------------------------------

        if current_password == "":

            messagebox.showwarning(
                "Warning",
                (
                    "Please enter your "
                    "Current Password"
                ),
                parent=window
            )

            return


        # ----------------------------------------------------
        # DATABASE VARIABLES
        # ----------------------------------------------------

        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor(
                dictionary=True
            )


            # ------------------------------------------------
            # SECURE MODE
            #
            # If Registration_No is provided,
            # only the logged-in account can be verified.
            # ------------------------------------------------

            if current_registration_no:

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
                        BINARY Username = BINARY %s

                    AND
                        BINARY Password = BINARY %s
                    """,
                    (
                        current_registration_no,
                        username,
                        current_password
                    )
                )


            # ------------------------------------------------
            # GENERIC MODE
            # ------------------------------------------------

            else:

                cursor.execute(
                    """
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
                    """,
                    (
                        username,
                        current_password
                    )
                )


            user = cursor.fetchone()


            # ------------------------------------------------
            # INVALID ACCOUNT
            # ------------------------------------------------

            if user is None:

                messagebox.showerror(
                    "Verification Failed",
                    (
                        "Invalid Username or "
                        "Current Password"
                    ),
                    parent=window
                )

                current_password_var.set(
                    ""
                )

                return


            # ------------------------------------------------
            # STORE VERIFIED USER
            # ------------------------------------------------

            verified_user[
                "registration_no"
            ] = user[
                "Registration_No"
            ]

            verified_user[
                "name"
            ] = user[
                "Name"
            ]

            verified_user[
                "username"
            ] = user[
                "Username"
            ]

            verified_user[
                "role"
            ] = user[
                "Role"
            ]


            # ------------------------------------------------
            # SHOW STEP 2
            # ------------------------------------------------

            show_new_password_form()


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Unable to verify "
                    "the account."
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


    # ========================================================
    # UPDATE PASSWORD
    # ========================================================

    def update_password():

        new_password = (
            new_password_var
            .get()
        )

        confirm_password = (
            confirm_password_var
            .get()
        )


        # ----------------------------------------------------
        # CHECK VERIFIED USER
        # ----------------------------------------------------

        if not verified_user[
            "registration_no"
        ]:

            messagebox.showerror(
                "Verification Required",
                (
                    "Please verify your "
                    "account first."
                ),
                parent=window
            )

            show_verify_form()

            return


        # ----------------------------------------------------
        # NEW PASSWORD REQUIRED
        # ----------------------------------------------------

        if new_password == "":

            messagebox.showwarning(
                "Warning",
                (
                    "Please enter a "
                    "New Password"
                ),
                parent=window
            )

            return


        # ----------------------------------------------------
        # MINIMUM LENGTH
        # ----------------------------------------------------

        if len(
            new_password
        ) < 6:

            messagebox.showwarning(
                "Weak Password",
                (
                    "New Password must contain "
                    "at least 6 characters."
                ),
                parent=window
            )

            return


        # ----------------------------------------------------
        # CONFIRM PASSWORD REQUIRED
        # ----------------------------------------------------

        if confirm_password == "":

            messagebox.showwarning(
                "Warning",
                (
                    "Please confirm your "
                    "New Password"
                ),
                parent=window
            )

            return


        # ----------------------------------------------------
        # PASSWORD MATCH
        # ----------------------------------------------------

        if new_password != confirm_password:

            messagebox.showerror(
                "Password Mismatch",
                (
                    "New Password and "
                    "Confirm Password "
                    "do not match."
                ),
                parent=window
            )

            confirm_password_var.set(
                ""
            )

            return


        # ----------------------------------------------------
        # PREVENT SAME PASSWORD
        # ----------------------------------------------------

        if (
            new_password
            ==
            current_password_var.get()
        ):

            messagebox.showwarning(
                "Same Password",
                (
                    "New Password cannot be "
                    "the same as your "
                    "Current Password."
                ),
                parent=window
            )

            return


        # ----------------------------------------------------
        # DATABASE VARIABLES
        # ----------------------------------------------------

        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()


            # ------------------------------------------------
            # UPDATE VERIFIED USER
            # ------------------------------------------------

            cursor.execute(
                """
                UPDATE registration

                SET
                    Password = %s

                WHERE
                    Registration_No = %s
                """,
                (
                    new_password,

                    verified_user[
                        "registration_no"
                    ]
                )
            )


            # ------------------------------------------------
            # UPDATE CHECK
            # ------------------------------------------------

            if cursor.rowcount == 0:

                con.rollback()

                messagebox.showerror(
                    "Update Failed",
                    (
                        "Password could not "
                        "be updated."
                    ),
                    parent=window
                )

                return


            # ------------------------------------------------
            # COMMIT
            # ------------------------------------------------

            con.commit()


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            messagebox.showinfo(
                "Password Updated",
                (
                    "Your password has been "
                    "updated successfully."
                ),
                parent=window
            )


            close_window()


        except mysql.connector.Error as error:

            if con is not None:

                con.rollback()


            messagebox.showerror(
                "Database Error",
                (
                    "Unable to update "
                    "the password."
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


    # ========================================================
    # STEP 1
    # VERIFY ACCOUNT FORM
    # ========================================================

    def show_verify_form():

        clear_form()


        # ----------------------------------------------------
        # RESET VERIFIED USER
        # ----------------------------------------------------

        verified_user[
            "registration_no"
        ] = None

        verified_user[
            "name"
        ] = None

        verified_user[
            "username"
        ] = None

        verified_user[
            "role"
        ] = None


        # ----------------------------------------------------
        # RESET STEP 2 FIELDS
        # ----------------------------------------------------

        new_password_var.set(
            ""
        )

        confirm_password_var.set(
            ""
        )


        # ====================================================
        # TITLE
        # ====================================================

        Label(
            form_frame,
            text="Change Password",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                28,
                "bold"
            )
        ).place(
            x=0,
            y=20
        )


        # ====================================================
        # SUBTITLE
        # ====================================================

        Label(
            form_frame,
            text=(
                "Verify your account "
                "to continue"
            ),
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                12
            )
        ).place(
            x=0,
            y=65
        )


        # ====================================================
        # USERNAME LABEL
        # ====================================================

        Label(
            form_frame,
            text="Username",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                11,
                "bold"
            )
        ).place(
            x=0,
            y=125
        )


        # ====================================================
        # USERNAME ENTRY
        # ====================================================

        username_entry = (
            create_normal_entry(
                155,
                username_var
            )
        )


        # ====================================================
        # CURRENT PASSWORD LABEL
        # ====================================================

        Label(
            form_frame,
            text="Current Password",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                11,
                "bold"
            )
        ).place(
            x=0,
            y=225
        )


        # ====================================================
        # CURRENT PASSWORD ENTRY
        # ====================================================

        current_password_entry = (
            create_password_entry(
                255,
                current_password_var,
                "current"
            )
        )


        # ====================================================
        # VERIFY BUTTON
        # ====================================================

        Button(
            form_frame,
            text="VERIFY ACCOUNT",
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
            command=verify_account
        ).place(
            x=0,
            y=335,
            width=340,
            height=45
        )


        # ====================================================
        # CANCEL BUTTON
        # ====================================================

        Button(
            form_frame,
            text="CANCEL",
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
            command=close_window
        ).place(
            x=135,
            y=410
        )


        # ====================================================
        # ENTER KEY EVENTS
        # ====================================================

        username_entry.bind(
            "<Return>",
            lambda event:
            current_password_entry
            .focus_set()
        )

        current_password_entry.bind(
            "<Return>",
            lambda event:
            verify_account()
        )


        username_entry.focus_set()


    # ========================================================
    # STEP 2
    # CREATE NEW PASSWORD FORM
    # ========================================================

    def show_new_password_form():

        clear_form()


        # ====================================================
        # TITLE
        # ====================================================

        Label(
            form_frame,
            text="Create New Password",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                25,
                "bold"
            )
        ).place(
            x=0,
            y=10
        )


        # ====================================================
        # VERIFIED MESSAGE
        # ====================================================

        Label(
            form_frame,
            text="Account verified successfully",
            bg=WHITE,
            fg=GREEN,
            font=(
                "Helvetica",
                10,
                "bold"
            )
        ).place(
            x=0,
            y=58
        )


        # ====================================================
        # WELCOME USER
        # ====================================================

        Label(
            form_frame,
            text=(
                f"Welcome, "
                f"{verified_user['name']}"
            ),
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                11
            )
        ).place(
            x=0,
            y=82
        )


        # ====================================================
        # NEW PASSWORD LABEL
        # ====================================================

        Label(
            form_frame,
            text="New Password",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                11,
                "bold"
            )
        ).place(
            x=0,
            y=135
        )


        # ====================================================
        # NEW PASSWORD ENTRY
        # ====================================================

        new_password_entry = (
            create_password_entry(
                165,
                new_password_var,
                "new"
            )
        )


        # ====================================================
        # CONFIRM PASSWORD LABEL
        # ====================================================

        Label(
            form_frame,
            text="Confirm New Password",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                11,
                "bold"
            )
        ).place(
            x=0,
            y=235
        )


        # ====================================================
        # CONFIRM PASSWORD ENTRY
        # ====================================================

        confirm_password_entry = (
            create_password_entry(
                265,
                confirm_password_var,
                "confirm"
            )
        )


        # ====================================================
        # PASSWORD INFORMATION
        # ====================================================

        Label(
            form_frame,
            text=(
                "Password must contain at "
                "least 6 characters"
            ),
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                9
            )
        ).place(
            x=0,
            y=315
        )


        # ====================================================
        # UPDATE PASSWORD BUTTON
        # ====================================================

        Button(
            form_frame,
            text="UPDATE PASSWORD",
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
            command=update_password
        ).place(
            x=0,
            y=350,
            width=340,
            height=45
        )


        # ====================================================
        # BACK BUTTON
        # ====================================================

        Button(
            form_frame,
            text="← BACK TO VERIFICATION",
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
            command=show_verify_form
        ).place(
            x=85,
            y=420
        )


        # ====================================================
        # ENTER KEY EVENTS
        # ====================================================

        new_password_entry.bind(
            "<Return>",
            lambda event:
            confirm_password_entry
            .focus_set()
        )

        confirm_password_entry.bind(
            "<Return>",
            lambda event:
            update_password()
        )


        new_password_entry.focus_set()


    # ========================================================
    # INITIAL FORM
    # ========================================================

    show_verify_form()


    # ========================================================
    # STANDALONE MAINLOOP
    # ========================================================

    if parent is None:

        window.mainloop()


# ============================================================
# RUN FILE DIRECTLY FOR TESTING
# ============================================================

if __name__ == "__main__":

    open_change_password()
