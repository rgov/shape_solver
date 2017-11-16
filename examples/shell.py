#!/usr/bin/env python
'''
Implements the constraints found in the paper

  Mario Deuss, Anders Holden Deleuran, Sofien Bouaziz, Bailin Deng, Daniel
  Piker, and Mark Pauly. 2015. ShapeOp - A Robust and Extensible Geometric
  Modelling Paradigm. Design Modelling Symposium.

The shell is described as follows:

  The vertices on the parameter lines of a quad-mesh are constrained to always
  lie on a circular arc using the circle constraint. Each face is constrained
  towards being square using the similarity constraint. Five vertices are
  anchored to different positions than their initial positions, enabling shape
  exploration.
'''
import os, sys; sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from solver import *

s = ShapeSolver()

# Construct a mesh
w, h, sz = 11, 11, 10
mesh = [ [ None ] * w for _ in xrange(h) ]
for x in xrange(w):
  for y in xrange(h):
    mesh[y][x] = s.point((sz * x, sz * y, 0.0))

# Give each quad in the mesh a similarity constraint to try to preserve shape
for x in xrange(w-1):
  for y in xrange(h-1):
    pts = [ mesh[y][x], mesh[y+1][x], mesh[y+1][x+1], mesh[y][x+1] ]
    s.add(SimilarityConstraint(pts))

# Bind the center point to be constrained near where we placed it
s.add(ClosenessConstraint(mesh[h/2][w/2]))

# Now add an anchor quad, centered below and fixed in place
a1 = s.point((sz * (w/2) - (sz/2.0), sz * (h/2) - (sz/2.0), -5.0 * sz))
a2 = s.point((sz * (w/2) + (sz/2.0), sz * (h/2) - (sz/2.0), -5.0 * sz))
a3 = s.point((sz * (w/2) - (sz/2.0), sz * (h/2) + (sz/2.0), -5.0 * sz))
a4 = s.point((sz * (w/2) + (sz/2.0), sz * (h/2) + (sz/2.0), -5.0 * sz))
for pt in (a1, a2, a3, a4):
  s.add(ClosenessConstraint(pt))

# Constrain each row and then each column to lie on a circle that includes the
# anchor quad
for y in xrange(h):
  pts = [ mesh[y][x] for x in xrange(w) ] + [ a1, a2 ]
  s.add(CircleConstraint(pts))
for x in xrange(w):
  pts = [ mesh[y][x] for y in xrange(h) ] + [ a2, a3 ]
  s.add(CircleConstraint(pts))

# FIXME
# This isn't quite correct... I'm not sure how the anchor quad is used
# to constrain the other points.

# Run the solver
s.solve(300)

# Output the solution as an STL file
if sys.stdout.isatty():
  print 'Mesh computed. Redirect output to a file to save as STL file.'
else:
  print 'solid mesh'
  
  # This part outputs the anchor quad; omit if you don't want it
  print
  print '  facet normal 1.0 0.0 0.0'
  print '    vertex %f %f %f' % s.get(a1)
  print '    vertex %f %f %f' % s.get(a2)
  print '    vertex %f %f %f' % s.get(a3)
  print '  endfacet'
  print '  facet normal 1.0 0.0 0.0'
  print '    vertex %f %f %f' % s.get(a2)
  print '    vertex %f %f %f' % s.get(a3)
  print '    vertex %f %f %f' % s.get(a4)
  print '  endfacet'
  
  print
  for x in xrange(w-1):
    for y in xrange(h-1):
      print '  facet normal 1.0 0.0 0.0'  # FIXME: what normal should I use?
      print '    vertex %f %f %f' % s.get(mesh[y][x+1])
      print '    vertex %f %f %f' % s.get(mesh[y+1][x])
      print '    vertex %f %f %f' % s.get(mesh[y+1][x+1])
      print '  endfacet'
      print '  facet normal 1.0 0.0 0.0'
      print '    vertex %f %f %f' % s.get(mesh[y][x])
      print '    vertex %f %f %f' % s.get(mesh[y][x+1])
      print '    vertex %f %f %f' % s.get(mesh[y+1][x])
      print '  endfacet' 
  print 'endsolid'
