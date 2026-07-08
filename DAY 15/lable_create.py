from tkinter import *

window=Tk()
window.title("Lable Python")
window.geometry("450x300+20+20")
window.resizable(False,False) # this is not allow to maximize the screen

def addition():
    num1=t1.get()
    num2=t2.get()
    num3=int(num1)+int(num2)
    t3.delete(0,END)
    t3.insert(1,str(num3))

lbl=Label(window,text="Sum of 2 numbers",bg='Yellow',fg='red',font=("helvetica",16))
lbl.place(x=130,y=20)

# This is used to make a Label Text
lbl=Label(window,text="Enter 1st number:",fg='blue',font=("helvetica",16))
lbl.place(x=60,y=70)
# This is used to make a Input Box (Which is Given by the user)
t1=Entry(window,bg='white',fg="black",bd=5)
t1.place(x=250,y=70)

lbl2=Label(window,text="Enter 2nd number:",fg='blue',font=("helvetica",16))
lbl2.place(x=60,y=110)
t2=Entry(window,bg='white',fg="black",bd=5)
t2.place(x=250,y=110)

lbl3=Label(window,text="Result: ",fg='blue',font=("helvetica",16))
lbl3.place(x=60,y=150)
t3=Entry(window,bg='white',fg="black",bd=5)
t3.place(x=250,y=150)

# This is For the Button Part
btn=Button(window,text="ADD",fg='White',bg='green',font=("helvetica",16),command=addition,height=1,width=7)
btn.place(x=320,y=200)

window.mainloop()
