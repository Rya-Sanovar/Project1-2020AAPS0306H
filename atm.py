lines= []
file = open('database.txt', 'r')#in the database.txt always put a newline as your last line for this code to work.
lines = file.readlines()
list_length = len(lines)
file.close()
#all the constants used for clarity in loops
running = True
user_account_number_running = True
recipient_account_number_running = True
amount_running = True
pin_running = True
new_account_number_running = True
new_pin_running = True
recipient_account_number_found = False
user_account_number_found = False

class Account:
    def __init__(self, pin, current_balance, account_number):
        self.pin = pin
        self.current_balance = current_balance
        self.account_number = account_number

    def send_money(self, recipient, amount):
        self.current_balance = self.current_balance - amount
        recipient.current_balance = recipient.current_balance + amount

    def deposit_money(self, amount):
        self.current_balance += amount
        return self.current_balance
        
    def withdraw_money(self, amount):
        self.current_balance -= amount
        return self.current_balance

    def display(self):
        print(f"Your current balance is: Rs.{self.current_balance}")

#exception classes I made
class UserPressNotInRangeError(Exception):
    """Raised when user input is an integer but they don't press a number between a given inclusive range"""
    pass

class NegativeNumberError(Exception):
    """Raised when user input is a negative integer"""
    pass


def check_pin(index_of_pin):#can use this ONLY if your account_number is valid and available in database.
    while(pin_running):
        pin = input("Enter the pin: ")
        if lines[index_of_pin][:-1] == pin:
            return True
        else:
            print("Wrong pin.")
            continue

def change_money_in_account(user_press):#useful if user presses options 4 or 5
    while(user_account_number_running):
        try:
            user_account_number = int(input("Enter your account number: "))
            if user_account_number < 0:
                raise NegativeNumberError
        except ValueError:
            print("Please enter a valid account number consisting of only digits.")
            continue
        except NegativeNumberError:
            print("Please enter a positive account number.")
            continue

        user_account_number = str(user_account_number)

        for i in range(2, list_length, 5):
            if user_account_number + "\n" == lines[i]:
                user_account_number_found = True
                if check_pin(i - 1):
                    pin = lines[i - 1][:-1]
                    current_balance = int(lines[i + 1][:-1])
                    user = Account(pin, current_balance, user_account_number)
                    while(amount_running):
                        try:
                            if user_press == 4:
                                amount = int(input("Enter the amount to be deposited: "))
                            if user_press == 5:
                                amount = int(input("Enter the amount to be withdrawn: "))
                            if amount < 0:
                                raise NegativeNumberError
                            break 
                        except ValueError:
                            print("Please enter a amount value consisting of only digits.")
                            continue
                        except NegativeNumberError:
                            print("Please enter a positive amount value.")
                            continue
                    if user_press == 4:
                        user.deposit_money(amount)
                    if user_press == 5:
                        user.withdraw_money(amount)
                    lines[i + 1] = str(user.current_balance) + "\n"
                    file = open('database.txt','w')
                    file.writelines(lines)
                    file.close()
                break
        if user_account_number_found == False:
            print("This account number does not exist in database.")
            continue
        else:
            user_account_number_found = False
            break

while(running):
    print("****************************************")
    print("Press 1 to send money")
    print("Press 2 to create a new account")
    print("Press 3 to display your balance")
    print("Press 4 to deposit money")
    print("Press 5 to withdraw money")
    print("Press 6 to exit\n****************************************")

    try:
        user_press = int(input())
        if not 1 <= user_press <= 6:
            raise UserPressNotInRangeError
    except ValueError:
        print("\nPlease press a number only.")
        continue 
    except UserPressNotInRangeError:
        print("\nPlease press a number between 1 and 6 only.")
        continue
    #now we have a valid user press

    if user_press == 1:
        while(user_account_number_running):
            try:
                user_account_number = int(input("Enter your account number: "))
                if user_account_number < 0:
                    raise NegativeNumberError
            except ValueError:
                print("Please enter a valid account number consisting of only digits.")
                continue
            except NegativeNumberError:
                print("Please enter a positive account number.")
                continue

            user_account_number = str(user_account_number)

            for i in range(2, list_length, 5):
                if user_account_number + "\n" == lines[i]:
                    user_account_number_found = True
                    if check_pin(i - 1):
                        pin = lines[i - 1][:-1]
                        current_balance = int(lines[i + 1][:-1])
                        user = Account(pin, current_balance, user_account_number)

                        while(recipient_account_number_running):
                            try:
                                recipient_account_number = int(input("Enter the recipient account number: "))
                                if recipient_account_number < 0:
                                    raise NegativeNumberError
                            except ValueError:
                                print("Please enter a valid recipient account number consisting of only digits.")
                                continue
                            except NegativeNumberError:
                                print("Please enter a positive account number.")
                                continue
                            recipient_account_number = str(recipient_account_number)
                            for j in range(2, list_length, 5):
                                if recipient_account_number + "\n" == lines[j]:
                                    recipient_account_number_found = True
                                    pin = lines[j - 1][:-1]
                                    current_balance = int(lines[j + 1][:-1])
                                    recipient = Account(pin, current_balance, recipient_account_number)
                                        
                                    while(amount_running):
                                        try:
                                            amount = int(input("Enter the amount to be transferred: "))
                                            if amount < 0:
                                                raise NegativeNumberError
                                            break 
                                        except ValueError:
                                            print("Please enter a amount value consisting of only digits.")
                                            continue
                                        except NegativeNumberError:
                                            print("Please enter a positive amount value.")
                                            continue
                                        
                                    user.send_money(recipient, amount)
                                    lines[j + 1] = str(recipient.current_balance) + "\n"
                                    lines[i + 1] = str(user.current_balance) + "\n"
                                    file = open('database.txt', 'w')
                                    file.writelines(lines)
                                    file.close()
                                    break
                            if recipient_account_number_found == False:
                                print("Recipient account number does not exist in database.")
                                continue
                            else:
                                recipient_account_number_found = False
                                break

            if user_account_number_found == False:
                print("User account number does not exist in database.")
                continue
            else:
                user_account_number_found = False
                break
        continue

    elif user_press == 2:
        while(new_account_number_running):    
            try:
                new_account_number = int(input("Enter your new account number: "))
                if new_account_number < 0:
                    raise NegativeNumberError
                break 
            except ValueError:
                print("Please enter an account number consisting of only digits.")
                continue
            except NegativeNumberError:
                print("Please enter a positive account number.")
                continue
        new_account_number = str(new_account_number)
        #now we have a valid new account number.

        while(new_pin_running):    
            try:
                new_pin = int(input("Make a new pin(consisting of only 4 digits): "))
                if new_pin < 0:
                    raise NegativeNumberError
                if not 1000 < new_pin < 9999:
                    raise UserPressNotInRangeError
                break 
            except ValueError:
                print("Please enter a pin consisting of only 4 digits.")
                continue
            except NegativeNumberError:
                print("Please enter a positive pin only.")
                continue
            except UserPressNotInRangeError:
                print("Please enter a 4 digit pin only.")
        new_pin = str(new_pin)
        #now we have a valid pin number

        while(amount_running):    
            try:
                new_balance = int(input("Enter amount you want to store in this account: "))
                if new_balance < 0:
                    raise NegativeNumberError
                break 
            except ValueError:
                print("Please enter a balance amount consisting of only digits.")
                continue
            except NegativeNumberError:
                print("Please enter a positive balance.")
                continue
        new_balance = str(new_balance)
        #now we have a valid new balance

        lines.append("\n")
        number_of_users = int((list_length + 1)/5) + 1
        number_of_users = str(number_of_users) #current number of users including new user account.
        lines.append(f"User{number_of_users}\n")
        lines.append(f"{new_pin}\n")
        lines.append(f"{new_account_number}\n")
        lines.append(f"{new_balance}\n")
        file = open('database.txt', 'w')
        file.writelines(lines)
        file.close()
        #all new changes made in text file.
        continue
    
    elif user_press == 3:
        while(user_account_number_running):
            try:
                user_account_number = int(input("Enter your account number: "))
                if user_account_number < 0:
                    raise NegativeNumberError
            except ValueError:
                print("Please enter a valid account number consisting of only digits.")
                continue
            except NegativeNumberError:
                print("Please enter a positive account number.")
                continue

            user_account_number = str(user_account_number)

            for i in range(2, list_length, 5):
                if user_account_number + "\n" == lines[i]:
                    user_account_number_found = True
                    if check_pin(i - 1):
                        pin = lines[i - 1][:-1]
                        current_balance = lines[i + 1][:-1]
                        user = Account(pin, current_balance, user_account_number)
                        user.display()
                        break
            if user_account_number_found == False:
                print("This account number does not exist in database.")
                continue
            else:
                user_account_number_found = True
                break
        continue
            
    elif user_press == 4 or user_press == 5:
        change_money_in_account(user_press)
        continue

    elif user_press == 6:
        file.close()
        print("Thank you for visiting the ATM!")
        break
