pin=1234
bank_Bal=10000
username="Debananda Kuanr"
attempt=0

print("-----Mini ATM System-----")
while attempt < 3:
    print()
    User_pin = int(input("Enter Your Pin: "))

    if pin == User_pin:
        print(f"\nWelcome {username}!")
        while 1:
            print("1. Withdraw\n2. Deposite\n3. Check Balance\n4. Exit")
            choice=int(input("Please Enter:"))
            if choice==1:
                while 1:
                    wid_Amt=int(input("Enter Withdraw Amount: "))
                    if wid_Amt==0:
                        print("Invalid Amount")
                    elif 0<wid_Amt<=bank_Bal and wid_Amt%100==0:
                        bank_Bal-=wid_Amt
                        print(f"\n{wid_Amt} Rupees Withdraw Sucessful....")
                        print(f"-------Recipt-------\nUser:{username}\n\nWithdraw Amt:{wid_Amt}\nAvl. Amt:{bank_Bal}\nMini ATM,Thankyou\n--------------------\n")
                        break
                    elif wid_Amt>bank_Bal:
                        print("Your Current Balance is",bank_Bal,"\n")
                    else:
                        print("Invalid Withdraw Amount.\n")
            elif choice==2:
                while 1:
                    dep_Amt=int(input("Enter Deposite Amount: "))
                    if dep_Amt==0:
                        print("Invalid Amount")
                    elif dep_Amt>0 and dep_Amt%100==0:
                        bank_Bal+=dep_Amt
                        print(f"\n{dep_Amt} Rupees Deposite Sucessful....")
                        print(f"-------Recipt-------\nUser:{username}\n\nDeposite Amt:{dep_Amt}\nAvl. Amt:{bank_Bal}\nMini ATM,Thankyou\n--------------------\n")
                        break
                    else:
                        print("Invalid Deposite Amount.\n")
            elif choice==3:
                print(f"\n-------Recipt-------\nUser:{username}\nAvl. Amt:{bank_Bal}\nMini ATM,Thankyou\n--------------------\n")
            elif choice==4:
                print("Thankyou from MINI ATM Service\n")
                break
            else:
                print("Invalid Choice\n")
        break
    else:
        attempt += 1
        if attempt == 3:
            print("Account Blocked\nContact to Bank Authority")
            
        else:
            print("Incorrect Password,Try Again.... \nAttempts left:", 3 - attempt)
