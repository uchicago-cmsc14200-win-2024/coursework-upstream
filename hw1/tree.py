"""
CMSC 14200, Winter 2024
tree.py

Contains the TreeNode class.
"""


class TreeNode:
    """ A node in a tree."""
    value: int
    children: list["TreeNode"]

    def __init__(self, value: int):
        self.value = value
        self.children = []

    def add_child(self, child: "TreeNode") -> None:
        self.children.append(child)

    def is_leaf(self) -> bool:
        return len(self.children) == 0