import numpy as np
from day03_1 import Line,record_moves

def get_intersection_distances(lines1,lines2):
    """
    Find the first intersection from line1 to line2
    Return the distance along line1 to this point
    :param lines1:
    :param lines2:
    :return:
    """

    xs = []
    ys = []

    distance_line1 = 0
    found_distances_line1 = []
    found_distances_line2 = []

    for line1 in lines1:
        assert isinstance(line1,Line)

        distance_line2 = 0
        for line2 in lines2:
            assert isinstance(line2,Line)

            found = False
            if line1.crosses(line2):
                x,y = line1.get_crossing_point(line2)

                if not((x==0) and (y==0)):
                    # Found!
                    found = True

            if found:

                xs.append(x)
                ys.append(y)

                found_distance_line1 = distance_line1 + line1.get_crossing_length(line2)
                found_distance_line2 = distance_line2 + line2.get_crossing_length(line1)
                found_distances_line1.append(found_distance_line1)
                found_distances_line2.append(found_distance_line2)


            distance_line2+=line2.length

        distance_line1 += line1.length

    return xs,ys,np.array(found_distances_line1),np.array(found_distances_line2)



def run(moves1_str:str, moves2_str:str):

    moves1 = moves1_str.split(',')
    moves2 = moves2_str.split(',')
    lines1 = record_moves(moves=moves1)
    lines2 = record_moves(moves=moves2)

    xs, ys, found_distances_line1, found_distances_line2 = get_intersection_distances(lines1=lines1, lines2=lines2)

    total_distances = found_distances_line1 + found_distances_line2
    index = np.argmin(total_distances)
    smallest_distance = total_distances[index]
    x = xs[index]
    y = ys[index]

    return smallest_distance,x,y

if __name__ == '__main__':

    with open('day03_input.txt') as file:
        lines = file.readlines()

    moves1_str = lines[0].replace('\n', '')
    moves2_str = lines[1].replace('\n', '')

    smallest_distance, x, y = run(moves1_str=moves1_str,moves2_str=moves2_str)
    print('Line1:%s' % moves1_str)
    print('Line2:%s' % moves2_str)
    print('Smallest distance:%i' % smallest_distance)

### Tests ####

def test_run():

    smallest_distance, x, y = run('R75,D30,R83,U83,L12,D49,R71,U7,L72',
                                    'U62,R66,U55,R34,D71,R55,D58,R83')
    assert smallest_distance == 610

    smallest_distance, x, y = run('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
        'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
    assert smallest_distance == 410