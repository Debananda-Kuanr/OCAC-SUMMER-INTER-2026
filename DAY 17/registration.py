from tkinter import *
from tkinter import messagebox
import mysql.connector

window=Tk()
window.title("Registration Form")
window.geometry("500x310+490+200")
window.resizable(False,False)

# Database Connection With Python 
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9439",
    database="OCAC"
) 
cursor=con.cursor()



def register_new():
    r=roll_no.get()
    n=name.get()
    u=username.get()
    p=password.get()

    if r=="" or n=="" or u=="" or p=="":
        messagebox.showinfo("Warning","All Field must be Filled")
    else:
        try:
            sql="INSERT INTO registration (Roll_No,Name,Username,Password) VALUES (%s,%s,%s,%s)"
            values=(r,n,u,p)
            cursor.execute(sql,values)
            con.commit() #Save the Changes Permanetly in Database 
        
            messagebox.showinfo("Sucess","Account Register Sucessfully")

            roll_no.delete(0,END)
            name.delete(0,END)
            username.delete(0,END)
            password.delete(0,END)
        except:
            messagebox.showinfo("Warning","Roll Number Exist in the Database")




def close_screen():
    window.destroy()

top_label=Label(window,text="Register a New User",fg='green',font=("helvetica",20,"bold"))
top_label.place(x=110,y=15)

display1=Label(window,text="Roll No",fg='Black',font=("helvetica",16))
display1.place(x=80,y=70)
roll_no=Entry(window,fg="black",bd=4,width=35)
roll_no.place(x=192,y=72)
roll_no.focus_set()

display1=Label(window,text="Name",fg='Black',font=("helvetica",16))
display1.place(x=80,y=110)
name=Entry(window,fg="black",bd=4,width=35)
name.place(x=192,y=112)

display1=Label(window,text="Username",fg='Black',font=("helvetica",16))
display1.place(x=80,y=150)
username=Entry(window,fg="black",bd=4,width=35)
username.place(x=192,y=152)

display1=Label(window,text="Password",fg='Black',font=("helvetica",16))
display1.place(x=80,y=190)
password=Entry(window,fg="black",bd=4,width=35)
password.place(x=192,y=192)


btn2=Button(window,text="Close",fg='white',bg='red',font=("helvetica",12,"bold"),width=8,command=close_screen)
btn2.place(x=210,y=240)
# btn2=Button(window,text="Clear",fg='White',bg='red',font=("helvetica",12,"bold"),width=8)
# btn2.place(x=200,y=240)
btn3=Button(window,text="Register",fg='White',bg='green',font=("helvetica",12,"bold"),width=8,command=register_new)
btn3.place(x=320,y=240)

window.mainloop()