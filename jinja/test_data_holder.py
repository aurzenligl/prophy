import os
import pytest

def sort_list(dic):
    out_list = []

    for key, val in dic.iteritems():
        if "_" not in val:
            out_list.insert(0,key)
        else:
            if val in out_list:
                index = out_list.index(val)
                out_list.insert(index + 1, key)
            else:
                out_list.append(key)
    return out_list



def test_of_sorter():
    dic = {"CONST_A": "CONST_B", "CONST_B": "5", "CONST_C": "4"}

    l = ['CONST_B', 'CONST_A', 'CONST_C']

    assert l == sort_list(dic)

def test_of_sorter_2():
    dic = {"C_A" : "C_B", "C_B" : "C_C", "C_C" : "5"}
    l = ['C_C', 'C_B', 'C_A']

    assert l == sort_list(dic)

def test_of_sorter_3():
    dic = {"C_A1" : "C_B", "C_A2" : "C_B" , "C_B" : "5"}
    l = ['C_B', 'C_A2', 'C_A1']
    assert l == sort_list(dic)

def test_of_sorter_4():
    dic = {"CC" : "5", "CB":"CC", "CA1":"CB", "CA2":"CB"}
    l = ["CA2","CA1","CB","CC"]
    assert l == sort_list(dic)


def test_of_ecev_of_file():
    from dic import dic

    sort = sort_list(dic)

    f = "";

    for x in sort:
        f += x + " = " + dic[x] + "\n"

    try:
        exec f
    except NameError, e:
        pytest.fail(e)

