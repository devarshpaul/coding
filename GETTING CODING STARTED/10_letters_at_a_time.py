sentence = 'There once lived a bee in a house by the sea'
position = 0
while position <= len(sentence)-10:
    index = position
    while index < position+10:
        print(sentence[index], end='')
        index += 1
    print()
    position += 1