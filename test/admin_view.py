from tkinter import *
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

    user_list.delete(0, END)

    sql="SELECT Username,Password FROM registration"
    cursor.execute(sql)
    result=cursor.fetchall()

    for i in range(len(result)):

        user_tuple=result[i]

        username=user_tuple[0]
        password=user_tuple[1]

        user_list.insert(
            END,
            f"{username:<25}{password}"
        )


top_label=Label(
    window,
    text="All Registration Details",
    fg='green',
    font=("helvetica",20,"bold")
)
top_label.place(x=90,y=15)


btn=Button(
    window,
    text="Show All",
    fg='black',
    bg='yellow',
    font=("helvetica",10,"bold"),
    width=7,
    command=display_users
)
btn.place(x=410,y=18)


top_label=Label(
    window,
    text="Username",
    fg='blue',
    font=("helvetica",15,"bold")
)
top_label.place(x=75,y=65)


top_label=Label(
    window,
    text="Password",
    fg='blue',
    font=("helvetica",15,"bold")
)
top_label.place(x=295,y=65)


# Listbox
user_list=Listbox(
    window,
    width=43,
    height=14,
    font=("Courier New",13)
)
user_list.place(x=35,y=105)


# Scrollbar
scrollbar=Scrollbar(
    window,
    command=user_list.yview
)
scrollbar.place(x=460,y=105,height=315)


# Connect Scrollbar with Listbox
user_list.config(
    yscrollcommand=scrollbar.set
)


window.mainloop()