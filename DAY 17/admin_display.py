from tkinter import *
from tkinter import messagebox
import mysql.connector

window=Tk()
window.title("Registration Form")
window.geometry("500x450+490+100")
window.resizable(False,False)

# Database Connection With Python 
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9439",
    database="OCAC"
) 
cursor=con.cursor()
def display_users():
    sql="SELECT Username,Password FROM registration"
    cursor.execute(sql)
    result=cursor.fetchall()

    count=0
    for i in range(len(result)):
        user_tuple = result[i]  
        username = user_tuple[0]
        password = user_tuple[1]
        top_label = Label(window, text=username, fg='black', font=("helvetica", 15)) 
        top_label.place(x=80, y=(105 + (40 * count)))

        top_label = Label(window, text=password, fg='black', font=("helvetica", 15)) 
        top_label.place(x=300, y=(105 + (40 * count)))
        count+=1


top_label=Label(window,text="All Registration Details",fg='green',font=("helvetica",20,"bold"))
top_label.place(x=95,y=15)

btn=Button(window,text="Show All",fg='black',bg='yellow',font=("helvetica",10,"bold"),width=7,command=display_users)
btn.place(x=415,y=18)

top_label=Label(window,text="Username",fg='blue',font=("helvetica",15,"bold"))
top_label.place(x=80,y=65)
top_label=Label(window,text="Password",fg='blue',font=("helvetica",15,"bold"))
top_label.place(x=300,y=65)

window.mainloop()