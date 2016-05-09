from oneliners import *
from types import *
from random import randint

def v__E(a):
    ''' Levi-Civita symbol '''
    n=0
    t=[]
    for ti in a:
        t.append(ti)
    for i in xrange(0,len(a)):
        for j in xrange(0,len(a)-i-1):
            if t[j]==t[j+1]:
                return 0
            elif t[j]>t[j+1]:
                n+=1
                t.insert(j+1,t.pop(j))
    if n%2==0:return 1
    return -1


def v_cross(A):
    ''' n-dimensional cross product on (n-1) vectors in list A '''
    for a in A:
        assert len(a) == len(A[0]), "Vector size mismatch in 'v_cross'"
    DIMM=len(A[0])
    N=len(A)
    assert N == DIMM-1, "Vector number mismatch in 'v_cross'"

    v_res=[]
    for i in xrange(0,DIMM):
        v_res.append(0.0)
        for jk in xrange(0,DIMM**N):
            v_ijk=[i]
            for j in xrange(0,N):
                v_ijk.append((jk/(DIMM**(N-j-1)))%DIMM)
            t_res=v__E(v_ijk)
            if t_res!=0:
                for k in xrange(0,N):
                    t_res*=A[k][v_ijk[k+1]]
                v_res[i]+=t_res
    return v_res

def point_on_plane(n, d):
	return [-d/n[0]] + [0]*(len(n)-1)

def project_by_vector(point, projection_vector, plane_n, plane_d):
	assert type(point) is ListType
	assert type(projection_vector) is ListType
	assert type(plane_n) is ListType
	assert type(plane_d) is FloatType 
	ponp = point_on_plane(plane_n, plane_d)
	k = dot_of(vector(point, ponp), plane_n) / dot_of(projection_vector, plane_n)
	return sum_of(point, scaled(projection_vector, k))

def exp_solution_for(A, B):
	p = [0. for each in B]
	for i in range(len(A)):
		plane_n = A[i]
		plane_d = -B[i]
		other_planes_ns = A[:i] + A[i+1:]
		projection_vector = v_cross(other_planes_ns)
		p = project_by_vector(p, projection_vector, plane_n, plane_d)
	return p



def Validate(A, B, X, eps = 0.0001):
	ret = []
	for i in range(len(B)):
		Bi = 0.0
		for j in range(len(B)):
			Bi += A[i][j] * X[j]
		if abs(Bi - B[i]) > eps:
			return False
	return True

if __name__ == '__main__':
	plane_n = [2., 3., 1.]
	plane_d = 4.
	point = point_on_plane(plane_n, plane_d)
	print 'Point on plane equation fit:', dot_of(plane_n, point) + plane_d
	point_to_project = [1., 1., 2.]
	projection_vector = [2., 1., 0.]
	projected_point = project_by_vector(point_to_project, projection_vector, plane_n, plane_d)	
	print 'Projected point equation fit:', dot_of(plane_n, projected_point) + plane_d
	
	dimm = 5
	for n in range(0, 100):
		A = [[] for each in range(dimm)]
		B = []
		for i in range(0, dimm):
			A += []
			for j in range(0, dimm):
				A[i] += [randint(-100, 100) / 100.0]
			B += [randint(-100, 100) / 100.0]
	
		try:
			X = exp_solution_for(A, B)
			print Validate(A, B, X)
		except ZeroDivisionError:
			print 'No'	