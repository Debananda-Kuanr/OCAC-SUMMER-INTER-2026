from tkinter import *
from tkinter import messagebox
import mysql.connector


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
DARK_BLUE = "#1E40AF"
LIGHT_BLUE = "#EFF6FF"

WHITE = "#FFFFFF"
BACKGROUND = "#F8FAFC"

TEXT_COLOR = "#1E293B"
GRAY = "#64748B"

BORDER_COLOR = "#E2E8F0"

GREEN = "#16A34A"
LIGHT_GREEN = "#F0FDF4"

RED = "#DC2626"
LIGHT_RED = "#FEF2F2"


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
# MAIN FEE STRUCTURE PAGE
# ============================================================

def show_fee_structure_page(parent):

    # ========================================================
    # CLEAR OLD PAGE
    # ========================================================

    for widget in parent.winfo_children():
        widget.destroy()


    # ========================================================
    # VARIABLES
    # ========================================================

    search_var = StringVar()

    SEARCH_PLACEHOLDER = (
        "Search by course, semester or academic year..."
    )


    # ========================================================
    # PAGE TITLE
    # ========================================================

    page_title = Label(
        parent,
        text="Fee Structure",
        bg=BACKGROUND,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            22,
            "bold"
        )
    )

    page_title.place(
        x=35,
        y=25
    )


    # ========================================================
    # PAGE SUBTITLE
    # ========================================================

    page_subtitle = Label(
        parent,
        text=(
            "Manage standard course and semester "
            "fee structures."
        ),
        bg=BACKGROUND,
        fg=GRAY,
        font=(
            "Helvetica",
            10
        )
    )

    page_subtitle.place(
        x=36,
        y=65
    )


    # ========================================================
    # ADD FEE STRUCTURE
    # ========================================================

    def add_fee_structure():

        try:

            from fee_structure_form import (
                open_fee_structure_form
            )

            open_fee_structure_form(
                parent=parent,
                refresh_callback=load_fee_structures
            )

        except ImportError:

            messagebox.showinfo(
                "Add Fee Structure",
                (
                    "The Fee Structure Form "
                    "will be connected here."
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "Unable to open the "
                    "Fee Structure Form."
                    f"\n\n{error}"
                )
            )


    # ========================================================
    # ADD FEE STRUCTURE BUTTON
    # ========================================================

    add_structure_button = Button(
        parent,
        text="+ ADD FEE STRUCTURE",
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
        relief=FLAT,
        highlightthickness=0,
        cursor="hand2",
        command=add_fee_structure
    )

    add_structure_button.place(
        relx=1.0,
        x=-35,
        y=28,
        width=170,
        height=42,
        anchor="ne"
    )


    # ========================================================
    # SECTION TAB / TITLE
    # ========================================================

    section_frame = Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    section_frame.place(
        x=35,
        y=110,
        relwidth=0.94,
        height=58
    )


    standard_section = Label(
        section_frame,
        text="STANDARD FEE STRUCTURES",
        bg=LIGHT_BLUE,
        fg=BLUE,
        font=(
            "Helvetica",
            9,
            "bold"
        ),
        anchor="center"
    )

    standard_section.place(
        x=0,
        y=0,
        width=220,
        height=55
    )


    standard_indicator = Frame(
        section_frame,
        bg=BLUE
    )

    standard_indicator.place(
        x=0,
        rely=1.0,
        y=-3,
        width=220,
        height=3
    )


    # ========================================================
    # SEARCH FRAME
    # ========================================================

    search_frame = Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    search_frame.place(
        x=35,
        y=190,
        relwidth=0.94,
        height=74
    )


    # ========================================================
    # SEARCH ENTRY BORDER
    # ========================================================

    search_entry_border = Frame(
        search_frame,
        bg=BORDER_COLOR
    )

    search_entry_border.place(
        x=20,
        y=16,
        relwidth=0.57,
        height=40
    )


    # ========================================================
    # SEARCH ENTRY
    # ========================================================

    search_entry = Entry(
        search_entry_border,
        textvariable=search_var,
        bg=WHITE,
        fg=GRAY,
        insertbackground=TEXT_COLOR,
        font=(
            "Helvetica",
            10
        ),
        relief=FLAT,
        bd=0,
        highlightthickness=0
    )

    search_entry.place(
        x=1,
        y=1,
        relwidth=1.0,
        width=-2,
        height=38
    )


    # ========================================================
    # SEARCH PLACEHOLDER
    # ========================================================

    def set_search_placeholder():

        if not search_var.get().strip():

            search_var.set(
                SEARCH_PLACEHOLDER
            )

            search_entry.config(
                fg=GRAY
            )


    def remove_search_placeholder(
        event=None
    ):

        if (
            search_var.get()
            == SEARCH_PLACEHOLDER
        ):

            search_var.set("")

            search_entry.config(
                fg=TEXT_COLOR
            )


    def restore_search_placeholder(
        event=None
    ):

        if not search_var.get().strip():

            set_search_placeholder()


    def get_search_text():

        search_text = (
            search_var
            .get()
            .strip()
        )

        if (
            search_text
            == SEARCH_PLACEHOLDER
        ):

            return ""

        return search_text


    search_entry.bind(
        "<FocusIn>",
        remove_search_placeholder
    )

    search_entry.bind(
        "<FocusOut>",
        restore_search_placeholder
    )


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
        relief=FLAT,
        highlightthickness=0,
        cursor="hand2"
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
        bg=WHITE,
        fg=GRAY,
        activebackground=BACKGROUND,
        activeforeground=TEXT_COLOR,
        font=(
            "Helvetica",
            9,
            "bold"
        ),
        bd=1,
        relief=SOLID,
        highlightthickness=0,
        cursor="hand2"
    )

    clear_button.place(
        relx=1.0,
        x=-25,
        y=17,
        width=90,
        height=40,
        anchor="ne"
    )


    # ========================================================
    # COUNT LABEL
    # ========================================================

    count_label = Label(
        parent,
        text="0 Fee Structures",
        bg=BACKGROUND,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            11,
            "bold"
        )
    )

    count_label.place(
        x=36,
        y=292
    )


    # ========================================================
    # TABLE CARD
    # ========================================================

    table_card = Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    table_card.place(
        x=35,
        y=325,
        relwidth=0.94,
        relheight=0.50
    )


    # ========================================================
    # TABLE HEADER
    # ========================================================

    table_header = Frame(
        table_card,
        bg=BACKGROUND,
        height=50
    )

    table_header.pack(
        fill=X
    )

    table_header.pack_propagate(
        False
    )


    # ========================================================
    # CREATE TABLE HEADER
    # ========================================================

    def create_header(
        text,
        relx_position
    ):

        label = Label(
            table_header,
            text=text,
            bg=BACKGROUND,
            fg=GRAY,
            font=(
                "Helvetica",
                8,
                "bold"
            ),
            anchor="w"
        )

        label.place(
            relx=relx_position,
            rely=0.5,
            anchor="w"
        )


    create_header(
        "COURSE",
        0.03
    )

    create_header(
        "SEMESTER",
        0.28
    )

    create_header(
        "ACADEMIC YEAR",
        0.41
    )

    create_header(
        "TOTAL FEE",
        0.58
    )

    create_header(
        "STATUS",
        0.72
    )

    create_header(
        "ACTIONS",
        0.84
    )


    # ========================================================
    # TABLE BODY CONTAINER
    # ========================================================

    table_body_container = Frame(
        table_card,
        bg=WHITE
    )

    table_body_container.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # TABLE CANVAS
    # ========================================================

    table_canvas = Canvas(
        table_body_container,
        bg=WHITE,
        highlightthickness=0,
        bd=0
    )

    table_canvas.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # SCROLLBAR
    # ========================================================

    vertical_scrollbar = Scrollbar(
        table_body_container,
        orient=VERTICAL,
        command=table_canvas.yview
    )

    vertical_scrollbar.pack(
        side=RIGHT,
        fill=Y
    )


    table_canvas.configure(
        yscrollcommand=(
            vertical_scrollbar.set
        )
    )


    # ========================================================
    # TABLE ROW FRAME
    # ========================================================

    table_rows_frame = Frame(
        table_canvas,
        bg=WHITE
    )


    table_window = (
        table_canvas.create_window(
            (
                0,
                0
            ),
            window=table_rows_frame,
            anchor="nw"
        )
    )


    # ========================================================
    # UPDATE SCROLL REGION
    # ========================================================

    def update_scroll_region(
        event=None
    ):

        try:

            if not table_canvas.winfo_exists():
                return

            table_canvas.configure(
                scrollregion=(
                    table_canvas.bbox(
                        "all"
                    )
                )
            )

        except TclError:

            pass


    table_rows_frame.bind(
        "<Configure>",
        update_scroll_region
    )


    # ========================================================
    # RESIZE TABLE ROWS
    # ========================================================

    def resize_table_rows(
        event
    ):

        try:

            if not table_canvas.winfo_exists():
                return

            table_canvas.itemconfig(
                table_window,
                width=event.width
            )

        except TclError:

            pass


    table_canvas.bind(
        "<Configure>",
        resize_table_rows
    )


    # ========================================================
    # MOUSE WHEEL
    # ========================================================

    def mouse_wheel(
        event
    ):

        try:

            if not table_canvas.winfo_exists():
                return

            table_canvas.yview_scroll(
                int(
                    -1
                    * (
                        event.delta
                        / 120
                    )
                ),
                "units"
            )

        except TclError:

            pass


    def bind_mouse_wheel(
        event=None
    ):

        try:

            table_canvas.bind_all(
                "<MouseWheel>",
                mouse_wheel
            )

        except TclError:

            pass


    def unbind_mouse_wheel(
        event=None
    ):

        try:

            table_canvas.unbind_all(
                "<MouseWheel>"
            )

        except TclError:

            pass


    table_canvas.bind(
        "<Enter>",
        bind_mouse_wheel
    )

    table_canvas.bind(
        "<Leave>",
        unbind_mouse_wheel
    )

    table_rows_frame.bind(
        "<Enter>",
        bind_mouse_wheel
    )

    table_rows_frame.bind(
        "<Leave>",
        unbind_mouse_wheel
    )


    # ========================================================
    # CLEAR TABLE
    # ========================================================

    def clear_table():

        for widget in (
            table_rows_frame
            .winfo_children()
        ):

            widget.destroy()


    # ========================================================
    # STATUS BADGE
    # ========================================================

    def create_status_badge(
        row,
        status
    ):

        status_text = (
            str(status)
            .strip()
            .title()
        )


        if (
            status_text.lower()
            == "active"
        ):

            badge_bg = LIGHT_GREEN
            badge_fg = GREEN

        else:

            badge_bg = LIGHT_RED
            badge_fg = RED


        status_label = Label(
            row,
            text=status_text,
            bg=badge_bg,
            fg=badge_fg,
            font=(
                "Helvetica",
                8,
                "bold"
            )
        )

        status_label.place(
            relx=0.72,
            rely=0.5,
            anchor="w",
            width=75,
            height=26
        )


    # ========================================================
    # EDIT FEE STRUCTURE
    # ========================================================

    def edit_fee_structure(
        fee_structure_id
    ):

        try:

            from fee_structure_form import (
                open_fee_structure_form
            )

            open_fee_structure_form(
                parent=parent,
                refresh_callback=load_fee_structures,
                fee_structure_id=fee_structure_id
            )

        except ImportError:

            messagebox.showinfo(
                "Edit Fee Structure",
                (
                    "Edit Fee Structure\n\n"
                    f"Fee Structure ID: "
                    f"{fee_structure_id}"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "Unable to open the "
                    "Fee Structure Form."
                    f"\n\n{error}"
                )
            )


    # ========================================================
    # DELETE FEE STRUCTURE
    # ========================================================

    def delete_fee_structure(
        fee_structure_id,
        course_name,
        semester,
        academic_year
    ):

        confirm = messagebox.askyesno(
            "Delete Fee Structure",
            (
                "Are you sure you want to delete "
                "this fee structure?\n\n"
                f"Course: {course_name}\n"
                f"Semester: {semester}\n"
                f"Academic Year: {academic_year}\n\n"
                "All fee components connected to "
                "this fee structure will also "
                "be deleted."
            )
        )


        if not confirm:
            return


        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()


            cursor.execute(
                """
                DELETE FROM fee_structures
                WHERE Fee_Structure_ID = %s
                """,
                (
                    fee_structure_id,
                )
            )


            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Not Found",
                    (
                        "The selected fee structure "
                        "was not found."
                    )
                )

                return


            con.commit()


            messagebox.showinfo(
                "Deleted",
                (
                    "Fee structure deleted "
                    "successfully."
                )
            )


            load_fee_structures(
                get_search_text()
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
                    "Unable to delete "
                    "fee structure."
                    "\n\n"
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
    # CREATE FEE STRUCTURE ROW
    # ========================================================

    def create_fee_structure_row(
        fee_structure
    ):

        (
            fee_structure_id,
            course_name,
            semester,
            academic_year,
            total_fee,
            status
        ) = fee_structure


        # ----------------------------------------------------
        # ROW
        # ----------------------------------------------------

        row = Frame(
            table_rows_frame,
            bg=WHITE,
            height=58
        )

        row.pack(
            fill=X
        )

        row.pack_propagate(
            False
        )


        # ----------------------------------------------------
        # COURSE
        # ----------------------------------------------------

        course_label = Label(
            row,
            text=course_name,
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            anchor="w"
        )

        course_label.place(
            relx=0.03,
            rely=0.5,
            anchor="w"
        )


        # ----------------------------------------------------
        # SEMESTER
        # ----------------------------------------------------

        semester_label = Label(
            row,
            text=str(
                semester
            ),
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                9
            ),
            anchor="w"
        )

        semester_label.place(
            relx=0.28,
            rely=0.5,
            anchor="w"
        )


        # ----------------------------------------------------
        # ACADEMIC YEAR
        # ----------------------------------------------------

        academic_year_label = Label(
            row,
            text=str(
                academic_year
            ),
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                9
            ),
            anchor="w"
        )

        academic_year_label.place(
            relx=0.41,
            rely=0.5,
            anchor="w"
        )


        # ----------------------------------------------------
        # TOTAL FEE
        # ----------------------------------------------------

        try:

            total_fee_value = float(
                total_fee
            )

        except:

            total_fee_value = 0


        total_fee_label = Label(
            row,
            text=(
                f"₹"
                f"{total_fee_value:,.2f}"
            ),
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            anchor="w"
        )

        total_fee_label.place(
            relx=0.58,
            rely=0.5,
            anchor="w"
        )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        create_status_badge(
            row,
            status
        )


        # ----------------------------------------------------
        # EDIT BUTTON
        # ----------------------------------------------------

        edit_button = Button(
            row,
            text="EDIT",
            bg=LIGHT_BLUE,
            fg=BLUE,
            activebackground=BLUE,
            activeforeground=WHITE,
            font=(
                "Helvetica",
                8,
                "bold"
            ),
            bd=0,
            relief=FLAT,
            highlightthickness=0,
            cursor="hand2",
            command=lambda
                structure_id=fee_structure_id:
                edit_fee_structure(
                    structure_id
                )
        )

        edit_button.place(
            relx=0.84,
            rely=0.5,
            anchor="w",
            width=55,
            height=28
        )


        # ----------------------------------------------------
        # DELETE BUTTON
        # ----------------------------------------------------

        delete_button = Button(
            row,
            text="DELETE",
            bg=LIGHT_RED,
            fg=RED,
            activebackground=RED,
            activeforeground=WHITE,
            font=(
                "Helvetica",
                8,
                "bold"
            ),
            bd=0,
            relief=FLAT,
            highlightthickness=0,
            cursor="hand2",
            command=lambda
                structure_id=fee_structure_id,
                selected_course=course_name,
                selected_semester=semester,
                selected_year=academic_year:
                delete_fee_structure(
                    structure_id,
                    selected_course,
                    selected_semester,
                    selected_year
                )
        )

        delete_button.place(
            relx=0.91,
            rely=0.5,
            anchor="w",
            width=65,
            height=28
        )


        # ----------------------------------------------------
        # ROW BORDER
        # ----------------------------------------------------

        row_border = Frame(
            row,
            bg=BORDER_COLOR,
            height=1
        )

        row_border.place(
            x=0,
            rely=1.0,
            relwidth=1.0,
            anchor="sw"
        )


    # ========================================================
    # EMPTY STATE
    # ========================================================

    def show_empty_fee_state(
        message="No fee structures found"
    ):

        clear_table()


        empty_frame = Frame(
            table_rows_frame,
            bg=WHITE,
            height=240
        )

        empty_frame.pack(
            fill=X
        )

        empty_frame.pack_propagate(
            False
        )


        empty_icon = Label(
            empty_frame,
            text="₹",
            bg=LIGHT_BLUE,
            fg=BLUE,
            font=(
                "Helvetica",
                18,
                "bold"
            )
        )

        empty_icon.place(
            relx=0.5,
            y=70,
            anchor="center",
            width=50,
            height=50
        )


        empty_title = Label(
            empty_frame,
            text=message,
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                11,
                "bold"
            )
        )

        empty_title.place(
            relx=0.5,
            y=140,
            anchor="center"
        )


        empty_subtitle = Label(
            empty_frame,
            text=(
                "Create a fee structure to "
                "manage course and semester fees."
            ),
            bg=WHITE,
            fg=GRAY,
            font=(
                "Helvetica",
                9
            )
        )

        empty_subtitle.place(
            relx=0.5,
            y=170,
            anchor="center"
        )


    # ========================================================
    # LOAD FEE STRUCTURES
    # ========================================================

    def load_fee_structures(
        search_text=""
    ):

        clear_table()


        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()


            query = """
                SELECT
                    fs.Fee_Structure_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year,

                    COALESCE(
                        SUM(
                            fsc.Amount
                        ),
                        0
                    ) AS Total_Fee,

                    fs.Status

                FROM fee_structures fs

                INNER JOIN courses c
                    ON fs.Course_ID =
                       c.Course_ID

                LEFT JOIN
                    fee_structure_components fsc

                    ON fs.Fee_Structure_ID =
                       fsc.Fee_Structure_ID
            """


            parameters = []


            # ------------------------------------------------
            # SEARCH
            # ------------------------------------------------

            if search_text:

                query += """
                    WHERE
                        c.Course_Name LIKE %s

                        OR CAST(
                            fs.Semester
                            AS CHAR
                        )
                        LIKE %s

                        OR fs.Academic_Year
                        LIKE %s

                        OR fs.Status
                        LIKE %s
                """


                search_pattern = (
                    f"%{search_text}%"
                )


                parameters = [

                    search_pattern,

                    search_pattern,

                    search_pattern,

                    search_pattern
                ]


            # ------------------------------------------------
            # GROUP AND ORDER
            # ------------------------------------------------

            query += """
                GROUP BY
                    fs.Fee_Structure_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year,
                    fs.Status

                ORDER BY
                    c.Course_Name ASC,
                    fs.Academic_Year DESC,
                    fs.Semester ASC
            """


            cursor.execute(
                query,
                tuple(
                    parameters
                )
            )


            fee_structures = (
                cursor.fetchall()
            )


            # ------------------------------------------------
            # COUNT
            # ------------------------------------------------

            total_count = len(
                fee_structures
            )


            if total_count == 1:

                count_label.config(
                    text="1 Fee Structure"
                )

            else:

                count_label.config(
                    text=(
                        f"{total_count} "
                        f"Fee Structures"
                    )
                )


            # ------------------------------------------------
            # EMPTY
            # ------------------------------------------------

            if not fee_structures:

                if search_text:

                    show_empty_fee_state(
                        (
                            "No matching fee "
                            "structures found"
                        )
                    )

                else:

                    show_empty_fee_state(
                        "No fee structures found"
                    )

                return


            # ------------------------------------------------
            # CREATE ROWS
            # ------------------------------------------------

            for fee_structure in (
                fee_structures
            ):

                create_fee_structure_row(
                    fee_structure
                )


            # ------------------------------------------------
            # RESET SCROLL
            # ------------------------------------------------

            table_canvas.yview_moveto(
                0
            )


        except mysql.connector.Error as error:

            count_label.config(
                text="0 Fee Structures"
            )


            show_empty_fee_state(
                (
                    "Unable to load "
                    "fee structures"
                )
            )


            messagebox.showerror(
                "Database Error",
                (
                    "Unable to load "
                    "fee structures."
                    "\n\n"
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
    # SEARCH FUNCTION
    # ========================================================

    def search_fee_structures():

        search_text = (
            get_search_text()
        )

        load_fee_structures(
            search_text
        )


    # ========================================================
    # CLEAR SEARCH
    # ========================================================

    def clear_search():

        search_var.set("")

        set_search_placeholder()

        load_fee_structures()


    # ========================================================
    # CONNECT BUTTONS
    # ========================================================

    search_button.config(
        command=search_fee_structures
    )


    clear_button.config(
        command=clear_search
    )


    # ========================================================
    # ENTER KEY SEARCH
    # ========================================================

    search_entry.bind(
        "<Return>",
        lambda event:
        search_fee_structures()
    )


    # ========================================================
    # INITIAL PAGE LOAD
    # ========================================================

    set_search_placeholder()

    load_fee_structures()