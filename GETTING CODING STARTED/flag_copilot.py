# Program to print a flag pattern based on user input

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a number.")

width = get_positive_int("Flag width:\n")
height = get_positive_int("Flag height:\n")

for row in range(height):
    if row < height // 2:
        # Top half: half '#' and half '-'
        line = '#' * (width // 2) + '-' * (width - (width // 2))
    else:
        # Bottom half: all '-'
        line = '-' * width
    print(line)