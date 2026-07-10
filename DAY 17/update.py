from tkinter import *
from tkinter import messagebox
import mysql.connector

window=Tk()
window.title("Registration Form")
window.geometry("500x220+490+200")
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
    n_p=new_password.get()


    if r=="" or n_p=="":
        messagebox.showinfo("Warning","All Field must be Filled")
    else:
        try:
            sql="UPDATE registration SET Password=%s WHERE Roll_no=%s"
            values=(n_p,r)
            cursor.execute(sql,values)
            con.commit() #Save the Changes Permanetly in Database 

            roll_no.delete(0,END)
            new_password.delete(0,END)

            if cursor.rowcount>0:
                messagebox.showinfo("Sucess","Password reset Sucessfully !!")
                roll_no.focus_set()
            else:
                messagebox.showinfo("Warning","Roll No is Not Available in Database") 
                roll_no.focus_set()
        except:
            messagebox.showinfo("Warning","Database Error")




def close_screen():
    window.destroy()

top_label=Label(window,text="Update Password",fg='Blue',font=("helvetica",20,"bold"))
top_label.place(x=140,y=15)

display1=Label(window,text="Roll No",fg='Black',font=("helvetica",16))
display1.place(x=80,y=70)
roll_no=Entry(window,fg="black",bd=4,width=35)
roll_no.place(x=220,y=72)
roll_no.focus_set()

display2=Label(window,text="New Password",fg='Black',font=("helvetica",16))
display2.place(x=60,y=110)
new_password=Entry(window,fg="black",bd=4,width=35)
new_password.place(x=220,y=112)


btn2=Button(window,text="Close",fg='white',bg='red',font=("helvetica",12,"bold"),width=8,command=close_screen)
btn2.place(x=250,y=160)

btn3=Button(window,text="Update",fg='White',bg='green',font=("helvetica",12,"bold"),width=8,command=register_new)
btn3.place(x=360,y=160)

window.mainloop()