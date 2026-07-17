"""
reports_page.py
Accountant Personal Collection Report Center

This page is intentionally designed differently from the Payments page.

Workflow:
1. Choose report period / custom dates / payment mode.
2. Click GENERATE MY REPORT.
3. Preview a formal report inside Tkinter.
4. Export the same generated report to PDF or CSV.

Security:
- No accountant selector exists.
- The logged-in accountant identity is fixed.
- Every database query is restricted to that accountant's collection records.
"""

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime, timedelta

import mysql.connector
from mysql.connector import Error


# ============================================================
# DATABASE
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "9439",
    "database": "OCAC_GROUP2",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# COLORS
# ============================================================

PAGE_BG = "#F4F7FB"
WHITE = "#FFFFFF"
TEXT = "#101828"
MUTED = "#667085"
BORDER = "#D9E2EC"
BLUE = "#2563EB"
BLUE_DARK = "#1D4ED8"
BLUE_LIGHT = "#EFF6FF"
GREEN = "#16A34A"
GREEN_LIGHT = "#F0FDF4"
PURPLE = "#7C3AED"
PURPLE_LIGHT = "#F5F3FF"
ORANGE = "#F59E0B"
ORANGE_LIGHT = "#FFFBEB"
RED = "#DC2626"
GRAY_BUTTON = "#475467"
PREVIEW_BG = "#E8EDF4"


# ============================================================
# HELPERS
# ============================================================

def money(value):
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"


def pdf_money(value):
    try:
        return f"Rs. {float(value):,.2f}"
    except (TypeError, ValueError):
        return "Rs. 0.00"


def safe_text(value):
    return "" if value is None else str(value)


def display_date(value):
    if isinstance(value, datetime):
        value = value.date()

    if isinstance(value, date):
        return value.strftime("%d %b %Y")

    text = safe_text(value).strip()

    try:
        return date.fromisoformat(text).strftime("%d %b %Y")
    except ValueError:
        return text


# ============================================================
# MAIN REPORT PAGE
# ============================================================

class AccountantReportsPage:

    def __init__(
        self,
        parent,
        current_user_name="",
        current_user_id="",
        current_username="",
        user_role="Accountant",
        back_command=None,
    ):

        self.parent = parent

        self.current_user_name = str(
            current_user_name or ""
        ).strip()

        self.current_user_id = str(
            current_user_id or ""
        ).strip()

        self.current_username = str(
            current_username or ""
        ).strip()

        self.user_role = str(
            user_role or "Accountant"
        ).strip()

        self.back_command = back_command

        self.generated_rows = []
        self.generated_mode_summary = {}
        self.generated_total = 0.0
        self.generated_count = 0
        self.generated_average = 0.0
        self.generated_from_date = None
        self.generated_to_date = None
        self.generated_at = None
        self.report_generated = False

        self.period_var = tk.StringVar(
            value="This Month"
        )

        self.from_var = tk.StringVar()

        self.to_var = tk.StringVar()

        self.mode_var = tk.StringVar(
            value="All Payment Modes"
        )

        self.status_var = tk.StringVar(
            value=(
                "Choose report options and click "
                "GENERATE MY REPORT."
            )
        )

        self.root_frame = tk.Frame(
            parent,
            bg=PAGE_BG
        )

        self.root_frame.pack(
            fill="both",
            expand=True
        )

        self.build_styles()

        self.build_ui()

        self.apply_period_defaults()

        self.show_empty_preview()


    # ========================================================
    # STYLE
    # ========================================================

    def build_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "ReportPreview.Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 9)
        )

        style.configure(
            "ReportPreview.Treeview.Heading",
            background="#EEF3F9",
            foreground="#344054",
            relief="flat",
            font=("Segoe UI", 8, "bold")
        )

        style.map(
            "ReportPreview.Treeview",
            background=[
                ("selected", "#DCEBFF")
            ],
            foreground=[
                ("selected", TEXT)
            ]
        )


    # ========================================================
    # DATABASE ACCOUNTANT FILTER
    # ========================================================

    def collector_filter_sql(
        self,
        alias="fp"
    ):
        """
        Restrict every report query to the current accountant.

        Existing database examples:
            Vijay Nayak - ACC041
            Debananda Kuanr - ACC085
            Administrator
            Accountant

        The dashboard may provide a differently padded ID such as ACC0041.
        Therefore the current accountant's name prefix is also supported:
            Vijay Nayak - %
        """

        conditions = []

        params = []


        if self.current_user_id:

            conditions.append(
                f"""
                LOWER(TRIM({alias}.Collected_By))
                =
                LOWER(TRIM(%s))
                """
            )

            params.append(
                self.current_user_id
            )


        if self.current_user_name:

            conditions.append(
                f"""
                LOWER(TRIM({alias}.Collected_By))
                =
                LOWER(TRIM(%s))
                """
            )

            params.append(
                self.current_user_name
            )


            conditions.append(
                f"""
                LOWER(TRIM({alias}.Collected_By))
                LIKE
                LOWER(%s)
                """
            )

            params.append(
                f"{self.current_user_name} - %"
            )


        if self.current_username:

            conditions.append(
                f"""
                LOWER(TRIM({alias}.Collected_By))
                =
                LOWER(TRIM(%s))
                """
            )

            params.append(
                self.current_username
            )


        if not conditions:

            return (
                "1 = 0",
                []
            )


        return (
            "("
            +
            " OR ".join(
                conditions
            )
            +
            ")",
            params
        )


    # ========================================================
    # UI HELPERS
    # ========================================================

    def make_button(
        self,
        parent,
        text,
        command,
        bg,
        width=None
    ):

        options = {
            "text": text,
            "command": command,
            "bg": bg,
            "fg": WHITE,
            "activebackground": bg,
            "activeforeground": WHITE,
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "font": (
                "Segoe UI",
                9,
                "bold"
            ),
            "padx": 18,
            "pady": 10
        }

        if width is not None:
            options["width"] = width

        return tk.Button(
            parent,
            **options
        )


    def section_title(
        self,
        parent,
        title,
        subtitle=""
    ):

        tk.Label(
            parent,
            text=title,
            bg=WHITE,
            fg=TEXT,
            font=(
                "Segoe UI",
                12,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        if subtitle:

            tk.Label(
                parent,
                text=subtitle,
                bg=WHITE,
                fg=MUTED,
                font=(
                    "Segoe UI",
                    8
                )
            ).pack(
                anchor="w",
                pady=(3, 0)
            )


    def field_label(
        self,
        parent,
        text,
        row,
        column
    ):

        tk.Label(
            parent,
            text=text,
            bg=WHITE,
            fg=MUTED,
            font=(
                "Segoe UI",
                8,
                "bold"
            )
        ).grid(
            row=row,
            column=column,
            sticky="w",
            padx=5,
            pady=(0, 6)
        )


    # ========================================================
    # BUILD PAGE
    # ========================================================

    def build_ui(self):

        self.build_report_center()

        self.build_preview_area()


    # ========================================================
    # REPORT CONFIGURATION AREA
    # ========================================================

    def build_report_center(self):

        center = tk.Frame(
            self.root_frame,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        center.pack(
            fill="x",
            padx=26,
            pady=(20, 14)
        )


        top = tk.Frame(
            center,
            bg=WHITE
        )

        top.pack(
            fill="x",
            padx=22,
            pady=(18, 14)
        )


        title_area = tk.Frame(
            top,
            bg=WHITE
        )

        title_area.pack(
            side="left"
        )


        self.section_title(
            title_area,
            "MY REPORT CENTER",
            (
                "Create a personal collection report "
                "for the currently logged-in accountant."
            )
        )


        owner_box = tk.Frame(
            top,
            bg=BLUE_LIGHT
        )

        owner_box.pack(
            side="right"
        )


        tk.Label(
            owner_box,
            text="REPORT OWNER",
            bg=BLUE_LIGHT,
            fg=BLUE,
            font=(
                "Segoe UI",
                7,
                "bold"
            )
        ).pack(
            anchor="e",
            padx=14,
            pady=(8, 2)
        )


        tk.Label(
            owner_box,
            text=(
                f"{self.current_user_name or 'Accountant'}"
                f"  •  "
                f"{self.current_user_id or 'No ID'}"
            ),
            bg=BLUE_LIGHT,
            fg=TEXT,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack(
            anchor="e",
            padx=14,
            pady=(0, 8)
        )


        tk.Frame(
            center,
            bg=BORDER,
            height=1
        ).pack(
            fill="x",
            padx=22
        )


        form = tk.Frame(
            center,
            bg=WHITE
        )

        form.pack(
            fill="x",
            padx=22,
            pady=18
        )


        for column in range(4):

            form.grid_columnconfigure(
                column,
                weight=1
            )


        self.field_label(
            form,
            "REPORT PERIOD",
            0,
            0
        )

        self.field_label(
            form,
            "FROM DATE",
            0,
            1
        )

        self.field_label(
            form,
            "TO DATE",
            0,
            2
        )

        self.field_label(
            form,
            "PAYMENT MODE",
            0,
            3
        )


        period_combo = ttk.Combobox(
            form,
            textvariable=self.period_var,
            values=[
                "Today",
                "Last 7 Days",
                "This Month",
                "This Year",
                "All Time",
                "Custom Range"
            ],
            state="readonly",
            font=(
                "Segoe UI",
                10
            )
        )

        period_combo.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 8),
            ipady=6
        )

        period_combo.bind(
            "<<ComboboxSelected>>",
            self.on_period_changed
        )


        self.from_entry = tk.Entry(
            form,
            textvariable=self.from_var,
            font=(
                "Segoe UI",
                10
            ),
            relief="solid",
            bd=1
        )

        self.from_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=4,
            ipady=8
        )


        self.to_entry = tk.Entry(
            form,
            textvariable=self.to_var,
            font=(
                "Segoe UI",
                10
            ),
            relief="solid",
            bd=1
        )

        self.to_entry.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=4,
            ipady=8
        )


        mode_combo = ttk.Combobox(
            form,
            textvariable=self.mode_var,
            values=[
                "All Payment Modes",
                "Cash",
                "UPI",
                "Card",
                "Bank Transfer",
                "Cheque",
                "Other"
            ],
            state="readonly",
            font=(
                "Segoe UI",
                10
            )
        )

        mode_combo.grid(
            row=1,
            column=3,
            sticky="ew",
            padx=(8, 0),
            ipady=6
        )


        action_row = tk.Frame(
            center,
            bg=WHITE
        )

        action_row.pack(
            fill="x",
            padx=22,
            pady=(0, 18)
        )


        tk.Label(
            action_row,
            textvariable=self.status_var,
            bg=WHITE,
            fg=MUTED,
            font=(
                "Segoe UI",
                8
            )
        ).pack(
            side="left"
        )


        self.make_button(
            action_row,
            "RESET",
            self.reset_report,
            GRAY_BUTTON
        ).pack(
            side="right",
            padx=(8, 0)
        )


        self.make_button(
            action_row,
            "GENERATE MY REPORT",
            self.generate_report,
            BLUE
        ).pack(
            side="right"
        )


    # ========================================================
    # PREVIEW AREA
    # ========================================================

    def build_preview_area(self):

        preview_outer = tk.Frame(
            self.root_frame,
            bg=PREVIEW_BG,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        preview_outer.pack(
            fill="both",
            expand=True,
            padx=26,
            pady=(0, 20)
        )


        preview_toolbar = tk.Frame(
            preview_outer,
            bg=PREVIEW_BG
        )

        preview_toolbar.pack(
            fill="x",
            padx=18,
            pady=12
        )


        tk.Label(
            preview_toolbar,
            text="GENERATED REPORT PREVIEW",
            bg=PREVIEW_BG,
            fg=TEXT,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            side="left"
        )


        self.export_pdf_button = self.make_button(
            preview_toolbar,
            "EXPORT PDF",
            self.export_pdf,
            PURPLE
        )

        self.export_pdf_button.pack(
            side="right"
        )


        self.export_csv_button = self.make_button(
            preview_toolbar,
            "EXPORT CSV",
            self.export_csv,
            GREEN
        )

        self.export_csv_button.pack(
            side="right",
            padx=(0, 8)
        )


        document_holder = tk.Frame(
            preview_outer,
            bg=PREVIEW_BG
        )

        document_holder.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=(0, 20)
        )


        self.document_canvas = tk.Canvas(
            document_holder,
            bg=PREVIEW_BG,
            highlightthickness=0
        )

        self.document_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        document_scrollbar = ttk.Scrollbar(
            document_holder,
            orient="vertical",
            command=self.document_canvas.yview
        )

        document_scrollbar.pack(
            side="right",
            fill="y"
        )


        self.document_canvas.configure(
            yscrollcommand=document_scrollbar.set
        )


        self.document = tk.Frame(
            self.document_canvas,
            bg=WHITE,
            highlightbackground="#C7D0DB",
            highlightthickness=1
        )


        self.document_window = self.document_canvas.create_window(
            (0, 0),
            window=self.document,
            anchor="n"
        )


        self.document.bind(
            "<Configure>",
            self.on_document_configure
        )


        self.document_canvas.bind(
            "<Configure>",
            self.on_canvas_configure
        )


        self.document_canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )


    def on_document_configure(
        self,
        event=None
    ):

        self.document_canvas.configure(
            scrollregion=
            self.document_canvas.bbox(
                "all"
            )
        )


    def on_canvas_configure(
        self,
        event
    ):

        width = max(
            900,
            event.width - 80
        )

        self.document_canvas.itemconfigure(
            self.document_window,
            width=width
        )

        self.document_canvas.coords(
            self.document_window,
            event.width / 2,
            0
        )


    def on_mousewheel(
        self,
        event
    ):

        try:

            self.document_canvas.yview_scroll(
                int(
                    -1 * (
                        event.delta / 120
                    )
                ),
                "units"
            )

        except tk.TclError:

            pass


    def clear_document(self):

        for child in (
            self.document.winfo_children()
        ):

            child.destroy()


    # ========================================================
    # EMPTY PREVIEW
    # ========================================================

    def show_empty_preview(self):

        self.clear_document()


        empty = tk.Frame(
            self.document,
            bg=WHITE,
            height=500
        )

        empty.pack(
            fill="both",
            expand=True
        )

        empty.pack_propagate(
            False
        )


        tk.Label(
            empty,
            text="REPORT PREVIEW",
            bg=WHITE,
            fg="#98A2B3",
            font=(
                "Segoe UI",
                18,
                "bold"
            )
        ).pack(
            pady=(145, 10)
        )


        tk.Label(
            empty,
            text=(
                "Your generated personal collection report "
                "will appear here."
            ),
            bg=WHITE,
            fg=MUTED,
            font=(
                "Segoe UI",
                10
            )
        ).pack()


        tk.Label(
            empty,
            text=(
                "Select a report period and click "
                "GENERATE MY REPORT."
            ),
            bg=WHITE,
            fg="#98A2B3",
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            pady=(7, 0)
        )


        self.set_export_state(
            "disabled"
        )


    # ========================================================
    # PERIOD / DATE LOGIC
    # ========================================================

    def set_date_entry_state(
        self,
        state
    ):

        self.from_entry.configure(
            state=state
        )

        self.to_entry.configure(
            state=state
        )


    def on_period_changed(
        self,
        event=None
    ):

        self.apply_period_defaults()


    def apply_period_defaults(self):

        today = date.today()

        period = self.period_var.get()


        if period == "Today":

            start = today

            end = today

            self.from_var.set(
                start.isoformat()
            )

            self.to_var.set(
                end.isoformat()
            )

            self.set_date_entry_state(
                "disabled"
            )


        elif period == "Last 7 Days":

            start = (
                today
                -
                timedelta(
                    days=6
                )
            )

            end = today

            self.from_var.set(
                start.isoformat()
            )

            self.to_var.set(
                end.isoformat()
            )

            self.set_date_entry_state(
                "disabled"
            )


        elif period == "This Month":

            start = today.replace(
                day=1
            )

            end = today

            self.from_var.set(
                start.isoformat()
            )

            self.to_var.set(
                end.isoformat()
            )

            self.set_date_entry_state(
                "disabled"
            )


        elif period == "This Year":

            start = today.replace(
                month=1,
                day=1
            )

            end = today

            self.from_var.set(
                start.isoformat()
            )

            self.to_var.set(
                end.isoformat()
            )

            self.set_date_entry_state(
                "disabled"
            )


        elif period == "All Time":

            self.from_var.set(
                ""
            )

            self.to_var.set(
                ""
            )

            self.set_date_entry_state(
                "disabled"
            )


        elif period == "Custom Range":

            if not self.from_var.get():

                self.from_var.set(
                    today.replace(
                        day=1
                    ).isoformat()
                )


            if not self.to_var.get():

                self.to_var.set(
                    today.isoformat()
                )


            self.set_date_entry_state(
                "normal"
            )


    def selected_date_bounds(self):

        today = date.today()

        period = self.period_var.get()


        if period == "All Time":

            return (
                None,
                None
            )


        from_text = (
            self.from_var.get().strip()
        )

        to_text = (
            self.to_var.get().strip()
        )


        try:

            start = date.fromisoformat(
                from_text
            )

            end = date.fromisoformat(
                to_text
            )

        except ValueError:

            raise ValueError(
                (
                    "From Date and To Date must use "
                    "YYYY-MM-DD format."
                )
            )


        if start > end:

            raise ValueError(
                (
                    "From Date cannot be after "
                    "To Date."
                )
            )


        if end > today:

            raise ValueError(
                (
                    "To Date cannot be after today's date."
                    "\n\n"
                    f"Today's Date: {today.isoformat()}"
                )
            )


        return (
            start,
            end
        )


    # ========================================================
    # GENERATE REPORT
    # ========================================================

    def generate_report(self):

        connection = None

        cursor = None


        try:

            start_date, end_date = (
                self.selected_date_bounds()
            )


            collector_sql, collector_params = (
                self.collector_filter_sql(
                    "fp"
                )
            )


            conditions = [
                collector_sql
            ]

            params = list(
                collector_params
            )


            if start_date is not None:

                conditions.append(
                    "fp.Payment_Date >= %s"
                )

                params.append(
                    start_date
                )


            if end_date is not None:

                conditions.append(
                    "fp.Payment_Date <= %s"
                )

                params.append(
                    end_date
                )


            selected_mode = (
                self.mode_var.get().strip()
            )


            if (
                selected_mode
                and
                selected_mode
                !=
                "All Payment Modes"
            ):

                conditions.append(
                    "fp.Payment_Mode = %s"
                )

                params.append(
                    selected_mode
                )


            where_sql = (
                " AND ".join(
                    conditions
                )
            )


            query = f"""
                SELECT
                    fp.Payment_ID,
                    fp.Payment_Date,
                    fp.Created_At,
                    r.Name,
                    sf.Registration_No,
                    COALESCE(
                        sd.Course,
                        ''
                    ),
                    COALESCE(
                        fs.Semester,
                        sd.Semester,
                        ''
                    ),
                    fp.Payment_Mode,
                    COALESCE(
                        fp.Transaction_Reference,
                        ''
                    ),
                    fp.Amount,
                    COALESCE(
                        fp.Remarks,
                        ''
                    ),
                    COALESCE(
                        fp.Collected_By,
                        ''
                    )
                FROM fee_payments fp

                INNER JOIN student_fees sf
                    ON
                    fp.Student_Fee_ID
                    =
                    sf.Student_Fee_ID

                INNER JOIN registration r
                    ON
                    sf.Registration_No
                    =
                    r.Registration_No

                LEFT JOIN student_details sd
                    ON
                    sf.Registration_No
                    =
                    sd.Registration_No

                LEFT JOIN fee_structures fs
                    ON
                    sf.Fee_Structure_ID
                    =
                    fs.Fee_Structure_ID

                WHERE
                    {where_sql}

                ORDER BY
                    fp.Payment_Date ASC,
                    fp.Created_At ASC,
                    fp.Payment_ID ASC
            """


            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute(
                query,
                params
            )

            result = cursor.fetchall()


            self.generated_rows = []


            for item in result:

                created_at = item[2]

                if isinstance(
                    created_at,
                    datetime
                ):

                    date_time_text = (
                        created_at.strftime(
                            "%d-%m-%Y %I:%M %p"
                        )
                    )

                else:

                    date_time_text = (
                        display_date(
                            item[1]
                        )
                    )


                semester = (
                    safe_text(
                        item[6]
                    ).strip()
                )


                if (
                    semester
                    and
                    not semester.lower().startswith(
                        "semester"
                    )
                ):

                    semester = (
                        f"Semester {semester}"
                    )


                self.generated_rows.append(
                    {
                        "payment_id": item[0],
                        "payment_date": item[1],
                        "date_time": date_time_text,
                        "student": safe_text(
                            item[3]
                        ),
                        "reg_no": safe_text(
                            item[4]
                        ),
                        "course": safe_text(
                            item[5]
                        ),
                        "semester": semester,
                        "mode": safe_text(
                            item[7]
                        ),
                        "reference": safe_text(
                            item[8]
                        ),
                        "amount": float(
                            item[9] or 0
                        ),
                        "remarks": safe_text(
                            item[10]
                        ),
                        "collected_by": safe_text(
                            item[11]
                        )
                    }
                )


            self.generated_total = sum(
                row["amount"]
                for row in self.generated_rows
            )


            self.generated_count = len(
                self.generated_rows
            )


            if self.generated_count:

                self.generated_average = (
                    self.generated_total
                    /
                    self.generated_count
                )

            else:

                self.generated_average = 0.0


            self.generated_mode_summary = (
                self.calculate_mode_summary()
            )


            self.generated_from_date = (
                start_date
            )

            self.generated_to_date = (
                end_date
            )

            self.generated_at = (
                datetime.now()
            )

            self.report_generated = True


            self.render_report_preview()


            self.set_export_state(
                "normal"
            )


            self.status_var.set(
                (
                    f"Report generated successfully: "
                    f"{self.generated_count} payment(s), "
                    f"{money(self.generated_total)} collected."
                )
            )


        except ValueError as error:

            messagebox.showwarning(
                "Invalid Report Period",
                str(error),
                parent=
                self.root_frame.winfo_toplevel()
            )


        except Error as error:

            messagebox.showerror(
                "Database Error",
                (
                    "Unable to generate the report."
                    "\n\n"
                    f"{error}"
                ),
                parent=
                self.root_frame.winfo_toplevel()
            )


        except Exception as error:

            messagebox.showerror(
                "Report Error",
                (
                    "Unable to generate the report."
                    "\n\n"
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
                parent=
                self.root_frame.winfo_toplevel()
            )


        finally:

            if cursor:

                cursor.close()


            if (
                connection
                and
                connection.is_connected()
            ):

                connection.close()


    def calculate_mode_summary(self):

        summary = {}


        for row in self.generated_rows:

            mode = (
                row["mode"].strip()
                or
                "Other"
            )


            if mode not in summary:

                summary[mode] = {
                    "count": 0,
                    "amount": 0.0
                }


            summary[mode]["count"] += 1

            summary[mode]["amount"] += (
                row["amount"]
            )


        return summary


    # ========================================================
    # RENDER REPORT PREVIEW
    # ========================================================

    def render_report_preview(self):

        self.clear_document()


        document_body = tk.Frame(
            self.document,
            bg=WHITE
        )

        document_body.pack(
            fill="both",
            expand=True,
            padx=42,
            pady=34
        )


        # ----------------------------------------------------
        # REPORT HEADER
        # ----------------------------------------------------

        tk.Label(
            document_body,
            text=(
                "FEE STATUS MANAGEMENT SYSTEM"
            ),
            bg=WHITE,
            fg=TEXT,
            font=(
                "Segoe UI",
                17,
                "bold"
            )
        ).pack()


        tk.Label(
            document_body,
            text=(
                "ACCOUNTANT COLLECTION REPORT"
            ),
            bg=WHITE,
            fg=BLUE,
            font=(
                "Segoe UI",
                11,
                "bold"
            )
        ).pack(
            pady=(4, 0)
        )


        tk.Frame(
            document_body,
            bg=BLUE,
            height=2
        ).pack(
            fill="x",
            pady=(18, 20)
        )


        # ----------------------------------------------------
        # REPORT IDENTITY
        # ----------------------------------------------------

        identity = tk.Frame(
            document_body,
            bg=WHITE
        )

        identity.pack(
            fill="x"
        )


        identity.grid_columnconfigure(
            0,
            weight=1
        )

        identity.grid_columnconfigure(
            1,
            weight=1
        )


        self.preview_info(
            identity,
            "ACCOUNTANT",
            self.current_user_name
            or
            "Accountant",
            0,
            0
        )


        self.preview_info(
            identity,
            "ACCOUNT ID",
            self.current_user_id
            or
            "—",
            0,
            1
        )


        self.preview_info(
            identity,
            "REPORT PERIOD",
            self.report_period_text(),
            1,
            0
        )


        self.preview_info(
            identity,
            "PAYMENT MODE",
            self.mode_var.get(),
            1,
            1
        )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        summary_frame = tk.Frame(
            document_body,
            bg=WHITE
        )

        summary_frame.pack(
            fill="x",
            pady=(24, 22)
        )


        self.preview_summary_card(
            summary_frame,
            "TOTAL COLLECTION",
            money(
                self.generated_total
            ),
            BLUE_LIGHT,
            BLUE
        )


        self.preview_summary_card(
            summary_frame,
            "TOTAL PAYMENTS",
            str(
                self.generated_count
            ),
            GREEN_LIGHT,
            GREEN
        )


        self.preview_summary_card(
            summary_frame,
            "AVERAGE PAYMENT",
            money(
                self.generated_average
            ),
            PURPLE_LIGHT,
            PURPLE
        )


        # ----------------------------------------------------
        # PAYMENT MODE SUMMARY
        # ----------------------------------------------------

        section = tk.Frame(
            document_body,
            bg=WHITE
        )

        section.pack(
            fill="x",
            pady=(2, 20)
        )


        tk.Label(
            section,
            text="PAYMENT MODE SUMMARY",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            anchor="w",
            pady=(0, 10)
        )


        if self.generated_mode_summary:

            for mode in sorted(
                self.generated_mode_summary
            ):

                data = (
                    self.generated_mode_summary[
                        mode
                    ]
                )


                row = tk.Frame(
                    section,
                    bg="#F8FAFC"
                )

                row.pack(
                    fill="x",
                    pady=2
                )


                tk.Label(
                    row,
                    text=mode,
                    bg="#F8FAFC",
                    fg=TEXT,
                    width=22,
                    anchor="w",
                    font=(
                        "Segoe UI",
                        9,
                        "bold"
                    )
                ).pack(
                    side="left",
                    padx=12,
                    pady=8
                )


                payment_word = (
                    "Payment"
                    if data["count"] == 1
                    else
                    "Payments"
                )


                tk.Label(
                    row,
                    text=(
                        f"{data['count']} "
                        f"{payment_word}"
                    ),
                    bg="#F8FAFC",
                    fg=MUTED,
                    font=(
                        "Segoe UI",
                        9
                    )
                ).pack(
                    side="left"
                )


                tk.Label(
                    row,
                    text=money(
                        data["amount"]
                    ),
                    bg="#F8FAFC",
                    fg=TEXT,
                    font=(
                        "Segoe UI",
                        9,
                        "bold"
                    )
                ).pack(
                    side="right",
                    padx=12
                )


        else:

            tk.Label(
                section,
                text=(
                    "No payment mode data "
                    "for this report."
                ),
                bg=WHITE,
                fg=MUTED,
                font=(
                    "Segoe UI",
                    9
                )
            ).pack(
                anchor="w"
            )


        # ----------------------------------------------------
        # TRANSACTION TABLE
        # ----------------------------------------------------

        tk.Label(
            document_body,
            text="TRANSACTION DETAILS",
            bg=WHITE,
            fg=TEXT,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            anchor="w",
            pady=(2, 10)
        )


        table_frame = tk.Frame(
            document_body,
            bg=WHITE
        )

        table_frame.pack(
            fill="both",
            expand=True
        )


        columns = (
            "id",
            "date",
            "student",
            "reg",
            "semester",
            "mode",
            "amount"
        )


        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="ReportPreview.Treeview",
            height=max(
                5,
                min(
                    12,
                    self.generated_count
                )
            )
        )


        headings = {
            "id": "ID",
            "date": "DATE",
            "student": "STUDENT",
            "reg": "REG. NO.",
            "semester": "SEMESTER",
            "mode": "MODE",
            "amount": "AMOUNT"
        }


        widths = {
            "id": 55,
            "date": 105,
            "student": 180,
            "reg": 105,
            "semester": 100,
            "mode": 100,
            "amount": 110
        }


        for column in columns:

            tree.heading(
                column,
                text=headings[
                    column
                ]
            )

            tree.column(
                column,
                width=widths[
                    column
                ],
                minwidth=50,
                anchor=(
                    "w"
                    if column
                    ==
                    "student"
                    else
                    "center"
                )
            )


        for row in self.generated_rows:

            tree.insert(
                "",
                "end",
                values=(
                    row["payment_id"],
                    display_date(
                        row["payment_date"]
                    ),
                    row["student"],
                    row["reg_no"],
                    row["semester"],
                    row["mode"],
                    money(
                        row["amount"]
                    )
                )
            )


        tree.pack(
            fill="both",
            expand=True
        )


        if not self.generated_rows:

            tk.Label(
                table_frame,
                text=(
                    "No payment transactions found "
                    "for the selected report options."
                ),
                bg=WHITE,
                fg=MUTED,
                font=(
                    "Segoe UI",
                    9
                )
            ).pack(
                pady=14
            )


        # ----------------------------------------------------
        # REPORT TOTAL
        # ----------------------------------------------------

        total_bar = tk.Frame(
            document_body,
            bg=BLUE_LIGHT
        )

        total_bar.pack(
            fill="x",
            pady=(18, 0)
        )


        tk.Label(
            total_bar,
            text="TOTAL COLLECTION",
            bg=BLUE_LIGHT,
            fg=TEXT,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            side="left",
            padx=14,
            pady=12
        )


        tk.Label(
            total_bar,
            text=money(
                self.generated_total
            ),
            bg=BLUE_LIGHT,
            fg=BLUE,
            font=(
                "Segoe UI",
                13,
                "bold"
            )
        ).pack(
            side="right",
            padx=14,
            pady=12
        )


        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        footer = tk.Frame(
            document_body,
            bg=WHITE
        )

        footer.pack(
            fill="x",
            pady=(22, 0)
        )


        tk.Frame(
            footer,
            bg=BORDER,
            height=1
        ).pack(
            fill="x",
            pady=(0, 12)
        )


        tk.Label(
            footer,
            text=(
                "Generated By: "
                f"{self.current_user_name}"
                " - "
                f"{self.current_user_id}"
            ),
            bg=WHITE,
            fg=MUTED,
            font=(
                "Segoe UI",
                8
            )
        ).pack(
            anchor="w"
        )


        tk.Label(
            footer,
            text=(
                "Generated On: "
                f"{self.generated_at.strftime('%d %B %Y, %I:%M %p')}"
            ),
            bg=WHITE,
            fg=MUTED,
            font=(
                "Segoe UI",
                8
            )
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


    def preview_info(
        self,
        parent,
        label,
        value,
        row,
        column
    ):

        box = tk.Frame(
            parent,
            bg=WHITE
        )

        box.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=8,
            pady=6
        )


        tk.Label(
            box,
            text=label,
            bg=WHITE,
            fg=MUTED,
            font=(
                "Segoe UI",
                7,
                "bold"
            )
        ).pack(
            anchor="w"
        )


        tk.Label(
            box,
            text=value,
            bg=WHITE,
            fg=TEXT,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


    def preview_summary_card(
        self,
        parent,
        title,
        value,
        bg,
        fg
    ):

        card = tk.Frame(
            parent,
            bg=bg
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )


        tk.Label(
            card,
            text=title,
            bg=bg,
            fg=MUTED,
            font=(
                "Segoe UI",
                7,
                "bold"
            )
        ).pack(
            pady=(12, 5)
        )


        tk.Label(
            card,
            text=value,
            bg=bg,
            fg=fg,
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).pack(
            pady=(0, 12)
        )


    def report_period_text(self):

        if (
            self.generated_from_date is None
            and
            self.generated_to_date is None
        ):

            return "All Time"


        return (
            f"{display_date(self.generated_from_date)}"
            "  -  "
            f"{display_date(self.generated_to_date)}"
        )


    # ========================================================
    # RESET
    # ========================================================

    def reset_report(self):

        self.period_var.set(
            "This Month"
        )

        self.mode_var.set(
            "All Payment Modes"
        )

        self.apply_period_defaults()

        self.generated_rows = []

        self.generated_mode_summary = {}

        self.generated_total = 0.0

        self.generated_count = 0

        self.generated_average = 0.0

        self.generated_from_date = None

        self.generated_to_date = None

        self.generated_at = None

        self.report_generated = False


        self.status_var.set(
            (
                "Choose report options and click "
                "GENERATE MY REPORT."
            )
        )


        self.show_empty_preview()


    def set_export_state(
        self,
        state
    ):

        self.export_pdf_button.configure(
            state=state
        )

        self.export_csv_button.configure(
            state=state
        )


    # ========================================================
    # CSV EXPORT
    # ========================================================

    def export_csv(self):

        if not self.report_generated:

            messagebox.showwarning(
                "Generate Report First",
                (
                    "Please generate your report "
                    "before exporting it."
                ),
                parent=
                self.root_frame.winfo_toplevel()
            )

            return


        default_name = (
            "my_collection_report_"
            f"{date.today().isoformat()}"
            ".csv"
        )


        path = filedialog.asksaveasfilename(
            parent=
            self.root_frame.winfo_toplevel(),
            title=(
                "Export Personal Collection Report"
            ),
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[
                (
                    "CSV File",
                    "*.csv"
                )
            ]
        )


        if not path:

            return


        try:

            with open(
                path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.writer(
                    file
                )


                writer.writerow(
                    [
                        "FEE STATUS MANAGEMENT SYSTEM"
                    ]
                )

                writer.writerow(
                    [
                        "ACCOUNTANT COLLECTION REPORT"
                    ]
                )

                writer.writerow(
                    []
                )


                writer.writerow(
                    [
                        "Accountant",
                        self.current_user_name
                    ]
                )

                writer.writerow(
                    [
                        "Account ID",
                        self.current_user_id
                    ]
                )

                writer.writerow(
                    [
                        "Report Period",
                        self.report_period_text()
                    ]
                )

                writer.writerow(
                    [
                        "Payment Mode",
                        self.mode_var.get()
                    ]
                )

                writer.writerow(
                    [
                        "Generated On",
                        self.generated_at.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    ]
                )


                writer.writerow(
                    []
                )


                writer.writerow(
                    [
                        "Total Collection",
                        f"{self.generated_total:.2f}"
                    ]
                )

                writer.writerow(
                    [
                        "Total Payments",
                        self.generated_count
                    ]
                )

                writer.writerow(
                    [
                        "Average Payment",
                        f"{self.generated_average:.2f}"
                    ]
                )


                writer.writerow(
                    []
                )


                writer.writerow(
                    [
                        "PAYMENT MODE SUMMARY"
                    ]
                )


                writer.writerow(
                    [
                        "Payment Mode",
                        "Payments",
                        "Amount"
                    ]
                )


                for mode in sorted(
                    self.generated_mode_summary
                ):

                    data = (
                        self.generated_mode_summary[
                            mode
                        ]
                    )


                    writer.writerow(
                        [
                            mode,
                            data["count"],
                            f"{data['amount']:.2f}"
                        ]
                    )


                writer.writerow(
                    []
                )


                writer.writerow(
                    [
                        "Payment ID",
                        "Payment Date",
                        "Date & Time",
                        "Student",
                        "Registration No.",
                        "Course",
                        "Semester",
                        "Payment Mode",
                        "Transaction Reference",
                        "Amount",
                        "Remarks",
                        "Collected By"
                    ]
                )


                for row in self.generated_rows:

                    writer.writerow(
                        [
                            row["payment_id"],
                            display_date(
                                row["payment_date"]
                            ),
                            row["date_time"],
                            row["student"],
                            row["reg_no"],
                            row["course"],
                            row["semester"],
                            row["mode"],
                            row["reference"],
                            f"{row['amount']:.2f}",
                            row["remarks"],
                            row["collected_by"]
                        ]
                    )


                writer.writerow(
                    []
                )


                writer.writerow(
                    [
                        "TOTAL COLLECTION",
                        f"{self.generated_total:.2f}"
                    ]
                )


            messagebox.showinfo(
                "Export Complete",
                (
                    "Your personal collection report "
                    "was exported successfully."
                    "\n\n"
                    f"{path}"
                ),
                parent=
                self.root_frame.winfo_toplevel()
            )


        except OSError as error:

            messagebox.showerror(
                "CSV Export Error",
                str(error),
                parent=
                self.root_frame.winfo_toplevel()
            )


    # ========================================================
    # PDF EXPORT
    # ========================================================

    def export_pdf(self):

        if not self.report_generated:

            messagebox.showwarning(
                "Generate Report First",
                (
                    "Please generate your report "
                    "before exporting it."
                ),
                parent=
                self.root_frame.winfo_toplevel()
            )

            return


        try:

            from reportlab.lib import colors

            from reportlab.lib.pagesizes import (
                A4,
                landscape
            )

            from reportlab.lib.styles import (
                getSampleStyleSheet,
                ParagraphStyle
            )

            from reportlab.lib.enums import (
                TA_CENTER
            )

            from reportlab.platypus import (
                SimpleDocTemplate,
                Table,
                TableStyle,
                Paragraph,
                Spacer,
                KeepTogether
            )


        except ImportError:

            messagebox.showerror(
                "PDF Library Required",
                (
                    "ReportLab is required for PDF export."
                    "\n\n"
                    "Install it with:"
                    "\n"
                    "python -m pip install reportlab"
                ),
                parent=
                self.root_frame.winfo_toplevel()
            )

            return


        default_name = (
            "my_collection_report_"
            f"{date.today().isoformat()}"
            ".pdf"
        )


        path = filedialog.asksaveasfilename(
            parent=
            self.root_frame.winfo_toplevel(),
            title=(
                "Export Personal Collection Report PDF"
            ),
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[
                (
                    "PDF File",
                    "*.pdf"
                )
            ]
        )


        if not path:

            return


        try:

            document = SimpleDocTemplate(
                path,
                pagesize=landscape(
                    A4
                ),
                rightMargin=28,
                leftMargin=28,
                topMargin=28,
                bottomMargin=28,
                title=(
                    "Accountant Collection Report"
                ),
                author=(
                    self.current_user_name
                    or
                    "Accountant"
                )
            )


            styles = getSampleStyleSheet()


            title_style = ParagraphStyle(
                "ReportMainTitle",
                parent=
                styles["Title"],
                fontName=
                "Helvetica-Bold",
                fontSize=17,
                leading=21,
                alignment=TA_CENTER,
                textColor=
                colors.HexColor(
                    "#101828"
                ),
                spaceAfter=3
            )


            subtitle_style = ParagraphStyle(
                "ReportSubtitle",
                parent=
                styles["Normal"],
                fontName=
                "Helvetica-Bold",
                fontSize=10,
                leading=14,
                alignment=TA_CENTER,
                textColor=
                colors.HexColor(
                    "#2563EB"
                ),
                spaceAfter=14
            )


            small_style = ParagraphStyle(
                "ReportSmall",
                parent=
                styles["Normal"],
                fontName=
                "Helvetica",
                fontSize=7,
                leading=9,
                textColor=
                colors.HexColor(
                    "#344054"
                )
            )


            small_bold_style = ParagraphStyle(
                "ReportSmallBold",
                parent=
                styles["Normal"],
                fontName=
                "Helvetica-Bold",
                fontSize=7,
                leading=9,
                textColor=
                colors.HexColor(
                    "#101828"
                )
            )


            story = []


            story.append(
                Paragraph(
                    (
                        "FEE STATUS MANAGEMENT SYSTEM"
                    ),
                    title_style
                )
            )


            story.append(
                Paragraph(
                    (
                        "ACCOUNTANT COLLECTION REPORT"
                    ),
                    subtitle_style
                )
            )


            info_data = [
                [
                    "ACCOUNTANT",
                    self.current_user_name,
                    "ACCOUNT ID",
                    self.current_user_id
                ],
                [
                    "REPORT PERIOD",
                    self.report_period_text(),
                    "PAYMENT MODE",
                    self.mode_var.get()
                ],
                [
                    "GENERATED ON",
                    self.generated_at.strftime(
                        "%d %B %Y, %I:%M %p"
                    ),
                    "GENERATED BY",
                    (
                        f"{self.current_user_name}"
                        " - "
                        f"{self.current_user_id}"
                    )
                ]
            ]


            info_table = Table(
                info_data,
                colWidths=[
                    85,
                    200,
                    85,
                    200
                ]
            )


            info_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            colors.HexColor(
                                "#EFF6FF"
                            )
                        ),
                        (
                            "BACKGROUND",
                            (2, 0),
                            (2, -1),
                            colors.HexColor(
                                "#EFF6FF"
                            )
                        ),
                        (
                            "FONTNAME",
                            (0, 0),
                            (0, -1),
                            "Helvetica-Bold"
                        ),
                        (
                            "FONTNAME",
                            (2, 0),
                            (2, -1),
                            "Helvetica-Bold"
                        ),
                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            8
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, -1),
                            colors.HexColor(
                                "#101828"
                            )
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.HexColor(
                                "#D9E2EC"
                            )
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE"
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            7
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            7
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            7
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            7
                        )
                    ]
                )
            )


            story.append(
                info_table
            )


            story.append(
                Spacer(
                    1,
                    14
                )
            )


            summary_data = [
                [
                    "TOTAL COLLECTION",
                    "TOTAL PAYMENTS",
                    "AVERAGE PAYMENT"
                ],
                [
                    pdf_money(
                        self.generated_total
                    ),
                    str(
                        self.generated_count
                    ),
                    pdf_money(
                        self.generated_average
                    )
                ]
            ]


            summary_table = Table(
                summary_data,
                colWidths=[
                    190,
                    190,
                    190
                ]
            )


            summary_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            colors.HexColor(
                                "#EFF6FF"
                            )
                        ),
                        (
                            "BACKGROUND",
                            (1, 0),
                            (1, -1),
                            colors.HexColor(
                                "#F0FDF4"
                            )
                        ),
                        (
                            "BACKGROUND",
                            (2, 0),
                            (2, -1),
                            colors.HexColor(
                                "#F5F3FF"
                            )
                        ),
                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, 0),
                            "Helvetica-Bold"
                        ),
                        (
                            "FONTNAME",
                            (0, 1),
                            (-1, 1),
                            "Helvetica-Bold"
                        ),
                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, 0),
                            7
                        ),
                        (
                            "FONTSIZE",
                            (0, 1),
                            (-1, 1),
                            12
                        ),
                        (
                            "ALIGN",
                            (0, 0),
                            (-1, -1),
                            "CENTER"
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE"
                        ),
                        (
                            "BOX",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.HexColor(
                                "#D9E2EC"
                            )
                        ),
                        (
                            "INNERGRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.HexColor(
                                "#D9E2EC"
                            )
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            8
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            8
                        )
                    ]
                )
            )


            story.append(
                summary_table
            )


            story.append(
                Spacer(
                    1,
                    16
                )
            )


            story.append(
                Paragraph(
                    "PAYMENT MODE SUMMARY",
                    small_bold_style
                )
            )


            story.append(
                Spacer(
                    1,
                    6
                )
            )


            mode_data = [
                [
                    "PAYMENT MODE",
                    "PAYMENTS",
                    "AMOUNT"
                ]
            ]


            for mode in sorted(
                self.generated_mode_summary
            ):

                data = (
                    self.generated_mode_summary[
                        mode
                    ]
                )


                mode_data.append(
                    [
                        mode,
                        str(
                            data["count"]
                        ),
                        pdf_money(
                            data["amount"]
                        )
                    ]
                )


            if len(
                mode_data
            ) == 1:

                mode_data.append(
                    [
                        "No Data",
                        "0",
                        "Rs. 0.00"
                    ]
                )


            mode_table = Table(
                mode_data,
                colWidths=[
                    190,
                    190,
                    190
                ],
                repeatRows=1
            )


            mode_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.HexColor(
                                "#EEF3F9"
                            )
                        ),
                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, 0),
                            "Helvetica-Bold"
                        ),
                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            8
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.HexColor(
                                "#D9E2EC"
                            )
                        ),
                        (
                            "ALIGN",
                            (1, 0),
                            (-1, -1),
                            "CENTER"
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE"
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            6
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            6
                        )
                    ]
                )
            )


            story.append(
                mode_table
            )


            story.append(
                Spacer(
                    1,
                    16
                )
            )


            story.append(
                Paragraph(
                    "TRANSACTION DETAILS",
                    small_bold_style
                )
            )


            story.append(
                Spacer(
                    1,
                    6
                )
            )


            transaction_data = [
                [
                    "ID",
                    "DATE",
                    "STUDENT",
                    "REG. NO.",
                    "COURSE",
                    "SEMESTER",
                    "MODE",
                    "REFERENCE",
                    "AMOUNT"
                ]
            ]


            for row in self.generated_rows:

                transaction_data.append(
                    [
                        str(
                            row["payment_id"]
                        ),
                        display_date(
                            row["payment_date"]
                        ),
                        Paragraph(
                            row["student"],
                            small_style
                        ),
                        row["reg_no"],
                        Paragraph(
                            row["course"],
                            small_style
                        ),
                        row["semester"],
                        row["mode"],
                        Paragraph(
                            row["reference"]
                            or
                            "—",
                            small_style
                        ),
                        pdf_money(
                            row["amount"]
                        )
                    ]
                )


            if not self.generated_rows:

                transaction_data.append(
                    [
                        "",
                        "",
                        Paragraph(
                            (
                                "No payment transactions "
                                "for this report."
                            ),
                            small_style
                        ),
                        "",
                        "",
                        "",
                        "",
                        "",
                        pdf_money(
                            0
                        )
                    ]
                )


            transaction_data.append(
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "TOTAL",
                    pdf_money(
                        self.generated_total
                    )
                ]
            )


            transaction_table = Table(
                transaction_data,
                repeatRows=1,
                colWidths=[
                    34,
                    67,
                    105,
                    70,
                    95,
                    65,
                    60,
                    90,
                    78
                ]
            )


            transaction_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.HexColor(
                                "#2563EB"
                            )
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, 0),
                            colors.white
                        ),
                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, 0),
                            "Helvetica-Bold"
                        ),
                        (
                            "FONTNAME",
                            (-2, -1),
                            (-1, -1),
                            "Helvetica-Bold"
                        ),
                        (
                            "BACKGROUND",
                            (-2, -1),
                            (-1, -1),
                            colors.HexColor(
                                "#EFF6FF"
                            )
                        ),
                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            6.5
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.4,
                            colors.HexColor(
                                "#D9E2EC"
                            )
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE"
                        ),
                        (
                            "ALIGN",
                            (0, 0),
                            (1, -1),
                            "CENTER"
                        ),
                        (
                            "ALIGN",
                            (3, 0),
                            (3, -1),
                            "CENTER"
                        ),
                        (
                            "ALIGN",
                            (5, 0),
                            (6, -1),
                            "CENTER"
                        ),
                        (
                            "ALIGN",
                            (-1, 1),
                            (-1, -1),
                            "RIGHT"
                        ),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -2),
                            [
                                colors.white,
                                colors.HexColor(
                                    "#F8FAFC"
                                )
                            ]
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            4
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            4
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            5
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            5
                        )
                    ]
                )
            )


            story.append(
                transaction_table
            )


            story.append(
                Spacer(
                    1,
                    14
                )
            )


            footer_data = [
                [
                    (
                        "Generated By: "
                        f"{self.current_user_name}"
                        " - "
                        f"{self.current_user_id}"
                    )
                ],
                [
                    (
                        "Generated On: "
                        f"{self.generated_at.strftime('%d %B %Y, %I:%M %p')}"
                    )
                ]
            ]


            footer_table = Table(
                footer_data,
                colWidths=[
                    570
                ]
            )


            footer_table.setStyle(
                TableStyle(
                    [
                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, -1),
                            "Helvetica"
                        ),
                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            7
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, -1),
                            colors.HexColor(
                                "#667085"
                            )
                        ),
                        (
                            "LINEABOVE",
                            (0, 0),
                            (-1, 0),
                            0.5,
                            colors.HexColor(
                                "#D9E2EC"
                            )
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, 0),
                            8
                        )
                    ]
                )
            )


            story.append(
                footer_table
            )


            document.build(
                story
            )


            messagebox.showinfo(
                "PDF Export Complete",
                (
                    "Your personal collection report "
                    "was exported successfully."
                    "\n\n"
                    f"{path}"
                ),
                parent=
                self.root_frame.winfo_toplevel()
            )


        except Exception as error:

            messagebox.showerror(
                "PDF Export Error",
                (
                    "Unable to export the PDF report."
                    "\n\n"
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
                parent=
                self.root_frame.winfo_toplevel()
            )


# ============================================================
# PUBLIC DASHBOARD FUNCTION
# ============================================================

def open_reports_page(
    parent,
    current_user_name="",
    current_user_id="",
    current_username="",
    user_role="Accountant",
    back_command=None
):
    """
    Open the Accountant personal report page inside the dashboard.

    Example:

        from reports_page import open_reports_page

        open_reports_page(
            parent=content,
            current_user_name=ACCOUNTANT_NAME,
            current_user_id=ACCOUNTANT_REGISTRATION_NO,
            current_username=ACCOUNTANT_USERNAME,
            user_role="Accountant",
            back_command=show_dashboard
        )
    """


    for child in (
        parent.winfo_children()
    ):

        child.destroy()


    return AccountantReportsPage(
        parent=parent,
        current_user_name=
        current_user_name,
        current_user_id=
        current_user_id,
        current_username=
        current_username,
        user_role=
        user_role,
        back_command=
        back_command
    )


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        (
            "Accountant Personal "
            "Collection Report"
        )
    )

    root.geometry(
        "1500x900"
    )

    root.configure(
        bg=PAGE_BG
    )


    open_reports_page(
        parent=root,
        current_user_name=
        "Vijay Nayak",
        current_user_id=
        "ACC0041",
        current_username=
        "vijay123",
        user_role=
        "Accountant",
        back_command=None
    )


    root.mainloop()
