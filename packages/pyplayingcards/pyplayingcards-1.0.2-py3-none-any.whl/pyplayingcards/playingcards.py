"""A simple playing cards module to allow you to manipulate playing card objects in Python."""
from random import choice, randint, shuffle
from pyplayingcards.errors import SuitError, NotPlayingCard, NotPlayingCards, NoValuesGiven


suits = ("hearts", "clubs", "diamonds", "spades")
values = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace")


class PlayingCard:
    """This class defines PlayingCard objects.

    Notes:
        The PlayingCard module and pyplayingcard package do not support the "Joker" card,
        though feel free to implement this yourself, or on a fork on our GitHub page.
    """

    def __init__(self, suit: str, value: str):
        """Initialize a PlayingCard object.

        Args:
            suit (str): The Suit of the Playing Card.
            value (str): The Value of the playing Card, whether it is a face card or not.

        Raises:
            SuitError: If the PlayingCard is initialized with an invalid suit.
            ValueError: If the PlayingCard is initialized with an invalid value.
        """
        suit = suit.lower()
        if suit in suits:
            self.suit = suit
        else:
            if suit in ["heart", "club", "diamond", "spade"]:
                self.suit = suit + "s"
            else:
                raise SuitError(f"'{suit1}' is not a valid suit.")

        if not value.isdigit():
            value = value.lower()
        if value in values:
            self.value = str(value)
        else:
            raise ValueError(f"'{value}' is not a valid PlayingCard value.")

    def __repr__(self):
        """Show how to create the PlayingCard object.

        Returns:
            str: A string that shows how to create the same PlayingCard object.
        """
        return f"{self.__class__.__name__}(\"{self.suit}\", \"{self.value}\")"

    def __str__(self):
        """Format the PlayingCard object nicely.

        Returns:
            str: A nicely formatted string for end-users to see what card the PlayingCard object is.
        """
        return f"The {str(self.value).capitalize()} of {self.suit.capitalize()}"

    def __eq__(self, other):
        """Equality operator for PlayingCard objects.

        Args:
            other (PlayingCard): Other PlayingCard object to be compared.

        Returns:
            bool: True if the two PlayingCard objects have the same value and suit.

        Raises:
            NotPlayingCard: If an object that is not of type PlayingCard is compared with.
        """
        if isinstance(other, PlayingCard):
            return self.suit == other.suit and self.value == other.value
        raise NotPlayingCard(f"\"{other}\" is not a PlayingCard object.")

    def __lt__(self, other):
        """Lower than equality operator for PlayingCard objects.

        Args:
            other (PlayingCard): Other PlayingCard object to be compared.

        Returns:
            bool: True if the self PlayingCard object has a lower value than the other PlayingCard object.

        Raises:
            NotPlayingCard: If an object is not of type PlayingCard is compared with.
        """
        if isinstance(other, PlayingCard):
            return values.index(self.value) < values.index(other.value)
        raise NotPlayingCard(f"\"{other}\" is not a PlayingCard object.")

    def __gt__(self, other):
        """Greater than equality operator for PlayingCard objects.

        Args:
            other (PlayingCard): Other PlayingCard object to be compared.

        Returns:
            bool: True if the self PlayingCard object has a greater value than the other PlayingCard object.

        Raises:
            NotPlayingCard: If an object is not of type PlayingCard is compared with.
        """
        return not self.__lt__(other)

    def __ne__(self, other):
        """Not equal to equality operator for PlayingCard objects.

        Args:
            other (PlayingCard): Other PlayingCard object to be compared.

        Returns:
            bool: True if the self PlayingCard object is not equal to the other PlayingCard object.

        Raises:
            NotPlayingCard: If an object is not of type PlayingCard is compared with.
        """
        return not self.__eq__(other)

    def __ge__(self, other):
        """Greater than or equal to equality operator for PlayingCard objects.

        Args:
            other (PlayingCard): Other PlayingCard object to be compared.

        Returns:
            bool: True if the self PlayingCard object if greater than or equal to the other PlayingCard object.

        Raises:
            NotPlayingCard: If an object is not of type PlayingCard is compared with.
        """
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        """Lower than or equal to equality operator for PlayingCard objects.

        Args:
            other (PlayingCard): Other PlayingCard object to be compared.

        Returns:
            bool: True if the self PlayingCard object is greater than or equal to the other PlayingCard object.

        Raises:
            NotPlayingCard: If an object is not of type PlayingCard is compared with.
        """
        return self.__lt__(other) or self.__eq__(other)

    def __iter__(self):
        """Allow PlayingCard objects to be converted to dictionaries, lists and tuples.

        Yields:
            "suit": self.suit, the PlayingCard object's suit.
            "value": self.value, the PlayingCard object's value.
        """
        yield "suit", self.suit
        yield "value", self.value

    @property
    def facecard(self):
        """Read-only property for PlayingCard objects that shows whether they are a face card or not.

        Returns:
            bool: True if the value of the PlayingCard object is a face card, or not a number, otherwise False.
        """
        return self.value in ("jack", "queen", "king", "ace")

    @property
    def colour(self):
        """Read-only property for PlayingCard objects that shows their colour.

        Returns:
            str: "black" if the card is black, or "red" if the card is red.
        """
        if self.suit in ("clubs", "spades"):
            return "black"
        else:
            return "red"


class PlayingCards:
    """PlayingCards can be used for a certain amount of randomly generated cards or user-defined cards.

    Notes:
        NOT to be confused with the PlayingCard class: this class is for multiple cards.
    """

    def __init__(self, amount: int, cardvalues: list = None, suit: str = None, random: bool = True):
        """Initialize a PlayingCards object.

        Args:
            amount (int): The number of cards you want to randomly generate, or create a PlayingCards object with.
            cardvalues (list): The values of the PlayingCard objects in the PlayingCards object, if random is set to False.
                The list should be in the following format:
                    [PlayingCard, PlayingCard, PlayingCard]
                    and so on.
                We have chosen lists as they are the most versatile of the three: lists, tuples and sets.
            suit (str): You can optionally set a suit, and cards will be randomly generated in that suit.
            random (bool): Default True, defines whether the PlayingCard objects in the PlayingCards object are
                randomly generated or not.

        Raises:
            SuitError: If the PlayingCards object is initialized with an invalid suit.
            NotPlayingCard: If even one of the items in values is not a PlayingCard.
            NoValuesGiven: If no PlayingCard objects are given in values
                even though the random parameter is set to False.

        Notes:
            Duplicate cards are allowed.
        """
        self.amount = amount
        self.cards = []
        self.cardvalues = cardvalues
        self.random = random
        if random:
            if cardvalues is not None and cardvalues != []:
                raise ValueError("Values were given but random was set to True.")
            if suit is not None:
                suit = suit.lower()
                if suit in suits:
                    self.suit = suit
                else:
                    if suit in ["heart", "club", "diamond", "spade"]:
                        self.suit = suit + "s"
                    else:
                        raise SuitError(f"'{suit1}' is not a valid suit.")
                self.cards = self.random_cards(self.amount, self.suit)
            else:
                self.cards = self.random_cards(self.amount)
                self.suit = None
        else:
            if cardvalues is not None and cardvalues != []:
                for card in cardvalues:
                    if not isinstance(card, PlayingCard):
                        raise NotPlayingCard("One of the items in values is not a PlayingCard object.")
                self.cards = cardvalues
            else:
                raise NoValuesGiven("No values were given even though the random parameter was set to False.")

    @staticmethod
    def random_cards(num: int, weight: str = None):
        """Create a list of randomly generated PlayingCard objects.

        Args:
            num (int): The number of cards to randomly generate.
            weight (str): Default None, the suit of cards you want to weight the random generation to.

        Returns:
            list: Returns a list of the randomly generated cards.
        """
        cards = []
        if weight is not None:
            if weight not in suits:
                raise SuitError("Invalid suit.")
            dupsuits = list(suits)
            dupsuits.append(weight)
        else:
            dupsuits = list(suits)
        for _ in range(0, num):
            cards.append(PlayingCard(choice(dupsuits), choice(values)))

        return cards

    def deal(self, amount: int):
        """Deal a PlayingCards object.

        Args:
            amount (int): The amount of PlayingCard objects you want in the list.

        Returns:
            list: A list of PlayingCard objects from the PlayingCards

        Raises:
            AssertionError: If they try and deal more cards than are in the PlayingCards.
        """
        cards = []
        assert amount <= len(self.cards), f"The maximum number of cards you can deal from this PlayingCards is {len(self.cards)}."
        for _ in range(0, amount):
            cards.append(choice(self.cards))

        return cards

    def regenerate(self):
        """Re-generate the cards of the PlayingCards object.

        Returns:
            list: Returns a list of the randomly generated cards.

        Notes:
            Regenerate does not work with weights.
        """
        self.cards = self.random_cards(len(self.cards))

        return self.cards

    def __iter__(self):
        """Allow PlayingCards objects to be converted to list and tuples.

        Yields:
            PlayingCard: Yields PlayingCard objects.

        Notes:
            PlayingCards objects should not be converted to dictionaries.
        """
        for card in self.cards:
            yield card

    def __repr__(self):
        """Show how to create the PlayingCards object.

        Returns:
            str: A string that shows how to create the same PlayingCards object.
        """
        return f"{self.__class__.__name__}({self.amount}, {self.cardvalues}, {self.suit}, {self.random})"

    def __str__(self):
        """Format the PlayingCards object nicely.

        Returns:
            str: A nicely formatted string for end-users to see what cards the PlayingCards object has.
        """
        cards = []
        for card in self.cards:
            cards.append(str(card))

        return "\n".join(cards)

    def __eq__(self, other):
        """Equality operator for PlayingCards objects.

        Args:
            other (PlayingCards): Other PlayingCards object to be compared.

        Returns:
            bool: True if the two PlayingCards objects have the same list of PlayingCard objects.

        Raises:
            NotPlayingCards: If an object that is not of type PlayingCards is compared with.
        """
        if isinstance(other, PlayingCards):
            return self.cards == other.cards
        raise NotPlayingCards(f"\"{other}\" is not a PlayingCards object.")

    def __lt__(self, other):
        """Lower than equality operator for PlayingCards objects.

        Args:
            other (PlayingCards): Other PlayingCards object to be compared.

        Returns:
            bool: True if the self PlayingCards object has a smaller cards list than the other PlayingCards object.

        Raises:
            NotPlayingCards: If an object is not of type PlayingCards is compared with.
        """
        if isinstance(other, PlayingCards):
            return len(self.cards) < len(other.cards)
        raise NotPlayingCards(f"\"{other}\" is not a PlayingCards object.")

    def __gt__(self, other):
        """Greater than equality operator for PlayingCards objects.

        Args:
            other (PlayingCards): Other PlayingCards object to be compared.

        Returns:
            bool: True if the self PlayingCards object has a longer cards list than the other PlayingCards object.

        Raises:
            NotPlayingCards: If an object is not of type PlayingCards is compared with.
        """
        return not self.__lt__(other)

    def __ne__(self, other):
        """Not equal to equality operator for PlayingCards objects.

        Args:
            other (PlayingCards): Other PlayingCards object to be compared.

        Returns:
            bool: True if the self PlayingCards object does not have the same cards list as the other PlayingCards object.

        Raises:
            NotPlayingCards: If an object is not of type PlayingCards is compared with.
        """
        return not self.__eq__(other)

    def __ge__(self, other):
        """Greater than or equal to equality operator for PlayingCards objects.

        Args:
            other (PlayingCards): Other PlayingCards object to be compared.

        Returns:
            bool: True if the self PlayingCards object if greater than or equal to the other PlayingCards object.

        Raises:
            NotPlayingCards: If an object is not of type PlayingCards is compared with.
        """
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        """Lower than or equal to equality operator for PlayingCards objects.

        Args:
            other (PlayingCards): Other PlayingCards object to be compared.

        Returns:
            bool: True if the self PlayingCards object is greater than or equal to the other PlayingCards object.

        Raises:
            NotPlayingCards: If an object is not of type PlayingCards is compared with.
        """
        return self.__lt__(other) or self.__eq__(other)

    def __add__(self, other):
        """Add two PlayingCards objects together.

        Args:
            other (PlayingCards): Other PlayingCards object to be compared.

        Returns:
            PlayingCards: Returns the PlayingCards object the two would create when added.

        Raises:
            NotPlayingCards: If an object is not of type PlayingCards is compared with.
        """
        return PlayingCards(self.amount+other.amount, cardvalues=self.cards+other.cards, random=False)


class Deck(PlayingCards):
    """Deck class inherits from PlayingCards, but with the default values of a deck of cards.

    Attributes:
        Deck.fullvalues (list): A list of all PlayingCard objects in a Deck.
    """

    fullvalues = []
    for suit in suits:
        for value in values:
            fullvalues.append(PlayingCard(suit, value))

    def __init__(self):
        """Initialize a Deck object."""
        PlayingCards.__init__(self, 52, cardvalues=__class__.fullvalues, random=False)

    def shuffle(self):
        """Shuffle the Deck object.

        Notes:
            This shuffles the Deck object in place.
        """
        shuffle(self.cards)

    def random_card(self):
        """Get a random card from the Deck object."""
        return choice(self.cards)


class Die:
    """A class for creating and manipulating Die objects."""

    def __init__(self, faces: int = 6):
        """Initialize the Die object.

        Args:
            faces (int): Default 6, the number of faces you want on the Die object.
        """
        self.faces = faces

    def roll(self):
        """Roll the Die.

        Returns:
            int: The random number generated.
        """
        return randint(0, self.faces)

