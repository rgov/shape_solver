# shape_solver

This is a Python interface for the [ShapeOp](http://shapeop.org/) geometric
constraint solver. It improves on the SWIG interface by providing a more
natural way to express constraints in the Python language.

## Building

Download ShapeOp 0.1.0 and place it in this directory. Then, run `build.sh` to
compile it and copy the Python bindings.

## Finding 2D solutions

ShapeOp finds 3-dimensional solutions. To constrain the solution to be on the
plane z = 0, define 3 non-colinear points on that plane and then constrain all
points to be coplanar with them.

    z1 = s.point((1.0, 0.0, 0.0))
    z2 = s.point((0.0, 1.0, 0.0))
    z3 = s.point((1.0, 1.0, 0.0))
    s.add(PlaneConstraint(s.all_points()))
