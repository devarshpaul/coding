value1=int(input("Enter a starting number: "))
value2=int(input("Enter a ending number: "))
divide=int(input("What number to check divisibility for: "))
num=value1
while num <= value2:
    if num % divide == 0:
        print(num, "is divisible by", divide)
    num+=1