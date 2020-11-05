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

    """
    def __init__(self, mii=4, iin="00000", card_number_len=16, checksum_type="any"):
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
        self.set_balance(0)

    def luhn_algo(self):
        # multiply even-indexed digits by 2
        multiplied_digits = [digit if index % 2 != 0 else int(digit) * 2 for index, digit in enumerate([*(self.mii + self.iin + self.ain)])]
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
        print(constants.CREATE_CARD_MSG)
        print(constants.CARD_NO_MSG)
        print(self.number)
        print(constants.CARD_PIN_MSG)
        print(self.pin + '\n')

    def get_balance(self):
        """Print card balance."""
        print(constants.CARD_BALANCE_MSG + self.balance + '\n')

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
        