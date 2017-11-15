#!/usr/bin/env python

from solver import *

s = ShapeSolver()

a = s.point((0.0, 0.0, 0.0))
b = s.point((0.5, 0.0, 1.0))
c = s.point((0.5, 1.0, 0.0))
d = s.point((0.0, 1.0, 1.0))

s.add(PlaneConstraint([a,b,c,d]))
s.add(ClosenessConstraint(a))
s.add(ClosenessConstraint(d))

s.solve(10)

print 'a =', s.get(a)
print 'b =', s.get(b)
print 'c =', s.get(c)
print 'd =', s.get(d)
