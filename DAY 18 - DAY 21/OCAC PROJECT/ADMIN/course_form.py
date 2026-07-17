from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
DARK_BLUE = "#1D4ED8"

WHITE = "#FFFFFF"
BACKGROUND = "#F8FAFC"

TEXT_COLOR = "#0F172A"
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
# GENERATE NEXT COURSE ID
#
# C001
# C002
# C003
# ...
#
# IMPORTANT:
# The ID is generated from the highest existing numeric ID.
# Deleted IDs are not reused.
# ============================================================

def generate_course_id():

    con = None
    cursor = None

    try:

        con = get_connection()

        cursor = con.cursor()


        # ----------------------------------------------------
        # GET ALL COURSE IDs STARTING WITH C
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT Course_ID

            FROM courses

            WHERE Course_ID LIKE 'C%'
            """
        )


        records = cursor.fetchall()


        # ----------------------------------------------------
        # FIND HIGHEST VALID NUMBER
        #
        # C001 -> 1
        # C025 -> 25
        # ----------------------------------------------------

        highest_number = 0


        for record in records:

            existing_id = str(
                record[0]
            ).strip()


            # Remove first character "C"
            number_part = (
                existing_id[1:]
            )


            # Only use valid numeric IDs
            if number_part.isdigit():

                current_number = int(
                    number_part
                )


                if (
                    current_number
                    >
                    highest_number
                ):

                    highest_number = (
                        current_number
                    )


        # ----------------------------------------------------
        # GENERATE NEXT ID
        # ----------------------------------------------------

        next_number = (
            highest_number + 1
        )


        return (
            f"C{next_number:03d}"
        )


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            (
                "Could not generate Course ID.\n\n"
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
# OPEN COURSE FORM
# ============================================================

def open_course_form(
    parent,
    refresh_callback=None,
    course_id=None
):

    # ========================================================
    # ADD OR EDIT MODE
    # ========================================================

    is_edit_mode = (
        course_id is not None
    )


    # ========================================================
    # CREATE SEPARATE WINDOW
    # ========================================================

    form_window = Toplevel()


    # ========================================================
    # WINDOW TITLE
    # ========================================================

    if is_edit_mode:

        form_window.title(
            "Edit Course"
        )

    else:

        form_window.title(
            "Add Course"
        )


    # ========================================================
    # WINDOW BACKGROUND
    # ========================================================

    form_window.configure(
        bg=BACKGROUND
    )


    # ========================================================
    # WINDOW SIZE
    # ========================================================

    WINDOW_WIDTH = 760
    WINDOW_HEIGHT = 540


    form_window.geometry(
        f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
    )


    # ========================================================
    # FIX WINDOW SIZE
    # ========================================================

    form_window.resizable(
        False,
        False
    )


    # ========================================================
    # CENTER WINDOW
    # ========================================================

    form_window.update_idletasks()


    screen_width = (
        form_window.winfo_screenwidth()
    )


    screen_height = (
        form_window.winfo_screenheight()
    )


    x_position = int(
        (
            screen_width
            -
            WINDOW_WIDTH
        )
        /
        2
    )


    y_position = int(
        (
            screen_height
            -
            WINDOW_HEIGHT
        )
        /
        2
    )


    form_window.geometry(
        f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        f"+{x_position}+{y_position}"
    )


    # ========================================================
    # BRING WINDOW TO FRONT
    # ========================================================

    form_window.lift()


    # ========================================================
    # CLOSE FORM
    # ========================================================

    def close_form():

        try:

            form_window.destroy()

        except TclError:

            pass


    # ========================================================
    # CLOSE FORM AND REFRESH COURSE TABLE
    # ========================================================

    def close_and_refresh():

        # ----------------------------------------------------
        # CLOSE ADD / EDIT WINDOW
        # ----------------------------------------------------

        close_form()


        # ----------------------------------------------------
        # REFRESH COURSE MANAGEMENT PAGE
        # ----------------------------------------------------

        if refresh_callback is not None:

            refresh_callback()


    # ========================================================
    # WINDOW X CLOSE BUTTON
    # ========================================================

    form_window.protocol(
        "WM_DELETE_WINDOW",
        close_form
    )


    # ========================================================
    # MAIN PAGE
    # ========================================================

    page = Frame(
        form_window,
        bg=BACKGROUND
    )


    page.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # HEADER
    # ========================================================

    header_frame = Frame(
        page,
        bg=BACKGROUND,
        height=90
    )


    header_frame.pack(
        fill=X
    )


    header_frame.pack_propagate(
        False
    )


    # ========================================================
    # TITLE AND SUBTITLE
    # ========================================================

    if is_edit_mode:

        title_text = (
            "Edit Course"
        )


        subtitle_text = (
            "Update course and academic information"
        )


    else:

        title_text = (
            "Add Course"
        )


        subtitle_text = (
            "Create a new course and academic structure"
        )


    # ========================================================
    # PAGE TITLE
    # ========================================================

    title_label = Label(
        header_frame,
        text=title_text,
        bg=BACKGROUND,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            20,
            "bold"
        )
    )


    title_label.place(
        x=25,
        y=18
    )


    # ========================================================
    # PAGE SUBTITLE
    # ========================================================

    subtitle_label = Label(
        header_frame,
        text=subtitle_text,
        bg=BACKGROUND,
        fg=GRAY,
        font=(
            "Helvetica",
            9
        )
    )


    subtitle_label.place(
        x=27,
        y=55
    )


    # ========================================================
    # FORM CARD
    # ========================================================

    form_card = Frame(
        page,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )


    form_card.pack(
        fill=BOTH,
        expand=True,
        padx=25,
        pady=(
            0,
            25
        )
    )


    # ========================================================
    # CARD HEADER
    # ========================================================

    card_header = Frame(
        form_card,
        bg=WHITE,
        height=75
    )


    card_header.pack(
        fill=X
    )


    card_header.pack_propagate(
        False
    )


    # ========================================================
    # CARD TITLE
    # ========================================================

    card_title = Label(
        card_header,
        text="Course Information",
        bg=WHITE,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            13,
            "bold"
        )
    )


    card_title.place(
        x=22,
        y=16
    )


    # ========================================================
    # CARD SUBTITLE
    # ========================================================

    card_subtitle = Label(
        card_header,
        text=(
            "Enter the course and academic details."
        ),
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            9
        )
    )


    card_subtitle.place(
        x=23,
        y=45
    )


    # ========================================================
    # SEPARATOR
    # ========================================================

    separator = Frame(
        form_card,
        bg=BORDER,
        height=1
    )


    separator.pack(
        fill=X,
        padx=22
    )


    # ========================================================
    # FORM CONTENT
    # ========================================================

    form_content = Frame(
        form_card,
        bg=WHITE
    )


    form_content.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # CREATE FIELD LABEL
    # ========================================================

    def create_label(
        text,
        x,
        y
    ):

        label = Label(
            form_content,
            text=text,
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        )


        label.place(
            x=x,
            y=y
        )


    # ========================================================
    # COURSE ID
    #
    # AUTO-GENERATED
    # CANNOT BE CHANGED
    # ========================================================

    create_label(
        "Course ID",
        25,
        22
    )


    course_id_var = StringVar()


    course_id_entry = Entry(
        form_content,
        textvariable=course_id_var,
        bg="#F8FAFC",
        fg=GRAY,
        disabledbackground="#F8FAFC",
        disabledforeground=GRAY,
        font=(
            "Helvetica",
            10
        ),
        bd=0,
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor="#CBD5E1",
        state="disabled"
    )


    course_id_entry.place(
        x=25,
        y=48,
        width=315,
        height=38
    )


    # ========================================================
    # COURSE NAME
    # ========================================================

    create_label(
        "Course Name",
        370,
        22
    )


    course_name_entry = Entry(
        form_content,
        bg=WHITE,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            10
        ),
        bd=0,
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor=BLUE
    )


    course_name_entry.place(
        x=370,
        y=48,
        width=315,
        height=38
    )


    # ========================================================
    # DURATION
    # ========================================================

    create_label(
        "Duration (Years)",
        25,
        110
    )


    duration_var = StringVar()


    duration_combo = ttk.Combobox(
        form_content,
        textvariable=duration_var,
        values=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6"
        ],
        state="readonly",
        font=(
            "Helvetica",
            10
        )
    )


    duration_combo.place(
        x=25,
        y=136,
        width=315,
        height=38
    )


    # ========================================================
    # TOTAL SEMESTERS
    # ========================================================

    create_label(
        "Total Semesters",
        370,
        110
    )


    semester_var = StringVar()


    semester_combo = ttk.Combobox(
        form_content,
        textvariable=semester_var,
        values=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12"
        ],
        state="readonly",
        font=(
            "Helvetica",
            10
        )
    )


    semester_combo.place(
        x=370,
        y=136,
        width=315,
        height=38
    )


    # ========================================================
    # STATUS
    # ========================================================

    create_label(
        "Status",
        25,
        198
    )


    status_var = StringVar(
        value="Active"
    )


    status_combo = ttk.Combobox(
        form_content,
        textvariable=status_var,
        values=[
            "Active",
            "Inactive"
        ],
        state="readonly",
        font=(
            "Helvetica",
            10
        )
    )


    status_combo.place(
        x=25,
        y=224,
        width=315,
        height=38
    )


    # ========================================================
    # LOAD COURSE FOR EDIT
    # ========================================================

    def load_course():

        if not is_edit_mode:

            return


        con = None
        cursor = None


        try:

            con = get_connection()


            cursor = con.cursor()


            cursor.execute(
                """
                SELECT
                    Course_ID,
                    Course_Name,
                    Duration_Years,
                    Total_Semesters,
                    Status

                FROM courses

                WHERE Course_ID = %s
                """,
                (
                    course_id,
                )
            )


            course = (
                cursor.fetchone()
            )


            # =================================================
            # COURSE NOT FOUND
            # =================================================

            if course is None:

                messagebox.showerror(
                    "Course Not Found",
                    (
                        "The selected course "
                        "could not be found."
                    ),
                    parent=form_window
                )


                close_form()


                return


            # =================================================
            # COURSE ID
            # =================================================

            course_id_var.set(
                str(
                    course[0]
                )
            )


            # =================================================
            # COURSE NAME
            # =================================================

            course_name_entry.delete(
                0,
                END
            )


            course_name_entry.insert(
                0,
                str(
                    course[1]
                )
            )


            # =================================================
            # DURATION
            # =================================================

            duration_var.set(
                str(
                    course[2]
                )
            )


            # =================================================
            # TOTAL SEMESTERS
            # =================================================

            semester_var.set(
                str(
                    course[3]
                )
            )


            # =================================================
            # STATUS
            # =================================================

            status_var.set(
                str(
                    course[4]
                )
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
    # VALIDATE FORM
    # ========================================================

    def validate_form():

        # ----------------------------------------------------
        # AUTO-GENERATED COURSE ID
        # ----------------------------------------------------

        entered_course_id = (
            course_id_var
            .get()
            .strip()
        )


        # ----------------------------------------------------
        # OTHER VALUES
        # ----------------------------------------------------

        course_name = (
            course_name_entry
            .get()
            .strip()
        )


        duration = (
            duration_var
            .get()
            .strip()
        )


        total_semesters = (
            semester_var
            .get()
            .strip()
        )


        status = (
            status_var
            .get()
            .strip()
        )


        # ====================================================
        # COURSE ID REQUIRED
        # ====================================================

        if entered_course_id == "":

            messagebox.showerror(
                "Course ID Error",
                (
                    "Course ID could not be generated."
                ),
                parent=form_window
            )


            return None


        # ====================================================
        # COURSE NAME REQUIRED
        # ====================================================

        if course_name == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter Course Name.",
                parent=form_window
            )


            course_name_entry.focus_set()


            return None


        # ====================================================
        # DURATION REQUIRED
        # ====================================================

        if duration == "":

            messagebox.showwarning(
                "Missing Information",
                "Please select Duration.",
                parent=form_window
            )


            return None


        # ====================================================
        # SEMESTERS REQUIRED
        # ====================================================

        if total_semesters == "":

            messagebox.showwarning(
                "Missing Information",
                (
                    "Please select Total Semesters."
                ),
                parent=form_window
            )


            return None


        # ====================================================
        # STATUS REQUIRED
        # ====================================================

        if status == "":

            messagebox.showwarning(
                "Missing Information",
                "Please select Status.",
                parent=form_window
            )


            return None


        # ====================================================
        # CONVERT TO INTEGER
        # ====================================================

        try:

            duration = int(
                duration
            )


            total_semesters = int(
                total_semesters
            )


        except ValueError:

            messagebox.showwarning(
                "Invalid Information",
                (
                    "Duration and Total Semesters "
                    "must be valid numbers."
                ),
                parent=form_window
            )


            return None


        # ====================================================
        # RETURN VALID DATA
        # ====================================================

        return {

            "course_id":
                entered_course_id,

            "course_name":
                course_name,

            "duration":
                duration,

            "total_semesters":
                total_semesters,

            "status":
                status

        }


    # ========================================================
    # ADD COURSE
    # ========================================================

    def add_course():

        data = (
            validate_form()
        )


        if data is None:

            return


        con = None
        cursor = None


        try:

            con = get_connection()


            cursor = con.cursor()


            # =================================================
            # GENERATE ID AGAIN BEFORE INSERT
            #
            # This makes sure the newest available ID is used.
            # =================================================

            final_course_id = (
                generate_course_id()
            )


            if final_course_id == "":

                return


            # =================================================
            # UPDATE DISPLAYED ID
            # =================================================

            course_id_var.set(
                final_course_id
            )


            # =================================================
            # CHECK COURSE NAME
            # =================================================

            cursor.execute(
                """
                SELECT Course_ID

                FROM courses

                WHERE LOWER(Course_Name) = LOWER(%s)
                """,
                (
                    data["course_name"],
                )
            )


            if cursor.fetchone() is not None:

                messagebox.showwarning(
                    "Course Already Exists",
                    (
                        "A course with this name "
                        "already exists."
                    ),
                    parent=form_window
                )


                return


            # =================================================
            # INSERT COURSE
            # =================================================

            cursor.execute(
                """
                INSERT INTO courses
                (
                    Course_ID,
                    Course_Name,
                    Duration_Years,
                    Total_Semesters,
                    Status
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    final_course_id,
                    data["course_name"],
                    data["duration"],
                    data["total_semesters"],
                    data["status"]
                )
            )


            con.commit()


            # =================================================
            # SUCCESS
            # =================================================

            messagebox.showinfo(
                "Course Added",
                (
                    f"{data['course_name']} "
                    "has been added successfully.\n\n"
                    f"Course ID: {final_course_id}"
                ),
                parent=form_window
            )


            close_and_refresh()


        except mysql.connector.IntegrityError as error:

            if con is not None:

                try:

                    con.rollback()

                except:

                    pass


            messagebox.showerror(
                "Database Error",
                (
                    "Could not add the course.\n\n"
                    f"{error}"
                ),
                parent=form_window
            )


        except mysql.connector.Error as error:

            if con is not None:

                try:

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
    # UPDATE COURSE
    # ========================================================

    def update_course():

        data = (
            validate_form()
        )


        if data is None:

            return


        con = None
        cursor = None


        try:

            con = get_connection()


            cursor = con.cursor()


            # =================================================
            # GET OLD COURSE
            # =================================================

            cursor.execute(
                """
                SELECT
                    Course_Name,
                    Total_Semesters

                FROM courses

                WHERE Course_ID = %s
                """,
                (
                    course_id,
                )
            )


            old_course = (
                cursor.fetchone()
            )


            if old_course is None:

                messagebox.showerror(
                    "Course Not Found",
                    (
                        "The selected course "
                        "could not be found."
                    ),
                    parent=form_window
                )


                return


            old_course_name = (
                old_course[0]
            )


            old_total_semesters = int(
                old_course[1]
            )


            # =================================================
            # CHECK DUPLICATE COURSE NAME
            # =================================================

            cursor.execute(
                """
                SELECT Course_ID

                FROM courses

                WHERE
                    LOWER(Course_Name) = LOWER(%s)

                AND
                    Course_ID <> %s
                """,
                (
                    data["course_name"],
                    course_id
                )
            )


            if cursor.fetchone() is not None:

                messagebox.showwarning(
                    "Course Already Exists",
                    (
                        "Another course with this "
                        "name already exists."
                    ),
                    parent=form_window
                )


                return


            # =================================================
            # CHECK BEFORE REDUCING SEMESTERS
            # =================================================

            if (
                data["total_semesters"]
                <
                old_total_semesters
            ):

                cursor.execute(
                    """
                    SELECT COUNT(*)

                    FROM student_details

                    WHERE
                        Course = %s

                    AND
                        Semester > %s
                    """,
                    (
                        old_course_name,
                        data["total_semesters"]
                    )
                )


                invalid_students = (
                    cursor.fetchone()[0]
                )


                if invalid_students > 0:

                    messagebox.showwarning(
                        "Cannot Reduce Semesters",
                        (
                            f"Total Semesters cannot be changed "
                            f"to {data['total_semesters']}.\n\n"

                            f"{invalid_students} student(s) are "
                            "currently in a higher semester."
                        ),
                        parent=form_window
                    )


                    return


            # =================================================
            # UPDATE COURSE
            #
            # COURSE ID IS NEVER CHANGED
            # =================================================

            cursor.execute(
                """
                UPDATE courses

                SET
                    Course_Name = %s,
                    Duration_Years = %s,
                    Total_Semesters = %s,
                    Status = %s

                WHERE Course_ID = %s
                """,
                (
                    data["course_name"],
                    data["duration"],
                    data["total_semesters"],
                    data["status"],
                    course_id
                )
            )


            # =================================================
            # UPDATE COURSE NAME IN STUDENT DETAILS
            # =================================================

            if (
                old_course_name
                !=
                data["course_name"]
            ):

                cursor.execute(
                    """
                    UPDATE student_details

                    SET Course = %s

                    WHERE Course = %s
                    """,
                    (
                        data["course_name"],
                        old_course_name
                    )
                )


            con.commit()


            # =================================================
            # SUCCESS
            # =================================================

            messagebox.showinfo(
                "Course Updated",
                (
                    f"{data['course_name']} "
                    "has been updated successfully."
                ),
                parent=form_window
            )


            close_and_refresh()


        except mysql.connector.Error as error:

            if con is not None:

                try:

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
    # SAVE COURSE
    # ========================================================

    def save_course():

        if is_edit_mode:

            update_course()

        else:

            add_course()


    # ========================================================
    # BUTTON AREA
    # ========================================================

    button_area = Frame(
        form_card,
        bg=WHITE,
        height=70
    )


    button_area.pack(
        fill=X,
        side=BOTTOM
    )


    button_area.pack_propagate(
        False
    )


    # ========================================================
    # BUTTON BORDER
    # ========================================================

    button_border = Frame(
        button_area,
        bg=BORDER,
        height=1
    )


    button_border.pack(
        fill=X,
        padx=22
    )


    # ========================================================
    # SAVE BUTTON TEXT
    # ========================================================

    if is_edit_mode:

        save_button_text = (
            "UPDATE COURSE"
        )

    else:

        save_button_text = (
            "ADD COURSE"
        )


    # ========================================================
    # SAVE BUTTON
    # ========================================================

    save_button = Button(
        button_area,
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
        command=save_course
    )


    save_button.place(
        relx=1.0,
        x=-22,
        y=16,
        width=140,
        height=38,
        anchor="ne"
    )


    # ========================================================
    # CANCEL BUTTON
    # ========================================================

    cancel_button = Button(
        button_area,
        text="CANCEL",
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
        command=close_form
    )


    cancel_button.place(
        relx=1.0,
        x=-177,
        y=16,
        width=105,
        height=38,
        anchor="ne"
    )


    # ========================================================
    # INITIALIZE FORM
    # ========================================================

    if is_edit_mode:

        # ----------------------------------------------------
        # EDIT MODE:
        # LOAD EXISTING COURSE ID AND DATA
        # ----------------------------------------------------

        load_course()


    else:

        # ----------------------------------------------------
        # ADD MODE:
        # AUTO-GENERATE COURSE ID
        # ----------------------------------------------------

        new_course_id = (
            generate_course_id()
        )


        course_id_var.set(
            new_course_id
        )


        # ----------------------------------------------------
        # FOCUS COURSE NAME
        # ----------------------------------------------------

        course_name_entry.focus_set()