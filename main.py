import sys
import random
import constants
from classes.card import Card

guest_options = ['1. Create an account', '2. Log into account', '0. Exit']
logged_in_options = ['1. Balance', '2. Log out', '0. Exit']
logged_in = -1
selected_option = None
cards = []

def login(cards):
    """Try and login with provided card data by searching card number and pin in cards array.
    
    Args:
        cards -- the array where all the cards are stored

    Returns:
        card index position in the cards array if successful, -1 if otherwise. 
    """
    card_number = str(input(constants.LOGIN_CARD_INPUT))
    card_pin = str(input(constants.LOGIN_PIN_INPUT))

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
                print(constants.LOGIN_SUCCES_MSG)
            else:
                print(constants.LOGIN_FAIL_MSG)
        else:
            print(constants.MENU_UNSUPPORTED_OPTION_MSG)
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
            print(constants.LOGOUT_SUCCES_MSG)
            index = -1
        else:
            print(constants.MENU_UNSUPPORTED_OPTION_MSG)
    return index

def exit_sbs(message=constants.MENU_EXIT_MSG):
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
                print(constants.MENU_UNSUPPORTED_OPTION_MSG)
        else:
            try:
                selected_option = int(input('\n'.join(logged_in_options) + '\n'))
                logged_in = logged_in_menu(selected_option, logged_in)
            except ValueError:
                print(constants.MENU_UNSUPPORTED_OPTION_MSG)
