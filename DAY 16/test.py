# pip install mysql-connector-python

from tkinter import *
from tkinter import messagebox
import mysql.connector

window=Tk()
window.title("Login")
window.geometry("350x350+600+200")
window.resizable(False,False)

# Database Connection With Python 
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9439",
    database="OCAC"
) 
cursor=con.cursor()

def login_sys():
    user_username = username.get()
    user_password = password.get()

    if len(username.get())==0 and len(password.get()) ==0:
        my_status = "Enter Username and Password"
        messagebox.showinfo("Warning","Username Password is blank\nPlease Enter")

    elif len(username.get())==0:
        my_status = "Enter Username"
    elif len(password.get())==0:
        my_status = "Enter Password"
    else:
        sql="SELECT * FROM login WHERE userid=%s AND password=%s"
        values=(user_username,user_password)

        cursor.execute(sql,values)
        result=cursor.fetchone()
        if result:
            my_status="Login Sucessful !!"
        else:
            my_status="Invalid Username and Password"

    status.delete(0, END)
    status.insert(1, my_status)

def clear_screen():
    username.delete(0,END)
    password.delete(0,END)
    status.delete(0, END)

def close_screen():
    window.destroy()


top_label=Label(window,text="User Login",fg='green',font=("helvetica",20,"bold"))
top_label.place(x=100,y=40)

display1=Label(window,text="Username",fg='Black',font=("helvetica",16))
display1.place(x=35,y=125)
username=Entry(window,fg="black",bd=4,width=25)
username.place(x=157,y=127)


display2=Label(window,text="Password",fg='Black',font=("helvetica",16))
display2.place(x=35,y=165)
password=Entry(window,fg="black",bd=4,width=25,show="*")
password.place(x=157,y=167)


display3=Label(window,text="Status",fg='Blue',font=("helvetica",16))
display3.place(x=35,y=205)
status=Entry(window,fg="black",bg="light blue",bd=2,font=("helvetica",10,'bold'),width=30)
status.place(x=104,y=210)


btn2=Button(window,text="Close",fg='black',bg='yellow',font=("helvetica",12,"bold"),width=8,command=close_screen)
btn2.place(x=30,y=270)
btn2=Button(window,text="Clear",fg='White',bg='red',font=("helvetica",12,"bold"),width=8,command=clear_screen)
btn2.place(x=130,y=270)
btn3=Button(window,text="Login",fg='White',bg='green',font=("helvetica",12,"bold"),width=8,command=login_sys)
btn3.place(x=230,y=270)

window.mainloop()
