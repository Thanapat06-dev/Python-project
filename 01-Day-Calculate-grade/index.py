while True:
    try:
        score = int(input("Enter your score ('00' for exit): "))

        if score == 00:
            break

        if 0 <= score <= 100:
            if score >= 80:
                grade = 'A'
            elif score >= 70:
                grade = 'B'
            elif score >= 60:
                grade = 'C'
            elif score >= 50:
                grade = 'D'
            else:
                grade = 'F'

            print(f'Your score is {score} and Your grade is: {grade}')
        else:
            print('Enter score betwen 0-100!')
    except ValueError:
        print('Please enter only number!')