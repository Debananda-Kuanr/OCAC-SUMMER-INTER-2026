# Name: Debananda Kuanr
# Date: 01-07-2026

""" Swapcase() """
# Name="Debananda Kuanr"
# print(Name.swapcase()) # O/P:- dEBANANDA kUANR

""" capitalize() """
# This will convert first ch of the string capital
# name="rama"
# print(name.capitalize()) # Rama

""" replace() """
# s="Computer is an Electronic Device"
# print(s.replace("Computer","Laptop"))

""" isalpha() """
# str="Rama"
# print(str.isalpha()) # True

# str="raMa"
# print(str.isalpha()) # True

# str="ra Ma"
# print(str.isalpha()) # False

# str="OCAC123"
# print(str.isalpha()) # False

# str="OCAC@123"
# print(str.isalpha()) # False



""" Program 1 """
# name=input("Enter Your name: ")
# if name.isalpha():
#     print("Your name is ",name)
# else:
#     print("Error in Your name")


""" isdigit() """
# Num="1234"
# print(Num.isdigit()) # True
# Num2="123.45"
# print(Num2.isdigit()) # False

""" Programe 2 """
# count=3
# sum=0
# while True:
#     if count<=0:
#         break
#     num=input("Enter a Number:")
#     if len(num)==4 and num.isdigit():
#         num=int(num)
#         com_num=9999-num
#         print("Computer Number:",com_num)
#         sum+=num+com_num
#         count-=1
#     else:
#         print("Invalid Number...")
# print("Sum is :",sum)

""" Programe 3 """
# zip_code=input("Enter Your Zip Code:")
# if len(zip_code)==6 and zip_code.isdigit():
#     print("Correct Zip Code")
#     print(zip_code)
# else:
#     print("Invalid ZIP Code")


""" Programe 4 """
# word=input("Enter a Word:")
# vow,cons=0,0
# for i in range(len(word)):
#     if word[i].lower() in ("a","e","i","o","u"):
#         vow+=1
#     else:
#         cons+=1
# print(f"Word: {word}\nNumber of Vowel:{vow}\nNumber of Consonant:{cons}")



""" islower() """
# name ="deba"
# print(name.islower()) # True


""" isupper() """
# name ="DEBA"
# print(name.islower()) # True


# """ Program 5 """
# name=input("Enter your Name: ")
# college_name=input("Enter your College Name: ")
# age=input("Enter Your Age: ")

# print("\nFinal List:")
# print("-"*20)
# if name.isalpha():
#     print("Your Name: ",name)
# else:
#     print("Error in Your Name")

# if college_name.isalpha():
#     print("Your Collge Name: ",college_name)
# else:
#     print("Error in Your college Name")

# if age.isdigit():
#     print("Your age: ",age)
# else:
#     print("Error in Your Age")


""" Calendar Module """
# import calendar
# year=2026
# print(calendar.calendar(year))

#                                   2026

#       January                   February                   March
# Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
#           1  2  3  4                         1                         1
#  5  6  7  8  9 10 11       2  3  4  5  6  7  8       2  3  4  5  6  7  8
# 12 13 14 15 16 17 18       9 10 11 12 13 14 15       9 10 11 12 13 14 15
# 19 20 21 22 23 24 25      16 17 18 19 20 21 22      16 17 18 19 20 21 22
# 26 27 28 29 30 31         23 24 25 26 27 28         23 24 25 26 27 28 29
#                                                     30 31

#        April                      May                       June
# Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
#        1  2  3  4  5                   1  2  3       1  2  3  4  5  6  7
#  6  7  8  9 10 11 12       4  5  6  7  8  9 10       8  9 10 11 12 13 14
# 13 14 15 16 17 18 19      11 12 13 14 15 16 17      15 16 17 18 19 20 21
# 20 21 22 23 24 25 26      18 19 20 21 22 23 24      22 23 24 25 26 27 28
# 27 28 29 30               25 26 27 28 29 30 31      29 30

#         July                     August                  September
# Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
#        1  2  3  4  5                      1  2          1  2  3  4  5  6
#  6  7  8  9 10 11 12       3  4  5  6  7  8  9       7  8  9 10 11 12 13
# 13 14 15 16 17 18 19      10 11 12 13 14 15 16      14 15 16 17 18 19 20
# 20 21 22 23 24 25 26      17 18 19 20 21 22 23      21 22 23 24 25 26 27
# 27 28 29 30 31            24 25 26 27 28 29 30      28 29 30
#                           31

#       October                   November                  December
# Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
#           1  2  3  4                         1          1  2  3  4  5  6
#  5  6  7  8  9 10 11       2  3  4  5  6  7  8       7  8  9 10 11 12 13
# 12 13 14 15 16 17 18       9 10 11 12 13 14 15      14 15 16 17 18 19 20
# 19 20 21 22 23 24 25      16 17 18 19 20 21 22      21 22 23 24 25 26 27
# 26 27 28 29 30 31         23 24 25 26 27 28 29      28 29 30 31
#                           30



# import calendar
# print(calendar.month(2026,9))
# print(calendar.month(2026,7))

#    September 2026
# Mo Tu We Th Fr Sa Su
#     1  2  3  4  5  6
#  7  8  9 10 11 12 13
# 14 15 16 17 18 19 20
# 21 22 23 24 25 26 27
# 28 29 30

#      July 2026
# Mo Tu We Th Fr Sa Su
#        1  2  3  4  5
#  6  7  8  9 10 11 12
# 13 14 15 16 17 18 19
# 20 21 22 23 24 25 26
# 27 28 29 30 31

# import calendar
# print("CALANDAR PRINTER")
# month=int(input("Enter the Month: "))
# year=int(input("Enter the Year:"))
# print()
# print(calendar.month(year,month))


""" Display the Month Name """
# import calendar
# for i in range(1,13):
#     print(calendar.month_name[i])

""" Display the Day Name """
# import calendar
# for i in calendar.day_name:
#     print(i)

""" isleap() """
# import calendar
# print(calendar.isleap(2021)) #False
# print(calendar.isleap(2022)) #False
# print(calendar.isleap(2023)) #False
# print(calendar.isleap(2024)) #True
# print(calendar.isleap(2025)) #False
# print(calendar.isleap(2026)) #False