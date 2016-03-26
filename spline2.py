import oneliners

polyline = [(0.,0.), (1.,1.), (2.,2.), (3.,2.), (4.,1.), (5.,0.)]
MAX_AXIS_DIFF = 0.5

def spline2(d1, p1, p2):
	return [(p1[i], d1[i], p2[i] - p1[i] - d1[i]) for i in range(2)]

def pol2(p, t):
	return p[2]*t*t + p[1]*t + p[0]

def spline2_point(s, t):
	return (pol2(s[0], t), pol2(s[1], t))

def pol2_d(p, t):
	return 2*p[2]*t + p[1]

def spline2_d(s, t):
	return (pol2_d(s[0], t), pol2_d(s[1], t))

def evaluate_pol2(p, xs):
	for i in range(1, len(xs)-1):
		t = float(i) / (len(xs)-1)
		if abs(pol2(p, t) - xs[i]) > MAX_AXIS_DIFF:
			return False
	return True 

def evaluate_spline2(s, pts):
	return sum([evaluate_pol2(s[i], [pt[i] for pt in pts]) for i in range(2)])

def approximate(d1, points):
	if len(points) <= 1:
		return points
	for i in range(len(points)-1, 0, -1):
		spline = spline2(d1, points[0], points[i])
		if evaluate_spline2(spline, points[:i+1]):
			new_points = [spline2_point(spline, float(j) / i) for j in range(i)]
			new_d = oneliners.normalized(spline2_d(spline, 1.))
			return new_points + approximate(new_d, points[i:])	
	

print approximate((0., 0.), polyline)
