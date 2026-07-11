from tkinter import *
from tkinter import messagebox
import mysql.connector


window = Tk()
window.title("Registration Form")
window.geometry("550x430+490+150")
window.resizable(False, False)


# Database Connection With Python
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9439",
    database="OCAC"
)

cursor = con.cursor()


# Register New User
def register_new():

    r = roll_no.get()
    n = name.get()
    u = username.get()
    p = password.get()
    q = security_question.get()
    a = security_answer.get()

    if r == "" or n == "" or u == "" or p == "" or q == "" or a == "":

        messagebox.showwarning(
            "Warning",
            "All Fields must be Filled"
        )

    else:

        try:

            sql = """
            INSERT INTO registration
            (Roll_No, Name, Username, Password, Security_Question, Security_Answer)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (r, n, u, p, q, a)

            cursor.execute(sql, values)

            # Save the Changes Permanently in Database
            con.commit()

            messagebox.showinfo(
                "Success",
                "Account Registered Successfully"
            )

            # Clear All Fields
            roll_no.delete(0, END)
            name.delete(0, END)
            username.delete(0, END)
            password.delete(0, END)
            security_question.delete(0, END)
            security_answer.delete(0, END)

        except:

            messagebox.showwarning(
                "Warning",
                "Roll Number Exists in the Database"
            )


# Close Screen
def close_screen():
    window.destroy()


# ---------------- TITLE ----------------

top_label = Label(
    window,
    text="Register a New User",
    fg="green",
    font=("helvetica", 20, "bold")
)
top_label.place(x=135, y=15)


# ---------------- ROLL NUMBER ----------------

display1 = Label(
    window,
    text="Roll No",
    fg="black",
    font=("helvetica", 16)
)
display1.place(x=50, y=70)

roll_no = Entry(
    window,
    fg="black",
    bd=4,
    width=35
)
roll_no.place(x=260, y=72)

roll_no.focus_set()


# ---------------- NAME ----------------

display2 = Label(
    window,
    text="Name",
    fg="black",
    font=("helvetica", 16)
)
display2.place(x=50, y=110)

name = Entry(
    window,
    fg="black",
    bd=4,
    width=35
)
name.place(x=260, y=112)


# ---------------- USERNAME ----------------

display3 = Label(
    window,
    text="Username",
    fg="black",
    font=("helvetica", 16)
)
display3.place(x=50, y=150)

username = Entry(
    window,
    fg="black",
    bd=4,
    width=35
)
username.place(x=260, y=152)


# ---------------- PASSWORD ----------------

display4 = Label(
    window,
    text="Password",
    fg="black",
    font=("helvetica", 16)
)
display4.place(x=50, y=190)

password = Entry(
    window,
    fg="black",
    bd=4,
    width=35
)
password.place(x=260, y=192)


# ---------------- SECURITY QUESTION ----------------

display5 = Label(
    window,
    text="Security Question",
    fg="black",
    font=("helvetica", 16)
)
display5.place(x=50, y=230)

security_question = Entry(
    window,
    fg="black",
    bd=4,
    width=35
)
security_question.place(x=260, y=232)


# ---------------- SECURITY ANSWER ----------------

display6 = Label(
    window,
    text="Security Answer",
    fg="black",
    font=("helvetica", 16)
)
display6.place(x=50, y=270)

security_answer = Entry(
    window,
    fg="black",
    bd=4,
    width=35
)
security_answer.place(x=260, y=272)


# ---------------- BUTTONS ----------------

btn2 = Button(
    window,
    text="Close",
    fg="white",
    bg="red",
    font=("helvetica", 12, "bold"),
    width=8,
    command=close_screen
)
btn2.place(x=240, y=340)


btn3 = Button(
    window,
    text="Register",
    fg="white",
    bg="green",
    font=("helvetica", 12, "bold"),
    width=8,
    command=register_new
)
btn3.place(x=350, y=340)


window.mainloop()