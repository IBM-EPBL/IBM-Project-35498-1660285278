#getting input 1
num1 = int(input("Enter 1st number:"))

#getting operator
op = input("+ or - or * or /")

#getting input 2
num2 = int(input("Enter 2nd number:"))

#addition
if (op == "+"):
    print(num1+num2)

#subtraction
elif (op == "-"):
    print(num1-num2)

#multiplication
elif (op == "*"):
    print(num1*num2)

#division
elif (op == "/"):
    print(num1/num2)
