# Fee Status Management System

## Flow Diagram and UI Design Blueprint

This document shows how the system should work and how the UI should look for a professional GUI-based Python and MySQL project.

---

## 1. Overall System Flow

```mermaid
flowchart TD
    A[Start Application] --> B[Splash Screen]
    B --> C[Login / Register]
    C --> D{User Role}
    D -->|Admin| E[Admin Dashboard]
    D -->|Student| F[Student Dashboard]
    D -->|Accountant| G[Accountant Dashboard]
    E --> H[Manage Users]
    E --> I[Manage Students]
    E --> J[Manage Courses]
    E --> K[View Reports]
    F --> L[View Fee Status]
    F --> M[View Payment History]
    F --> N[Download Receipt]
    G --> O[Search Student]
    G --> P[Add / Update Payment]
    G --> Q[Generate Receipt]
    G --> R[View Due List]
```

---

## 2. Login to Dashboard Flow

```mermaid
flowchart TD
    A[User Enters Username and Password] --> B{Credentials Valid?}
    B -->|No| C[Show Error Message]
    B -->|Yes| D{Role Check}
    D -->|Admin| E[Open Admin Dashboard]
    D -->|Student| F[Open Student Dashboard]
    D -->|Accountant| G[Open Accountant Dashboard]
```

---

## 3. Fee Payment Flow

```mermaid
flowchart TD
    A[Accountant Searches Student] --> B[Open Student Record]
    B --> C[Enter Paid Amount]
    C --> D[System Calculates Pending Amount]
    D --> E{Full Fee Paid?}
    E -->|Yes| F[Set Status = Paid]
    E -->|No| G{Any Payment Made?}
    G -->|Yes| H[Set Status = Partial]
    G -->|No| I[Set Status = Pending]
    F --> J[Save Transaction]
    H --> J
    I --> J
    J --> K[Generate Receipt]
    K --> L[Update Student Dashboard]
```

---

## 4. User Registration Flow

```mermaid
flowchart TD
    A[Open Registration Form] --> B[Fill Details]
    B --> C[Validate Input]
    C --> D{Valid Data?}
    D -->|No| E[Show Validation Errors]
    D -->|Yes| F[Save to Database]
    F --> G[Show Success Message]
    G --> H[Redirect to Login]
```

---

## 5. Forgot Password Flow

```mermaid
flowchart TD
    A[Open Forgot Password Page] --> B[Enter Email or Username]
    B --> C{User Found?}
    C -->|No| D[Show Not Found Message]
    C -->|Yes| E[Send Reset Token]
    E --> F[Verify Token]
    F --> G[Set New Password]
    G --> H[Password Updated]
```

---

## 6. Recommended UI Layout

### A. Login Screen

```
-----------------------------------------------------------
|  BRAND PANEL            |        LOGIN PANEL            |
|-------------------------|--------------------------------|
|  Logo                   |  Username / Email              |
|  Project Name           |  Password                      |
|  Tagline                |  Role Select / Auto Detect    |
|  Illustration           |  [Login Button]                |
|                         |  Forgot Password               |
|                         |  Register                      |
-----------------------------------------------------------
```

### UI Style for Login
- Left side should carry branding
- Right side should contain the form
- Use a clean card with soft shadow
- Add subtle gradient or glass effect
- Keep the form centered and spacious

---

### B. Dashboard Screen

```
-----------------------------------------------------------------------------------
| Top Bar: Logo | Search | Notifications | Profile | Logout                        |
-----------------------------------------------------------------------------------
| Sidebar       |  Stat Card 1   | Stat Card 2   | Stat Card 3   | Stat Card 4    |
| - Dashboard   |------------------------------------------------------------------|
| - Students    |  Recent Table / Chart Area                                         |
| - Fees        |                                                                   |
| - Reports     |  Quick Actions / Alerts / Due List                                |
| - Settings    |                                                                   |
-----------------------------------------------------------------------------------
```

### UI Style for Dashboard
- Fixed sidebar on the left
- Top navigation bar with profile and logout
- Main content area with cards and tables
- Use charts for total collection and pending dues
- Keep spacing open and balanced

---

### C. Student Fee View Screen

```
-----------------------------------------------------------
| Student Profile Card                                    |
|---------------------------------------------------------|
| Name:            | Course:                              |
| Admission No:     | Total Fee:                           |
| Paid Amount:      | Pending Amount:                      |
| Fee Status:       | Last Payment Date:                   |
-----------------------------------------------------------
| Payment History Table                                   |
| Receipt Download Button                                 |
-----------------------------------------------------------
```

### UI Style for Student Screen
- Simple and clean
- Use status badges for `Paid`, `Partial`, `Pending`
- Show readable tables
- Keep actions minimal and clear

---

### D. Accountant Screen

```
-----------------------------------------------------------
| Search Student                                           |
|---------------------------------------------------------|
| Search by ID / Name / Mobile                             |
| [Search Button]                                          |
-----------------------------------------------------------
| Student Details | Fee Entry Form | Payment Summary       |
|---------------------------------------------------------|
| Payment History Table                                    |
| [Save Payment] [Generate Receipt]                        |
-----------------------------------------------------------
```

### UI Style for Accountant Screen
- Search box at top
- Student info on the left
- Payment form on the right
- History table below
- Action buttons should be clearly visible

---

## 7. Visual Style Direction

The interface should look like a real SaaS/admin product:

- Use a navy, blue, teal, or charcoal base
- Keep background light or softly textured
- Use white cards with subtle shadows
- Use rounded corners
- Use smooth hover effects
- Use consistent SVG icons
- Use modern typography
- Avoid clutter
- Maintain strong spacing and alignment

---

## 8. Screen Priority Order

Build the UI in this order:

1. Splash screen
2. Login screen
3. Registration screen
4. Forgot password screen
5. Admin dashboard
6. Accountant dashboard
7. Student dashboard
8. Student management screen
9. Fee entry screen
10. Reports screen
11. Settings screen

---

## 9. Recommended Components

Reusable components should include:

- Sidebar
- Navbar
- Stat card
- Table component
- Form input
- Dropdown
- Button
- Modal
- Toast notification
- Status badge
- Receipt card

---

## 10. Final Visual Summary

The application should feel like:

- a premium school ERP system
- a professional fee management dashboard
- a clean commercial software product
- not a simple student project

The design should be modern, structured, and easy to use for staff and students.

