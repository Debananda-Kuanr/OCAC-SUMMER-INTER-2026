# num=70
# if num%7== 0:
#     print("The number is divisible by 7")


# price=90
# if price>100:
#     final_price = price-(price*0.1)
# print("The Final Price is : ",final_price)
# if price<100:
#     print("The Final Price is : ",price)


# a,b,c=10,20,15
# if a>b:
#     if a>c:
#         print("A is greater")  
# if b>a:
#     if b>c:
#         print("B is greater")
# if c>a:
#     if c>b:
#         print("C is greater")


# Number= 10
# if Number%2==0:
#     print("The number is even")
# else:
#     print("The number is odd")


# price=90
# if price>100:
#     final_price = price-(price*0.1)
# else:
#     final_price = price-(price*0.05) 
# print("The Final Price is : ",final_price)


# print(10>5 and 7>10) #False
# print(10>5 and 5>3) #True

# num1,num2,num3=10,20,30
# if num1>num2 and num1>num3:
#     print("Num1 is greater")
# if num2>num1 and num2>num3:
#     print("Num2 is greater")
# if num3>num1 and num3>num2:
#     print("Num3 is greater")


# Debananda Kuanr
# day = 4
# month = 9
# year = 2007

# today_day = 19
# today_month = 6
# today_year = 2026

# valid = 1


# if day < 1 or day > 31:
#     print("Invalid Birth Day")
#     valid = 0

# if month < 1 or month > 12:
#     print("Invalid Birth Month")
#     valid = 0

# if year < 1:
#     print("Invalid Birth Year")
#     valid = 0



# if today_day < 1 or today_day > 31:
#     print("Invalid Today's Day")
#     valid = 0

# if today_month < 1 or today_month > 12:
#     print("Invalid Today's Month")
#     valid = 0

# if today_year < 1:
#     print("Invalid Today's Year")
#     valid = 0



# if valid == 1:
#     if (year > today_year) or (year == today_year and month > today_month) or (year == today_year and month == today_month and day > today_day):
#         print("Invalid Birth Date")
#         valid = 0



# if valid == 1:

#     if today_day >= day:
#         age_day = today_day - day
#     else:
#         age_day = today_day + 30 - day
#         today_month = today_month - 1

#     if today_month >= month:
#         age_month = today_month - month
#     else:
#         age_month = today_month + 12 - month
#         today_year = today_year - 1

#     age_year = today_year - year

#     print("Your age is :", age_year, "Years", age_month, "Months", age_day, "Days")


# num = 45

# digit1 = num // 10
# digit2 = num % 10
# sum = digit1 + digit2
# print("Sum of digits =", sum)

#Debananda Kuanr
# num= 45

# digit1 = num // 10
# digit2 = num % 10

# word1 = ""
# word2 = ""

# if digit1 == 0:
#     word1 = "Zero"
# if digit1 == 1:
#     word1 = "One"
# if digit1 == 2:
#     word1 = "Two"
# if digit1 == 3:
#     word1 = "Three"
# if digit1 == 4:
#     word1 = "Four"
# if digit1 == 5:
#     word1 = "Five"
# if digit1 == 6:
#     word1 = "Six"
# if digit1 == 7:
#     word1 = "Seven"
# if digit1 == 8:
#     word1 = "Eight"
# if digit1 == 9:
#     word1 = "Nine"

# if digit2 == 0:
#     word2 = "Zero"
# if digit2 == 1:
#     word2 = "One"
# if digit2 == 2:
#     word2 = "Two"
# if digit2 == 3:
#     word2 = "Three"
# if digit2 == 4:
#     word2 = "Four"
# if digit2 == 5:
#     word2 = "Five"
# if digit2 == 6:
#     word2 = "Six"
# if digit2 == 7:
#     word2 = "Seven"
# if digit2 == 8:
#     word2 = "Eight"
# if digit2 == 9:
#     word2 = "Nine"

# print(word1, word2)


# Debananda Kuanr
# num1 = 45
# num2 = 45

# if num1 == num2:
#     print("Both numbers are equal")
# else:
#     print("Both numbers are not equal")

#Debananda Kuanr
num = 17

if num % 5 == 0:
    print("Number is divisible by 5")
else:
    print("Number is not divisible by 5")