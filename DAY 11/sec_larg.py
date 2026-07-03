
my_list=[10,20,30,40,50]
a=my_list
large=a[1]
for i in range(len(a)):
    if a[i]>large:
        large=a[i]
a.remove(large)
large=a[1]
for i in range(len(a)):
    if a[i]>large:
        large=a[i]
print("Second largest number is",large)
