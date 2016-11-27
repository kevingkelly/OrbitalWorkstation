import math
import orbitalUtilities as utils
import Earth

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
        self.objInclination = objInclination*utils.DEG2RAD
        self.objRightAscension = objRightAscension*utils.DEG2RAD
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
