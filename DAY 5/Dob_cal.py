# Debananda Kuanr
# Date:24-06-2026

print("--------Today's Date-------")
while True:
    today_year=int(input("Enter Year: "))
    if today_year==2026:
        break
    else:
        print("Invalid Year....")
while True:
    today_month=int(input("Enter Month: "))
    if today_month==6:
        break
    else:
        print("Invalid month....")    
while True:
    today_day=int(input("Enter Day: "))
    if today_day==25:
        break
    else:
        print("Invalid day....")



print("------Your Date of Birth-----")
while True:
    year=int(input("Enter Year: "))
    if 1700<=year<=2026:
        if (year > today_year):
            print("year is Greater than Current Year....")
        else:
            break
    else:
        print("Invalid....") 
while True:
    month=int(input("Enter Month: "))
    if 1<=month<=12:
        if (year == today_year and month > today_month):
            print("Invalid....")
        else:
            break
    else:
        print("Invalid month....")  
while True:
    day=int(input("Enter Day: "))
    if 1<=day<=31:
        if (year == today_year and month == today_month and day > today_day):
            print("Invalid....")
        else:
            break
    else:
        print("Invalid day....")
 
  
print("-------------------------------------------------------")
print(f"Your date of Birth is {day}-{month}-{year}")
print(f"Today's Date is {today_day}-{today_month}-{today_year}")
print("-------------------------------------------------------")

valid=1
if valid == 1:

    if today_day >= day:
        age_day = today_day - day
    else:
        age_day = today_day + 30 - day
        today_month = today_month - 1

    if today_month >= month:
        age_month = today_month - month
    else:
        age_month = today_month + 12 - month
        today_year = today_year - 1

    age_year = today_year - year

    print()
    print("Your age is :", age_year, "Years", age_month, "Months", age_day, "Days")