import math
import random
import Earth
import Projectile as prj

def createConstellation (constellationName, altitude, inclination, numPlanes,
                         numObjectsPerPlane, startingRightAscension):

    totalObjects = numPlanes * numObjectsPerPlane
    deltaLongitude = 2.0*math.pi/numPlanes
    deltaAnomaly = 2.0*math.pi/numObjectsPerPlane
    print ("Create constellation: ",totalObjects, deltaLongitude, deltaAnomaly)
    constellation = []
    for plane in range(numPlanes):
        rightAscension = startingRightAscension + plane*deltaLongitude
        startingAnomaly = random.uniform(0, 2*math.pi)
        for objNum in range(numObjectsPerPlane):
            objectName = constellationName + "_" + str(plane) + "_" + str(objNum)
            inclination = inclination
            rightAscension = rightAscension
            semiMajorAxis = altitude*1000 + Earth.radius
            anomaly = startingAnomaly + objNum*deltaAnomaly
            x = prj.Projectile(0, objectName, 0, 0, 0,
                           inclination, rightAscension, altitude,
                           anomaly, anomaly)
            print ("X ",plane,":", objNum," ", x)
            constellation.append(x)

    # print (constellation)
    return constellation
    
    
    
createConstellation("Iridium", 600, 0.25, 3, 3, 0)
