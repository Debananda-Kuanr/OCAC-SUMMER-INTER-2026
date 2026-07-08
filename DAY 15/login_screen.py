from tkinter import *

window=Tk()
window.title("Login")
window.geometry("350x350+600+200")
window.resizable(False,False)

def login_sys():
    default_username = "ram"
    default_password = "ram123"

    user_username = username.get()
    user_password = password.get()

    if user_username == default_username and user_password == default_password:
        my_status = "           Login Successful !!"
    elif user_username != default_username and user_password != default_password:
        my_status = "Invalid Username and Password"
    elif user_username != default_username:
        my_status = "  Invalid Username !!"
    else:
        my_status = "  Invalid Password !!"

    status.delete(0, END)
    status.insert(0, my_status)
def clear_screen():
    username.delete(0,END)
    password.delete(0,END)
    status.delete(0, END)

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


btn1=Button(window,text="Clear",fg='White',bg='red',font=("helvetica",12,"bold"),width=8,command=clear_screen)
btn1.place(x=80,y=270)
btn2=Button(window,text="Login",fg='White',bg='green',font=("helvetica",12,"bold"),width=8,command=login_sys)
btn2.place(x=190,y=270)

window.mainloop()
