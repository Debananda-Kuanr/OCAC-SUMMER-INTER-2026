# Fee Status Management System

## All Page Design Blueprint

This file defines how every page of the application should look and behave. The goal is a clean, premium, professional desktop GUI for Python and MySQL.

---

## Global UI Rules

- Use a fixed left sidebar for dashboards
- Use a top bar for search, profile, and logout
- Use soft shadows and rounded cards
- Use SVG icons only
- Use readable spacing and strong alignment
- Use one primary color system across all pages
- Keep action buttons consistent
- Use tables for records and cards for summaries

---

## 1. Splash Screen

### Purpose
Show branding while the app loads.

### Layout
```
----------------------------------------------------
|                                                  |
|                    LOGO                          |
|             Fee Status Management                |
|          Smart Fee Tracking System               |
|                                                  |
|               Loading Progress                   |
|                                                  |
----------------------------------------------------
```

### Design Notes
- Centered logo and app name
- Dark or gradient background
- Minimal text
- Smooth loading animation

---

## 2. Login Page

### Purpose
Allow users to access the system.

### Layout
```
---------------------------------------------------------------
| BRAND PANEL                 |           LOGIN PANEL         |
|-----------------------------|--------------------------------|
| Logo                        | Username / Email               |
| App Name                    | Password                       |
| Short tagline               | Role Selection                 |
| Illustration / Pattern      | [ Login Button ]               |
|                              | Forgot Password                |
|                              | Register New Account           |
---------------------------------------------------------------
```

### Design Notes
- Left panel for branding
- Right panel for form
- Role dropdown or role auto-detect
- Clean button hover effect
- Clear error messages

---

## 3. Registration Page

### Purpose
Create new user accounts.

### Layout
```
---------------------------------------------------------------
| Registration Form                                           |
|-------------------------------------------------------------|
| Full Name      | Email                                      |
| Mobile No.     | Username                                   |
| Password       | Confirm Password                            |
| Role Selection | [ Register Button ]                         |
|-------------------------------------------------------------|
| Already have an account? Login                              |
---------------------------------------------------------------
```

### Design Notes
- Use two-column form
- Include validation hints
- Show password strength or basic checks
- Use a card centered on the page

---

## 4. Forgot Password Page

### Purpose
Recover access through registered email or username.

### Layout
```
----------------------------------------------
| Forgot Password                            |
|--------------------------------------------|
| Enter Email / Username                     |
| [ Send Reset Link / OTP ]                  |
| Verification Code                          |
| New Password                               |
| Confirm Password                           |
| [ Reset Password ]                         |
----------------------------------------------
```

### Design Notes
- Keep the page simple
- Show step-by-step recovery fields
- Use friendly instructions

---

## 5. Change Password Page

### Purpose
Let logged-in users update their password.

### Layout
```
----------------------------------------------
| Change Password                            |
|--------------------------------------------|
| Current Password                           |
| New Password                               |
| Confirm New Password                       |
| [ Update Password ]                        |
----------------------------------------------
```

### Design Notes
- Compact form
- Security-focused styling
- Clear success message after update

---

## 6. Admin Dashboard

### Purpose
Give admin full control over the system.

### Layout
```
--------------------------------------------------------------------------------
| Top Bar: Logo |                                                | Logout      |
--------------------------------------------------------------------------------
| Sidebar      | Stat 1 | Stat 2 | Stat 3 | Stat 4                             |
|--------------|---------------------------------------------------------------|
| Dashboard    |                     Collection Summary                        |
| Users        |---------------------------------------------------------------|
| Students     | Recent Activity Table                                         |
| Courses      | Pending Fees List                                             |
| Fees         | Quick Actions                                                 |
| Reports      |                                                               |
| Change Pass  |                                                               |
--------------------------------------------------------------------------------
```

### Dashboard Cards
- Total Students
- Total Paid
- Total Pending
- Monthly Collection

### Design Notes
- Sidebar stays fixed
- Main area uses cards and charts
- Tables show recent records
- Quick action buttons for common admin tasks

---

## 7. Accountant Dashboard

### Purpose
Handle student fee records and payments.

### Layout
```
--------------------------------------------------------------------------------
| Top Bar: Search | Profile | Logout                                          |
--------------------------------------------------------------------------------
| Sidebar      | Search Student Panel                                          |
|--------------|---------------------------------------------------------------|
| Dashboard    | Student Detail Card | Payment Form                           |
| Students     |---------------------------------------------------------------|
| Payments     | Payment History Table                                        |
| Receipts     | Due List / Pending List                                      |
| Reports      |                                                               |
--------------------------------------------------------------------------------
```

### Design Notes
- Search first workflow
- Strong focus on payment entry
- Student summary visible beside form
- Receipt and save actions clearly separated

---

## 8. Student Dashboard

### Purpose
Let students view fee status and history.

### Layout
```
--------------------------------------------------------------------------------
| Top Bar: Logo | Profile | Logout                                            |
--------------------------------------------------------------------------------
| Sidebar      | Profile Summary Card                                         |
|--------------|---------------------------------------------------------------|
| Dashboard    | Fee Status Card | Payment Summary Card                       |
| Fee Status   |---------------------------------------------------------------|
| History      | Payment History Table                                        |
| Profile      | Download Receipt Button                                      |
--------------------------------------------------------------------------------
```

### Design Notes
- Simple and clean
- Only relevant information
- Status badges for payment state
- Easy-to-read cards

---

## 9. Manage Users Page

### Purpose
Admin manages all login accounts.

### Layout
```
--------------------------------------------------------------------------------
| Manage Users                                                                  |
| [Add User] [Edit] [Delete] [Search Box]                                      |
|------------------------------------------------------------------------------|
| User Table: Name | Email | Username | Role | Status | Actions                |
--------------------------------------------------------------------------------
```

### Design Notes
- Use table with actions
- Include filters by role
- Status badge for active/inactive

---

## 10. Manage Students Page

### Purpose
Add, edit, search, and view students.

### Layout
```
--------------------------------------------------------------------------------
| Manage Students                                                               |
| [Add Student] [Update] [Delete] [Search Box]                                 |
|------------------------------------------------------------------------------|
| Student Form / Detail Panel                                                  |
|------------------------------------------------------------------------------|
| Student Table: ID | Name | Course | Fee | Paid | Pending | Status | Actions  |
--------------------------------------------------------------------------------
```

### Design Notes
- Form and table can be side by side
- Use strong data alignment
- Include auto-calculated fee fields

---

## 11. Student Details Page

### Purpose
Show one student record in detail.

### Layout
```
---------------------------------------------------------------
| Student Profile Summary                                     |
|-------------------------------------------------------------|
| Photo | Name | ID | Course | Contact | Email                |
|-------------------------------------------------------------|
| Fee Summary: Total | Paid | Pending | Status                |
|-------------------------------------------------------------|
| Payment History Table                                        |
---------------------------------------------------------------
```

### Design Notes
- Profile style layout
- Clean summary cards
- Good for viewing before payment update

---

## 12. Manage Courses Page

### Purpose
Add and maintain course fee structures.

### Layout
```
---------------------------------------------------------------
| Manage Courses                                              |
| [Add Course] [Edit] [Delete] [Search]                       |
|-------------------------------------------------------------|
| Course Form                                                 |
|-------------------------------------------------------------|
| Course Table: Course Name | Duration | Fee | Status        |
---------------------------------------------------------------
```

### Design Notes
- Straightforward admin panel
- Keep course fee fields clear

---

## 13. Payment Entry Page

### Purpose
Record student fee payments.

### Layout
```
--------------------------------------------------------------------------------
| Payment Entry                                                                 |
|------------------------------------------------------------------------------|
| Search Student by ID / Name / Mobile                                         |
|------------------------------------------------------------------------------|
| Student Info Card | Fee Entry Form | Payment Summary                         |
|------------------------------------------------------------------------------|
| Payment Table                                                               |
| [Save Payment] [Print Receipt] [Clear]                                       |
--------------------------------------------------------------------------------
```

### Design Notes
- Make the payment form prominent
- Show live calculations
- Receipt button placed after save

---

## 14. Fee Status Page

### Purpose
Show current payment condition.

### Layout
```
---------------------------------------------------------------
| Fee Status                                                  |
|-------------------------------------------------------------|
| Total Fee | Paid Amount | Pending Amount | Status Badge    |
|-------------------------------------------------------------|
| Payment Progress Bar                                        |
|-------------------------------------------------------------|
| Payment History                                             |
---------------------------------------------------------------
```

### Design Notes
- Use visual progress bar
- Show status in color-coded badge
- Clean KPI-style presentation

---

## 15. Payment History Page

### Purpose
Display all fee transactions.

### Layout
```
---------------------------------------------------------------
| Payment History                                             |
|-------------------------------------------------------------|
| Filters: Date | Student | Course | Status                  |
|-------------------------------------------------------------|
| Table: Receipt No | Date | Amount | Mode | Status | Action |
---------------------------------------------------------------
```

### Design Notes
- Table-focused page
- Add filters at top
- Export button can be placed on top right

---

## 16. Receipt Page

### Purpose
Generate payment receipt.

### Layout
```
---------------------------------------------------------------
| Receipt                                                     |
|-------------------------------------------------------------|
| Institute Name                                              |
| Student Name | ID | Course | Receipt No                    |
|-------------------------------------------------------------|
| Total Fee | Paid Amount | Pending Amount                   |
| Payment Date | Mode | Remarks                              |
|-------------------------------------------------------------|
| [Print] [Download PDF]                                      |
---------------------------------------------------------------
```

### Design Notes
- Receipt should look formal
- Use print-friendly layout
- Include branding and signature space

---

## 17. Reports Page

### Purpose
View fee and collection summaries.

### Layout
```
--------------------------------------------------------------------------------
| Reports                                                                       |
|------------------------------------------------------------------------------|
| Report Cards: Total Collection | Pending Due | Paid Students | Partial       |
|------------------------------------------------------------------------------|
| Chart Area                                                                    |
|------------------------------------------------------------------------------|
| Report Table                                                                  |                                        |
--------------------------------------------------------------------------------
```

### Design Notes
- Visual charts on top
- Table below for details
- Export actions clearly visible

---

## 18. Pending Due List Page

### Purpose
Show students who still owe fees.

### Layout
```
---------------------------------------------------------------
| Pending Due List                                            |
|-------------------------------------------------------------|
| Search | Filter by Course | Filter by Status               |
|-------------------------------------------------------------|
| Table: Student | Total Fee | Paid | Pending | Action       |
---------------------------------------------------------------
```

### Design Notes
- Use red or amber status badges
- Designed for quick follow-up work

---

## 19. Profile Page

### Purpose
Let users view and update their profile.

### Layout
```
---------------------------------------------------------------
| Profile                                                    |
|-------------------------------------------------------------|
| Avatar | Name | Email | Mobile | Role                       |
|-------------------------------------------------------------|
| Edit Profile Form                                           |
|-------------------------------------------------------------|
| [Save Changes]                                              |
---------------------------------------------------------------
```

### Design Notes
- Minimal and personal
- Show editable fields in a clean card

---

```

### Design Notes
- Group settings in sections
- Avoid clutter
- Use toggles and simple inputs

---

## 21. Logout Confirmation Modal

### Purpose
Confirm the user wants to exit.

### Layout
```
-------------------------------------
| Confirm Logout                    |
|-----------------------------------|
| Do you want to logout now?        |
| [Cancel] [Logout]                 |
-------------------------------------
```

---

## 22. Common Page Components

Every page should reuse these elements:

- Sidebar navigation
- Top bar
- Breadcrumb
- Search box
- Stat cards
- Data table
- Form card
- Modal dialog
- Toast notification
- Status badge

---

## 23. Color and Style System

Suggested style direction:

- Primary: navy blue
- Accent: teal
- Success: green
- Warning: amber
- Danger: red
- Background: off-white or soft gray
- Cards: white with subtle shadow
- Borders: light and thin

Typography:
- Use clean sans-serif fonts
- Keep headings bold
- Keep body text readable

Spacing:
- Use generous padding
- Align elements consistently
- Avoid crowded screens

---

## 24. Visual Priority

The pages should feel like:

1. premium school ERP software
2. professional fee management dashboard
3. real commercial desktop product
4. not a student-style demo

---

## 25. Final Page Set

If you build the complete project, the app should include at least these pages:


- Login
- Register
- Forgot Password
- Change Password
- Admin Dashboard
- Accountant Dashboard
- Student Dashboard
- Manage Users
- Manage Students
- Student Details
- Manage Courses
- Payment Entry
- Fee Status
- Payment History
- Receipt
- Reports
- Pending Due List
- Profile
- Settings
- Logout Confirmation

