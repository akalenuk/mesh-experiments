from sympy import *

a, b, c, ai, bi, ci  = symbols('a b c ai bi ci')
x1, y1, z1, xi1, yi1, zi1 = symbols('x1 y1 z1 xi1 yi1 zi1')
x2, y2, z2, xi2, yi2, zi2 = symbols('x2 y2 z2 xi2 yi2 zi2')
x3, y3, z3, xi3, yi3, zi3 = symbols('x3 y3 z3 xi3 yi3 zi3')


if False:
	p1 = expand((a + I*ai)*(x1 + I*xi1) + (b + I*bi)*(y1 + I*yi1) + (c + I*ci)*(z1 + I*zi1) + 1)
	p2 = expand((a + I*ai)*(x2 + I*xi2) + (b + I*bi)*(y2 + I*yi2) + (c + I*ci)*(z2 + I*zi2) + 1)
	p3 = expand((a + I*ai)*(x3 + I*xi3) + (b + I*bi)*(y3 + I*yi3) + (c + I*ci)*(z3 + I*zi3) + 1)
	print(collect(p1, I))
	print(collect(p2, I))
	print(collect(p3, I))
	#a*x1 - ai*xi1 + b*y1 - bi*yi1 + c*z1 - ci*zi1 + 1 + I*(a*xi1 + ai*x1 + b*yi1 + bi*y1 + c*zi1 + ci*z1)
	#a*x2 - ai*xi2 + b*y2 - bi*yi2 + c*z2 - ci*zi2 + 1 + I*(a*xi2 + ai*x2 + b*yi2 + bi*y2 + c*zi2 + ci*z2)
	#a*x3 - ai*xi3 + b*y3 - bi*yi3 + c*z3 - ci*zi3 + 1 + I*(a*xi3 + ai*x3 + b*yi3 + bi*y3 + c*zi3 + ci*z3)

if False:
	plane = solve([
	a*x1 - ai*xi1 + b*y1 - bi*yi1 + c*z1 - ci*zi1 + 1,
	a*x2 - ai*xi2 + b*y2 - bi*yi2 + c*z2 - ci*zi2 + 1,
	a*x3 - ai*xi3 + b*y3 - bi*yi3 + c*z3 - ci*zi3 + 1,
	(a*xi1 + ai*x1 + b*yi1 + bi*y1 + c*zi1 + ci*z1),
	(a*xi2 + ai*x2 + b*yi2 + bi*y2 + c*zi2 + ci*z2),
	(a*xi3 + ai*x3 + b*yi3 + bi*y3 + c*zi3 + ci*z3)]
		,(a, b, c, ai, bi, ci), check=False, simplify=False)

# these two are equivalent
#print(linsolve((Matrix([[x1, y1], [x2, y2]]), Matrix([[0], [1]]))))
#print(solve([a*x1+b*y1,a*x2+b*y2-1], (a,b)))

if False:
	A = Matrix([
	[x1, - xi1,  y1, -yi1, z1, -zi1],
	[x2, - xi2,  y2, -yi2, z2, -zi2],
	[x3, - xi3,  y3, -yi3, z3, -zi3],
	[xi1,  x1,  yi1, y1, zi1, z1],
	[xi2,  x2,  yi2, y2, zi2, z2],
	[xi3,  x3,  yi3, y3, zi3, z3]
	])
	B = Matrix([
	[-1],
	[-1],
	[-1],
	[0],
	[0],
	[0]
	])
	plane = linsolve((A, B))
	
if True:
	A = Matrix([
	[x1, - xi1,  y1, -yi1, z1, -zi1, 1],
	[x2, - xi2,  y2, -yi2, z2, -zi2, 1],
	[x3, - xi3,  y3, -yi3, z3, -zi3, 1],
	[xi1,  x1,  yi1, y1, zi1, z1, 0],
	[xi2,  x2,  yi2, y2, zi2, z2, 0],
	[xi3,  x3,  yi3, y3, zi3, z3, 0]
	])
	plane = solve_linear_system_LU(A, (a, ai, b, bi, c, ci))

a = plane[a]
print(simplify(a))




# I stopped this after a few hours
#plane = solve([
#(a + I*ai)*(x1 + I*xi1) + (b + I*bi)*(y1 + I*yi1) + (c + I*ci)*(z1 + I*zi1) + 1,
#(a + I*ai)*(x2 + I*xi2) + (b + I*bi)*(y2 + I*yi2) + (c + I*ci)*(z2 + I*zi2) + 1,
#(a + I*ai)*(x3 + I*xi3) + (b + I*bi)*(y3 + I*yi3) + (c + I*ci)*(z3 + I*zi3) + 1], (a, b, c, ai, bi, ci))
#
#print(plane)

