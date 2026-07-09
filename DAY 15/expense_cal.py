from tkinter import *
from tkinter import messagebox

window=Tk()
window.title("Finance Management Software")
window.geometry("600x670+500+50")
window.resizable(False,False)


def calculation():
    income1 = inc_mon.get()
    income2 = inc_tue.get()
    income3 = inc_wed.get()
    income4 = inc_thu.get()
    income5 = inc_fri.get()
    income6 = inc_sat.get()
    income7 = inc_sun.get()

    expense1 = exp_mon.get()
    expense2 = exp_tue.get()
    expense3 = exp_wed.get()
    expense4 = exp_thu.get()
    expense5 = exp_fri.get()
    expense6 = exp_sat.get()
    expense7 = exp_sun.get()


    if len(inc_mon.get())==0 and len(inc_tue.get())==0 and len(inc_wed.get())==0 and len(inc_thu.get())==0 and len(inc_fri.get())==0 and len(inc_sat.get())==0 and len(inc_sun.get())==0 and len(exp_mon.get())==0 and len(exp_tue.get())==0 and len(exp_wed.get())==0 and len(exp_thu.get())==0 and len(exp_fri.get())==0 and len(exp_sat.get())==0 and len(exp_sun.get())==0:
        messagebox.showinfo("Warning","All Fields are blank\nAll Must be Filled")

    elif len(inc_mon.get())==0 :
        messagebox.showinfo("Warning","Mon- Income Field is Blank\nPlease Enter")
    elif len(inc_tue.get())==0 :
        messagebox.showinfo("Warning","Tue- Income Field is Blank\nPlease Enter")
    elif len(inc_wed.get())==0 :
        messagebox.showinfo("Warning","Wed- Income Field is Blank\nPlease Enter")
    elif len(inc_thu.get())==0 :
        messagebox.showinfo("Warning","Thu- Income Field is Blank\nPlease Enter")
    elif len(inc_fri.get())==0 :
        messagebox.showinfo("Warning","Fri- Income Field is Blank\nPlease Enter")
    elif len(inc_sat.get())==0 :
        messagebox.showinfo("Warning","Sat- Income Field is Blank\nPlease Enter")
    elif len(inc_sun.get())==0 :
        messagebox.showinfo("Warning","Sun- Income Field is Blank\nPlease Enter")
    elif len(exp_mon.get())==0 :
        messagebox.showinfo("Warning","Mon- Expense Field is Blank\nPlease Enter")
    elif len(exp_tue.get())==0 :
        messagebox.showinfo("Warning","Tue- Expense Field is Blank\nPlease Enter")
    elif len(exp_wed.get())==0 :
        messagebox.showinfo("Warning","Wed- Expense Field is Blank\nPlease Enter")
    elif len(exp_thu.get())==0 :
        messagebox.showinfo("Warning","Thu- Expense Field is Blank\nPlease Enter")
    elif len(exp_fri.get())==0 :
        messagebox.showinfo("Warning","Fri- Expense Field is Blank\nPlease Enter")
    elif len(exp_sat.get())==0 :
        messagebox.showinfo("Warning","Sat- Expense Field is Blank\nPlease Enter")
    elif len(exp_sun.get())==0 :
        messagebox.showinfo("Warning","Sun- Expense Field is Blank\nPlease Enter")
    elif int(income1)<0 :
        messagebox.showinfo("Warning","Mon- Income Must be Greater than 0")
    elif int(income2)<0 :
        messagebox.showinfo("Warning","Tue- Income Must be Greater than 0")
    elif int(income3)<0 :
        messagebox.showinfo("Warning","Wed- Income Must be Greater than 0")
    elif int(income4)<0 :
        messagebox.showinfo("Warning","Thu- Income Must be Greater than 0")
    elif int(income5)<0 :
        messagebox.showinfo("Warning","Fri- Income Must be Greater than 0")
    elif int(income6)<0 :
        messagebox.showinfo("Warning","Sat- Income Must be Greater than 0")
    elif int(income7)<0 :
        messagebox.showinfo("Warning","Sun- Income Must be Greater than 0")
    elif int(expense1)<0:
        messagebox.showinfo("Warning","Mon- Expense Must be Greater than 0")
    elif int(expense2)<0:
        messagebox.showinfo("Warning","Tue- Expense Must be Greater than 0")
    elif int(expense2)<0:
        messagebox.showinfo("Warning","Wed- Expense Must be Greater than 0")
    elif int(expense4)<0:
        messagebox.showinfo("Warning","Thu- Expense Must be Greater than 0")
    elif int(expense5)<0:
        messagebox.showinfo("Warning","Fri- Expense Must be Greater than 0")
    elif int(expense6)<0:
        messagebox.showinfo("Warning","Sat- Expense Must be Greater than 0")
    elif int(expense7)<0:
        messagebox.showinfo("Warning","Sun- Expense Must be Greater than 0")
    
    else:
        total_income =int(income1) + int(income2) + int(income3) +int(income4) + int(income5) + int(income6) +int(income7)
        total_expense = int(expense1) + int(expense2) + int(expense3) + int(expense4) + int(expense5) + int(expense6) + int(expense7)
        total_savings = total_income - total_expense

        total_inc.delete(0,END)
        total_exp.delete(0,END)
        avl_bal.delete(0,END)
        total_inc.insert(1,str(total_income))
        total_exp.insert(1,str(total_expense))
        avl_bal.insert(1,str(total_savings))


top_label=Label(window,text="Income Expense Management",fg='green',font=("helvetica",20,"bold"))
top_label.place(x=100,y=20)

head_1=Label(window,text="Days",fg='Blue',font=("helvetica",15,"bold"))
head_1.place(x=70,y=100)

head_1=Label(window,text="Incomes",fg='Blue',font=("helvetica",15,"bold"))
head_1.place(x=235,y=100)

head_1=Label(window,text="Expense",fg='Blue',font=("helvetica",15,"bold"))
head_1.place(x=415,y=100)


# Monday
monday = Label(window, text="Monday: ", fg="Black", font=("helvetica", 14))
monday.place(x=70, y=150)
inc_mon = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
inc_mon.place(x=210, y=150)
exp_mon = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
exp_mon.place(x=400, y=150)

# Tuesday
tuesday = Label(window, text="Tuesday: ", fg="Black", font=("helvetica", 14))
tuesday.place(x=70, y=190)
inc_tue = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
inc_tue.place(x=210, y=190)
exp_tue = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
exp_tue.place(x=400, y=190)

# Wednesday
wednesday = Label(window, text="Wednesday: ", fg="Black", font=("helvetica", 14))
wednesday.place(x=70, y=230)
inc_wed = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
inc_wed.place(x=210, y=230)
exp_wed = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
exp_wed.place(x=400, y=230)

# Thursday
thursday = Label(window, text="Thursday: ", fg="Black", font=("helvetica", 14))
thursday.place(x=70, y=270)
inc_thu = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
inc_thu.place(x=210, y=270)
exp_thu = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
exp_thu.place(x=400, y=270)

# Friday
friday = Label(window, text="Friday: ", fg="Black", font=("helvetica", 14))
friday.place(x=70, y=310)
inc_fri = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
inc_fri.place(x=210, y=310)
exp_fri = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
exp_fri.place(x=400, y=310)

# Saturday
saturday = Label(window, text="Saturday: ", fg="Black", font=("helvetica", 14))
saturday.place(x=70, y=350)
inc_sat = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
inc_sat.place(x=210, y=350)
exp_sat = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
exp_sat.place(x=400, y=350)

# Sunday
sunday = Label(window, text="Sunday: ", fg="Black", font=("helvetica", 14))
sunday.place(x=70, y=390)
inc_sun = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
inc_sun.place(x=210, y=390)
exp_sun = Entry(window, fg="black", bd=4, width=14, font=("helvetica", 12))
exp_sun.place(x=400, y=390)

# Button For Calculate
calculate_btn=Button(window,text="Calculate All Payments ",fg='White',bg='green',font=("helvetica",14,"bold"),width=37,command=calculation)
calculate_btn.place(x=76, y=450)

# Here we will Show the Total income and Expense

output=Label(window,text="Total\nIncome:",fg='Blue',font=("helvetica",15,"bold"))
output.place(x=70,y=520)
total_inc = Entry(window, fg="black",bg="yellow", bd=1, width=10, font=("helvetica", 15,"bold"))
total_inc.place(x=160, y=540)

output=Label(window,text="Total\nExpense:",fg='Blue',font=("helvetica",15,"bold"))
output.place(x=312,y=520)
total_exp = Entry(window, fg="black",bg="yellow", bd=1, width=10, font=("helvetica", 15,"bold"))
total_exp.place(x=415, y=540)

# Available Balance

output=Label(window,text="Available Balance : ",fg='green',font=("helvetica",17,"bold"))
output.place(x=70,y=600)

avl_bal = Entry(window, fg="black",bg="yellow", bd=1, width=19, font=("helvetica", 16,"bold"))
avl_bal.place(x=300, y=602)

window.mainloop()