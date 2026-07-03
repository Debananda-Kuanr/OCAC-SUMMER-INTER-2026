while True:

    print("=" * 45)
    print("      EMPLOYEE ATTENDANCE SYSTEM")
    print("=" * 45)

    
    # salary_per_hour = 200          # working hour
    # overtime_rate = 300            # overtime hour
    # late_deduction_rate = 100      # eduction per late hour

    attempt = 1

    while attempt <= 3:

        emp_id = input("Enter Employee ID : ")

        if emp_id == "1234":
            emp_name = "Debananda"
            break

        else:
            print("Invalid Employee ID!")
            print("Remaining Attempts :", 3 - attempt)
            attempt += 1
            print()

    if attempt == 4:
        print("\nEmployee ID Blocked!")
        print("Contact Office.")
        break

    print("\nWelcome", emp_name, "!")
    print("Office Timing : 08:00 AM to 08:00 PM")


    while True:

        print("\n---------------------------------------------")
        print("Enter Check-in Time")
        print("---------------------------------------------")

        while True:
            cin_hour = int(input("Hour   : "))
            if 1 <= cin_hour <= 12:
                break
            print("Invalid Hour! Enter between 1 and 12.")

        while True:
            cin_min = int(input("Minute : "))
            if 0 <= cin_min <= 59:
                break
            print("Invalid Minute! Enter between 0 and 59.")

        while True:
            cin_am_pm = input("AM/PM  : ").upper()
            if cin_am_pm in ["AM", "PM"]:
                break
            print("Enter only AM or PM.")

        temp_hour = cin_hour

        if cin_am_pm == "PM" and temp_hour != 12:
            temp_hour += 12

        if cin_am_pm == "AM" and temp_hour == 12:
            temp_hour = 0

        checkin = temp_hour * 60 + cin_min

        if checkin < 8 * 60:
            print("\nCheck-in must be after 08:00 AM.")
            continue

        elif checkin >= 20 * 60:
            print("\nCheck in must be before 08:00 PM.")
            continue
        
        # elif checkin > 12 * 60:
        #     print("\nCheck-in must be before 12:00 PM.")
        #     print("Employee must complete 8 working hours before 08:00 PM.")
        #     continue

        else:
            break


    while True:

        print("\n---------------------------------------------")
        print("Enter Check-out Time")
        print("---------------------------------------------")

        while True:
            cout_hour = int(input("Hour   : "))
            if 1 <= cout_hour <= 12:
                break
            print("Invalid Hour! Enter between 1 and 12.")

        while True:
            cout_min = int(input("Minute : "))
            if 0 <= cout_min <= 59:
                break
            print("Invalid Minute! Enter between 0 and 59.")

        while True:
            cout_am_pm = input("AM/PM  : ").upper()
            if cout_am_pm in ["AM", "PM"]:
                break
            print("Enter only AM or PM.")

        temp_hour = cout_hour

        if cout_am_pm == "PM" and temp_hour != 12:
            temp_hour += 12

        if cout_am_pm == "AM" and temp_hour == 12:
            temp_hour = 0

        checkout = temp_hour * 60 + cout_min

        if checkout > 20 * 60:
            print("\nCheck-out must be before 08:00 PM.")
            continue

        elif checkout <= checkin:
            print("\nCheck-out must be after Check-in.")
            continue

        else:
            break


    working = checkout - checkin

    work_hour = working // 60
    work_min = working % 60

    

    # late = checkin - (8 * 60)

    # if late < 0:
    #     late = 0

    # late_hour = late // 60
    # late_min = late % 60



    overtime = working - (8 * 60)

    if overtime < 0:
        overtime = 0

    ot_hour = overtime // 60
    ot_min = overtime % 60



    # if working >= 480:
    #     status = "Full Day"

    # elif working >= 240:
    #     status = "Half Day"

    # else:
    #     status = "Absent"



    #basic_salary = (working / 60) * salary_per_hour


    #late_deduction = (late / 60) * late_deduction_rate

    
    #overtime_pay = (overtime / 60) * overtime_rate


    #net_salary = basic_salary - late_deduction + overtime_pay

    # if net_salary < 0:
    #     net_salary = 0

    

    print()
    print("=" * 45)
    print("           ATTENDANCE REPORT")
    print("=" * 45)

    print("Employee ID      :", emp_id)
    print("Employee Name    :", emp_name)
    print()

    print(f"Check-in Time    : {cin_hour}:{cin_min} {cin_am_pm}")
    print(f"Check-out Time   : {cout_hour}:{cout_min} {cout_am_pm}")
    print()

    print(f"Working Time     : {work_hour} Hours {work_min} Minutes")
    #print(f"Late By          : {late_hour} Hours {late_min} Minutes")
    print(f"Overtime         : {ot_hour} Hours {ot_min} Minutes")
    #print(f"Attendance       : {status}")

    # print("-" * 45)
    # print(f"Basic Salary     : ₹{basic_salary}")
    # print(f"Late Deduction   : ₹{late_deduction}")
    # print(f"Overtime Pay     : ₹{overtime_pay}")
    # print("-" * 45)
    # print(f"Net Salary       : ₹{net_salary}")

    print("=" * 45)
    print("            Thank You!")
    print("=" * 45)

    break