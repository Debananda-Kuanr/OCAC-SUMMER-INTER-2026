from tkinter import *
from tkinter import messagebox
import mysql.connector

from course_form import open_course_form


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
# SHOW COURSE PAGE
# ============================================================

def show_course_page(parent):

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
        text="Courses",
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
        text="Manage courses and their academic structure",
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
    # ADD COURSE
    # ========================================================

    def add_course():

        open_course_form(
            parent,
            refresh_callback=lambda: show_course_page(parent)
        )


    # ========================================================
    # ADD COURSE BUTTON
    # ========================================================

    add_button = Button(
        header_frame,
        text="+  ADD COURSE",
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
        command=add_course
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
        "Search by course ID, course name, duration, semesters or status..."
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


    def remove_placeholder(event=None):

        if search_entry.get() == PLACEHOLDER:

            search_entry.delete(
                0,
                END
            )

            search_entry.config(
                fg=TEXT_COLOR
            )


    def restore_placeholder(event=None):

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
    # COURSE COUNT
    # ========================================================

    count_label = Label(
        table_top,
        text="0 Courses",
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
    # VERTICAL SCROLLBAR ONLY
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
    # CONFIGURE TABLE CONTAINER
    # ========================================================

    table_container.grid_rowconfigure(
        0,
        weight=1
    )

    table_container.grid_columnconfigure(
        0,
        weight=1
    )


    table_canvas.configure(
        yscrollcommand=y_scrollbar.set
    )


    # ========================================================
    # COMPLETE TABLE FRAME
    # ========================================================

    table_frame = Frame(
        table_canvas,
        bg=WHITE
    )

    canvas_window = table_canvas.create_window(
        (
            0,
            0
        ),
        window=table_frame,
        anchor="nw"
    )


    # ========================================================
    # FIT TABLE TO COMPLETE AVAILABLE WIDTH
    # ========================================================

    def resize_table_width(event):

        table_canvas.itemconfigure(
            canvas_window,
            width=event.width
        )


    table_canvas.bind(
        "<Configure>",
        resize_table_width
    )


    # ========================================================
    # TABLE HEADER
    # ========================================================

    table_header = Frame(
        table_frame,
        bg=TABLE_HEADER,
        height=48
    )

    table_header.pack(
        fill=X
    )

    # IMPORTANT: header children use grid(), so disable GRID propagation.
    # pack_propagate(False) does not preserve the requested height here.
    table_header.grid_propagate(
        False
    )


    # ========================================================
    # COLUMN WEIGHTS
    #
    # SAME STYLE AS STUDENT MANAGEMENT, BUT THE COURSE TABLE
    # FITS THE COMPLETE AVAILABLE WIDTH, SO NO X SCROLLBAR.
    # ========================================================

    COLUMN_WEIGHTS = {
        "course_id": 14,
        "course_name": 28,
        "duration": 16,
        "semesters": 16,
        "status": 12,
        "actions": 18
    }


    for column_index, weight in enumerate(
        COLUMN_WEIGHTS.values()
    ):

        table_header.grid_columnconfigure(
            column_index,
            weight=weight,
            uniform="course_columns"
        )


    table_header.grid_rowconfigure(
        0,
        weight=1
    )


    # ========================================================
    # HEADER COLUMN
    # ========================================================

    def header_column(
        text,
        column
    ):

        label = Label(
            table_header,
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

        label.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=10
        )


    # ========================================================
    # CREATE TABLE HEADERS
    # ========================================================

    header_column(
        "COURSE ID",
        0
    )

    header_column(
        "COURSE NAME",
        1
    )

    header_column(
        "DURATION",
        2
    )

    header_column(
        "SEMESTERS",
        3
    )

    header_column(
        "STATUS",
        4
    )

    header_column(
        "ACTIONS",
        5
    )


    # ========================================================
    # ROWS FRAME
    # ========================================================

    rows_frame = Frame(
        table_frame,
        bg=WHITE
    )

    rows_frame.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # UPDATE SCROLL REGION
    # ========================================================

    def update_scroll_region(event=None):

        table_canvas.configure(
            scrollregion=table_canvas.bbox(
                "all"
            )
        )


    table_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    rows_frame.bind(
        "<Configure>",
        update_scroll_region
    )


    # ========================================================
    # MOUSE WHEEL SCROLLING
    # ========================================================

    def mouse_wheel_y(event):

        if event.delta:

            table_canvas.yview_scroll(
                int(
                    -1 * (
                        event.delta / 120
                    )
                ),
                "units"
            )

        return "break"


    def enable_mouse_scroll(event=None):

        table_canvas.bind_all(
            "<MouseWheel>",
            mouse_wheel_y
        )


    def disable_mouse_scroll(event=None):

        table_canvas.unbind_all(
            "<MouseWheel>"
        )


    table_container.bind(
        "<Enter>",
        enable_mouse_scroll
    )

    table_container.bind(
        "<Leave>",
        disable_mouse_scroll
    )


    # ========================================================
    # EDIT COURSE
    # ========================================================

    def edit_course(course_id):

        open_course_form(
            parent,
            refresh_callback=lambda: show_course_page(parent),
            course_id=course_id
        )


    # ========================================================
    # DELETE COURSE
    # ========================================================

    def delete_course(
        course_id,
        course_name
    ):

        confirm = messagebox.askyesno(
            "Delete Course",
            (
                f"Are you sure you want to delete "
                f"{course_name}?\n\n"
                f"Course ID: {course_id}\n\n"
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


            # ------------------------------------------------
            # CHECK IF STUDENTS ARE USING THIS COURSE
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM student_details
                WHERE Course = %s
                """,
                (
                    course_name,
                )
            )


            student_count = cursor.fetchone()[0]


            if student_count > 0:

                messagebox.showwarning(
                    "Course In Use",
                    (
                        f"{course_name} cannot be deleted.\n\n"
                        f"{student_count} student(s) are currently "
                        "assigned to this course.\n\n"
                        "Set the course status to Inactive instead."
                    )
                )

                return


            # ------------------------------------------------
            # DELETE COURSE
            # ------------------------------------------------

            cursor.execute(
                """
                DELETE FROM courses
                WHERE Course_ID = %s
                """,
                (
                    course_id,
                )
            )


            if cursor.rowcount == 0:

                con.rollback()

                messagebox.showwarning(
                    "Course Not Found",
                    "The selected course could not be found."
                )

                return


            con.commit()


            messagebox.showinfo(
                "Course Deleted",
                (
                    f"{course_name} "
                    "has been deleted successfully."
                )
            )


            load_courses()


        except mysql.connector.Error as error:

            if con is not None:
                con.rollback()


            messagebox.showerror(
                "Database Error",
                str(error)
            )


        finally:

            if cursor is not None:
                cursor.close()


            if con is not None:
                con.close()


    # ========================================================
    # CREATE NORMAL TABLE CELL
    # ========================================================

    def create_cell(
        row,
        text,
        column,
        color=TEXT_COLOR,
        bold=False
    ):

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
            row,
            text=text,
            bg=WHITE,
            fg=color,
            font=cell_font,
            anchor="w"
        )

        cell_label.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=10
        )


    # ========================================================
    # CREATE COURSE ROW
    # ========================================================

    def create_course_row(course):

        # ----------------------------------------------------
        # GET VALUES
        # ----------------------------------------------------

        course_id = course[0]
        course_name = course[1]
        duration_years = course[2]
        total_semesters = course[3]
        status = course[4]


        # ----------------------------------------------------
        # HANDLE NULL VALUES
        # ----------------------------------------------------

        if course_id is None:
            course_id = "-"


        if course_name is None:
            course_name = "-"


        if duration_years is None:

            duration_display = "-"

        else:

            try:

                duration_number = int(
                    duration_years
                )

                if duration_number == 1:

                    duration_display = "1 Year"

                else:

                    duration_display = (
                        f"{duration_number} Years"
                    )

            except (ValueError, TypeError):

                duration_display = str(
                    duration_years
                )


        if total_semesters is None:

            semester_display = "-"

        else:

            semester_display = str(
                total_semesters
            )


        if status is None:

            status_display = "Inactive"

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
            height=59
        )

        row.pack(
            fill=X
        )

        # IMPORTANT: row children use grid(), so disable GRID propagation.
        # This keeps every row at the same 59 px height like Student Management.
        row.grid_propagate(
            False
        )


        # ====================================================
        # SAME COLUMN STRUCTURE AS HEADER
        # ====================================================

        for column_index, weight in enumerate(
            COLUMN_WEIGHTS.values()
        ):

            row.grid_columnconfigure(
                column_index,
                weight=weight,
                uniform="course_columns"
            )


        row.grid_rowconfigure(
            0,
            weight=1
        )


        # ====================================================
        # COURSE ID
        # ====================================================

        create_cell(
            row,
            str(course_id),
            0,
            BLUE,
            True
        )


        # ====================================================
        # COURSE NAME
        # ====================================================

        create_cell(
            row,
            str(course_name),
            1,
            TEXT_COLOR,
            True
        )


        # ====================================================
        # DURATION
        # ====================================================

        create_cell(
            row,
            duration_display,
            2
        )


        # ====================================================
        # SEMESTERS
        # ====================================================

        create_cell(
            row,
            semester_display,
            3
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
            4,
            status_color,
            True
        )


        # ====================================================
        # ACTION CELL
        # ====================================================

        action_frame = Frame(
            row,
            bg=WHITE
        )

        action_frame.grid(
            row=0,
            column=5,
            sticky="nsew",
            padx=10
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
            command=lambda selected_course_id=course_id: (
                edit_course(
                    selected_course_id
                )
            )
        )

        edit_button.place(
            x=0,
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
            command=lambda selected_course_id=course_id,
            selected_course_name=course_name: (
                delete_course(
                    selected_course_id,
                    selected_course_name
                )
            )
        )

        delete_button.place(
            x=70,
            y=13,
            width=70,
            height=30
        )


        # ====================================================
        # BOTTOM BORDER
        # ====================================================

        bottom_border = Frame(
            row,
            bg="#F1F5F9",
            height=1
        )

        bottom_border.place(
            x=0,
            rely=1.0,
            relwidth=1.0,
            height=1,
            anchor="sw"
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

    def show_empty_message(message):

        empty_frame = Frame(
            rows_frame,
            bg=WHITE,
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
    # LOAD COURSES
    # ========================================================

    def load_courses(search_text=""):

        clear_rows()


        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()


            # =================================================
            # SEARCH COURSES
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
                        Course_ID,
                        Course_Name,
                        Duration_Years,
                        Total_Semesters,
                        Status

                    FROM courses

                    WHERE
                        Course_ID LIKE %s

                        OR Course_Name LIKE %s

                        OR CAST(
                            Duration_Years AS CHAR
                        ) LIKE %s

                        OR CAST(
                            Total_Semesters AS CHAR
                        ) LIKE %s

                        OR Status LIKE %s

                    ORDER BY Course_Name ASC
                    """,
                    (
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value
                    )
                )


            # =================================================
            # LOAD ALL COURSES
            # =================================================

            else:

                cursor.execute(
                    """
                    SELECT
                        Course_ID,
                        Course_Name,
                        Duration_Years,
                        Total_Semesters,
                        Status

                    FROM courses

                    ORDER BY Course_Name ASC
                    """
                )


            courses = cursor.fetchall()


            # ------------------------------------------------
            # UPDATE COURSE COUNT
            # ------------------------------------------------

            if len(courses) == 1:

                count_label.config(
                    text="1 Course"
                )

            else:

                count_label.config(
                    text=f"{len(courses)} Courses"
                )


            # ------------------------------------------------
            # NO COURSES
            # ------------------------------------------------

            if len(courses) == 0:

                if search_text == "":

                    show_empty_message(
                        "No courses found."
                    )

                else:

                    show_empty_message(
                        "No courses match your search."
                    )


                update_scroll_region()

                return


            # ------------------------------------------------
            # CREATE COURSE ROWS
            # ------------------------------------------------

            for course in courses:

                create_course_row(
                    course
                )


            # ------------------------------------------------
            # UPDATE SCROLLING
            # ------------------------------------------------

            rows_frame.update_idletasks()

            table_frame.update_idletasks()

            update_scroll_region()


            # ------------------------------------------------
            # RETURN SCROLL POSITION TO START
            # ------------------------------------------------

            table_canvas.yview_moveto(
                0
            )


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )


        finally:

            if cursor is not None:
                cursor.close()


            if con is not None:
                con.close()


    # ========================================================
    # SEARCH COURSES
    # ========================================================

    def search_courses():

        search_text = (
            search_entry
            .get()
            .strip()
        )


        if (
            search_text == ""
            or search_text == PLACEHOLDER
        ):

            load_courses()

            return


        load_courses(
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


        load_courses(
            search_text=""
        )


        search_entry.delete(
            0,
            END
        )


        search_entry.insert(
            0,
            PLACEHOLDER
        )


        search_entry.config(
            fg=LIGHT_GRAY
        )


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
        command=search_courses
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
        lambda event: search_courses()
    )


    # ========================================================
    # LOAD ALL COURSES
    # ========================================================

    load_courses()
