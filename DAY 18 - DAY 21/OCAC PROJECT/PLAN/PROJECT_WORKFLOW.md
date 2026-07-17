# Fee Status Management System

## How the Project Works

This is a GUI-based Python and MySQL desktop application for managing student fee records in a school or college.

The system helps the institution:
- register users
- manage student fee details
- track paid and pending amounts
- update payment status
- generate reports
- control access by role

The application is designed for three user roles:

1. Admin
2. Student
3. Fee Management Staff / Accountant

---

## Common Features

All users will have access to:
- Registration
- Login
- Logout
- Forgot Password
- Change Password

---

## Project Working Flow

### 1. User Registration
New users create an account by entering their basic details such as:
- name
- email
- mobile number
- username
- password
- role

The data is saved in the MySQL database after validation.

### 2. User Login
The user enters username and password.
The system checks the database and opens the correct dashboard based on the role.

### 3. Role-Based Dashboard

#### Admin
The admin manages the full system:
- view all students
- manage staff accounts
- manage courses
- check fee reports
- monitor total collections
- view pending dues

#### Student
The student can:
- view personal profile
- view fee status
- see paid amount
- see pending amount
- view payment history
- download receipt if available

#### Fee Management Staff / Accountant
The accountant can:
- search student records
- add payment details
- update partial payments
- calculate pending amount automatically
- generate fee receipt
- view fee collection status

### 4. Fee Management
When a student pays fees:
- the staff enters the paid amount
- the system compares it with the total fee
- the remaining amount is calculated automatically
- fee status is updated as:
  - Paid
  - Partial
  - Pending

### 5. Report Generation
The system can display and generate:
- student-wise fee report
- pending fee report
- total collection report
- monthly payment report
- course-wise fee summary

---

## Database Concept

The project will use MySQL tables such as:
- `users` for login and role data
- `students` for student information
- `payments` for transaction history
- `courses` for course details
- `password_reset` for forgot password support

---

## Suggested Screens

- Splash Screen
- Login Screen
- Registration Screen
- Forgot Password Screen
- Admin Dashboard
- Student Dashboard
- Accountant Dashboard
- Student List Screen
- Payment Entry Screen
- Reports Screen
- Settings Screen

---

## Simple Working Example

1. A student registers or is added by the admin.
2. The accountant searches the student record.
3. The total fee is already stored in the database.
4. The accountant enters the paid amount.
5. The system calculates the pending balance automatically.
6. The fee status changes based on the payment.
7. The student can later log in and view the updated fee status.

---

## Project Goal

The main goal of this project is to replace manual fee tracking with a fast, secure, and organized digital system that reduces errors and saves time.

---

## Technologies Used

- Python
- MySQL
- Tkinter or CustomTkinter
- Pillow for images
- ttk Treeview for tables

---

## Conclusion

This project is a complete fee management solution for schools and colleges. It supports role-based access, fee tracking, payment updates, and report generation in a simple GUI desktop application.

