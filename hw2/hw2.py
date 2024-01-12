"""
CMSC 14200, Winter 2024
Homework #2

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from typing import Optional
from trees import StrExp, BSTNode, BSTEmpty, BaseBST


#### Task 1 ####

class StrNode(StrExp):
    """
    Class to represent a String node in an expression tree
    """


class Concat(StrExp):
    """
    Class to represent the "concatenation" operator
    """


class Slice(StrExp):
    """
    Class to represent the "slice" operator
    """


class Replace(StrExp):
    """
    Class to represent the "replace" operator
    """


#### Task 2 ####

def valid_bst(tree: BaseBST) -> bool:
    """
    Determine whether or not a tree respects the BST ordering property

    Input:
        t (BST): the tree

    Returns (bool): True if t is a properly-ordered BST, False otherwise
    """
    raise NotImplementedError


#### Task 3 ####

class BSTEmptyOpt:
    """
    Empty (Optimized) BST Tree
    """

    # No constructor needed (nothing to initialize)

    @property
    def is_empty(self) -> bool:
        """
        Returns: True if the tree is empty, False otherwise
        """
        return True

    @property
    def is_leaf(self) -> bool:
        """
        Returns: True if the tree is a leaf node, False otherwise
        """
        return False

    @property
    def num_nodes(self) -> int:
        """
        Returns: The number of nodes in the tree
        """
        return 0

    @property
    def height(self) -> int:
        """
        Returns: The height of the tree
        """
        return 0

    @property
    def span(self) -> Optional[tuple[int, int]]:
        """
        Returns: A tuple with the min and max value in the tree;
                 None for an empty tree
        """
        return None

    def contains(self, n: int) -> bool:  # pylint: disable=unused-argument
        """
        Determines whether a value is contained in the tree.

        Args:
            n: The value to check

        Returns: True if the value is contained in the tree,
            False otherwise.
        """
        return False

    def insert(self, n: int) -> "BSTNodeOpt":
        """
        Inserts a value into the tree

        Args:
            n: Value to insert

        Returns: A new tree with the value inserted into it
        """
        return BSTNodeOpt(n, BSTEmptyOpt(), BSTEmptyOpt())


class BSTNodeOpt:
    """
    (Optimized) BST Tree Node
    """

    value: int
    left: "BSTEmptyOpt | BSTNodeOpt"
    right: "BSTEmptyOpt | BSTNodeOpt"

    def __init__(self, n: int,
                 left: "BSTEmptyOpt | BSTNodeOpt",
                 right: "BSTEmptyOpt | BSTNodeOpt"):
        """
        Constructor

        Args:
            n: Value associated with the tree node
            left: Left child tree
            right: Right child tree
        """
        self.value = n
        self.left = left
        self.right = right

    @property
    def is_empty(self) -> bool:
        """
        Returns: True if the tree is empty, False otherwise
        """
        return False

    @property
    def is_leaf(self) -> bool:
        """
        Returns: True if the tree is a leaf node, False otherwise
        """
        return self.left.is_empty and self.right.is_empty

    @property
    def num_nodes(self) -> int:
        """
        Returns: The number of nodes in the tree
        """
        return 1 + self.left.num_nodes + self.right.num_nodes

    @property
    def height(self) -> int:
        """
        Returns: The height of the tree
        """
        return 1 + max(self.left.height, self.right.height)

    @property
    def span(self) -> Optional[tuple[int, int]]:
        """
        Returns: A tuple with the min and max value in the tree;
                 None for an empty tree
        """
        left_span = self.left.span
        right_span = self.right.span
        min = self.value
        max = self.value
        if left_span is not None:
            min = left_span[0]
        if right_span is not None:
            max = right_span[1]
        return (min, max)

    @property
    def balance_factor(self) -> int:
        """
        Returns: Balance factor of the tree
        """
        return self.right.height - self.left.height

    def contains(self, n: int) -> bool:
        """
        Determines whether a value is contained in the tree.

        Args:
            n: The value to check

        Returns: True if the value is contained in the tree,
            False otherwise.
        """
        if n < self.value:
            return self.left.contains(n)
        elif n > self.value:
            return self.right.contains(n)
        else:
            return True

    def insert(self, n: int) -> "BSTNodeOpt":
        """
        Inserts a value into the tree

        Args:
            n: Value to insert

        Returns: A new tree with the value inserted into it
        """
        if n < self.value:
            return BSTNodeOpt(self.value, self.left.insert(n), self.right)
        elif n > self.value:
            return BSTNodeOpt(self.value, self.left, self.right.insert(n))
        else:
            return self


#### Task 4 ####

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
    rows: int
    cols: int
    board: list[list[Optional[str]]]

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.board = [[None] * cols for _ in range(rows)]

    def add_piece(self, piece: str, location: tuple[int, int]) -> bool:
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
            return True
        return False

    # Add your dominating property here
