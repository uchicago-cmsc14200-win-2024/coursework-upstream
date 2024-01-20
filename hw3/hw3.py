"""
CMSC 14200, Spring 2024
Homework #3

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from typing import Optional, Literal
from graphs import Graph, AdjacencyListDigraph, AdjacencyMatrixDigraph

def like_component(g: Graph, src: str) -> set[str]:
    """
    Computes and returns the connected component originating
    at src such that the value associated with each vertex
    is the same.

    Inputs:
      g (graph)
      src (str) a vertex label

    Returns:
      a set of strings, the labels of vertices in the component
    """
    raise NotImplementedError

Stone = Literal['BLACK']|Literal['WHITE']

class GoBoard:
    """ Class for representing Go boards """

    _size:  int
    _board: list[list[Optional[Stone]]]

    def __init__(self, size: int):
        """
        Inputs:
          size (int), the number of positions in each column and row
        """
        if size<2:
            raise ValueError('too small for Go')
        self._size = size
        self._board = [[]] * size
        for i in range(size):
            self._board[i] = [None] * size

    @property
    def size(self) -> int:
        """
        The side length of the Go board.

        Inputs: (nothing)

        Returns:
          the side length
        """
        return self._size

    def put(self, col: int, row: int, s: Stone) -> None:
        """
        Place a stone on the board. Overwrite whatever is there.

        Inputs:
          col (int), the target column
          row (int), the target row
          s (Stone), either 'BLACK' or 'WHITE'

        Returns: (nothing)
        """
        self._board[col][row] = s

    def get(self, col: int, row: int) -> Optional[Stone]:
        """
        Retrieve a stone, or None, from the designated location.

        Inputs:
          col (int), the target column
          row (int), the target row

        Returns:
          an Optional Stone
        """
        return self._board[col][row]

def go_graph(gb: GoBoard) -> Graph:
    """
    Given a Go board, construct a graph such that each
    board location is a vertex in the graph, all of that
    location's orthogonal neighbors are connected by an
    edge, and an optional stone is stored as the value at
    each location's vertex.

    Inputs:
      gb: a GoBoard object

    Returns:
      a graph as described
    """
    raise NotImplementedError
