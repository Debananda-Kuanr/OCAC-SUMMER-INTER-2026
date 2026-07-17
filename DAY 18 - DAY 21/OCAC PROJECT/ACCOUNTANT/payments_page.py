"""
payments_page.py
Accountant -> Payments / My Collections

Purpose:
- Show payment history collected by the currently logged-in accountant.
- Summary cards for today, this month, total collected, and today's transactions.
- Search by Payment ID, Student Name, Registration No., or Transaction Reference.
- Filter by date range and payment mode.
- View complete payment details.
- Show collection breakdown by payment mode.
- Open inside an existing Tkinter dashboard frame.

Required tables:
    fee_payments
    student_fees
    registration
    student_details
    fee_structures
    courses

Expected fee_payments columns:
    Payment_ID
    Student_Fee_ID
    Amount
    Payment_Mode
    Transaction_Reference
    Remarks
    Collected_By
    Payment_Date
    Created_At

IMPORTANT:
Update DB_CONFIG below if your MySQL username/password/database is different.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
import mysql.connector
from mysql.connector import Error


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "9439",
    "database": "OCAC_GROUP2"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# COLORS / UI
# ============================================================

BG = "#F4F7FB"
WHITE = "#FFFFFF"
TEXT = "#0F172A"
TEXT_2 = "#334155"
MUTED = "#64748B"
BORDER = "#DCE3EC"

BLUE = "#2563EB"
BLUE_HOVER = "#1D4ED8"
LIGHT_BLUE = "#EFF6FF"

GREEN = "#16A34A"
GREEN_HOVER = "#15803D"
LIGHT_GREEN = "#F0FDF4"

PURPLE = "#7C3AED"
LIGHT_PURPLE = "#F5F3FF"

ORANGE = "#F59E0B"
LIGHT_ORANGE = "#FFFBEB"

RED = "#DC2626"
LIGHT_RED = "#FEF2F2"

SLATE = "#475569"
SLATE_HOVER = "#334155"

FONT = "Segoe UI"


# ============================================================
# HELPERS
# ============================================================

def money(value):
    try:
        amount = Decimal(str(value or 0))
    except (InvalidOperation, ValueError, TypeError):
        amount = Decimal("0.00")
    return f"₹{amount:,.2f}"


def safe_text(value, fallback="-"):
    if value is None:
        return fallback
    value = str(value).strip()
    return value if value else fallback


def format_date(value):
    if value is None:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%d %b %Y")
    if isinstance(value, date):
        return value.strftime("%d %b %Y")
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").strftime("%d %b %Y")
    except Exception:
        return str(value)


def format_datetime(value):
    if value is None:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%d %b %Y, %I:%M %p")
    return str(value)


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# ============================================================
# MAIN PAYMENTS PAGE
# ============================================================

class PaymentsPage:
    def __init__(
        self,
        parent,
        current_user_name="",
        current_user_id="",
        current_username="",
        user_role="Accountant",
        back_command=None
    ):
        self.parent = parent
        self.current_user_name = str(current_user_name or "").strip()
        self.current_user_id = str(current_user_id or "").strip()
        self.current_username = str(current_username or "").strip()
        self.user_role = str(user_role or "Accountant").strip()
        self.back_command = back_command

        self.page = tk.Frame(parent, bg=BG)

        # Fill dashboard content area.
        self.page.pack(fill="both", expand=True)

        self.search_var = tk.StringVar()
        self.date_filter_var = tk.StringVar(value="Today")
        self.payment_mode_var = tk.StringVar(value="All Modes")
        self.custom_from_var = tk.StringVar()
        self.custom_to_var = tk.StringVar()

        self.summary_today_var = tk.StringVar(value="₹0.00")
        self.summary_month_var = tk.StringVar(value="₹0.00")
        self.summary_total_var = tk.StringVar(value="₹0.00")
        self.summary_today_count_var = tk.StringVar(value="0")

        self.result_count_var = tk.StringVar(value="0 Payments")
        self.status_var = tk.StringVar(value="Ready")

        self.payment_rows = {}
        self.breakdown_labels = {}

        self.setup_styles()
        self.show_payments_page()


    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------

    def setup_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Payments.Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT_2,
            rowheight=40,
            borderwidth=0,
            font=(FONT, 9)
        )

        style.configure(
            "Payments.Treeview.Heading",
            background="#F8FAFC",
            foreground=MUTED,
            relief="flat",
            font=(FONT, 8, "bold"),
            padding=(8, 10)
        )

        style.map(
            "Payments.Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", TEXT)]
        )

        style.configure(
            "Payments.TCombobox",
            padding=7,
            font=(FONT, 9)
        )


    # --------------------------------------------------------
    # GENERIC UI HELPERS
    # --------------------------------------------------------

    def button(self, parent, text, command, kind="primary", width=16):
        palettes = {
            "primary": (BLUE, WHITE, BLUE_HOVER),
            "success": (GREEN, WHITE, GREEN_HOVER),
            "danger": (RED, WHITE, "#B91C1C"),
            "warning": (ORANGE, WHITE, "#D97706"),
            "secondary": (SLATE, WHITE, SLATE_HOVER),
        }

        bg, fg, active_bg = palettes.get(kind, palettes["primary"])

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=WHITE,
            disabledforeground="#CBD5E1",
            bd=0,
            relief="flat",
            cursor="hand2",
            width=width,
            pady=9,
            font=(FONT, 9, "bold")
        )


    def card(self, parent):
        return tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )


    def summary_card(self, parent, title, variable, accent, soft_bg):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        strip = tk.Frame(card, bg=accent, width=5)
        strip.pack(side="left", fill="y")

        content = tk.Frame(card, bg=WHITE)
        content.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        tk.Label(
            content,
            text=title,
            bg=WHITE,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(anchor="w")

        tk.Label(
            content,
            textvariable=variable,
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 18, "bold")
        ).pack(anchor="w", pady=(5, 0))

        return card


    # --------------------------------------------------------
    # MAIN PAGE
    # --------------------------------------------------------

    def show_payments_page(self):
        clear_frame(self.page)

        self.build_header()
        self.build_summary_cards()
        self.build_filter_card()
        self.build_main_content()
        self.build_status_bar()

        self.load_all_data()


    def build_header(self):
        header = tk.Frame(self.page, bg=WHITE, height=92)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=WHITE)
        left.pack(side="left", fill="y", padx=28)

        if self.back_command:
            tk.Button(
                left,
                text="← BACK",
                command=self.back_command,
                bg=WHITE,
                fg=BLUE,
                activebackground=WHITE,
                activeforeground=BLUE_HOVER,
                bd=0,
                cursor="hand2",
                font=(FONT, 9, "bold")
            ).pack(anchor="w", pady=(12, 2))

        tk.Label(
            left,
            text="Payments",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 20, "bold")
        ).pack(anchor="w", pady=(14 if not self.back_command else 2, 1))

        tk.Label(
            left,
            text="My collection history and payment transactions.",
            bg=WHITE,
            fg=MUTED,
            font=(FONT, 9)
        ).pack(anchor="w")

        right = tk.Frame(header, bg=WHITE)
        right.pack(side="right", padx=28)

        tk.Label(
            right,
            text="COLLECTION ACCOUNT",
            bg=WHITE,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(anchor="e")

        identity = self.current_user_name or "Current User"
        if self.current_user_id:
            identity += f"  •  {self.current_user_id}"

        tk.Label(
            right,
            text=identity,
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(anchor="e", pady=(3, 0))


    def build_summary_cards(self):
        area = tk.Frame(self.page, bg=BG)
        area.pack(fill="x", padx=28, pady=(18, 10))

        for column in range(4):
            area.grid_columnconfigure(column, weight=1)

        cards = [
            ("TODAY'S COLLECTION", self.summary_today_var, BLUE, LIGHT_BLUE),
            ("THIS MONTH", self.summary_month_var, GREEN, LIGHT_GREEN),
            ("TOTAL COLLECTED", self.summary_total_var, PURPLE, LIGHT_PURPLE),
            ("TODAY'S PAYMENTS", self.summary_today_count_var, ORANGE, LIGHT_ORANGE),
        ]

        for index, (title, variable, accent, soft_bg) in enumerate(cards):
            card = self.summary_card(area, title, variable, accent, soft_bg)
            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=(0 if index == 0 else 6, 0 if index == 3 else 6)
            )


    def build_filter_card(self):
        card = self.card(self.page)
        card.pack(fill="x", padx=28, pady=(0, 10))

        top = tk.Frame(card, bg=WHITE)
        top.pack(fill="x", padx=18, pady=(14, 8))

        tk.Label(
            top,
            text="PAYMENT HISTORY FILTERS",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(side="left")

        self.button(
            top,
            "REFRESH",
            self.load_all_data,
            "success",
            12
        ).pack(side="right")

        filters = tk.Frame(card, bg=WHITE)
        filters.pack(fill="x", padx=18, pady=(0, 14))

        filters.grid_columnconfigure(0, weight=3)
        filters.grid_columnconfigure(1, weight=1)
        filters.grid_columnconfigure(2, weight=1)

        # Search
        search_box = tk.Frame(filters, bg=WHITE)
        search_box.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        tk.Label(
            search_box,
            text="SEARCH",
            bg=WHITE,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.search_entry = tk.Entry(
            search_box,
            textvariable=self.search_var,
            bg="#F8FAFC",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightbackground=BORDER,
            highlightcolor=BLUE,
            highlightthickness=1,
            font=(FONT, 10)
        )
        self.search_entry.pack(fill="x", ipady=8)
        self.search_entry.bind("<Return>", lambda event: self.load_payment_history())

        # Date filter
        date_box = tk.Frame(filters, bg=WHITE)
        date_box.grid(row=0, column=1, sticky="ew", padx=8)

        tk.Label(
            date_box,
            text="DATE RANGE",
            bg=WHITE,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.date_combo = ttk.Combobox(
            date_box,
            textvariable=self.date_filter_var,
            values=[
                "Today",
                "Yesterday",
                "Last 7 Days",
                "This Month",
                "All Time",
                "Custom Range"
            ],
            state="readonly",
            style="Payments.TCombobox"
        )
        self.date_combo.pack(fill="x")
        self.date_combo.bind("<<ComboboxSelected>>", self.on_date_filter_changed)

        # Mode filter
        mode_box = tk.Frame(filters, bg=WHITE)
        mode_box.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        tk.Label(
            mode_box,
            text="PAYMENT MODE",
            bg=WHITE,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.mode_combo = ttk.Combobox(
            mode_box,
            textvariable=self.payment_mode_var,
            values=[
                "All Modes",
                "Cash",
                "UPI",
                "Card",
                "Bank Transfer",
                "Cheque"
            ],
            state="readonly",
            style="Payments.TCombobox"
        )
        self.mode_combo.pack(fill="x")
        self.mode_combo.bind("<<ComboboxSelected>>", lambda event: self.load_payment_history())

        # Custom date row
        self.custom_date_frame = tk.Frame(card, bg="#F8FAFC")

        custom_inner = tk.Frame(self.custom_date_frame, bg="#F8FAFC")
        custom_inner.pack(fill="x", padx=18, pady=10)

        tk.Label(
            custom_inner,
            text="FROM (YYYY-MM-DD)",
            bg="#F8FAFC",
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(side="left")

        tk.Entry(
            custom_inner,
            textvariable=self.custom_from_var,
            width=14,
            font=(FONT, 9)
        ).pack(side="left", padx=(8, 18), ipady=5)

        tk.Label(
            custom_inner,
            text="TO (YYYY-MM-DD)",
            bg="#F8FAFC",
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(side="left")

        tk.Entry(
            custom_inner,
            textvariable=self.custom_to_var,
            width=14,
            font=(FONT, 9)
        ).pack(side="left", padx=(8, 18), ipady=5)

        self.button(
            custom_inner,
            "APPLY",
            self.load_payment_history,
            "primary",
            10
        ).pack(side="left")

        actions = tk.Frame(card, bg=WHITE)
        actions.pack(fill="x", padx=18, pady=(0, 14))

        tk.Label(
            actions,
            text="Search by Payment ID, Student Name, Registration No. or Transaction Reference.",
            bg=WHITE,
            fg=MUTED,
            font=(FONT, 8)
        ).pack(side="left")

        self.button(
            actions,
            "RESET",
            self.reset_filters,
            "secondary",
            10
        ).pack(side="right", padx=(8, 0))

        self.button(
            actions,
            "SEARCH",
            self.load_payment_history,
            "primary",
            12
        ).pack(side="right")


    def build_main_content(self):
        main = tk.Frame(self.page, bg=BG)
        main.pack(fill="both", expand=True, padx=28, pady=(0, 10))

        main.grid_columnconfigure(0, weight=4)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Payment table
        table_card = self.card(main)
        table_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        table_head = tk.Frame(table_card, bg=WHITE)
        table_head.pack(fill="x", padx=18, pady=(14, 10))

        tk.Label(
            table_head,
            text="MY COLLECTIONS",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 11, "bold")
        ).pack(side="left")

        tk.Label(
            table_head,
            textvariable=self.result_count_var,
            bg=LIGHT_BLUE,
            fg=BLUE,
            padx=11,
            pady=5,
            font=(FONT, 8, "bold")
        ).pack(side="right", padx=(8, 0))

        self.button(
            table_head,
            "VIEW DETAILS",
            self.open_selected_payment,
            "primary",
            14
        ).pack(side="right")

        holder = tk.Frame(table_card, bg=WHITE)
        holder.pack(fill="both", expand=True, padx=18, pady=(0, 16))

        columns = (
            "payment_id",
            "date_time",
            "student",
            "registration",
            "semester",
            "mode",
            "amount"
        )

        self.payment_tree = ttk.Treeview(
            holder,
            columns=columns,
            show="headings",
            style="Payments.Treeview",
            selectmode="browse"
        )

        headings = {
            "payment_id": "PAYMENT ID",
            "date_time": "DATE & TIME",
            "student": "STUDENT",
            "registration": "REG. NO.",
            "semester": "SEMESTER",
            "mode": "MODE",
            "amount": "AMOUNT"
        }

        widths = {
            "payment_id": 95,
            "date_time": 155,
            "student": 190,
            "registration": 120,
            "semester": 100,
            "mode": 115,
            "amount": 120
        }

        for column in columns:
            self.payment_tree.heading(column, text=headings[column])
            self.payment_tree.column(
                column,
                width=widths[column],
                minwidth=80,
                anchor="w" if column in ("student", "registration", "date_time") else "center"
            )

        y_scroll = ttk.Scrollbar(
            holder,
            orient="vertical",
            command=self.payment_tree.yview
        )
        x_scroll = ttk.Scrollbar(
            holder,
            orient="horizontal",
            command=self.payment_tree.xview
        )

        self.payment_tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        self.payment_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        holder.grid_rowconfigure(0, weight=1)
        holder.grid_columnconfigure(0, weight=1)

        self.payment_tree.bind("<Double-1>", lambda event: self.open_selected_payment())

        # Breakdown
        breakdown = self.card(main)
        breakdown.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        tk.Label(
            breakdown,
            text="COLLECTION BREAKDOWN",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 11, "bold")
        ).pack(anchor="w", padx=18, pady=(16, 3))

        tk.Label(
            breakdown,
            text="For the current filters",
            bg=WHITE,
            fg=MUTED,
            font=(FONT, 8)
        ).pack(anchor="w", padx=18, pady=(0, 14))

        for mode in ["Cash", "UPI", "Card", "Bank Transfer", "Cheque", "Other"]:
            row = tk.Frame(breakdown, bg=WHITE)
            row.pack(fill="x", padx=18, pady=5)

            tk.Label(
                row,
                text=mode,
                bg=WHITE,
                fg=TEXT_2,
                font=(FONT, 9)
            ).pack(side="left")

            variable = tk.StringVar(value="₹0.00")
            self.breakdown_labels[mode] = variable

            tk.Label(
                row,
                textvariable=variable,
                bg=WHITE,
                fg=TEXT,
                font=(FONT, 9, "bold")
            ).pack(side="right")

        tk.Frame(breakdown, bg=BORDER, height=1).pack(fill="x", padx=18, pady=12)

        total_row = tk.Frame(breakdown, bg=LIGHT_BLUE)
        total_row.pack(fill="x", padx=18)

        tk.Label(
            total_row,
            text="FILTERED TOTAL",
            bg=LIGHT_BLUE,
            fg=BLUE,
            font=(FONT, 9, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 2))

        self.filtered_total_var = tk.StringVar(value="₹0.00")

        tk.Label(
            total_row,
            textvariable=self.filtered_total_var,
            bg=LIGHT_BLUE,
            fg=TEXT,
            font=(FONT, 16, "bold")
        ).pack(anchor="w", padx=12, pady=(0, 10))

        tk.Label(
            breakdown,
            text=(
                "Only payment transactions collected by the currently "
                "logged-in accountant are shown."
            ),
            bg=WHITE,
            fg=MUTED,
            wraplength=220,
            justify="left",
            font=(FONT, 8)
        ).pack(anchor="w", padx=18, pady=18)


    def build_status_bar(self):
        bar = tk.Frame(self.page, bg=WHITE, height=30)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        tk.Label(
            bar,
            textvariable=self.status_var,
            bg=WHITE,
            fg=MUTED,
            font=(FONT, 8)
        ).pack(side="left", padx=28)


    # --------------------------------------------------------
    # ACCOUNTANT FILTER
    # --------------------------------------------------------

    def collector_filter_sql(self, alias="fp"):
        """
        Return a SQL condition that shows only the current accountant's payments.

        The database currently stores collector values in mixed formats such as:
            Vijay Nayak - ACC041
            Debananda Kuanr - ACC085
            Administrator
            Accountant

        The dashboard may provide Vijay's ID as ACC0041, so exact ID matching
        alone cannot find rows stored as "Vijay Nayak - ACC041".

        We therefore match the current accountant by:
            - exact Registration_No
            - exact Name
            - exact Username
            - "<current accountant name> - ..." combined format
        """
        conditions = []
        params = []

        if self.current_user_id:
            conditions.append(
                f"LOWER(TRIM({alias}.Collected_By)) = LOWER(TRIM(%s))"
            )
            params.append(self.current_user_id)

        if self.current_user_name:
            conditions.append(
                f"LOWER(TRIM({alias}.Collected_By)) = LOWER(TRIM(%s))"
            )
            params.append(self.current_user_name)

            conditions.append(
                f"LOWER(TRIM({alias}.Collected_By)) LIKE LOWER(%s)"
            )
            params.append(f"{self.current_user_name} - %")

        if self.current_username:
            conditions.append(
                f"LOWER(TRIM({alias}.Collected_By)) = LOWER(TRIM(%s))"
            )
            params.append(self.current_username)

        if not conditions:
            return "1 = 0", []

        return "(" + " OR ".join(conditions) + ")", params
    def on_date_filter_changed(self, event=None):
        if self.date_filter_var.get() == "Custom Range":
            self.custom_date_frame.pack(fill="x", before=self.custom_date_frame.master.winfo_children()[-1])
        else:
            self.custom_date_frame.pack_forget()
            self.load_payment_history()


    def get_date_conditions(self, alias="fp"):
        selected = self.date_filter_var.get()
        today = date.today()

        if selected == "Today":
            return f"{alias}.Payment_Date = %s", [today]

        if selected == "Yesterday":
            return f"{alias}.Payment_Date = %s", [today - timedelta(days=1)]

        if selected == "Last 7 Days":
            start = today - timedelta(days=6)
            return f"{alias}.Payment_Date BETWEEN %s AND %s", [start, today]

        if selected == "This Month":
            start = today.replace(day=1)
            if today.month == 12:
                next_month = date(today.year + 1, 1, 1)
            else:
                next_month = date(today.year, today.month + 1, 1)
            return (
                f"{alias}.Payment_Date >= %s AND {alias}.Payment_Date < %s",
                [start, next_month]
            )

        if selected == "Custom Range":
            from_text = self.custom_from_var.get().strip()
            to_text = self.custom_to_var.get().strip()

            try:
                from_date = datetime.strptime(from_text, "%Y-%m-%d").date()
                to_date = datetime.strptime(to_text, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Custom dates must use YYYY-MM-DD format.")

            if from_date > to_date:
                raise ValueError("From date cannot be after To date.")

            return (
                f"{alias}.Payment_Date BETWEEN %s AND %s",
                [from_date, to_date]
            )

        return "1 = 1", []


    # --------------------------------------------------------
    # DATA LOAD
    # --------------------------------------------------------

    def load_all_data(self):
        self.load_summary()
        self.load_payment_history()


    def load_summary(self):
        connection = None
        cursor = None

        try:
            collector_sql, collector_params = self.collector_filter_sql("fp")

            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            today = date.today()
            month_start = today.replace(day=1)

            query = f"""
                SELECT
                    COALESCE(SUM(
                        CASE
                            WHEN fp.Payment_Date = %s
                            THEN fp.Amount
                            ELSE 0
                        END
                    ), 0) AS Today_Collection,

                    COALESCE(SUM(
                        CASE
                            WHEN fp.Payment_Date >= %s
                            THEN fp.Amount
                            ELSE 0
                        END
                    ), 0) AS Month_Collection,

                    COALESCE(SUM(fp.Amount), 0) AS Total_Collection,

                    COALESCE(SUM(
                        CASE
                            WHEN fp.Payment_Date = %s
                            THEN 1
                            ELSE 0
                        END
                    ), 0) AS Today_Count

                FROM fee_payments AS fp
                WHERE {collector_sql}
            """

            params = [today, month_start, today] + collector_params
            cursor.execute(query, params)
            row = cursor.fetchone() or {}

            self.summary_today_var.set(money(row.get("Today_Collection")))
            self.summary_month_var.set(money(row.get("Month_Collection")))
            self.summary_total_var.set(money(row.get("Total_Collection")))
            self.summary_today_count_var.set(str(int(row.get("Today_Count") or 0)))

        except Error as error:
            self.status_var.set(f"Summary load failed: {error}")
            messagebox.showerror(
                "Payment Summary Error",
                str(error),
                parent=self.parent.winfo_toplevel()
            )

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()


    def load_payment_history(self):
        connection = None
        cursor = None

        try:
            date_sql, date_params = self.get_date_conditions("fp")
            collector_sql, collector_params = self.collector_filter_sql("fp")

            conditions = [collector_sql, date_sql]
            params = collector_params + date_params

            mode = self.payment_mode_var.get().strip()
            if mode and mode != "All Modes":
                conditions.append("LOWER(TRIM(fp.Payment_Mode)) = LOWER(TRIM(%s))")
                params.append(mode)

            search = self.search_var.get().strip()
            if search:
                like = f"%{search}%"
                conditions.append(
                    """
                    (
                        CAST(fp.Payment_ID AS CHAR) LIKE %s
                        OR r.Name LIKE %s
                        OR sf.Registration_No LIKE %s
                        OR COALESCE(fp.Transaction_Reference, '') LIKE %s
                    )
                    """
                )
                params.extend([like, like, like, like])

            where_sql = " AND ".join(f"({condition})" for condition in conditions)

            query = f"""
                SELECT
                    fp.Payment_ID,
                    fp.Student_Fee_ID,
                    fp.Amount,
                    fp.Payment_Mode,
                    fp.Transaction_Reference,
                    fp.Remarks,
                    fp.Collected_By,
                    fp.Payment_Date,
                    fp.Created_At,

                    sf.Registration_No,
                    sf.Total_Fee,
                    sf.Amount_Paid,
                    sf.Due_Amount,
                    sf.Payment_Status,

                    r.Name AS Student_Name,

                    sd.Course AS Student_Course,
                    sd.Semester AS Current_Semester,
                    sd.Admission_Year,

                    fs.Semester AS Fee_Semester,
                    fs.Academic_Year,
                    fs.Course_ID,

                    c.Course_Name

                FROM fee_payments AS fp

                INNER JOIN student_fees AS sf
                    ON sf.Student_Fee_ID = fp.Student_Fee_ID

                INNER JOIN registration AS r
                    ON r.Registration_No = sf.Registration_No

                LEFT JOIN student_details AS sd
                    ON sd.Registration_No = sf.Registration_No

                LEFT JOIN fee_structures AS fs
                    ON fs.Fee_Structure_ID = sf.Fee_Structure_ID

                LEFT JOIN courses AS c
                    ON c.Course_ID = fs.Course_ID

                WHERE {where_sql}

                ORDER BY
                    fp.Payment_Date DESC,
                    fp.Created_At DESC,
                    fp.Payment_ID DESC
            """

            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

            for item in self.payment_tree.get_children():
                self.payment_tree.delete(item)

            self.payment_rows = {}

            breakdown = {
                "Cash": Decimal("0.00"),
                "UPI": Decimal("0.00"),
                "Card": Decimal("0.00"),
                "Bank Transfer": Decimal("0.00"),
                "Cheque": Decimal("0.00"),
                "Other": Decimal("0.00")
            }

            filtered_total = Decimal("0.00")

            for row in rows:
                payment_id = int(row["Payment_ID"])
                amount = Decimal(str(row["Amount"] or 0))
                filtered_total += amount

                raw_mode = safe_text(row.get("Payment_Mode"), "Other")
                normalized_mode = self.normalize_payment_mode(raw_mode)

                if normalized_mode in breakdown:
                    breakdown[normalized_mode] += amount
                else:
                    breakdown["Other"] += amount

                fee_semester = row.get("Fee_Semester")
                semester_text = (
                    f"Semester {fee_semester}"
                    if fee_semester is not None
                    else "-"
                )

                self.payment_tree.insert(
                    "",
                    "end",
                    iid=str(payment_id),
                    values=(
                        f"PAY{payment_id:05d}",
                        format_datetime(row.get("Created_At")),
                        safe_text(row.get("Student_Name")),
                        safe_text(row.get("Registration_No")),
                        semester_text,
                        raw_mode,
                        money(amount)
                    )
                )

                self.payment_rows[payment_id] = row

            count = len(rows)
            self.result_count_var.set(
                f"{count} Payment" if count == 1 else f"{count} Payments"
            )

            for mode_name, variable in self.breakdown_labels.items():
                variable.set(money(breakdown.get(mode_name, 0)))

            self.filtered_total_var.set(money(filtered_total))
            self.status_var.set(
                f"Loaded {count} payment transaction(s) for "
                f"{self.current_user_name or self.current_user_id or 'current accountant'}."
            )

        except ValueError as error:
            messagebox.showwarning(
                "Invalid Filter",
                str(error),
                parent=self.parent.winfo_toplevel()
            )

        except Error as error:
            self.status_var.set(f"Payment history load failed: {error}")
            messagebox.showerror(
                "Payment History Error",
                str(error),
                parent=self.parent.winfo_toplevel()
            )

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()


    def normalize_payment_mode(self, mode):
        value = str(mode or "").strip().lower()

        mapping = {
            "cash": "Cash",
            "upi": "UPI",
            "card": "Card",
            "credit card": "Card",
            "debit card": "Card",
            "bank transfer": "Bank Transfer",
            "bank": "Bank Transfer",
            "neft": "Bank Transfer",
            "rtgs": "Bank Transfer",
            "imps": "Bank Transfer",
            "cheque": "Cheque",
            "check": "Cheque"
        }

        return mapping.get(value, "Other")


    def reset_filters(self):
        self.search_var.set("")
        self.date_filter_var.set("Today")
        self.payment_mode_var.set("All Modes")
        self.custom_from_var.set("")
        self.custom_to_var.set("")
        self.custom_date_frame.pack_forget()
        self.load_payment_history()


    # --------------------------------------------------------
    # PAYMENT DETAILS
    # --------------------------------------------------------

    def open_selected_payment(self):
        selected = self.payment_tree.selection()

        if not selected:
            focused = self.payment_tree.focus()
            if focused:
                selected = (focused,)

        if not selected:
            messagebox.showwarning(
                "Select Payment",
                "Please select one payment transaction first.",
                parent=self.parent.winfo_toplevel()
            )
            return

        try:
            payment_id = int(selected[0])
        except ValueError:
            return

        payment = self.payment_rows.get(payment_id)

        if not payment:
            messagebox.showerror(
                "Payment Error",
                "The selected payment data is not available. Please refresh the page.",
                parent=self.parent.winfo_toplevel()
            )
            return

        self.show_payment_details(payment)


    def show_payment_details(self, payment):
        clear_frame(self.page)

        # Header
        header = tk.Frame(self.page, bg=WHITE, height=88)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=WHITE)
        left.pack(side="left", padx=28, pady=14)

        tk.Button(
            left,
            text="← BACK TO PAYMENTS",
            command=self.show_payments_page,
            bg=WHITE,
            fg=BLUE,
            activebackground=WHITE,
            activeforeground=BLUE_HOVER,
            bd=0,
            cursor="hand2",
            font=(FONT, 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Payment Details",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 19, "bold")
        ).pack(anchor="w", pady=(5, 0))

        payment_id = int(payment["Payment_ID"])

        badge = tk.Label(
            header,
            text=f"PAYMENT #PAY{payment_id:05d}",
            bg=LIGHT_GREEN,
            fg=GREEN,
            padx=14,
            pady=8,
            font=(FONT, 9, "bold")
        )
        badge.pack(side="right", padx=28)

        body = tk.Frame(self.page, bg=BG)
        body.pack(fill="both", expand=True, padx=28, pady=20)

        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=1)

        # Main details card
        details = self.card(body)
        details.grid(row=0, column=0, sticky="nsew", padx=(0, 7))

        top = tk.Frame(details, bg=LIGHT_GREEN)
        top.pack(fill="x")

        tk.Label(
            top,
            text="PAYMENT RECORDED",
            bg=LIGHT_GREEN,
            fg=GREEN,
            font=(FONT, 12, "bold")
        ).pack(anchor="w", padx=20, pady=(16, 3))

        tk.Label(
            top,
            text=f"Amount received: {money(payment.get('Amount'))}",
            bg=LIGHT_GREEN,
            fg=TEXT,
            font=(FONT, 18, "bold")
        ).pack(anchor="w", padx=20, pady=(0, 16))

        info = tk.Frame(details, bg=WHITE)
        info.pack(fill="both", expand=True, padx=20, pady=18)

        rows = [
            ("Student", safe_text(payment.get("Student_Name"))),
            ("Registration No.", safe_text(payment.get("Registration_No"))),
            (
                "Course",
                safe_text(
                    payment.get("Course_Name")
                    or payment.get("Student_Course")
                )
            ),
            (
                "Fee Semester",
                f"Semester {payment.get('Fee_Semester')}"
                if payment.get("Fee_Semester") is not None
                else "-"
            ),
            ("Academic Year", safe_text(payment.get("Academic_Year"))),
            ("Payment Amount", money(payment.get("Amount"))),
            ("Payment Mode", safe_text(payment.get("Payment_Mode"))),
            (
                "Transaction Reference",
                safe_text(payment.get("Transaction_Reference"))
            ),
            ("Payment Date", format_date(payment.get("Payment_Date"))),
            ("Recorded At", format_datetime(payment.get("Created_At"))),
            ("Collected By", safe_text(payment.get("Collected_By"))),
            ("Remarks", safe_text(payment.get("Remarks"))),
        ]

        for label_text, value_text in rows:
            row = tk.Frame(info, bg=WHITE)
            row.pack(fill="x", pady=5)

            tk.Label(
                row,
                text=label_text,
                bg=WHITE,
                fg=MUTED,
                width=23,
                anchor="w",
                font=(FONT, 9, "bold")
            ).pack(side="left")

            tk.Label(
                row,
                text=value_text,
                bg=WHITE,
                fg=TEXT,
                anchor="w",
                justify="left",
                wraplength=520,
                font=(FONT, 9)
            ).pack(side="left", fill="x", expand=True)

        # Fee status side card
        side = self.card(body)
        side.grid(row=0, column=1, sticky="nsew", padx=(7, 0))

        tk.Label(
            side,
            text="FEE ACCOUNT AFTER PAYMENT",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(anchor="w", padx=18, pady=(18, 14))

        fee_values = [
            ("Total Fee", money(payment.get("Total_Fee"))),
            ("Total Paid", money(payment.get("Amount_Paid"))),
            ("Remaining Due", money(payment.get("Due_Amount"))),
            ("Current Status", safe_text(payment.get("Payment_Status"))),
        ]

        for title, value in fee_values:
            box = tk.Frame(side, bg="#F8FAFC")
            box.pack(fill="x", padx=18, pady=5)

            tk.Label(
                box,
                text=title,
                bg="#F8FAFC",
                fg=MUTED,
                font=(FONT, 8, "bold")
            ).pack(anchor="w", padx=12, pady=(9, 2))

            tk.Label(
                box,
                text=value,
                bg="#F8FAFC",
                fg=TEXT,
                font=(FONT, 13, "bold")
            ).pack(anchor="w", padx=12, pady=(0, 9))

        actions = tk.Frame(side, bg=WHITE)
        actions.pack(fill="x", padx=18, pady=18)

        self.button(
            actions,
            "COPY RECEIPT TEXT",
            lambda: self.copy_receipt_text(payment),
            "primary",
            20
        ).pack(fill="x", pady=(0, 8))

        self.button(
            actions,
            "BACK TO PAYMENTS",
            self.show_payments_page,
            "secondary",
            20
        ).pack(fill="x")


    # --------------------------------------------------------
    # RECEIPT TEXT
    # --------------------------------------------------------

    def build_receipt_text(self, payment):
        payment_id = int(payment["Payment_ID"])

        return (
            "PAYMENT RECEIPT\n"
            "========================================\n"
            f"Payment ID       : PAY{payment_id:05d}\n"
            f"Student          : {safe_text(payment.get('Student_Name'))}\n"
            f"Registration No. : {safe_text(payment.get('Registration_No'))}\n"
            f"Course           : {safe_text(payment.get('Course_Name') or payment.get('Student_Course'))}\n"
            f"Semester         : {('Semester ' + str(payment.get('Fee_Semester'))) if payment.get('Fee_Semester') is not None else '-'}\n"
            f"Academic Year    : {safe_text(payment.get('Academic_Year'))}\n"
            "----------------------------------------\n"
            f"Amount Paid      : {money(payment.get('Amount'))}\n"
            f"Payment Mode     : {safe_text(payment.get('Payment_Mode'))}\n"
            f"Reference        : {safe_text(payment.get('Transaction_Reference'))}\n"
            f"Payment Date     : {format_date(payment.get('Payment_Date'))}\n"
            f"Collected By     : {safe_text(payment.get('Collected_By'))}\n"
            f"Remarks          : {safe_text(payment.get('Remarks'))}\n"
            "========================================\n"
        )


    def copy_receipt_text(self, payment):
        receipt = self.build_receipt_text(payment)

        root = self.parent.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(receipt)

        messagebox.showinfo(
            "Receipt Copied",
            "The payment receipt text has been copied to the clipboard.",
            parent=root
        )


# ============================================================
# DASHBOARD INTEGRATION FUNCTION
# ============================================================

def open_payments_page(
    parent,
    current_user_name="",
    current_user_id="",
    current_username="",
    user_role="Accountant",
    back_command=None
):
    """
    Open the Payments / My Collections page inside an existing dashboard frame.

    Example:

        open_payments_page(
            parent=content_frame,
            current_user_name=current_user_name,
            current_user_id=current_user_id,
            user_role=user_role
        )

    If your dashboard reuses one content frame, clear it before calling this
    function, or let this function clear it automatically as below.
    """

    for widget in parent.winfo_children():
        widget.destroy()

    return PaymentsPage(
        parent=parent,
        current_user_name=current_user_name,
        current_user_id=current_user_id,
        current_username=current_username,
        user_role=user_role,
        back_command=back_command
    )


# ============================================================
# OPTIONAL STANDALONE TEST
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Payments - My Collections")
    root.geometry("1450x850")
    root.minsize(1100, 700)
    root.configure(bg=BG)

    # Change these test values to an accountant that actually appears
    # in fee_payments.Collected_By.
    #
    # The page supports matching either:
    #   current_user_id   e.g. ACC0001
    #   current_user_name e.g. Debananda Kuanr
    #
    # If your old rows contain "Administrator", use that value while testing.
    open_payments_page(
        parent=root,
        current_user_name="Administrator",
        current_user_id="",
        current_username="",
        user_role="Accountant"
    )

    root.mainloop()
