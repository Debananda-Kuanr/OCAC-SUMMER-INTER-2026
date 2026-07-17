# Fee Status Management System

## File Creation Plan

This document explains how the project files will be organized for a GUI-based Python and MySQL application.

The goal is to build a real production-style desktop system with clean separation of code, database scripts, UI screens, business logic, and reusable components.

The structure below is designed for a project with minimum 25 to 30 files so it stays modular, maintainable, and easy to present in college or internship work.

---

## What We Learned and How It Fits

This project should reflect the common Python and database concepts usually learned in a practical training program:

- Python syntax and program structure
- Functions and modules
- Object-oriented programming
- File organization
- GUI development
- MySQL database design
- CRUD operations
- Login and role-based access
- Form validation
- Report generation
- Error handling

The project should use these ideas in a real working application instead of a simple demo.

---

## Main Application Areas

The system will be divided into these parts:

1. Authentication
2. Admin panel
3. Student panel
4. Accountant panel
5. Database layer
6. UI components
7. Reports and utilities

---

## Recommended File Structure

### Root Files

1. `main.py`
   - Starts the application
   - Loads the first screen

2. `config.py`
   - Stores constants
   - Holds database credentials and app settings

3. `requirements.txt`
   - Lists Python dependencies

4. `README.md`
   - Project overview and setup guide

---

### Database and SQL Files

5. `database/schema.sql`
   - Creates all tables
   - Builds the full database structure

6. `database/seed_admin.sql`
   - Inserts default admin account

7. `database/seed_courses.sql`
   - Adds sample courses or fee structures

8. `database/seed_students.sql`
   - Adds sample student records for testing

9. `database/triggers.sql`
   - Optional triggers for automatic updates

10. `database/views.sql`
    - Optional SQL views for reports

11. `database/indexes.sql`
    - Adds performance indexes

12. `database/reset_password.sql`
    - SQL support for password reset tokens

---

### Application Package

13. `app/__init__.py`
    - Marks app as a Python package

14. `app/db.py`
    - MySQL connection handling

15. `app/helpers.py`
    - Shared helper functions

16. `app/constants.py`
    - Common values and role names

17. `app/validators.py`
    - Form validation logic

18. `app/security.py`
    - Password hashing and security checks

---

### Authentication Files

19. `app/auth/login.py`
    - Login screen and login logic

20. `app/auth/register.py`
    - Registration screen

21. `app/auth/forgot_password.py`
    - Password recovery screen

22. `app/auth/change_password.py`
    - Change password screen

23. `app/auth/logout.py`
    - Logout handling

---

### Dashboard Files

24. `app/dashboards/admin_dashboard.py`
    - Admin home screen

25. `app/dashboards/student_dashboard.py`
    - Student home screen

26. `app/dashboards/accountant_dashboard.py`
    - Fee staff home screen

---

### Student and Fee Management Files

27. `app/students/student_form.py`
    - Add and update student data

28. `app/students/student_list.py`
    - Show all students in table form

29. `app/students/student_details.py`
    - View a single student profile

30. `app/fees/payment_entry.py`
    - Add payment records

31. `app/fees/payment_history.py`
    - Show all payment transactions

32. `app/fees/fee_status.py`
    - Calculate paid, partial, and pending status

33. `app/fees/receipt.py`
    - Generate payment receipt

---

### Course and Report Files

34. `app/courses/course_form.py`
    - Add or edit course details

35. `app/courses/course_list.py`
    - Manage course records

36. `app/reports/fee_report.py`
    - Student fee report

37. `app/reports/collection_report.py`
    - Monthly collection report

38. `app/reports/due_report.py`
    - Pending dues report

39. `app/reports/export_report.py`
    - Export report to file

---

### UI and Utility Files

40. `app/ui/sidebar.py`
    - Left navigation panel

41. `app/ui/navbar.py`
    - Top navigation bar

42. `app/ui/cards.py`
    - Dashboard stat cards

43. `app/ui/table_view.py`
    - Reusable table widget

44. `app/ui/forms.py`
    - Reusable input form widgets

45. `app/ui/dialogs.py`
    - Confirmation and alert dialogs

46. `app/ui/theme.py`
    - Colors, fonts, and theme settings

---

### Asset Files

47. `assets/images/logo.png`
    - Application logo

48. `assets/images/background.png`
    - Login or dashboard background

49. `assets/icons/`
    - SVG icons for buttons and menus

50. `assets/fonts/`
    - Optional custom fonts

---

## Minimum SQL Files to Create

For a proper project, the SQL section should include at least these files:

1. `schema.sql`
2. `seed_admin.sql`
3. `seed_courses.sql`
4. `seed_students.sql`
5. `triggers.sql`
6. `views.sql`
7. `indexes.sql`
8. `reset_password.sql`

If you want a simpler version, the minimum must still include:

- one schema file
- one seed file
- one reset-password file

---

## Suggested Database Tables

The `schema.sql` file should create these tables:

- `users`
- `students`
- `courses`
- `payments`
- `payment_receipts`
- `password_resets`
- `audit_logs`
- `notifications`
- `settings`

Optional tables if needed:

- `roles`
- `sessions`
- `fee_history`
- `student_documents`

---

## How the Files Will Work Together

### Step 1: Start Application
`main.py` loads the GUI and opens the login screen.

### Step 2: Authentication
`login.py`, `register.py`, `forgot_password.py`, and `change_password.py` handle user access.

### Step 3: Load Dashboard
After login, the system opens the correct dashboard based on role.

### Step 4: Manage Students
Student data is inserted, updated, searched, and displayed using the student files.

### Step 5: Manage Fees
Fee entry files calculate paid amount and pending balance.

### Step 6: Generate Reports
Report files pull MySQL data and show summaries on screen.

### Step 7: Store and Query Data
`db.py` connects to MySQL and handles all database operations.

---

## Recommended Final Count

This structure gives you:
- 10 database/SQL and configuration files
- 8 authentication and dashboard files
- 8 student, fee, and report files
- 7 UI and utility files
- 3 asset folders

That makes the project look complete, scalable, and professional.

---

## Conclusion

This file plan is suitable for a real GUI-based school or college fee management system. It supports the technology you learned, keeps the code organized, and creates a proper foundation for a production-style Python and MySQL desktop application.

