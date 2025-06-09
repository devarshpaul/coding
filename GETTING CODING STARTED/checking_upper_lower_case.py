text=input("Type some text and then press enter: ")
upper_count=0
lower_count=0
for i in range(0, len(text)):
    char=text[i]
    if char.isupper():
        upper_count+=1
    elif char.islower():
        lower_count+=1
print("Number of uppercase letters: ", upper_count)
print("Number of lowercase letters: ", lower_count)