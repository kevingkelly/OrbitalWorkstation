#!/usr/bin/python3
        
import math
import numpy as np

from math import cos
from math import sin

import Projectile as prj
import Earth
import orbitalUtilities as util

import atmosphere
 
# For projectiles, only circular orbits have been implemented so
# set the Semimajor Axis, the Eccentricity, Inclination, Right Acension of the Ascending Node,
# and the True Anomaly
#       objNum
#       objName
#       objEpochDate
#       objEpochTime
#       objDragCoeff
#       objInclination, objRightAscension
#       objSemiMajorAxis
#       objMeanAnomaly, objTrueAnomaly


print (" initialize objects")

dayInSeconds = 8 # 86400.
numberOfObjects = 2 # 10
positions = []
objs = []
for i in range(0,numberOfObjects):
    inclination = util.rand_PI(0.5)
    rightAscension = util.rand_PI(2)
    semiMajorAxis = Earth.radius+1e6+(300.*np.random.rand())
    anomaly = util.rand_PI(2)
    objs.append(prj.Projectile(i,"    ", 0., 0., 0.,
                           inclination, rightAscension, semiMajorAxis, anomaly, 0.))
for i in range (0,numberOfObjects):
    positions.append(objs[i].propagate(dayInSeconds))
    
try:
    file1 = open('obj1.txt', 'w+')
    file2 = open('obj2.txt', 'w+')
    file3 = open('obj3.txt', 'w+')
    file_dist = open('dist.txt', 'w+')
except IOError:
    print ("Error opening files")

delta_t = 100

for t in range(8):
    time = t*delta_t
##    pos1 = objs[1].propogate(time)
##    pos2 = objs[2].propogate(time)
##    pos3 = objs[3].propogate(time)
##
##    drag1 = objs[1].atmospheric_drag();
##
##    file1.write("%f %f %f %f\n" % (time,pos1.x,pos1.y,pos1.z))
##    file2.write("%f %f %f %f\n" % (time,pos2.x,pos2.y,pos2.z))
##    file3.write("%f %f %f %f\n" % (time,pos3.x,pos3.y,pos3.z))
##    delta_12 = distance(obj1, obj2)
##    delta_13 = distance(obj1, obj3)
##    file_dist.write("%f %f %f\n" % (time,delta_12,delta_13))

print ("Completed")
file1.close()
file2.close()
file3.close()
file_dist.close()

print ("Closed")
