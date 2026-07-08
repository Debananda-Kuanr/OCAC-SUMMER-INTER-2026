from tkinter import *

window=Tk()
window.title("Finance Management Software")
window.geometry("600x670+500+50")
window.resizable(False,False)


def calculation():
    income1 = int(inc_mon.get())
    income2 = int(inc_tue.get())
    income3 = int(inc_wed.get())
    income4 = int(inc_thu.get())
    income5 = int(inc_fri.get())
    income6 = int(inc_sat.get())
    income7 = int(inc_sun.get())

    expense1 = int(exp_mon.get())
    expense2 = int(exp_tue.get())
    expense3 = int(exp_wed.get())
    expense4 = int(exp_thu.get())
    expense5 = int(exp_fri.get())
    expense6 = int(exp_sat.get())
    expense7 = int(exp_sun.get())

    total_income =income1 + income2 + income3 +income4 + income5 + income6 +income7
    total_expense = expense1 + expense2 + expense3 + expense4 + expense5 + expense6 + expense7
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