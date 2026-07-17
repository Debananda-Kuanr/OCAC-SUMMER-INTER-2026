from tkinter import *
from tkinter import messagebox
import mysql.connector

from student_form import open_student_form


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
TABLE_HEADER = "#F1F5F9"

GREEN = "#16A34A"
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
# SHOW STUDENT PAGE
# ============================================================

def show_student_page(parent):

    # ========================================================
    # CLEAR OLD CONTENT
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
    # PAGE HEADER
    # ========================================================

    header_frame = Frame(
        page,
        bg=BACKGROUND,
        height=95
    )

    header_frame.pack(
        fill=X
    )

    header_frame.pack_propagate(
        False
    )


    # ========================================================
    # TITLE
    # ========================================================

    title_label = Label(
        header_frame,
        text="Students",
        bg=BACKGROUND,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            22,
            "bold"
        )
    )

    title_label.place(
        x=30,
        y=20
    )


    # ========================================================
    # SUBTITLE
    # ========================================================

    subtitle_label = Label(
        header_frame,
        text="Manage student accounts, profiles and verification status",
        bg=BACKGROUND,
        fg=GRAY,
        font=(
            "Helvetica",
            10
        )
    )

    subtitle_label.place(
        x=32,
        y=60
    )


    # ========================================================
    # ADD STUDENT
    # ========================================================

    def add_student():

        disable_mouse_scroll()

        open_student_form(
            parent,
            mode="add",
            on_back=lambda: show_student_page(
                parent
            )
        )


    # ========================================================
    # ADD STUDENT BUTTON
    # ========================================================

    add_button = Button(
        header_frame,
        text="+  ADD STUDENT",
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
        command=add_student
    )

    add_button.place(
        relx=1.0,
        x=-30,
        y=28,
        width=145,
        height=40,
        anchor="ne"
    )


    # ========================================================
    # SEARCH SECTION
    # ========================================================

    search_frame = Frame(
        page,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1,
        height=75
    )

    search_frame.pack(
        fill=X,
        padx=30,
        pady=(
            0,
            15
        )
    )

    search_frame.pack_propagate(
        False
    )


    # ========================================================
    # SEARCH ENTRY
    # ========================================================

    search_entry = Entry(
        search_frame,
        font=(
            "Helvetica",
            11
        ),
        fg=TEXT_COLOR,
        bg=WHITE,
        bd=0,
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor=BLUE
    )

    search_entry.place(
        x=20,
        y=17,
        relwidth=1.0,
        width=-275,
        height=40
    )


    # ========================================================
    # SEARCH PLACEHOLDER
    # ========================================================

    PLACEHOLDER = (
        "Search by ID, name, username, course, email, phone or status..."
    )


    def set_placeholder():

        if search_entry.get() == "":

            search_entry.insert(
                0,
                PLACEHOLDER
            )

            search_entry.config(
                fg=LIGHT_GRAY
            )


    def remove_placeholder(
        event=None
    ):

        if search_entry.get() == PLACEHOLDER:

            search_entry.delete(
                0,
                END
            )

            search_entry.config(
                fg=TEXT_COLOR
            )


    def restore_placeholder(
        event=None
    ):

        if search_entry.get().strip() == "":

            set_placeholder()


    set_placeholder()


    search_entry.bind(
        "<FocusIn>",
        remove_placeholder
    )

    search_entry.bind(
        "<FocusOut>",
        restore_placeholder
    )


    # ========================================================
    # TABLE CARD
    # ========================================================

    table_card = Frame(
        page,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    table_card.pack(
        fill=BOTH,
        expand=True,
        padx=30,
        pady=(
            0,
            25
        )
    )


    # ========================================================
    # TABLE TOP
    # ========================================================

    table_top = Frame(
        table_card,
        bg=WHITE,
        height=50
    )

    table_top.pack(
        fill=X
    )

    table_top.pack_propagate(
        False
    )


    # ========================================================
    # STUDENT COUNT
    # ========================================================

    count_label = Label(
        table_top,
        text="0 Students",
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            9,
            "bold"
        )
    )

    count_label.place(
        x=18,
        y=17
    )


    # ========================================================
    # SCROLL INFORMATION
    # ========================================================

    scroll_info = Label(
        table_top,
        text="Scroll horizontally to view all student details",
        bg=WHITE,
        fg=LIGHT_GRAY,
        font=(
            "Helvetica",
            8
        )
    )

    scroll_info.place(
        relx=1.0,
        x=-18,
        y=17,
        anchor="ne"
    )


    # ========================================================
    # TABLE CONTAINER
    # ========================================================

    table_container = Frame(
        table_card,
        bg=WHITE
    )

    table_container.pack(
        fill=BOTH,
        expand=True,
        padx=10,
        pady=(
            0,
            10
        )
    )


    # ========================================================
    # MAIN TABLE CANVAS
    # ========================================================

    table_canvas = Canvas(
        table_container,
        bg=WHITE,
        highlightthickness=0
    )

    table_canvas.grid(
        row=0,
        column=0,
        sticky="nsew"
    )


    # ========================================================
    # VERTICAL SCROLLBAR
    # ========================================================

    y_scrollbar = Scrollbar(
        table_container,
        orient=VERTICAL,
        command=table_canvas.yview
    )

    y_scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )


    # ========================================================
    # HORIZONTAL SCROLLBAR
    # ========================================================

    x_scrollbar = Scrollbar(
        table_container,
        orient=HORIZONTAL,
        command=table_canvas.xview
    )

    x_scrollbar.grid(
        row=1,
        column=0,
        sticky="ew"
    )


    # ========================================================
    # CONFIGURE GRID
    # ========================================================

    table_container.grid_rowconfigure(
        0,
        weight=1
    )

    table_container.grid_columnconfigure(
        0,
        weight=1
    )


    # ========================================================
    # CONNECT SCROLLBARS
    # ========================================================

    table_canvas.configure(
        yscrollcommand=y_scrollbar.set,
        xscrollcommand=x_scrollbar.set
    )


    # ========================================================
    # COMPLETE TABLE FRAME
    # ========================================================

    table_frame = Frame(
        table_canvas,
        bg=WHITE
    )

    table_canvas.create_window(
        (
            0,
            0
        ),
        window=table_frame,
        anchor="nw"
    )


    # ========================================================
    # TABLE WIDTH
    # ========================================================

    TABLE_WIDTH = 1690


    table_frame.config(
        width=TABLE_WIDTH
    )


    # ========================================================
    # TABLE HEADER
    # ========================================================

    table_header = Frame(
        table_frame,
        bg=TABLE_HEADER,
        width=TABLE_WIDTH,
        height=48
    )

    table_header.pack(
        fill=X
    )

    table_header.pack_propagate(
        False
    )


    # ========================================================
    # COLUMN WIDTHS
    # ========================================================

    COLUMN_WIDTHS = {

        "registration": 135,

        "name": 165,

        "username": 135,

        "course": 175,

        "semester": 85,

        "year": 115,

        "email": 210,

        "age": 70,

        "gender": 90,

        "phone": 130,

        "status": 105,

        "actions": 175

    }


    # ========================================================
    # HEADER COLUMN
    # ========================================================

    def header_column(
        text,
        width
    ):

        frame = Frame(
            table_header,
            bg=TABLE_HEADER,
            width=width,
            height=48
        )

        frame.pack(
            side=LEFT
        )

        frame.pack_propagate(
            False
        )


        label = Label(
            frame,
            text=text,
            bg=TABLE_HEADER,
            fg=GRAY,
            font=(
                "Helvetica",
                8,
                "bold"
            ),
            anchor="w"
        )

        label.pack(
            fill=BOTH,
            expand=True,
            padx=10
        )


    # ========================================================
    # CREATE TABLE HEADERS
    # ========================================================

    header_column(
        "REGISTRATION NO.",
        COLUMN_WIDTHS["registration"]
    )

    header_column(
        "NAME",
        COLUMN_WIDTHS["name"]
    )

    header_column(
        "USERNAME",
        COLUMN_WIDTHS["username"]
    )

    header_column(
        "COURSE",
        COLUMN_WIDTHS["course"]
    )

    header_column(
        "SEMESTER",
        COLUMN_WIDTHS["semester"]
    )

    header_column(
        "ADMISSION YEAR",
        COLUMN_WIDTHS["year"]
    )

    header_column(
        "EMAIL",
        COLUMN_WIDTHS["email"]
    )

    header_column(
        "AGE",
        COLUMN_WIDTHS["age"]
    )

    header_column(
        "GENDER",
        COLUMN_WIDTHS["gender"]
    )

    header_column(
        "PHONE",
        COLUMN_WIDTHS["phone"]
    )

    header_column(
        "STATUS",
        COLUMN_WIDTHS["status"]
    )

    header_column(
        "ACTIONS",
        COLUMN_WIDTHS["actions"]
    )


    # ========================================================
    # ROWS FRAME
    # ========================================================

    rows_frame = Frame(
        table_frame,
        bg=WHITE,
        width=TABLE_WIDTH
    )

    rows_frame.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # UPDATE SCROLL REGION
    # ========================================================

    def update_scroll_region(
        event=None
    ):

        # Prevent TclError if page has already been destroyed

        if not table_canvas.winfo_exists():
            return

        try:

            table_canvas.configure(
                scrollregion=table_canvas.bbox(
                    "all"
                )
            )

        except TclError:

            pass


    table_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    rows_frame.bind(
        "<Configure>",
        update_scroll_region
    )


    # ========================================================
    # SAFE MOUSE WHEEL SCROLLING
    # ========================================================

    def mouse_wheel_y(
        event
    ):

        try:

            if (
                table_canvas.winfo_exists()
                and event.delta
            ):

                table_canvas.yview_scroll(
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
    # SAFE HORIZONTAL SCROLLING
    # ========================================================

    def mouse_wheel_x(
        event
    ):

        try:

            if (
                table_canvas.winfo_exists()
                and event.delta
            ):

                table_canvas.xview_scroll(
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
    # ENABLE MOUSE SCROLLING
    # ========================================================

    def enable_mouse_scroll(
        event=None
    ):

        try:

            if table_canvas.winfo_exists():

                table_canvas.bind_all(
                    "<MouseWheel>",
                    mouse_wheel_y
                )

                table_canvas.bind_all(
                    "<Shift-MouseWheel>",
                    mouse_wheel_x
                )

        except TclError:

            pass


    # ========================================================
    # DISABLE MOUSE SCROLLING
    # ========================================================

    def disable_mouse_scroll(
        event=None
    ):

        try:

            table_canvas.unbind_all(
                "<MouseWheel>"
            )

            table_canvas.unbind_all(
                "<Shift-MouseWheel>"
            )

        except TclError:

            pass


    # ========================================================
    # ACTIVATE SCROLLING
    # ========================================================

    table_container.bind(
        "<Enter>",
        enable_mouse_scroll
    )

    table_container.bind(
        "<Leave>",
        disable_mouse_scroll
    )


    # ========================================================
    # EDIT STUDENT
    # ========================================================

    def edit_student(
        registration_no
    ):

        disable_mouse_scroll()

        open_student_form(
            parent,
            mode="edit",
            registration_no=registration_no,
            on_back=lambda: show_student_page(
                parent
            )
        )


    # ========================================================
    # DELETE STUDENT
    # ========================================================

    def delete_student(
        registration_no,
        student_name
    ):

        confirm = messagebox.askyesno(
            "Delete Student",
            (
                f"Are you sure you want to delete "
                f"{student_name}?\n\n"

                f"Registration No: "
                f"{registration_no}\n\n"

                "This will delete the student account "
                "and student profile.\n\n"

                "This action cannot be undone."
            )
        )


        if not confirm:

            return


        con = None

        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()

            con.start_transaction()


            # ------------------------------------------------
            # DELETE STUDENT DETAILS FIRST
            # ------------------------------------------------

            cursor.execute(
                """
                DELETE FROM student_details

                WHERE Registration_No = %s
                """,
                (
                    registration_no,
                )
            )


            # ------------------------------------------------
            # DELETE REGISTRATION ACCOUNT
            # ------------------------------------------------

            cursor.execute(
                """
                DELETE FROM registration

                WHERE Registration_No = %s

                AND LOWER(Role) = 'student'
                """,
                (
                    registration_no,
                )
            )


            con.commit()


            messagebox.showinfo(
                "Student Deleted",
                (
                    f"{student_name} "
                    "has been deleted successfully."
                )
            )


            load_students()


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
    # CREATE NORMAL TABLE CELL
    # ========================================================

    def create_cell(
        row,
        text,
        width,
        color=TEXT_COLOR,
        bold=False
    ):

        cell_frame = Frame(
            row,
            bg=WHITE,
            width=width,
            height=58
        )

        cell_frame.pack(
            side=LEFT
        )

        cell_frame.pack_propagate(
            False
        )


        if bold:

            cell_font = (
                "Helvetica",
                9,
                "bold"
            )

        else:

            cell_font = (
                "Helvetica",
                9
            )


        cell_label = Label(
            cell_frame,
            text=text,
            bg=WHITE,
            fg=color,
            font=cell_font,
            anchor="w"
        )

        cell_label.pack(
            fill=BOTH,
            expand=True,
            padx=10
        )


    # ========================================================
    # CREATE STUDENT ROW
    # ========================================================

    def create_student_row(
        student
    ):

        # ----------------------------------------------------
        # GET VALUES
        # ----------------------------------------------------

        registration_no = student[0]

        student_name = student[1]

        username = student[2]

        course = student[3]

        semester = student[4]

        admission_year = student[5]

        email = student[6]

        age = student[7]

        gender = student[8]

        phone = student[9]

        status = student[10]


        # ----------------------------------------------------
        # HANDLE NULL VALUES
        # ----------------------------------------------------

        registration_no = (
            str(registration_no)
            if registration_no
            else "-"
        )


        student_name = (
            str(student_name)
            if student_name
            else "-"
        )


        username = (
            str(username)
            if username
            else "-"
        )


        course_display = (
            str(course)
            if course
            else "Not Assigned"
        )


        semester_display = (
            str(semester)
            if semester is not None
            else "-"
        )


        year_display = (
            str(admission_year)
            if admission_year is not None
            else "-"
        )


        email_display = (
            str(email)
            if email
            else "-"
        )


        age_display = (
            str(age)
            if age is not None
            else "-"
        )


        gender_display = (
            str(gender)
            if gender
            else "-"
        )


        phone_display = (
            str(phone)
            if phone
            else "-"
        )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if status is None or str(
            status
        ).strip() == "":

            status_display = "Incomplete"

        else:

            status_display = str(
                status
            )


        # ====================================================
        # ROW FRAME
        # ====================================================

        row = Frame(
            rows_frame,
            bg=WHITE,
            width=TABLE_WIDTH,
            height=59
        )

        row.pack(
            fill=X
        )

        row.pack_propagate(
            False
        )


        # ====================================================
        # REGISTRATION NUMBER
        # ====================================================

        create_cell(
            row,
            registration_no,
            COLUMN_WIDTHS["registration"],
            BLUE,
            True
        )


        # ====================================================
        # NAME
        # ====================================================

        create_cell(
            row,
            student_name,
            COLUMN_WIDTHS["name"],
            TEXT_COLOR,
            True
        )


        # ====================================================
        # USERNAME
        # ====================================================

        create_cell(
            row,
            username,
            COLUMN_WIDTHS["username"]
        )


        # ====================================================
        # COURSE
        # ====================================================

        create_cell(
            row,
            course_display,
            COLUMN_WIDTHS["course"]
        )


        # ====================================================
        # SEMESTER
        # ====================================================

        create_cell(
            row,
            semester_display,
            COLUMN_WIDTHS["semester"]
        )


        # ====================================================
        # ADMISSION YEAR
        # ====================================================

        create_cell(
            row,
            year_display,
            COLUMN_WIDTHS["year"]
        )


        # ====================================================
        # EMAIL
        # ====================================================

        create_cell(
            row,
            email_display,
            COLUMN_WIDTHS["email"]
        )


        # ====================================================
        # AGE
        # ====================================================

        create_cell(
            row,
            age_display,
            COLUMN_WIDTHS["age"]
        )


        # ====================================================
        # GENDER
        # ====================================================

        create_cell(
            row,
            gender_display,
            COLUMN_WIDTHS["gender"]
        )


        # ====================================================
        # PHONE
        # ====================================================

        create_cell(
            row,
            phone_display,
            COLUMN_WIDTHS["phone"]
        )


        # ====================================================
        # STATUS COLOR
        # ====================================================

        if status_display.lower() == "active":

            status_color = GREEN


        elif status_display.lower() == "inactive":

            status_color = RED


        else:

            status_color = ORANGE


        # ====================================================
        # STATUS
        # ====================================================

        create_cell(
            row,
            status_display,
            COLUMN_WIDTHS["status"],
            status_color,
            True
        )


        # ====================================================
        # ACTION CELL
        # ====================================================

        action_frame = Frame(
            row,
            bg=WHITE,
            width=COLUMN_WIDTHS["actions"],
            height=58
        )

        action_frame.pack(
            side=LEFT
        )

        action_frame.pack_propagate(
            False
        )


        # ====================================================
        # EDIT BUTTON
        # ====================================================

        edit_button = Button(
            action_frame,
            text="Edit",
            bg="#EFF6FF",
            fg=BLUE,
            activebackground="#DBEAFE",
            activeforeground=DARK_BLUE,
            font=(
                "Helvetica",
                8,
                "bold"
            ),
            bd=0,
            cursor="hand2",
            command=lambda student_id=registration_no: (
                edit_student(
                    student_id
                )
            )
        )

        edit_button.place(
            x=10,
            y=13,
            width=60,
            height=30
        )


        # ====================================================
        # DELETE BUTTON
        # ====================================================

        delete_button = Button(
            action_frame,
            text="Delete",
            bg="#FEF2F2",
            fg=RED,
            activebackground="#FEE2E2",
            activeforeground=RED,
            font=(
                "Helvetica",
                8,
                "bold"
            ),
            bd=0,
            cursor="hand2",
            command=lambda student_id=registration_no,
            name=student_name: (
                delete_student(
                    student_id,
                    name
                )
            )
        )

        delete_button.place(
            x=80,
            y=13,
            width=70,
            height=30
        )


        # ====================================================
        # BOTTOM BORDER
        # ====================================================

        bottom_border = Frame(
            row,
            bg="#F1F5F9"
        )

        bottom_border.place(
            x=0,
            y=58,
            width=TABLE_WIDTH,
            height=1
        )


    # ========================================================
    # CLEAR TABLE ROWS
    # ========================================================

    def clear_rows():

        for widget in rows_frame.winfo_children():

            widget.destroy()


    # ========================================================
    # EMPTY MESSAGE
    # ========================================================

    def show_empty_message(
        message
    ):

        empty_frame = Frame(
            rows_frame,
            bg=WHITE,
            width=TABLE_WIDTH,
            height=180
        )

        empty_frame.pack(
            fill=X
        )

        empty_frame.pack_propagate(
            False
        )


        empty_label = Label(
            empty_frame,
            text=message,
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                11
            )
        )

        empty_label.place(
            x=30,
            y=70
        )


    # ========================================================
    # LOAD STUDENTS
    # ========================================================

    def load_students(
        search_text=""
    ):

        clear_rows()


        con = None

        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()


            # =================================================
            # SEARCH STUDENTS
            # =================================================

            if search_text != "":

                search_value = (
                    "%"
                    + search_text
                    + "%"
                )


                cursor.execute(
                    """
                    SELECT
                        r.Registration_No,
                        r.Name,
                        r.Username,

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
                        ) AS Status

                    FROM registration r

                    LEFT JOIN student_details s
                    ON r.Registration_No =
                       s.Registration_No

                    WHERE
                        LOWER(r.Role) = 'student'

                    AND
                    (
                        r.Registration_No LIKE %s

                        OR r.Name LIKE %s

                        OR r.Username LIKE %s

                        OR s.Course LIKE %s

                        OR CAST(
                            s.Semester AS CHAR
                        ) LIKE %s

                        OR CAST(
                            s.Admission_Year AS CHAR
                        ) LIKE %s

                        OR s.Email LIKE %s

                        OR CAST(
                            s.Age AS CHAR
                        ) LIKE %s

                        OR s.Gender LIKE %s

                        OR s.Phone LIKE %s

                        OR COALESCE(
                            s.Status,
                            'Incomplete'
                        ) LIKE %s
                    )

                    ORDER BY r.Name ASC
                    """,
                    (
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value
                    )
                )


            # =================================================
            # LOAD ALL STUDENTS
            # =================================================

            else:

                cursor.execute(
                    """
                    SELECT
                        r.Registration_No,
                        r.Name,
                        r.Username,

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
                        ) AS Status

                    FROM registration r

                    LEFT JOIN student_details s
                    ON r.Registration_No =
                       s.Registration_No

                    WHERE
                        LOWER(r.Role) = 'student'

                    ORDER BY r.Name ASC
                    """
                )


            # =================================================
            # FETCH STUDENTS
            # =================================================

            students = cursor.fetchall()


            # =================================================
            # UPDATE STUDENT COUNT
            # =================================================

            if len(students) == 1:

                count_label.config(
                    text="1 Student"
                )


            else:

                count_label.config(
                    text=(
                        f"{len(students)} "
                        "Students"
                    )
                )


            # =================================================
            # NO STUDENTS
            # =================================================

            if len(students) == 0:

                if search_text == "":

                    show_empty_message(
                        "No students found."
                    )


                else:

                    show_empty_message(
                        "No students match your search."
                    )


                update_scroll_region()

                return


            # =================================================
            # CREATE STUDENT ROWS
            # =================================================

            for student in students:

                create_student_row(
                    student
                )


            # =================================================
            # UPDATE SCROLLING
            # =================================================

            rows_frame.update_idletasks()

            table_frame.update_idletasks()

            update_scroll_region()


            # =================================================
            # RETURN SCROLL POSITION TO START
            # =================================================

            table_canvas.yview_moveto(
                0
            )

            table_canvas.xview_moveto(
                0
            )


        except mysql.connector.Error as error:

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
    # SEARCH STUDENTS
    # ========================================================

    def search_students():

        search_text = (
            search_entry
            .get()
            .strip()
        )


        if (
            search_text == ""
            or search_text == PLACEHOLDER
        ):

            load_students()

            return


        load_students(
            search_text
        )


    # ========================================================
    # CLEAR SEARCH
    # ========================================================

    def clear_search():

        search_entry.delete(
            0,
            END
        )

        search_entry.config(
            fg=TEXT_COLOR
        )

        load_students()

        set_placeholder()

        page.focus_set()


    # ========================================================
    # SEARCH BUTTON
    # ========================================================

    search_button = Button(
        search_frame,
        text="SEARCH",
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
        command=search_students
    )

    search_button.place(
        relx=1.0,
        x=-135,
        y=17,
        width=100,
        height=40,
        anchor="ne"
    )


    # ========================================================
    # CLEAR BUTTON
    # ========================================================

    clear_button = Button(
        search_frame,
        text="CLEAR",
        bg="#F1F5F9",
        fg=TEXT_COLOR,
        activebackground="#E2E8F0",
        activeforeground=TEXT_COLOR,
        font=(
            "Helvetica",
            9,
            "bold"
        ),
        bd=0,
        cursor="hand2",
        command=clear_search
    )

    clear_button.place(
        relx=1.0,
        x=-20,
        y=17,
        width=100,
        height=40,
        anchor="ne"
    )


    # ========================================================
    # PRESS ENTER TO SEARCH
    # ========================================================

    search_entry.bind(
        "<Return>",
        lambda event: search_students()
    )


    # ========================================================
    # LOAD ALL STUDENTS
    # ========================================================

    load_students()