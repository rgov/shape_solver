#!/bin/sh

mkdir build
pushd build
cmake -D SWIG_PYTHON=1 ../ShapeOp.0.1.0
cmake --build .
popd

cp build/libShapeOp/bindings/python/{_shapeopPython.so,shapeopPython.py} .
