"""
CMSC 14200, Winter 2024
Homework #1

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from typing import Optional
from abc import ABC, abstractmethod
from tree import TreeNode


def count_words(list_of_strings: list[str], starts_with: str) -> dict[str, int]:
    """
    Find the words that start with a given substring and count the number of
    times each word appears.

    Inputs:
        list_of_strings (list): the list of words
        starts_with (string): substring that has to appear in each word

    Returns (dict): the words and counts of each word that starts with the given
    """
    raise NotImplementedError("todo: count_words")


class Board:
    """
    Class to represent a game board.

    Attributes:
        rows (int): number of rows
        cols (int): number of columns
        board (list): the game board
        location_of_pieces (dictionary): the location of each piece on the board

    Methods:
        add_piece: add a piece represented by a string to the board
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[None] * cols for _ in range(rows)]
        self.location_of_pieces = {}

    def add_piece(self, piece, location):
        """
        Add a piece represented by a string to the board.

        Inputs:
            piece (string): the piece to add
            location (tuple): the (row, column) location of where to add
                the piece

        Returns (bool): True if the piece was added successfully,
            False otherwise
        """
        row, col = location

        if self.board[row][col] is None:
            self.board[row][col] = piece
            if piece in self.location_of_pieces:
                self.location_of_pieces[piece].append(location)
            else:
                self.location_of_pieces[piece] = [location]
            return True
        return False


def get_all_paths(t: TreeNode) -> list[list[int]]:
    """
    Find all the unique paths from the root to a leaf node in a tree.

    Inputs:
        t (TreeNode): the tree

    Returns (list): the list of paths
    """
    raise NotImplementedError("todo: get_all_paths")

class InsufficientFundsError(Exception):
    """
    Exception to be raised when an account has insufficient funds
    """
    pass

class Account(ABC):
    """
    Class to represent a bank account.

    Methods:
        deposit: deposit money into the account
        withdraw: withdraw money from the account

    Property:
        balance: the balance of the account
    """
    def __init__(self, account_number: int, balance: float = 0):
        self._account_number = account_number
        self._balance = float(balance)

    @abstractmethod
    def deposit(self, amount: float) -> None:
        """
        Makes a deposit in the account.

        Inputs:
            amount (float): Amount to deposit

        Returns: Nothing
        """
        raise NotImplementedError

    @abstractmethod
    def withdraw(self, amount: float) -> float:
        """
        Makes a withdrawal from the account.

        Inputs:
            amount (float): Amount to withdraw

        Returns (float): Withdrawn amount.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def balance(self) -> float:
        """
        Returns the balance of the account

        Returns (float): Account balance
        """
        raise NotImplementedError


class SavingsAccount(Account):
    """
    Class to represent a savings account
    """


class CheckingAccount(Account):
    """
    Class to represent a checking account
    """


class HighYieldSavingsAccount(SavingsAccount):
    """
    Class to represent a high yeild savings account
    """
