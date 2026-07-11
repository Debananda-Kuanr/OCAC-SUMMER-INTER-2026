from tkinter import *
from tkinter import messagebox
import mysql.connector


window = Tk()
window.title("Forgot Password")
window.geometry("500x310+490+200")
window.resizable(False, False)


# Database Connection With Python
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9439",
    database="OCAC"
)

cursor = con.cursor()


# VERIFY ROLL NUMBER

def verify_roll():

    global user_name
    global user_password
    global correct_answer

    r = roll_no.get()

    if r == "":

        messagebox.showwarning(
            "Warning",
            "Enter Roll Number"
        )

    else:

        try:

            sql = """
            SELECT Name, Password, Security_Question, Security_Answer
            FROM registration
            WHERE Roll_No=%s
            """

            values = (r,)

            cursor.execute(sql, values)
            result = cursor.fetchone()
            if result:

                user_name = result[0]
                user_password = result[1]
                user_question = result[2]
                correct_answer = result[3]

                display1.place_forget()
                roll_no.place_forget()
                verify_btn.place_forget()

                question_label["text"] = user_question

                question_title.place(x=50, y=90)
                question_label.place(x=50, y=125)

                # Show Answer Field
                answer_display.place(x=50, y=170)
                security_answer.place(x=220, y=172)

                # Show Verify Answer Button
                answer_btn.place(x=185, y=230)

            else:

                messagebox.showerror(
                    "Error",
                    "Roll Number Not Found"
                )

        except:

            messagebox.showerror(
                "Error",
                "Database Error"
            )


# VERIFY SECURITY ANSWER 

def verify_answer():

    answer = security_answer.get()

    if answer == "":

        messagebox.showwarning(
            "Warning",
            "Enter Security Answer"
        )

    elif answer.lower() == correct_answer.lower():

        messagebox.showinfo(
            "Success",
            "Answer Verified Successfully"
        )

        question_title.place_forget()
        question_label.place_forget()

        answer_display.place_forget()
        security_answer.place_forget()

        answer_btn.place_forget()

        welcome_label["text"] = "Welcome Back " + user_name + "!"
        welcome_label.place(x=50, y=110)

        password_label["text"]="Your Password is: " + user_password
        
        password_label.place(x=50, y=165)


        close_btn.place(x=205, y=230)

    else:

        messagebox.showerror(
            "Error",
            "Incorrect Security Answer"
        )


# CLOSE SCREEN 

def close_screen():
    window.destroy()


# TITLE

top_label = Label(
    window,
    text="Forgot Password",
    fg="green",
    font=("helvetica", 20, "bold")
)

top_label.place(x=135, y=25)


# ROLL NUMBER

display1 = Label(
    window,
    text="Roll No",
    fg="black",
    font=("helvetica", 16)
)

display1.place(x=80, y=115)


roll_no = Entry(
    window,
    fg="black",
    bd=4,
    width=30
)

roll_no.place(x=190, y=117)

roll_no.focus_set()


# VERIFY ROLL BUTTON 

verify_btn = Button(
    window,
    text="Verify",
    fg="white",
    bg="green",
    font=("helvetica", 12, "bold"),
    width=10,
    command=verify_roll
)

verify_btn.place(x=195, y=180)


# SECURITY QUESTION 
# These will appear after Roll Number verification

question_title = Label(
    window,
    text="Security Question",
    fg="blue",
    font=("helvetica", 14, "bold")
)


question_label = Label(
    window,
    text="",
    fg="black",
    font=("helvetica", 13)
)


# SECURITY ANSWER

answer_display = Label(
    window,
    text="Your Answer",
    fg="black",
    font=("helvetica", 16)
)


security_answer = Entry(
    window,
    fg="black",
    bd=4,
    width=25
)


# VERIFY ANSWER BUTTON 

answer_btn = Button(
    window,
    text="Verify Answer",
    fg="white",
    bg="green",
    font=("helvetica", 12, "bold"),
    width=12,
    command=verify_answer
)


# WELCOME MESSAGE
# These will appear after correct security answer

welcome_label = Label(
    window,
    text="",
    fg="green",
    font=("helvetica", 18, "bold")
)


password_label = Label(
    window,
    text="",
    fg="blue",
    font=("helvetica", 16, "bold")
)


# CLOSE BUTTON

close_btn = Button(
    window,
    text="Close",
    fg="white",
    bg="red",
    font=("helvetica", 12, "bold"),
    width=8,
    command=close_screen
)


window.mainloop()