"""
CMSC 14200
Winter 2024

Test code for Homework #1
"""

import os
import sys
from typing import Optional
import hw1

import pytest

from tree import TreeNode


@pytest.mark.parametrize("list_of_strings, starts_with, expected",
                         [(["cmsc142"], "cmsc142", {"cmsc142": 1}),
    (["cmsc142", "cmsc142-1"], "cmsc142", {"cmsc142": 1, "cmsc142-1": 1}),
    (["bye", "hello", "goodbye", "goodnight", "Goodfellow"], "good", {'goodbye': 1, 'goodnight': 1}),
    (["Abcd","Abcd","abcd"],"Ab",{"Abcd": 2})
])
def test_task1_count_words(list_of_strings: list[str], starts_with: str, expected: str) -> None:
    """Do a single test for Task 1: count_words"""
    assert hw1.count_words(list_of_strings, starts_with) == expected


def create_tree(tree_string: str) -> Optional[TreeNode]:
    """
    Takes a string description of a tree and creates the appropriate
    tree using the correct class. Eg:

        0
       / \
      1   3
     /   / \
    2   4   6
       /
      5

    is represented by the string "0:1 1:2 0:3 3:4 4:5 3:6"
    The first node is presumed to be the root.    
    """
    root_node = None
    node_dict = {}
    for edge_str in tree_string.strip().split():
        u,v = tuple(int(x) for x in edge_str.split(":"))
        if u not in node_dict:
            node_dict[u] = TreeNode(u)
            if not root_node:
                root_node = node_dict[u]
        if v not in node_dict:
            node_dict[v] = TreeNode(v)

        node_dict[u].add_child(node_dict[v])

    return root_node


def compare_paths_unordered(paths1: list[list[int]], paths2: list[list[int]]) -> bool:
    """
    Compares two lists of paths, ignoring the order of the paths
    """
    if len(paths1) != len(paths2):
        return False

    for path in paths1:
        if path not in paths2:
            return False

    return True

    
@pytest.mark.parametrize("tree_string, expected",
    [['0:1 1:2 0:3 3:4 4:5 3:6', [[0, 1, 2], [0, 3, 4, 5], [0, 3, 6]]],
    ['0:1 1:2 2:3 3:4 4:5 5:6', [[0, 1, 2, 3, 4, 5, 6]]],
    ['0:1 0:2 1:3 1:4 2:5 2:6', [[0, 1, 3], [0, 1, 4], [0, 2, 5], [0, 2, 6]]]]
)
def test_task3_get_all_paths(tree_string: str, expected: list[list[int]])  -> None:
    root = create_tree(tree_string)
    assert root is not None
    assert compare_paths_unordered(hw1.get_all_paths(root), expected)


def test_task4_account_creation()  -> None:
    """Test creation of the Account Class (should not be allowed)"""
    # pylint: disable=abstract-class-instantiated
    with pytest.raises(TypeError):
        a = hw1.Account(12345)  # type: ignore


def test_task4_savings_account_1() -> None:
    a = hw1.SavingsAccount(1234)
    a.deposit(1000)
    assert a.balance == 1000


def test_task4_savings_account_2() -> None:
    a = hw1.SavingsAccount(1234,1000)
    a.withdraw(100)


def test_task4_savings_account_3() -> None:
    a = hw1.SavingsAccount(1234,1000)
    with pytest.raises(hw1.InsufficientFundsError):
        a.withdraw(2000)

def test_task4_savings_account_4() -> None:
    a = hw1.SavingsAccount(1234)
    a.deposit(1000)
    assert a.balance == 1000
    assert a.withdraw(150) == 150.0
    assert a.balance == 850
    assert a.withdraw(850) == 850.0
    with pytest.raises(hw1.InsufficientFundsError):
        a.withdraw(100)
    assert a.balance == 0

def test_task4_checking_account_1() -> None:
    a = hw1.CheckingAccount(1234,100,50)
    assert a.balance == 100
    assert a.available_overdraft == 50


def test_task4_checking_account_2() -> None:
    a = hw1.CheckingAccount(1234,100,50)
    assert a.withdraw(100) == 100.0
    assert a.balance == 0

def test_task4_checking_account_3() -> None:
    a = hw1.CheckingAccount(1234,100,50)
    assert a.withdraw(100) == 100.0
    assert a.balance == 0
    assert a.withdraw(25) == 25.0
    assert a.balance == 0 
    assert a.available_overdraft == 25
    assert a.withdraw(25) == 25.0
    assert a.balance == 0
    assert a.available_overdraft == 0

    with pytest.raises(hw1.InsufficientFundsError):
        a.withdraw(10)


def test_task4_checking_account_4() -> None:
    a = hw1.CheckingAccount(1234,100,50)
    assert a.withdraw(100) == 100.0
    assert a.balance == 0
    assert a.withdraw(25) == 25.0
    assert a.balance == 0 
    assert a.available_overdraft == 25
    assert a.withdraw(25) == 25.0
    assert a.balance == 0
    assert a.available_overdraft == 0

    with pytest.raises(hw1.InsufficientFundsError):
        a.withdraw(10)
    a.deposit(30)
    assert a.balance == 0
    assert a.available_overdraft == 30

    a.deposit(120)
    assert a.balance == 100
    assert a.available_overdraft == 50


def test_task5_hy_savings_account_1() -> None:
    a = hw1.HighYieldSavingsAccount(1234,1000,100,0.0425)
    assert isinstance(a, hw1.SavingsAccount)
    assert a.balance == 1000


def test_task5_hy_savings_account_2() -> None:
    a = hw1.HighYieldSavingsAccount(1234,1000,100,0.0425)
    assert a.balance == 1000
    with pytest.raises(hw1.InsufficientFundsError):
        a.withdraw(1000)
    assert a.withdraw(900) == 900.0
    assert a.balance == 100


def test_task5_hy_savings_account_3() -> None:
    a = hw1.HighYieldSavingsAccount(1234,1000,100,0.0425)
    a.add_monthly_interest()
    assert a.balance == 1042.5
    a.add_monthly_interest()
    assert a.balance == pytest.approx(1086.80625)
    with pytest.raises(hw1.InsufficientFundsError):
        a.withdraw(1000)