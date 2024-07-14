import random
import pywhatkit
from datetime import datetime
import contextlib
import io

class Bank:
    cust_cnt = 0  # class attribute to manage the customer count
    __cust_details = list()

    def __init__(self, name, age, balance, acc_no, phone_no):
        self.name = name
        self.age = age
        self.__balance = balance  # creating a private attribute balance for each instance
        self.__pin = 1234  # Default pin set to 1234
        Bank.cust_cnt += 1  # incrementing customer count after each instance creating
        self.acc_no = acc_no
        self.phone_no = phone_no
        # storing individual instances into the list
        Bank.__cust_details.append(self)

    def get_balance(self, pin_required=True):
        if not pin_required or self.__verify_pin():
            return self.__balance
        else:
            print("Invalid pin")

    def __debit_balance(self, pin_required=True):
        if not pin_required or self.__verify_pin():
            amt = int(input("Enter the amount to Debit: "))
            if self.__balance > amt:
                self.__balance -= amt
                print(f"Transaction of {amt} is successful")
            else:
                print("Insufficient Balance")
        else:
            print("Invalid Pin")

    def __credit_balance(self, pin_required=True):
        if not pin_required or self.__verify_pin():
            amt = int(input("Enter the amount to Credit: "))
            if amt >= 0:
                self.__balance += amt
                print(f"Credited {amt} successfully")
            else:
                print("Invalid amount")
        else:
            print("Invalid pin")
        
    def __pin_gen(self):
        pin = int(input("Enter New 4 digit Pin: "))
        self.__pin = pin
        print("Pin set successfully")

    def __generate_otp(self):
        return random.randint(1000, 9999)

    def __send_otp(self, otp):
        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute + 1

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            pywhatkit.sendwhatmsg(f"+{self.phone_no}", f"Your OTP is: {otp}", current_hour, current_minute)
        print("OTP sent successfully!")

    def __verify_pin(self):
        pin = int(input("Enter Pin: "))
        print(f"Entered PIN: {pin}, Stored PIN: {self.__pin}")  
        return pin == self.__pin

    @classmethod 
    def atm_op(cls):
        account_no = int(input("Enter your account number: "))
        check = False
        for i in Bank.__cust_details:
            if account_no == i.acc_no:
                check = True
                print('''Select login method:
                      1. Login via account number and PIN
                      2. Login via OTP
                      ''')
                login_choice = int(input("Enter choice: "))
                if login_choice == 1:
                    if not i.__verify_pin():
                        print("Invalid PIN!")
                        return
                elif login_choice == 2:
                    otpw = i.__generate_otp()
                    i.__send_otp(otpw)
                    entered_otp = int(input("Enter the OTP sent to your WhatsApp: "))
                    if entered_otp != otpw:
                        print("Invalid OTP!")
                        return
                    else:
                        print("OTP verified successfully!")
                else:
                    print("Invalid choice!")
                    return

                while True:
                    print(''' Enter the transaction to perform:
                          press 1 for pin generate 
                          press 2 for withdraw
                          press 3 for Credit
                          press 4 for Balance enquiry
                          press 5 for exit
                          ''')
                    choice = int(input("Enter choice: "))
                    if choice == 1:
                        i.__pin_gen()
                    elif choice == 2:
                        i.__debit_balance(pin_required=(login_choice == 1))
                    elif choice == 3:
                        i.__credit_balance(pin_required=(login_choice == 1))
                    elif choice == 4:
                        balance = i.get_balance(pin_required=(login_choice == 1))
                        if balance is not None:
                            print("Balance:", balance)
                    else:
                        print(f"Thank you {i.name} for the transaction")
                        print("Exit")
                        break
        if not check:
            print("Customer Not found")

# All the account holders   
cust1 = Bank("Abhishek", 20, 65000, 1234, "9100000000")
cust2 = Bank("Suman", 19, 98000, 2255, "9100000001")
cust3 = Bank("Suvadwip", 19, 80000, 9785, "9100000002")
cust4 = Bank("Soumajit", 19, 365000, 3364, "9100000003")
cust5 = Bank("Souvick", 19, 67000, 9999, "9100000004")
cust6 = Bank("Arnab", 19, 99000, 7456, "9100000005")
cust7 = Bank("Akash", 19, 123000, 5064, "+919798948639")
cust8 = Bank("Sumit", 20, 90000, 11123, "9100000007")
cust9 = Bank("Arvind", 20, 55000, 34568, "9100000008")

Bank.atm_op()
