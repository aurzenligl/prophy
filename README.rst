.. image:: https://img.shields.io/pypi/v/prophy.svg
    :target: https://pypi.python.org/pypi/prophy
    :alt: Pypi Package Version
.. image:: https://img.shields.io/pypi/pyversions/prophy.svg
    :target: https://pypi.python.org/pypi/prophy
    :alt: Supported Python Versions
.. image:: https://readthedocs.org/projects/prophy/badge
    :target: http://prophy.readthedocs.io/en/latest
    :alt: Documentation Status
.. image:: https://coveralls.io/repos/github/aurzenligl/prophy/badge.svg?branch=master
    :target: https://coveralls.io/github/aurzenligl/prophy?branch=master
    :alt: Coverage Status
.. image:: https://travis-ci.org/aurzenligl/prophy.svg?branch=master
    :target: https://travis-ci.org/aurzenligl/prophy
    :alt: Travis-CI Build Status

Prophy is a statically typed, binary, tag-free, unpacked serialization protocol.

You can define message schema::

    struct MyMsg
    {
        u16 x<>;
    };

generate codecs for chosen languages::

    prophyc --python_out . --cpp_full_out . --cpp_out . test.prophy

and serialize data in Python::

    >>> import test
    >>> msg = test.MyMsg()
    >>> msg.x[:] = [1, 2, 3]
    >>> msg.encode('<')
    '\x03\x00\x00\x00\x01\x00\x02\x00\x03\x00\x00\x00'
    >>> print msg
    x: 1
    x: 2
    x: 3

in C++::

    #include <iostream>
    #include <iterator>
    #include "test.ppf.hpp"

    int main()
    {
        prophy::generated::MyMsg msg{{1, 2, 3}};
        std::vector<uint8_t> data = msg.encode();
        std::copy(data.begin(), data.end(), std::ostream_iterator<unsigned>(std::cout, " "));
        std::cout << '\n' << msg.print();
        return 0;
    }

::

    3 0 0 0 1 0 2 0 3 0 0 0
    x: 1
    x: 2
    x: 3

again in C++ (half hand-rolled, compiler-dependent, but fastest option)::

    #include <iostream>
    #include <iterator>
    #include <cstdlib>
    #include "test.pp.hpp"

    int main()
    {
        MyMsg* msg = static_cast<MyMsg*>(std::malloc(12));
        msg->num_of_x = 3;
        msg->x[0] = 1;
        msg->x[1] = 2;
        msg->x[2] = 3;
        std::copy((uint8_t*)msg, ((uint8_t*)msg) + 12, std::ostream_iterator<unsigned>(std::cout, " "));
        std::cout << '\n';
        return 0;
    }

::

    3 0 0 0 1 0 2 0 3 0 0 0

Documentation: http://prophy.readthedocs.org

Issues: https://github.com/aurzenligl/prophy/issues
