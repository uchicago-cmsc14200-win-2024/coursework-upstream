from hw2 import *
from trees import *

BST = BSTEmpty | BSTNode

def test_task1_1() -> None:
    s = StrNode("Rosenwald")
    assert s.is_const()
    assert s.num_nodes() == 1
    assert s.eval() == "Rosenwald"
    assert str(s) == '"Rosenwald"'

def test_task1_2() -> None:
    s1 = StrNode("Ryerson")
    s2 = StrNode(" Laboratory")
    op = Concat(s1, s2)
    assert not op.is_const()
    assert op.num_nodes() == 3
    assert op.eval() == "Ryerson Laboratory"
    assert str(op) == 'Concat("Ryerson", " Laboratory")'

def test_task1_3() -> None:
    s1 = StrNode("Ryerson")
    s2 = StrNode(" Physical")
    s3 = StrNode(" Laboratory")
    op = Concat(s1, Concat(s2, s3))
    assert not op.is_const()
    assert op.num_nodes() == 5
    assert op.eval() == "Ryerson Physical Laboratory"
    assert str(op) == 'Concat("Ryerson", Concat(" Physical", " Laboratory"))'

def test_task1_4() -> None:
    s = StrNode("Laboratory")
    op = Slice(s, 0, 3, 1)
    assert not op.is_const()
    assert op.num_nodes() == 2
    assert op.eval() == "Lab"
    assert str(op) == 'Slice("Laboratory", 0, 3, 1)'

def test_task1_5() -> None:
    s = StrNode("Laboratory")
    op = Slice(s, -7, 10, 1)
    assert not op.is_const()
    assert op.num_nodes() == 2
    assert op.eval() == "oratory"
    assert str(op) == 'Slice("Laboratory", -7, 10, 1)'

def test_task1_6() -> None:
    s = StrNode("Laboratory")
    op = Slice(s, -6, 1, -1)
    assert not op.is_const()
    assert op.num_nodes() == 2
    assert op.eval() == "rob"
    assert str(op) == 'Slice("Laboratory", -6, 1, -1)'

def test_task1_7() -> None:
    s = StrNode("Laboratory")
    op = Slice(s, 2, 20, 2)
    assert not op.is_const()
    assert op.num_nodes() == 2
    assert op.eval() == "brtr"
    assert str(op) == 'Slice("Laboratory", 2, 20, 2)'

def test_task1_8() -> None:
    s1 = StrNode("Pick Hall")
    s2 = StrNode("Pick")
    s3 = StrNode("Eckhart")
    op = Replace(s1, s2, s3)
    assert not op.is_const()
    assert op.num_nodes() == 4
    assert op.eval() == "Eckhart Hall"
    assert str(op) == 'Replace("Pick Hall", "Pick", "Eckhart")'

def test_task1_9() -> None:
    s1 = StrNode("Ryerson Physical Laboratory")
    s2 = StrNode("Hall")
    s3 = StrNode("")
    op = Replace(s1, s2, s3)
    assert not op.is_const()
    assert op.num_nodes() == 4
    assert op.eval() == "Ryerson Physical Laboratory"
    assert str(op) == 'Replace("Ryerson Physical Laboratory", "Hall", "")'

def test_task1_10() -> None:
    s1 = StrNode("CMSC")
    s2 = StrNode(" 14200")
    s3 = StrNode(" meets in ")
    s4 = StrNode("Rosenwald Hall 011")
    s5 = StrNode(" Hall")
    s6 = StrNode("")
    cs = Concat(Slice(s1, 0, 1, 1), Slice(s1, 2, 3, 1))
    oft = Slice(s2, 0, 4, 1)
    cs142 = Concat(cs, oft)
    ro011 = Replace(s4,s5, s6)
    res = Concat(cs142, Concat(s3, ro011))
    assert not res.is_const()
    assert res.num_nodes() == 15
    assert res.eval() == "CS 142 meets in Rosenwald 011"
    assert str(res) == 'Concat(Concat(Concat(Slice("CMSC", 0, 1, 1), ' + \
                       'Slice("CMSC", 2, 3, 1)), ' + \
                       'Slice(" 14200", 0, 4, 1)), Concat(" meets in ", ' + \
                       'Replace("Rosenwald Hall 011", " Hall", "")))'


def test_task2_1() -> None:
    bst = BSTEmpty()
    assert valid_bst(bst)

def test_task2_2() -> None:
    values = [1]
    bst: BST = BSTEmpty()
    for v in values:
        bst = bst.insert(v)
    assert valid_bst(bst)

def test_task2_3() -> None:
    values = [1, 2]
    bst: BST = BSTEmpty()
    for v in values:
        bst = bst.insert(v)
    assert valid_bst(bst)

def test_task2_4() -> None:
    values = [2, 1]
    bst: BST = BSTEmpty()
    for v in values:
        bst = bst.insert(v)
    assert valid_bst(bst)

def test_task2_5() -> None:
    values = [2, 1, 3]
    bst: BST = BSTEmpty()
    for v in values:
        bst = bst.insert(v)
    assert valid_bst(bst)

def test_task2_6() -> None:
    values = [1, 2, 3]
    bst: BST = BSTEmpty()
    for v in values:
        bst = bst.insert(v)
    assert valid_bst(bst)

def test_task2_7() -> None:
    values = [3, 2, 1]
    bst: BST = BSTEmpty()
    for v in values:
        bst = bst.insert(v)
    assert valid_bst(bst)

def test_task2_8() -> None:
    values = [4, 2, 6, 1, 3, 5, 7]
    bst: BST = BSTEmpty()
    for v in values:
        bst = bst.insert(v)
    assert valid_bst(bst)

def test_task2_9() -> None:
    empty = BSTEmpty()
    bst = BSTNode(0, BSTNode(1, empty, empty), empty)
    assert not valid_bst(bst)

def test_task2_10() -> None:
    empty = BSTEmpty()
    bst = BSTNode(0, empty, BSTNode(-1, empty, empty))
    assert not valid_bst(bst)

def test_task2_11() -> None:
    empty = BSTEmpty()
    bst = BSTNode(0,
            BSTNode(-2,
              BSTNode(10, empty, empty),
              BSTNode(-1, empty, empty)),
            BSTNode(2,
              BSTNode(1, empty, empty),
              BSTNode(3, empty, empty)))
    assert not valid_bst(bst)

def test_task2_12() -> None:
    empty = BSTEmpty()
    bst = BSTNode(0,
            BSTNode(-2,
              BSTNode(-3, empty, empty),
              BSTNode(-10, empty, empty)),
            BSTNode(2,
              BSTNode(1, empty, empty),
              BSTNode(3, empty, empty)))
    assert not valid_bst(bst)

def test_task2_13() -> None:
    empty = BSTEmpty()
    bst = BSTNode(0,
            BSTNode(-2,
              BSTNode(-3, empty, empty),
              BSTNode(-1, empty, empty)),
            BSTNode(2,
              BSTNode(10, empty, empty),
              BSTNode(3, empty, empty)))
    assert not valid_bst(bst)
    
def test_task2_14() -> None:
    empty = BSTEmpty()
    bst = BSTNode(0,
            BSTNode(-2,
              BSTNode(-3, empty, empty),
              BSTNode(-1, empty, empty)),
            BSTNode(2,
              BSTNode(1, empty, empty),
              BSTNode(-10, empty, empty)))
    assert not valid_bst(bst)
    
def test_task2_15() -> None:
    empty = BSTEmpty()
    bst = BSTNode(0,
            BSTNode(-2,
              BSTNode(-3, empty, empty),
              BSTNode(1, empty, empty)),
            BSTNode(2,
              BSTNode(1, empty, empty),
              BSTNode(3, empty, empty)))
    assert not valid_bst(bst)
    
def test_task2_16() -> None:
    empty = BSTEmpty()
    bst = BSTNode(0,
            BSTNode(-2,
              BSTNode(-3, empty, empty),
              BSTNode(-1, empty, empty)),
            BSTNode(2,
              BSTNode(-1, empty, empty),
              BSTNode(3, empty, empty)))
    assert not valid_bst(bst)


def test_task3_1() -> None:
    bst = BSTEmptyOpt()
    assert bst.span is None

def test_task3_2() -> None:
    values = [4, 2, 6, 1, 3, 5, 7]
    bst: BSTEmptyOpt | BSTNodeOpt = BSTEmptyOpt()
    for v in values:
        bst = bst.insert(v)
    assert bst.span == (1, 7)

def test_task3_3() -> None:
    values = [4, 2, 1, 3, 6, 5, 7]
    bst: BSTEmptyOpt | BSTNodeOpt = BSTEmptyOpt()
    for v in values:
        bst = bst.insert(v)
    assert bst.span == (1, 7)
    for v in values:
        assert bst.contains(v)
    assert not bst.contains(0)
    assert not bst.contains(8)

def test_task3_4() -> None:
    values = [4, 5, 6, 3]
    bst: BSTEmptyOpt | BSTNodeOpt = BSTEmptyOpt()
    for v in values:
        bst = bst.insert(v)
    assert bst.span == (3, 6)
    for v in values:
        assert bst.contains(v)
    assert not bst.contains(2)
    assert not bst.contains(7)

def test_task3_5() -> None:
    values = [2, 3, 4, 5, 6]
    bst: BSTEmptyOpt | BSTNodeOpt = BSTEmptyOpt()
    for v in values:
        bst = bst.insert(v)
    assert bst.span == (2, 6)
    for v in values:
        assert bst.contains(v)
    assert not bst.contains(1)
    assert not bst.contains(7)

def test_task3_6() -> None:
    values =[0, 3, 5, 2, 9, 4, 8, 6, 1, 7]
    bst: BSTEmptyOpt | BSTNodeOpt = BSTEmptyOpt()
    for v in values:
        bst = bst.insert(v)
    assert bst.span == (0, 9)
    for v in values:
        assert bst.contains(v)
    assert not bst.contains(-1)
    assert not bst.contains(10)

def test_task3_7() -> None:
    values =[6, 3, 2, 4, 9, 5, 7, 8]
    bst: BSTEmptyOpt | BSTNodeOpt = BSTEmptyOpt()
    for v in values:
        bst = bst.insert(v)
    assert bst.span == (2, 9)
    for v in values:
        assert bst.contains(v)
    assert not bst.contains(1)
    assert not bst.contains(10)
    
def test_task3_8() -> None:
    values = [2, 7, 6, 8, 3, 4, 5]
    bst: BSTEmptyOpt | BSTNodeOpt = BSTEmptyOpt()
    for v in values:
        bst = bst.insert(v)
    assert bst.span == (2, 8)
    for v in values:
        assert bst.contains(v)
    assert not bst.contains(1)
    assert not bst.contains(9)
    
def test_task3_9() -> None:
    values =[5, 3, 10, 6, 9, 8, 7, 2, 4]
    bst: BSTEmptyOpt | BSTNodeOpt = BSTEmptyOpt()
    for v in values:
        bst = bst.insert(v)
    assert bst.span == (2, 10)
    for v in values:
        assert bst.contains(v)
    assert not bst.contains(1)
    assert not bst.contains(11)
    
def test_task3_10() -> None:
    values = [8, 5, 7, 9, 6]
    bst: BSTEmptyOpt | BSTNodeOpt = BSTEmptyOpt()
    for v in values:
        bst = bst.insert(v)
    assert bst.span == (5, 9)
    for v in values:
        assert bst.contains(v)
    assert not bst.contains(4)
    assert not bst.contains(10)


def test_task4_1() -> None:
    b = Board(3, 3)
    assert b.dominating is None

def test_task4_2() -> None:
    b = Board(3, 3)
    b.add_piece("BLACK", (0, 0))
    assert b.dominating == "BLACK"

def test_task4_3() -> None:
    b = Board(3, 3)
    b.add_piece("BLACK", (0, 0))
    b.add_piece("WHITE", (0, 1))
    assert b.dominating is None

def test_task4_4() -> None:
    b = Board(3, 3)
    b.add_piece("BLACK", (0, 0))
    b.add_piece("WHITE", (0, 2))
    b.add_piece("BLACK", (0, 1))
    assert b.dominating == "BLACK"

def test_task4_5() -> None:
    b = Board(3, 3)
    b.add_piece("BLACK", (0, 0))
    b.add_piece("WHITE", (0, 1))
    b.add_piece("RED", (0, 2))
    b.add_piece("BLACK", (1, 0))
    b.add_piece("WHITE", (1, 1))
    b.add_piece("BLACK", (1, 2))
    assert b.dominating == "BLACK"

def test_task4_6() -> None:
    b = Board(3, 3)
    b.add_piece("BLACK", (0, 0))
    b.add_piece("WHITE", (0, 1))
    b.add_piece("RED", (0, 2))
    b.add_piece("BLACK", (1, 0))
    b.add_piece("WHITE", (1, 1))
    b.add_piece("RED", (1, 2))
    b.add_piece("RED", (2, 0))
    assert b.dominating == "RED"

