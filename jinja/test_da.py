import pytest
from data_holder import DataHolder as dh
from data_holder import ConstantHolder as ch
import dic


def test_of_sorting_of_constant():

    cho = ch()
    cho.add_to_list("C_A","5");
    cho.add_to_list("C_B","3");
    cho.add_to_list("C_C","C_A + C_B");

    l = [('C_B', '3'), ('C_A', '5'), ('C_C', 'C_A + C_B')]
    print cho.get_sorted_list()
    assert l == cho.get_sorted_list()




