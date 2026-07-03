# Name = input("Enter Your Name:")
# print(Name)


# First_name = input("Enter Your First Name:")
# Mid_name = input("Enter Your Middle Name:")
# Last_name = input("Enter Your Last Name:")
# print("Full Name is ",First_name,Mid_name,Last_name)

# Num1=int(input("Enter 1st Number:"))
# Num2=int(input("Enter 2nd Number:"))
# print("Sum is",Num1+Num2)


# PI=3.141
# r=int(input("Enter The Radius of the Sphear:"))
# v=4/3*(PI*r**3)
# print("The Volume of teh Sphere is :",v)


# Num= int(input("Enter a Number:"))
# if Num>0:
#     print("This is a +ve Number")
# if Num<0:
#     print("This is a -ve Number")
# if Num==0:
#     print("This is Zero")


# Num= int(input("Enter a Number:"))

# if Num%2==0:
#     if Num>20:
#         print("Number is even and Greater than 20")


# Num=15
# if Num%5==0:
#     if Num%2!=0:
#         print("15 is divisible by 5 and odd number")

# Amt_500,Amt_100,Amt_200=0,0,0
# org_Amount= int(input("Enter the Amount:"))
# Amount=org_Amount
# if Amount%100== 0:
#     print("Combination 1:")
#     if Amount>=500:
#         Amt_500=Amount//500
#         Amount=Amount-Amt_500*500
#     if Amount>=200:
#         Amt_200=Amount//200
#         Amount=Amount-Amt_200*200
#     if Amount>=100:
#         Amt_100=Amount//100
#         Amount=Amount-Amt_100*100
#     print("500 Rupees:",Amt_500)
#     print("200 Rupees:",Amt_200)
#     print("100 Rupees:",Amt_100)
    
#     Amt_500,Amt_100,Amt_200=0,0,0
#     Amount=org_Amount
#     print()
#     print("Combination 2:")
#     if Amount>=200:
#         Amt_200=Amount//200
#         Amount=Amount-Amt_200*200
    
#     if Amount>=100:
#         Amt_100=Amount//100
#         Amount=Amount-Amt_100*100
#     if Amount>=500:
#         Amt_500=Amount//500
#         Amount=Amount-Amt_500*500
#     print("200 Rupees:",Amt_200)
#     print("500 Rupees:",Amt_500)
#     print("100 Rupees:",Amt_100)


#     Amt_500,Amt_100,Amt_200=0,0,0
#     Amount=org_Amount
#     print()
#     print("Combination 3:")
#     if Amount>=100:
#         Amt_100=Amount//100
#         Amount=Amount-Amt_100*100
#     if Amount>=200:
#         Amt_200=Amount//200
#         Amount=Amount-Amt_200*200
    
#     if Amount>=500:
#         Amt_500=Amount//500
#         Amount=Amount-Amt_500*500
#     print("200 Rupees:",Amt_200)
#     print("500 Rupees:",Amt_500)
#     print("100 Rupees:",Amt_100)
    
# else:
#     print("Invalid Amount")


# A_day=int(input("Enter day(A)"))
# A_month=int(input("Enter Month(A)"))
# A_year=int(input("Enter Year(A)"))
# print()
# B_day=int(input("Enter day(B)"))
# B_month=int(input("Enter Month(B)"))
# B_year=int(input("Enter Year(B)"))
# print()

# if A_year<B_year:
#     print("User A is Elder")
# elif A_year>B_year:
#     print("User B is Elder")
# else:
#     if A_month<B_month:
#         print("User A is Elder")
#     elif A_month>B_month:
#         print("User B is Elder")
#     else:
#         if A_day<B_day:
#             print("User A is Elder")
#         elif A_day>B_day:
#             print("User B is Elder")
#         else:
#             print("Both Are Same Age")


# num=-7
# if(num!=0):
#     if(num>0):
#         print("Number is Possitive")
#     else:
#         print("Number is Negative")
# else:
#     print("Number is Zero")


# Number=70
# if Number%7==0:
#     print("Number is Divisible by 7")
#     if Number>50:
#         print("Also Greater than 50")
#     else:
#         print("and Not Greater than 50")
# else:
#     print("Number is Not Divisible by 7")
    


# Num=int(input("Enter a Number:"))
# if Num%2==0:
#     print("This is a Even Number",end=" ")
#     if Num>20:
#         print("and also Greater than 20")


# n = int(input("Enter a 3-digit number: "))
# if 100<=n<=999:
#     a = n // 100
#     b = (n // 10) % 10
#     c = n % 10

#     if a == b and b == c:
#         print("Equal digit number")
#     else:
#         print("Not an equal digit number")
# else:
#     print("Invalid Number")


# Num=int(input("Enter a Number:"))
# if Num%3!=0:
#     print("Number is not divisible by 3",end=" ")
#     if Num<20:
#         print("Also number is less than 20")
#     else:
#         print(" and Number is Greater than 20")
# else:
#     print("number is  divisible by 3")


# Num1=int(input("Enter 1st Number:"))
# Num2=int(input("Enter 2nd Number:"))
# Num3=int(input("Enter 3rd Number:"))

# if Num1>Num2 and Num1>Num3:
#     print(Num1," is greatest")
# elif Num2>Num3:
#     print(Num2," is greatest")
# else:
#     print(Num3," is greatest")


Edge=int(input("Enter the Edge of a Cube: "))
Volume = Edge**3
print("The Volume of a Cube is ",Volume)