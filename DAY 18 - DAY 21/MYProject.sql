-- MYProject.sql
-- Complete MySQL schema for the OCAC SUMMER INTER project
-- Database name used by the application: OCAC_GROUP2

CREATE DATABASE IF NOT EXISTS OCAC_GROUP2
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE OCAC_GROUP2;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS fee_payments;
DROP TABLE IF EXISTS student_fees;
DROP TABLE IF EXISTS fee_structure_components;
DROP TABLE IF EXISTS fee_structures;
DROP TABLE IF EXISTS student_approval_requests;
DROP TABLE IF EXISTS student_details;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS registration;

SET FOREIGN_KEY_CHECKS = 1;

-- --------------------------------------------------------
-- 1) REGISTRATION
-- --------------------------------------------------------
CREATE TABLE registration (
    Registration_No VARCHAR(50) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Security_Question VARCHAR(255) NOT NULL,
    Security_Answer VARCHAR(255) NOT NULL,
    Role VARCHAR(30) NOT NULL DEFAULT 'Student',
    Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (Registration_No),
    UNIQUE KEY uk_registration_username (Username),
    KEY idx_registration_role (Role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 2) COURSES
-- --------------------------------------------------------
CREATE TABLE courses (
    Course_ID INT NOT NULL AUTO_INCREMENT,
    Course_Name VARCHAR(150) NOT NULL,
    Duration VARCHAR(50) NULL,
    Description TEXT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Active',
    Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (Course_ID),
    UNIQUE KEY uk_courses_course_name (Course_Name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 3) STUDENT DETAILS
-- --------------------------------------------------------
CREATE TABLE student_details (
    Student_Detail_ID INT NOT NULL AUTO_INCREMENT,
    Registration_No VARCHAR(50) NOT NULL,
    Course VARCHAR(150) NOT NULL,
    Semester VARCHAR(50) NOT NULL,
    Admission_Year VARCHAR(20) NOT NULL,
    Email VARCHAR(255) NULL,
    Age VARCHAR(10) NULL,
    Gender VARCHAR(20) NULL,
    Phone VARCHAR(20) NULL,
    Status VARCHAR(30) NOT NULL DEFAULT 'Pending Approval',
    Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (Student_Detail_ID),
    UNIQUE KEY uk_student_details_registration_no (Registration_No),
    KEY idx_student_details_course (Course),
    KEY idx_student_details_status (Status),
    CONSTRAINT fk_student_details_registration
        FOREIGN KEY (Registration_No) REFERENCES registration (Registration_No)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 4) STUDENT APPROVAL REQUESTS
-- --------------------------------------------------------
CREATE TABLE student_approval_requests (
    Request_ID INT NOT NULL AUTO_INCREMENT,
    Registration_No VARCHAR(50) NOT NULL,
    Request_Type VARCHAR(30) NOT NULL,
    Student_Name VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    Previous_Data LONGTEXT NOT NULL,
    Proposed_Data LONGTEXT NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    Requested_At DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Reviewed_At DATETIME NULL,
    Reviewed_By VARCHAR(255) NULL,
    Remarks TEXT NULL,
    PRIMARY KEY (Request_ID),
    KEY idx_student_approval_status (Status),
    KEY idx_student_approval_regno (Registration_No),
    CONSTRAINT fk_student_approval_registration
        FOREIGN KEY (Registration_No) REFERENCES registration (Registration_No)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 5) FEE STRUCTURES
-- --------------------------------------------------------
CREATE TABLE fee_structures (
    Fee_Structure_ID INT NOT NULL AUTO_INCREMENT,
    Course VARCHAR(150) NOT NULL,
    Semester VARCHAR(50) NOT NULL,
    Admission_Batch VARCHAR(50) NULL,
    Title VARCHAR(255) NOT NULL,
    Total_Fee DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    Status VARCHAR(20) NOT NULL DEFAULT 'Active',
    Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (Fee_Structure_ID),
    KEY idx_fee_structures_course_semester (Course, Semester),
    KEY idx_fee_structures_status (Status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 6) FEE STRUCTURE COMPONENTS
-- --------------------------------------------------------
CREATE TABLE fee_structure_components (
    Component_ID INT NOT NULL AUTO_INCREMENT,
    Fee_Structure_ID INT NOT NULL,
    Component_Name VARCHAR(255) NOT NULL,
    Amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    Sort_Order INT NOT NULL DEFAULT 0,
    PRIMARY KEY (Component_ID),
    KEY idx_fee_components_structure (Fee_Structure_ID),
    CONSTRAINT fk_fee_components_structure
        FOREIGN KEY (Fee_Structure_ID) REFERENCES fee_structures (Fee_Structure_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 7) STUDENT FEES
-- --------------------------------------------------------
CREATE TABLE student_fees (
    Student_Fee_ID INT NOT NULL AUTO_INCREMENT,
    Registration_No VARCHAR(50) NOT NULL,
    Fee_Structure_ID INT NOT NULL,
    Total_Fee DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    Amount_Paid DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    Due_Amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    Payment_Status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (Student_Fee_ID),
    UNIQUE KEY uk_student_fees_registration (Registration_No),
    KEY idx_student_fees_status (Payment_Status),
    KEY idx_student_fees_structure (Fee_Structure_ID),
    CONSTRAINT fk_student_fees_registration
        FOREIGN KEY (Registration_No) REFERENCES registration (Registration_No)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_student_fees_structure
        FOREIGN KEY (Fee_Structure_ID) REFERENCES fee_structures (Fee_Structure_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 8) FEE PAYMENTS
-- --------------------------------------------------------
CREATE TABLE fee_payments (
    Payment_ID INT NOT NULL AUTO_INCREMENT,
    Student_Fee_ID INT NOT NULL,
    Amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    Payment_Mode VARCHAR(50) NOT NULL,
    Transaction_Reference VARCHAR(100) NOT NULL,
    Remarks TEXT NULL,
    Collected_By VARCHAR(255) NULL,
    Payment_Date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (Payment_ID),
    UNIQUE KEY uk_fee_payments_reference (Transaction_Reference),
    KEY idx_fee_payments_student_fee (Student_Fee_ID),
    KEY idx_fee_payments_date (Payment_Date),
    CONSTRAINT fk_fee_payments_student_fee
        FOREIGN KEY (Student_Fee_ID) REFERENCES student_fees (Student_Fee_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- OPTIONAL SAMPLE DATA
-- Uncomment if you want a ready-to-login admin account.
-- --------------------------------------------------------
-- INSERT INTO registration
-- (
--     Registration_No,
--     Name,
--     Username,
--     Password,
--     Security_Question,
--     Security_Answer,
--     Role
-- )
-- VALUES
-- (
--     'ADM0001',
--     'System Admin',
--     'admin',
--     'admin123',
--     'What is the project name?',
--     'OCAC',
--     'Admin'
-- );

-- --------------------------------------------------------
-- USEFUL INDEX FOR QUICK LOOKUP
-- --------------------------------------------------------
CREATE INDEX idx_fee_payments_collected_by ON fee_payments (Collected_By);

