from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
DARK_BLUE = "#1D4ED8"

WHITE = "#FFFFFF"
TEXT_COLOR = "#0F172A"
GRAY = "#64748B"
BORDER = "#CBD5E1"
DISABLED_BG = "#F1F5F9"


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

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="9439",
        database="OCAC_GROUP2"
    )


# ============================================================
# GENERATE ACCOUNTANT ID
# ============================================================

def generate_accountant_id():

    con = None
    cursor = None

    try:

        # ----------------------------------------------------
        # DATABASE CONNECTION
        # ----------------------------------------------------

        con = get_connection()

        cursor = con.cursor()


        # ----------------------------------------------------
        # FIND HIGHEST ACCOUNTANT ID
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT Registration_No

            FROM registration

            WHERE
                LOWER(Role) = 'accountant'

                AND Registration_No
                REGEXP '^ACC[0-9]+$'

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
        # FIRST ACCOUNTANT
        # ----------------------------------------------------

        if result is None:

            return "ACC00001"


        # ----------------------------------------------------
        # GET LAST ACCOUNTANT ID
        # ----------------------------------------------------

        last_accountant_id = str(
            result[0]
        )


        # Example:
        #
        # ACC00025
        #
        # last_accountant_id[3:]
        #
        # becomes:
        #
        # 00025

        last_number = int(
            last_accountant_id[3:]
        )


        # ----------------------------------------------------
        # GENERATE NEXT NUMBER
        # ----------------------------------------------------

        next_number = (
            last_number + 1
        )


        # ----------------------------------------------------
        # RETURN NEW ACCOUNTANT ID
        # ----------------------------------------------------

        return (
            f"ACC{next_number:05d}"
        )


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            (
                "Unable to generate "
                "Accountant ID."
                "\n\n"
                f"{error}"
            )
        )

        return ""


    except ValueError:

        return "ACC00001"


    finally:

        if cursor is not None:

            try:

                cursor.close()

            except:

                pass


        if con is not None:

            try:

                if con.is_connected():

                    con.close()

            except:

                pass


# ============================================================
# OPEN ACCOUNTANT FORM
# ============================================================

def open_accountant_form(
    parent,
    refresh_callback,
    accountant_id=None
):

    # ========================================================
    # CHECK MODE
    # ========================================================

    # accountant_id is None
    #     -> Add Accountant
    #
    # accountant_id has value
    #     -> Edit Accountant

    edit_mode = (
        accountant_id is not None
    )


    # ========================================================
    # CREATE NEW WINDOW
    # ========================================================

    form_window = Toplevel(
        parent
    )


    # ========================================================
    # WINDOW TITLE
    # ========================================================

    if edit_mode:

        form_window.title(
            (
                "Edit Accountant - "
                "Fee Status Management System"
            )
        )


    else:

        form_window.title(
            (
                "Add Accountant - "
                "Fee Status Management System"
            )
        )


    # ========================================================
    # WINDOW SIZE
    # ========================================================

    WINDOW_WIDTH = 700

    WINDOW_HEIGHT = 500


    form_window.geometry(
        (
            f"{WINDOW_WIDTH}"
            f"x"
            f"{WINDOW_HEIGHT}"
        )
    )


    form_window.resizable(
        False,
        False
    )


    form_window.configure(
        bg=WHITE
    )


    # ========================================================
    # MAKE WINDOW MODAL
    # ========================================================

    main_window = (
        parent.winfo_toplevel()
    )


    form_window.transient(
        main_window
    )


    form_window.grab_set()


    # ========================================================
    # CENTER WINDOW
    # ========================================================

    form_window.update_idletasks()


    screen_width = (
        form_window
        .winfo_screenwidth()
    )


    screen_height = (
        form_window
        .winfo_screenheight()
    )


    x = (
        screen_width
        - WINDOW_WIDTH
    ) // 2


    y = (
        screen_height
        - WINDOW_HEIGHT
    ) // 2


    form_window.geometry(
        (
            f"{WINDOW_WIDTH}"
            f"x"
            f"{WINDOW_HEIGHT}"
            f"+{x}"
            f"+{y}"
        )
    )


    # ========================================================
    # TITLE TEXT
    # ========================================================

    if edit_mode:

        title_text = (
            "Edit Accountant"
        )


        subtitle_text = (
            "Update accountant information"
        )


        save_button_text = (
            "SAVE CHANGES"
        )


    else:

        title_text = (
            "Add Accountant"
        )


        subtitle_text = (
            (
                "Enter details to create "
                "a new accountant"
            )
        )


        save_button_text = (
            "ADD ACCOUNTANT"
        )


    # ========================================================
    # TITLE
    # ========================================================

    title_label = Label(
        form_window,
        text=title_text,
        bg=WHITE,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            20,
            "bold"
        )
    )


    title_label.place(
        x=40,
        y=30
    )


    # ========================================================
    # SUBTITLE
    # ========================================================

    subtitle_label = Label(
        form_window,
        text=subtitle_text,
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            10
        )
    )


    subtitle_label.place(
        x=42,
        y=68
    )


    # ========================================================
    # SEPARATOR
    # ========================================================

    separator = Frame(
        form_window,
        bg="#E2E8F0"
    )


    separator.place(
        x=40,
        y=105,
        width=620,
        height=1
    )


    # ========================================================
    # FORM POSITIONS
    # ========================================================

    LEFT_X = 40

    RIGHT_X = 370

    FIELD_WIDTH = 290

    FIELD_HEIGHT = 40


    # ========================================================
    # ACCOUNTANT ID LABEL
    # ========================================================

    id_label = Label(
        form_window,
        text="Accountant ID",
        bg=WHITE,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            10,
            "bold"
        )
    )


    id_label.place(
        x=LEFT_X,
        y=130
    )


    # ========================================================
    # ACCOUNTANT ID ENTRY
    # READ ONLY
    # ========================================================

    id_entry = Entry(
        form_window,
        font=(
            "Helvetica",
            11,
            "bold"
        ),
        fg=BLUE,
        bg=DISABLED_BG,
        readonlybackground=DISABLED_BG,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BORDER,
        state="readonly"
    )


    id_entry.place(
        x=LEFT_X,
        y=160,
        width=FIELD_WIDTH,
        height=FIELD_HEIGHT
    )


    # ========================================================
    # FULL NAME LABEL
    # ========================================================

    name_label = Label(
        form_window,
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
        x=RIGHT_X,
        y=130
    )


    # ========================================================
    # FULL NAME ENTRY
    # ========================================================

    name_entry = Entry(
        form_window,
        font=(
            "Helvetica",
            11
        ),
        fg=TEXT_COLOR,
        bg=WHITE,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BLUE
    )


    name_entry.place(
        x=RIGHT_X,
        y=160,
        width=FIELD_WIDTH,
        height=FIELD_HEIGHT
    )


    # ========================================================
    # USERNAME LABEL
    # ========================================================

    username_label = Label(
        form_window,
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
        x=LEFT_X,
        y=225
    )


    # ========================================================
    # USERNAME ENTRY
    # ========================================================

    username_entry = Entry(
        form_window,
        font=(
            "Helvetica",
            11
        ),
        fg=TEXT_COLOR,
        bg=WHITE,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BLUE
    )


    username_entry.place(
        x=LEFT_X,
        y=255,
        width=FIELD_WIDTH,
        height=FIELD_HEIGHT
    )


    # ========================================================
    # PASSWORD LABEL
    # ========================================================

    password_label = Label(
        form_window,
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
        x=RIGHT_X,
        y=225
    )


    # ========================================================
    # PASSWORD CONTAINER
    # ========================================================

    password_frame = Frame(
        form_window,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightcolor=BLUE,
        highlightthickness=1
    )


    password_frame.place(
        x=RIGHT_X,
        y=255,
        width=FIELD_WIDTH,
        height=FIELD_HEIGHT
    )


    # ========================================================
    # PASSWORD ENTRY
    # ========================================================

    password_entry = Entry(
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


    password_entry.place(
        x=10,
        y=2,
        width=220,
        height=34
    )


    # ========================================================
    # PASSWORD VISIBILITY
    # ========================================================

    password_visible = False


    # ========================================================
    # TOGGLE PASSWORD
    # ========================================================

    def toggle_password():

        nonlocal password_visible


        if password_visible:

            password_entry.config(
                show="*"
            )


            show_password_button.config(
                text="Show"
            )


            password_visible = False


        else:

            password_entry.config(
                show=""
            )


            show_password_button.config(
                text="Hide"
            )


            password_visible = True


    # ========================================================
    # SHOW / HIDE PASSWORD BUTTON
    # ========================================================

    show_password_button = Button(
        password_frame,
        text="Show",
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
        command=toggle_password
    )


    show_password_button.place(
        x=235,
        y=3,
        width=45,
        height=32
    )


    # ========================================================
    # SECURITY QUESTION LABEL
    # ========================================================

    question_label = Label(
        form_window,
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
        x=LEFT_X,
        y=320
    )


    # ========================================================
    # COMBOBOX STYLE
    # ========================================================

    style = ttk.Style(
        form_window
    )


    try:

        style.theme_use(
            "clam"
        )

    except TclError:

        pass


    style.configure(
        "Accountant.Security.TCombobox",
        fieldbackground=WHITE,
        background=WHITE,
        foreground=TEXT_COLOR,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        arrowcolor=GRAY,
        padding=8
    )


    style.map(
        "Accountant.Security.TCombobox",

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


    # ========================================================
    # SECURITY QUESTION DROPDOWN
    # ========================================================

    question_entry = ttk.Combobox(
        form_window,
        values=SECURITY_QUESTIONS,
        state="readonly",
        style=(
            "Accountant.Security.TCombobox"
        ),
        font=(
            "Helvetica",
            10
        )
    )


    question_entry.place(
        x=LEFT_X,
        y=350,
        width=FIELD_WIDTH,
        height=FIELD_HEIGHT
    )


    # ========================================================
    # DEFAULT SECURITY QUESTION
    # ========================================================

    question_entry.set(
        DEFAULT_SECURITY_QUESTION
    )


    # ========================================================
    # SECURITY ANSWER LABEL
    # ========================================================

    answer_label = Label(
        form_window,
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
        x=RIGHT_X,
        y=320
    )


    # ========================================================
    # SECURITY ANSWER ENTRY
    # ========================================================

    answer_entry = Entry(
        form_window,
        font=(
            "Helvetica",
            11
        ),
        fg=TEXT_COLOR,
        bg=WHITE,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BLUE
    )


    answer_entry.place(
        x=RIGHT_X,
        y=350,
        width=FIELD_WIDTH,
        height=FIELD_HEIGHT
    )


    # ========================================================
    # SET ACCOUNTANT ID
    # ========================================================

    def set_accountant_id(
        generated_id
    ):

        id_entry.config(
            state=NORMAL
        )


        id_entry.delete(
            0,
            END
        )


        id_entry.insert(
            0,
            generated_id
        )


        id_entry.config(
            state="readonly"
        )


    # ========================================================
    # LOAD ACCOUNTANT DATA
    # ========================================================

    def load_accountant():

        # ----------------------------------------------------
        # ONLY FOR EDIT MODE
        # ----------------------------------------------------

        if not edit_mode:

            return


        con = None

        cursor = None


        try:

            # ------------------------------------------------
            # CONNECT DATABASE
            # ------------------------------------------------

            con = get_connection()


            cursor = con.cursor()


            # ------------------------------------------------
            # GET ACCOUNTANT DATA
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT
                    Registration_No,
                    Name,
                    Username,
                    Password,
                    Security_Question,
                    Security_Answer

                FROM registration

                WHERE Registration_No = %s

                AND LOWER(Role) = 'accountant'
                """,
                (
                    accountant_id,
                )
            )


            result = cursor.fetchone()


            # ------------------------------------------------
            # ACCOUNTANT NOT FOUND
            # ------------------------------------------------

            if result is None:

                messagebox.showerror(
                    "Accountant Not Found",
                    (
                        "The selected accountant "
                        "was not found."
                    ),
                    parent=form_window
                )


                form_window.destroy()


                return


            # ------------------------------------------------
            # ACCOUNTANT ID
            # ------------------------------------------------

            set_accountant_id(
                result[0]
            )


            # ------------------------------------------------
            # NAME
            # ------------------------------------------------

            name_entry.delete(
                0,
                END
            )


            name_entry.insert(
                0,
                result[1]
            )


            # ------------------------------------------------
            # USERNAME
            # ------------------------------------------------

            username_entry.delete(
                0,
                END
            )


            username_entry.insert(
                0,
                result[2]
            )


            # ------------------------------------------------
            # PASSWORD
            # ------------------------------------------------

            password_entry.delete(
                0,
                END
            )


            password_entry.insert(
                0,
                result[3]
            )


            # ------------------------------------------------
            # SECURITY QUESTION
            # ------------------------------------------------

            saved_question = (
                result[4]
                if result[4]
                else DEFAULT_SECURITY_QUESTION
            )


            # If an old accountant has a question
            # that is not in the new list, add it
            # temporarily so existing data is not lost.

            if (
                saved_question
                != DEFAULT_SECURITY_QUESTION

                and saved_question
                not in SECURITY_QUESTIONS
            ):

                question_entry.config(
                    values=(
                        SECURITY_QUESTIONS
                        + [
                            saved_question
                        ]
                    )
                )


            question_entry.set(
                saved_question
            )


            # ------------------------------------------------
            # SECURITY ANSWER
            # ------------------------------------------------

            answer_entry.delete(
                0,
                END
            )


            answer_entry.insert(
                0,
                result[5]
            )


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=form_window
            )


        finally:

            if cursor is not None:

                try:

                    cursor.close()

                except:

                    pass


            if con is not None:

                try:

                    if con.is_connected():

                        con.close()

                except:

                    pass


    # ========================================================
    # SAVE ACCOUNTANT
    # ========================================================

    def save_accountant():

        # ====================================================
        # GET ACCOUNTANT ID
        # ====================================================

        if edit_mode:

            registration_no = (
                accountant_id
            )


        else:

            registration_no = (
                id_entry
                .get()
                .strip()
            )


        # ====================================================
        # GET FULL NAME
        # ====================================================

        full_name = (
            name_entry
            .get()
            .strip()
        )


        # ====================================================
        # GET USERNAME
        # ====================================================

        username = (
            username_entry
            .get()
            .strip()
        )


        # ====================================================
        # GET PASSWORD
        # ====================================================

        password = (
            password_entry
            .get()
            .strip()
        )


        # ====================================================
        # GET SECURITY QUESTION
        # ====================================================

        security_question = (
            question_entry
            .get()
            .strip()
        )


        # ====================================================
        # GET SECURITY ANSWER
        # ====================================================

        security_answer = (
            answer_entry
            .get()
            .strip()
        )


        # ====================================================
        # CHECK EMPTY FIELDS
        # ====================================================

        if (
            registration_no == ""
            or full_name == ""
            or username == ""
            or password == ""
            or security_question == ""
            or security_question
            == DEFAULT_SECURITY_QUESTION
            or security_answer == ""
        ):

            messagebox.showwarning(
                "Incomplete Form",
                (
                    "Please fill in all fields "
                    "and select a security question."
                ),
                parent=form_window
            )


            return


        # ====================================================
        # PASSWORD VALIDATION
        # ====================================================

        if len(password) < 4:

            messagebox.showwarning(
                "Invalid Password",
                (
                    "Password must contain "
                    "at least 4 characters."
                ),
                parent=form_window
            )


            password_entry.focus_set()


            return


        # ====================================================
        # DATABASE VARIABLES
        # ====================================================

        con = None

        cursor = None


        try:

            # ------------------------------------------------
            # DATABASE CONNECTION
            # ------------------------------------------------

            con = get_connection()


            cursor = con.cursor()


            # =================================================
            # EDIT ACCOUNTANT
            # =================================================

            if edit_mode:

                # --------------------------------------------
                # CHECK DUPLICATE USERNAME
                # --------------------------------------------

                cursor.execute(
                    """
                    SELECT Registration_No

                    FROM registration

                    WHERE Username = %s

                    AND Registration_No != %s
                    """,
                    (
                        username,
                        accountant_id
                    )
                )


                duplicate = (
                    cursor.fetchone()
                )


                if duplicate is not None:

                    messagebox.showerror(
                        "Username Exists",
                        (
                            "This Username is "
                            "already being used."
                        ),
                        parent=form_window
                    )


                    username_entry.focus_set()


                    return


                # --------------------------------------------
                # UPDATE ACCOUNTANT
                # --------------------------------------------

                cursor.execute(
                    """
                    UPDATE registration

                    SET
                        Name = %s,
                        Username = %s,
                        Password = %s,
                        Security_Question = %s,
                        Security_Answer = %s

                    WHERE Registration_No = %s

                    AND LOWER(Role) = 'accountant'
                    """,
                    (
                        full_name,
                        username,
                        password,
                        security_question,
                        security_answer,
                        accountant_id
                    )
                )


                # --------------------------------------------
                # SAVE CHANGES
                # --------------------------------------------

                con.commit()


                # --------------------------------------------
                # SUCCESS MESSAGE
                # --------------------------------------------

                messagebox.showinfo(
                    "Accountant Updated",
                    (
                        "Accountant information "
                        "updated successfully."
                    ),
                    parent=form_window
                )


            # =================================================
            # ADD ACCOUNTANT
            # =================================================

            else:

                # --------------------------------------------
                # CHECK DUPLICATE USERNAME
                # --------------------------------------------

                cursor.execute(
                    """
                    SELECT Registration_No

                    FROM registration

                    WHERE Username = %s
                    """,
                    (
                        username,
                    )
                )


                duplicate = (
                    cursor.fetchone()
                )


                if duplicate is not None:

                    messagebox.showerror(
                        "Username Exists",
                        (
                            "This Username is "
                            "already being used."
                        ),
                        parent=form_window
                    )


                    username_entry.focus_set()


                    return


                # --------------------------------------------
                # CHECK GENERATED ACCOUNTANT ID
                # --------------------------------------------

                cursor.execute(
                    """
                    SELECT Registration_No

                    FROM registration

                    WHERE Registration_No = %s
                    """,
                    (
                        registration_no,
                    )
                )


                duplicate_id = (
                    cursor.fetchone()
                )


                # --------------------------------------------
                # GENERATE NEW ID IF DUPLICATE
                # --------------------------------------------

                if duplicate_id is not None:

                    new_accountant_id = (
                        generate_accountant_id()
                    )


                    set_accountant_id(
                        new_accountant_id
                    )


                    messagebox.showwarning(
                        "Accountant ID Updated",
                        (
                            "The previous Accountant ID "
                            "was already used."
                            "\n\n"
                            "A new Accountant ID has "
                            "been generated."
                            "\n\n"
                            f"New ID: "
                            f"{new_accountant_id}"
                            "\n\n"
                            "Click ADD ACCOUNTANT again "
                            "to save the account."
                        ),
                        parent=form_window
                    )


                    return


                # --------------------------------------------
                # INSERT ACCOUNTANT
                # --------------------------------------------

                cursor.execute(
                    """
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
                    """,
                    (
                        registration_no,
                        full_name,
                        username,
                        password,
                        security_question,
                        security_answer,
                        "Accountant"
                    )
                )


                # --------------------------------------------
                # SAVE DATA
                # --------------------------------------------

                con.commit()


                # --------------------------------------------
                # SUCCESS MESSAGE
                # --------------------------------------------

                messagebox.showinfo(
                    "Accountant Added",
                    (
                        "New accountant added "
                        "successfully."
                        "\n\n"
                        f"Accountant ID: "
                        f"{registration_no}"
                    ),
                    parent=form_window
                )


            # =================================================
            # CLOSE FORM WINDOW
            # =================================================

            form_window.destroy()


            # =================================================
            # REFRESH ACCOUNTANT TABLE
            # =================================================

            refresh_callback()


        except mysql.connector.IntegrityError as error:

            try:

                if con is not None:

                    con.rollback()

            except:

                pass


            messagebox.showerror(
                "Account Already Exists",
                (
                    "Accountant ID or Username "
                    "already exists."
                    "\n\n"
                    f"{error}"
                ),
                parent=form_window
            )


        except mysql.connector.Error as error:

            try:

                if con is not None:

                    con.rollback()

            except:

                pass


            messagebox.showerror(
                "Database Error",
                str(error),
                parent=form_window
            )


        finally:

            if cursor is not None:

                try:

                    cursor.close()

                except:

                    pass


            if con is not None:

                try:

                    if con.is_connected():

                        con.close()

                except:

                    pass


    # ========================================================
    # CANCEL BUTTON
    # ========================================================

    cancel_button = Button(
        form_window,
        text="CANCEL",
        bg=WHITE,
        fg=TEXT_COLOR,
        activebackground="#F1F5F9",
        activeforeground=TEXT_COLOR,
        font=(
            "Helvetica",
            9,
            "bold"
        ),
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        cursor="hand2",
        command=form_window.destroy
    )


    cancel_button.place(
        x=420,
        y=425,
        width=105,
        height=40
    )


    # ========================================================
    # SAVE BUTTON
    # ========================================================

    save_button = Button(
        form_window,
        text=save_button_text,
        bg=BLUE,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        font=(
            "Helvetica",
            9,
            "bold"
        ),
        bd=0,
        cursor="hand2",
        command=save_accountant
    )


    save_button.place(
        x=540,
        y=425,
        width=120,
        height=40
    )


    # ========================================================
    # PRESS ENTER TO SAVE
    # ========================================================

    def enter_key(
        event
    ):

        save_accountant()


    form_window.bind(
        "<Return>",
        enter_key
    )


    # ========================================================
    # PRESS ESCAPE TO CLOSE
    # ========================================================

    form_window.bind(
        "<Escape>",
        lambda event: (
            form_window.destroy()
        )
    )


    # ========================================================
    # INITIAL PAGE LOAD
    # ========================================================

    if edit_mode:

        # ----------------------------------------------------
        # LOAD EXISTING ACCOUNTANT
        # ----------------------------------------------------

        load_accountant()


        name_entry.focus_set()


    else:

        # ----------------------------------------------------
        # AUTO GENERATE ACCOUNTANT ID
        # ----------------------------------------------------

        new_accountant_id = (
            generate_accountant_id()
        )


        set_accountant_id(
            new_accountant_id
        )


        # ----------------------------------------------------
        # FOCUS NAME FIELD
        # ----------------------------------------------------

        name_entry.focus_set()