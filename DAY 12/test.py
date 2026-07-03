# Name: Debananda Kuanr
# Date: 03-07-2026

# my_list=['python','swift','Java','JavaScript','Rust','R']
# del my_list[1]
# print(my_list) # ['python', 'Java', 'JavaScript', 'Rust', 'R']


# my_list=['python','swift','Java','JavaScript','Rust','R']
# del my_list[-1]
# print(my_list) # ['python', 'swift', 'Java', 'JavaScript', 'Rust']


# my_list=['python','swift','Java','JavaScript','Rust','R']
# del my_list[0:4]
# print(my_list) # ['Rust', 'R']


# my_list=['python','swift','Java','JavaScript','Rust','R']
# my_list.remove('python')
# print(my_list) # ['swift', 'Java', 'JavaScript', 'Rust', 'R']


# nums = [1,2,3,4,1,5]
# print("Before: ",nums)
# nums.remove(1)
# nums.remove(2)
# nums.remove(3)
# nums.remove(4)
# print("After: ",nums)


# my_list=[10,20,30,40,45,70,80,85]
# my_list.insert(5,50)
# print(my_list)


# my_list = [2,3,5,7]
# removed_item=my_list.pop(2)
# print(my_list)  # [2, 3, 7]
# print(removed_item) # 5 

# my_list=[10,20,30,40,50,60]
# print("Before: ",my_list)
# my_list.clear()
# print("After: ",my_list)

#  o/p:   Before:  [10, 20, 30, 40, 50, 60]
#         After:  []


# my_list=[10,20,10,40,10,60]
# count=my_list.count(10)
# print(count) # 3


# my_list=[10,20,30,40]
# new_var=my_list.copy()
# print(new_var) # [10, 20, 30, 40]



'''SET IN PYTHON'''
# nums = {1,2,2,3,3}
# print(nums) # {1,2,3}


# a={10,5,8,4}
# b={45,75}
# a.update(b)
# print(a) # {4, 5, 8, 10, 75, 45}


# a={10,5,8,4}
# a.remove(5) # It will remove the 5 from the set
# a.remove(11) # KeyError: 11 => it will  give this error bcz this element is not in the set


# a={10,5,8,4}
# a.discard(10) # Remove the element 10
# a.discard(11) # If the element is not there it will not Throught the eRROR where as the remove method through the "Key Error"


# Names={'Ram','Hari','Sita'}
# for i in Names:
#     print(i)


# a={1,2,3,4,5}
# b={5,6,7,8,9}
# union_ab=a|b
# c=a.union(b)
# print(union_ab)


# a={1,2,3,4,5,6}
# b={5,6,7,8,9,10}
# print(a.intersection(b)) # Using Method 
# print(a&b) # Using Operator


# a={1,2,3,4,5,6}
# b={5,6,7,8,9,10}
# print(a.difference(b)) # Using the Method 
# print(a-b) # Using the Operator


# a={1,2,3,4,5,6}
# b={1,2,3,4,5,7}
# if a|b == a:
#     print("Both are equal")
# else:
#     print("Both are Not Equal")


# a={1,2,3,4,5,6}
# b={1,2,3,4,5,6}
# if a==b:
#     print("Equal")
# else:
#     print("Not Equal")
