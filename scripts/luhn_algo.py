# Description
# In this stage, we will find out what the purpose of the checksum is and what the Luhn algorithm is used for.
# The main purpose of the check digit is to verify that the card number is valid. 
# Say you're buying something online, and you type in your credit card number incorrectly by accidentally swapping two digits, 
# which is one of the most common errors. 
# When the website looks at the number you've entered and applies the Luhn algorithm to the first 15 digits, 
# the result won't match the 16th digit on the number you entered. 
# The computer knows the number is invalid, and it knows the number will be rejected if it tries to submit the purchase for approval, 
# so you're asked to re-enter the number. 
# Another purpose of the check digit is to catch clumsy attempts to create fake credit card numbers. 
# Those who are familiar with the Luhn algorithm, however, could get past this particular security measure.
#
# Luhn Algorithm in action
# The Luhn algorithm is used to validate a credit card number or other identifying numbers, 
# such as Social Security. The Luhn algorithm, also called the Luhn formula or modulus 10, 
# checks the sum of the digits in the card number and checks whether the sum matches the expected result 
# or if there is an error in the number sequence. After working through the algorithm, 
# if the total modulus 10 equals zero, then the number is valid according to the Luhn method.
# While the algorithm can be used to verify other identification numbers, 
# it is usually associated with credit card verification. The algorithm works for all major credit cards.
# Here is how it works for a credit card with the number 4000008449433403:
# If the received number is divisible by 10 with the remainder equal to zero, then this number is valid; 
# otherwise, the card number is not valid. When registering in your banking system, 
# you should generate cards with numbers that are checked by the Luhn algorithm. 
# You know how to check the card for validity. But how do you generate a card number so that it passes the validation test? 
# It's very simple!
# First, we need to generate an Account Identifier, which is unique to each card. 
# Then we need to assign the Account Identifier to our BIN (Bank Identification Number). 
# As a result, we get a 15-digit number 400000844943340, so we only have to generate the last digit, which is a checksum.
# To find the checksum, it is necessary to find the control number for 400000844943340 by the Luhn algorithm. 
# It equals 57 (from the example above). The final check digit of the generated map is 57+X, where X is checksum. 
# In order for the final card number to pass the validity check, 
# the check number must be a multiple of 10, so 57+X must be a multiple of 10. The only number that satisfies this condition is 3.
# Therefore, the checksum is 3. So the total number of the generated card is 4000008449433403. 
# The received card is checked by the Luhn algorithm.
# You need to change the credit card generation algorithm so that they pass the Luhn algorithm.
# 
# Instruction
# You should allow customers to create a new account in our banking system.
# Once the program starts you should print the menu:
#   1. Create an account
#   2. Log into account
#   0. Exit
# If the customer chooses ‘Create an account’, you should generate a new card number that satisfies all the conditions described above. 
# Then you should generate a PIN code that belongs to the generated card number. 
# PIN is a sequence of 4 digits; it should be generated in the range from 0000 to 9999.
# If the customer chooses ‘Log into account’, you should ask to enter card information.
# After the information has been entered correctly, you should allow the user to check the account balance; 
# after creating the account, the balance should be 0. It should also be possible to log out of the account and exit the program.
#
# Example
# The symbol > represents the user input. 
# Notice that it's not a part of the input.
# 1. Create an account
# 2. Log into account
# 0. Exit
# >1
# 
# Your card has been created
# Your card number:
# 4000004938320896
# Your card PIN:
# 6826
# 
# 1. Create an account
# 2. Log into account
# 0. Exit
# >2
# 
# Enter your card number:
# >4000004938320896
# Enter your PIN:
# >4444
# 
# Wrong card number or PIN!
# 
# 1. Create an account
# 2. Log into account
# 0. Exit
# >2
# 
# Enter your card number:
# >4000004938320896
# Enter your PIN:
# >6826
# 
# You have successfully logged in!
# 
# 1. Balance
# 2. Log out
# 0. Exit
# >1
# 
# Balance: 0
# 
# 1. Balance
# 2. Log out
# 0. Exit
# >2
# 
# You have successfully logged out!
# 
# 1. Create an account
# 2. Log into account
# 0. Exit
# >0
# 
# Bye!

import sys
import random

MENU_UNSUPPORTED_OPTION_MSG = 'Sorry, that option is unsupported!'
MENU_EXIT_MSG = 'Bye!'
LOGIN_CARD_MSG = 'Enter your card number:\n'
LOGIN_PIN_MSG = 'Enter your PIN:\n'
LOGIN_SUCCES = '\nYou have successfully logged in!\n'
LOGIN_FAIL = '\nWrong card number or PIN!\n'
LOGOUT_SUCCES = '\nYou have successfully logged out!\n'
CREATE_CARD_MSG = '\nYour card has been created'
CARD_NO_MSG = 'Your card number:'
CARD_PIN_MSG = 'Your card PIN:'
CARD_BALANCE_MSG = '\nBalance: '

guest_options = ['1. Create an account', '2. Log into account', '0. Exit']
logged_in_options = ['1. Balance', '2. Log out', '0. Exit']
logged_in = -1
selected_option = None
cards = []

class Card():
    """Create a card with a unique Customer Account Number and a PIN.

    Keyword arguments:
    mii -- Major Industry Identifier: the sort of institution that issued the card (default 4 - banking & financial institutions)
    iin -- Issuer Identification Number: who issued the card (default 00000)
    card_number_len -- Customer Account Number card length; it counts the `mii` & `iin` as well (default 16)
    checksum -- Used to validate the credit card number using the Luhn algorithm (default "any")

    """
    def __init__(self, mii=4, iin="00000", card_number_len=16, checksum_type="any"):
        self.mii = str(mii)
        self.iin = str(iin)
        self.checksum_type = checksum_type
        self.card_number_len = card_number_len
        self.set_ain()
        self.luhn_algo()
        self.set_number()
        self.set_pin()
        self.set_balance(0)

    def luhn_algo(self):
        # multiply even-indexed digits by 2
        multiplied_digits = [digit if index % 2 != 0 else int(digit) * 2 for index, digit in enumerate([*(self.mii + self.iin + self.ain)])]
        # substract 9 from digits greater than 9
        substracted_digits = [digit if int(digit) <= 9 else (int(digit) - 9) for digit in multiplied_digits]
        # add all digits
        summed_digits = sum(int(digit) for digit in [*substracted_digits])
        if summed_digits % 10 == 0:
            self.checksum = str(0)
        else:
            self.checksum = str(10 - (summed_digits % 10))

    def set_checksum(self):
        """Set card checksum (last digit of card)."""
        if self.checksum_type == "luhn":
            self.luhn_algo()
        else:    
            self.checksum = str(random.randint(0, 9))

    def set_ain(self):
        """Set account identifier number (7th to 15th card number digit)."""
        ain_len = self.card_number_len - len(self.mii) - len(self.iin) - 1 # len(self.checksum)
        self.ain = (str(random.randint(0, pow(10, ain_len) - 1))).zfill(ain_len)

    def set_number(self):
        """Set card number."""
        self.set_checksum()
        self.number = self.mii + self.iin + self.ain + self.checksum

    def set_pin(self):
        """Set card PIN."""
        pin_number = random.randint(0, 9999)
        self.pin = (str(pin_number)).zfill(4)

    def set_balance(self, sum):
        """Set card balance to a given sum.
    
        Arguments:
        sum -- the card balance to be set
        """
        self.balance = str(sum)

    def created(self):
        """Print created messages and card details."""
        print(CREATE_CARD_MSG)
        print(CARD_NO_MSG)
        print(self.number)
        print(CARD_PIN_MSG)
        print(self.pin + '\n')

    def get_balance(self):
        """Print card balance."""
        print(CARD_BALANCE_MSG + self.balance + '\n')

    def __repr__(self):
        return "Card (number: {}, pin: {}, balance: {})".format(
            self.number, 
            self.pin,
            self.balance
        )

    def __str__(self):
        return """
        Current card details: card number is `{}`, pin number is `{}, card balance is `{}`.
        """.format(
            self.number, 
            self.pin,
            self.balance
            )
        
def login(cards):
    """Try and login with provided card data by searching card number and pin in cards array.
    
    Args:
        cards -- the array where all the cards are stored

    Returns:
        card index position in the cards array if successful, -1 if otherwise. 
    """
    card_number = str(input(LOGIN_CARD_MSG))
    card_pin = str(input(LOGIN_PIN_MSG))

    for index, card in enumerate(cards):
        if card_number == card.number:
            if card_pin == card.pin:
                return index
    return -1

def guest_menu(selected_option, index):
    """Try and access selected option in the guest menu (see guest_options list).

    Args:
        selected_option -- valid integer matching an option from guest_options list
        index -- card index position in the cards array or -1 if guest

    Returns:
        index
    """
    if selected_option == 0:
        exit_sbs()
    else:
        if selected_option == 1:
            current_card = Card(checksum_type="luhn")
            cards.append(current_card)
            current_card.created()
        elif selected_option == 2:
            index = login(cards)
            if index != -1:
                print(LOGIN_SUCCES)
            else:
                print(LOGIN_FAIL)
        else:
            print(MENU_UNSUPPORTED_OPTION_MSG)
    return index

def logged_in_menu(selected_option, index):
    """Try and access selected option in the logged in menu (see logegd_in_options list).

    Args:
        selected_option -- valid integer matching an option from logged_in_options list
        index -- card index position in the cards array or -1 if guest

    Returns:
        index
    """
    if selected_option == 0:
        exit_sbs()
    else:
        if selected_option == 1:
            cards[index].get_balance()
        elif selected_option == 2:
            print(LOGOUT_SUCCES)
            index = -1
        else:
            print(MENU_UNSUPPORTED_OPTION_MSG)
    return index

def exit_sbs(message=MENU_EXIT_MSG):
    """Exit with message.
    
    Keyword arguments:
        message -- string to exit with as message (default MENU_EXIT_MSG)
    """
    sys.exit(message)

while selected_option not in range(0, 3):
    while selected_option != 0:        
        if logged_in == -1:
            try:
                selected_option = int(input('\n'.join(guest_options) + '\n'))
                logged_in = guest_menu(selected_option, logged_in)
            except ValueError:
                print(MENU_UNSUPPORTED_OPTION_MSG)
        else:
            try:
                selected_option = int(input('\n'.join(logged_in_options) + '\n'))
                logged_in = logged_in_menu(selected_option, logged_in)
            except ValueError:
                print(MENU_UNSUPPORTED_OPTION_MSG)
