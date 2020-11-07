import sys
import random
import constants


class Card:
    """Create a card with a unique Customer Account Number and a PIN.

    Keyword arguments:
    mii -- Major Industry Identifier: the sort of institution that issued the card (default 4 - banking & financial institutions)
    iin -- Issuer Identification Number: who issued the card (default 00000)
    card_number_len -- Customer Account Number card length; it counts the `mii` & `iin` as well (default 16)
    checksum -- Used to validate the credit card number using the Luhn algorithm (default "any")
    data -- Used when passing an existing card

    """
    def __init__(self, mii=4, iin="00000", card_number_len=16, checksum_type="any", data=()):
        if not data:
            self.mii = str(mii)
            self.iin = str(iin)
            self.checksum = ""
            self.checksum_type = checksum_type
            self.card_number_len = card_number_len
            self.ain = ""
            self.set_ain()
            self.set_checksum()
            self.number = ""
            self.set_number()
            self.pin = ""
            self.set_pin()
            self.balance = ""
            self.set_balance()
        else:
            self.set_id(data[0])
            self.set_number(data[1])
            self.set_pin(data[2])
            self.set_balance(data[3])

    def luhn_algo(self, to_check=None):
        """Set the card digits based on the Luhn algorithm or check a given number.
        
        Keyword arguments:
            to_check -- used when checking a given card number against the algorithm
        """
        if to_check:
            original = to_check
        else:
            original = self.mii + self.iin + self.ain
        # multiply even-indexed digits by 2
        multiplied_digits = [digit if index % 2 != 0 else int(digit) * 2 for index, digit in enumerate([*(original)])]
        # substract 9 from digits greater than 9
        substracted_digits = [digit if int(digit) <= 9 else (int(digit) - 9) for digit in multiplied_digits]
        # add all digits
        summed_digits = sum(int(digit) for digit in [*substracted_digits])
        if summed_digits % 10 == 0:
            checksum = str(0)
        else:
            checksum = str(10 - (summed_digits % 10))
        return checksum

    def set_checksum(self):
        """Set card checksum (last digit of card)."""
        if self.checksum_type == "luhn":
            self.checksum = str(self.luhn_algo())
        else:
            self.checksum = str(random.randint(0, 9))

    def set_ain(self):
        """Set account identifier number (7th to 15th card number digit)."""
        ain_len = self.card_number_len - len(self.mii) - len(self.iin) - 1 # len(self.checksum)
        self.ain = (str(random.randint(0, pow(10, ain_len) - 1))).zfill(ain_len)

    def set_id(self, card_id):
        """Set the card id (used only for a pre-existing card)."""
        self.id = card_id

    def set_number(self, number=None):
        """Set the card number.

        Keyword arguments:
            number -- the card number (used for a pre-existing card)
        """
        if not number:
            self.set_checksum()
            number = self.mii + self.iin + self.ain + self.checksum

        self.number = number

    def set_pin(self, pin=None):
        """Set the card PIN.

        Keyword arguments:
            pin -- the card pin (used for a pre-existing card)
        """
        if not pin:
            pin_number = random.randint(0, 9999)
            pin = (str(pin_number)).zfill(4)
        self.pin = pin

    def set_balance(self, amount=None):
        """Set the card balance to a given amount.
    
        Arguments:
            amount -- the card balance to be set
        """
        if not amount:
            amount = 0
        self.balance = str(amount)

    def created(self):
        """Print created messages and card details."""
        print(constants.CREATE_CARD_MSG)
        print(constants.CARD_NO_MSG)
        print(self.number)
        print(constants.CARD_PIN_MSG)
        print(self.pin + '\n')

    def get_balance(self):
        """Print card balance."""
        print(constants.CARD_BALANCE_MSG + self.balance + '\n')

    def get_data(self):
        """Return a list with the card data."""
        data = [self.number, self.pin, self.balance]
        if hasattr(self, 'id'):
            data.append(self.id)
        return data
        
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
        