# Debananada Kuanr
# Date:25-06-2026

# import array
# a=array.array('i',[10,20,30,40])
# print(a[0])
# print(a[1])
# print(a[2])
# print(a[3])

# print(a[-1])
# print(a[-2])
# print(a[-3])
# print(a[-4])

# for i in range(len(a)):
#     print(a[i],end=" ")

# import array
# a=array.array('i',[10,20,30,40])
# print(a[0])
# a[0]=100
# print(a[0])


# import array
# sum_even=0
# sum_odd=0
# a=array.array('i',[2,3,6,7,8,9])

# for i in range(len(a)):
#     if a[i]%2==0:
#         sum_even+=a[i]
#     else:
#         sum_odd+=a[i]
# print("Sum of Even Number are",sum_even)
# print("Sum of odd Number are",sum_odd)


# even_count,odd_count=0,0
# for i in range(len(a)):
#     if a[i]%2==0:
#         even_count+=1
#     else:
#         odd_count+=1
# print(f"Even:{even_count} odd:{odd_count}")


# import array
# a=array.array('i',[10,20,30,40,50])
# print(a[2:4]) #20,30
# print(a[1:]) #20,30,40,50
# print(len(a)) #5


# import array
# sum_even=0
# a=array.array('i',[12,22,34,38])
# for i in range(len(a)):
#     temp=a[i]
#     while temp>0:
#         dig=temp%10
#         if dig%2==0:
#             sum_even+=dig
#         temp=temp//10
# print("Sum of even digit is",sum_even)


# import array 
# a=array.array('i',[1,2,3,4,5])
# key=int(input("Enter :"))
# valid=1
# for i in range(len(a)):
#     if key==a[i]:
#         print("Your key is in position ",i+1)
#         valid=1
#         break
#     else:
#         valid=0

# if valid==0:
#     print("Key is Not Found ")



# import array 
# arr1= array.array('i',[2,4,6,8,10,11])
# arr2= array.array('i',[2,4,6,8,12,11])

# count=0
# for i in range(len(arr1)):
#     if arr1[i]==arr2[i]:

#         pass
#         count+=1
#     else:
#         print("Both arrays are not same")
#         break
# if count==len(arr1):
#     print("Both arrays are same")


import array
a=array.array('i',[4,5,6,7])
print(a) # array('i', [4, 5, 6, 7])
a.insert(1,2)
print(a) # array('i', [4, 2, 5, 6, 7])
a.append(10)
print(a) # array('i', [4, 2, 5, 6, 7, 10])
a.remove(4)
print(a) # array('i', [2, 5, 6, 7, 10])
a.pop()
print(a) # array('i', [2, 5, 6, 7])









