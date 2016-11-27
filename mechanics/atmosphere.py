import math

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
