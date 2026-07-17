from tkinter import *
from tkinter import messagebox
import mysql.connector

from accountant_form import open_accountant_form


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

RED = "#DC2626"


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
# SHOW ACCOUNTANT PAGE
# ============================================================

def show_accountant_page(parent):

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
        text="Accountants",
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
        text="Manage accountant accounts and login information",
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
    # ADD ACCOUNTANT
    # ========================================================

    def add_accountant():

        open_accountant_form(
            parent,
            refresh_callback=lambda: show_accountant_page(parent)
        )


    # ========================================================
    # ADD ACCOUNTANT BUTTON
    # ========================================================

    add_button = Button(
        header_frame,
        text="+  ADD ACCOUNTANT",
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
        command=add_accountant
    )

    add_button.place(
        relx=1.0,
        x=-30,
        y=28,
        width=165,
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

    PLACEHOLDER = "Search by ID, name or username..."


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
    # ACCOUNTANT COUNT
    # ========================================================

    count_label = Label(
        table_top,
        text="0 Accountants",
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
    # VERTICAL Y SCROLLBAR ONLY
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


    # ========================================================
    # CONNECT Y SCROLLBAR
    # ========================================================

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
    # CURRENT TABLE WIDTH
    # ========================================================

    table_width = 1000


    # ========================================================
    # COLUMN RATIOS
    #
    # TOTAL = 1.00
    # ========================================================

    COLUMN_RATIOS = {

        "registration": 0.15,

        "name": 0.20,

        "username": 0.18,

        "password": 0.17,

        "role": 0.13,

        "actions": 0.17

    }


    # ========================================================
    # CURRENT COLUMN WIDTHS
    # ========================================================

    COLUMN_WIDTHS = {

        "registration": 150,

        "name": 200,

        "username": 180,

        "password": 170,

        "role": 130,

        "actions": 170

    }


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

    table_header.pack_propagate(
        False
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
    # UPDATE COLUMN WIDTHS
    # ========================================================

    def update_column_widths(
        total_width
    ):

        COLUMN_WIDTHS["registration"] = int(
            total_width
            * COLUMN_RATIOS["registration"]
        )


        COLUMN_WIDTHS["name"] = int(
            total_width
            * COLUMN_RATIOS["name"]
        )


        COLUMN_WIDTHS["username"] = int(
            total_width
            * COLUMN_RATIOS["username"]
        )


        COLUMN_WIDTHS["password"] = int(
            total_width
            * COLUMN_RATIOS["password"]
        )


        COLUMN_WIDTHS["role"] = int(
            total_width
            * COLUMN_RATIOS["role"]
        )


        # ----------------------------------------------------
        # LAST COLUMN GETS REMAINING WIDTH
        # ----------------------------------------------------

        used_width = (

            COLUMN_WIDTHS["registration"]

            + COLUMN_WIDTHS["name"]

            + COLUMN_WIDTHS["username"]

            + COLUMN_WIDTHS["password"]

            + COLUMN_WIDTHS["role"]

        )


        COLUMN_WIDTHS["actions"] = (

            total_width

            - used_width

        )


    # ========================================================
    # CREATE HEADER COLUMN
    #
    # SAME STYLE AS STUDENT MANAGEMENT
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
    # BUILD TABLE HEADER
    # ========================================================

    def build_header():

        # ----------------------------------------------------
        # DELETE OLD HEADER
        # ----------------------------------------------------

        for widget in table_header.winfo_children():

            widget.destroy()


        # ----------------------------------------------------
        # REGISTRATION NUMBER
        # ----------------------------------------------------

        header_column(
            "REGISTRATION NO.",
            COLUMN_WIDTHS["registration"]
        )


        # ----------------------------------------------------
        # NAME
        # ----------------------------------------------------

        header_column(
            "NAME",
            COLUMN_WIDTHS["name"]
        )


        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        header_column(
            "USERNAME",
            COLUMN_WIDTHS["username"]
        )


        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        header_column(
            "PASSWORD",
            COLUMN_WIDTHS["password"]
        )


        # ----------------------------------------------------
        # ROLE
        # ----------------------------------------------------

        header_column(
            "ROLE",
            COLUMN_WIDTHS["role"]
        )


        # ----------------------------------------------------
        # ACTIONS
        # ----------------------------------------------------

        header_column(
            "ACTIONS",
            COLUMN_WIDTHS["actions"]
        )


    # ========================================================
    # UPDATE SCROLL REGION
    # ========================================================

    def update_scroll_region(
        event=None
    ):

        table_canvas.configure(
            scrollregion=table_canvas.bbox(
                "all"
            )
        )


    # ========================================================
    # RESIZE TABLE TO COMPLETE AVAILABLE WIDTH
    # ========================================================

    def resize_table(
        event
    ):

        nonlocal table_width


        # ----------------------------------------------------
        # IGNORE INVALID WIDTH
        # ----------------------------------------------------

        if event.width <= 1:

            return


        # ----------------------------------------------------
        # SAVE WIDTH
        # ----------------------------------------------------

        table_width = event.width


        # ----------------------------------------------------
        # MAKE INTERNAL FRAME SAME WIDTH AS CANVAS
        # ----------------------------------------------------

        table_canvas.itemconfig(
            canvas_window,
            width=table_width
        )


        # ----------------------------------------------------
        # UPDATE COLUMN WIDTHS
        # ----------------------------------------------------

        update_column_widths(
            table_width
        )


        # ----------------------------------------------------
        # REBUILD HEADER
        # ----------------------------------------------------

        build_header()


        # ----------------------------------------------------
        # RELOAD CURRENT DATA
        #
        # This makes row widths match new header widths.
        # ----------------------------------------------------

        current_search = (
            search_entry
            .get()
            .strip()
        )


        if (
            current_search == PLACEHOLDER
            or current_search == ""
        ):

            load_accountants()

        else:

            load_accountants(
                current_search
            )


    # ========================================================
    # BIND TABLE RESIZE
    # ========================================================

    table_canvas.bind(
        "<Configure>",
        resize_table
    )


    # ========================================================
    # SCROLL REGION BINDS
    # ========================================================

    table_frame.bind(
        "<Configure>",
        update_scroll_region
    )


    rows_frame.bind(
        "<Configure>",
        update_scroll_region
    )


    # ========================================================
    # MOUSE WHEEL Y SCROLLING
    # ========================================================

    def mouse_wheel_y(
        event
    ):

        if event.delta:

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


        return "break"


    # ========================================================
    # ENABLE MOUSE SCROLL
    # ========================================================

    def enable_mouse_scroll(
        event=None
    ):

        table_canvas.bind_all(
            "<MouseWheel>",
            mouse_wheel_y
        )


    # ========================================================
    # DISABLE MOUSE SCROLL
    # ========================================================

    def disable_mouse_scroll(
        event=None
    ):

        table_canvas.unbind_all(
            "<MouseWheel>"
        )


    # ========================================================
    # ACTIVATE MOUSE SCROLLING
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
    # EDIT ACCOUNTANT
    # ========================================================

    def edit_accountant(
        accountant_id
    ):

        open_accountant_form(
            parent,
            refresh_callback=lambda: show_accountant_page(
                parent
            ),
            accountant_id=accountant_id
        )


    # ========================================================
    # DELETE ACCOUNTANT
    # ========================================================

    def delete_accountant(
        accountant_id,
        accountant_name
    ):

        # ----------------------------------------------------
        # CONFIRM DELETE
        # ----------------------------------------------------

        confirm = messagebox.askyesno(
            "Delete Accountant",
            (
                f"Are you sure you want to delete "
                f"{accountant_name}?\n\n"
                f"Registration No: {accountant_id}\n\n"
                "This action cannot be undone."
            )
        )


        if not confirm:

            return


        con = None

        cursor = None


        try:

            # ------------------------------------------------
            # DATABASE CONNECTION
            # ------------------------------------------------

            con = get_connection()

            cursor = con.cursor()


            # ------------------------------------------------
            # DELETE ACCOUNTANT
            # ------------------------------------------------

            cursor.execute(
                """
                DELETE FROM registration

                WHERE Registration_No = %s

                AND LOWER(Role) = 'accountant'
                """,
                (
                    accountant_id,
                )
            )


            # ------------------------------------------------
            # ACCOUNTANT NOT FOUND
            # ------------------------------------------------

            if cursor.rowcount == 0:

                con.rollback()


                messagebox.showerror(
                    "Accountant Not Found",
                    "The accountant could not be found."
                )


                return


            # ------------------------------------------------
            # SAVE CHANGES
            # ------------------------------------------------

            con.commit()


            # ------------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------------

            messagebox.showinfo(
                "Accountant Deleted",
                (
                    f"{accountant_name} "
                    "has been deleted successfully."
                )
            )


            # ------------------------------------------------
            # REFRESH TABLE
            # ------------------------------------------------

            load_accountants()


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
    #
    # SAME METHOD AS STUDENT MANAGEMENT
    # ========================================================

    def create_cell(
        row,
        text,
        width,
        color=TEXT_COLOR,
        bold=False
    ):

        # ----------------------------------------------------
        # CELL FRAME
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # FONT
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # CELL LABEL
        # ----------------------------------------------------

        cell_label = Label(
            cell_frame,
            text=str(text),
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
    # CREATE ACCOUNTANT ROW
    # ========================================================

    def create_accountant_row(
        accountant
    ):

        # ----------------------------------------------------
        # GET VALUES
        # ----------------------------------------------------

        registration_no = accountant[0]

        accountant_name = accountant[1]

        username = accountant[2]

        password = accountant[3]

        role = accountant[4]


        # ----------------------------------------------------
        # HANDLE NULL VALUES
        # ----------------------------------------------------

        if registration_no is None:

            registration_no = "-"


        if accountant_name is None:

            accountant_name = "-"


        if username is None:

            username = "-"


        if password is None:

            password = "-"


        if role is None:

            role = "Accountant"


        # ====================================================
        # ROW FRAME
        #
        # SAME HEIGHT AS STUDENT MANAGEMENT
        # ====================================================

        row = Frame(
            rows_frame,
            bg=WHITE,
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
            accountant_name,
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
        # PASSWORD
        # ====================================================

        create_cell(
            row,
            password,
            COLUMN_WIDTHS["password"]
        )


        # ====================================================
        # ROLE
        # ====================================================

        create_cell(
            row,
            role,
            COLUMN_WIDTHS["role"]
        )


        # ====================================================
        # ACTION FRAME
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
            command=lambda accountant_id=registration_no: (
                edit_accountant(
                    accountant_id
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
            command=lambda
            accountant_id=registration_no,
            name=accountant_name: (
                delete_accountant(
                    accountant_id,
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
            bg="#F1F5F9",
            height=1
        )

        bottom_border.place(
            x=0,
            y=58,
            relwidth=1.0,
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
    # LOAD ACCOUNTANTS
    # ========================================================

    def load_accountants(
        search_text=""
    ):

        # ----------------------------------------------------
        # CLEAR OLD DATA
        # ----------------------------------------------------

        clear_rows()


        con = None

        cursor = None


        try:

            # ------------------------------------------------
            # DATABASE CONNECTION
            # ------------------------------------------------

            con = get_connection()

            cursor = con.cursor()


            # =================================================
            # SEARCH ACCOUNTANTS
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
                        Registration_No,
                        Name,
                        Username,
                        Password,
                        Role

                    FROM registration

                    WHERE LOWER(Role) = 'accountant'

                    AND
                    (
                        Registration_No LIKE %s

                        OR Name LIKE %s

                        OR Username LIKE %s
                    )

                    ORDER BY Name ASC
                    """,
                    (
                        search_value,
                        search_value,
                        search_value
                    )
                )


            # =================================================
            # LOAD ALL ACCOUNTANTS
            # =================================================

            else:

                cursor.execute(
                    """
                    SELECT
                        Registration_No,
                        Name,
                        Username,
                        Password,
                        Role

                    FROM registration

                    WHERE LOWER(Role) = 'accountant'

                    ORDER BY Name ASC
                    """
                )


            # ------------------------------------------------
            # FETCH DATA
            # ------------------------------------------------

            accountants = cursor.fetchall()


            # ------------------------------------------------
            # UPDATE ACCOUNTANT COUNT
            # ------------------------------------------------

            if len(accountants) == 1:

                count_label.config(
                    text="1 Accountant"
                )


            else:

                count_label.config(
                    text=f"{len(accountants)} Accountants"
                )


            # ------------------------------------------------
            # NO ACCOUNTANTS
            # ------------------------------------------------

            if len(accountants) == 0:

                if search_text == "":

                    show_empty_message(
                        "No accountants found."
                    )


                else:

                    show_empty_message(
                        "No accountants match your search."
                    )


                rows_frame.update_idletasks()

                table_frame.update_idletasks()

                update_scroll_region()


                return


            # ------------------------------------------------
            # CREATE ACCOUNTANT ROWS
            # ------------------------------------------------

            for accountant in accountants:

                create_accountant_row(
                    accountant
                )


            # ------------------------------------------------
            # UPDATE SCROLLING
            # ------------------------------------------------

            rows_frame.update_idletasks()

            table_frame.update_idletasks()

            update_scroll_region()


            # ------------------------------------------------
            # RETURN TO TOP
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
    # SEARCH ACCOUNTANTS
    # ========================================================

    def search_accountants():

        search_text = (
            search_entry
            .get()
            .strip()
        )


        # ----------------------------------------------------
        # EMPTY OR PLACEHOLDER
        # ----------------------------------------------------

        if (
            search_text == ""
            or search_text == PLACEHOLDER
        ):

            load_accountants()

            return


        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        load_accountants(
            search_text
        )


    # ========================================================
    # CLEAR SEARCH
    # ========================================================

    def clear_search():

        # ----------------------------------------------------
        # CLEAR SEARCH ENTRY
        # ----------------------------------------------------

        search_entry.delete(
            0,
            END
        )


        # ----------------------------------------------------
        # LOAD ALL ACCOUNTANTS
        # ----------------------------------------------------

        load_accountants(
            search_text=""
        )


        # ----------------------------------------------------
        # RESTORE PLACEHOLDER
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # REMOVE FOCUS
        # ----------------------------------------------------

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
        command=search_accountants
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
        lambda event: search_accountants()
    )


    # ========================================================
    # INITIAL TABLE SETUP
    # ========================================================

    page.update_idletasks()


    initial_width = table_canvas.winfo_width()


    if initial_width <= 1:

        initial_width = 1000


    table_width = initial_width


    table_canvas.itemconfig(
        canvas_window,
        width=table_width
    )


    update_column_widths(
        table_width
    )


    build_header()


    # ========================================================
    # LOAD ALL ACCOUNTANTS
    # ========================================================

    load_accountants()