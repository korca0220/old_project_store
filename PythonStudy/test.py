while(1):
    print("")
    num = input("Enter num :")
    n = input("Enter n :")

    if not num.isdigit() or n.isdigit() == False:
        print(n.isdigit())
    elif n == "0":
        print("Invalid")
    else:
        n= int(n)
        num=int(num)
        for i in range(1, n+1):
            result = i * num
            print("%d * %s = %d" % (i, num, result))
