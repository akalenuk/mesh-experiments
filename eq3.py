from sympy import *

x1, y1, z1, x2, y2, z2, x3, y3, z3, a, b, c = symbols('x1 y1 z1 x2 y2 z2 x3 y3 z3 a b c')
x,y,z = symbols('x y z')

r = solve([a*x1 + b*x2 + c*x3 - x, a*y1 + b*y2 + c*y3 - y, a*z1 + b*z2 + c*z3 - z], (a, b, c))

print(r)
