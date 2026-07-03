# Date: 30-06-2026
# Name: Debananda Kuanr

""" This is the Multi Return value """

# def circle(r,pi=3.141):
#     area=pi*r**2
#     perimeter=2*pi*r
#     return area,perimeter
# cir_area,cir_perimeter=circle(5)
# print(f"Area of Circle:{cir_area}\nPeimeter of Circle:{cir_perimeter}")


""" This is the Recursion Function """

# def factorial(x):
#     if x==1 :
#         return 1
#     else:
#         return (x*factorial(x-1))
# x=int(input("Enter a Number:"))
# print("The Factorial is",factorial(x))


# def adding(x):
#     if x==1:
#         return 1
#     else:
#         return(x+adding(x-1))
# print("Sum is :",adding(10))


""" String and Character """
# Name="Debananda"
# print("Length:",len(Name))


# Name="Ram Krishna Panda"
# for i in range(len(Name)):
#     print(Name[i],end=" ")


# Name="Python"
# for i in range(len(Name)):
#     if Name[i]=="n" or Name[i]=="N":
#         print("N is present in ",Name)
#         break
# else:
#     print("N is not present in ",Name)



""" Deleting a String """

# new_str="OCAC Training Center"
# del new_str
# print(new_str) # Now it will Give Error Bcz the String is Deleted


""" Escap Character """
# print("Hello Good Morning\nI am Debananda Kuanr\nBATCH:\tOKCL/10/Python")


""" Compare the String """
# String1="Hello, World!"
# String2="Hello, World!"
# if(String1==String2):
#     print("Both are EQUAL")
# else:
#     print("Both are NOT EQUAL")


# def_user="Ram"
# def_pass="1234"

# user_id=input("Enter User ID:")
# user_Pass=input("Enter Password:")

# if def_user==user_id and def_pass==user_Pass:
#     print("Login Sucessful")
# else:
#     print("Invalid ID and Password")



""" String Repeating Operator """
# print("Hello World\n"*10)

""" Checking the word in a String """

# line=input("Enter a Line: ")
# word=input("Enter a Word: ")
# if word in line:
#     print("Word is Present in line ")
# else:
#     print("Word is not Present in line ")



# Word=input("Enter a Word: ")
# char=input("Enter a Char: ")
# if char in Word:
#     print("Char is Present in Word ")
# else:
#     print("Char is not Present in Word ")


""" Removing the Space From a String """
# Name="   Debananda"
# print(Name)
# print(len(Name))
# New_name=Name.lstrip()
# print(New_name)
# print(len(New_name))

# Name="Debananda    "
# print(Name)
# print(len(Name))
# New_name=Name.rstrip()
# print(New_name)
# print(len(New_name))

# Name="    Debananda    "
# print(Name)
# print(len(Name))
# New_name=Name.strip()
# print(New_name)
# print(len(New_name))


# Convert RaMa --> rAmA without Using the In-built Method
# upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# lower = "abcdefghijklmnopqrstuvwxyz"
# s = input("Enter a Word:")
# result = ""
# for ch in s:
#     valid = 0
#     for i in range(26):
#         if ch == upper[i]:
#             result += lower[i]
#             valid = 1
#             break
#         elif ch == lower[i]:
#             result += upper[i]
#             valid = 1
#             break
#     if valid == 0:
#         result += ch
# print("Your Output is :",result)



# name=input("Enter: ")
# new=""
# for i in range(len(name)):
#     if name[i]==name[i].lower():
#         new+=name[i].upper()
#     elif name[i]==name[i].upper():
#         new+=name[i].lower()
#     else:
#         new+=name[i]
# print("Result: ",new)