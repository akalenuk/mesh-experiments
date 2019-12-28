import time
import obj_io
from oneliners import *

OUTPUT = 'ppout.obj'
SDF = lambda xyz : (xyz[0]**2 + xyz[1]**2 + xyz[2]**2) ** 0.5 - 1.    # spere 0-1
R3 = 97./56.

# three axes
a1 = [R3, 1., 0]
a2 = [R3, -1., 0]
a3 = [1., 0, R3]

def triangulate(sdf, p0, scale, subdivisions, ts, vs):
    if subdivisions > 0:
        # subdivide
        p1 = sum_of(p0, scaled(a1, scale / 2.))
        p2 = sum_of(p0, scaled(a2, scale / 2.))
        p3 = sum_of(p0, scaled(a3, scale / 2.))
        p12 = sum_of(sum_of(p0, scaled(a1, scale / 2.)), scaled(a2, scale / 2.))
        p23 = sum_of(sum_of(p0, scaled(a2, scale / 2.)), scaled(a3, scale / 2.))
        p31 = sum_of(sum_of(p0, scaled(a3, scale / 2.)), scaled(a1, scale / 2.))
        p123 = sum_of(sum_of(p0, scaled(a1, scale / 2.)), sum_of(scaled(a2, scale / 2.), scaled(a3, scale / 2.)))
        ps = [p0, p1, p2, p3, p12, p23, p31, p123]
        for p in ps:
            triangulate(sdf, p, scale / 2., subdivisions - 1, ts, vs)
    else:
        # triangulate
        p1 = sum_of(p0, scaled(a1, scale))
        p2 = sum_of(p0, scaled(a2, scale))
        p3 = sum_of(p0, scaled(a3, scale))
        p12 = sum_of(sum_of(p0, scaled(a1, scale)), scaled(a2, scale))
        p23 = sum_of(sum_of(p0, scaled(a2, scale)), scaled(a3, scale))
        p31 = sum_of(sum_of(p0, scaled(a3, scale)), scaled(a1, scale))
        p123 = sum_of(sum_of(p0, scaled(a1, scale)), sum_of(scaled(a2, scale), scaled(a3, scale)))
        ps = [p0, p1, p2, p3, p12, p23, p31, p123]
        sdfs = [sdf(p) for p in ps]
        if sum([1 for f in sdfs if f > 0]) == 8: # no conflict
            return
        tis = [[0, 1, 2], [0, 2, 3], [0, 3, 1], 
               [1, 2, 4], [2, 3, 5], [3, 1, 6],
               [1, 4, 6], [2, 5, 4], [3, 6, 5],
               [7, 6, 5], [7, 5, 4], [7, 4, 6]]
        for ti in tis:
            if sdf(ps[ti[0]]) > 0 and sdf(ps[ti[1]]) > 0 and sdf(ps[ti[2]]) > 0:
                ts += [[len(vs), len(vs)+1, len(vs)+2]]
                vs += [ps[ti[0]], ps[ti[1]], ps[ti[2]]]

if __name__ == "__main__":
    vs = []
    ts = []
    triangulate(SDF, [-3*R3/2., 0, -R3/2.], 2, 4, ts, vs)
    print ("triangles: " + str(len(ts)) + "   vertices: " + str(len(vs)))

    f = open(OUTPUT, 'w')
    f.write(obj_io.str_from_vertexes(vs))
    f.write('\n')
    f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in ts]))
    f.close()

