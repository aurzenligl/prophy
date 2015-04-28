#!/bin/bash

VERSION=$(grep -Po "version = '\K[0-9.]*" setup.py)

cd prophy_cpp
tar zcvf prophy-cpp-${VERSION}.tar.gz include
cd -
