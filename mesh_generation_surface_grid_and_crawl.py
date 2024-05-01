import time
import obj_io
from oneliners import *


def triangulate(bbox_min, bbox_max, cube_size, distance_in_point):
    vs = []
    ts = []
    
    # 1. create square walls
    for z in float_range(bbox_min[2], bbox_max[2], cube_size):
      #print(z)
      for y in float_range(bbox_min[1], bbox_max[1], cube_size):
        for x in float_range(bbox_min[0], bbox_max[0], cube_size):
          # detect border, create walls
          cube_center = (x + cube_size / 2., y + cube_size / 2., z + cube_size / 2.)
          neighbor100 = (x - cube_size / 2., y + cube_size / 2., z + cube_size / 2.)
          neighbor010 = (x + cube_size / 2., y - cube_size / 2., z + cube_size / 2.)
          neighbor001 = (x + cube_size / 2., y + cube_size / 2., z - cube_size / 2.)
          d = distance_in_point(cube_center)
          d100 = distance_in_point(neighbor100)
          d010 = distance_in_point(neighbor010)
          d001 = distance_in_point(neighbor001)

          # x-wall
          if d * d100 < 0:
            start_index = len(vs)
            vs+=[(x, y, z)]
            vs+=[(x, y + cube_size, z)]
            vs+=[(x, y + cube_size, z + cube_size)]
            vs+=[(x, y, z + cube_size)]
            if (d > d100):
              ts+=[(start_index, start_index + 1, start_index + 2)]
              ts+=[(start_index, start_index + 2, start_index + 3)]
            else:
              ts+=[(start_index, start_index + 2, start_index + 1)]
              ts+=[(start_index, start_index + 3, start_index + 2)]

          # y-wall
          if d * d010 < 0:
            start_index = len(vs)
            vs+=[(x, y, z)]
            vs+=[(x + cube_size, y, z)]
            vs+=[(x + cube_size, y, z + cube_size)]
            vs+=[(x, y, z + cube_size)]
            if (d < d010):
              ts+=[(start_index, start_index + 1, start_index + 2)]
              ts+=[(start_index, start_index + 2, start_index + 3)]
            else:
              ts+=[(start_index, start_index + 2, start_index + 1)]
              ts+=[(start_index, start_index + 3, start_index + 2)]
            
          # z-wall
          if d * d001 < 0:
            start_index = len(vs)
            vs+=[(x, y, z)]
            vs+=[(x + cube_size, y, z)]
            vs+=[(x + cube_size, y + cube_size, z)]
            vs+=[(x, y + cube_size, z)]
            if (d > d001):
              ts+=[(start_index, start_index + 1, start_index + 2)]
              ts+=[(start_index, start_index + 2, start_index + 3)]
            else:
              ts+=[(start_index, start_index + 2, start_index + 1)]
              ts+=[(start_index, start_index + 3, start_index + 2)]
              
    # 2 crawl the vertices closer to the SDF
    for j in range(4):
        for i in range(len(vs)):
            #print(i, len(vs))
            new_vsi = sum_of(vs[i], [cube_size / 4., 0., 0.])
            if abs(distance_in_point(new_vsi)) < abs(distance_in_point(vs[i])):
                vs[i] = new_vsi
            new_vsi = sum_of(vs[i], [0., cube_size / 4., 0.])
            if abs(distance_in_point(new_vsi)) < abs(distance_in_point(vs[i])):
                vs[i] = new_vsi
            new_vsi = sum_of(vs[i], [0., 0., cube_size / 4.])
            if abs(distance_in_point(new_vsi)) < abs(distance_in_point(vs[i])):
                vs[i] = new_vsi
            new_vsi = sum_of(vs[i], [-cube_size / 4., 0., 0.])
            if abs(distance_in_point(new_vsi)) < abs(distance_in_point(vs[i])):
                vs[i] = new_vsi
            new_vsi = sum_of(vs[i], [0., -cube_size / 4., 0.])
            if abs(distance_in_point(new_vsi)) < abs(distance_in_point(vs[i])):
                vs[i] = new_vsi
            new_vsi = sum_of(vs[i], [0., 0., -cube_size / 4.])
            if abs(distance_in_point(new_vsi)) < abs(distance_in_point(vs[i])):
                vs[i] = new_vsi
    return (vs, ts)

 
if __name__ == "__main__":
    OUTPUT = 'ppout.obj'
    SDF = lambda xyz : (xyz[0]**2 + xyz[1]**2 + xyz[2]**2) ** 0.5 - 0.5    # spere 0-0.5
    
    (vs, ts) = triangulate([-0.6, -0.6, -0.6], [+0.6, +0.6, +0.6], 0.1, SDF)

    print ("triangles: " + str(len(ts)) + "   vertices: " + str(len(vs)))

    f = open(OUTPUT, 'w')
    f.write(obj_io.str_from_vertexes(vs))
    f.write('\n')
    f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in ts]))
    f.close()

