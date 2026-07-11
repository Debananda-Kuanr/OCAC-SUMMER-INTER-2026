# pip install mysql-connector-python
import subprocess
from tkinter import *
from tkinter import messagebox
import mysql.connector


window = Tk()
window.title("Login")
window.geometry("450x380+550+180")
window.resizable(False, False)


# Database Connection With Python
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9439",
    database="OCAC"
)
cursor = con.cursor()


# Forgot Password Function
def forgot_password():
    window.destroy()
    subprocess.Popen(["python",r"C:\Users\deban\Desktop\OCAC\OCAC-SUMMER-INTER-2026\test\forgot.py"])


# Login Function
def login_sys():
    user_username = username.get()
    user_password = password.get()

    if len(username.get()) == 0 and len(password.get()) == 0:

        my_status = "Enter Username and Password"

        messagebox.showinfo(
            "Warning",
            "Username and Password is blank\nPlease Enter"
        )

    elif len(username.get()) == 0:

        my_status = "Enter Username"

    elif len(password.get()) == 0:

        my_status = "Enter Password"

    else:

        try:

            sql = """
            SELECT * FROM registration
            WHERE Username=%s AND Password=%s
            """

            values = (user_username, user_password)

            cursor.execute(sql, values)
            result = cursor.fetchone()

            if result:
                my_status = "Login Successful !!"

            else:
                my_status = "Invalid Username and Password"

        except:

            my_status = "Database Error"

    status.delete(0, END)
    status.insert(1, my_status)

# Clear Function
def clear_screen():
    username.delete(0, END)
    password.delete(0, END)
    status.delete(0, END)

# Close Function
def close_screen():
    window.destroy()

top_label = Label(
    window,
    text="User Login",
    fg="green",
    font=("helvetica", 20, "bold")
)

top_label.place(x=150, y=35)


# USERNAME
display1 = Label(
    window,
    text="Username",
    fg="black",
    font=("helvetica", 16)
)
display1.place(x=50, y=110)


username = Entry(
    window,
    fg="black",
    bd=4,
    width=25
)
username.place(x=180, y=113)


# PASSWORD
display2 = Label(
    window,
    text="Password",
    fg="black",
    font=("helvetica", 16)
)
display2.place(x=50, y=155)


password = Entry(
    window,
    fg="black",
    bd=4,
    width=25,
    show="*"
)
password.place(x=180, y=158)


# FORGOT PASSWORD
forgot_btn = Button(
    window,
    text="Forgot Password?",
    fg="blue",
    bd=0,
    command=forgot_password
)

forgot_btn.place(x=245, y=195)


# STATUS

display3 = Label(
    window,
    text="Status",
    fg="blue",
    font=("helvetica", 16)
)

display3.place(x=50, y=240)


status = Entry(
    window,
    fg="black",
    bg="light blue",
    bd=2,
    font=("helvetica", 10, "bold"),
    width=30
)

status.place(x=130, y=245)


# BUTTONS 

btn1 = Button(
    window,
    text="Close",
    fg="black",
    bg="yellow",
    font=("helvetica", 12, "bold"),
    width=8,
    command=close_screen
)

btn1.place(x=55, y=310)


btn2 = Button(
    window,
    text="Clear",
    fg="white",
    bg="red",
    font=("helvetica", 12, "bold"),
    width=8,
    command=clear_screen
)

btn2.place(x=180, y=310)


btn3 = Button(
    window,
    text="Login",
    fg="white",
    bg="green",
    font=("helvetica", 12, "bold"),
    width=8,
    command=login_sys
)

btn3.place(x=305, y=310)


window.mainloop()