"""
CMSC 14200, Spring 2024
Homework #3
"""
from abc import ABC, abstractmethod
from typing import Any, Optional

class Graph(ABC):
    """ Abstract class for graphs """

    @property
    @abstractmethod
    def num_vertices(self) -> int:
        """
        Inputs: (nothing)

        Returns: the number of vertices in the graph.
        """
        raise NotImplementedError


    @property
    @abstractmethod
    def num_edges(self) -> int:
        """
        Inputs: (nothing)

        Returns: the number of edges in the graph.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def vertex_labels(self) -> set[str]:
        """
        Inputs: (nothing)

        Returns: the set of all vertex labels in the graph.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def edges(self) -> set[tuple[str, str]]:
        """
        Inputs: (nothing)

        Returns: the set of all edges in the graph. Each edge is a
        tuple of labels in (source, destination) order.
        """
        raise NotImplementedError

    @abstractmethod
    def connect(self, src: str, dst: str) -> None:
        """
        Adds an edge to the graph.

        Inputs:
           src, the label of the origin of the new edge
           dst, the label of the destination of the new edge

        Returns: (nothing)

        Raises:
            ValueError if src or dst not in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def connected(self, src: str, dst: str) -> bool:
        """
        Inputs:
           src, the label of the origin of the new edge
           dst, the label of the destination of the new edge

        Returns: True is there is such an edge, False otherwise

        Raises:
            ValueError if src or dst not in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def out_neighbors(self, src: str) -> set[str]:
        """
        Returns the set of the labels of all vertices
        directly connected to src by an edge originating
        at src.

        Inputs:
          src, a vertex label

        Returns: a set of strings

        Raises:
            ValueError if src not in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def get_value(self, vertex: str) -> Any:
        """
        Return the value associated with a vertex.

        Inputs:
          vertex, a label

        Returns: the value at the chosen vertex.

        Raises:
            ValueError if vertex not in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def set_value(self, vertex: str, value: Any) -> None:
        """
        Set the value at the chosen vertex to what is given,
        overwriting whatever value was already present.

        Inputs:
          vertex, a label
          value, a value of any kind of data

        Returns: (nothing)

        Raises:
            ValueError if vertex not in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def to_adj_list(self) -> 'AdjacencyListDigraph':
        """
        Return the same graph in adjacency list form.

        Inputs: (nothing)

        Returns: an AdjacencyListDigraph.
        """
        raise NotImplementedError

    @abstractmethod
    def to_adj_matrix(self) -> 'AdjacencyMatrixDigraph':
        """
        Return the same graph in adjacency matrix form.

        Inputs: (nothing)

        Returns: an AdjacencyMatrixDigraph.
        """
        raise NotImplementedError

class AdjacencyListDigraph(Graph):
    """ Adjacency list implementation of graphs """

    _neighbors:     dict[str,list[str]]
    _vertex_values: dict[str,Any]

    def __init__(self, vertex_labels:list[str]):
        raise NotImplementedError

class AdjacencyMatrixDigraph(Graph):
    """ Adjacency matrix implementation of graphs """

    _labels_to_ints: dict[str, int]
    _ints_to_labels: list[str]
    _adjacency:      list[list[bool]]
    _vertex_values:  dict[str, Any]

    def __init__(self, vertex_labels: list[str]):
        raise NotImplementedError
