# Name: Debananda Kuanr
# Date: 29-06-2026

# Function
# def Fun():
#     print("Hello World")
# Fun() # O/P:Hello World 


# def sum(x,y):
#     return x+y
# def subtraction(x,y):
#     return x-y
# def multiplication(x,y):
#     return x*y
# def division(x,y):
#     return x/y
# sum_val,subtract,multi,divis=sum(20,10),subtraction(20,10),multiplication(20,10),division(20,10)
# print(f"Sum:{sum_val}\nSubtraction:{subtract}\nMultiplication:{multi}\nDivision:{divis}")




# def sum(x,y):
#     print("Sum is ",x+y)
# def subtraction(x,y):
#     print("Subtraction is ",x-y)
# def multiplication(x,y):
#     print("Multiplication is ",x*y)
# def division(x,y):
#     print("Division is ",x/y)

# sum(20,10)
# subtraction(20,10)
# multiplication(20,10)
# division(20,10)



# def square_fun(num):
#     squ=num**2
#     print(f"Square of {num} is {squ}")
# for i in range(1,21):
#     square_fun(i)


# def square_fun(num):
#     squ=num**2
#     print(squ,end=" ")
# print("Square of the Numbers are :")
# for i in range(1,21):
#     square_fun(i)


# def factorial(num):
#     temp=num
#     fact=1
#     while temp>0:
#         fact*=temp
#         temp-=1
#     print(f"Factorial of {num} is {fact}")
# factorial(5)


# def largest(x,y,z):
#     if x>y and x>z:
#         print(x,"is Largest")
#     elif y>z:
#         print(y,"is Largest")
#     else:
#         print(z,"is Largest")
# largest(20,30,10)


# def square_func(num):
#     return num**2
# result=square_func(2)
# print(result) 


# def add(a,b):
#     return a+b
# result=add(10,20)
# print(result)


# def sum(x,y):
#     return x+y
# num1=int(input("Enter Num1 :"))
# num2=int(input("Enter Num2 :"))
# add_result=sum(num1,num2)
# print("Result: ",add_result)


# def prime_or_not(num):
#     count=0
#     for i in range(1,num+1):
#         if num%i==0:
#             count+=1
#     if count==2:
#         print(num,"is Prime Number")
#     else:
#         print(num,"is not a Prime Number")
# Number=int(input("Enter a Number:"))
# prime_or_not(Number)



# def addition(a,b):
#     return a+b
# def subtraction(a,b):
#     return a-b
# def multiplication(a,b):
#     return a*b
# def division(a,b):
#     return a/b
# print(""""
# Please Select the Option
#       a. Add
#       b. Subtraction
#       c. Multiplication
#       d. Division      
# """)
# choice=input("Enter Here:").lower()
# if choice=="a":
#     num1=int(input("\nEnter Num1:"))
#     num2=int(input("Enter Num2:"))
#     result=addition(num1,num2)
#     print("Result:",result)
# elif choice=="b":
#     num1=int(input("\nEnter Num1:"))
#     num2=int(input("Enter Num2:"))
#     result=subtraction(num1,num2)
#     print("Result:",result)
# elif choice=="c":
#     num1=int(input("\nEnter Num1:"))
#     num2=int(input("Enter Num2:"))
#     result=multiplication(num1,num2)
#     print("Result:",result)
# elif choice=="d":
#     num1=int(input("\nEnter Num1:"))
#     num2=int(input("Enter Num2:"))
#     result=division(num1,num2)
#     print("Result:",result)
# else:
#     print("Invalid Choice")



# Print the larger Number among 2 integer using function with return type 
# def larger(a,b):
#     if a>b:
#         return a
#     else:
#         return b

# larger = larger(10,20)
# print("Larger is",larger)



# calculate sum of the factors of a Number Using The Function 
# def sum_factors(num):
#     sum=0
#     for i in range(1,num+1):
#         if num%i==0:
#             sum+=i
#     return sum

# sum=sum_factors(10)
# print("Sum of the Factor is",sum)


# To check how many even Number Greater than 50 from 30 to 60 using the Function
# def my_func():
#     count =0
#     for i in range(30,61):
#         if i%2==0 and i>50:
#             count+=1
#     return count

# count_num=my_func()
# print(f"There are {count_num} even Number Greater than 50 from 30 to 60")


# To calculate area of a circle and and rectangle of using a Function 
# def area_circle(radius):
#     area = 3.14 * radius * radius
#     return area

# def area_rectangle(length, width):
#     area = length * width
#     return area

# radius = float(input("Enter the radius of the circle: "))
# circle_area = area_circle(radius)
# print("Area of the circle is:", circle_area)

# length = float(input("Enter the length of the rectangle: "))
# width = float(input("Enter the width of the rectangle: "))
# rectangle_area = area_rectangle(length, width)
# print("Area of the rectangle is:", rectangle_area)
