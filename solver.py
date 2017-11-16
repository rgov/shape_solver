#!/usr/bin/env python

import numpy as np
import shapeopPython


class ShapeSolver(object):
  def __init__(self, capacity=10):
    self.npoints = 0
    self.constraints = []
    self.capacity = capacity
    self.data = np.zeros((3, self.capacity), dtype=np.float64)
  
  def resize(self, capacity):
    newcols = np.zeros(
      (self.data.shape[0], capacity - self.capacity),
      dtype=np.float64
    )
    self.data = np.concatenate((self.data, newcols), axis=1)
    self.capacity = capacity
  
  def point(self, initial=(0.0, 0.0, 0.0)):
    out, self.npoints = self.npoints, self.npoints + 1
    if self.npoints > self.capacity:
      self.resize(2 * self.npoints)
    self.data[:,self.npoints - 1] = initial
    return out
  
  def points(self, n, initial=(0.0, 0.0, 0.0)):
    out, self.npoints = range(self.npoints, self.npoints + n), self.npoints + n
    # TODO: Resize if npoints > capacity
    if self.npoints > self.capacity:
      self.resize(2 * self.npoints)
    for c in xrange(self.npoints - n, self.npoints):
      self.data[:,c] = initial  # TODO: Magic one-line np invocation?
    return out
  
  def set(self, n, value):
    self.data[:,n] = value
  
  def get(self, n):
    return tuple(self.data[:,n])
  
  def all_points(self):
    return range(self.npoints)
  
  def add(self, c, weight=1.0):
    self.constraints.append((c, weight))
  
  def solve(self, niter):
    s = shapeopPython.shapeop_create()
    
    # Doesn't seem that we could just create a doubleArray that references the
    # same underlying data
    array = shapeopPython.doubleArray(self.data.shape[0] * self.npoints)
    for y in xrange(self.data.shape[0]):
      for x in xrange(self.npoints):
        array[self.data.shape[0] * x + y] = self.data[y,x]
    shapeopPython.shapeop_setPoints(s, array, self.npoints)
    
    for c, w in self.constraints:
      ids = shapeopPython.intArray(len(c.args))
      for i in xrange(len(c.args)):
        ids[i] = c.args[i]
      shapeopPython.shapeop_addConstraint(s, c.__cname__, ids, len(c.args), w)
    
    shapeopPython.shapeop_init(s)
    shapeopPython.shapeop_solve(s, niter)
    shapeopPython.shapeop_getPoints(s, array, self.npoints)
    shapeopPython.shapeop_delete(s)
    
    # np might be more willing to convert from raw memory, but we'll just
    # copy it back to the data manually
    for y in xrange(self.data.shape[0]):
      for x in xrange(self.npoints):
        self.data[y,x] = array[self.data.shape[0] * x + y]


class Constraint(object):
  def __new__(cls, *args, **kwargs):
    if cls == Constraint:
      raise Exception('Do not instantiate Constraint directly')
    return super(Constraint, cls).__new__(cls, *args, **kwargs)
  
  def __init__(self, args):
    if isinstance(args, int):
      if self.__argc__[0] != 1:
        raise ValueError('Expected a list of points, got one point')
      self.args = [ args ]
      return
    
    if len(args) < self.__argc__[0]:
      raise ValueError(
        'Too few arguments for %s constraint (expected %d, got %d)' \
        % (self.__cname__, self.__argc__[0], len(args)))
    if self.__argc__[1] is not None and len(args) > self.__argc__[1]:
      raise ValueError(
        'Too many arguments for %s constraint (expected %d, got %d)' \
        % (self.__cname__, self.__argc__[1], len(args)))
    self.args = list(args)

# FIXME: What about additional arguments?

class EdgeStrainConstraint(Constraint):
  __cname__ = "EdgeStrain"
  __argc__ = (2, 2)
class TriangleStrainConstraint(Constraint):
  __cname__ = "TriangleStrain"
  __argc__ = (3, 3)
class TetrahedronStrainConstraint(Constraint):
  __cname__ = "TetrahedronStrain"
  __argc__ = (4, 4)
class AreaConstraint(Constraint):
  __cname__ = "Area"
  __argc__ = (3, 3)
class VolumeConstraint(Constraint):
  __cname__ = "Volume"
  __argc__ = (4, 4)
class BendingConstraint(Constraint):
  __cname__ = "Bending"
  __argc__ = (4, 4)
class ClosenessConstraint(Constraint):
  __cname__ = "Closeness"
  __argc__ = (1, 1)
class LineConstraint(Constraint):
  __cname__ = "Line"
  __argc__ = (2, None)
class PlaneConstraint(Constraint):
  __cname__ = "Plane"
  __argc__ = (3, None)
class CircleConstraint(Constraint):
  __cname__ = "Circle"
  __argc__ = (4, None)
class SphereConstraint(Constraint):
  __cname__ = "Sphere"
  __argc__ = (4, None)
class SimilarityConstraint(Constraint):
  __cname__ = "Similarity"
  __argc__ = (1, None)
class RigidConstraint(Constraint):
  __cname__ = "Rigid"
  __argc__ = (1, None)
class RectangleConstraint(Constraint):
  __cname__ = "Rectangle"
  __argc__ = (4, 4)
class ParallelogramConstraint(Constraint):
  __cname__ = "Parallelogram"
  __argc__ = (4, 4)
class LaplacianConstraint(Constraint):
  __cname__ = "Laplacian"
  __argc__ = (2, None)
class LaplacianDisplacementConstraint(Constraint):
  __cname__ = "LaplacianDisplacement"
  __argc__ = (2, None)
class AngleConstraint(Constraint):
  __cname__ = "Angle"
  __argc__ = (3, 3)
