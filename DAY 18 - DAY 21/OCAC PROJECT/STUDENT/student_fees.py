from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector


# ============================================================
# DATABASE CONFIGURATION
# Change these values if your MySQL settings are different.
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ocac_group2"
}


# ============================================================
# DEFAULT COLORS
# The dashboard can pass its own color dictionary.
# ============================================================

DEFAULT_COLORS = {
    "BG": "#F4F7FB",
    "WHITE": "#FFFFFF",
    "TEXT": "#0F172A",
    "MUTED": "#64748B",
    "BLUE": "#2563EB",
    "GREEN": "#16A34A",
    "RED": "#DC2626",
    "AMBER": "#D97706",
    "BORDER": "#E2E8F0",
    "SOFT_BLUE": "#EFF6FF",
    "SOFT_GREEN": "#F0FDF4",
    "SOFT_RED": "#FEF2F2",
    "SOFT_AMBER": "#FFFBEB"
}


# ============================================================
# DATABASE HELPERS
# ============================================================

def get_connection():
    return mysql.connector.connect(
        **DB_CONFIG
    )


def fetch_all(query, params=()):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            query,
            params
        )

        return cursor.fetchall()

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )

        return []

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()


def fetch_one(query, params=()):
    rows = fetch_all(
        query,
        params
    )

    return rows[0] if rows else None


# ============================================================
# FORMAT HELPERS
# ============================================================

def money(value):
    try:
        amount = float(value or 0)
    except (TypeError, ValueError):
        amount = 0.0

    return f"Rs. {amount:,.2f}"


def format_date(value):
    if value is None:
        return "-"

    if hasattr(
        value,
        "strftime"
    ):
        return value.strftime(
            "%d-%m-%Y"
        )

    return str(value)


# ============================================================
# MAIN MY FEES PAGE
# ============================================================

def show_student_fees(
    parent,
    registration_no,
    student_name="Student",
    colors=None,
    on_dashboard=None
):

    palette = DEFAULT_COLORS.copy()

    if colors:
        palette.update(colors)

    BG = palette["BG"]
    WHITE = palette["WHITE"]
    TEXT = palette["TEXT"]
    MUTED = palette["MUTED"]
    BLUE = palette["BLUE"]
    GREEN = palette["GREEN"]
    RED = palette["RED"]
    AMBER = palette["AMBER"]
    BORDER = palette["BORDER"]

    # --------------------------------------------------------
    # CLEAR PARENT
    # --------------------------------------------------------

    for widget in parent.winfo_children():
        widget.destroy()

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    summary = fetch_one(
        """
        SELECT
            COALESCE(
                SUM(Total_Fee),
                0
            ) AS Total_Assigned,

            COALESCE(
                SUM(Amount_Paid),
                0
            ) AS Total_Paid,

            COALESCE(
                SUM(Due_Amount),
                0
            ) AS Total_Due,

            COUNT(*) AS Semester_Count

        FROM student_fees

        WHERE Registration_No = %s
        """,
        (registration_no,)
    ) or {}

    payment_count_row = fetch_one(
        """
        SELECT
            COUNT(*) AS Payment_Count

        FROM fee_payments fp

        INNER JOIN student_fees sf
            ON sf.Student_Fee_ID =
               fp.Student_Fee_ID

        WHERE sf.Registration_No = %s
        """,
        (registration_no,)
    ) or {}

    semester_rows = fetch_all(
        """
        SELECT
            sf.Student_Fee_ID,
            sf.Fee_Structure_ID,
            sf.Total_Fee,
            sf.Amount_Paid,
            sf.Due_Amount,
            sf.Payment_Status,

            fs.Semester,
            fs.Academic_Year,

            (
                SELECT
                    fp.Payment_Date

                FROM fee_payments fp

                WHERE
                    fp.Student_Fee_ID =
                    sf.Student_Fee_ID

                ORDER BY
                    fp.Payment_Date DESC,
                    fp.Payment_ID DESC

                LIMIT 1
            ) AS Last_Payment_Date,

            (
                SELECT
                    fp.Payment_Mode

                FROM fee_payments fp

                WHERE
                    fp.Student_Fee_ID =
                    sf.Student_Fee_ID

                ORDER BY
                    fp.Payment_Date DESC,
                    fp.Payment_ID DESC

                LIMIT 1
            ) AS Last_Payment_Mode,

            (
                SELECT
                    fp.Amount

                FROM fee_payments fp

                WHERE
                    fp.Student_Fee_ID =
                    sf.Student_Fee_ID

                ORDER BY
                    fp.Payment_Date DESC,
                    fp.Payment_ID DESC

                LIMIT 1
            ) AS Last_Payment_Amount

        FROM student_fees sf

        INNER JOIN fee_structures fs
            ON fs.Fee_Structure_ID =
               sf.Fee_Structure_ID

        WHERE
            sf.Registration_No = %s

        ORDER BY
            fs.Semester ASC,
            sf.Student_Fee_ID ASC
        """,
        (registration_no,)
    )

    total_assigned = float(
        summary.get(
            "Total_Assigned"
        )
        or 0
    )

    total_paid = float(
        summary.get(
            "Total_Paid"
        )
        or 0
    )

    total_due = float(
        summary.get(
            "Total_Due"
        )
        or 0
    )

    semester_count = int(
        summary.get(
            "Semester_Count"
        )
        or 0
    )

    payment_count = int(
        payment_count_row.get(
            "Payment_Count"
        )
        or 0
    )

    # --------------------------------------------------------
    # SCROLLABLE PAGE
    # --------------------------------------------------------

    outer = Frame(
        parent,
        bg=BG
    )

    outer.pack(
        fill=BOTH,
        expand=True
    )

    canvas = Canvas(
        outer,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        outer,
        orient=VERTICAL,
        command=canvas.yview
    )

    body = Frame(
        canvas,
        bg=BG
    )

    body_window = canvas.create_window(
        (0, 0),
        window=body,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )

    scrollbar.pack(
        side=RIGHT,
        fill=Y
    )

    def update_scroll_region(
        event=None
    ):
        canvas.configure(
            scrollregion=canvas.bbox(
                "all"
            )
        )

    def fit_body_width(event):
        canvas.itemconfigure(
            body_window,
            width=event.width
        )

    body.bind(
        "<Configure>",
        update_scroll_region
    )

    canvas.bind(
        "<Configure>",
        fit_body_width
    )

    # --------------------------------------------------------
    # SMOOTH MOUSE-WHEEL SCROLL
    # --------------------------------------------------------

    scroll_state = {
        "target": 0.0,
        "job": None
    }

    def scroll_metrics():
        bbox = canvas.bbox(
            "all"
        )

        if not bbox:
            return 1.0, 0.0

        content_height = max(
            1.0,
            float(
                bbox[3] - bbox[1]
            )
        )

        viewport_height = max(
            1.0,
            float(
                canvas.winfo_height()
            )
        )

        max_scroll = max(
            0.0,
            content_height
            - viewport_height
        )

        return (
            content_height,
            max_scroll
        )

    def current_scroll_pixels():
        content_height, _ = (
            scroll_metrics()
        )

        return (
            canvas.yview()[0]
            * content_height
        )

    def animate_scroll():
        content_height, max_scroll = (
            scroll_metrics()
        )

        target = max(
            0.0,
            min(
                scroll_state["target"],
                max_scroll
            )
        )

        current = (
            current_scroll_pixels()
        )

        difference = (
            target - current
        )

        if abs(difference) < 0.8:
            canvas.yview_moveto(
                target
                / content_height
            )

            scroll_state["job"] = None

            return

        next_position = (
            current
            + difference * 0.24
        )

        canvas.yview_moveto(
            next_position
            / content_height
        )

        scroll_state["job"] = (
            parent.after(
                10,
                animate_scroll
            )
        )

    def mouse_wheel(event):
        _, max_scroll = (
            scroll_metrics()
        )

        if max_scroll <= 0:
            return "break"

        direction = (
            -1
            if event.delta > 0
            else 1
        )

        scroll_state["target"] = max(
            0.0,
            min(
                current_scroll_pixels()
                + direction * 120,
                max_scroll
            )
        )

        if (
            scroll_state["job"]
            is None
        ):
            animate_scroll()

        return "break"

    def enable_scroll(
        event=None
    ):
        scroll_state["target"] = (
            current_scroll_pixels()
        )

        canvas.bind_all(
            "<MouseWheel>",
            mouse_wheel
        )

    def disable_scroll(
        event=None
    ):
        canvas.unbind_all(
            "<MouseWheel>"
        )

    canvas.bind(
        "<Enter>",
        enable_scroll
    )

    body.bind(
        "<Enter>",
        enable_scroll
    )

    canvas.bind(
        "<Leave>",
        disable_scroll
    )

    # --------------------------------------------------------
    # PAGE INTRO
    # --------------------------------------------------------

    intro = Frame(
        body,
        bg=BG
    )

    intro.pack(
        fill=X,
        padx=28,
        pady=(24, 18)
    )

    Label(
        intro,
        text="My Fees",
        bg=BG,
        fg=TEXT,
        font=(
            "Helvetica",
            22,
            "bold"
        )
    ).pack(
        anchor="w"
    )

    Label(
        intro,
        text=(
            "View your semester-wise assigned "
            "fees and outstanding dues."
        ),
        bg=BG,
        fg=MUTED,
        font=(
            "Helvetica",
            10
        )
    ).pack(
        anchor="w",
        pady=(6, 0)
    )

    # --------------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------------

    Label(
        body,
        text="MY FEE OVERVIEW",
        bg=BG,
        fg=TEXT,
        font=(
            "Helvetica",
            11,
            "bold"
        )
    ).pack(
        anchor="w",
        padx=28,
        pady=(0, 10)
    )

    overview = Frame(
        body,
        bg=BG
    )

    overview.pack(
        fill=X,
        padx=28,
        pady=(0, 20)
    )

    for column in range(3):
        overview.grid_columnconfigure(
            column,
            weight=1,
            uniform="fee_overview"
        )

    def overview_card(
        column,
        title,
        value,
        subtitle,
        value_color
    ):

        card = Frame(
            overview,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(
                0 if column == 0 else 7,
                0 if column == 2 else 7
            )
        )

        Label(
            card,
            text=title,
            bg=WHITE,
            fg=MUTED,
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 7)
        )

        Label(
            card,
            text=value,
            bg=WHITE,
            fg=value_color,
            font=(
                "Helvetica",
                18,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=20
        )

        Label(
            card,
            text=subtitle,
            bg=WHITE,
            fg=MUTED,
            font=(
                "Helvetica",
                9
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(7, 18)
        )

    overview_card(
        0,
        "TOTAL ASSIGNED",
        money(total_assigned),
        (
            f"{semester_count} "
            f"Semester"
            f"{'' if semester_count == 1 else 's'}"
        ),
        BLUE
    )

    overview_card(
        1,
        "TOTAL PAID",
        money(total_paid),
        (
            f"{payment_count} "
            f"Payment"
            f"{'' if payment_count == 1 else 's'}"
        ),
        GREEN
    )

    overview_card(
        2,
        "TOTAL DUE",
        money(total_due),
        (
            "All fees cleared"
            if total_due <= 0
            else "Payment pending"
        ),
        (
            GREEN
            if total_due <= 0
            else RED
        )
    )

    # --------------------------------------------------------
    # FEE ATTENTION
    # --------------------------------------------------------

    previous_due_rows = [
        row
        for row in semester_rows
        if float(
            row.get(
                "Due_Amount"
            )
            or 0
        ) > 0
    ]

    attention_title = ""
    attention_message = ""
    attention_meta = ""
    attention_color = BLUE
    attention_bg = palette.get(
        "SOFT_BLUE",
        "#EFF6FF"
    )

    attention_row = None

    if previous_due_rows:
        attention_row = (
            previous_due_rows[0]
        )

        due_semesters = len(
            previous_due_rows
        )

        if due_semesters == 1:
            attention_title = (
                "OUTSTANDING FEE"
            )

            attention_message = (
                f"Semester "
                f"{attention_row['Semester']} "
                f"has an outstanding balance "
                f"of "
                f"{money(attention_row['Due_Amount'])}."
            )

            attention_meta = (
                f"Semester "
                f"{attention_row['Semester']}  •  "
                f"{attention_row['Academic_Year']}"
            )

        else:
            attention_title = (
                "OUTSTANDING IN "
                f"{due_semesters} SEMESTERS"
            )

            attention_message = (
                "Multiple semester fee balances "
                "are still pending."
            )

            attention_meta = (
                f"Total outstanding: "
                f"{money(total_due)}"
            )

        attention_color = RED
        attention_bg = palette.get(
            "SOFT_RED",
            "#FEF2F2"
        )

    elif semester_count > 0:
        attention_title = (
            "ALL ASSIGNED FEES CLEARED"
        )

        attention_message = (
            "There is no outstanding balance "
            "in your assigned semester fees."
        )

        attention_meta = (
            f"{semester_count} assigned "
            f"semester"
            f"{'' if semester_count == 1 else 's'}"
        )

        attention_color = GREEN
        attention_bg = palette.get(
            "SOFT_GREEN",
            "#F0FDF4"
        )

    else:
        attention_title = (
            "NO FEE ASSIGNED YET"
        )

        attention_message = (
            "No semester fee structure has "
            "been assigned to your account."
        )

        attention_meta = (
            "Please check again later."
        )

        attention_color = AMBER
        attention_bg = palette.get(
            "SOFT_AMBER",
            "#FFFBEB"
        )

    Label(
        body,
        text="FEE ATTENTION",
        bg=BG,
        fg=TEXT,
        font=(
            "Helvetica",
            11,
            "bold"
        )
    ).pack(
        anchor="w",
        padx=28,
        pady=(0, 10)
    )

    attention = Frame(
        body,
        bg=attention_bg,
        highlightbackground=attention_color,
        highlightthickness=1
    )

    attention.pack(
        fill=X,
        padx=28,
        pady=(0, 22)
    )

    attention_text = Frame(
        attention,
        bg=attention_bg
    )

    attention_text.pack(
        side=LEFT,
        fill=X,
        expand=True,
        padx=22,
        pady=18
    )

    Label(
        attention_text,
        text=attention_title,
        bg=attention_bg,
        fg=attention_color,
        font=(
            "Helvetica",
            10,
            "bold"
        )
    ).pack(
        anchor="w"
    )

    Label(
        attention_text,
        text=attention_message,
        bg=attention_bg,
        fg=TEXT,
        font=(
            "Helvetica",
            11,
            "bold"
        ),
        wraplength=650,
        justify=LEFT
    ).pack(
        anchor="w",
        pady=(7, 4)
    )

    Label(
        attention_text,
        text=attention_meta,
        bg=attention_bg,
        fg=MUTED,
        font=(
            "Helvetica",
            9
        )
    ).pack(
        anchor="w"
    )

    # --------------------------------------------------------
    # SEMESTER RECORDS TITLE
    # --------------------------------------------------------

    Label(
        body,
        text="SEMESTER-WISE FEE RECORDS",
        bg=BG,
        fg=TEXT,
        font=(
            "Helvetica",
            11,
            "bold"
        )
    ).pack(
        anchor="w",
        padx=28,
        pady=(0, 10)
    )

    records = Frame(
        body,
        bg=BG
    )

    records.pack(
        fill=X,
        padx=28,
        pady=(0, 28)
    )

    # --------------------------------------------------------
    # FEE DETAILS POPUP
    # --------------------------------------------------------

    def open_fee_details(
        semester_row
    ):

        student_fee_id = (
            semester_row[
                "Student_Fee_ID"
            ]
        )

        fee_structure_id = (
            semester_row[
                "Fee_Structure_ID"
            ]
        )

        components = fetch_all(
            """
            SELECT
                *

            FROM fee_structure_components

            WHERE Fee_Structure_ID = %s

            ORDER BY 1 ASC
            """,
            (fee_structure_id,)
        )

        latest_payment = fetch_one(
            """
            SELECT
                Payment_Date,
                Payment_Mode,
                Amount

            FROM fee_payments

            WHERE Student_Fee_ID = %s

            ORDER BY
                Payment_Date DESC,
                Payment_ID DESC

            LIMIT 1
            """,
            (student_fee_id,)
        )

        popup = Toplevel(
            parent
        )

        popup.title(
            "Fee Details"
        )

        popup.configure(
            bg=BG
        )

        popup.geometry(
            "760x650"
        )

        popup.minsize(
            700,
            560
        )

        popup.transient(
            parent.winfo_toplevel()
        )

        popup.grab_set()

        popup.update_idletasks()

        screen_width = (
            popup.winfo_screenwidth()
        )

        screen_height = (
            popup.winfo_screenheight()
        )

        popup_width = (
            popup.winfo_width()
        )

        popup_height = (
            popup.winfo_height()
        )

        x_position = (
            screen_width
            - popup_width
        ) // 2

        y_position = (
            screen_height
            - popup_height
        ) // 2

        popup.geometry(
            f"+{x_position}+{y_position}"
        )

        # ---------------- POPUP HEADER ----------------

        header = Frame(
            popup,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        header.pack(
            fill=X
        )

        header_text = Frame(
            header,
            bg=WHITE
        )

        header_text.pack(
            side=LEFT,
            fill=X,
            expand=True,
            padx=24,
            pady=18
        )

        Label(
            header_text,
            text=(
                f"SEMESTER "
                f"{semester_row['Semester']} "
                f"— FEE DETAILS"
            ),
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                16,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        Label(
            header_text,
            text=(
                f"Academic Year "
                f"{semester_row['Academic_Year']}"
            ),
            bg=WHITE,
            fg=MUTED,
            font=(
                "Helvetica",
                9
            )
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # ALL CLOSE BUTTONS ARE RED
        Button(
            header,
            text="X",
            command=popup.destroy,
            bg=RED,
            fg=WHITE,
            activebackground="#B91C1C",
            activeforeground=WHITE,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            font=(
                "Helvetica",
                10,
                "bold"
            ),
            width=4,
            pady=8
        ).pack(
            side=RIGHT,
            padx=20,
            pady=18
        )

        # ---------------- POPUP SCROLL AREA ----------------

        popup_outer = Frame(
            popup,
            bg=BG
        )

        popup_outer.pack(
            fill=BOTH,
            expand=True
        )

        popup_canvas = Canvas(
            popup_outer,
            bg=BG,
            highlightthickness=0
        )

        popup_scrollbar = ttk.Scrollbar(
            popup_outer,
            orient=VERTICAL,
            command=popup_canvas.yview
        )

        popup_body = Frame(
            popup_canvas,
            bg=BG
        )

        popup_window = (
            popup_canvas.create_window(
                (0, 0),
                window=popup_body,
                anchor="nw"
            )
        )

        popup_canvas.configure(
            yscrollcommand=(
                popup_scrollbar.set
            )
        )

        popup_canvas.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        popup_scrollbar.pack(
            side=RIGHT,
            fill=Y
        )

        popup_body.bind(
            "<Configure>",
            lambda event: (
                popup_canvas.configure(
                    scrollregion=(
                        popup_canvas.bbox(
                            "all"
                        )
                    )
                )
            )
        )

        popup_canvas.bind(
            "<Configure>",
            lambda event: (
                popup_canvas.itemconfigure(
                    popup_window,
                    width=event.width
                )
            )
        )

        # ---------------- SUMMARY ----------------

        total_value = float(
            semester_row.get(
                "Total_Fee"
            )
            or 0
        )

        paid_value = float(
            semester_row.get(
                "Amount_Paid"
            )
            or 0
        )

        due_value = float(
            semester_row.get(
                "Due_Amount"
            )
            or 0
        )

        status_value = (
            semester_row.get(
                "Payment_Status"
            )
            or "Unpaid"
        )

        summary_title = Frame(
            popup_body,
            bg=BG
        )

        summary_title.pack(
            fill=X,
            padx=24,
            pady=(22, 10)
        )

        Label(
            summary_title,
            text="FEE SUMMARY",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                10,
                "bold"
            )
        ).pack(
            side=LEFT
        )

        Label(
            summary_title,
            text=(
                f"STATUS: "
                f"{status_value.upper()}"
            ),
            bg=BG,
            fg=(
                GREEN
                if due_value <= 0
                else (
                    AMBER
                    if paid_value > 0
                    else RED
                )
            ),
            font=(
                "Helvetica",
                9,
                "bold"
            )
        ).pack(
            side=RIGHT
        )

        popup_summary = Frame(
            popup_body,
            bg=BG
        )

        popup_summary.pack(
            fill=X,
            padx=24,
            pady=(0, 20)
        )

        for column in range(3):
            popup_summary.grid_columnconfigure(
                column,
                weight=1,
                uniform="popup_summary"
            )

        popup_values = [
            (
                "TOTAL FEE",
                money(total_value),
                BLUE
            ),
            (
                "PAID",
                money(paid_value),
                GREEN
            ),
            (
                "OUTSTANDING",
                money(due_value),
                (
                    GREEN
                    if due_value <= 0
                    else RED
                )
            )
        ]

        for column, item in enumerate(
            popup_values
        ):
            title_text, value_text, value_color = (
                item
            )

            card = Frame(
                popup_summary,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            card.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=(
                    0 if column == 0 else 6,
                    0 if column == 2 else 6
                )
            )

            Label(
                card,
                text=title_text,
                bg=WHITE,
                fg=MUTED,
                font=(
                    "Helvetica",
                    8,
                    "bold"
                )
            ).pack(
                anchor="w",
                padx=16,
                pady=(15, 6)
            )

            Label(
                card,
                text=value_text,
                bg=WHITE,
                fg=value_color,
                font=(
                    "Helvetica",
                    14,
                    "bold"
                )
            ).pack(
                anchor="w",
                padx=16,
                pady=(0, 16)
            )

        # ---------------- COMPONENT BREAKDOWN ----------------

        Label(
            popup_body,
            text="FEE COMPONENT BREAKDOWN",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                10,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=24,
            pady=(0, 10)
        )

        component_card = Frame(
            popup_body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        component_card.pack(
            fill=X,
            padx=24,
            pady=(0, 20)
        )

        component_header = Frame(
            component_card,
            bg="#F8FAFC"
        )

        component_header.pack(
            fill=X
        )

        Label(
            component_header,
            text="FEE COMPONENT",
            bg="#F8FAFC",
            fg=MUTED,
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            anchor="w"
        ).pack(
            side=LEFT,
            fill=X,
            expand=True,
            padx=18,
            pady=11
        )

        Label(
            component_header,
            text="AMOUNT",
            bg="#F8FAFC",
            fg=MUTED,
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            width=20,
            anchor="e"
        ).pack(
            side=RIGHT,
            padx=18,
            pady=11
        )

        if components:
            for component in components:

                row_frame = Frame(
                    component_card,
                    bg=WHITE
                )

                row_frame.pack(
                    fill=X
                )

                # Try common component-name columns safely.
                component_name = (
                    component.get(
                        "Component_Name"
                    )
                    or component.get(
                        "Fee_Component"
                    )
                    or component.get(
                        "Component"
                    )
                    or component.get(
                        "Name"
                    )
                    or "Fee Component"
                )

                # Try common amount columns safely.
                component_amount = (
                    component.get(
                        "Amount"
                    )
                    or component.get(
                        "Component_Amount"
                    )
                    or component.get(
                        "Fee_Amount"
                    )
                    or 0
                )

                Label(
                    row_frame,
                    text=str(
                        component_name
                    ),
                    bg=WHITE,
                    fg=TEXT,
                    font=(
                        "Helvetica",
                        10
                    ),
                    anchor="w"
                ).pack(
                    side=LEFT,
                    fill=X,
                    expand=True,
                    padx=18,
                    pady=10
                )

                Label(
                    row_frame,
                    text=money(
                        component_amount
                    ),
                    bg=WHITE,
                    fg=TEXT,
                    font=(
                        "Helvetica",
                        10,
                        "bold"
                    ),
                    width=20,
                    anchor="e"
                ).pack(
                    side=RIGHT,
                    padx=18,
                    pady=10
                )

        else:
            Label(
                component_card,
                text=(
                    "No fee component breakdown "
                    "is available for this structure."
                ),
                bg=WHITE,
                fg=MUTED,
                font=(
                    "Helvetica",
                    10
                ),
                pady=22
            ).pack(
                fill=X
            )

        total_row = Frame(
            component_card,
            bg="#F8FAFC"
        )

        total_row.pack(
            fill=X
        )

        Label(
            total_row,
            text="TOTAL FEE",
            bg="#F8FAFC",
            fg=TEXT,
            font=(
                "Helvetica",
                10,
                "bold"
            ),
            anchor="w"
        ).pack(
            side=LEFT,
            fill=X,
            expand=True,
            padx=18,
            pady=12
        )

        Label(
            total_row,
            text=money(
                total_value
            ),
            bg="#F8FAFC",
            fg=BLUE,
            font=(
                "Helvetica",
                11,
                "bold"
            ),
            width=20,
            anchor="e"
        ).pack(
            side=RIGHT,
            padx=18,
            pady=12
        )

        # ---------------- PAYMENT SUMMARY ----------------

        Label(
            popup_body,
            text="PAYMENT SUMMARY",
            bg=BG,
            fg=TEXT,
            font=(
                "Helvetica",
                10,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=24,
            pady=(0, 10)
        )

        payment_card = Frame(
            popup_body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        payment_card.pack(
            fill=X,
            padx=24,
            pady=(0, 20)
        )

        payment_items = [
            (
                "Amount Paid",
                money(
                    paid_value
                )
            ),
            (
                "Outstanding Balance",
                money(
                    due_value
                )
            ),
            (
                "Last Payment",
                (
                    format_date(
                        latest_payment[
                            "Payment_Date"
                        ]
                    )
                    if latest_payment
                    else "No payment recorded"
                )
            )
        ]

        for title_text, value_text in (
            payment_items
        ):

            item_row = Frame(
                payment_card,
                bg=WHITE
            )

            item_row.pack(
                fill=X,
                padx=18,
                pady=9
            )

            Label(
                item_row,
                text=title_text,
                bg=WHITE,
                fg=MUTED,
                font=(
                    "Helvetica",
                    10
                )
            ).pack(
                side=LEFT
            )

            Label(
                item_row,
                text=value_text,
                bg=WHITE,
                fg=TEXT,
                font=(
                    "Helvetica",
                    10,
                    "bold"
                )
            ).pack(
                side=RIGHT
            )

        # RED CLOSE BUTTON AT BOTTOM
        Button(
            popup_body,
            text="CLOSE",
            command=popup.destroy,
            bg=RED,
            fg=WHITE,
            activebackground="#B91C1C",
            activeforeground=WHITE,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            font=(
                "Helvetica",
                9,
                "bold"
            ),
            padx=26,
            pady=10
        ).pack(
            anchor="e",
            padx=24,
            pady=(0, 24)
        )

    # --------------------------------------------------------
    # SEMESTER CARDS
    # --------------------------------------------------------

    if semester_rows:

        for semester_row in semester_rows:

            semester = (
                semester_row.get(
                    "Semester"
                )
                or "-"
            )

            academic_year = (
                semester_row.get(
                    "Academic_Year"
                )
                or "-"
            )

            total_value = float(
                semester_row.get(
                    "Total_Fee"
                )
                or 0
            )

            paid_value = float(
                semester_row.get(
                    "Amount_Paid"
                )
                or 0
            )

            due_value = float(
                semester_row.get(
                    "Due_Amount"
                )
                or 0
            )

            if total_value <= 0:
                status_text = (
                    "NOT ASSIGNED"
                )
                status_color = MUTED

            elif due_value <= 0:
                status_text = "PAID"
                status_color = GREEN

            elif paid_value > 0:
                status_text = "PARTIAL"
                status_color = AMBER

            else:
                status_text = "UNPAID"
                status_color = RED

            card = Frame(
                records,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            card.pack(
                fill=X,
                pady=(0, 14)
            )

            card_header = Frame(
                card,
                bg="#F8FAFC"
            )

            card_header.pack(
                fill=X
            )

            Label(
                card_header,
                text=(
                    f"SEMESTER {semester}  •  "
                    f"{academic_year}"
                ),
                bg="#F8FAFC",
                fg=TEXT,
                font=(
                    "Helvetica",
                    11,
                    "bold"
                )
            ).pack(
                side=LEFT,
                padx=20,
                pady=14
            )

            Label(
                card_header,
                text=(
                    f"  {status_text}  "
                ),
                bg=status_color,
                fg=WHITE,
                font=(
                    "Helvetica",
                    8,
                    "bold"
                )
            ).pack(
                side=RIGHT,
                padx=20,
                pady=12
            )

            amounts = Frame(
                card,
                bg=WHITE
            )

            amounts.pack(
                fill=X,
                padx=20,
                pady=(18, 12)
            )

            for column in range(3):
                amounts.grid_columnconfigure(
                    column,
                    weight=1
                )

            amount_items = [
                (
                    "TOTAL FEE",
                    money(
                        total_value
                    ),
                    BLUE
                ),
                (
                    "PAID",
                    money(
                        paid_value
                    ),
                    GREEN
                ),
                (
                    "OUTSTANDING",
                    money(
                        due_value
                    ),
                    (
                        GREEN
                        if due_value <= 0
                        else RED
                    )
                )
            ]

            for column, item in enumerate(
                amount_items
            ):

                title_text, value_text, value_color = (
                    item
                )

                box = Frame(
                    amounts,
                    bg=WHITE
                )

                box.grid(
                    row=0,
                    column=column,
                    sticky="w"
                )

                Label(
                    box,
                    text=title_text,
                    bg=WHITE,
                    fg=MUTED,
                    font=(
                        "Helvetica",
                        8,
                        "bold"
                    )
                ).pack(
                    anchor="w"
                )

                Label(
                    box,
                    text=value_text,
                    bg=WHITE,
                    fg=value_color,
                    font=(
                        "Helvetica",
                        14,
                        "bold"
                    )
                ).pack(
                    anchor="w",
                    pady=(5, 0)
                )

            footer = Frame(
                card,
                bg=WHITE
            )

            footer.pack(
                fill=X,
                padx=20,
                pady=(8, 18)
            )

            last_payment_date = (
                semester_row.get(
                    "Last_Payment_Date"
                )
            )

            if last_payment_date:
                last_payment_text = (
                    f"Last Payment: "
                    f"{format_date(last_payment_date)}"
                    f"  •  "
                    f"{semester_row.get('Last_Payment_Mode') or '-'}"
                    f"  •  "
                    f"{money(semester_row.get('Last_Payment_Amount'))}"
                )
            else:
                last_payment_text = (
                    "Last Payment: "
                    "No payment recorded"
                )

            Label(
                footer,
                text=last_payment_text,
                bg=WHITE,
                fg=MUTED,
                font=(
                    "Helvetica",
                    9
                )
            ).pack(
                side=LEFT
            )

            Button(
                footer,
                text="VIEW FEE DETAILS",
                command=lambda row=semester_row: (
                    open_fee_details(
                        row
                    )
                ),
                bg=BLUE,
                fg=WHITE,
                activebackground="#1D4ED8",
                activeforeground=WHITE,
                relief=FLAT,
                bd=0,
                cursor="hand2",
                font=(
                    "Helvetica",
                    9,
                    "bold"
                ),
                padx=18,
                pady=9
            ).pack(
                side=RIGHT
            )

    else:

        empty = Frame(
            records,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        empty.pack(
            fill=X
        )

        Label(
            empty,
            text="No fee records found.",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Helvetica",
                13,
                "bold"
            )
        ).pack(
            pady=(35, 8)
        )

        Label(
            empty,
            text=(
                "Your assigned semester fees "
                "will appear here."
            ),
            bg=WHITE,
            fg=MUTED,
            font=(
                "Helvetica",
                10
            )
        ).pack(
            pady=(0, 35)
        )


# ============================================================
# OPTIONAL STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    root = Tk()

    root.title(
        "Student My Fees"
    )

    root.geometry(
        "1200x760"
    )

    root.configure(
        bg=DEFAULT_COLORS["BG"]
    )

    test_registration_no = input(
        "Enter Student Registration No: "
    ).strip()

    show_student_fees(
        parent=root,
        registration_no=(
            test_registration_no
        ),
        student_name="Student"
    )

    root.mainloop()
