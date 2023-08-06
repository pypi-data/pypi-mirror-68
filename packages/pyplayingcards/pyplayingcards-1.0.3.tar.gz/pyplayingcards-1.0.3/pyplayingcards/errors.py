"""Module for card related exceptions."""


class SuitError(Exception):
    """Raised when a PlayingCard object is created with an invalid suit."""


class NotPlayingCard(Exception):
    """Raised when a PlayingCard object is compared to a different object."""


class NotPlayingCards(Exception):
    """Raised when a PlayingCards object is compared to a different object."""


class NoValuesGiven(Exception):
    """Raised when no values are given when initializing a PlayingCards object, even though the random parameter is set to False."""
