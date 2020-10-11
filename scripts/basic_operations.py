# Description
# We live busy lives these days. Between work, chores, and other things in our to-do lists, 
# it can be tough to catch your breath and stay calm. Credit cards are one of the things 
# that save us time, energy, and nerves. From not having to carry a wallet full of cash to consumer protection, 
# cards make our lives easier in many ways. 
# In this project, you will develop a simple banking system with a database.
# If you’re curious about business, technology, or how things around you work, 
# you'll probably enjoy learning how credit card numbers work. 
# These numbers ensure easy payments, and they also help prevent payment errors and fraud. 
# Card numbers are evolving, and they might look different in the near future.
# The anatomy of a card:
#
# - the very first number is the Major Industry Identifier (MII), which tells you what sort of institution issued the card.
#   + 1 and 2 are issued by airlines
#   + 3 is issued by travel and entertainment
#   + 4 and 5 are issued by banking and financial institutions
#   + 6 is issued by merchandising and banking
#   + 7 is issued by petroleum companies
#   + 8 is issued by telecommunications companies
#   + 9 is issued by national assignment
#   Note: In our banking system, credit cards should begin with 4.
#
# - the first six digits are the Issuer Identification Number (IIN);
# these can be used to look up where the card originated from. 
# If you have access to a list that provides detail on who owns each IIN, 
# you can see who issued the card just by reading the card number.
# Here are a few you might recognize:
#   + Visa: 4*****
#   + American Express (AMEX): 34**** or 37****
#   + Mastercard: 51**** to 55****
#   Note: in our banking system, the IIN must be 400000.
#
# - the seventh digit to the second-to-last digit is the customer account number; 
# most companies use just 9 digits for the account numbers, but it’s possible to use up to 12. 
# This means that using the current algorithm for credit cards, 
# the world can issue about a trillion cards before it has to change the system.
# We often see 16-digit credit card numbers today, 
# but it’s possible to issue a card with up to 19 digits using the current system. 
# In the future, we may see longer numbers becoming more common.
#   Note: in our banking system, the customer account number can be any number, 
# but it should be unique and have a length of 16 digits.
#
# - the very last digit of a credit card is the check digit or checksum; 
# it is used to validate the credit card number using the Luhn algorithm, 
# which we will explain in the next stage of this project. 
#   Note: for now, the checksum can be any digit you like.
#
# Instruction
# You should allow customers to create a new account in our banking system.
# Once the program starts, you should print the menu:
#  1. Create an account
#  2. Log into account
#  0. Exit
# If the customer chooses ‘Create an account’, 
# you should generate a new card number which satisfies all the conditions described above. 
# Then you should generate a PIN code that belongs to the generated card number. 
# A PIN code is a sequence of any 4 digits. PIN should be generated in a range from 0000 to 9999.
# If the customer chooses ‘Log into account’, you should ask them to enter their card information. 
# Your program should store all generated data until it is terminated 
# so that a user is able to log into any of the created accounts by a card number and its pin. 
# You can use an array to store the information.
# After all information is entered correctly, you should allow the user to check the account balance; 
# right after creating the account, the balance should be 0. 
# It should also be possible to log out of the account and exit the program.
#
# Example
# The symbol > represents the user input. 
# Notice that it's not a part of the input.
# 1. Create an account
# 2. Log into account
# 0. Exit
# >1
# Your card has been created
# Your card number:
# 4000004938320895
# Your card PIN:
# 6826
#
# 1. Create an account
# 2. Log into account
# 0. Exit
# >2
#
# Enter your card number:
# >4000004938320895
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
# >4000004938320895
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
        self.set_checksum()
        self.set_ain()
        self.set_number()
        self.set_pin()
        self.set_balance(0)

    def set_checksum(self):
        """Set card checksum (last digit of card)."""
        if self.checksum_type != "any":
            print("Not supported yet!")
        self.checksum = str(random.randint(0, 9))

    def set_ain(self):
        """Set account identifier number (7th to 15th card number digit)."""
        ain_len = self.card_number_len - len(self.mii) - len(self.iin) - len(self.checksum)
        self.ain = (str(random.randint(0, pow(10, ain_len) - 1))).zfill(ain_len)

    def set_number(self):
        """Set card number."""
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
            current_card = Card()
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
