# Description
# You have created the foundation of our banking system. Now let's take the opportunity to deposit money into an account, 
# make transfers and close an account if necessary.
# 
# Now your menu should look like this:
# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit
#
# If the user asks for Balance, you should read the balance of the account from the database and output it into the console.
# 
# Add income item should allow us to deposit money to the account.
# 
# Do transfer item should allow transferring money to another account. You should handle the following errors:
# 
# If the user tries to transfer more money than he/she has, output: "Not enough money!"
# If the user tries to transfer money to the same account, output the following message:
#  “You can't transfer money to the same account!”
# If the receiver's card number doesn’t pass the Luhn algorithm, you should output: 
#  “Probably you made a mistake in the card number. Please try again!”
# If the receiver's card number doesn’t exist, you should output: “Such a card does not exist.”
# If there is no error, ask the user how much money they want to transfer and make the transaction.
# If the user chooses the Close account item, you should delete that account from the database.
# 
# Do not forget to commit your DB changes right after executing a query!
#
# Examples
# The symbol > represents the user input. Notice that it's not a part of the input. 
# Example 1:
# 
# 1. Create an account
# 2. Log into account
# 0. Exit
# >1
# 
# Your card have been created
# Your card number:
# 4000009455296122
# Your card PIN:
# 1961
# 
# 1. Create an account
# 2. Log into account
# 0. Exit
# >1
# 
# Your card have been created
# Your card number:
# 4000003305160034
# Your card PIN:
# 5639
# 
# 1. Create an account
# 2. Log into account
# 0. Exit
# >2
# 
# Enter your card number:
# >4000009455296122
# Enter your PIN:
# >1961
# 
# You have successfully logged in!
# 
# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit
# >2
# 
# Enter income:
# >10000
# Income was added!
# 
# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit
# >1
# 
# Balance: 10000
# 
# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit
# >3
# 
# Transfer
# Enter card number:
# >4000003305160035
# Probably you made a mistake in the card number. Please try again!
# 
# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit
# >3
# 
# Transfer
# Enter card number:
# >4000003305061034
# Such a card does not exist.
# 
# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit
# >3
# 
# Transfer
# Enter card number:
# >4000003305160034
# Enter how much money you want to transfer:
# >15000
# Not enough money!
# 
# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit
# >3
# 
# Transfer
# Enter card number:
# >4000003305160034
# Enter how much money you want to transfer:
# >5000
# Success!
# 
# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit
# >1
# 
# Balance: 5000
# 
# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit
# 
# >0
# Bye!
#
# Example 2:
# 
# 1. Create an account
# 2. Log into account
# 0. Exit
# >1
# 
# Your card has been created
# Your card number:
# 4000007916053702
# Your card PIN:
# 6263
# 
# 1. Create an account
# 2. Log into account
# 0. Exit
# >2
# 
# Enter your card number:
# >4000007916053702
# Enter your PIN:
# >6263
# 
# You have successfully logged in!
# 
# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit
# >4
# 
# The account has been closed!
# 
# 1. Create an account
# 2. Log into account
# 0. Exit
# >2
# 
# Enter your card number:
# >4000007916053702
# Enter your PIN:
# >6263
# 
# Wrong card number or PIN!
# 
# 1. Create an account
# 2. Log into account
# 0. Exit
# >0
# 
# Bye!

import sys
import random
import constants
from classes.card import Card
from classes.database import Database


guest_options = ['1. Create an account', '2. Log into account', '0. Exit']
logged_in_options = ['1. Balance', '2. Add income', '3. Do transfer', '4. Close account', '5. Log out', '0. Exit']
logged_in = -1
selected_option = None
db=Database()
db.connect()


def login():
    """Try and login with provided card data by searching card number and pin in the database.

    Returns:
        The card id if successful, -1 if otherwise.
    """
    card_number = str(input(constants.LOGIN_CARD_INPUT))
    card_pin = str(input(constants.LOGIN_PIN_INPUT))
    # if found, the response contains the card data (id, number, pin, balance)
    response = db.get_card_data_by_number(card_number)

    if not response:
        return -1
    if response[2] != card_pin:
        return -1
    return response[0]


def show_balance(balance):
    """Print the given balance."""
    print(constants.CARD_BALANCE_MSG + str(balance) + '\n')


def guest_menu(selected, card_id):
    """Try and access selected option in the guest menu (see guest_options list).

    Arguments:
        selected -- a valid integer matching an option from guest_options list
        card_id -- the card id or -1 if guest

    Returns:
        The card id or -1 if guest
    """
    if selected_option == 0:
        exit_sbs()
    else:
        if selected_option == 1:
            current_card = Card(checksum_type="luhn")
            db.create_card_record(current_card.get_data())
            current_card.created()
        elif selected_option == 2:
            card_id = login()
            if card_id != -1:
                print(constants.LOGIN_SUCCESS_MSG)
            else:
                print(constants.LOGIN_FAIL_MSG)
        else:
            print(constants.MENU_UNSUPPORTED_OPTION_MSG)
    return card_id


def logged_in_menu(selected, card_id):
    """Try and access selected option in the logged in menu (see logged_in_options list).

    Arguments:
        selected -- valid integer matching an option from logged_in_options list
        card_id -- card id or -1 if guest

    Returns:
        The card id or -1 if guest
    """
    if selected_option == 0:
        exit_sbs()
    else:
        # if found, the response contains the card data (id, number, pin, balance)
        response = db.get_card_data_by_id(card_id)
        current_card = Card(data=response)
        # show balance option
        if selected_option == 1:
            current_card.get_balance()
        # add income option
        elif selected == 2:
            add_income(current_card)
        # do transfer option
        elif selected == 3:
            do_transfer(current_card)
        # close card option
        elif selected == 4:
            print(constants.CARD_CLOSE_MSG)
            db.delete_card_record(current_card.id)
            card_id = -1
        # logout option
        elif selected == 5:
            print(constants.LOGOUT_SUCCESS_MSG)
            card_id = -1
        else:
            print(constants.MENU_UNSUPPORTED_OPTION_MSG)
    return card_id


def updated(old, new):
    return (old == new) is False


def update_balance(card, amount, success_msg="", fail_msg="", quiet=False):
    result = False
    old_balance = card.balance
    card.set_balance(int(old_balance) + int(amount))
    db.update_card_record(card.get_data())
    if updated(old_balance, card.balance):
        if not quiet:
            print(success_msg)
        result = True
    else:
        if not quiet:
            print(fail_msg)
    return result


def add_income(card):
    income = str(input(constants.CARD_ADD_INCOME_MSG))
    while not income.isdigit():
        print(constants.POSITIVE_INTEGER_FAIL)
        income = str(input(constants.CARD_ADD_INCOME_MSG))
    update_balance(card, income, constants.CARD_ADD_INCOME_SUCCESS, constants.CARD_ADD_INCOME_FAIL)


def valid_number(number, number_length=16, algo="luhn"):
    result = False
    if not number.isdigit():
        return result
    if len(number) != number_length:
        return result
    data = (-1, number, 0000, -1)
    fake_card = Card(data=data)
    if algo == "luhn":
        check_digit = fake_card.number[-1:]
        to_check = fake_card.number[:len(fake_card.number)-1]
        result = (check_digit == fake_card.luhn_algo(to_check))
    return result


def check_amount(card, amount):
    if not amount.isdigit():
        print(constants.POSITIVE_INTEGER_FAIL)
        return False
    if int(card.balance) < int(amount):
        print(constants.CARD_TRANSFER_AMOUNT_FAIL)
        return False
    return True


def check_number(card, number, algo="luhn"):
    if not valid_number(number, algo=algo):
        print(constants.CARD_TRANSFER_NUMBER_FAIL)
        return False
    if card.number == number:
        print(constants.CARD_TRANSFER_NUMBER_OWN)
        return False
    if not db.get_card_data_by_number(number):
        print(constants.CARD_TRANSFER_NUMBER_NONEXISTENT)
        return False
    return True


def do_transfer(card):
    print(constants.CARD_TRANSFER_MSG)
    receiver = str(input(constants.CARD_TRANSFER_NUMBER_MSG))
    if not check_number(card, receiver):
        return False
    amount = str(input(constants.CARD_TRANSFER_AMOUNT_MSG))
    if not check_amount(card, amount):
        return False
    is_successful = update_balance(card, int(amount) * -1, quiet=True)
    if is_successful:
        receiver_card = Card(data=db.get_card_data_by_number(receiver))
        is_successful = update_balance(receiver_card, int(amount), quiet=True)
    if is_successful:
        print(constants.CARD_TRANSFER_AMOUNT_SUCCESS)
    else:
        print(constants.CARD_TRANSFER_AMOUNT_FAIL)

def exit_sbs(message=constants.MENU_EXIT_MSG):
    """Exit with message and close database connection.
    
    Keyword arguments:
        message -- string to exit with as message (default MENU_EXIT_MSG)
    """
    db.disconnect()
    sys.exit(message)


while selected_option not in range(0, 3):
    while selected_option != 0:        
        if logged_in == -1:
            try:
                selected_option = int(input('\n'.join(guest_options) + '\n'))
                logged_in = guest_menu(selected_option, logged_in)
            except ValueError:
                print(constants.MENU_UNSUPPORTED_OPTION_MSG)
        else:
            try:
                selected_option = int(input('\n'.join(logged_in_options) + '\n'))
                logged_in = logged_in_menu(selected_option, logged_in)
            except ValueError:
                print(constants.MENU_UNSUPPORTED_OPTION_MSG)
