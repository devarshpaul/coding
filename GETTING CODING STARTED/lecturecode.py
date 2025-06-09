gpa=float(input("Enter your GPA: "))
instapp=input("Are you applying to an institution? (yes/no): ")
if gpa >= 3.7:
    if instapp=="yes":
        print("The applicant is elligible for a low APR student loan")
    else:
        print("The applicant does not qualify as they have not been acepted into an approved institution")
else:
    print("The applicant needs to improve their GPA to be eligible for a low APR student loan")
