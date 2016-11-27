#!/usr/bin/python3
        
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

def standard_atmosphere(altitude):

    zone = [86000, 91000, 100000, 110000, 120000, 150000, 
        200000, 300000, 500000, 750000, 1000000]

    parameters = [ 
        [0.000000, -3.322622E-06, 9.111460E-04, -0.2609971, 5.944694],
        [0.000000, 2.873405E-05, -0.008492037, 0.6541179, -23.62010],
        [-1.240774E-05, 0.005162063, -0.8048342, 55.55996, -1443.338],
        [0.00000, -8.854164E-05, 0.03373254, -4.390837, 176.5294],
        [3.661771E-07, -2.154344E-04, 0.04809214, -4.884744, 172.3597],
        [1.906032E-08, -1.527799E-05, 0.004724294, -0.6992340, 20.50921],
        [1.199282E-09, -1.451051E-06, 6.910474E-04, -0.1736220, -5.321644],
        [1.140564E-10, -2.130756E-07, 1.570762E-04, -0.07029296, -12.89844],
        [8.105631E-12, -2.358417E-09, -2.635110E-06, -0.01562608, -20.02246],
        [-3.701195E-12, -8.608611E-09, 5.118829E-05, -0.06600998, -6.137674]]

    if altitude < zone[0]:
       altitude = zone[0]
    if altitude > zone[10]:
       altitude = zone[10]
    for i in range(10):
       if altitude > zone[i]:
          z = i
    z4 = math.pow(altitude/1000., 4)
    z3 = math.pow(altitude/1000., 3)
    z2 = math.pow(altitude/1000., 2)
    z  = altitude/1000.
    p = parameters[i][0]*z4 + parameters[i][1]*z3 + parameters[i][2]*z2 + parameters[i][3]*z + parameters[i][4]
    pressure = math.exp(p)
    # print (i, " A ", parameters[i][0],z4 , "B ", parameters[i][1], z3,  " C ", parameters[i][2], z2, 
    #   " D ", parameters[i][3], z, "E ", parameters[i][4])
    # print(" Pressure: ", pressure, " Altitude: ", altitude, " Zone: ", i)
    return pressure

class Earth:
    radius = 6378.e3 # Radius of the Earth in m
    atmosphericPressureGroundLevel = 1.0
    GM = 3.986004415e14
    x = 0.
    y = 0.
    z = 0.

class Projectile:
    count = 0

    def __init__ (self, objNum, objName, 
        objEpochDate, objEpochTime, 
        objDragCoeff, 
        objInclination, objRightAscension, 
        objSemiMajorAxis,
        objMeanAnomaly, objTrueAnomaly):

        self.objNum = objNum
        self.objName = objName
        self.objEpochDate = objEpochDate
        self.objEpochTime = objEpochTime
        self.objDragCoeff = objDragCoeff
        if objDragCoeff == 0 :
            self.objDragCoeff = 0.001
        self.objInclination = objInclination*DEG2RAD
        self.objRightAscension = objRightAscension*DEG2RAD
        self.objEccentricity = 0.0 # just handle circular orbits for now
        self.objArgumentofPerigee = 0.0 # just circular orbits
        self.objMeanAnomaly = objMeanAnomaly*DEG2RAD
        self.objTrueAnomaly = objTrueAnomaly
        self.objSemiMajorAxis = objSemiMajorAxis
        # self.objMeanMotion = objMeanMotion
        # self.objSemiMajorAxis = math.pow(objMeanMotion*Earth.GM, 0.33)
        self.objMeanMotion = math.sqrt(Earth.GM/math.pow(objSemiMajorAxis,3))
        print(" Mean Motion: ",self.objMeanMotion, (1./self.objMeanMotion))
        self.objSemiMinorAxis = self.objSemiMajorAxis*math.pow((1-(pow(self.objEccentricity,2.))), 0.5)
        print ("SemiMajor:", self.objSemiMajorAxis, (self.objSemiMajorAxis-Earth.radius))
        # print ("SemiMinor:", self.objSemiMinorAxis, self.objEccentricity)
        # print ("Drag Coeff: ", self.objDragCoeff)

        sma = self.objSemiMajorAxis
        ecc = self.objEccentricity
        incl = self.objInclination
        raan = self.objRightAscension
        argp = self.objArgumentofPerigee
        ta = self.objTrueAnomaly

        self.rotationMatrix = [
            [cos(raan)*cos(argp+ta)-sin(raan)*sin(argp+ta)*cos(incl),
             -cos(raan)*sin(argp+ta)-sin(raan)*cos(argp+ta)*cos(incl),
             sin(raan)*sin(incl)],
            [sin(raan)*cos(argp+ta)+cos(raan)*sin(argp+ta)*cos(incl),
             -sin(raan)*sin(argp+ta)+cos(raan)*cos(argp+ta)*cos(incl),
             -cos(raan)*sin(incl)],
            [sin(argp+ta)*sin(incl),
             cos(argp+ta)*sin(incl),
             cos(incl)]]
        # print (" Rotation Matrix ", self.rotationMatrix)

        Projectile.count += 1
        
    def propagate (self, propagationTime):
        self.time = propagationTime
        # Equations from https://en.wikipedia.org/wiki/Kepler%27s_laws_of_planetary_motion
        # compute Mean Anomanly
        
        # compute Eccentric Anomaly
        # compute True Anomaly
	# compute object x,y on ellipse
        # translate into ECI space
        theta = ((2*math.pi*self.time/self.objMeanMotion) + self.objTrueAnomaly) % 2*math.pi
        # just circular orbits for now
        tempx = self.objSemiMajorAxis*math.cos(theta)
        tempy = self.objSemiMajorAxis*math.sin(theta)
        tempz = 0.0

        self.x = (self.rotationMatrix[0][0]*tempx +
            self.rotationMatrix[0][1]*tempy +
            self.rotationMatrix[0][2]*tempz)
        self.y = (self.rotationMatrix[1][0]*tempx +
            self.rotationMatrix[1][1]*tempy +
            self.rotationMatrix[1][2]*tempz)
        self.z = (self.rotationMatrix[2][0]*tempx +
            self.rotationMatrix[2][1]*tempy +
            self.rotationMatrix[2][2]*tempz)

        # Approximate velocity from the semiMajor Axis and the mean motion
        self.velocity = self.objSemiMajorAxis*2*math.pi/self.objMeanMotion
        print (" x,y,z: ",self.x,self.y,self.z," velocity: ",self.velocity)
        
        return self

    def atmospheric_drag(self):
        # Initially make atmospheric drag a function of altitude with a simple model 
        # where pressure depends solely on altitude
        # - then, altitude with simple diurnal effect
        # - followed by relative velocity and pressure
        altitude = distance(self, Earth) - Earth.radius
        standAtmos = standard_atmosphere(altitude)
        # print(" Standard Atmosphere: ", standAtmos)
        # The drag coefficient is based on the objects aerodynamic cross section and mass
        # Drag is an acceleration applied opposite the velocity vector
        drag = pressure * self.objDragCoeff * self.velocity
        # print ("Drag: ", math.log10(drag), " Pressue: ", math.log10(pressure), " Velocity: ", math.log10(self.velocity))
        return drag
        
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
    objs.append(Projectile(i,"    ", 0., 0., 0., rand_PI(0.5), rand_PI(2),
                              Earth.radius+1e6+(300.*np.random.rand()), rand_PI(2), 0.))
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
