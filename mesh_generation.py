import time
import obj_io
from oneliners import *

OUTPUT = 'ppout.obj'
SDF = lambda xyz : (xyz[0]**2 + xyz[1]**2 + xyz[2]**2) ** 0.5 -1    # spere 0-1
R3 = 97./56.

# three axes
a1 = [R3, 0.5, 0]
a2 = [R3, -0.5, 0]
a3 = [0.5, 0, R3]



if __name__ == "__main__":

    f = open(OUTPUT, 'w')
    f.write(obj_io.str_from_vertexes(vertexes))
    f.write('\n')
    f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in triangles]))
    f.close()

