from sympy import *

x1, y1, z1, x2, y2, z2, xi2, x3, y3, z3, yi3, x4, y4, z4, zi4 = symbols('x1 y1 z1 x2 y2 z2 xi2 x3 y3 z3 yi3 x4 y4 z4 zi4')

#d = (x2 + I*xi2 - x1)**2 + (y2 + I*yi2 - y1)**2 + (z2 + I*zi2 - y2)**2

d2 = (x2 + I*xi2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2
d3 = (x3 - x1)**2 + (y3 + I*yi3 - y1)**2 + (z3 - z1)**2
d4 = (x4 - x1)**2 + (y4 - y1)**2 + (z4 + I*zi4 - z1)**2

s = solve([d2, d3, d4], (xi2, yi3, zi4))
#s = solve([d2], (xi2))
print (s)
