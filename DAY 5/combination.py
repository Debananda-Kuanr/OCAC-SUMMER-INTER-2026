while True:
    Amt_500,Amt_100,Amt_200=0,0,0
    org_Amount= int(input("\nEnter the Amount:"))
    Amount=org_Amount
    if Amount==0:
        print("Code Terminated...")
        break
    if Amount%100== 0:
        print("Combination 1:")
        if Amount>=500:
            Amt_500=Amount//500
            Amount=Amount-Amt_500*500
        if Amount>=200:
            Amt_200=Amount//200
            Amount=Amount-Amt_200*200
        if Amount>=100:
            Amt_100=Amount//100
            Amount=Amount-Amt_100*100
        print("500 Rupees:",Amt_500)
        print("200 Rupees:",Amt_200)
        print("100 Rupees:",Amt_100)
    
        Amt_500,Amt_100,Amt_200=0,0,0
        Amount=org_Amount
        print()
        print("Combination 2:")
        if Amount>=200:
            Amt_200=Amount//200
            Amount=Amount-Amt_200*200
    
        if Amount>=100:
            Amt_100=Amount//100
            Amount=Amount-Amt_100*100
        if Amount>=500:
            Amt_500=Amount//500
            Amount=Amount-Amt_500*500
        print("200 Rupees:",Amt_200)
        print("500 Rupees:",Amt_500)
        print("100 Rupees:",Amt_100)


        Amt_500,Amt_100,Amt_200=0,0,0
        Amount=org_Amount
        print()
        print("Combination 3:")
        if Amount>=100:
            Amt_100=Amount//100
            Amount=Amount-Amt_100*100
        if Amount>=200:
            Amt_200=Amount//200
            Amount=Amount-Amt_200*200
    
        if Amount>=500:
            Amt_500=Amount//500
            Amount=Amount-Amt_500*500
        print("200 Rupees:",Amt_200)
        print("500 Rupees:",Amt_500)
        print("100 Rupees:",Amt_100)    
    else:
        print("Invalid Amount")
