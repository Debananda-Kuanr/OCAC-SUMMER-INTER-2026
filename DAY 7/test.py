# Debananda Kuanr
# Date:26-06-2026

import numpy
# print(numpy.arange(1,11))

# arr=numpy.arange(1,11)
# for i in arr:
#     if i%2==0:
#         print(i," :Even")
#     else:
#         print(i," :Odd")


# a=numpy.arange(1,31)
# for i in a:
#     if i%3==0 and i%5==0:
#         print(i)


# a=numpy.arange(1,31)
# print("Divisible by 2 but not by 7:")
# for i in a:
#     if i%2==0 and i%7!=0:
#         print(i)


# arr1=numpy.array([1,2,3,4])
# arr2=numpy.array([1,2,3,4])

# if numpy.array_equal(arr1,arr2):
#     print("Equal")
# else:
#     print("Not Equal")


#Element wise Sum :
# arr1=numpy.array([10,20,30,40,50])
# arr2=numpy.array([1,2,3,4,5])
# sum_arr= arr1+arr2
# print("Sum of Arrays: ",sum_arr)


# arr1=numpy.array([10,20,30,40,50])
# rev_arr=numpy.flipud(arr1)
# print(rev_arr)

# a=numpy.arange(1,6)
# b=a 


# arr=numpy.array([1,2,3,4,5,6])
# x=arr.copy()
# x[0]=100
# print(arr)
# print(x)


# arr=numpy.array([10,20,30,40,50])
# x=arr.copy()
# for i in range(len(x)):
#     x[i]+=50
# print("Original:",arr)
# print("Modified:",x)


# arr1=numpy.array([[1,2],[3,4],[5,6]])
# print(arr1.shape)


# arr=numpy.array([10,20,30,40,50,60])
# arr1=arr.reshape(2,3)
# print(arr1)


# arr1=numpy.array([10,20,30])
# arr2=numpy.array([1,2,3])
# arr=numpy.concatenate((arr1,arr2))
# print(arr)


# arr=numpy.array([1,2,3,4,5,6,7])
# mid= len(arr)//2
# print(arr[mid])


# arr1=numpy.array([1,2,3,4,5,6,7,8,9,10])
# sqr_arr=arr1.copy()
# for i in range(len(sqr_arr)):
#     sqr_arr[i]=sqr_arr[i]**2
# print(sqr_arr)


# Sort without using sort method
# arr1=numpy.array([5,7,1,3,8,4])
# temp=arr1.copy()
# for i in range(len(temp)):
#     for j in range(len(temp)):
#         if temp[i]<temp[j]:
#             temp[i],temp[j]=temp[j],temp[i]
# print("Before Sort: ",arr1)
# print("After Sort: ",temp)
        

# find the min value and max value and diff between min and max
# arr1=numpy.array([10,20,30,40,50,60])
# print("Differnce between Max and Min is",arr1.max()-arr1.min())

# factorial of a Number 
# num= int(input("Enter a Number:"))
# temp=num
# fact=1
# while temp>0:
#     fact*=temp
#     temp-=1
# print(f"factorial of {num} is {fact}")


# Check Number is Prime or not 
# num= int(input("Enter a Number:"))
# count=0
# for i in range(1,num+1):
#     if num%i==0:
#         count+=1
# if count==2:
#     print("This is a Prime Number")
# else:
#     print("This is not a Prime Number ")
    
