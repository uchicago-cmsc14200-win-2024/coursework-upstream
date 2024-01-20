from typing import Any, Optional

import pytest

from graphs import Graph, AdjacencyListDigraph, AdjacencyMatrixDigraph
from hw3 import like_component, GoBoard, go_graph


# === generic testers of graph properties and methods

def num_vertices(g: Graph, n: int) -> None:
    assert g.num_vertices == n


def num_edges(g: Graph, n: int) -> None:
    assert g.num_edges == n


def vertex_labels(g: Graph, ss: list[str]) -> None:
    assert g.vertex_labels == set(ss)


def edges(g: Graph, es: list[tuple[str, str]]) -> None:
    assert g.edges == set(es)


def out_neighbors(g: Graph, v: str, vs: list[str]) -> None:
    assert g.out_neighbors(v) == set(vs)


def get_value(g: Graph, v: str, x: Any) -> None:
    assert g.get_value(v) == x


def like(g: Graph, v: str, comp: list[str]) -> None:
    assert like_component(g, v) == set(comp)


# === initialize graphs as test subjects

@pytest.fixture
def ab_list() -> AdjacencyListDigraph:
    g = AdjacencyListDigraph(['a', 'b'])
    g.connect('a', 'b')
    g.set_value('a', 60615)
    g.set_value('b', 60637)

    return g


@pytest.fixture
def ab_mat() -> AdjacencyMatrixDigraph:
    g = AdjacencyMatrixDigraph(['a', 'b'])
    g.connect('a', 'b')
    g.set_value('a', 60615)
    g.set_value('b', 60637)

    return g


@pytest.fixture
def aba_list() -> AdjacencyListDigraph:
    g = AdjacencyListDigraph(['a', 'b'])
    g.connect('a', 'b')
    g.connect('b', 'a')
    g.set_value('a', 60615)
    g.set_value('b', 60637)

    return g


@pytest.fixture
def aba_mat() -> AdjacencyMatrixDigraph:
    g = AdjacencyMatrixDigraph(['a', 'b'])
    g.connect('a', 'b')
    g.connect('b', 'a')
    g.set_value('a', 60615)
    g.set_value('b', 60637)

    return g


@pytest.fixture
def abc_list() -> AdjacencyListDigraph:
    g = AdjacencyListDigraph(['a', 'b', 'c'])
    g.connect('a', 'b')
    g.connect('a', 'c')
    g.connect('b', 'a')
    g.set_value('a', 60615)
    g.set_value('b', 60637)
    g.set_value('c', 60615)

    return g


@pytest.fixture
def abc_mat() -> AdjacencyMatrixDigraph:
    g = AdjacencyMatrixDigraph(['a', 'b', 'c'])
    g.connect('a', 'b')
    g.connect('a', 'c')
    g.connect('b', 'a')
    g.set_value('a', 60615)
    g.set_value('b', 60637)
    g.set_value('c', 60615)

    return g


@pytest.fixture
def k4_list() -> AdjacencyListDigraph:
    g = AdjacencyListDigraph(['1', '2', '3', '4'])
    g.connect('1', '2')
    g.connect('1', '3')
    g.connect('1', '4')
    g.connect('2', '1')
    g.connect('2', '3')
    g.connect('2', '4')
    g.connect('3', '1')
    g.connect('3', '2')
    g.connect('3', '4')
    g.connect('4', '1')
    g.connect('4', '2')
    g.connect('4', '3')
    for v in '1234':
        g.set_value(v, True)

    return g


@pytest.fixture
def k4_mat() -> AdjacencyMatrixDigraph:
    g = AdjacencyMatrixDigraph(['1', '2', '3', '4'])
    g.connect('1', '2')
    g.connect('1', '3')
    g.connect('1', '4')
    g.connect('2', '1')
    g.connect('2', '3')
    g.connect('2', '4')
    g.connect('3', '1')
    g.connect('3', '2')
    g.connect('3', '4')
    g.connect('4', '1')
    g.connect('4', '2')
    g.connect('4', '3')
    for v in '1234':
        g.set_value(v, True)

    return g


@pytest.fixture
def abba() -> Graph:
    g = AdjacencyMatrixDigraph(['a', 'b'])
    g.connect('a', 'b')
    g.connect('b', 'a')
    for v in 'ab':
        g.set_value(v, True)

    return g


# === tests of specific graphs

# --- ab_list

def test_task1_l1(ab_list: AdjacencyListDigraph) -> None:
    num_vertices(ab_list, 2)


def test_task1_l2(ab_list: AdjacencyListDigraph) -> None:
    num_edges(ab_list, 1)


def test_task1_l3(ab_list: AdjacencyListDigraph) -> None:
    vertex_labels(ab_list, ['a', 'b'])


def test_task1_l4(ab_list: AdjacencyListDigraph) -> None:
    edges(ab_list, [('a', 'b')])


def test_task1_l5(ab_list: AdjacencyListDigraph) -> None:
    assert ab_list.connected('a', 'b')


def test_task1_l6(ab_list: AdjacencyListDigraph) -> None:
    assert not (ab_list.connected('b', 'a'))


def test_task1_l7(ab_list: AdjacencyListDigraph) -> None:
    out_neighbors(ab_list, 'a', ['b'])


def test_task1_l8(ab_list: AdjacencyListDigraph) -> None:
    out_neighbors(ab_list, 'b', [])


def test_task1_l9(ab_list: AdjacencyListDigraph) -> None:
    get_value(ab_list, 'a', 60615)


def test_task1_lA(ab_list: AdjacencyListDigraph) -> None:
    get_value(ab_list, 'b', 60637)


def test_task3_lB(ab_list: AdjacencyListDigraph) -> None:
    like(ab_list, 'a', ['a'])


def test_task3_lC(ab_list: AdjacencyListDigraph) -> None:
    like(ab_list, 'b', ['b'])


def test_task1_lD(ab_list: AdjacencyListDigraph) -> None:
    assert isinstance(ab_list.to_adj_list(), AdjacencyListDigraph)


def test_task1_lE(ab_list: AdjacencyListDigraph) -> None:
    assert isinstance(ab_list.to_adj_matrix(), AdjacencyMatrixDigraph)
    

# --- ab_mat

def test_task2_m1(ab_mat: AdjacencyMatrixDigraph) -> None:
    num_vertices(ab_mat, 2)


def test_task2_m2(ab_mat: AdjacencyMatrixDigraph) -> None:
    num_edges(ab_mat, 1)


def test_task2_m3(ab_mat: AdjacencyMatrixDigraph) -> None:
    vertex_labels(ab_mat, ['a', 'b'])


def test_task2_4(ab_mat: AdjacencyMatrixDigraph) -> None:
    edges(ab_mat, [('a', 'b')])


def test_task2_m5(ab_mat: AdjacencyMatrixDigraph) -> None:
    assert ab_mat.connected('a', 'b')


def test_task2_m6(ab_mat: AdjacencyMatrixDigraph) -> None:
    assert not (ab_mat.connected('b', 'a'))


def test_task2_m7(ab_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(ab_mat, 'a', ['b'])


def test_task2_m8(ab_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(ab_mat, 'b', [])


def test_task2_m9(ab_mat: AdjacencyMatrixDigraph) -> None:
    get_value(ab_mat, 'a', 60615)


def test_task2_mA(ab_mat: AdjacencyMatrixDigraph) -> None:
    get_value(ab_mat, 'b', 60637)


def test_task3_mB(ab_mat: AdjacencyMatrixDigraph) -> None:
    like(ab_mat, 'a', ['a'])


def test_task3_mC(ab_mat: AdjacencyMatrixDigraph) -> None:
    like(ab_mat, 'b', ['b'])

    
def test_task1_mD(ab_mat: AdjacencyMatrixDigraph) -> None:
    assert isinstance(ab_mat.to_adj_list(), AdjacencyListDigraph)


def test_task1_mE(ab_mat: AdjacencyMatrixDigraph) -> None:
    assert isinstance(ab_mat.to_adj_matrix(), AdjacencyMatrixDigraph)

    
# --- aba_list

def test_task1_la1(aba_list: AdjacencyListDigraph) -> None:
    num_vertices(aba_list, 2)


def test_task1_la2(aba_list: AdjacencyListDigraph) -> None:
    num_edges(aba_list, 2)


def test_task1_la3(aba_list: AdjacencyListDigraph) -> None:
    vertex_labels(aba_list, ['a', 'b'])


def test_task1_la4(aba_list: AdjacencyListDigraph) -> None:
    edges(aba_list, [('a', 'b'), ('b', 'a')])


def test_task1_la5(aba_list: AdjacencyListDigraph) -> None:
    assert aba_list.connected('a', 'b')


def test_task1_la6(aba_list: AdjacencyListDigraph) -> None:
    assert aba_list.connected('b', 'a')


def test_task1_la7(aba_list: AdjacencyListDigraph) -> None:
    out_neighbors(aba_list, 'a', ['b'])


def test_task1_la8(aba_list: AdjacencyListDigraph) -> None:
    out_neighbors(aba_list, 'b', ['a'])


def test_task1_la9(aba_list: AdjacencyListDigraph) -> None:
    get_value(aba_list, 'a', 60615)


def test_task1_laA(aba_list: AdjacencyListDigraph) -> None:
    get_value(aba_list, 'b', 60637)


def test_task3_laB(aba_list: AdjacencyListDigraph) -> None:
    like(aba_list, 'a', ['a'])


def test_task3_laC(aba_list: AdjacencyListDigraph) -> None:
    like(aba_list, 'b', ['b'])


# --- aba_mat

def test_task2_ma1(aba_mat: AdjacencyMatrixDigraph) -> None:
    num_vertices(aba_mat, 2)


def test_task2_ma2(aba_mat: AdjacencyMatrixDigraph) -> None:
    num_edges(aba_mat, 2)


def test_task2_ma3(aba_mat: AdjacencyMatrixDigraph) -> None:
    vertex_labels(aba_mat, ['a', 'b'])


def test_task2_ma4(aba_mat: AdjacencyMatrixDigraph) -> None:
    edges(aba_mat, [('a', 'b'), ('b', 'a')])


def test_task2_ma5(aba_mat: AdjacencyMatrixDigraph) -> None:
    assert aba_mat.connected('a', 'b')


def test_task2_ma6(aba_mat: AdjacencyMatrixDigraph) -> None:
    assert aba_mat.connected('b', 'a')


def test_task2_ma7(aba_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(aba_mat, 'a', ['b'])


def test_task2_ma8(aba_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(aba_mat, 'b', ['a'])


def test_task2_ma9(aba_mat: AdjacencyMatrixDigraph) -> None:
    get_value(aba_mat, 'a', 60615)


def test_task2_maA(aba_mat: AdjacencyMatrixDigraph) -> None:
    get_value(aba_mat, 'b', 60637)


def test_task3_maB(aba_mat: AdjacencyMatrixDigraph) -> None:
    like(aba_mat, 'a', ['a'])


def test_task3_maC(aba_mat: AdjacencyMatrixDigraph) -> None:
    like(aba_mat, 'b', ['b'])


# --- abc_list

def test_task1_labc1(abc_list: AdjacencyListDigraph) -> None:
    num_vertices(abc_list, 3)


def test_task1_labc2(abc_list: AdjacencyListDigraph) -> None:
    num_edges(abc_list, 3)


def test_task1_labc3(abc_list: AdjacencyListDigraph) -> None:
    vertex_labels(abc_list, ['a', 'b', 'c'])


def test_task1_labc4(abc_list: AdjacencyListDigraph) -> None:
    edges(abc_list, [('a', 'b'), ('b', 'a'), ('a', 'c')])


def test_task1_labc5(abc_list: AdjacencyListDigraph) -> None:
    assert abc_list.connected('a', 'b')


def test_task1_labc6(abc_list: AdjacencyListDigraph) -> None:
    assert abc_list.connected('a', 'c')


def test_task1_labc7(abc_list: AdjacencyListDigraph) -> None:
    assert abc_list.connected('b', 'a')


def test_task1_labc8(abc_list: AdjacencyListDigraph) -> None:
    assert abc_list.connected('a', 'c')


def test_task1_labc9(abc_list: AdjacencyListDigraph) -> None:
    assert not (abc_list.connected('b', 'c'))


def test_task1_labcA(abc_list: AdjacencyListDigraph) -> None:
    out_neighbors(abc_list, 'a', ['b', 'c'])


def test_task1_labcB(abc_list: AdjacencyListDigraph) -> None:
    out_neighbors(abc_list, 'b', ['a'])


def test_task1_labcC(abc_list: AdjacencyListDigraph) -> None:
    out_neighbors(abc_list, 'c', [])


def test_task1_labcD(abc_list: AdjacencyListDigraph) -> None:
    get_value(abc_list, 'a', 60615)


def test_task1_labcE(abc_list: AdjacencyListDigraph) -> None:
    get_value(abc_list, 'b', 60637)


def test_task1_labcF(abc_list: AdjacencyListDigraph) -> None:
    get_value(abc_list, 'c', 60615)


def test_task3_labcG(abc_list: AdjacencyListDigraph) -> None:
    like(abc_list, 'a', ['a', 'c'])


def test_task3_labcH(abc_list: AdjacencyListDigraph) -> None:
    like(abc_list, 'b', ['b'])


def test_task3_labcI(abc_list: AdjacencyListDigraph) -> None:
    like(abc_list, 'c', ['c'])


# --- abc_mat

def test_task2_mabc1(abc_mat: AdjacencyMatrixDigraph) -> None:
    num_vertices(abc_mat, 3)


def test_task2_mabc2(abc_mat: AdjacencyMatrixDigraph) -> None:
    num_edges(abc_mat, 3)


def test_task2_mabc3(abc_mat: AdjacencyMatrixDigraph) -> None:
    vertex_labels(abc_mat, ['a', 'b', 'c'])


def test_task2_mabc4(abc_mat: AdjacencyMatrixDigraph) -> None:
    edges(abc_mat, [('a', 'b'), ('b', 'a'), ('a', 'c')])


def test_task2_mabc5(abc_mat: AdjacencyMatrixDigraph) -> None:
    assert abc_mat.connected('a', 'b')


def test_task2_mabc6(abc_mat: AdjacencyMatrixDigraph) -> None:
    assert abc_mat.connected('a', 'c')


def test_task2_mabc7(abc_mat: AdjacencyMatrixDigraph) -> None:
    assert abc_mat.connected('b', 'a')


def test_task2_mabc8(abc_mat: AdjacencyMatrixDigraph) -> None:
    assert abc_mat.connected('a', 'c')


def test_task2_mabc9(abc_mat: AdjacencyMatrixDigraph) -> None:
    assert not (abc_mat.connected('b', 'c'))


def test_task2_mabcA(abc_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(abc_mat, 'a', ['b', 'c'])


def test_task2_mabcB(abc_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(abc_mat, 'b', ['a'])


def test_task2_mabcC(abc_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(abc_mat, 'c', [])


def test_task2_mabcD(abc_mat: AdjacencyMatrixDigraph) -> None:
    get_value(abc_mat, 'a', 60615)


def test_task2_mabcE(abc_mat: AdjacencyMatrixDigraph) -> None:
    get_value(abc_mat, 'b', 60637)


def test_task2_mabcF(abc_mat: AdjacencyMatrixDigraph) -> None:
    get_value(abc_mat, 'c', 60615)


def test_task3_mabcG(abc_mat: AdjacencyMatrixDigraph) -> None:
    like(abc_mat, 'a', ['a', 'c'])


def test_task3_mabcH(abc_mat: AdjacencyMatrixDigraph) -> None:
    like(abc_mat, 'b', ['b'])


def test_task3_mabcI(abc_mat: AdjacencyMatrixDigraph) -> None:
    like(abc_mat, 'c', ['c'])


# --- k4_list

def test_task1_k4l1(k4_list: AdjacencyListDigraph) -> None:
    num_vertices(k4_list, 4)


def test_task1_k4l2(k4_list: AdjacencyListDigraph) -> None:
    num_edges(k4_list, 12)


def test_task1_k4l3(k4_list: AdjacencyListDigraph) -> None:
    vertex_labels(k4_list, ['1', '2', '3', '4'])


def test_task1_k4l4(k4_list: AdjacencyListDigraph) -> None:
    edges(k4_list, [('1', '2'), ('1', '3'), ('1', '4'),
                    ('2', '1'), ('2', '3'), ('2', '4'),
                    ('3', '1'), ('3', '2'), ('3', '4'),
                    ('4', '1'), ('4', '2'), ('4', '3')])


def test_task1_k4l5(k4_list: AdjacencyListDigraph) -> None:
    assert k4_list.connected('1', '2')


def test_task1_k4l6(k4_list: AdjacencyListDigraph) -> None:
    assert k4_list.connected('1', '3')


def test_task1_k4l7(k4_list: AdjacencyListDigraph) -> None:
    assert k4_list.connected('2', '3')


def test_task1_k4l8(k4_list: AdjacencyListDigraph) -> None:
    assert k4_list.connected('2', '4')


def test_task1_k4l9(k4_list: AdjacencyListDigraph) -> None:
    assert not (k4_list.connected('3', '3'))


def test_task1_k4lA(k4_list: AdjacencyListDigraph) -> None:
    out_neighbors(k4_list, '1', ['2', '3', '4'])


def test_task1_k4lB(k4_list: AdjacencyListDigraph) -> None:
    out_neighbors(k4_list, '2', ['1', '3', '4'])


def test_task1_k4lC(k4_list: AdjacencyListDigraph) -> None:
    out_neighbors(k4_list, '3', ['1', '2', '4'])


def test_task1_k4lD(k4_list: AdjacencyListDigraph) -> None:
    out_neighbors(k4_list, '4', ['1', '2', '3'])


def test_task1_k4lE(k4_list: AdjacencyListDigraph) -> None:
    get_value(k4_list, '1', True)


def test_task3_k4lF(k4_list: AdjacencyListDigraph) -> None:
    like(k4_list, '1', ['1', '2', '3', '4'])


def test_task3_k4lG(k4_list: AdjacencyListDigraph) -> None:
    like(k4_list, '2', ['1', '2', '3', '4'])


def test_task3_k4lH(k4_list: AdjacencyListDigraph) -> None:
    like(k4_list, '3', ['1', '2', '3', '4'])


def test_task3_k4lI(k4_list: AdjacencyListDigraph) -> None:
    like(k4_list, '4', ['1', '2', '3', '4'])


# --- k4_mat

def test_task2_k4m1(k4_mat: AdjacencyMatrixDigraph) -> None:
    num_vertices(k4_mat, 4)


def test_task2_k4m2(k4_mat: AdjacencyMatrixDigraph) -> None:
    num_edges(k4_mat, 12)


def test_task2_k4m3(k4_mat: AdjacencyMatrixDigraph) -> None:
    vertex_labels(k4_mat, ['1', '2', '3', '4'])


def test_task2_k4m4(k4_mat: AdjacencyMatrixDigraph) -> None:
    edges(k4_mat, [('1', '2'), ('1', '3'), ('1', '4'),
                   ('2', '1'), ('2', '3'), ('2', '4'),
                   ('3', '1'), ('3', '2'), ('3', '4'),
                   ('4', '1'), ('4', '2'), ('4', '3')])


def test_task2_k4m5(k4_mat: AdjacencyMatrixDigraph) -> None:
    assert k4_mat.connected('1', '2')


def test_task2_k4m6(k4_mat: AdjacencyMatrixDigraph) -> None:
    assert k4_mat.connected('1', '3')


def test_task2_k4m7(k4_mat: AdjacencyMatrixDigraph) -> None:
    assert k4_mat.connected('2', '3')


def test_task2_k4m8(k4_mat: AdjacencyMatrixDigraph) -> None:
    assert k4_mat.connected('2', '4')


def test_task2_k4m9(k4_mat: AdjacencyMatrixDigraph) -> None:
    assert not (k4_mat.connected('3', '3'))


def test_task2_k4mA(k4_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(k4_mat, '1', ['2', '3', '4'])


def test_task2_k4mB(k4_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(k4_mat, '2', ['1', '3', '4'])


def test_task2_k4mC(k4_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(k4_mat, '3', ['1', '2', '4'])


def test_task2_k4mD(k4_mat: AdjacencyMatrixDigraph) -> None:
    out_neighbors(k4_mat, '4', ['1', '2', '3'])


def test_task2_k4mE(k4_mat: AdjacencyMatrixDigraph) -> None:
    get_value(k4_mat, '1', True)


def test_task3_k4mF(k4_mat: AdjacencyMatrixDigraph) -> None:
    like(k4_mat, '1', ['1', '2', '3', '4'])


def test_task3_k4mG(k4_mat: AdjacencyMatrixDigraph) -> None:
    like(k4_mat, '2', ['1', '2', '3', '4'])


def test_task3_k4mH(k4_mat: AdjacencyMatrixDigraph) -> None:
    like(k4_mat, '3', ['1', '2', '3', '4'])


def test_task3_k4mI(k4_mat: AdjacencyMatrixDigraph) -> None:
    like(k4_mat, '4', ['1', '2', '3', '4'])


# === test go_graph

@pytest.fixture()
def go_graph2() -> Graph:
    board2: GoBoard = GoBoard(2)
    g: Graph = go_graph(board2)

    return g


def test_task4_gg1(go_graph2: Graph) -> None:
    num_vertices(go_graph2, 4)


def test_task4_gg2(go_graph2: Graph) -> None:
    num_edges(go_graph2, 8)


def test_task4_gg3(go_graph2: Graph) -> None:
    vertex_labels(go_graph2, ['0:0', '0:1', '1:0', '1:1'])


def test_task4_gg4(go_graph2: Graph) -> None:
    def both(a: str, b: str) -> list[tuple[str, str]]: return [(a, b), (b, a)]

    edges(go_graph2, both('0:0', '0:1') +
          both('0:1', '1:1') +
          both('1:1', '1:0') +
          both('1:0', '0:0'))


def test_task4_gg5(go_graph2: Graph) -> None:
    out_neighbors(go_graph2, '0:0', ['0:1', '1:0'])


def test_task4_gg6(go_graph2: Graph) -> None:
    out_neighbors(go_graph2, '0:1', ['0:0', '1:1'])


def test_task4_gg7(go_graph2: Graph) -> None:
    out_neighbors(go_graph2, '1:0', ['0:0', '1:1'])


def test_task4_gg8(go_graph2: Graph) -> None:
    out_neighbors(go_graph2, '1:1', ['0:1', '1:0'])


def test_task4_gg9(go_graph2: Graph) -> None:
    get_value(go_graph2, '1:1', None)


def test_task4_ggA(go_graph2: Graph) -> None:
    like(go_graph2, '0:0', ['0:0', '0:1', '1:0', '1:1'])


# --- now test a board with some pieces on it
@pytest.fixture()
def go_graph3() -> Graph:
    board3: GoBoard = GoBoard(3)

    # 0,0 is upper left in this diagram
    # B B B
    # B W W
    # W . W

    board3.put(0, 0, 'BLACK')
    board3.put(1, 0, 'BLACK')
    board3.put(2, 0, 'BLACK')
    board3.put(0, 1, 'BLACK')
    board3.put(0, 2, 'WHITE')
    board3.put(1, 1, 'WHITE')
    board3.put(2, 1, 'WHITE')
    board3.put(2, 2, 'WHITE')

    g: Graph = go_graph(board3)

    return g

def test_task4_ggg1(go_graph3: Graph) -> None:
    num_vertices(go_graph3, 9)


def test_task4_ggg2(go_graph3: Graph) -> None:
    num_edges(go_graph3, 24)


def test_task4_ggg3(go_graph3: Graph) -> None:
    out_neighbors(go_graph3, '0:0', ['0:1', '1:0'])


def test_task4_ggg4(go_graph3: Graph) -> None:
    out_neighbors(go_graph3, '0:1', ['0:0', '1:1', '0:2'])


def test_task4_ggg5(go_graph3: Graph) -> None:
    out_neighbors(go_graph3, '1:1', ['0:1', '1:0', '2:1', '1:2'])


def test_task4_ggg6(go_graph3: Graph) -> None:
    like(go_graph3, '0:0', ['0:0', '1:0', '2:0', '0:1'])


def test_task4_ggg7(go_graph3: Graph) -> None:
    like(go_graph3, '2:0', ['0:0', '1:0', '2:0', '0:1'])


def test_task4_ggg8(go_graph3: Graph) -> None:
    like(go_graph3, '0:2', ['0:2'])


def test_task4_ggg9(go_graph3: Graph) -> None:
    like(go_graph3, '1:1', ['1:1', '2:1', '2:2'])


def test_task4_gggA(go_graph3: Graph) -> None:
    like(go_graph3, '1:2', ['1:2'])


# make sure like_component doesn't iterate forever

def test_task4_abba_a(abba: Graph) -> None:
    like(abba, 'a', ['a','b'])

def test_task4_abba_b(abba: Graph) -> None:
    like(abba, 'b', ['a','b'])


# another board with stones not adjacent to one another

@pytest.fixture()
def go_graphX() -> Graph:
    boardX: GoBoard = GoBoard(3)

    # 0,0 is upper left in this diagram
    # B W B
    # . B W
    # B . B

    boardX.put(0, 0, 'BLACK')
    boardX.put(1, 0, 'WHITE')
    boardX.put(2, 0, 'BLACK')
    boardX.put(1, 1, 'BLACK')
    boardX.put(2, 1, 'WHITE')
    boardX.put(0, 2, 'BLACK')
    boardX.put(2, 2, 'BLACK')

    g: Graph = go_graph(boardX)

    return g




def test_task4_ggx1(go_graphX: Graph) -> None:
    like(go_graphX, '0:0', ['0:0'])


def test_task4_ggx2(go_graphX: Graph) -> None:
    like(go_graphX, '1:0', ['1:0'])


def test_task4_ggx3(go_graphX: Graph) -> None:
    like(go_graphX, '2:0', ['2:0'])


def test_task4_ggx4(go_graphX: Graph) -> None:
    like(go_graphX, '0:1', ['0:1'])


def test_task4_ggx5(go_graphX: Graph) -> None:
    like(go_graphX, '1:1', ['1:1'])


def test_task4_ggx6(go_graphX: Graph) -> None:
    like(go_graphX, '1:2', ['1:2'])


def test_task4_ggx7(go_graphX: Graph) -> None:
    like(go_graphX, '2:0', ['2:0'])


def test_task4_ggx8(go_graphX: Graph) -> None:
    like(go_graphX, '2:1', ['2:1'])


def test_task4_ggx9(go_graphX: Graph) -> None:
    like(go_graphX, '2:2', ['2:2'])
