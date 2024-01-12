from abc import ABC, abstractmethod
from typing import Optional


class StrExp(ABC):
    
    @abstractmethod
    def is_const(self) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def num_nodes(self) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def eval(self) -> str:
        raise NotImplementedError
        
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError
        

class BaseBST(ABC):

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def is_leaf(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def num_nodes(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def height(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def span(self) -> Optional[tuple[int, int]]:
        raise NotImplementedError

    @abstractmethod
    def contains(self, n: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def insert(self, n: int) -> "BSTNode":
        raise NotImplementedError


class BSTEmpty(BaseBST):

    # No constructor needed

    @property
    def is_empty(self) -> bool:
        return True

    @property
    def is_leaf(self) -> bool:
        return False

    @property
    def num_nodes(self) -> int:
        return 0

    @property
    def height(self) -> int:
        return 0
        
    @property
    def span(self) -> Optional[tuple[int, int]]:
        return None

    def contains(self, n: int) -> bool:
        return False

    def insert(self, n: int) -> "BSTNode":
        return BSTNode(n, BSTEmpty(), BSTEmpty())


class BSTNode(BaseBST):
    value: int
    left: "BSTEmpty | BSTNode"
    right: "BSTEmpty | BSTNode"

    def __init__(self, n: int, left: "BSTEmpty | BSTNode",
                 right: "BSTEmpty | BSTNode"):
        self.value = n
        self.left = left
        self.right = right

    @property
    def is_empty(self) -> bool:
        return False

    @property
    def is_leaf(self) -> bool:
        return self.left.is_empty and self.right.is_empty

    @property
    def num_nodes(self) -> int:
        return 1 + self.left.num_nodes + self.right.num_nodes

    @property
    def height(self) -> int:
        return 1 + max(self.left.height, self.right.height)
        
    @property
    def span(self) -> Optional[tuple[int, int]]:
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
        return self.right.height - self.left.height

    def contains(self, n: int) -> bool:
        if n < self.value:
            return self.left.contains(n)
        elif n > self.value:
            return self.right.contains(n)
        else:
            return True

    def insert(self, n: int) -> "BSTNode":
        if n < self.value:
            return BSTNode(self.value, self.left.insert(n), self.right)
        elif n > self.value:
            return BSTNode(self.value, self.left, self.right.insert(n))
        else:
            return self
