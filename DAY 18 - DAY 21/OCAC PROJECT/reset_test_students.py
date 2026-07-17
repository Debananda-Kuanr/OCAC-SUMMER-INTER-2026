from datetime import date, timedelta
import json

import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "9439",
    "database": "OCAC_GROUP2",
}


MALE_FIRST = [
    "Aarav",
    "Arjun",
    "Aryan",
    "Dev",
    "Ishaan",
]

MALE_LAST = [
    "Das",
    "Nayak",
    "Patel",
    "Sahu",
    "Pradhan",
]

FEMALE_FIRST = [
    "Aanya",
    "Ananya",
    "Ishita",
    "Priya",
    "Riya",
]

FEMALE_LAST = [
    "Mishra",
    "Panda",
    "Behera",
    "Sahoo",
    "Jena",
]

SECURITY_QUESTIONS = [
    "What is your favourite color?",
    "What is the name of your first school?",
    "What is your favourite food?",
    "What is your favourite sport?",
    "What is the name of your childhood friend?",
]

PAYMENT_MODES = [
    "UPI",
    "Cash",
    "Card",
    "Net Banking",
]

COURSE_BASE = {
    "C001": 52000.00,
    "C002": 50000.00,
    "C003": 36000.00,
    "C004": 42000.00,
    "C005": 48000.00,
}


def build_name(gender, index):
    slot = (index - 1) % 25
    first_idx = slot % 5
    last_idx = slot // 5
    if gender == "Male":
        return f"{MALE_FIRST[first_idx]} {MALE_LAST[last_idx]}"
    return f"{FEMALE_FIRST[first_idx]} {FEMALE_LAST[last_idx]}"


def seeded_students():
    rows = []
    for index in range(1, 51):
        gender = "Male" if index <= 25 else "Female"
        name = build_name(gender, index)
        username = f"teststudent{index:02d}"
        password = "student123"
        if index == 1:
            name = "Debananda Kuanr"
            username = "debananda_99"
            password = "123456"
        reg_no = f"STU{index:05d}"
        question = SECURITY_QUESTIONS[(index - 1) % len(SECURITY_QUESTIONS)]
        answer = f"Answer {index:02d}"
        age = 18 + ((index - 1) % 7)
        phone = f"90000{index:05d}"[:10]
        email = f"{username}@example.com"

        rows.append(
            {
                "Registration_No": reg_no,
                "Name": name,
                "Username": username,
                "Password": password,
                "Security_Question": question,
                "Security_Answer": answer,
                "Gender": gender,
                "Age": age,
                "Phone": phone,
                "Email": email,
            }
        )

    return rows


def build_previous_data(row):
    return {
        "Name": row["Name"],
        "Username": row["Username"],
        "Password": row["Password"],
        "Security_Question": row["Security_Question"],
        "Security_Answer": row["Security_Answer"],
        "Course": row["Course"],
        "Semester": row["Semester"],
        "Admission_Year": row["Admission_Year"],
        "Email": row["Email"],
        "Age": row["Age"],
        "Gender": row["Gender"],
        "Phone": row["Phone"],
        "Status": row["Status"],
    }


def build_proposed_data(row, index):
    proposed = build_previous_data(row).copy()

    if index == 46:
        proposed["Phone"] = "9999912346"
        proposed["Admission_Year"] = "2027-28"
    elif index == 47:
        proposed["Course"] = "B.Tech CSE"
        proposed["Semester"] = 2
    elif index == 48:
        proposed["Email"] = "updated48@example.com"
        proposed["Phone"] = "9999912348"
    elif index == 49:
        proposed["Name"] = "Changed Name 49"
        proposed["Username"] = "changeduser49"
        proposed["Security_Answer"] = "Updated Answer 49"
    elif index == 50:
        proposed["Age"] = 24
        proposed["Gender"] = "Female"
        proposed["Admission_Year"] = "2028-29"

    proposed["Status"] = "Pending Approval"
    return proposed


def payment_patterns_for(index, total_fee, today, yesterday, two_days_ago):
    if index == 1:
        part1 = round(total_fee * 0.20, 2)
        part2 = round(total_fee * 0.20, 2)
        part3 = round(total_fee * 0.20, 2)
        part4 = round(total_fee * 0.20, 2)
        part5 = round(total_fee - part1 - part2 - part3 - part4, 2)
        return {
            "status": "Partial",
            "amount_paid": round(part1 + part2 + part3 + part4 + part5, 2),
            "payments": [
                (part1, "Installment 1", two_days_ago),
                (part2, "Installment 2", two_days_ago),
                (part3, "Installment 3", yesterday),
                (part4, "Installment 4", yesterday),
                (part5, "Installment 5", today),
            ],
        }

    pattern = (index - 1) % 5

    if pattern == 0:
        return {
            "status": "Paid",
            "amount_paid": total_fee,
            "payments": [(total_fee, "Full fee paid", today)],
        }

    if pattern == 1:
        first_payment = round(total_fee * 0.40, 2)
        second_payment = round(total_fee - first_payment, 2)
        return {
            "status": "Partial",
            "amount_paid": round(first_payment + second_payment, 2),
            "payments": [
                (first_payment, "Part payment - installment 1", two_days_ago),
                (second_payment, "Part payment - installment 2", today),
            ],
        }

    if pattern == 2:
        first_payment = round(total_fee * 0.30, 2)
        second_payment = round(total_fee * 0.35, 2)
        third_payment = round(total_fee - first_payment - second_payment, 2)
        return {
            "status": "Partial",
            "amount_paid": round(first_payment + second_payment + third_payment, 2),
            "payments": [
                (first_payment, "Part payment - installment 1", two_days_ago),
                (second_payment, "Part payment - installment 2", yesterday),
                (third_payment, "Part payment - installment 3", today),
            ],
        }

    if pattern == 3:
        return {
            "status": "Unpaid",
            "amount_paid": 0.0,
            "payments": [],
        }

    first_payment = round(total_fee * 0.55, 2)
    second_payment = round(total_fee * 0.25, 2)
    return {
        "status": "Partial",
        "amount_paid": round(first_payment + second_payment, 2),
        "payments": [
            (first_payment, "Advance payment", yesterday),
            (second_payment, "Balance payment", today),
        ],
    }


def accountant_cycle(accountants, index):
    if not accountants:
        return "Debananda Kuanr"
    return accountants[index % len(accountants)]


def main():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                fs.Fee_Structure_ID,
                fs.Course_ID,
                c.Course_Name,
                fs.Semester,
                fs.Academic_Year
            FROM fee_structures fs
            INNER JOIN courses c
                ON c.Course_ID = fs.Course_ID
            WHERE LOWER(TRIM(fs.Status)) = 'active'
            ORDER BY fs.Fee_Structure_ID ASC
            """
        )
        fee_structures = cursor.fetchall()
        if not fee_structures:
            raise RuntimeError("No active fee structures were found.")

        cursor.execute(
            """
            SELECT Name
            FROM registration
            WHERE LOWER(TRIM(Role)) = 'accountant'
            ORDER BY Name ASC
            """
        )
        accountants = [row["Name"] for row in cursor.fetchall()]
        if len(accountants) < 3:
            accountants = ["Debananda Kuanr", "Vijay Nayak", "Vikash Sahu"]

        today = date.today()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)

        student_rows = seeded_students()
        detail_rows = []
        fee_rows = []
        payment_rows = []
        request_rows = []

        cursor.execute(
            """
            DELETE fp
            FROM fee_payments fp
            INNER JOIN student_fees sf
                ON sf.Student_Fee_ID = fp.Student_Fee_ID
            """
        )
        cursor.execute("DELETE FROM student_fees")
        cursor.execute("DELETE FROM student_approval_requests")
        cursor.execute("DELETE FROM student_details")
        cursor.execute(
            """
            DELETE FROM registration
            WHERE LOWER(TRIM(Role)) = 'student'
            """
        )

        for index, row in enumerate(student_rows, start=1):
            if index == 1:
                fee_row = next(
                    (
                        item
                        for item in fee_structures
                        if str(item["Course_Name"]).strip().lower() == "bca"
                        and int(item["Semester"]) == 1
                    ),
                    fee_structures[0],
                )
            else:
                fee_row = fee_structures[(index - 1) % len(fee_structures)]
            course_id = fee_row["Course_ID"]
            course_name = fee_row["Course_Name"]
            semester = int(fee_row["Semester"])
            academic_year = str(fee_row["Academic_Year"])
            total_fee = float(COURSE_BASE.get(course_id, 40000.00) + (semester * 1250.00))

            payment_state = payment_patterns_for(
                index,
                total_fee,
                today,
                yesterday,
                two_days_ago,
            )

            if index <= 30:
                status = "Active"
            elif index <= 40:
                status = "Inactive"
            else:
                status = "Pending Approval"

            detail_rows.append(
                (
                    row["Registration_No"],
                    course_name,
                    semester,
                    academic_year,
                    row["Email"],
                    row["Age"],
                    row["Gender"],
                    row["Phone"],
                    status,
                )
            )

            fee_rows.append(
                (
                    row["Registration_No"],
                    fee_row["Fee_Structure_ID"],
                    total_fee,
                    payment_state["amount_paid"],
                    round(total_fee - payment_state["amount_paid"], 2),
                    payment_state["status"],
                )
            )

            cursor.execute(
                """
                INSERT INTO registration
                (
                    Registration_No,
                    Name,
                    Username,
                    Password,
                    Security_Question,
                    Security_Answer,
                    Role
                )
                VALUES
                (%s, %s, %s, %s, %s, %s, 'Student')
                """,
                (
                    row["Registration_No"],
                    row["Name"],
                    row["Username"],
                    row["Password"],
                    row["Security_Question"],
                    row["Security_Answer"],
                ),
            )

            if index >= 41:
                request_type = "new_student" if index <= 45 else "profile_update"
                current_snapshot = {
                    "Name": row["Name"],
                    "Username": row["Username"],
                    "Password": row["Password"],
                    "Security_Question": row["Security_Question"],
                    "Security_Answer": row["Security_Answer"],
                    "Course": course_name,
                    "Semester": semester,
                    "Admission_Year": academic_year,
                    "Email": row["Email"],
                    "Age": row["Age"],
                    "Gender": row["Gender"],
                    "Phone": row["Phone"],
                    "Status": status,
                }
                if request_type == "new_student":
                    previous_snapshot = {
                        "Name": "",
                        "Username": "",
                        "Password": "",
                        "Security_Question": "",
                        "Security_Answer": "",
                        "Course": "",
                        "Semester": "",
                        "Admission_Year": "",
                        "Email": "",
                        "Age": "",
                        "Gender": "",
                        "Phone": "",
                        "Status": "",
                    }
                    proposed_snapshot = current_snapshot.copy()
                else:
                    previous_snapshot = build_previous_data(current_snapshot)
                    proposed_snapshot = build_proposed_data(current_snapshot, index)

                request_rows.append(
                    (
                        row["Registration_No"],
                        request_type,
                        row["Name"],
                        row["Username"],
                        json.dumps(previous_snapshot, ensure_ascii=True),
                        json.dumps(proposed_snapshot, ensure_ascii=True),
                        "Pending",
                    )
                )

            collector_base = (index - 1) % len(accountants)
            for payment_index, payment in enumerate(payment_state["payments"]):
                amount, remarks, payment_date = payment
                payment_rows.append(
                    (
                        row["Registration_No"],
                        amount,
                        PAYMENT_MODES[(index + payment_index - 1) % len(PAYMENT_MODES)],
                        f"PAY{index:05d}{chr(65 + payment_index)}",
                        remarks,
                        accountant_cycle(accountants, collector_base + payment_index),
                        payment_date,
                    )
                )

        cursor.executemany(
            """
            INSERT INTO student_details
            (
                Registration_No,
                Course,
                Semester,
                Admission_Year,
                Email,
                Age,
                Gender,
                Phone,
                Status
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            detail_rows,
        )

        cursor.executemany(
            """
            INSERT INTO student_fees
            (
                Registration_No,
                Fee_Structure_ID,
                Total_Fee,
                Amount_Paid,
                Due_Amount,
                Payment_Status
            )
            VALUES
            (%s, %s, %s, %s, %s, %s)
            """,
            fee_rows,
        )

        cursor.execute(
            """
            SELECT Student_Fee_ID, Registration_No
            FROM student_fees
            ORDER BY Student_Fee_ID ASC
            """
        )
        fee_id_by_reg = {
            row["Registration_No"]: row["Student_Fee_ID"]
            for row in cursor.fetchall()
        }

        payment_insert_rows = []
        for payment in payment_rows:
            reg_no = payment[0]
            fee_id = fee_id_by_reg[reg_no]
            payment_insert_rows.append(
                (
                    fee_id,
                    payment[1],
                    payment[2],
                    payment[3],
                    payment[4],
                    payment[5],
                    payment[6],
                )
            )

        cursor.executemany(
            """
            INSERT INTO fee_payments
            (
                Student_Fee_ID,
                Amount,
                Payment_Mode,
                Transaction_Reference,
                Remarks,
                Collected_By,
                Payment_Date
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            """,
            payment_insert_rows,
        )

        cursor.executemany(
            """
            INSERT INTO student_approval_requests
            (
                Registration_No,
                Request_Type,
                Student_Name,
                Username,
                Previous_Data,
                Proposed_Data,
                Status
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            """,
            request_rows,
        )

        connection.commit()

        print("Reset complete.")
        print("Students inserted: 50")
        print("Payment history inserted with 5 distinct patterns.")
        print("Approval requests inserted: 10")
        print(f"Login student: debananda_99 / 123456")
        print(f"Payment date max: {today.isoformat()}")
        print("Accountant collectors used:", ", ".join(accountants[:3]))

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
