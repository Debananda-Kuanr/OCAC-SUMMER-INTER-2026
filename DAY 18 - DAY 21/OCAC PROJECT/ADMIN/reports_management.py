from tkinter import *
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import csv
from datetime import date, datetime


# ============================================================
# FILE NAME: reports_management.py
# PURPOSE:
#   Read-only Reports module for the Fee Status Management System.
#
# MAIN FUNCTION:
#   open_reports_management(parent, current_role="Admin")
#
# DATABASE TABLES USED:
#   registration
#   student_details
#   courses
#   fee_structures
#   fee_structure_components
#   student_fees
#   fee_payments
# ============================================================


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
DARK_BLUE = "#1D4ED8"
PURPLE = "#7C3AED"
WHITE = "#FFFFFF"
BG = "#F8FAFC"
TEXT = "#0F172A"
GRAY = "#64748B"
BORDER = "#CBD5E1"
LIGHT_BORDER = "#E2E8F0"
LIGHT_BLUE = "#EFF6FF"
LIGHT_GREEN = "#F0FDF4"
GREEN = "#16A34A"
LIGHT_RED = "#FEF2F2"
RED = "#DC2626"
LIGHT_ORANGE = "#FFF7ED"
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
# MONEY FORMAT
# ============================================================

def money(value):
    try:
        return f"₹{float(value or 0):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"


# ============================================================
# MAIN REPORTS PAGE
# ============================================================

def open_reports_management(parent, current_role="Admin"):

    # --------------------------------------------------------
    # CLEAR CURRENT PAGE
    # --------------------------------------------------------

    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg=BG)

    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    active_report = StringVar(value="Overview")
    current_export_headers = []
    current_export_rows = []
    current_report_title = "Reports Overview"
    current_report_subtitle = "A summary of the current fee status."

    search_var = StringVar()
    course_var = StringVar(value="All Courses")
    status_var = StringVar(value="All Status")
    mode_var = StringVar(value="All Modes")
    academic_year_var = StringVar(value="All Academic Years")
    from_date_var = StringVar()
    to_date_var = StringVar()
    accountant_var = StringVar(value="All Accountants")
    report_period_var = StringVar(value="This Month")

    course_map = {}
    accountant_values = ["All Accountants"]

    # --------------------------------------------------------
    # STYLES
    # --------------------------------------------------------

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except TclError:
        pass

    style.configure(
        "Report.Treeview",
        background=WHITE,
        fieldbackground=WHITE,
        foreground=TEXT,
        rowheight=38,
        borderwidth=0,
        font=("Helvetica", 9)
    )

    style.configure(
        "Report.Treeview.Heading",
        background="#F1F5F9",
        foreground=TEXT,
        relief=FLAT,
        font=("Helvetica", 9, "bold")
    )

    style.map(
        "Report.Treeview",
        background=[("selected", LIGHT_BLUE)],
        foreground=[("selected", TEXT)]
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    header = Frame(parent, bg=BG)
    header.pack(fill=X, padx=28, pady=(24, 14))

    header_left = Frame(header, bg=BG)
    header_left.pack(side=LEFT)

    Label(
        header_left,
        text="Reports",
        bg=BG,
        fg=TEXT,
        font=("Helvetica", 23, "bold")
    ).pack(anchor="w")

    Label(
        header_left,
        text="View and analyze fee collection, outstanding dues and student fee records.",
        bg=BG,
        fg=GRAY,
        font=("Helvetica", 10)
    ).pack(anchor="w", pady=(4, 0))

    Label(
        header,
        text=f"VIEW ONLY  •  {str(current_role).upper()}",
        bg=LIGHT_BLUE,
        fg=BLUE,
        font=("Helvetica", 8, "bold"),
        padx=12,
        pady=7
    ).pack(side=RIGHT)

    # --------------------------------------------------------
    # SUMMARY CARDS
    # --------------------------------------------------------

    summary_frame = Frame(parent, bg=BG)
    summary_frame.pack(fill=X, padx=28, pady=(0, 14))

    for column in range(4):
        summary_frame.grid_columnconfigure(column, weight=1)

    total_fee_var = StringVar(value="₹0.00")
    collected_var = StringVar(value="₹0.00")
    due_var = StringVar(value="₹0.00")
    rate_var = StringVar(value="0.00%")

    def create_summary_card(column, title, variable, bg_color, value_color):
        card = Frame(
            summary_frame,
            bg=WHITE,
            highlightbackground=LIGHT_BORDER,
            highlightthickness=1
        )
        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(0 if column == 0 else 6, 0 if column == 3 else 6)
        )

        top_line = Frame(card, bg=bg_color, height=4)
        top_line.pack(fill=X)

        Label(
            card,
            text=title,
            bg=WHITE,
            fg=GRAY,
            font=("Helvetica", 8, "bold")
        ).pack(anchor="w", padx=17, pady=(15, 5))

        Label(
            card,
            textvariable=variable,
            bg=WHITE,
            fg=value_color,
            font=("Helvetica", 18, "bold")
        ).pack(anchor="w", padx=17, pady=(0, 16))

    create_summary_card(0, "TOTAL ASSIGNED FEES", total_fee_var, BLUE, TEXT)
    create_summary_card(1, "TOTAL COLLECTED", collected_var, GREEN, GREEN)
    create_summary_card(2, "TOTAL OUTSTANDING", due_var, RED, RED)
    create_summary_card(3, "COLLECTION RATE", rate_var, PURPLE, PURPLE)

    # --------------------------------------------------------
    # TAB BAR
    # --------------------------------------------------------

    tab_card = Frame(
        parent,
        bg=WHITE,
        highlightbackground=LIGHT_BORDER,
        highlightthickness=1
    )
    tab_card.pack(fill=X, padx=28, pady=(0, 12))

    tabs_frame = Frame(tab_card, bg=WHITE)
    tabs_frame.pack(fill=X, padx=10, pady=9)

    tab_buttons = {}

    # --------------------------------------------------------
    # CONTENT AREA
    # --------------------------------------------------------

    content_card = Frame(
        parent,
        bg=WHITE,
        highlightbackground=LIGHT_BORDER,
        highlightthickness=1
    )
    content_card.pack(fill=BOTH, expand=True, padx=28, pady=(0, 24))

    content_header = Frame(content_card, bg=WHITE)
    content_header.pack(fill=X, padx=22, pady=(18, 10))

    report_title_var = StringVar(value="Reports Overview")
    report_subtitle_var = StringVar(value="A summary of the current fee status.")

    title_area = Frame(content_header, bg=WHITE)
    title_area.pack(side=LEFT)

    Label(
        title_area,
        textvariable=report_title_var,
        bg=WHITE,
        fg=TEXT,
        font=("Helvetica", 15, "bold")
    ).pack(anchor="w")

    Label(
        title_area,
        textvariable=report_subtitle_var,
        bg=WHITE,
        fg=GRAY,
        font=("Helvetica", 9)
    ).pack(anchor="w", pady=(3, 0))

    action_area = Frame(content_header, bg=WHITE)
    action_area.pack(side=RIGHT)

    # --------------------------------------------------------
    # FILTER AREA
    # --------------------------------------------------------

    filter_frame = Frame(content_card, bg="#F8FAFC")
    filter_frame.pack(fill=X, padx=22, pady=(0, 12))

    # --------------------------------------------------------
    # TABLE AREA
    # --------------------------------------------------------

    table_outer = Frame(content_card, bg=WHITE)
    table_outer.pack(fill=BOTH, expand=True, padx=22, pady=(0, 18))

    # ========================================================
    # DATABASE HELPERS
    # ========================================================

    def fetch_one(query, params=()):
        con = None
        cursor = None

        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchone()

        finally:
            if cursor is not None:
                cursor.close()

            if con is not None and con.is_connected():
                con.close()

    def fetch_all(query, params=()):
        con = None
        cursor = None

        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()

        finally:
            if cursor is not None:
                cursor.close()

            if con is not None and con.is_connected():
                con.close()

    # ========================================================
    # LOAD MASTER FILTER DATA
    # ========================================================

    def load_filter_data():
        nonlocal course_map, accountant_values

        try:
            course_records = fetch_all(
                """
                SELECT
                    Course_ID,
                    Course_Name
                FROM courses
                WHERE LOWER(TRIM(Status)) = 'active'
                ORDER BY Course_Name
                """
            )

            course_map = {
                record["Course_Name"]: record["Course_ID"]
                for record in course_records
            }

            years = fetch_all(
                """
                SELECT DISTINCT Academic_Year
                FROM fee_structures
                WHERE Academic_Year IS NOT NULL
                  AND TRIM(Academic_Year) <> ''
                ORDER BY Academic_Year DESC
                """
            )

            course_values = ["All Courses"] + list(course_map.keys())
            year_values = ["All Academic Years"] + [
                str(record["Academic_Year"])
                for record in years
            ]

            collectors = fetch_all(
                """
                    SELECT DISTINCT TRIM(Collected_By) AS Collected_By
                    FROM fee_payments
                    WHERE Collected_By IS NOT NULL
                      AND TRIM(Collected_By) <> ''
                    ORDER BY Collected_By
                """
            )

            accountant_values = ["All Accountants"] + [
                str(record["Collected_By"]).strip()
                for record in collectors
                if str(record["Collected_By"] or "").strip()
            ]

            return course_values, year_values

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load report filters.\n\n{error}",
                parent=parent
            )

            return ["All Courses"], ["All Academic Years"]

    course_values, year_values = load_filter_data()

    # ========================================================
    # SUMMARY
    # ========================================================

    def load_summary():
        try:
            result = fetch_one(
                """
                SELECT
                    COALESCE(SUM(Total_Fee), 0) AS Total_Fee,
                    COALESCE(SUM(Amount_Paid), 0) AS Amount_Paid,
                    COALESCE(SUM(Due_Amount), 0) AS Due_Amount
                FROM student_fees
                """
            )

            total = float(result["Total_Fee"] or 0)
            paid = float(result["Amount_Paid"] or 0)
            due = float(result["Due_Amount"] or 0)

            rate = (paid / total * 100) if total > 0 else 0

            total_fee_var.set(money(total))
            collected_var.set(money(paid))
            due_var.set(money(due))
            rate_var.set(f"{rate:.2f}%")

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load report summary.\n\n{error}",
                parent=parent
            )

    # ========================================================
    # UI HELPERS
    # ========================================================

    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def create_filter_label(container, text):
        Label(
            container,
            text=text,
            bg="#F8FAFC",
            fg=TEXT,
            font=("Helvetica", 8, "bold")
        ).pack(anchor="w", pady=(0, 5))

    def create_entry_filter(container, label_text, variable, width=22):
        box = Frame(container, bg="#F8FAFC")
        box.pack(side=LEFT, padx=(0, 10), pady=12)

        create_filter_label(box, label_text)

        entry = Entry(
            box,
            textvariable=variable,
            bg=WHITE,
            fg=TEXT,
            relief=SOLID,
            bd=1,
            font=("Helvetica", 9),
            width=width
        )
        entry.pack(ipady=6)

        return entry

    def create_combo_filter(container, label_text, variable, values, width=18):
        box = Frame(container, bg="#F8FAFC")
        box.pack(side=LEFT, padx=(0, 10), pady=12)

        create_filter_label(box, label_text)

        combo = ttk.Combobox(
            box,
            textvariable=variable,
            values=values,
            state="readonly",
            width=width,
            font=("Helvetica", 9)
        )
        combo.pack(ipady=4)

        return combo

    def create_table(columns, headings, widths, rows, anchors=None):
        nonlocal current_export_headers, current_export_rows
        nonlocal current_report_title, current_report_subtitle

        current_report_title = report_title_var.get()
        current_report_subtitle = report_subtitle_var.get()

        clear_frame(table_outer)

        current_export_headers = list(headings)
        current_export_rows = [list(row) for row in rows]

        if anchors is None:
            anchors = ["w"] * len(columns)

        tree_frame = Frame(table_outer, bg=WHITE)
        tree_frame.pack(fill=BOTH, expand=True)

        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Report.Treeview"
        )

        y_scroll = ttk.Scrollbar(
            tree_frame,
            orient=VERTICAL,
            command=tree.yview
        )

        x_scroll = ttk.Scrollbar(
            tree_frame,
            orient=HORIZONTAL,
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        for index, column in enumerate(columns):
            tree.heading(column, text=headings[index])
            tree.column(
                column,
                width=widths[index],
                minwidth=70,
                anchor=anchors[index],
                stretch=True
            )

        for row in rows:
            tree.insert("", END, values=row)

        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        if not rows:
            empty = Label(
                tree,
                text=""
            )

        return tree

    # ========================================================
    # EXPORT CSV
    # ========================================================

    def export_csv():
        if not current_export_rows:
            messagebox.showwarning(
                "No Data",
                "There is no report data to export.",
                parent=parent
            )
            return

        report_name = active_report.get().lower().replace(" ", "_")

        file_path = filedialog.asksaveasfilename(
            parent=parent,
            title="Export Report",
            defaultextension=".csv",
            initialfile=f"{report_name}_report_{date.today().isoformat()}.csv",
            filetypes=[("CSV File", "*.csv")]
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(current_export_headers)
                writer.writerows(current_export_rows)

            messagebox.showinfo(
                "Export Complete",
                f"Report exported successfully.\n\n{file_path}",
                parent=parent
            )

        except Exception as error:
            messagebox.showerror(
                "Export Error",
                f"Could not export the report.\n\n{error}",
                parent=parent
            )


    # ========================================================
    # EXPORT PDF
    # ========================================================

    def export_pdf():
        if not current_export_rows:
            messagebox.showwarning(
                "No Data",
                "There is no report data to export.",
                parent=parent
            )
            return

        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER
            from reportlab.platypus import (
                SimpleDocTemplate,
                Table,
                TableStyle,
                Paragraph,
                Spacer
            )
        except ImportError:
            messagebox.showerror(
                "PDF Library Required",
                "ReportLab is required for PDF export.\n\n"
                "Install it using:\npython -m pip install reportlab",
                parent=parent
            )
            return

        report_name = active_report.get().lower().replace(" ", "_")

        file_path = filedialog.asksaveasfilename(
            parent=parent,
            title="Export PDF Report",
            defaultextension=".pdf",
            initialfile=f"{report_name}_report_{date.today().isoformat()}.pdf",
            filetypes=[("PDF File", "*.pdf")]
        )

        if not file_path:
            return

        try:
            document = SimpleDocTemplate(
                file_path,
                pagesize=landscape(A4),
                rightMargin=24,
                leftMargin=24,
                topMargin=24,
                bottomMargin=24,
                title=current_report_title,
                author="Administrator"
            )

            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                "AdminReportTitle",
                parent=styles["Title"],
                fontName="Helvetica-Bold",
                fontSize=17,
                leading=21,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#0F172A"),
                spaceAfter=4
            )

            subtitle_style = ParagraphStyle(
                "AdminReportSubtitle",
                parent=styles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=10,
                leading=14,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#2563EB"),
                spaceAfter=6
            )

            small_style = ParagraphStyle(
                "AdminReportSmall",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=6.5,
                leading=8,
                textColor=colors.HexColor("#334155")
            )

            story = []

            story.append(
                Paragraph(
                    "FEE STATUS MANAGEMENT SYSTEM",
                    title_style
                )
            )

            story.append(
                Paragraph(
                    current_report_title.upper(),
                    subtitle_style
                )
            )

            story.append(
                Paragraph(
                    current_report_subtitle,
                    ParagraphStyle(
                        "AdminReportDescription",
                        parent=styles["Normal"],
                        fontName="Helvetica",
                        fontSize=8,
                        leading=11,
                        alignment=TA_CENTER,
                        textColor=colors.HexColor("#64748B"),
                        spaceAfter=12
                    )
                )
            )

            info_data = [
                [
                    "GENERATED BY",
                    "Administrator",
                    "GENERATED ON",
                    datetime.now().strftime("%d %B %Y, %I:%M %p")
                ]
            ]

            if active_report.get() == "Accountant-Wise":
                info_data.append(
                    [
                        "ACCOUNTANT",
                        accountant_var.get(),
                        "REPORT PERIOD",
                        (
                            f"{from_date_var.get() or 'Beginning'}"
                            f" to "
                            f"{to_date_var.get() or date.today().isoformat()}"
                        )
                    ]
                )

            info_table = Table(
                info_data,
                colWidths=[90, 210, 90, 210]
            )

            info_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EFF6FF")),
                        ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#EFF6FF")),
                        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 7),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                        ("TOPPADDING", (0, 0), (-1, -1), 7),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                    ]
                )
            )

            story.append(info_table)
            story.append(Spacer(1, 14))

            if active_report.get() == "Accountant-Wise":
                total_amount = 0.0
                payment_count = len(current_export_rows)

                for row in current_export_rows:
                    try:
                        amount_text = str(row[-1]).replace("₹", "").replace(",", "").strip()
                        total_amount += float(amount_text)
                    except (ValueError, TypeError):
                        pass

                average = total_amount / payment_count if payment_count else 0

                summary_table = Table(
                    [
                        ["TOTAL COLLECTION", "TOTAL PAYMENTS", "AVERAGE PAYMENT"],
                        [
                            f"Rs. {total_amount:,.2f}",
                            str(payment_count),
                            f"Rs. {average:,.2f}"
                        ]
                    ],
                    colWidths=[200, 200, 200]
                )

                summary_table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EFF6FF")),
                            ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F0FDF4")),
                            ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#F5F3FF")),
                            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, 0), 7),
                            ("FONTSIZE", (0, 1), (-1, 1), 12),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                            ("TOPPADDING", (0, 0), (-1, -1), 8),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ]
                    )
                )

                story.append(summary_table)
                story.append(Spacer(1, 14))

            pdf_rows = [
                [
                    Paragraph(str(header), small_style)
                    for header in current_export_headers
                ]
            ]

            for row in current_export_rows:
                pdf_rows.append(
                    [
                        Paragraph(str(value), small_style)
                        for value in row
                    ]
                )

            usable_width = landscape(A4)[0] - 48
            column_count = max(1, len(current_export_headers))
            column_width = usable_width / column_count

            data_table = Table(
                pdf_rows,
                repeatRows=1,
                colWidths=[column_width] * column_count
            )

            data_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.HexColor("#F8FAFC")]
                        ),
                        ("LEFTPADDING", (0, 0), (-1, -1), 4),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )

            story.append(data_table)
            story.append(Spacer(1, 12))

            story.append(
                Paragraph(
                    "Generated by Administrator • "
                    + datetime.now().strftime("%d %B %Y, %I:%M %p"),
                    small_style
                )
            )

            document.build(story)

            messagebox.showinfo(
                "PDF Export Complete",
                f"PDF report generated successfully.\n\n{file_path}",
                parent=parent
            )

        except Exception as error:
            messagebox.showerror(
                "PDF Export Error",
                f"Could not export the PDF report.\n\n"
                f"{type(error).__name__}: {error}",
                parent=parent
            )


    # ========================================================
    # ACTION BUTTONS
    # ========================================================

    Button(
        action_area,
        text="EXPORT PDF",
        bg=PURPLE,
        fg=WHITE,
        activebackground="#6D28D9",
        activeforeground=WHITE,
        bd=0,
        relief=FLAT,
        cursor="hand2",
        font=("Helvetica", 8, "bold"),
        command=export_pdf
    ).pack(side=RIGHT, padx=(8, 0), ipadx=14, ipady=8)

    Button(
        action_area,
        text="EXPORT CSV",
        bg=GREEN,
        fg=WHITE,
        activebackground="#15803D",
        activeforeground=WHITE,
        bd=0,
        relief=FLAT,
        cursor="hand2",
        font=("Helvetica", 8, "bold"),
        command=export_csv
    ).pack(side=RIGHT, ipadx=14, ipady=8)

    # ========================================================
    # FILTER RESET
    # ========================================================

    def reset_filters():
        search_var.set("")
        course_var.set("All Courses")
        status_var.set("All Status")
        mode_var.set("All Modes")
        academic_year_var.set("All Academic Years")
        from_date_var.set("")
        to_date_var.set("")
        accountant_var.set("All Accountants")
        report_period_var.set("This Month")

        show_report(active_report.get())

    def add_filter_buttons(container):
        button_box = Frame(container, bg="#F8FAFC")
        button_box.pack(side=RIGHT, padx=(10, 10), pady=12)

        Label(
            button_box,
            text=" ",
            bg="#F8FAFC",
            font=("Helvetica", 8)
        ).pack()

        Button(
            button_box,
            text="CLEAR",
            bg=WHITE,
            fg=TEXT,
            activebackground="#F1F5F9",
            relief=SOLID,
            bd=1,
            cursor="hand2",
            font=("Helvetica", 8, "bold"),
            command=reset_filters
        ).pack(side=RIGHT, ipadx=12, ipady=6)

        Button(
            button_box,
            text="SEARCH",
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            bd=0,
            cursor="hand2",
            font=("Helvetica", 8, "bold"),
            command=lambda: show_report(active_report.get())
        ).pack(side=RIGHT, padx=8, ipadx=13, ipady=7)

    # ========================================================
    # OVERVIEW REPORT
    # ========================================================

    def show_overview():
        clear_frame(filter_frame)

        report_title_var.set("Reports Overview")
        report_subtitle_var.set(
            "A summary of system-wide fee collection with quick access to detailed admin reports."
        )

        overview_filter_text = Label(
            filter_frame,
            text="Latest payment transactions are shown below. Use the report tabs for detailed analysis.",
            bg="#F8FAFC",
            fg=GRAY,
            font=("Helvetica", 9)
        )
        overview_filter_text.pack(anchor="w", padx=15, pady=16)

        try:
            records = fetch_all(
                """
                SELECT
                    fp.Payment_ID,
                    fp.Payment_Date,
                    r.Name,
                    sf.Registration_No,
                    sd.Course,
                    fp.Payment_Mode,
                    fp.Amount
                FROM fee_payments fp
                INNER JOIN student_fees sf
                    ON sf.Student_Fee_ID = fp.Student_Fee_ID
                INNER JOIN registration r
                    ON r.Registration_No = sf.Registration_No
                LEFT JOIN student_details sd
                    ON sd.Registration_No = sf.Registration_No
                ORDER BY
                    fp.Payment_Date DESC,
                    fp.Payment_ID DESC
                LIMIT 50
                """
            )

            rows = []

            for record in records:
                rows.append(
                    (
                        f"PAY-{int(record['Payment_ID']):06d}",
                        record["Payment_Date"],
                        record["Name"],
                        record["Registration_No"],
                        record["Course"] or "-",
                        record["Payment_Mode"],
                        money(record["Amount"])
                    )
                )

            create_table(
                ("payment_id", "date", "student", "reg_no", "course", "mode", "amount"),
                ("PAYMENT ID", "DATE", "STUDENT", "REG. NO", "COURSE", "MODE", "AMOUNT"),
                (110, 100, 170, 110, 190, 100, 120),
                rows,
                ("center", "center", "w", "center", "w", "center", "e")
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load the overview report.\n\n{error}",
                parent=parent
            )

    # ========================================================
    # COLLECTION REPORT
    # ========================================================

    def show_collection():
        clear_frame(filter_frame)

        report_title_var.set("Fee Collection Report")
        report_subtitle_var.set(
            "View all recorded fee payment transactions."
        )

        create_entry_filter(filter_frame, "SEARCH STUDENT / REG. NO", search_var, 25)
        create_entry_filter(filter_frame, "FROM DATE (YYYY-MM-DD)", from_date_var, 16)
        create_entry_filter(filter_frame, "TO DATE (YYYY-MM-DD)", to_date_var, 16)
        create_combo_filter(
            filter_frame,
            "PAYMENT MODE",
            mode_var,
            ["All Modes", "Cash", "UPI", "Card", "Bank Transfer", "Cheque", "Other"],
            16
        )
        add_filter_buttons(filter_frame)

        query = """
            SELECT
                fp.Payment_ID,
                fp.Payment_Date,
                r.Name,
                sf.Registration_No,
                sd.Course,
                fp.Payment_Mode,
                fp.Transaction_Reference,
                fp.Amount
            FROM fee_payments fp
            INNER JOIN student_fees sf
                ON sf.Student_Fee_ID = fp.Student_Fee_ID
            INNER JOIN registration r
                ON r.Registration_No = sf.Registration_No
            LEFT JOIN student_details sd
                ON sd.Registration_No = sf.Registration_No
            WHERE 1 = 1
        """

        params = []

        keyword = search_var.get().strip()

        if keyword:
            pattern = f"%{keyword}%"
            query += """
                AND
                (
                    r.Name LIKE %s
                    OR sf.Registration_No LIKE %s
                )
            """
            params.extend([pattern, pattern])

        if from_date_var.get().strip():
            query += " AND fp.Payment_Date >= %s"
            params.append(from_date_var.get().strip())

        if to_date_var.get().strip():
            query += " AND fp.Payment_Date <= %s"
            params.append(to_date_var.get().strip())

        if mode_var.get() != "All Modes":
            query += " AND fp.Payment_Mode = %s"
            params.append(mode_var.get())

        query += " ORDER BY fp.Payment_Date DESC, fp.Payment_ID DESC"

        try:
            records = fetch_all(query, tuple(params))

            rows = [
                (
                    f"PAY-{int(record['Payment_ID']):06d}",
                    record["Payment_Date"],
                    record["Name"],
                    record["Registration_No"],
                    record["Course"] or "-",
                    record["Payment_Mode"],
                    record["Transaction_Reference"] or "-",
                    money(record["Amount"])
                )
                for record in records
            ]

            create_table(
                ("payment", "date", "student", "reg", "course", "mode", "reference", "amount"),
                ("PAYMENT ID", "DATE", "STUDENT", "REG. NO", "COURSE", "MODE", "REFERENCE", "AMOUNT"),
                (105, 95, 160, 105, 170, 100, 150, 110),
                rows,
                ("center", "center", "w", "center", "w", "center", "w", "e")
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load the collection report.\n\n{error}",
                parent=parent
            )

    # ========================================================
    # OUTSTANDING REPORT
    # ========================================================

    def show_outstanding():
        clear_frame(filter_frame)

        report_title_var.set("Outstanding Dues Report")
        report_subtitle_var.set(
            "View students with unpaid or partially paid fee balances."
        )

        create_entry_filter(filter_frame, "SEARCH STUDENT / REG. NO", search_var, 26)
        create_combo_filter(filter_frame, "COURSE", course_var, course_values, 22)
        create_combo_filter(
            filter_frame,
            "STATUS",
            status_var,
            ["All Status", "Partial", "Unpaid", "Paid"],
            14
        )
        add_filter_buttons(filter_frame)

        query = """
            SELECT
                sf.Student_Fee_ID,
                sf.Registration_No,
                r.Name,
                sd.Course,
                sd.Semester,
                fs.Academic_Year,
                sf.Total_Fee,
                sf.Amount_Paid,
                sf.Due_Amount,
                sf.Payment_Status
            FROM student_fees sf
            INNER JOIN registration r
                ON r.Registration_No = sf.Registration_No
            LEFT JOIN student_details sd
                ON sd.Registration_No = sf.Registration_No
            INNER JOIN fee_structures fs
                ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
            WHERE 1 = 1
        """

        params = []

        keyword = search_var.get().strip()

        if keyword:
            pattern = f"%{keyword}%"
            query += """
                AND
                (
                    r.Name LIKE %s
                    OR sf.Registration_No LIKE %s
                )
            """
            params.extend([pattern, pattern])

        if course_var.get() != "All Courses":
            query += " AND sd.Course = %s"
            params.append(course_var.get())

        if status_var.get() == "All Status":
            query += " AND sf.Due_Amount > 0"
        else:
            query += " AND sf.Payment_Status = %s"
            params.append(status_var.get())

        query += " ORDER BY sf.Due_Amount DESC, r.Name"

        try:
            records = fetch_all(query, tuple(params))

            rows = [
                (
                    record["Registration_No"],
                    record["Name"],
                    record["Course"] or "-",
                    record["Semester"] or "-",
                    record["Academic_Year"],
                    money(record["Total_Fee"]),
                    money(record["Amount_Paid"]),
                    money(record["Due_Amount"]),
                    record["Payment_Status"]
                )
                for record in records
            ]

            create_table(
                ("reg", "student", "course", "semester", "year", "total", "paid", "due", "status"),
                ("REG. NO", "STUDENT", "COURSE", "SEM", "ACADEMIC YEAR", "TOTAL FEE", "PAID", "DUE", "STATUS"),
                (105, 160, 180, 70, 115, 110, 110, 110, 95),
                rows,
                ("center", "w", "w", "center", "center", "e", "e", "e", "center")
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load the outstanding report.\n\n{error}",
                parent=parent
            )

    # ========================================================
    # STUDENT REPORT
    # ========================================================

    def show_student_report():
        clear_frame(filter_frame)

        report_title_var.set("Student Fee Report")
        report_subtitle_var.set(
            "Search for a student and view the complete assigned fee summary."
        )

        create_entry_filter(filter_frame, "STUDENT NAME / REGISTRATION NO", search_var, 34)
        create_combo_filter(
            filter_frame,
            "PAYMENT STATUS",
            status_var,
            ["All Status", "Paid", "Partial", "Unpaid"],
            15
        )
        add_filter_buttons(filter_frame)

        query = """
            SELECT
                sf.Student_Fee_ID,
                sf.Registration_No,
                r.Name,
                sd.Course,
                sd.Semester,
                fs.Academic_Year,
                sf.Total_Fee,
                sf.Amount_Paid,
                sf.Due_Amount,
                sf.Payment_Status,
                sf.Assigned_At
            FROM student_fees sf
            INNER JOIN registration r
                ON r.Registration_No = sf.Registration_No
            LEFT JOIN student_details sd
                ON sd.Registration_No = sf.Registration_No
            INNER JOIN fee_structures fs
                ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
            WHERE 1 = 1
        """

        params = []

        keyword = search_var.get().strip()

        if keyword:
            pattern = f"%{keyword}%"
            query += """
                AND
                (
                    r.Name LIKE %s
                    OR sf.Registration_No LIKE %s
                )
            """
            params.extend([pattern, pattern])

        if status_var.get() != "All Status":
            query += " AND sf.Payment_Status = %s"
            params.append(status_var.get())

        query += " ORDER BY r.Name, fs.Academic_Year DESC"

        try:
            records = fetch_all(query, tuple(params))

            rows = [
                (
                    record["Registration_No"],
                    record["Name"],
                    record["Course"] or "-",
                    record["Semester"] or "-",
                    record["Academic_Year"],
                    money(record["Total_Fee"]),
                    money(record["Amount_Paid"]),
                    money(record["Due_Amount"]),
                    record["Payment_Status"]
                )
                for record in records
            ]

            create_table(
                ("reg", "student", "course", "sem", "year", "total", "paid", "due", "status"),
                ("REG. NO", "STUDENT", "COURSE", "SEM", "ACADEMIC YEAR", "TOTAL FEE", "PAID", "DUE", "STATUS"),
                (105, 170, 180, 70, 115, 110, 110, 110, 95),
                rows,
                ("center", "w", "w", "center", "center", "e", "e", "e", "center")
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load the student fee report.\n\n{error}",
                parent=parent
            )

    # ========================================================
    # COURSE REPORT
    # ========================================================

    def show_course_report():
        clear_frame(filter_frame)

        report_title_var.set("Course-Wise Fee Report")
        report_subtitle_var.set(
            "Compare assigned fees, collections and outstanding balances by course."
        )

        create_combo_filter(
            filter_frame,
            "ACADEMIC YEAR",
            academic_year_var,
            year_values,
            20
        )
        create_combo_filter(filter_frame, "COURSE", course_var, course_values, 24)
        add_filter_buttons(filter_frame)

        query = """
            SELECT
                sd.Course,
                fs.Academic_Year,
                COUNT(DISTINCT sf.Registration_No) AS Students,
                COALESCE(SUM(sf.Total_Fee), 0) AS Total_Fee,
                COALESCE(SUM(sf.Amount_Paid), 0) AS Amount_Paid,
                COALESCE(SUM(sf.Due_Amount), 0) AS Due_Amount
            FROM student_fees sf
            INNER JOIN student_details sd
                ON sd.Registration_No = sf.Registration_No
            INNER JOIN fee_structures fs
                ON fs.Fee_Structure_ID = sf.Fee_Structure_ID
            WHERE 1 = 1
        """

        params = []

        if academic_year_var.get() != "All Academic Years":
            query += " AND fs.Academic_Year = %s"
            params.append(academic_year_var.get())

        if course_var.get() != "All Courses":
            query += " AND sd.Course = %s"
            params.append(course_var.get())

        query += """
            GROUP BY
                sd.Course,
                fs.Academic_Year
            ORDER BY
                fs.Academic_Year DESC,
                sd.Course
        """

        try:
            records = fetch_all(query, tuple(params))

            rows = []

            for record in records:
                total = float(record["Total_Fee"] or 0)
                paid = float(record["Amount_Paid"] or 0)
                rate = (paid / total * 100) if total > 0 else 0

                rows.append(
                    (
                        record["Course"],
                        record["Academic_Year"],
                        record["Students"],
                        money(total),
                        money(paid),
                        money(record["Due_Amount"]),
                        f"{rate:.2f}%"
                    )
                )

            create_table(
                ("course", "year", "students", "total", "collected", "due", "rate"),
                ("COURSE", "ACADEMIC YEAR", "STUDENTS", "TOTAL FEES", "COLLECTED", "DUE", "RATE"),
                (220, 120, 90, 130, 130, 130, 90),
                rows,
                ("w", "center", "center", "e", "e", "e", "center")
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load the course-wise report.\n\n{error}",
                parent=parent
            )


    # ========================================================
    # ACCOUNTANT-WISE REPORT
    # ========================================================

    def apply_report_period(event=None):
        today = date.today()
        period = report_period_var.get()

        if period == "Today":
            start = today
            end = today

        elif period == "Last 7 Days":
            from datetime import timedelta
            start = today - timedelta(days=6)
            end = today

        elif period == "This Month":
            start = today.replace(day=1)
            end = today

        elif period == "This Year":
            start = today.replace(month=1, day=1)
            end = today

        elif period == "All Time":
            from_date_var.set("")
            to_date_var.set("")
            return

        else:
            return

        from_date_var.set(start.isoformat())
        to_date_var.set(end.isoformat())


    def validate_admin_report_dates():
        today = date.today()

        start_text = from_date_var.get().strip()
        end_text = to_date_var.get().strip()

        start_date = None
        end_date = None

        if start_text:
            try:
                start_date = date.fromisoformat(start_text)
            except ValueError:
                raise ValueError(
                    "From Date must use YYYY-MM-DD format."
                )

        if end_text:
            try:
                end_date = date.fromisoformat(end_text)
            except ValueError:
                raise ValueError(
                    "To Date must use YYYY-MM-DD format."
                )

        if start_date and end_date and start_date > end_date:
            raise ValueError(
                "From Date cannot be after To Date."
            )

        if end_date and end_date > today:
            raise ValueError(
                "To Date cannot be after today's date.\n\n"
                f"Today's Date: {today.isoformat()}"
            )


    def show_accountant_wise():
        clear_frame(filter_frame)

        report_title_var.set("Accountant-Wise Collection Report")
        report_subtitle_var.set(
            "Select an accountant and analyze only the payments collected by that user."
        )

        # Accountant selector
        accountant_box = Frame(filter_frame, bg="#F8FAFC")
        accountant_box.pack(side=LEFT, padx=(10, 10), pady=12)

        create_filter_label(accountant_box, "ACCOUNTANT")

        accountant_combo = ttk.Combobox(
            accountant_box,
            textvariable=accountant_var,
            values=accountant_values,
            state="readonly",
            width=28,
            font=("Helvetica", 9)
        )
        accountant_combo.pack(ipady=4)

        # Report period selector
        period_box = Frame(filter_frame, bg="#F8FAFC")
        period_box.pack(side=LEFT, padx=(0, 10), pady=12)

        create_filter_label(period_box, "REPORT PERIOD")

        period_combo = ttk.Combobox(
            period_box,
            textvariable=report_period_var,
            values=[
                "Today",
                "Last 7 Days",
                "This Month",
                "This Year",
                "All Time",
                "Custom Range"
            ],
            state="readonly",
            width=16,
            font=("Helvetica", 9)
        )
        period_combo.pack(ipady=4)
        period_combo.bind("<<ComboboxSelected>>", apply_report_period)

        create_entry_filter(
            filter_frame,
            "FROM DATE (YYYY-MM-DD)",
            from_date_var,
            15
        )

        create_entry_filter(
            filter_frame,
            "TO DATE (YYYY-MM-DD)",
            to_date_var,
            15
        )

        create_combo_filter(
            filter_frame,
            "PAYMENT MODE",
            mode_var,
            [
                "All Modes",
                "Cash",
                "UPI",
                "Card",
                "Bank Transfer",
                "Cheque",
                "Other"
            ],
            15
        )

        button_box = Frame(filter_frame, bg="#F8FAFC")
        button_box.pack(side=RIGHT, padx=(5, 10), pady=12)

        Label(
            button_box,
            text=" ",
            bg="#F8FAFC",
            font=("Helvetica", 8)
        ).pack()

        Button(
            button_box,
            text="CLEAR",
            bg=WHITE,
            fg=TEXT,
            activebackground="#F1F5F9",
            relief=SOLID,
            bd=1,
            cursor="hand2",
            font=("Helvetica", 8, "bold"),
            command=reset_filters
        ).pack(side=RIGHT, ipadx=10, ipady=6)

        Button(
            button_box,
            text="GENERATE REPORT",
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            bd=0,
            cursor="hand2",
            font=("Helvetica", 8, "bold"),
            command=lambda: load_accountant_report()
        ).pack(side=RIGHT, padx=8, ipadx=12, ipady=7)

        if report_period_var.get() != "Custom Range":
            apply_report_period()

        load_accountant_report()


    def load_accountant_report():
        try:
            validate_admin_report_dates()

            query = """
                SELECT
                    fp.Payment_ID,
                    fp.Payment_Date,
                    r.Name,
                    sf.Registration_No,
                    COALESCE(sd.Course, '-') AS Course,
                    COALESCE(fs.Semester, sd.Semester, '-') AS Semester,
                    fp.Payment_Mode,
                    COALESCE(fp.Transaction_Reference, '-') AS Transaction_Reference,
                    fp.Amount,
                    COALESCE(fp.Collected_By, '-') AS Collected_By
                FROM fee_payments fp

                INNER JOIN student_fees sf
                    ON sf.Student_Fee_ID = fp.Student_Fee_ID

                INNER JOIN registration r
                    ON r.Registration_No = sf.Registration_No

                LEFT JOIN student_details sd
                    ON sd.Registration_No = sf.Registration_No

                LEFT JOIN fee_structures fs
                    ON fs.Fee_Structure_ID = sf.Fee_Structure_ID

                WHERE 1 = 1
            """

            params = []

            if accountant_var.get() != "All Accountants":
                query += " AND TRIM(fp.Collected_By) = %s"
                params.append(accountant_var.get())

            if from_date_var.get().strip():
                query += " AND fp.Payment_Date >= %s"
                params.append(from_date_var.get().strip())

            if to_date_var.get().strip():
                query += " AND fp.Payment_Date <= %s"
                params.append(to_date_var.get().strip())

            if mode_var.get() != "All Modes":
                query += " AND fp.Payment_Mode = %s"
                params.append(mode_var.get())

            query += """
                ORDER BY
                    fp.Payment_Date DESC,
                    fp.Payment_ID DESC
            """

            records = fetch_all(
                query,
                tuple(params)
            )

            rows = []

            for record in records:
                semester = str(record["Semester"] or "-")

                if (
                    semester != "-"
                    and
                    not semester.lower().startswith("semester")
                ):
                    semester = f"Semester {semester}"

                rows.append(
                    (
                        f"PAY-{int(record['Payment_ID']):06d}",
                        record["Payment_Date"],
                        record["Name"],
                        record["Registration_No"],
                        record["Course"],
                        semester,
                        record["Payment_Mode"],
                        record["Transaction_Reference"],
                        record["Collected_By"],
                        money(record["Amount"])
                    )
                )

            create_table(
                (
                    "payment",
                    "date",
                    "student",
                    "reg",
                    "course",
                    "semester",
                    "mode",
                    "reference",
                    "collector",
                    "amount"
                ),
                (
                    "PAYMENT ID",
                    "DATE",
                    "STUDENT",
                    "REG. NO",
                    "COURSE",
                    "SEMESTER",
                    "MODE",
                    "REFERENCE",
                    "COLLECTED BY",
                    "AMOUNT"
                ),
                (
                    105,
                    95,
                    155,
                    105,
                    160,
                    95,
                    90,
                    130,
                    180,
                    110
                ),
                rows,
                (
                    "center",
                    "center",
                    "w",
                    "center",
                    "w",
                    "center",
                    "center",
                    "w",
                    "w",
                    "e"
                )
            )

        except ValueError as error:
            messagebox.showwarning(
                "Invalid Date",
                str(error),
                parent=parent
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load the accountant-wise report.\n\n{error}",
                parent=parent
            )



    # ========================================================
    # REPORT SWITCHING
    # ========================================================

    def update_tab_styles():
        for name, button in tab_buttons.items():
            if name == active_report.get():
                button.configure(
                    bg=BLUE,
                    fg=WHITE,
                    activebackground=DARK_BLUE,
                    activeforeground=WHITE
                )
            else:
                button.configure(
                    bg=WHITE,
                    fg=GRAY,
                    activebackground=LIGHT_BLUE,
                    activeforeground=BLUE
                )

    def show_report(report_name):
        active_report.set(report_name)
        update_tab_styles()

        try:
            if report_name == "Overview":
                show_overview()

            elif report_name == "Accountant-Wise":
                show_accountant_wise()

            elif report_name == "Collection":
                show_collection()

            elif report_name == "Outstanding":
                show_outstanding()

            elif report_name == "Student Report":
                show_student_report()

            elif report_name == "Course Report":
                show_course_report()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load the selected report.\n\n{error}",
                parent=parent
            )

    # --------------------------------------------------------
    # CREATE TABS
    # --------------------------------------------------------

    tab_names = [
        "Overview",
        "Accountant-Wise",
        "Collection",
        "Outstanding",
        "Student Report",
        "Course Report"
    ]

    for tab_name in tab_names:
        button = Button(
            tabs_frame,
            text=tab_name.upper(),
            bg=WHITE,
            fg=GRAY,
            activebackground=LIGHT_BLUE,
            activeforeground=BLUE,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            font=("Helvetica", 8, "bold"),
            command=lambda name=tab_name: show_report(name)
        )

        button.pack(
            side=LEFT,
            padx=3,
            ipadx=14,
            ipady=8
        )

        tab_buttons[tab_name] = button

    # ========================================================
    # INITIAL LOAD
    # ========================================================

    load_summary()
    show_report("Overview")


# ============================================================
# OPTIONAL STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    root = Tk()
    root.title("Reports Management")
    root.geometry("1400x800")
    root.minsize(1100, 650)
    root.configure(bg=BG)

    open_reports_management(
        root,
        current_role="Admin"
    )

    root.mainloop()
