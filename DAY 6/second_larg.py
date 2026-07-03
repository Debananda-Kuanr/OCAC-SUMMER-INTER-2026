import array
arr=array.array('i',[10,20,30,40,50])
a=arr
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
