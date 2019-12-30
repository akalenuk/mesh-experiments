import time
import obj_io
from oneliners import *

OUTPUT = 'ppout.obj'
SDF = lambda xyz : (xyz[0]**2 + xyz[1]**2 + xyz[2]**2) ** 0.5 - 1.    # spere 0-1
R3 = 3**0.5

def grad(f, xyz):
    EPS = 1.e-5;
    return [(f(sum_of(xyz, [EPS, 0., 0.])) - f(xyz)) / EPS,
            (f(sum_of(xyz, [0., EPS, 0.])) - f(xyz)) / EPS,
            (f(sum_of(xyz, [0., 0., EPS])) - f(xyz)) / EPS]

def snap(f, xyz):
    return sum_of(xyz, scaled(normalized(grad(f, xyz)), -f(xyz)))

def add_tri(f, a, p1, p2, p0, i1, i2, vs, ts, it):
    if it == 3: # exploratory
        return
    old_norm = normalized(cross_of(sub_of(p0, p1), sub_of(p2, p1)))
    new_point_dir = normalized(cross_of(old_norm, sub_of(p2, p1)))
    new_point = sum_of(scaled(sum_of(p1, p2), 0.5), scaled(new_point_dir, a))
    new_snapped_point = snap(f, new_point)
    
    d1 = distance_between(new_snapped_point, p1)
    d2 = distance_between(new_snapped_point, p2)
    
    for i in range(len(vs)):
        if distance_between(vs[i], new_snapped_point) < min(d1, d2):
            return
 
    new_point_i = len(vs)
    vs += [new_snapped_point]
    ts += [[i1, i2, new_point_i]]
    
    add_tri(f, a, p1, new_snapped_point, p2, i1, new_point_i, vs, ts, it+1)
    add_tri(f, a, new_snapped_point, p2, p1, new_point_i, i2, vs, ts, it+1)


if __name__ == "__main__":
    vs = []
    ts = []
    a = 0.2

    first_tri_ps = [snap(SDF, [0., 0., 1.]), snap(SDF, [0., 0.1, 1.]), snap(SDF, [0.1, 0., 1.])]
    vs += [snap(SDF, [0., 0., 1.]), snap(SDF, [0., a, 1.])]

    add_tri(SDF, a, vs[0], vs[1],  snap(SDF, [a, 0., 1.]), 0, 1, vs, ts, 0)
    
    print ("triangles: " + str(len(ts)) + "   vertices: " + str(len(vs)))

    f = open(OUTPUT, 'w')
    f.write(obj_io.str_from_vertexes(vs))
    f.write('\n')
    f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in ts]))
    f.close()

