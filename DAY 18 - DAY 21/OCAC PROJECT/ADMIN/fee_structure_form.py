from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
DARK_BLUE = "#1D4ED8"

WHITE = "#FFFFFF"
BACKGROUND = "#F8FAFC"

TEXT_COLOR = "#0F172A"
GRAY = "#64748B"

BORDER_COLOR = "#CBD5E1"
LIGHT_BORDER = "#E2E8F0"

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


def academic_session_label(start_year):
    return f"{start_year}-{str(start_year + 1)[-2:]}"


def current_academic_session():
    today = date.today()
    start_year = today.year if today.month >= 4 else today.year - 1
    return academic_session_label(start_year)


def academic_year_options():
    today = date.today()
    current_start_year = today.year if today.month >= 4 else today.year - 1
    first_start_year = max(2020, current_start_year - 8)
    return [
        academic_session_label(year)
        for year in range(first_start_year, current_start_year + 1)
    ]


def normalize_academic_year(value):
    value = (value or "").strip()
    if not value:
        return current_academic_session()

    if "-" in value:
        return value

    try:
        start_year = int(value)
    except ValueError:
        return value

    return academic_session_label(start_year)


# ============================================================
# OPEN FEE STRUCTURE FORM
# ============================================================

def open_fee_structure_form(
    parent,
    refresh_callback=None,
    fee_structure_id=None
):

    # ========================================================
    # MODE
    # ========================================================

    is_edit_mode = fee_structure_id is not None


    # ========================================================
    # WINDOW
    # ========================================================

    form_window = Toplevel(parent)

    form_window.title(
        "Edit Fee Structure"
        if is_edit_mode
        else "Add Fee Structure"
    )

    form_window.configure(bg=BACKGROUND)

    form_window.resizable(True, True)

    form_window.minsize(900, 650)


    # ========================================================
    # WINDOW POSITION
    # ========================================================

    window_width = 950
    window_height = 700

    form_window.update_idletasks()

    screen_width = form_window.winfo_screenwidth()
    screen_height = form_window.winfo_screenheight()

    x_position = max(
        0,
        (screen_width - window_width) // 2
    )

    # Move window upward
    y_position = max(
        20,
        (screen_height - window_height) // 2 - 45
    )

    form_window.geometry(
        f"{window_width}x{window_height}"
        f"+{x_position}+{y_position}"
    )


    # ========================================================
    # MODAL WINDOW
    # ========================================================

    try:
        form_window.transient(
            parent.winfo_toplevel()
        )
    except TclError:
        pass

    form_window.grab_set()


    # ========================================================
    # VARIABLES
    # ========================================================

    course_var = StringVar()
    semester_var = StringVar()

    academic_year_var = StringVar(
        value=current_academic_session()
    )

    status_var = StringVar(
        value="Active"
    )


    # ========================================================
    # DATA
    # ========================================================

    course_map = {}

    # Example:
    #
    # [
    #     {
    #         "name": "Tuition Fee",
    #         "amount": 50000.00
    #     }
    # ]

    fee_components = []


    # ========================================================
    # CLOSE FORM
    # ========================================================

    def close_form():

        try:
            form_window.grab_release()
        except TclError:
            pass

        form_window.destroy()


    # ========================================================
    # CLOSE AND REFRESH
    # ========================================================

    def close_and_refresh():

        close_form()

        if refresh_callback:

            try:
                refresh_callback()
            except Exception:
                pass


    form_window.protocol(
        "WM_DELETE_WINDOW",
        close_form
    )


    # ========================================================
    # MAIN HEADER
    # ========================================================

    header = Frame(
        form_window,
        bg=BACKGROUND
    )

    header.pack(
        fill=X,
        padx=35,
        pady=(18, 12)
    )


    Label(
        header,
        text=(
            "Edit Fee Structure"
            if is_edit_mode
            else "Add Fee Structure"
        ),
        bg=BACKGROUND,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            21,
            "bold"
        )
    ).pack(
        anchor="w"
    )


    Label(
        header,
        text=(
            "Create a standard semester fee "
            "structure for a course."
        ),
        bg=BACKGROUND,
        fg=GRAY,
        font=(
            "Helvetica",
            10
        )
    ).pack(
        anchor="w",
        pady=(4, 0)
    )


    # ========================================================
    # BOTTOM ACTION BAR
    #
    # IMPORTANT:
    # Packed before the main card so buttons remain visible.
    # ========================================================

    actions = Frame(
        form_window,
        bg=BACKGROUND
    )

    actions.pack(
        side=BOTTOM,
        fill=X,
        padx=35,
        pady=(5, 15)
    )


    # ========================================================
    # MAIN CARD
    # ========================================================

    card = Frame(
        form_window,
        bg=WHITE,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    card.pack(
        fill=BOTH,
        expand=True,
        padx=35,
        pady=(0, 5)
    )


    # ========================================================
    # FEE STRUCTURE INFORMATION
    # ========================================================

    Label(
        card,
        text="FEE STRUCTURE INFORMATION",
        bg=WHITE,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            12,
            "bold"
        )
    ).pack(
        anchor="w",
        padx=28,
        pady=(18, 4)
    )


    Label(
        card,
        text=(
            "Select the course, semester "
            "and academic year."
        ),
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            9
        )
    ).pack(
        anchor="w",
        padx=28
    )


    # ========================================================
    # DIVIDER
    # ========================================================

    Frame(
        card,
        bg=LIGHT_BORDER,
        height=1
    ).pack(
        fill=X,
        padx=28,
        pady=12
    )


    # ========================================================
    # INFORMATION GRID
    # ========================================================

    information_grid = Frame(
        card,
        bg=WHITE
    )

    information_grid.pack(
        fill=X,
        padx=28
    )


    for column in range(3):

        information_grid.grid_columnconfigure(
            column,
            weight=1,
            uniform="info"
        )


    # ========================================================
    # CREATE COMBOBOX FIELD
    # ========================================================

    def create_combo_field(
        parent_frame,
        label_text,
        variable,
        row,
        column
    ):

        field_frame = Frame(
            parent_frame,
            bg=WHITE
        )

        field_frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=10,
            pady=6
        )


        Label(
            field_frame,
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
            pady=(0, 6)
        )


        combo = ttk.Combobox(
            field_frame,
            textvariable=variable,
            state="readonly",
            font=(
                "Helvetica",
                10
            )
        )

        combo.pack(
            fill=X,
            ipady=5
        )

        return combo


    # ========================================================
    # COURSE
    # ========================================================

    course_combo = create_combo_field(
        information_grid,
        "Course",
        course_var,
        0,
        0
    )


    # ========================================================
    # SEMESTER
    # ========================================================

    semester_combo = create_combo_field(
        information_grid,
        "Semester",
        semester_var,
        0,
        1
    )


    # ========================================================
    # ACADEMIC YEAR
    # ========================================================

    academic_year_frame = Frame(
        information_grid,
        bg=WHITE
    )

    academic_year_frame.grid(
        row=0,
        column=2,
        sticky="ew",
        padx=10,
        pady=6
    )


    Label(
        academic_year_frame,
        text="Academic Year",
        bg=WHITE,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            9,
            "bold"
        )
    ).pack(
        anchor="w",
        pady=(0, 6)
    )


    academic_year_combo = ttk.Combobox(
        academic_year_frame,
        textvariable=academic_year_var,
        values=academic_year_options(),
        state="readonly",
        font=(
            "Helvetica",
            10
        )
    )

    academic_year_combo.pack(
        fill=X,
        ipady=7
    )


    # ========================================================
    # STATUS
    # ========================================================

    status_combo = create_combo_field(
        information_grid,
        "Status",
        status_var,
        1,
        0
    )

    status_combo["values"] = [
        "Active",
        "Inactive"
    ]


    # ========================================================
    # DIVIDER
    # ========================================================

    Frame(
        card,
        bg=LIGHT_BORDER,
        height=1
    ).pack(
        fill=X,
        padx=28,
        pady=(12, 14)
    )


    # ========================================================
    # COMPONENT HEADER
    # ========================================================

    component_header = Frame(
        card,
        bg=WHITE
    )

    component_header.pack(
        fill=X,
        padx=38
    )


    component_header_left = Frame(
        component_header,
        bg=WHITE
    )

    component_header_left.pack(
        side=LEFT
    )


    Label(
        component_header_left,
        text="FEE COMPONENTS",
        bg=WHITE,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            12,
            "bold"
        )
    ).pack(
        anchor="w"
    )


    Label(
        component_header_left,
        text=(
            "Add the individual fees "
            "included in this structure."
        ),
        bg=WHITE,
        fg=GRAY,
        font=(
            "Helvetica",
            9
        )
    ).pack(
        anchor="w",
        pady=(3, 0)
    )


    # ========================================================
    # COMPONENT TABLE
    # ========================================================

    component_table = Frame(
        card,
        bg=WHITE,
        highlightbackground=LIGHT_BORDER,
        highlightthickness=1
    )

    component_table.pack(
        fill=BOTH,
        expand=True,
        padx=38,
        pady=(12, 8)
    )


    # ========================================================
    # TABLE HEADER
    # ========================================================

    component_table_header = Frame(
        component_table,
        bg=BACKGROUND,
        height=38
    )

    component_table_header.pack(
        fill=X
    )

    component_table_header.pack_propagate(
        False
    )


    Label(
        component_table_header,
        text="COMPONENT NAME",
        bg=BACKGROUND,
        fg=GRAY,
        font=(
            "Helvetica",
            8,
            "bold"
        )
    ).place(
        relx=0.04,
        rely=0.5,
        anchor="w"
    )


    Label(
        component_table_header,
        text="AMOUNT",
        bg=BACKGROUND,
        fg=GRAY,
        font=(
            "Helvetica",
            8,
            "bold"
        )
    ).place(
        relx=0.63,
        rely=0.5,
        anchor="w"
    )


    Label(
        component_table_header,
        text="ACTION",
        bg=BACKGROUND,
        fg=GRAY,
        font=(
            "Helvetica",
            8,
            "bold"
        )
    ).place(
        relx=0.84,
        rely=0.5,
        anchor="w"
    )


    # ========================================================
    # TABLE BODY
    # ========================================================

    component_body = Frame(
        component_table,
        bg=WHITE
    )

    component_body.pack(
        fill=BOTH,
        expand=True
    )


    component_canvas = Canvas(
        component_body,
        bg=WHITE,
        highlightthickness=0,
        height=115
    )


    component_scrollbar = Scrollbar(
        component_body,
        orient=VERTICAL,
        command=component_canvas.yview
    )


    component_rows = Frame(
        component_canvas,
        bg=WHITE
    )


    component_window = (
        component_canvas.create_window(
            (0, 0),
            window=component_rows,
            anchor="nw"
        )
    )


    component_canvas.configure(
        yscrollcommand=component_scrollbar.set
    )


    component_canvas.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )


    component_scrollbar.pack(
        side=RIGHT,
        fill=Y
    )


    # ========================================================
    # CANVAS EVENTS
    # ========================================================

    def update_component_scroll(
        event=None
    ):

        component_canvas.configure(
            scrollregion=(
                component_canvas.bbox(
                    "all"
                )
            )
        )


    def update_component_width(
        event
    ):

        component_canvas.itemconfig(
            component_window,
            width=event.width
        )


    component_rows.bind(
        "<Configure>",
        update_component_scroll
    )


    component_canvas.bind(
        "<Configure>",
        update_component_width
    )


    # ========================================================
    # SUMMARY VARIABLES
    # ========================================================

    component_count_var = StringVar(
        value="0 Fee Components"
    )


    total_fee_var = StringVar(
        value="TOTAL FEE: ₹0.00"
    )


    # ========================================================
    # CALCULATE TOTAL
    # ========================================================

    def calculate_total():

        total = sum(
            component["amount"]
            for component
            in fee_components
        )

        count = len(
            fee_components
        )


        component_count_var.set(
            (
                "1 Fee Component"
                if count == 1
                else f"{count} Fee Components"
            )
        )


        total_fee_var.set(
            f"TOTAL FEE: ₹{total:,.2f}"
        )


    # ========================================================
    # REMOVE COMPONENT
    # ========================================================

    def remove_component(
        index
    ):

        if (
            0 <= index
            < len(fee_components)
        ):

            del fee_components[index]

            refresh_component_table()


    # ========================================================
    # REFRESH COMPONENT TABLE
    # ========================================================

    def refresh_component_table():

        for widget in (
            component_rows.winfo_children()
        ):
            widget.destroy()


        # ----------------------------------------------------
        # EMPTY STATE
        # ----------------------------------------------------

        if not fee_components:

            empty_frame = Frame(
                component_rows,
                bg=WHITE,
                height=95
            )

            empty_frame.pack(
                fill=X
            )

            empty_frame.pack_propagate(
                False
            )


            Label(
                empty_frame,
                text="No fee components added",
                bg=WHITE,
                fg=TEXT_COLOR,
                font=(
                    "Helvetica",
                    10,
                    "bold"
                )
            ).pack(
                pady=(24, 4)
            )


            Label(
                empty_frame,
                text=(
                    "Click + ADD COMPONENT "
                    "to add a fee."
                ),
                bg=WHITE,
                fg=GRAY,
                font=(
                    "Helvetica",
                    9
                )
            ).pack()


        # ----------------------------------------------------
        # COMPONENT ROWS
        # ----------------------------------------------------

        else:

            for index, component in enumerate(
                fee_components
            ):

                row = Frame(
                    component_rows,
                    bg=WHITE,
                    height=50
                )

                row.pack(
                    fill=X
                )

                row.pack_propagate(
                    False
                )


                Label(
                    row,
                    text=component["name"],
                    bg=WHITE,
                    fg=TEXT_COLOR,
                    font=(
                        "Helvetica",
                        9,
                        "bold"
                    )
                ).place(
                    relx=0.04,
                    rely=0.5,
                    anchor="w"
                )


                Label(
                    row,
                    text=(
                        f"₹"
                        f"{component['amount']:,.2f}"
                    ),
                    bg=WHITE,
                    fg=TEXT_COLOR,
                    font=(
                        "Helvetica",
                        9,
                        "bold"
                    )
                ).place(
                    relx=0.63,
                    rely=0.5,
                    anchor="w"
                )


                Button(
                    row,
                    text="REMOVE",
                    bg=LIGHT_RED,
                    fg=RED,
                    activebackground=RED,
                    activeforeground=WHITE,
                    bd=0,
                    relief=FLAT,
                    cursor="hand2",
                    font=(
                        "Helvetica",
                        8,
                        "bold"
                    ),
                    command=lambda i=index:
                    remove_component(i)
                ).place(
                    relx=0.84,
                    rely=0.5,
                    anchor="w",
                    width=72,
                    height=27
                )


                Frame(
                    row,
                    bg=LIGHT_BORDER,
                    height=1
                ).place(
                    x=0,
                    rely=1.0,
                    relwidth=1.0,
                    anchor="sw"
                )


        calculate_total()


    # ========================================================
    # ADD COMPONENT POPUP
    # ========================================================

    def open_add_component_window():

        component_popup = Toplevel(
            form_window
        )

        component_popup.title(
            "Add Fee Component"
        )


        # ====================================================
        # POPUP SIZE
        # ====================================================

        popup_width = 460
        popup_height = 360


        component_popup.configure(
            bg=BACKGROUND
        )


        component_popup.resizable(
            False,
            False
        )


        component_popup.transient(
            form_window
        )


        # ====================================================
        # POSITION POPUP UPWARD
        # ====================================================

        component_popup.update_idletasks()

        screen_width = (
            component_popup.winfo_screenwidth()
        )

        screen_height = (
            component_popup.winfo_screenheight()
        )


        popup_x = max(
            0,
            (screen_width - popup_width) // 2
        )


        popup_y = max(
            20,
            (screen_height - popup_height) // 2 - 100
        )


        component_popup.geometry(
            f"{popup_width}x{popup_height}"
            f"+{popup_x}+{popup_y}"
        )


        component_popup.grab_set()


        # ====================================================
        # VARIABLES
        # ====================================================

        component_name_var = StringVar()
        component_amount_var = StringVar()


        # ====================================================
        # HEADER
        # ====================================================

        Label(
            component_popup,
            text="Add Fee Component",
            bg=BACKGROUND,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                18,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(22, 3)
        )


        Label(
            component_popup,
            text=(
                "Enter the component "
                "name and amount."
            ),
            bg=BACKGROUND,
            fg=GRAY,
            font=(
                "Helvetica",
                9
            )
        ).pack(
            anchor="w",
            padx=30
        )


        # ====================================================
        # CARD
        # ====================================================

        popup_card = Frame(
            component_popup,
            bg=WHITE,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        popup_card.pack(
            fill=BOTH,
            expand=True,
            padx=30,
            pady=(16, 20)
        )


        # ====================================================
        # COMPONENT NAME
        # ====================================================

        Label(
            popup_card,
            text="Component Name",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(18, 6)
        )


        component_name_entry = Entry(
            popup_card,
            textvariable=component_name_var,
            bg=WHITE,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            font=(
                "Helvetica",
                10
            ),
            relief=SOLID,
            bd=1
        )

        component_name_entry.pack(
            fill=X,
            padx=22,
            ipady=7
        )


        # ====================================================
        # AMOUNT
        # ====================================================

        Label(
            popup_card,
            text="Amount (₹)",
            bg=WHITE,
            fg=TEXT_COLOR,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(14, 6)
        )


        component_amount_entry = Entry(
            popup_card,
            textvariable=component_amount_var,
            bg=WHITE,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            font=(
                "Helvetica",
                10
            ),
            relief=SOLID,
            bd=1
        )

        component_amount_entry.pack(
            fill=X,
            padx=22,
            ipady=7
        )


        # ====================================================
        # CLEAR COMPONENT FORM
        # ====================================================

        def clear_component_form():

            component_name_var.set("")
            component_amount_var.set("")

            component_name_entry.focus_set()


        # ====================================================
        # ADD COMPONENT
        # ====================================================

        def add_component():

            component_name = (
                component_name_var
                .get()
                .strip()
            )


            amount_text = (
                component_amount_var
                .get()
                .strip()
            )


            # -----------------------------------------------
            # VALIDATE NAME
            # -----------------------------------------------

            if not component_name:

                messagebox.showwarning(
                    "Required Field",
                    (
                        "Please enter the "
                        "Component Name."
                    ),
                    parent=component_popup
                )

                component_name_entry.focus_set()

                return


            # -----------------------------------------------
            # VALIDATE AMOUNT
            # -----------------------------------------------

            try:

                component_amount = float(
                    amount_text
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Amount",
                    (
                        "Please enter a valid "
                        "numeric amount."
                    ),
                    parent=component_popup
                )

                component_amount_entry.focus_set()

                return


            if component_amount <= 0:

                messagebox.showwarning(
                    "Invalid Amount",
                    (
                        "Amount must be "
                        "greater than 0."
                    ),
                    parent=component_popup
                )

                component_amount_entry.focus_set()

                return


            # -----------------------------------------------
            # DUPLICATE COMPONENT CHECK
            # -----------------------------------------------

            for component in fee_components:

                if (
                    component["name"]
                    .strip()
                    .lower()
                    ==
                    component_name.lower()
                ):

                    messagebox.showwarning(
                        "Duplicate Component",
                        (
                            "This fee component "
                            "has already been added."
                        ),
                        parent=component_popup
                    )

                    return


            # -----------------------------------------------
            # ADD TO TEMPORARY LIST
            # -----------------------------------------------

            fee_components.append(
                {
                    "name": component_name,
                    "amount": round(
                        component_amount,
                        2
                    )
                }
            )


            # -----------------------------------------------
            # REFRESH MAIN TABLE
            # -----------------------------------------------

            refresh_component_table()


            # -----------------------------------------------
            # CLOSE POPUP
            # -----------------------------------------------

            component_popup.destroy()


        # ====================================================
        # BUTTON AREA
        # ====================================================

        button_frame = Frame(
            popup_card,
            bg=WHITE
        )

        button_frame.pack(
            side=BOTTOM,
            fill=X,
            padx=22,
            pady=(15, 18)
        )


        # ====================================================
        # CLEAR BUTTON
        # ====================================================

        Button(
            button_frame,
            text="CLEAR",
            bg=WHITE,
            fg=TEXT_COLOR,
            activebackground="#F1F5F9",
            activeforeground=TEXT_COLOR,
            relief=SOLID,
            bd=1,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=clear_component_form
        ).pack(
            side=RIGHT,
            ipadx=18,
            ipady=7
        )


        # ====================================================
        # ADD BUTTON
        # ====================================================

        Button(
            button_frame,
            text="ADD",
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            command=add_component
        ).pack(
            side=RIGHT,
            padx=(0, 10),
            ipadx=25,
            ipady=8
        )


        # ====================================================
        # ENTER KEY EVENTS
        # ====================================================

        component_name_entry.bind(
            "<Return>",
            lambda event:
            component_amount_entry.focus_set()
        )


        component_amount_entry.bind(
            "<Return>",
            lambda event:
            add_component()
        )


        component_name_entry.focus_set()


    # ========================================================
    # ADD COMPONENT BUTTON
    # ========================================================

    Button(
        component_header,
        text="+ ADD COMPONENT",
        bg=BLUE,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        bd=0,
        relief=FLAT,
        cursor="hand2",
        font=(
            "Helvetica",
            9,
            "bold"
        ),
        command=open_add_component_window
    ).pack(
        side=RIGHT,
        ipadx=15,
        ipady=8
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    summary = Frame(
        card,
        bg=LIGHT_GREEN,
        highlightbackground="#BBF7D0",
        highlightthickness=1
    )

    summary.pack(
        fill=X,
        padx=38,
        pady=(0, 12)
    )


    Label(
        summary,
        textvariable=component_count_var,
        bg=LIGHT_GREEN,
        fg=GREEN,
        font=(
            "Helvetica",
            10,
            "bold"
        )
    ).pack(
        side=LEFT,
        padx=15,
        pady=10
    )


    Label(
        summary,
        textvariable=total_fee_var,
        bg=LIGHT_GREEN,
        fg=TEXT_COLOR,
        font=(
            "Helvetica",
            10,
            "bold"
        )
    ).pack(
        side=RIGHT,
        padx=15,
        pady=10
    )


    # ========================================================
    # LOAD COURSES
    # ========================================================

    def load_courses():

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
                    Total_Semesters

                FROM courses

                WHERE
                    LOWER(TRIM(Status)) = 'active'

                ORDER BY
                    Course_Name
                """
            )


            records = cursor.fetchall()


            course_map.clear()

            course_names = []


            for (
                course_id,
                course_name,
                total_semesters
            ) in records:

                course_map[
                    course_name
                ] = {
                    "course_id": course_id,
                    "total_semesters": int(
                        total_semesters
                    )
                }


                course_names.append(
                    course_name
                )


            course_combo[
                "values"
            ] = course_names


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load courses."
                    f"\n\n{error}"
                ),
                parent=form_window
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
    # UPDATE SEMESTERS
    # ========================================================

    def update_semesters(
        event=None
    ):

        selected_course = (
            course_var
            .get()
            .strip()
        )


        if selected_course not in course_map:

            semester_combo[
                "values"
            ] = []

            semester_var.set("")

            return


        total_semesters = (
            course_map[
                selected_course
            ][
                "total_semesters"
            ]
        )


        semester_values = [

            str(semester)

            for semester in range(
                1,
                total_semesters + 1
            )
        ]


        semester_combo[
            "values"
        ] = semester_values


        if (
            semester_var.get()
            not in semester_values
        ):

            semester_var.set("")


    course_combo.bind(
        "<<ComboboxSelected>>",
        update_semesters
    )


    # ========================================================
    # VALIDATE FORM
    # ========================================================

    def validate_form():

        selected_course = (
            course_var
            .get()
            .strip()
        )


        # ----------------------------------------------------
        # COURSE
        # ----------------------------------------------------

        if selected_course not in course_map:

            messagebox.showwarning(
                "Required Field",
                "Please select a valid Course.",
                parent=form_window
            )

            course_combo.focus_set()

            return None


        # ----------------------------------------------------
        # SEMESTER
        # ----------------------------------------------------

        semester_text = (
            semester_var
            .get()
            .strip()
        )


        if not semester_text:

            messagebox.showwarning(
                "Required Field",
                "Please select the Semester.",
                parent=form_window
            )

            semester_combo.focus_set()

            return None


        try:

            semester = int(
                semester_text
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Semester",
                "Please select a valid Semester.",
                parent=form_window
            )

            return None


        # ----------------------------------------------------
        # ACADEMIC YEAR
        # ----------------------------------------------------

        academic_year = (
            academic_year_var
            .get()
            .strip()
        )


        if not academic_year:

            messagebox.showwarning(
                "Required Field",
                "Please select the Academic Year.",
                parent=form_window
            )

            academic_year_combo.focus_set()

            return None


        # ----------------------------------------------------
        # COMPONENTS
        # ----------------------------------------------------

        if not fee_components:

            messagebox.showwarning(
                "No Fee Components",
                (
                    "Please add at least "
                    "one Fee Component."
                ),
                parent=form_window
            )

            return None


        # ----------------------------------------------------
        # RETURN DATA
        # ----------------------------------------------------

        return {

            "course_id":
                course_map[
                    selected_course
                ][
                    "course_id"
                ],

            "course_name":
                selected_course,

            "semester":
                semester,

            "academic_year":
                academic_year,

            "status":
                status_var
                .get()
                .strip()
        }


    # ========================================================
    # SAVE FEE STRUCTURE
    # ========================================================

    def save_fee_structure():

        data = validate_form()


        if data is None:
            return


        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor()


            # =================================================
            # DUPLICATE CHECK
            # =================================================

            if is_edit_mode:

                cursor.execute(
                    """
                    SELECT
                        Fee_Structure_ID

                    FROM fee_structures

                    WHERE
                        Course_ID = %s

                    AND
                        Semester = %s

                    AND
                        Academic_Year = %s

                    AND
                        Fee_Structure_ID <> %s
                    """,
                    (
                        data["course_id"],
                        data["semester"],
                        data["academic_year"],
                        fee_structure_id
                    )
                )


            else:

                cursor.execute(
                    """
                    SELECT
                        Fee_Structure_ID

                    FROM fee_structures

                    WHERE
                        Course_ID = %s

                    AND
                        Semester = %s

                    AND
                        Academic_Year = %s
                    """,
                    (
                        data["course_id"],
                        data["semester"],
                        data["academic_year"]
                    )
                )


            duplicate = cursor.fetchone()


            if duplicate:

                messagebox.showwarning(
                    "Duplicate Fee Structure",
                    (
                        "A fee structure already "
                        "exists for:\n\n"

                        f"Course: "
                        f"{data['course_name']}\n"

                        f"Semester: "
                        f"{data['semester']}\n"

                        f"Academic Year: "
                        f"{data['academic_year']}"
                    ),
                    parent=form_window
                )

                return


            # =================================================
            # EDIT MODE
            # =================================================

            if is_edit_mode:

                current_fee_structure_id = int(
                    fee_structure_id
                )


                cursor.execute(
                    """
                    UPDATE fee_structures

                    SET
                        Course_ID = %s,
                        Semester = %s,
                        Academic_Year = %s,
                        Status = %s

                    WHERE
                        Fee_Structure_ID = %s
                    """,
                    (
                        data["course_id"],
                        data["semester"],
                        data["academic_year"],
                        data["status"],
                        current_fee_structure_id
                    )
                )


                # ---------------------------------------------
                # DELETE OLD COMPONENTS
                # ---------------------------------------------

                cursor.execute(
                    """
                    DELETE FROM
                        fee_structure_components

                    WHERE
                        Fee_Structure_ID = %s
                    """,
                    (
                        current_fee_structure_id,
                    )
                )


            # =================================================
            # ADD MODE
            # =================================================

            else:

                cursor.execute(
                    """
                    INSERT INTO fee_structures
                    (
                        Course_ID,
                        Semester,
                        Academic_Year,
                        Status
                    )

                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        data["course_id"],
                        data["semester"],
                        data["academic_year"],
                        data["status"]
                    )
                )


                current_fee_structure_id = (
                    cursor.lastrowid
                )


            # =================================================
            # INSERT FEE COMPONENTS
            #
            # CORRECT DATABASE COLUMNS:
            #
            # Fee_Structure_ID
            # Fee_Type
            # Amount
            # =================================================

            for component in fee_components:

                cursor.execute(
                    """
                    INSERT INTO fee_structure_components
                    (
                        Fee_Structure_ID,
                        Fee_Type,
                        Amount
                    )

                    VALUES
                    (
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        current_fee_structure_id,
                        component["name"],
                        component["amount"]
                    )
                )


            # =================================================
            # COMMIT
            # =================================================

            con.commit()


            # =================================================
            # SUCCESS
            # =================================================

            messagebox.showinfo(
                "Success",
                (
                    "Fee structure updated successfully."
                    if is_edit_mode
                    else
                    "Fee structure created successfully."
                ),
                parent=form_window
            )


            close_and_refresh()


        except mysql.connector.Error as error:

            if con is not None:

                try:
                    con.rollback()
                except Exception:
                    pass


            messagebox.showerror(
                "Database Error",
                (
                    "Could not save the "
                    "Fee Structure."
                    f"\n\n{error}"
                ),
                parent=form_window
            )


        finally:

            if cursor is not None:

                try:
                    cursor.close()
                except Exception:
                    pass


            if (
                con is not None
                and con.is_connected()
            ):
                con.close()


    # ========================================================
    # LOAD EDIT DATA
    # ========================================================

    def load_edit_data():

        if not is_edit_mode:
            return


        con = None
        cursor = None


        try:

            con = get_connection()

            cursor = con.cursor(
                dictionary=True
            )


            # -------------------------------------------------
            # LOAD MAIN FEE STRUCTURE
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    fs.Fee_Structure_ID,
                    fs.Course_ID,
                    c.Course_Name,
                    fs.Semester,
                    fs.Academic_Year,
                    fs.Status

                FROM fee_structures fs

                INNER JOIN courses c
                    ON
                        fs.Course_ID
                        =
                        c.Course_ID

                WHERE
                    fs.Fee_Structure_ID = %s
                """,
                (
                    fee_structure_id,
                )
            )


            record = cursor.fetchone()


            if not record:

                messagebox.showerror(
                    "Not Found",
                    (
                        "The selected Fee Structure "
                        "was not found."
                    ),
                    parent=form_window
                )

                close_form()

                return


            # -------------------------------------------------
            # SET COURSE
            # -------------------------------------------------

            course_var.set(
                record["Course_Name"]
            )


            update_semesters()


            # -------------------------------------------------
            # SET VALUES
            # -------------------------------------------------

            semester_var.set(
                str(
                    record["Semester"]
                )
            )


            academic_year_var.set(
                normalize_academic_year(
                    record["Academic_Year"]
                )
            )


            status_var.set(
                record["Status"]
                or "Active"
            )


            # -------------------------------------------------
            # LOAD COMPONENTS
            #
            # CORRECT DATABASE COLUMNS:
            #
            # Fee_Type
            # Amount
            # Component_ID
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    Fee_Type,
                    Amount

                FROM fee_structure_components

                WHERE
                    Fee_Structure_ID = %s

                ORDER BY
                    Component_ID
                """,
                (
                    fee_structure_id,
                )
            )


            component_records = (
                cursor.fetchall()
            )


            fee_components.clear()


            for component in component_records:

                fee_components.append(
                    {
                        "name":
                            component[
                                "Fee_Type"
                            ],

                        "amount":
                            float(
                                component[
                                    "Amount"
                                ]
                            )
                    }
                )


            refresh_component_table()


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Could not load the "
                    "Fee Structure."
                    f"\n\n{error}"
                ),
                parent=form_window
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
    # CANCEL BUTTON
    # ========================================================

    Button(
        actions,
        text="CANCEL",
        bg=WHITE,
        fg=TEXT_COLOR,
        activebackground="#F1F5F9",
        activeforeground=TEXT_COLOR,
        relief=SOLID,
        bd=1,
        cursor="hand2",
        font=(
            "Helvetica",
            9,
            "bold"
        ),
        command=close_form
    ).pack(
        side=RIGHT,
        ipadx=22,
        ipady=9
    )


    # ========================================================
    # CREATE / UPDATE BUTTON
    # ========================================================

    Button(
        actions,
        text=(
            "UPDATE FEE STRUCTURE"
            if is_edit_mode
            else "CREATE FEE STRUCTURE"
        ),
        bg=BLUE,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        bd=0,
        relief=FLAT,
        cursor="hand2",
        font=(
            "Helvetica",
            9,
            "bold"
        ),
        command=save_fee_structure
    ).pack(
        side=RIGHT,
        padx=10,
        ipadx=22,
        ipady=10
    )


    # ========================================================
    # INITIALIZE
    # ========================================================

    load_courses()

    refresh_component_table()


    if is_edit_mode:
        load_edit_data()


    course_combo.focus_set()
