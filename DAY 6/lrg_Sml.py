import array
a=array.array('i',[10,20,30,40,50])
large=a[1]
small=a[1]

for i in range(len(a)):
    if a[i]>large:
        large=a[i]
    if a[i]<small:
        small=a[i]
print(f"Largest: {large}\nSmallest: {small}")