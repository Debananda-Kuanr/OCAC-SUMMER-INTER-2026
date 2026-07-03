# Debananda Kuanr
day = 4
month = 9
year = 2007

today_day = 19
today_month = 6
today_year = 2026

valid = 1


if day < 1 or day > 31:
    print("Invalid Birth Day")
    valid = 0

if month < 1 or month > 12:
    print("Invalid Birth Month")
    valid = 0

if year < 1:
    print("Invalid Birth Year")
    valid = 0



if today_day < 1 or today_day > 31:
    print("Invalid Today's Day")
    valid = 0

if today_month < 1 or today_month > 12:
    print("Invalid Today's Month")
    valid = 0

if today_year < 1:
    print("Invalid Today's Year")
    valid = 0



if valid == 1:
    if (year > today_year) or (year == today_year and month > today_month) or (year == today_year and month == today_month and day > today_day):
        print("Invalid Birth Date")
        valid = 0



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

    print("Your age is :", age_year, "Years", age_month, "Months", age_day, "Days")