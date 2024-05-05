from sympy import *

x1, y1, z1, x2, y2, z2, xi2, yi2, x3, y3, z3, yi3, zi3, x4, y4, z4, zi4, xi4 = symbols('x1 y1 z1 x2 y2 z2 xi2 yi2 x3 y3 z3 yi3 zi3 x4 y4 z4 zi4 xi4', real = True)

d2 = (x2 + I*xi2 - x1)**2 + (y2 + I*yi2 - y1)**2 + (z2 - z1)**2
d3 = (x3 - x1)**2 + (y3 + I*yi3 - y1)**2 + (z3 + I*zi3 - z1)**2
d4 = (x4 + I*xi4 - x1)**2 + (y4 - y1)**2 + (z4 + I*zi4 - z1)**2

s2 = solve([d2], (xi2, yi2))
print ('xi2 = ', s2[0][0])
print ('yi2 = ', s2[0][1])

s3 = solve([d3], (yi3, zi3))
print ('yi3 = ', s3[0][0])
print ('zi3 = ', s3[0][1])

s4 = solve([d4], (zi4, xi4))
print ('zi4 = ', s4[0][0])
print ('xi4 = ', s4[0][1])


