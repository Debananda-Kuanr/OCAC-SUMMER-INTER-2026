from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import re


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
DARK_BLUE = "#1D4ED8"

WHITE = "#FFFFFF"
BACKGROUND = "#F8FAFC"

TEXT_COLOR = "#0F172A"
GRAY = "#64748B"
LIGHT_GRAY = "#94A3B8"

BORDER = "#E2E8F0"
INPUT_BORDER = "#CBD5E1"

GREEN = "#16A34A"
DARK_GREEN = "#15803D"

RED = "#DC2626"
ORANGE = "#EA580C"


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
# SECURITY QUESTIONS
# ============================================================

SECURITY_QUESTIONS = (

    "What is your favourite color?",

    "What is the name of your first school?",

    "What is your favourite food?",

    "What is your favourite sport?",

    "What is the name of your childhood friend?",

    "What is your favourite movie?",

    "What is your favourite book?",

    "What is your dream destination?",

    "What is your favourite subject?",

    "What is the name of your favourite teacher?"

)


# ============================================================
# GENERATE NEXT STUDENT ID
#
# STU00001
# STU00002
# STU00003
# ============================================================

def generate_student_registration_no():

    con = None
    cursor = None

    try:

        con = get_connection()

        cursor = con.cursor()


        cursor.execute(
            """
            SELECT Registration_No

            FROM registration

            WHERE Registration_No LIKE 'STU%'

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


        record = cursor.fetchone()


        if record is None:

            next_number = 1


        else:

            last_registration_no = str(
                record[0]
            )


            try:

                last_number = int(
                    last_registration_no[3:]
                )

            except ValueError:

                last_number = 0


            next_number = (
                last_number + 1
            )


        return (
            f"STU{next_number:05d}"
        )


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            (
                "Could not generate student ID.\n\n"
                f"{error}"
            )
        )

        return ""


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
# OPEN STUDENT FORM
# ============================================================

def open_student_form(
    parent,
    refresh_callback=None,
    student_id=None,
    mode=None,
    on_back=None,
    registration_no=None
):

    # ========================================================
    # SUPPORT DIFFERENT CALLING STYLES
    # ========================================================

    if (
        refresh_callback is None
        and on_back is not None
    ):

        refresh_callback = on_back


    if (
        student_id is None
        and registration_no is not None
    ):

        student_id = registration_no


    if mode is not None:

        mode = (
            str(mode)
            .strip()
            .lower()
        )


        if mode == "add":

            student_id = None


        elif (
            mode == "edit"
            and student_id is None
        ):

            messagebox.showerror(
                "Edit Student",
                (
                    "Registration number is required "
                    "to edit a student."
                )
            )

            return


    # ========================================================
    # EDIT MODE
    # ========================================================

    edit_mode = (
        student_id is not None
    )


    # ========================================================
    # CLEAR OLD PAGE
    # ========================================================

    for widget in parent.winfo_children():

        widget.destroy()


    # ========================================================
    # MAIN PAGE
    # ========================================================

    page = Frame(
        parent,
        bg=BACKGROUND
    )

    page.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # VARIABLES
    # ========================================================

    registration_var = StringVar()

    name_var = StringVar()

    username_var = StringVar()

    password_var = StringVar()

    security_question_var = StringVar()

    security_answer_var = StringVar()

    course_var = StringVar()

    semester_var = StringVar()

    admission_year_var = StringVar()

    email_var = StringVar()

    age_var = StringVar()

    gender_var = StringVar()

    phone_var = StringVar()

    status_var = StringVar(
        value="Inactive"
    )


    # ========================================================
    # COURSE DATA
    # ========================================================

    course_semester_map = {}


    # ========================================================
    # LOAD COURSES
    # ========================================================

    def load_courses_from_database(
        existing_course=None
    ):

        course_semester_map.clear()


        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()


            # =================================================
            # ACTIVE COURSES ONLY
            # =================================================

            cursor.execute(
                """
                SELECT
                    Course_Name,
                    Total_Semesters

                FROM courses

                WHERE LOWER(Status) = 'active'

                ORDER BY Course_Name ASC
                """
            )


            records = cursor.fetchall()


            for record in records:

                course_name = str(
                    record[0]
                ).strip()


                total_semesters = int(
                    record[1]
                )


                course_semester_map[
                    course_name
                ] = total_semesters


            # =================================================
            # KEEP OLD INACTIVE COURSE DURING EDIT
            # =================================================

            if (
                existing_course
                and
                existing_course
                not in course_semester_map
            ):

                cursor.execute(
                    """
                    SELECT
                        Course_Name,
                        Total_Semesters

                    FROM courses

                    WHERE Course_Name = %s

                    LIMIT 1
                    """,
                    (
                        existing_course,
                    )
                )


                existing_record = (
                    cursor.fetchone()
                )


                if existing_record:

                    existing_name = str(
                        existing_record[0]
                    ).strip()


                    existing_semesters = int(
                        existing_record[1]
                    )


                    course_semester_map[
                        existing_name
                    ] = existing_semesters


            return tuple(
                course_semester_map.keys()
            )


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load courses.\n\n"
                    f"{error}"
                )
            )

            return ()


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
    # BACK TO STUDENTS
    # ========================================================

    def back_to_students():

        disable_mouse_wheel()


        if refresh_callback is not None:

            refresh_callback()


    # ========================================================
    # BACK BUTTON
    # ========================================================

    Button(
        page,
        text="←  Back to Students",
        bg=BACKGROUND,
        fg=BLUE,
        activebackground=BACKGROUND,
        activeforeground=DARK_BLUE,
        font=(
            "Helvetica",
            10,
            "bold"
        ),
        bd=0,
        cursor="hand2",
        command=back_to_students
    ).place(
        relx=1.0,
        x=-35,
        y=32,
        anchor="ne"
    )


    # ========================================================
    # PAGE TITLE
    # ========================================================

    if edit_mode:

        form_title = "Edit Student"

        form_subtitle = (
            "Update student account, academic "
            "and personal information"
        )


    else:

        form_title = "Add Student"

        form_subtitle = (
            "Create a new student account "
            "with complete information"
        )


    Label(
        page,
        text=form_title,
        bg=BACKGROUND,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            22,
            "bold"
        )
    ).place(
        x=35,
        y=20
    )


    Label(
        page,
        text=form_subtitle,
        bg=BACKGROUND,
        fg=GRAY,
        font=(
            "Helvetica",
            10
        )
    ).place(
        x=37,
        y=60
    )


    # ========================================================
    # FORM CONTAINER
    # ========================================================

    form_container = Frame(
        page,
        bg=BACKGROUND
    )

    form_container.place(
        x=30,
        y=90,
        relwidth=1.0,
        width=-60,
        relheight=1.0,
        height=-110
    )


    # ========================================================
    # FORM CANVAS
    # ========================================================

    form_canvas = Canvas(
        form_container,
        bg=BACKGROUND,
        bd=0,
        highlightthickness=0
    )

    form_canvas.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # SCROLLBAR
    # ========================================================

    y_scrollbar = Scrollbar(
        form_container,
        orient=VERTICAL,
        command=form_canvas.yview
    )

    y_scrollbar.pack(
        side=RIGHT,
        fill=Y
    )


    form_canvas.configure(
        yscrollcommand=y_scrollbar.set
    )


    # ========================================================
    # FORM
    # ========================================================

    form = Frame(
        form_canvas,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )


    form_window = (
        form_canvas.create_window(
            (
                0,
                0
            ),
            window=form,
            anchor="nw"
        )
    )


    # ========================================================
    # RESIZE FORM
    # ========================================================

    def resize_form(
        event
    ):

        try:

            form_canvas.itemconfigure(
                form_window,
                width=event.width
            )

        except TclError:

            pass


    form_canvas.bind(
        "<Configure>",
        resize_form
    )


    # ========================================================
    # UPDATE SCROLL REGION
    # ========================================================

    def update_scroll_region(
        event=None
    ):

        try:

            if form_canvas.winfo_exists():

                form_canvas.configure(
                    scrollregion=(
                        form_canvas.bbox(
                            "all"
                        )
                    )
                )

        except TclError:

            pass


    form.bind(
        "<Configure>",
        update_scroll_region
    )


    # ========================================================
    # GRID CONFIGURATION
    # ========================================================

    form.grid_columnconfigure(
        0,
        weight=1
    )

    form.grid_columnconfigure(
        1,
        weight=1
    )


    # ========================================================
    # CREATE SECTION
    # ========================================================

    def create_section(
        title,
        subtitle,
        row
    ):

        section = Frame(
            form,
            bg=WHITE
        )

        section.grid(
            row=row,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=(
                22,
                8
            )
        )


        Label(
            section,
            text=title,
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                16,
                "bold"
            )
        ).pack(
            anchor="w"
        )


        Label(
            section,
            text=subtitle,
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                9
            )
        ).pack(
            anchor="w",
            pady=(
                5,
                12
            )
        )


        Frame(
            section,
            bg=BORDER,
            height=1
        ).pack(
            fill=X
        )


    # ========================================================
    # CREATE ENTRY FIELD
    # ========================================================

    def create_entry_field(
        label_text,
        variable,
        row,
        column,
        disabled=False,
        show=None
    ):

        field = Frame(
            form,
            bg=WHITE
        )

        field.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=(
                30
                if column == 0
                else 15,

                15
                if column == 0
                else 30
            ),
            pady=8
        )


        Label(
            field,
            text=label_text,
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            pady=(
                0,
                7
            )
        )


        entry = Entry(
            field,
            textvariable=variable,
            bg=(
                "#F1F5F9"
                if disabled
                else WHITE
            ),
            fg=(
                GRAY
                if disabled
                else TEXT_COLOR
            ),
            disabledbackground="#F1F5F9",
            disabledforeground=GRAY,
            font=(
                "Helvetica",
                11
            ),
            bd=0,
            highlightthickness=1,
            highlightbackground=INPUT_BORDER,
            highlightcolor=BLUE
        )


        if show is not None:

            entry.config(
                show=show
            )


        entry.pack(
            fill=X,
            ipady=9
        )


        if disabled:

            entry.config(
                state="disabled"
            )


        return entry


    # ========================================================
    # CREATE COMBOBOX
    # ========================================================

    def create_combobox_field(
        label_text,
        variable,
        values,
        row,
        column
    ):

        field = Frame(
            form,
            bg=WHITE
        )

        field.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=(
                30
                if column == 0
                else 15,

                15
                if column == 0
                else 30
            ),
            pady=8
        )


        Label(
            field,
            text=label_text,
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            pady=(
                0,
                7
            )
        )


        combo = ttk.Combobox(
            field,
            textvariable=variable,
            values=values,
            state="readonly",
            font=(
                "Helvetica",
                11
            )
        )

        combo.pack(
            fill=X,
            ipady=7
        )


        return combo


    # ========================================================
    # CREATE GENDER FIELD
    #
    # Gender*  ○ Male  ○ Female
    # ========================================================

    def create_gender_field(
        row,
        column
    ):

        field = Frame(
            form,
            bg=WHITE
        )

        field.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=(
                30
                if column == 0
                else 15,

                15
                if column == 0
                else 30
            ),
            pady=8
        )


        # ====================================================
        # SPACER TO ALIGN WITH PHONE FIELD
        # ====================================================

        Label(
            field,
            text="",
            bg=WHITE,
            font=(
                "Helvetica",
                9
            )
        ).pack(
            anchor="w",
            pady=(
                0,
                7
            )
        )


        # ====================================================
        # GENDER ROW
        # ====================================================

        gender_row = Frame(
            field,
            bg=WHITE,
            height=40
        )

        gender_row.pack(
            fill=X
        )

        gender_row.pack_propagate(
            False
        )


        # ====================================================
        # GENDER LABEL
        # ====================================================

        Label(
            gender_row,
            text="Gender*",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                10,
                "bold"
            )
        ).pack(
            side=LEFT
        )


        # ====================================================
        # MALE
        # ====================================================

        Radiobutton(
            gender_row,
            text="Male",
            variable=gender_var,
            value="Male",
            bg=WHITE,
            fg=TEXT_COLOR,
            activebackground=WHITE,
            activeforeground=TEXT_COLOR,
            selectcolor=WHITE,
            font=(
                "Helvetica",
                10
            ),
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        ).pack(
            side=LEFT,
            padx=(
                10,
                5
            )
        )


        # ====================================================
        # FEMALE
        # ====================================================

        Radiobutton(
            gender_row,
            text="Female",
            variable=gender_var,
            value="Female",
            bg=WHITE,
            fg=TEXT_COLOR,
            activebackground=WHITE,
            activeforeground=TEXT_COLOR,
            selectcolor=WHITE,
            font=(
                "Helvetica",
                10
            ),
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        ).pack(
            side=LEFT,
            padx=5
        )


    # ========================================================
    # ACCOUNT INFORMATION
    # ========================================================

    create_section(
        "Account Information",
        (
            "The registration number is automatically "
            "generated and cannot be changed."
        ),
        0
    )


    registration_entry = create_entry_field(
        "Registration Number",
        registration_var,
        1,
        0,
        disabled=True
    )


    name_entry = create_entry_field(
        "Full Name",
        name_var,
        1,
        1
    )


    username_entry = create_entry_field(
        "Username",
        username_var,
        2,
        0
    )


    password_entry = create_entry_field(
        "Password",
        password_var,
        2,
        1
    )


    # ========================================================
    # SECURITY INFORMATION
    # ========================================================

    create_section(
        "Security Information",
        (
            "Select a security question and enter "
            "the answer for account recovery."
        ),
        3
    )


    security_question_combo = (
        create_combobox_field(
            "Security Question",
            security_question_var,
            SECURITY_QUESTIONS,
            4,
            0
        )
    )


    security_answer_entry = (
        create_entry_field(
            "Security Answer",
            security_answer_var,
            4,
            1
        )
    )


    # ========================================================
    # ACADEMIC INFORMATION
    # ========================================================

    create_section(
        "Academic Information",
        (
            "Select the student's course "
            "and academic details."
        ),
        5
    )


    # ========================================================
    # LOAD COURSES
    # ========================================================

    course_values = (
        load_courses_from_database()
    )


    # ========================================================
    # COURSE
    # ========================================================

    course_combo = (
        create_combobox_field(
            "Course",
            course_var,
            course_values,
            6,
            0
        )
    )


    # ========================================================
    # SEMESTER
    # ========================================================

    semester_combo = (
        create_combobox_field(
            "Semester",
            semester_var,
            (),
            6,
            1
        )
    )


    # ========================================================
    # UPDATE SEMESTERS
    # ========================================================

    def update_semesters(
        clear_invalid=True
    ):

        selected_course = (
            course_var
            .get()
            .strip()
        )


        total_semesters = (
            course_semester_map.get(
                selected_course,
                0
            )
        )


        semester_values = tuple(

            str(i)

            for i in range(
                1,
                total_semesters + 1
            )

        )


        semester_combo.configure(
            values=semester_values
        )


        current_semester = (
            semester_var
            .get()
            .strip()
        )


        if (
            clear_invalid
            and
            current_semester
            not in semester_values
        ):

            semester_var.set(
                ""
            )


        return semester_values


    # ========================================================
    # COURSE CHANGED
    # ========================================================

    def on_course_changed(
        event=None
    ):

        semester_var.set(
            ""
        )

        update_semesters()


    course_combo.bind(
        "<<ComboboxSelected>>",
        on_course_changed
    )


    # ========================================================
    # ADMISSION YEAR
    # ========================================================

    current_year = datetime.now().year

    admission_session_values = tuple(
        f"{year}-{str(year + 1)[-2:]}"
        for year in range(1901, current_year + 2)
    )

    admission_year_combo = (
        create_combobox_field(
            "Admission Session",
            admission_year_var,
            admission_session_values,
            7,
            0
        )
    )


    # ========================================================
    # PERSONAL INFORMATION
    # ========================================================

    create_section(
        "Personal Information",
        (
            "Enter the student's personal "
            "and contact information."
        ),
        8
    )


    # ========================================================
    # EMAIL
    # ========================================================

    email_entry = (
        create_entry_field(
            "Email",
            email_var,
            9,
            0
        )
    )


    # ========================================================
    # AGE
    # ========================================================

    age_entry = (
        create_entry_field(
            "Age",
            age_var,
            9,
            1
        )
    )


    # ========================================================
    # GENDER
    # ========================================================

    create_gender_field(
        10,
        0
    )


    # ========================================================
    # PHONE
    # ========================================================

    phone_entry = (
        create_entry_field(
            "Phone",
            phone_var,
            10,
            1
        )
    )


    # ========================================================
    # VERIFICATION STATUS
    # ========================================================

    create_section(
        "Verification Status",
        (
            "New students are created as Inactive. "
            "An administrator can approve them after verification."
        ),
        11
    )


    # ========================================================
    # STATUS FIELD
    # ========================================================

    status_field = Frame(
        form,
        bg=WHITE
    )

    status_field.grid(
        row=12,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=30,
        pady=8
    )


    Label(
        status_field,
        text="Current Status",
        bg=WHITE,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            9,
            "bold"
        )
    ).pack(
        anchor="w",
        pady=(
            0,
            7
        )
    )


    status_display = Label(
        status_field,
        textvariable=status_var,
        bg="#FFF7ED",
        fg=ORANGE,
        font=(
            "Helvetica",
            10,
            "bold"
        ),
        anchor="w",
        padx=15,
        pady=10
    )

    status_display.pack(
        fill=X
    )


    # ========================================================
    # UPDATE STATUS COLOR
    # ========================================================

    def update_status_display():

        status = (
            status_var
            .get()
            .strip()
            .lower()
        )


        if status == "active":

            status_display.config(
                bg="#F0FDF4",
                fg=GREEN
            )


        elif status == "inactive":

            status_display.config(
                bg="#FEF2F2",
                fg=RED
            )


        else:

            status_display.config(
                bg="#FFF7ED",
                fg=ORANGE
            )


    # ========================================================
    # VALIDATE FORM
    # ========================================================

    def validate_form():

        name = (
            name_var
            .get()
            .strip()
        )


        username = (
            username_var
            .get()
            .strip()
        )


        password = (
            password_var
            .get()
            .strip()
        )


        security_question = (
            security_question_var
            .get()
            .strip()
        )


        security_answer = (
            security_answer_var
            .get()
            .strip()
        )


        course = (
            course_var
            .get()
            .strip()
        )


        semester = (
            semester_var
            .get()
            .strip()
        )


        admission_year = (
            admission_year_var
            .get()
            .strip()
        )


        email = (
            email_var
            .get()
            .strip()
        )


        age = (
            age_var
            .get()
            .strip()
        )


        gender = (
            gender_var
            .get()
            .strip()
        )


        phone = (
            phone_var
            .get()
            .strip()
        )


        # ====================================================
        # FULL NAME
        # ====================================================

        if name == "":

            messagebox.showwarning(
                "Required Field",
                "Please enter the student's full name."
            )

            return False


        # ====================================================
        # USERNAME
        # ====================================================

        if username == "":

            messagebox.showwarning(
                "Required Field",
                "Please enter the username."
            )

            return False


        # ====================================================
        # PASSWORD
        # ====================================================

        if password == "":

            messagebox.showwarning(
                "Required Field",
                "Please enter the password."
            )

            return False


        # ====================================================
        # SECURITY QUESTION
        # ====================================================

        if security_question == "":

            messagebox.showwarning(
                "Required Field",
                "Please select a security question."
            )

            return False


        if (
            security_question
            not in SECURITY_QUESTIONS
        ):

            messagebox.showwarning(
                "Invalid Security Question",
                (
                    "Please select a valid "
                    "security question."
                )
            )

            return False


        # ====================================================
        # SECURITY ANSWER
        # ====================================================

        if security_answer == "":

            messagebox.showwarning(
                "Required Field",
                "Please enter the security answer."
            )

            return False


        # ====================================================
        # COURSE
        # ====================================================

        if course == "":

            messagebox.showwarning(
                "Required Field",
                "Please select a course."
            )

            return False


        if course not in course_semester_map:

            messagebox.showerror(
                "Invalid Course",
                (
                    "The selected course could not "
                    "be found in the courses table."
                )
            )

            return False


        # ====================================================
        # SEMESTER
        # ====================================================

        if semester == "":

            messagebox.showwarning(
                "Required Field",
                "Please select a semester."
            )

            return False


        try:

            semester_number = int(
                semester
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Semester",
                "Please select a valid semester."
            )

            return False


        total_semesters = (
            course_semester_map[
                course
            ]
        )


        if not (
            1
            <= semester_number
            <= total_semesters
        ):

            messagebox.showwarning(
                "Invalid Semester",
                (
                    f"{course} has only "
                    f"{total_semesters} semesters."
                )
            )

            return False


        # ====================================================
        # ADMISSION YEAR
        # ====================================================

        if admission_year == "":

            messagebox.showwarning(
                "Required Field",
                "Please select the admission session."
            )

            return False


        if not re.fullmatch(
            r"\d{4}-\d{2}",
            admission_year
        ):

            messagebox.showwarning(
                "Invalid Admission Session",
                (
                    "Admission session must be in YYYY-YY format.\n"
                    "Example: 2025-26"
                )
            )

            return False


        start_year = int(
            admission_year[:4]
        )

        end_year = int(
            admission_year[-2:]
        )

        expected_end_year = (
            start_year + 1
        ) % 100

        current_year = (
            datetime.now().year
        )


        if (
            end_year != expected_end_year
            or start_year < 1901
            or start_year > current_year + 1
        ):

            messagebox.showwarning(
                "Invalid Admission Session",
                (
                    "Please select a valid admission session.\n"
                    "Example: 2025-26"
                )
            )

            return False


        # ====================================================
        # EMAIL
        # ====================================================

        if email == "":

            messagebox.showwarning(
                "Required Field",
                "Please enter the email address."
            )

            return False


        email_pattern = (
            r"^[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+"
            r"\.[A-Za-z]{2,}$"
        )


        if not re.fullmatch(
            email_pattern,
            email
        ):

            messagebox.showwarning(
                "Invalid Email",
                (
                    "Please enter a valid "
                    "email address."
                )
            )

            return False


        # ====================================================
        # AGE
        # ====================================================

        if age == "":

            messagebox.showwarning(
                "Required Field",
                "Please enter the student's age."
            )

            return False


        if not age.isdigit():

            messagebox.showwarning(
                "Invalid Age",
                "Age must contain only numbers."
            )

            return False


        age_number = int(
            age
        )


        if not (
            10
            <= age_number
            <= 100
        ):

            messagebox.showwarning(
                "Invalid Age",
                (
                    "Please enter a valid age "
                    "between 10 and 100."
                )
            )

            return False


        # ====================================================
        # GENDER
        # ====================================================

        if gender not in (
            "Male",
            "Female"
        ):

            messagebox.showwarning(
                "Invalid Gender",
                "Please select Male or Female."
            )

            return False


        # ====================================================
        # PHONE
        # ====================================================

        if phone == "":

            messagebox.showwarning(
                "Required Field",
                "Please enter the phone number."
            )

            return False


        if not phone.isdigit():

            messagebox.showwarning(
                "Invalid Phone",
                (
                    "Phone number must contain "
                    "only numbers."
                )
            )

            return False


        if len(phone) != 10:

            messagebox.showwarning(
                "Invalid Phone",
                (
                    "Phone number must contain "
                    "exactly 10 digits."
                )
            )

            return False


        return True


    # ========================================================
    # SAVE STUDENT
    # ========================================================

    def save_student():

        if not validate_form():

            return


        # ====================================================
        # CONFIRM UPDATE IN EDIT MODE
        # ====================================================

        if edit_mode:

            confirm_change = messagebox.askyesno(
                "Confirm Changes",
                (
                    "Do you want to save the changes made "
                    "to this student?\n\n"
                    f"Registration No: {student_id}"
                )
            )

            if not confirm_change:

                return


        # ====================================================
        # GET VALUES
        # ====================================================

        name = (
            name_var
            .get()
            .strip()
        )


        username = (
            username_var
            .get()
            .strip()
        )


        password = (
            password_var
            .get()
            .strip()
        )


        security_question = (
            security_question_var
            .get()
            .strip()
        )


        security_answer = (
            security_answer_var
            .get()
            .strip()
        )


        course = (
            course_var
            .get()
            .strip()
        )


        semester = int(
            semester_var
            .get()
        )


        admission_year = (
            admission_year_var
            .get()
            .strip()
        )


        email = (
            email_var
            .get()
            .strip()
        )


        age = int(
            age_var
            .get()
        )


        gender = (
            gender_var
            .get()
            .strip()
        )


        phone = (
            phone_var
            .get()
            .strip()
        )


        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()

            con.start_transaction()


            # =================================================
            # CHECK DUPLICATE USERNAME
            # =================================================

            if edit_mode:

                cursor.execute(
                    """
                    SELECT Registration_No

                    FROM registration

                    WHERE Username = %s

                    AND Registration_No <> %s

                    LIMIT 1
                    """,
                    (
                        username,
                        student_id
                    )
                )


            else:

                cursor.execute(
                    """
                    SELECT Registration_No

                    FROM registration

                    WHERE Username = %s

                    LIMIT 1
                    """,
                    (
                        username,
                    )
                )


            if cursor.fetchone():

                con.rollback()


                messagebox.showwarning(
                    "Duplicate Username",
                    (
                        "This username is already "
                        "used by another account."
                    )
                )

                return


            # =================================================
            # EDIT STUDENT
            # =================================================

            if edit_mode:

                # =============================================
                # UPDATE REGISTRATION
                # =============================================

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

                    AND LOWER(Role) = 'student'
                    """,
                    (
                        name,
                        username,
                        password,
                        security_question,
                        security_answer,
                        student_id
                    )
                )


                # =============================================
                # CHECK STUDENT DETAILS
                # =============================================

                cursor.execute(
                    """
                    SELECT Registration_No

                    FROM student_details

                    WHERE Registration_No = %s

                    LIMIT 1
                    """,
                    (
                        student_id,
                    )
                )


                details_exist = (
                    cursor.fetchone()
                )


                # =============================================
                # KEEP CURRENT STATUS
                # =============================================

                current_status = (
                    status_var
                    .get()
                    .strip()
                )


                if current_status == "":

                    current_status = (
                        "Inactive"
                    )


                # =============================================
                # UPDATE DETAILS
                # =============================================

                if details_exist:

                    cursor.execute(
                        """
                        UPDATE student_details

                        SET
                            Course = %s,
                            Semester = %s,
                            Admission_Year = %s,
                            Email = %s,
                            Age = %s,
                            Gender = %s,
                            Phone = %s,
                            Status = %s

                        WHERE Registration_No = %s
                        """,
                        (
                            course,
                            semester,
                            admission_year,
                            email,
                            age,
                            gender,
                            phone,
                            current_status,
                            student_id
                        )
                    )


                # =============================================
                # INSERT DETAILS IF MISSING
                # =============================================

                else:

                    cursor.execute(
                        """
                        INSERT INTO student_details
                        (
                            Registration_No,
                            Course,
                            Semester,
                            Admission_Year,
                            Email,
                            Age,
                            Gender,
                            Phone,
                            Status
                        )

                        VALUES
                        (
                            %s,
                            %s,
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
                            student_id,
                            course,
                            semester,
                            admission_year,
                            email,
                            age,
                            gender,
                            phone,
                            "Inactive"
                        )
                    )


                con.commit()


                messagebox.showinfo(
                    "Student Updated",
                    (
                        "Student information has been "
                        "updated successfully."
                    )
                )


            # =================================================
            # ADD NEW STUDENT
            # =================================================

            else:

                # =============================================
                # GENERATE FINAL STUDENT ID
                # =============================================

                registration_no = (
                    generate_student_registration_no()
                )


                if registration_no == "":

                    con.rollback()

                    return


                registration_var.set(
                    registration_no
                )


                # =============================================
                # INSERT REGISTRATION
                # =============================================

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
                        name,
                        username,
                        password,
                        security_question,
                        security_answer,
                        "Student"
                    )
                )


                # =============================================
                # INSERT STUDENT DETAILS
                #
                # ADMIN-CREATED STUDENT = INACTIVE
                # =============================================

                cursor.execute(
                    """
                    INSERT INTO student_details
                    (
                        Registration_No,
                        Course,
                        Semester,
                        Admission_Year,
                        Email,
                        Age,
                        Gender,
                        Phone,
                        Status
                    )

                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        'Inactive'
                    )
                    """,
                    (
                        registration_no,
                        course,
                        semester,
                        admission_year,
                        email,
                        age,
                        gender,
                        phone
                    )
                )


                con.commit()


                messagebox.showinfo(
                    "Student Added",
                    (
                        "Student added successfully.\n\n"
                        f"Registration No: {registration_no}\n"
                        "Status: Inactive"
                    )
                )


            # =================================================
            # RETURN TO STUDENT PAGE
            # =================================================

            if refresh_callback is not None:

                disable_mouse_wheel()

                refresh_callback()


        except mysql.connector.IntegrityError as error:

            if con is not None:

                try:
                    con.rollback()

                except:
                    pass


            messagebox.showerror(
                "Database Error",
                (
                    "Could not save the student.\n\n"
                    f"{error}"
                )
            )


        except mysql.connector.Error as error:

            if con is not None:

                try:
                    con.rollback()

                except:
                    pass


            messagebox.showerror(
                "Database Error",
                str(error)
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
    # APPROVE STUDENT
    # ========================================================

    def approve_student():

        if not edit_mode:

            return


        # ====================================================
        # ALREADY ACTIVE
        # ====================================================

        current_status = (
            status_var
            .get()
            .strip()
            .lower()
        )


        if current_status == "active":

            messagebox.showinfo(
                "Already Approved",
                "This student is already active."
            )

            return


        # ====================================================
        # VALIDATE FORM BEFORE APPROVAL
        # ====================================================

        if not validate_form():

            return


        # ====================================================
        # CONFIRM APPROVAL
        # ====================================================

        confirm = messagebox.askyesno(
            "Approve Student",
            (
                "Are you sure you want to approve "
                "this student?\n\n"

                f"Registration No: {student_id}\n\n"

                "The student status will change "
                "to Active."
            )
        )


        if not confirm:

            return


        # ====================================================
        # GET FORM VALUES
        # ====================================================

        name = (
            name_var
            .get()
            .strip()
        )


        username = (
            username_var
            .get()
            .strip()
        )


        password = (
            password_var
            .get()
            .strip()
        )


        security_question = (
            security_question_var
            .get()
            .strip()
        )


        security_answer = (
            security_answer_var
            .get()
            .strip()
        )


        course = (
            course_var
            .get()
            .strip()
        )


        semester = int(
            semester_var
            .get()
        )


        admission_year = (
            admission_year_var
            .get()
            .strip()
        )


        email = (
            email_var
            .get()
            .strip()
        )


        age = int(
            age_var
            .get()
        )


        gender = (
            gender_var
            .get()
            .strip()
        )


        phone = (
            phone_var
            .get()
            .strip()
        )


        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()

            con.start_transaction()


            # =================================================
            # DUPLICATE USERNAME CHECK
            # =================================================

            cursor.execute(
                """
                SELECT Registration_No

                FROM registration

                WHERE Username = %s

                AND Registration_No <> %s

                LIMIT 1
                """,
                (
                    username,
                    student_id
                )
            )


            if cursor.fetchone():

                con.rollback()


                messagebox.showwarning(
                    "Duplicate Username",
                    (
                        "This username is already "
                        "used by another account."
                    )
                )

                return


            # =================================================
            # UPDATE ACCOUNT INFORMATION
            # =================================================

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

                AND LOWER(Role) = 'student'
                """,
                (
                    name,
                    username,
                    password,
                    security_question,
                    security_answer,
                    student_id
                )
            )


            # =================================================
            # CHECK DETAILS EXISTS
            # =================================================

            cursor.execute(
                """
                SELECT Registration_No

                FROM student_details

                WHERE Registration_No = %s

                LIMIT 1
                """,
                (
                    student_id,
                )
            )


            details_exist = (
                cursor.fetchone()
            )


            # =================================================
            # UPDATE AND APPROVE
            # =================================================

            if details_exist:

                cursor.execute(
                    """
                    UPDATE student_details

                    SET
                        Course = %s,
                        Semester = %s,
                        Admission_Year = %s,
                        Email = %s,
                        Age = %s,
                        Gender = %s,
                        Phone = %s,
                        Status = 'Active'

                    WHERE Registration_No = %s
                    """,
                    (
                        course,
                        semester,
                        admission_year,
                        email,
                        age,
                        gender,
                        phone,
                        student_id
                    )
                )


            # =================================================
            # CREATE DETAILS AND APPROVE
            # =================================================

            else:

                cursor.execute(
                    """
                    INSERT INTO student_details
                    (
                        Registration_No,
                        Course,
                        Semester,
                        Admission_Year,
                        Email,
                        Age,
                        Gender,
                        Phone,
                        Status
                    )

                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        'Active'
                    )
                    """,
                    (
                        student_id,
                        course,
                        semester,
                        admission_year,
                        email,
                        age,
                        gender,
                        phone
                    )
                )


            con.commit()


            # =================================================
            # UPDATE UI STATUS
            # =================================================

            status_var.set(
                "Active"
            )


            update_status_display()


            update_approve_button()


            messagebox.showinfo(
                "Student Approved",
                (
                    "Student approved successfully.\n\n"
                    f"Registration No: {student_id}\n"
                    "Status: Active"
                )
            )


        except mysql.connector.Error as error:

            if con is not None:

                try:
                    con.rollback()

                except:
                    pass


            messagebox.showerror(
                "Database Error",
                (
                    "Could not approve the student.\n\n"
                    f"{error}"
                )
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
    # BUTTON AREA
    # ========================================================

    button_frame = Frame(
        form,
        bg=WHITE,
        height=100
    )

    button_frame.grid(
        row=13,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=30,
        pady=(
            20,
            25
        )
    )

    button_frame.pack_propagate(
        False
    )


    # ========================================================
    # CANCEL BUTTON
    # ========================================================

    cancel_button = Button(
        button_frame,
        text="CANCEL",
        bg="#F1F5F9",
        fg=TEXT_COLOR,
        activebackground="#E2E8F0",
        activeforeground=TEXT_COLOR,
        font=(
            "Helvetica",
            10,
            "bold"
        ),
        bd=0,
        cursor="hand2",
        command=back_to_students
    )

    cancel_button.pack(
        side=RIGHT,
        padx=(
            10,
            0
        ),
        pady=20,
        ipadx=25,
        ipady=10
    )


    # ========================================================
    # ADD / UPDATE BUTTON
    # ========================================================

    if edit_mode:

        save_button_text = (
            "UPDATE STUDENT"
        )


    else:

        save_button_text = (
            "ADD STUDENT"
        )


    save_button = Button(
        button_frame,
        text=save_button_text,
        bg=BLUE,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        font=(
            "Helvetica",
            10,
            "bold"
        ),
        bd=0,
        cursor="hand2",
        command=save_student
    )

    save_button.pack(
        side=RIGHT,
        pady=20,
        ipadx=25,
        ipady=10
    )


    # ========================================================
    # APPROVE BUTTON
    # ========================================================

    approve_button = None


    if edit_mode:

        approve_button = Button(
            button_frame,
            text="APPROVE STUDENT",
            bg=GREEN,
            fg=WHITE,
            activebackground=DARK_GREEN,
            activeforeground=WHITE,
            font=(
                "Helvetica",
                10,
                "bold"
            ),
            bd=0,
            cursor="hand2",
            command=approve_student
        )


    # ========================================================
    # UPDATE APPROVE BUTTON VISIBILITY
    #
    # INACTIVE   -> SHOW
    # INCOMPLETE -> SHOW
    # ACTIVE     -> HIDE
    # ========================================================

    def update_approve_button():

        if not edit_mode:

            return


        if approve_button is None:

            return


        current_status = (
            status_var
            .get()
            .strip()
            .lower()
        )


        # ====================================================
        # REMOVE OLD POSITION
        # ====================================================

        approve_button.pack_forget()


        # ====================================================
        # SHOW APPROVE BUTTON
        # ====================================================

        if current_status in (
            "inactive",
            "incomplete"
        ):

            approve_button.pack(
                side=RIGHT,
                before=save_button,
                padx=(
                    0,
                    10
                ),
                pady=20,
                ipadx=25,
                ipady=10
            )


    # ========================================================
    # LOAD STUDENT DATA
    # ========================================================

    def load_student_data():

        if not edit_mode:

            return


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

                    r.Username,

                    r.Password,

                    r.Security_Question,

                    r.Security_Answer,

                    s.Course,

                    s.Semester,

                    s.Admission_Year,

                    s.Email,

                    s.Age,

                    s.Gender,

                    s.Phone,

                    COALESCE(
                        s.Status,
                        'Incomplete'
                    )

                FROM registration r

                LEFT JOIN student_details s

                ON
                    r.Registration_No
                    =
                    s.Registration_No

                WHERE
                    r.Registration_No = %s

                AND
                    LOWER(r.Role) = 'student'

                LIMIT 1
                """,
                (
                    student_id,
                )
            )


            student = (
                cursor.fetchone()
            )


            if student is None:

                messagebox.showerror(
                    "Student Not Found",
                    (
                        "The selected student "
                        "could not be found."
                    )
                )

                back_to_students()

                return


            # =================================================
            # EXISTING COURSE
            # =================================================

            existing_course = (

                student[6]

                if student[6] is not None

                else ""

            )


            existing_semester = (

                str(
                    student[7]
                )

                if student[7] is not None

                else ""

            )


            # =================================================
            # RELOAD COURSES
            # =================================================

            course_values_for_edit = (
                load_courses_from_database(
                    existing_course=existing_course
                )
            )


            course_combo.configure(
                values=course_values_for_edit
            )


            # =================================================
            # SET ACCOUNT DATA
            # =================================================

            registration_var.set(
                student[0] or ""
            )


            name_var.set(
                student[1] or ""
            )


            username_var.set(
                student[2] or ""
            )


            password_var.set(
                student[3] or ""
            )


            # =================================================
            # SET SECURITY DATA
            # =================================================

            security_question_var.set(
                student[4] or ""
            )


            security_answer_var.set(
                student[5] or ""
            )


            # =================================================
            # SET COURSE
            # =================================================

            course_var.set(
                existing_course
            )


            valid_semesters = (
                update_semesters(
                    clear_invalid=False
                )
            )


            if (
                existing_semester
                in valid_semesters
            ):

                semester_var.set(
                    existing_semester
                )


            else:

                semester_var.set(
                    ""
                )


            # =================================================
            # SET ADMISSION YEAR
            # =================================================

            admission_year_var.set(

                str(
                    student[8]
                )

                if student[8] is not None

                else ""

            )


            # =================================================
            # SET EMAIL
            # =================================================

            email_var.set(
                student[9] or ""
            )


            # =================================================
            # SET AGE
            # =================================================

            age_var.set(

                str(
                    student[10]
                )

                if student[10] is not None

                else ""

            )


            # =================================================
            # SET GENDER
            # =================================================

            gender_var.set(
                student[11] or ""
            )


            # =================================================
            # SET PHONE
            # =================================================

            phone_var.set(
                student[12] or ""
            )


            # =================================================
            # SET STATUS
            # =================================================

            status_var.set(
                student[13] or "Incomplete"
            )


            # =================================================
            # UPDATE STATUS DESIGN
            # =================================================

            update_status_display()


            # =================================================
            # SHOW / HIDE APPROVE BUTTON
            # =================================================

            update_approve_button()


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load student information.\n\n"
                    f"{error}"
                )
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
    # SAFE MOUSE WHEEL
    # ========================================================

    def mouse_wheel_scroll(
        event
    ):

        try:

            if (
                form_canvas.winfo_exists()
                and event.delta
            ):

                form_canvas.yview_scroll(
                    int(
                        -1
                        * (
                            event.delta / 120
                        )
                    ),
                    "units"
                )

        except TclError:

            pass


        return "break"


    # ========================================================
    # ENABLE MOUSE WHEEL
    # ========================================================

    def enable_mouse_wheel(
        event=None
    ):

        try:

            if form_canvas.winfo_exists():

                form_canvas.bind_all(
                    "<MouseWheel>",
                    mouse_wheel_scroll
                )

        except TclError:

            pass


    # ========================================================
    # DISABLE MOUSE WHEEL
    # ========================================================

    # ========================================================
    # PREVENT COMBOBOX VALUE CHANGE WHILE MOUSE-WHEEL SCROLLING
    #
    # Without this binding, a readonly ttk.Combobox can change
    # its selected value when the user scrolls over it.
    # The wheel is redirected to the form canvas instead.
    # ========================================================

    def combobox_mouse_wheel(
        event
    ):

        return mouse_wheel_scroll(
            event
        )


    for combo_widget in (
        security_question_combo,
        course_combo,
        semester_combo
    ):

        combo_widget.bind(
            "<MouseWheel>",
            combobox_mouse_wheel
        )

        combo_widget.bind(
            "<Button-4>",
            lambda event: "break"
        )

        combo_widget.bind(
            "<Button-5>",
            lambda event: "break"
        )


    def disable_mouse_wheel(
        event=None
    ):

        try:

            form_canvas.unbind_all(
                "<MouseWheel>"
            )

        except TclError:

            pass


    form_container.bind(
        "<Enter>",
        enable_mouse_wheel
    )


    form_container.bind(
        "<Leave>",
        disable_mouse_wheel
    )


    # ========================================================
    # INITIALIZE FORM
    # ========================================================

    if edit_mode:

        load_student_data()


    else:

        # ====================================================
        # AUTO-GENERATE STUDENT ID
        # ====================================================

        generated_registration_no = (
            generate_student_registration_no()
        )


        registration_var.set(
            generated_registration_no
        )


        # ====================================================
        # DEFAULT STATUS
        # ====================================================

        status_var.set(
            "Inactive"
        )


        # ====================================================
        # DEFAULT ADMISSION YEAR
        # ====================================================

        admission_year_var.set(
            str(
                datetime.now().year
            )
        )


        update_status_display()


    # ========================================================
    # UPDATE SCROLL REGION
    # ========================================================

    form.update_idletasks()

    update_scroll_region()


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

def show_student_form(
    parent,
    mode="add",
    registration_no=None,
    on_back=None
):

    open_student_form(
        parent=parent,
        mode=mode,
        registration_no=registration_no,
        on_back=on_back
    )