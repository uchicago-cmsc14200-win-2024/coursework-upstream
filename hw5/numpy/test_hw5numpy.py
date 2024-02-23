import pytest
import pandas as pd
import os

from hw5numpy import (
    NDArray,
    NDArray1,
    NDArray2
)

def test_task1_init1() -> None:
    d = NDArray1([1,2,3])
    assert len(d._data)==3

def test_task1_plus1() -> None:
    d = NDArray1([1,2,3])
    assert (d+1)._data==[2,3,4]

def test_task1_plus2() -> None:
    d = NDArray1([1,2,3])
    assert (d+d)._data==[2,4,6]

def test_task1_plus3() -> None:
    d = NDArray1([1,2,3])
    assert (d+d+1)._data==[3,5,7]

def test_task1_plus4() -> None:
    d = NDArray1([1,2,3])
    e = NDArray1([2])
    with pytest.raises(ValueError):
        d+e

def test_task1_plus5() -> None:
    d = NDArray1([10,20,30,200,300,400])
    assert (d+9)._data==[19,29,39,209,309,409]
    
def test_task1_gt1() -> None:
    d = NDArray1([1,2,3])
    assert (d>2)==[False,False,True]

def test_task1_gt2() -> None:
    d = NDArray1([1,2,3])
    assert (d>10)==[False,False,False]

def test_task1_gt3() -> None:
    d = NDArray1([1,2,3])
    assert (d>0)==[True,True,True]

def test_task1_gt4() -> None:
    d = NDArray1(list(range(1000)))
    assert (d>-1)==([True]*1000)

def test_task1_in1() -> None:
    d = NDArray1([1,2,3])
    assert 1 in d

def test_task1_in2() -> None:
    d = NDArray1([1,2,3])
    assert 11 not in d

def test_task1_in3() -> None:
    d = NDArray1(list(range(1000)))
    assert 123 in d

def test_task1_in4() -> None:
    d = NDArray1(list(range(1000)))
    assert 999 in d

def test_task1_in5() -> None:
    d = NDArray1(list(range(1000)))
    assert 9999 not in d

def test_task1_shape1() -> None:
    d = NDArray1([1,2,3])
    assert d.shape==3

def test_task1_shape2() -> None:
    d = NDArray1(list(range(1000)))
    assert d.shape==1000

def test_task1_eq1() -> None:
    d = NDArray1([1,2,3])
    e = NDArray1([1,2,3])
    assert d==e and e==d and d is not e and e is not d

def test_task1_eq2() -> None:
    d = NDArray1([1,2,3])
    e = NDArray1([3,2,1])
    assert d!=e and e!=d

def test_task1_eq3() -> None:
    d = NDArray1(list(range(789)))
    e = NDArray1(list(range(789)))
    assert d==e and e==d and d is not e and e is not d

def test_task1_T1() -> None:
    d = NDArray1([1,2,3])
    assert d.T.data==[[1],[2],[3]]

def test_task1_T2() -> None:
    d = NDArray1([1])
    assert d.T.data==[[1]]

def test_task1_T3() -> None:
    d = NDArray1(list(range(100)))
    assert d.T.data==list(map(lambda n: [n], range(100)))

def test_task2_init1() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    assert d.shape==(2,3)
    
def test_task2_init2() -> None:
    with pytest.raises(ValueError):
        d = NDArray2([[1,2,3],[4,5,6,7]])
        
def test_task2_init3() -> None:
    with pytest.raises(ValueError):
        d = NDArray2([[1,2,3],[4,7]])
    
def test_task2_plus1() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    assert (d+1).data==[[2,3,4],[5,6,7]]
    
def test_task2_plus2() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    assert (d+d).data==[[2,4,6],[8,10,12]]

def test_task2_plus3() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    e = NDArray2([[1],[2]])
    with pytest.raises(ValueError):
        d+e

def test_task2_gt1() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    assert (d>2)==[[False,False,True],[True,True,True]]

def test_task2_gt2() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    assert (d>22)==[[False,False,False],[False,False,False]]

def test_task2_gt3() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    assert (d>0)==[[True,True,True],[True,True,True]]

def test_task2_in1() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    assert 2 in d and 6 in d

def test_task2_in2() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    assert 0 not in d and 66 not in d

def test_task2_eq1() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    e = NDArray2([[1,2,3],[4,5,6]])
    assert d==e and e==d and d is not e and e is not d
    
def test_task2_eq2() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    e = 'foo'
    assert d!=e

def test_task2_eq3() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    e = NDArray2([[1,2],[3,4],[5,6]])
    assert d!=e

def test_task2_eq4() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    e = NDArray1([1,2,3,4,5,6])
    assert d!=e and e!=d
    
def test_task2_eq5() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    e = NDArray2([[1,2,3],[4,0,6]])
    assert d!=e

def test_task2_eq6() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    e = NDArray2([[1,2,3],[4,5,69]])
    assert d!=e

def test_task2_shape1() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    assert d.shape==(2,3)

def test_task2_shape2() -> None:
    d = NDArray2([[1,2],[3,4],[5,6]])
    assert d.shape==(3,2)

def test_task2_T1() -> None:
    d = NDArray2([[1,2,3],[4,5,6]])
    assert d.T.shape==(3,2) and d.T.data==[[1,4],[2,5],[3,6]]

def test_task2_T2() -> None:
    d = NDArray2([[1],[2],[3]])
    assert d.T.shape==3 and d.T.data==[1,2,3]
