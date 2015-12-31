def scale(A, x):
	return [ai*x for ai in A]

def add(A, B):
	return [ai+bi for (ai, bi) in zip(A, B)]

def dot(A, B):
	return sum([ai*bi for (ai, bi) in zip(A, B)])

def length(A):
	return pow(dot(A, A), 0.5)

def normalize(A):
	return scale(A, 1.0 / length(A))

def ident(n):
	return [[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]

def transpose(A):
	return [list(aj) for aj in zip(*A)]

def mul(A, X):
	return [dot(ai, X) for ai in A]

def vector(P1, P2):
	return add(scale(P1, -1.), P2)

def project(A, Pn, Pd):
	return add(A, scale(Pn, (Pd - dot(Pn, A)) / dot(Pn, Pn)))

def distance(A, B):
	return pow(dot( *(vector(A, B), )*2 ), 0.5)

def solve(A, B, Xi):
	return Xi if distance(mul(A, Xi), B) < 0.0001 else solve(A[1:] + [A[0]], B[1:] + [B[0]], project(Xi, A[0], B[0]))

def invert(A):
	return transpose([solve(A, ort, [0.0]*len(A)) for ort in ident(len(A))])

def centroid(Ps):
	return [sum(xi) / len(Ps) for xi in transpose(Ps)]

if __name__ == "__main__":
	A = [[0.78, -0.42, 0.59], [0.95, 0.31, 0.26], [-0.44, -0.1, -0.38]]
	B = [1.0, 2.0, 3.0]
	print 'A, B:', A, B
	X = solve(A, B, [0.0]*3)
	err = distance(mul(A, X), B)
	print 'X, error:', X, err
	Ai = invert(A)
	print 'A^-1:', Ai
	Aii = invert(Ai)
	print '(A^-1)^-1:',Aii
	print B
	X = mul(Ai, B)
	err = distance(mul(A, X), B)
	print 'Ai*B, error:', X, err
	points = [[1., 2., 3.], [2., 4., 6.], [3., 6., 9.]]
	print 'Centroid of', points, '=', centroid(points)
