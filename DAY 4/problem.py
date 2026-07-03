# Date: 23/06/2026
# Debananda Kuanr 

# Price=int(input("Enter the Price:"))
# if Price>100:
#     print("Price is Greater than 100")
# elif Price<100:
#     print("Price is Less than 100")
# else:
#     print("Price is Equal 100")


# character=input("Enter a Character(C/H/V/F): ")
# if character=="c" or character=="C":
#     print("You are a Cricket Player")
# elif character=="H" or character=="h":
#     print("You are a Hockey Player")
# elif character=="V" or character=="v":
#     print("You are a Volley Player")
# elif character=="f" or character=="F":
#     print("You are a Football Player")
# else:
#     print("You are not a Player")


# print("Number From 1 to 10:")
# for i in range(1,11,1):
#     print(i)


# print("From 10 to 1")
# for i in range(10,0,-1):
#     print(i)


# for i in range(2,11,2):
#     print(i)


# for i in range(1,11):
#     if i%2==0:
#         print(i)


# for i in range(1,11):
#     if i%2!=0:
#         print(i)


# sum=0
# for i in range(1,21):
#     if i%2==0:
#         sum+=i
# print("Sum of even Number is",sum)
# sum=0
# for i in range(1,21):
#     if i%2!=0:
#         sum+=i
# print("Sum of odd Number is",sum)


# Num=int(input("Enter a Number: "))
# print("Factors Of the Number are :")
# for i in range(1,Num+1):
#     if Num%i==0:
#         print(i)


# sum=0
# Num=int(input("Enter a Number: "))
# print("Sum of the even factor Of the Number is :")
# for i in range(1,Num+1):
#     if Num%i==0:
#         if i%2==0:
#             sum+=i
# print(sum)


# for i in range(3):
#     for j in range(3):
#         print(i,j)


# Num=int(input("Enter a Number:"))
# for i in range(1,11):
#     print(Num,"x",i,"=",Num*i)


# i=1
# while i<=10:
#     print(i)
#     i+=1


# Num=50
# while Num<=100:
#     print(Num)
#     Num+=1


# Num=20
# while Num>=1:
#     print(Num)
#     Num-=1


# N=int(input("Enter a Number :"))
# while N>0:
#     print("Hello")
#     N-=1


# R1=int(input("Enter a Start Range :"))
# R2=int(input("Enter an End Range :"))
# while R1<=R2:
#     if R1%2==0:
#         print(R1)
#     R1=R1+1


# print("-----Mark Grading System-----")
# Seq_mark=0
# for i in range(5):
#     while True:
#         Mark = int(input(f"Enter the mark of Subject {i+1}: "))
        
#         if 0 <= Mark <= 100:
#             Seq_mark += Mark
#             break
#         else:
#             print("Mark must be between 0 and 100")
# Per=int(Seq_mark/500*100)
# print()
# print("Your Grade is :",end="")
# if Per>=90 and Per<=100:
#     print("O")
# elif Per>=80 and Per<=89:
#     print("E")
# elif Per>=70 and Per<=79:
#     print("A")
# elif Per>=60 and Per<=69:
#     print("B")
# elif Per>=50 and Per<=59:
#     print("C")
# elif Per>=40 and Per<=49:
#     print("D")
# elif Per>=30 and Per<=39:
#     print("Pass")
# else:
#     print("FAIL")