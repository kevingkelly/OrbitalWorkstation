import math
import numpy as np

from math import cos
from math import sin

DEG2RAD = (180./3.14159)

def rand_PI(scale):
    return math.pi*np.random.rand()*scale

def distance (objA, objB):
    delta_x = objA.x-objB.x
    delta_y = objA.y-objB.y
    delta_z = objA.z-objB.z
    delta = math.sqrt(delta_x*delta_x + delta_y*delta_y + delta_z*delta_z)
    # print ("Distance: ", delta_x, delta_y, delta_z, delta)
    return delta
