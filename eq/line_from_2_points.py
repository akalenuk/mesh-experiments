from sympy import *

ax, ay, x1, y1, x2, y2 = symbols('ax ay x1 y1 x2 y2')

eqs = solve([
    ax*x1 + ay*y1 + 1,
    ax*x2 + ay*y2 + 1
    ], (ax, ay))

print (eqs)
