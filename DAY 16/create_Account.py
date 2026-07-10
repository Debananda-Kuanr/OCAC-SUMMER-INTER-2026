import subprocess
import sys
import os
from tkinter import *
from tkinter import messagebox
import mysql.connector

window=Tk()
window.title("New User")
window.geometry("480x300+520+280")
window.resizable(False,False)

# Database Connection With Python 
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9439",
    database="OCAC"
) 
cursor=con.cursor()

def login():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(
        current_dir,
        "OCAC-SUMMER-INTER-2026",
        "DAY 16",
        "test.py"
    )
    subprocess.Popen([sys.executable, test_file])
    window.destroy()

def create_account():
    u_username=username.get()
    p_password=password.get()
    p_con_password=conf_password.get()

    if len(username.get())==0:
        messagebox.showinfo("Warning","Username is Empty !\nEnter the Username")
    elif len(password.get())==0:
        messagebox.showinfo("Warning","Password is Empty !\nEnter the Password")
    elif len(conf_password.get())==0:
        messagebox.showinfo("Warning","Confirm Password is Empty !\nRe-enter the Password")
    elif p_password!=p_con_password:
        messagebox.showinfo("Warning","Your Password and \nconfirm Password are Different")
    else: 
        sql="SELECT * FROM login WHERE userid=%s"
        values=(u_username,)
        cursor.execute(sql,values)
        result=cursor.fetchone()
        if result:
            messagebox.showinfo("Warning",f"{u_username} username is already exist !!\nChoose Different Username") 
        else:
            try:
                sql = "INSERT INTO login (userid, password) VALUES (%s, %s)"
                values = (u_username, p_password)
                cursor.execute(sql, values)
                con.commit()

                messagebox.showinfo("Success",f"Welcome {u_username}\nUser Account Created Successfully")
                
                # Here open the login File
                window.destroy() 
                current_dir = os.path.dirname(os.path.abspath(__file__))
                test_file = os.path.join(
                current_dir,"OCAC-SUMMER-INTER-2026","DAY 16","test.py")
                subprocess.Popen([sys.executable, test_file])
                

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

def close_screen():
    window.destroy()

top_label=Label(window,text="Create New User Account ",fg='green',font=("helvetica",20,"bold"))
top_label.place(x=80,y=20)

display1=Label(window,text="Username",fg='Black',font=("helvetica",16))
display1.place(x=85,y=90)
username=Entry(window,fg="black",bd=4,width=35)
username.place(x=197,y=92)


display2=Label(window,text="Password",fg='Black',font=("helvetica",16))
display2.place(x=85,y=130)
password=Entry(window,fg="black",bd=4,width=35)
password.place(x=197,y=132)


display3=Label(window,text="Password(Cnf)",fg='Black',font=("helvetica",16))
display3.place(x=46,y=170)
conf_password=Entry(window,fg="black",bd=4,width=35)
conf_password.place(x=197,y=172)

btn1=Button(window,text="Close",fg='white',bg='red',font=("helvetica",12,"bold"),width=8,command=close_screen)
btn1.place(x=170,y=231)
btn2=Button(window,text="Create Account",fg='White',bg='green',font=("helvetica",12,"bold"),width=13,command=create_account)
btn2.place(x=274,y=230)


btn1=Button(window,text="Login Here",fg='blue',font=("helvetica",11,"bold"),width=10,command=login)
btn1.place(x=55,y=232)



window.mainloop()