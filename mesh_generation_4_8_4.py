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
        def triangulate_tetrahedron(ps, sdfs, indices, ts, vs):
            for i in range(4):
                if sdfs[indices[i]] < 0 and sdfs[indices[(i + 1) % 4]] > 0 and sdfs[indices[(i + 2) % 4]] > 0 and sdfs[indices[(i + 3) % 4]] > 0:
                    ts += [[len(vs), len(vs)+1, len(vs)+2]]
                    vs += [ps[indices[(i + 1) % 4]], ps[indices[(i + 2) % 4]], ps[indices[(i + 3) % 4]]]
        def triangulate_octahedron(ps, sdfs, indices, ts, vs):
            if sum([1 for i in indices if sdf(ps[i]) > 0]) == 6: # no conflict
                return
            t8s = [[indices[0], indices[1], indices[2]],
                   [indices[0], indices[1], indices[3]],
                   [indices[1], indices[2], indices[4]],
                   [indices[2], indices[0], indices[5]],
                   [indices[3], indices[4], indices[1]],
                   [indices[4], indices[5], indices[2]],
                   [indices[5], indices[3], indices[0]],
                   [indices[5], indices[3], indices[4]]]
            for ti in t8s:
                if sdf(ps[ti[0]]) > 0 and sdf(ps[ti[1]]) > 0 and sdf(ps[ti[2]]) > 0:
                    ts += [[len(vs), len(vs)+1, len(vs)+2]]
                    vs += [ps[ti[0]], ps[ti[1]], ps[ti[2]]]
        triangulate_tetrahedron(ps, sdfs, [0, 1, 2, 3], ts, vs)
        triangulate_octahedron(ps, sdfs, [1, 2, 3, 4, 5, 6], ts, vs)
        triangulate_tetrahedron(ps, sdfs, [7, 6, 5, 4], ts, vs)

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

