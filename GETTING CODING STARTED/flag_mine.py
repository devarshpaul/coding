width = input("Flag width:\n")
width = int(width)
height = input("Flag height:\n")
height = int(height)
print((('#'*int(width/2)+'-'*int((width/2)-1)+'-\n')*int(height/2))+('-'*int(width-1)+'-\n')*int(height/2))
