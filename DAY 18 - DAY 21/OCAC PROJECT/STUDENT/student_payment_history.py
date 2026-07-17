from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
import os
import tempfile
import mysql.connector


# ============================================================
# DATABASE CONFIGURATION
# Updated from student_dashboard.py at runtime.
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ocac_group2"
}


# ============================================================
# DEFAULT COLORS
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
    "BORDER": "#DCE3EC",
    "SOFT_BLUE": "#EFF6FF",
    "SOFT_GREEN": "#F0FDF4",
    "SOFT_RED": "#FEF2F2",
    "SOFT_AMBER": "#FFFBEB",
    "SIDEBAR": "#0F172A",
    "SIDEBAR_HOVER": "#1E293B"
}


# ============================================================
# DATABASE HELPERS
# ============================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(query, params=()):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchall()
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))
        return []
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def fetch_one(query, params=()):
    rows = fetch_all(query, params)
    return rows[0] if rows else None


# ============================================================
# FORMAT HELPERS
# ============================================================

def money(value):
    try:
        amount = Decimal(str(value or 0))
    except (InvalidOperation, TypeError, ValueError):
        amount = Decimal("0.00")
    return f"Rs. {amount:,.2f}"


def safe_text(value, fallback="-"):
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


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


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def normalize_text(value):
    return str(value or "").strip().lower()


# ============================================================
# MAIN PAYMENT HISTORY PAGE
# ============================================================

class StudentPaymentHistoryPage:
    def __init__(
        self,
        parent,
        registration_no,
        student_name="Student",
        colors=None,
        on_dashboard=None
    ):
        self.parent = parent
        self.registration_no = str(registration_no or "").strip()
        self.student_name = str(student_name or "Student").strip() or "Student"
        self.on_dashboard = on_dashboard

        palette = DEFAULT_COLORS.copy()
        if colors:
            palette.update(colors)

        self.BG = palette["BG"]
        self.WHITE = palette["WHITE"]
        self.TEXT = palette["TEXT"]
        self.MUTED = palette["MUTED"]
        self.BLUE = palette["BLUE"]
        self.GREEN = palette["GREEN"]
        self.RED = palette["RED"]
        self.AMBER = palette["AMBER"]
        self.BORDER = palette["BORDER"]
        self.SOFT_BLUE = palette["SOFT_BLUE"]
        self.SOFT_GREEN = palette["SOFT_GREEN"]
        self.SOFT_RED = palette["SOFT_RED"]
        self.SOFT_AMBER = palette["SOFT_AMBER"]
        self.SIDEBAR = palette["SIDEBAR"]
        self.SIDEBAR_HOVER = palette["SIDEBAR_HOVER"]

        self.search_var = StringVar()
        self.semester_var = StringVar(value="All Semesters")
        self.mode_var = StringVar(value="All Modes")
        self.year_var = StringVar(value="All Years")
        self.status_var = StringVar(value="All Status")
        self.page_var = IntVar(value=1)

        self.all_rows = []
        self.filtered_rows = []
        self.pagination_buttons = []
        self.summary_vars = {}

        clear_frame(self.parent)
        self.build_ui()
        self.load_data()

    # --------------------------------------------------------
    # UI HELPERS
    # --------------------------------------------------------

    def button(self, parent, text, command, bg, fg, active_bg=None, width=15):
        return Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active_bg or bg,
            activeforeground=fg,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=("Helvetica", 9, "bold"),
            padx=14,
            pady=9,
            width=width
        )

    def pill(self, parent, text, bg, fg):
        return Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=("Helvetica", 8, "bold"),
            padx=10,
            pady=5
        )

    def format_semester(self, value):
        text = safe_text(value)
        if text.lower().startswith("semester"):
            return text
        try:
            return f"Semester {int(float(text))}"
        except Exception:
            return text

    def currency_value(self, value):
        try:
            return float(Decimal(str(value or 0)))
        except (InvalidOperation, TypeError, ValueError):
            return 0.0

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    def load_data(self):
        rows = fetch_all(
            """
            SELECT
                fp.Payment_ID,
                fp.Payment_Date,
                fp.Payment_Mode,
                fp.Amount,
                fp.Transaction_Reference,
                fp.Remarks,
                fp.Collected_By,
                COALESCE(sf.Payment_Status, 'Paid') AS Payment_Status,
                sf.Registration_No,
                fs.Semester,
                fs.Academic_Year,
                COALESCE(r.Name, %s) AS Student_Name,
                COALESCE(sd.Course, '') AS Course
            FROM fee_payments fp
            INNER JOIN student_fees sf
                ON sf.Student_Fee_ID = fp.Student_Fee_ID
            INNER JOIN fee_structures fs
                ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
            LEFT JOIN registration r
                ON r.Registration_No = sf.Registration_No
            LEFT JOIN student_details sd
                ON sd.Registration_No = sf.Registration_No
            WHERE sf.Registration_No = %s
            ORDER BY fp.Payment_Date DESC, fp.Payment_ID DESC
            """,
            (self.student_name, self.registration_no)
        )

        self.all_rows = rows or []
        self.filtered_rows = list(self.all_rows)

        semesters = []
        modes = []
        years = []
        statuses = []

        for row in self.all_rows:
            semester_text = self.format_semester(row.get("Semester"))
            if semester_text and semester_text not in semesters:
                semesters.append(semester_text)

            mode_text = safe_text(row.get("Payment_Mode"))
            if mode_text and mode_text not in modes:
                modes.append(mode_text)

            year_text = safe_text(row.get("Academic_Year"))
            if year_text and year_text not in years:
                years.append(year_text)

            status_text = safe_text(row.get("Payment_Status"), "Paid")
            if status_text and status_text not in statuses:
                statuses.append(status_text)

        self.semester_options = ["All Semesters"] + semesters
        self.mode_options = ["All Modes"] + modes
        self.year_options = ["All Years"] + years
        self.status_options = ["All Status"] + statuses

        self.semester_combo["values"] = self.semester_options
        self.mode_combo["values"] = self.mode_options
        self.year_combo["values"] = self.year_options
        self.status_combo["values"] = self.status_options

        self.semester_combo.set(self.semester_options[0])
        self.mode_combo.set(self.mode_options[0])
        self.year_combo.set(self.year_options[0])
        self.status_combo.set(self.status_options[0])

        self.update_summary()
        self.apply_filters()

    def update_summary(self):
        total_payments = len(self.all_rows)
        total_amount = sum(self.currency_value(row.get("Amount")) for row in self.all_rows)

        last_payment = self.all_rows[0] if self.all_rows else None
        last_payment_date = format_date(last_payment.get("Payment_Date")) if last_payment else "-"
        if self.all_rows:
            recent_modes = []
            for row in self.all_rows[:3]:
                mode = safe_text(row.get("Payment_Mode"))
                if mode and mode not in recent_modes:
                    recent_modes.append(mode)
            payment_mode = " / ".join(recent_modes[:2]) if recent_modes else "-"
        else:
            payment_mode = "-"

        self.summary_vars["total_payment"].set(f"{total_payments} Transactions")
        self.summary_vars["total_amount"].set(money(total_amount))
        self.summary_vars["last_payment"].set(last_payment_date)
        self.summary_vars["payment_mode"].set(payment_mode)

    # --------------------------------------------------------
    # BUILD UI
    # --------------------------------------------------------

    def build_ui(self):
        root = Frame(self.parent, bg=self.BG)
        root.pack(fill=BOTH, expand=True)

        canvas = Canvas(root, bg=self.BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
        content = Frame(canvas, bg=self.BG)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        def refresh_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def fit_width(event):
            canvas.itemconfigure(window_id, width=event.width)

        content.bind("<Configure>", refresh_scroll_region)
        canvas.bind("<Configure>", fit_width)

        scroll_state = {"target": 0.0, "job": None}

        def current_scroll_pixels():
            bbox = canvas.bbox("all")
            if not bbox:
                return 0.0, 0.0
            content_height = max(1.0, float(bbox[3] - bbox[1]))
            viewport_height = max(1.0, float(canvas.winfo_height()))
            max_scroll = max(0.0, content_height - viewport_height)
            return content_height, max_scroll

        def animate_scroll():
            content_height, max_scroll = current_scroll_pixels()
            target = max(0.0, min(scroll_state["target"], max_scroll))
            current = canvas.yview()[0] * content_height
            delta = target - current

            if abs(delta) < 1.0:
                canvas.yview_moveto(target / content_height)
                scroll_state["job"] = None
                return

            next_position = current + delta * 0.22
            canvas.yview_moveto(next_position / content_height)
            scroll_state["job"] = self.parent.after(10, animate_scroll)

        def mouse_wheel(event):
            content_height, max_scroll = current_scroll_pixels()
            if max_scroll <= 0:
                return "break"

            direction = -1 if event.delta > 0 else 1
            scroll_state["target"] = max(
                0.0,
                min(
                    canvas.yview()[0] * content_height + direction * 120,
                    max_scroll
                )
            )
            if scroll_state["job"] is None:
                animate_scroll()
            return "break"

        def enable_scroll(event=None):
            scroll_state["target"] = canvas.yview()[0] * current_scroll_pixels()[0]
            canvas.bind_all("<MouseWheel>", mouse_wheel)

        def disable_scroll(event=None):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", enable_scroll)
        content.bind("<Enter>", enable_scroll)
        canvas.bind("<Leave>", disable_scroll)

        self.build_header(content)
        self.build_summary(content)
        self.build_filters(content)
        self.build_timeline_area(content)
        self.build_pagination(content)

    def build_header(self, parent):
        header = Frame(parent, bg=self.BG)
        header.pack(fill=X, padx=28, pady=(24, 14))

        left = Frame(header, bg=self.BG)
        left.pack(side=LEFT, fill=BOTH, expand=True)

        Label(
            left,
            text="Payment History",
            bg=self.BG,
            fg=self.TEXT,
            font=("Helvetica", 22, "bold")
        ).pack(anchor="w")

        Label(
            left,
            text="View all your fee payment transactions.",
            bg=self.BG,
            fg=self.MUTED,
            font=("Helvetica", 10)
        ).pack(anchor="w", pady=(5, 0))

        right = Frame(header, bg=self.BG)
        right.pack(side=RIGHT)

        Label(
            right,
            text=self.student_name,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Helvetica", 10, "bold"),
            padx=14,
            pady=10,
            highlightbackground=self.BORDER,
            highlightthickness=1
        ).pack(side=TOP, anchor="e")

        Label(
            right,
            text=self.registration_no,
            bg=self.BG,
            fg=self.MUTED,
            font=("Helvetica", 8)
        ).pack(side=TOP, anchor="e", pady=(8, 0))

    def build_summary(self, parent):
        Label(
            parent,
            text="PAYMENT OVERVIEW",
            bg=self.BG,
            fg=self.TEXT,
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w", padx=28, pady=(4, 10))

        summary = Frame(parent, bg=self.BG)
        summary.pack(fill=X, padx=28, pady=(0, 18))

        for column in range(4):
            summary.grid_columnconfigure(column, weight=1, uniform="payment_summary")

        cards = [
            ("Total Payment", "total_payment", self.SOFT_BLUE, self.BLUE),
            ("Total Amount", "total_amount", self.SOFT_GREEN, self.GREEN),
            ("Last Payment", "last_payment", self.SOFT_AMBER, self.AMBER),
            ("Payment Mode", "payment_mode", self.SOFT_RED, self.RED),
        ]

        for column, (title, key, bg_color, accent) in enumerate(cards):
            card = Frame(
                summary,
                bg=self.WHITE,
                highlightbackground=self.BORDER,
                highlightthickness=1
            )
            card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 7, 0 if column == 3 else 7))

            Label(
                card,
                text=title,
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 9, "bold")
            ).pack(anchor="w", padx=18, pady=(16, 6))

            value_var = StringVar(value="-")
            self.summary_vars[key] = value_var

            Label(
                card,
                textvariable=value_var,
                bg=self.WHITE,
                fg=self.TEXT,
                font=("Helvetica", 17, "bold")
            ).pack(anchor="w", padx=18, pady=(0, 16))

            Frame(card, bg=accent, height=3).pack(fill=X, padx=18, pady=(0, 14))

    def build_filters(self, parent):
        filters = Frame(parent, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        filters.pack(fill=X, padx=28, pady=(0, 18))

        inner = Frame(filters, bg=self.WHITE)
        inner.pack(fill=X, padx=18, pady=16)

        Label(
            inner,
            text="FILTERS",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Helvetica", 10, "bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))

        Label(
            inner,
            text="Search",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Helvetica", 8, "bold")
        ).grid(row=0, column=1, sticky="w")

        search_entry = Entry(
            inner,
            textvariable=self.search_var,
            bd=1,
            relief=SOLID,
            fg=self.TEXT,
            bg=self.WHITE,
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.BLUE,
            font=("Helvetica", 10),
            width=28
        )
        search_entry.grid(row=1, column=1, sticky="we", padx=(0, 12), pady=(6, 0))

        self.button(
            inner,
            "Search",
            self.apply_filters,
            self.BLUE,
            self.WHITE,
            active_bg="#1D4ED8",
            width=11
        ).grid(row=1, column=2, sticky="w", pady=(6, 0))

        self.button(
            inner,
            "Reset",
            self.reset_filters,
            self.SIDEBAR,
            self.WHITE,
            active_bg=self.SIDEBAR_HOVER,
            width=11
        ).grid(row=1, column=3, sticky="w", padx=(10, 0), pady=(6, 0))

        combos = Frame(inner, bg=self.WHITE)
        combos.grid(row=2, column=0, columnspan=4, sticky="we", pady=(16, 0))

        for column in range(4):
            combos.grid_columnconfigure(column, weight=1)

        self.semester_combo = self.make_filter_combo(combos, 0, "Semester")
        self.mode_combo = self.make_filter_combo(combos, 1, "Payment Mode")
        self.year_combo = self.make_filter_combo(combos, 2, "Year")
        self.status_combo = self.make_filter_combo(combos, 3, "Status")

        inner.grid_columnconfigure(1, weight=1)
        inner.grid_columnconfigure(4, weight=1)

        self.semester_combo.bind("<<ComboboxSelected>>", lambda event=None: self.apply_filters())
        self.mode_combo.bind("<<ComboboxSelected>>", lambda event=None: self.apply_filters())
        self.year_combo.bind("<<ComboboxSelected>>", lambda event=None: self.apply_filters())
        self.status_combo.bind("<<ComboboxSelected>>", lambda event=None: self.apply_filters())
        self.search_var.trace_add("write", lambda *args: self.apply_filters(debounce=True))

    def make_filter_combo(self, parent, column, label_text):
        holder = Frame(parent, bg=self.WHITE)
        holder.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 0))

        Label(
            holder,
            text=label_text,
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Helvetica", 8, "bold")
        ).pack(anchor="w")

        combo = ttk.Combobox(
            holder,
            state="readonly",
            width=20,
            font=("Helvetica", 9)
        )
        combo.pack(fill=X, pady=(6, 0))
        combo.set("All")
        return combo

    def build_timeline_area(self, parent):
        section = Frame(parent, bg=self.BG)
        section.pack(fill=X, padx=28, pady=(0, 10))

        left = Frame(section, bg=self.BG)
        left.pack(side=LEFT, fill=X, expand=True)

        Label(
            left,
            text="PAYMENT TIMELINE",
            bg=self.BG,
            fg=self.TEXT,
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w")

        self.result_count_var = StringVar(value="0 records")
        Label(
            left,
            textvariable=self.result_count_var,
            bg=self.BG,
            fg=self.MUTED,
            font=("Helvetica", 9)
        ).pack(anchor="w", pady=(4, 0))

        self.refresh_button = self.button(
            section,
            "Refresh",
            self.load_data,
            self.WHITE,
            self.TEXT,
            active_bg="#EEF2FF",
            width=11
        )
        self.refresh_button.config(highlightbackground=self.BORDER, highlightthickness=1)
        self.refresh_button.pack(side=RIGHT)

        self.timeline = Frame(parent, bg=self.BG)
        self.timeline.pack(fill=BOTH, expand=True, padx=28, pady=(0, 18))

    def build_pagination(self, parent):
        bar = Frame(parent, bg=self.BG)
        bar.pack(fill=X, padx=28, pady=(0, 28))

        self.pagination_info = Label(
            bar,
            text="",
            bg=self.BG,
            fg=self.MUTED,
            font=("Helvetica", 9)
        )
        self.pagination_info.pack(side=LEFT)

        self.pagination_holder = Frame(bar, bg=self.BG)
        self.pagination_holder.pack(side=RIGHT)

    # --------------------------------------------------------
    # FILTERING / RENDERING
    # --------------------------------------------------------

    def reset_filters(self):
        self.search_var.set("")
        self.semester_combo.set("All Semesters")
        self.mode_combo.set("All Modes")
        self.year_combo.set("All Years")
        self.status_combo.set("All Status")
        self.page_var.set(1)
        self.apply_filters()

    def apply_filters(self, debounce=False):
        if debounce:
            if hasattr(self, "_debounce_job") and self._debounce_job is not None:
                try:
                    self.parent.after_cancel(self._debounce_job)
                except Exception:
                    pass
            self._debounce_job = self.parent.after(180, self.apply_filters)
            return

        query = normalize_text(self.search_var.get())
        semester_filter = normalize_text(self.semester_combo.get())
        mode_filter = normalize_text(self.mode_combo.get())
        year_filter = normalize_text(self.year_combo.get())
        status_filter = normalize_text(self.status_combo.get())

        filtered = []
        for row in self.all_rows:
            row_semester = normalize_text(self.format_semester(row.get("Semester")))
            row_mode = normalize_text(row.get("Payment_Mode"))
            row_year = normalize_text(row.get("Academic_Year"))
            row_status = normalize_text(row.get("Payment_Status") or "Paid")
            row_payment_id = normalize_text(f"PAY-{int(row.get('Payment_ID') or 0):06d}")
            row_reference = normalize_text(row.get("Transaction_Reference"))
            row_remarks = normalize_text(row.get("Remarks"))
            row_collected = normalize_text(row.get("Collected_By"))
            row_text = " ".join([
                row_payment_id,
                row_semester,
                row_mode,
                row_year,
                row_status,
                row_reference,
                row_remarks,
                row_collected
            ])

            if semester_filter != "all semesters" and row_semester != semester_filter:
                continue
            if mode_filter != "all modes" and row_mode != mode_filter:
                continue
            if year_filter != "all years" and row_year != year_filter:
                continue
            if status_filter != "all status" and row_status != status_filter:
                continue
            if query and query not in row_text:
                continue
            filtered.append(row)

        self.filtered_rows = filtered
        self.page_var.set(1)
        self.render_timeline()
        self.render_pagination()

    def render_timeline(self):
        clear_frame(self.timeline)

        total = len(self.filtered_rows)
        page_size = 4
        total_pages = max(1, (total + page_size - 1) // page_size)
        current_page = min(max(1, int(self.page_var.get() or 1)), total_pages)
        self.page_var.set(current_page)

        start = (current_page - 1) * page_size
        end = start + page_size
        page_rows = self.filtered_rows[start:end]

        self.result_count_var.set(f"{total} record(s) found")
        self.pagination_info.config(
            text=f"Showing {start + 1 if total else 0}-{min(end, total)} of {total}"
        )

        if not page_rows:
            empty = Frame(
                self.timeline,
                bg=self.WHITE,
                highlightbackground=self.BORDER,
                highlightthickness=1
            )
            empty.pack(fill=X)

            Label(
                empty,
                text="No payment records found.",
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 11, "bold"),
                pady=24
            ).pack(fill=X)
            return

        grouped = {}
        for row in page_rows:
            grouped.setdefault(format_date(row.get("Payment_Date")), []).append(row)

        for date_text, items in grouped.items():
            date_label = Frame(self.timeline, bg=self.BG)
            date_label.pack(fill=X, pady=(0, 8))

            Label(
                date_label,
                text=date_text,
                bg=self.BG,
                fg=self.MUTED,
                font=("Helvetica", 10, "bold")
            ).pack(anchor="w")

            for row in items:
                self.render_payment_card(self.timeline, row)

    def render_payment_card(self, parent, row):
        card = Frame(
            parent,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        card.pack(fill=X, pady=(0, 14))

        top = Frame(card, bg=self.WHITE)
        top.pack(fill=X, padx=18, pady=(16, 8))

        left = Frame(top, bg=self.WHITE)
        left.pack(side=LEFT, fill=X, expand=True)

        payment_id = f"PAY-{int(row.get('Payment_ID') or 0):06d}"
        semester = self.format_semester(row.get("Semester"))
        mode = safe_text(row.get("Payment_Mode"))
        status = safe_text(row.get("Payment_Status"), "Paid")
        status_lower = status.lower()

        Label(
            left,
            text=payment_id,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Helvetica", 12, "bold")
        ).pack(anchor="w")

        Label(
            left,
            text=f"{semester}  |  {format_date(row.get('Payment_Date'))}",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Helvetica", 9)
        ).pack(anchor="w", pady=(4, 0))

        self.pill(
            top,
            status.upper(),
            self.SOFT_GREEN if status_lower == "paid" else self.SOFT_AMBER,
            self.GREEN if status_lower == "paid" else self.AMBER
        ).pack(side=RIGHT)

        body = Frame(card, bg=self.WHITE)
        body.pack(fill=X, padx=18, pady=(2, 14))
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_columnconfigure(2, weight=1)

        details = [
            ("Amount", money(row.get("Amount"))),
            ("Mode", mode),
            ("Collected By", safe_text(row.get("Collected_By"))),
            ("Transaction", safe_text(row.get("Transaction_Reference"))),
            ("Remarks", safe_text(row.get("Remarks"))),
            ("Academic Year", safe_text(row.get("Academic_Year")))
        ]

        for index, (label, value) in enumerate(details):
            column = index % 3
            row_number = index // 3
            slot = Frame(body, bg=self.WHITE)
            slot.grid(row=row_number, column=column, sticky="nsew", padx=(0 if column == 0 else 8, 8 if column < 2 else 0), pady=6)

            Label(
                slot,
                text=label.upper(),
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 8, "bold")
            ).pack(anchor="w")

            Label(
                slot,
                text=value,
                bg=self.WHITE,
                fg=self.TEXT,
                font=("Helvetica", 10, "bold"),
                wraplength=210,
                justify=LEFT
            ).pack(anchor="w", pady=(4, 0))

        actions = Frame(card, bg=self.WHITE)
        actions.pack(fill=X, padx=18, pady=(0, 16))

        self.button(
            actions,
            "View Receipt",
            lambda payment_id=row.get("Payment_ID"): self.open_receipt(payment_id),
            self.BLUE,
            self.WHITE,
            active_bg="#1D4ED8",
            width=14
        ).pack(side=RIGHT)

    def render_pagination(self):
        clear_frame(self.pagination_holder)
        self.pagination_buttons = []

        total = len(self.filtered_rows)
        page_size = 4
        total_pages = max(1, (total + page_size - 1) // page_size)
        current_page = min(max(1, int(self.page_var.get() or 1)), total_pages)

        def go_to(page):
            self.page_var.set(page)
            self.render_timeline()
            self.render_pagination()

        self.button(
            self.pagination_holder,
            "Previous",
            lambda: go_to(max(1, current_page - 1)),
            self.WHITE,
            self.TEXT,
            active_bg="#EEF2FF",
            width=12
        ).pack(side=LEFT, padx=(0, 8))

        page_numbers = list(range(1, total_pages + 1))
        if len(page_numbers) > 5:
            start = max(1, current_page - 2)
            end = min(total_pages, start + 4)
            start = max(1, end - 4)
            page_numbers = list(range(start, end + 1))

        for page in page_numbers:
            active = page == current_page
            button = Button(
                self.pagination_holder,
                text=str(page),
                command=lambda p=page: go_to(p),
                bg=self.BLUE if active else self.WHITE,
                fg=self.WHITE if active else self.TEXT,
                activebackground=self.BLUE,
                activeforeground=self.WHITE,
                bd=0,
                relief=FLAT,
                cursor="hand2",
                font=("Helvetica", 9, "bold"),
                padx=12,
                pady=8,
                width=4
            )
            if not active:
                button.config(highlightbackground=self.BORDER, highlightthickness=1)
            button.pack(side=LEFT, padx=4)

        self.button(
            self.pagination_holder,
            "Next",
            lambda: go_to(min(total_pages, current_page + 1)),
            self.WHITE,
            self.TEXT,
            active_bg="#EEF2FF",
            width=10
        ).pack(side=LEFT, padx=(8, 0))

    # --------------------------------------------------------
    # RECEIPT
    # --------------------------------------------------------

    def load_receipt(self, payment_id):
        return fetch_one(
            """
            SELECT
                fp.Payment_ID,
                fp.Payment_Date,
                fp.Payment_Mode,
                fp.Amount,
                fp.Transaction_Reference,
                fp.Remarks,
                fp.Collected_By,
                COALESCE(sf.Payment_Status, 'Paid') AS Payment_Status,
                sf.Registration_No,
                sf.Total_Fee,
                sf.Amount_Paid,
                sf.Due_Amount,
                fs.Semester,
                fs.Academic_Year,
                COALESCE(r.Name, %s) AS Student_Name,
                COALESCE(sd.Course, '') AS Course
            FROM fee_payments fp
            INNER JOIN student_fees sf
                ON sf.Student_Fee_ID = fp.Student_Fee_ID
            INNER JOIN fee_structures fs
                ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
            LEFT JOIN registration r
                ON r.Registration_No = sf.Registration_No
            LEFT JOIN student_details sd
                ON sd.Registration_No = sf.Registration_No
            WHERE fp.Payment_ID = %s
            LIMIT 1
            """,
            (self.student_name, payment_id)
        )

    def build_pdf(self, receipt, output_path):
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import mm
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        except Exception as error:
            raise RuntimeError(
                "PDF export requires reportlab. Install it with: python -m pip install reportlab"
            ) from error

        document = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=16 * mm,
            bottomMargin=16 * mm
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "ReceiptTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0F172A"),
            alignment=1,
            spaceAfter=6
        )
        sub_style = ParagraphStyle(
            "ReceiptSub",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#64748B"),
            alignment=1
        )
        label_style = ParagraphStyle(
            "ReceiptLabel",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=colors.HexColor("#64748B")
        )
        value_style = ParagraphStyle(
            "ReceiptValue",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#0F172A")
        )

        story = [
            Paragraph("PAYMENT RECEIPT", title_style),
            Paragraph("Student Payment History", sub_style),
            Spacer(1, 8)
        ]

        header_data = [
            [Paragraph("<b>Receipt No.</b>", label_style), Paragraph(f"PAY-{int(receipt['Payment_ID']):06d}", value_style)],
            [Paragraph("<b>Student Name</b>", label_style), Paragraph(safe_text(receipt.get("Student_Name")), value_style)],
            [Paragraph("<b>Registration No.</b>", label_style), Paragraph(safe_text(receipt.get("Registration_No")), value_style)],
            [Paragraph("<b>Course</b>", label_style), Paragraph(safe_text(receipt.get("Course")), value_style)],
            [Paragraph("<b>Semester</b>", label_style), Paragraph(self.format_semester(receipt.get("Semester")), value_style)],
            [Paragraph("<b>Payment Date</b>", label_style), Paragraph(format_date(receipt.get("Payment_Date")), value_style)],
            [Paragraph("<b>Payment Mode</b>", label_style), Paragraph(safe_text(receipt.get("Payment_Mode")), value_style)],
            [Paragraph("<b>Amount Paid</b>", label_style), Paragraph(money(receipt.get("Amount")), value_style)],
            [Paragraph("<b>Collected By</b>", label_style), Paragraph(safe_text(receipt.get("Collected_By")), value_style)],
            [Paragraph("<b>Transaction ID</b>", label_style), Paragraph(safe_text(receipt.get("Transaction_Reference")), value_style)],
            [Paragraph("<b>Remarks</b>", label_style), Paragraph(safe_text(receipt.get("Remarks")), value_style)],
            [Paragraph("<b>Status</b>", label_style), Paragraph(safe_text(receipt.get("Payment_Status"), "Paid"), value_style)],
        ]

        receipt_table = Table(header_data, colWidths=[50 * mm, 110 * mm], hAlign="LEFT")
        receipt_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E2E8F0")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        story.append(receipt_table)
        story.append(Spacer(1, 10))

        totals = Table([
            [Paragraph("<b>Total Fee</b>", label_style), Paragraph(money(receipt.get("Total_Fee")), value_style)],
            [Paragraph("<b>Total Paid</b>", label_style), Paragraph(money(receipt.get("Amount_Paid")), value_style)],
            [Paragraph("<b>Due Amount</b>", label_style), Paragraph(money(receipt.get("Due_Amount")), value_style)],
        ], colWidths=[50 * mm, 110 * mm], hAlign="LEFT")
        totals.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E2E8F0")),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(totals)
        story.append(Spacer(1, 12))
        story.append(Paragraph("This is a computer-generated payment receipt.", sub_style))

        document.build(story)

    def download_receipt(self, receipt, owner):
        default_name = f"PAY-{int(receipt['Payment_ID']):06d}_{safe_text(receipt.get('Registration_No'))}.pdf"
        file_path = filedialog.asksaveasfilename(
            parent=owner,
            title="Save Payment Receipt",
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF File", "*.pdf")]
        )
        if not file_path:
            return

        try:
            self.build_pdf(receipt, file_path)
            messagebox.showinfo("Receipt Saved", "Payment receipt saved successfully.", parent=owner)
        except Exception as error:
            messagebox.showerror("Save Error", str(error), parent=owner)

    def print_receipt(self, receipt, owner):
        temp_dir = tempfile.gettempdir()
        temp_name = f"PAY-{int(receipt['Payment_ID']):06d}_{safe_text(receipt.get('Registration_No'))}.pdf"
        temp_path = os.path.join(temp_dir, temp_name)

        try:
            self.build_pdf(receipt, temp_path)
        except Exception as error:
            messagebox.showerror("Print Error", str(error), parent=owner)
            return

        try:
            if os.name == "nt":
                os.startfile(temp_path, "print")
            else:
                os.startfile(temp_path)
        except Exception:
            messagebox.showinfo(
                "Print Receipt",
                f"Receipt file created at:\n{temp_path}",
                parent=owner
            )

    def open_receipt(self, payment_id):
        receipt = self.load_receipt(payment_id)
        if not receipt:
            messagebox.showerror("Receipt Error", "Payment receipt data was not found.", parent=self.parent)
            return

        owner = self.parent.winfo_toplevel()
        window = Toplevel(owner)
        window.title("Payment Receipt")
        window.configure(bg=self.BG)
        window.resizable(False, False)
        window.transient(owner)

        width = 620
        height = 720
        screen_width = window.winfo_screenwidth()
        x = max(10, int((screen_width - width) / 2))
        y = 40
        window.geometry(f"{width}x{height}+{x}+{y}")

        try:
            owner.grab_release()
        except TclError:
            pass

        def close_receipt():
            try:
                window.grab_release()
            except TclError:
                pass
            window.destroy()
            if owner is not None and owner.winfo_exists():
                owner.lift()
                owner.focus_force()

        window.protocol("WM_DELETE_WINDOW", close_receipt)

        header = Frame(window, bg=self.BLUE, height=108)
        header.pack(fill=X)
        header.pack_propagate(False)

        Label(
            header,
            text="PAYMENT RECEIPT",
            bg=self.BLUE,
            fg=self.WHITE,
            font=("Helvetica", 20, "bold")
        ).place(x=26, y=20)

        Label(
            header,
            text=f"Receipt No: PAY-{int(receipt['Payment_ID']):06d}",
            bg=self.BLUE,
            fg="#DBEAFE",
            font=("Helvetica", 9)
        ).place(x=26, y=67)

        body = Frame(window, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        body.pack(fill=BOTH, expand=True, padx=22, pady=(18, 12))

        details = [
            ("Student Name", safe_text(receipt.get("Student_Name"))),
            ("Registration No.", safe_text(receipt.get("Registration_No"))),
            ("Course", safe_text(receipt.get("Course"))),
            ("Semester", self.format_semester(receipt.get("Semester"))),
            ("Payment Date", format_date(receipt.get("Payment_Date"))),
            ("Payment Mode", safe_text(receipt.get("Payment_Mode"))),
            ("Amount Paid", money(receipt.get("Amount"))),
            ("Collected By", safe_text(receipt.get("Collected_By"))),
            ("Transaction ID", safe_text(receipt.get("Transaction_Reference"))),
            ("Remarks", safe_text(receipt.get("Remarks"))),
        ]

        info = Frame(body, bg=self.WHITE)
        info.pack(fill=X, padx=24, pady=(18, 10))

        for label, value in details:
            row = Frame(info, bg=self.WHITE, height=28)
            row.pack(fill=X)
            row.pack_propagate(False)

            Label(
                row,
                text=label,
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 8, "bold"),
                anchor=W
            ).place(x=0, y=5, width=160)

            Label(
                row,
                text=value,
                bg=self.WHITE,
                fg=self.TEXT,
                font=("Helvetica", 9, "bold"),
                anchor=W
            ).place(x=168, y=4, width=330)

        Frame(body, bg=self.BORDER, height=1).pack(fill=X, padx=24, pady=(6, 10))

        amount_box = Frame(body, bg=self.SOFT_GREEN, highlightbackground="#BBF7D0", highlightthickness=1, height=78)
        amount_box.pack(fill=X, padx=24)
        amount_box.pack_propagate(False)

        Label(
            amount_box,
            text="AMOUNT PAID",
            bg=self.SOFT_GREEN,
            fg=self.MUTED,
            font=("Helvetica", 8, "bold")
        ).place(x=18, y=12)

        Label(
            amount_box,
            text=money(receipt.get("Amount")),
            bg=self.SOFT_GREEN,
            fg=self.GREEN,
            font=("Helvetica", 20, "bold")
        ).place(x=18, y=34)

        summary = Frame(body, bg=self.WHITE)
        summary.pack(fill=X, padx=24, pady=(12, 8))

        summary_rows = [
            ("Total Fee", money(receipt.get("Total_Fee"))),
            ("Total Paid", money(receipt.get("Amount_Paid"))),
            ("Due Amount", money(receipt.get("Due_Amount"))),
            ("Payment Status", safe_text(receipt.get("Payment_Status"), "Paid")),
        ]

        for label, value in summary_rows:
            row = Frame(summary, bg=self.WHITE, height=26)
            row.pack(fill=X)
            row.pack_propagate(False)

            Label(
                row,
                text=label,
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Helvetica", 8, "bold"),
                anchor=W
            ).pack(side=LEFT)

            Label(
                row,
                text=value,
                bg=self.WHITE,
                fg=self.TEXT,
                font=("Helvetica", 9, "bold"),
                anchor=E
            ).pack(side=RIGHT)

        actions = Frame(window, bg=self.WHITE, height=72, highlightbackground=self.BORDER, highlightthickness=1)
        actions.pack(side=BOTTOM, fill=X)
        actions.pack_propagate(False)

        self.button(
            actions,
            "Download PDF",
            lambda: self.download_receipt(receipt, window),
            self.BLUE,
            self.WHITE,
            active_bg="#1D4ED8",
            width=15
        ).pack(side=LEFT, padx=(20, 8), pady=14)

        self.button(
            actions,
            "Print Receipt",
            lambda: self.print_receipt(receipt, window),
            self.SIDEBAR,
            self.WHITE,
            active_bg=self.SIDEBAR_HOVER,
            width=15
        ).pack(side=LEFT, pady=14)

        self.button(
            actions,
            "Close",
            close_receipt,
            self.RED,
            self.WHITE,
            active_bg="#B91C1C",
            width=12
        ).pack(side=RIGHT, padx=(8, 20), pady=14)

        window.update_idletasks()
        window.lift()
        window.focus_force()
        try:
            window.grab_set()
        except TclError:
            pass


def show_student_payment_history(
    parent,
    registration_no,
    student_name="Student",
    colors=None,
    on_dashboard=None
):
    StudentPaymentHistoryPage(
        parent=parent,
        registration_no=registration_no,
        student_name=student_name,
        colors=colors,
        on_dashboard=on_dashboard
    )
