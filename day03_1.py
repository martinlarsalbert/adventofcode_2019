import pytest
import numpy as np

def get_direction(move):
    return move[0]

def do_move(x:int, y:int, move:str):

    direction = get_direction(move)
    step = int(move[1:])

    new_x = int(x)
    new_y = int(y)

    if direction=='R':
        new_x+=step
    elif direction=='L':
        new_x-=step
    elif direction=='U':
        new_y+=step
    elif direction=='D':
        new_y-=step
    else:
        raise ValueError('Unknown move:%s' % move)

    return new_x,new_y

class Line():

    def __init__(self,x1,y1,x2,y2):
        self.xs = [x1,x2]
        self.ys = [y1,y2]
        self.verify()

    def verify(self):
        pass

    def plot(self,ax,**kwargs):
        ax.plot(self.xs,self.ys,**kwargs)

class HorizontalLine(Line):

    def verify(self):
        if self.ys[0] != self.ys[1]:
            raise ValueError('Line verify error')


    def crosses(self,line:Line):
        """
        Does this horiozontal line cross other vertical line?

        y2'      x1'
                  !
        y1 x1-----x------x2
        y1'       !

        :param line: VerticalLine
        :return: True/False
        """

        if isinstance(line,HorizontalLine):
            return False  # Horizontal line cannot cross another horizontal line

        x_min = np.min(self.xs)
        x_max = np.max(self.xs)
        y_min = np.min(line.ys)
        y_max = np.max(line.ys)

        y = self.ys[0]
        x = line.xs[0]

        does_cross = ((x_max >= x) and (x_min <= x) and
                      (y >= y_min) and (y <= y_max)
                     )
        return does_cross

    def get_crossing_point(self, line:Line):
        x = line.xs[0]
        y = self.ys[0]
        return x,y



class VerticalLine(Line):

    def verify(self):
        if self.xs[0] != self.xs[1]:
            raise ValueError('Line verify error')


    def crosses(self,line:Line):
        """
        Does this vertical line cross other horizontal line?

        y2       x1
                  !
        y1' x1'---x------x2'
        y1        !

        :param line: VerticalLine
        :return: True/False
        """

        if isinstance(line,VerticalLine):
            return False  # VerticalLine line cannot cross another VerticalLine

        x_min = np.min(line.xs)
        x_max = np.max(line.xs)
        y_min = np.min(self.ys)
        y_max = np.max(self.ys)

        y = line.ys[0]
        x = self.xs[0]

        does_cross = ((x_max >= x) and (x_min <= x) and
                      (y >= y_min) and (y <= y_max)
                     )
        return does_cross

    def get_crossing_point(self, line:Line):
        x = self.xs[0]
        y = line.ys[0]
        return x,y


def record_moves(moves:list):

    x = 0
    y = 0

    xs = [x]
    ys = [y]

    lines = []

    for move in moves:
        old_x = x
        old_y = y
        x,y = do_move(x,y,move)
        xs.append(x)
        ys.append(y)

        if x==old_x:
            LineClass = VerticalLine
        else:
            LineClass = HorizontalLine

        line = LineClass(x1=old_x, y1=old_y, x2=x, y2=y)

        lines.append(line)

    return lines

def calculate_manhattan_distance(x,y):
    return abs(x)+abs(y)

def get_intersections(lines1,lines2):

    xs = []
    ys = []

    for line1 in lines1:
        assert isinstance(line1,Line)

        for line2 in lines2:
            assert isinstance(line2,Line)

            if line1.crosses(line2):
                x,y = line1.get_crossing_point(line2)

                if not((x==0) and (y==0)):
                    xs.append(x)
                    ys.append(y)

    return xs,ys

def run(moves1_str:str, moves2_str:str):

    moves1 = moves1_str.split(',')
    moves2 = moves2_str.split(',')
    lines1 = record_moves(moves=moves1)
    lines2 = record_moves(moves=moves2)

    xs,ys = get_intersections(lines1=lines1, lines2=lines2)

    smallest_distance = None
    for x,y in zip(xs,ys):
        distance = calculate_manhattan_distance(x=x, y=y)

        if smallest_distance is None:
            smallest_distance=distance
        else:
            if distance<smallest_distance:
                smallest_distance=distance

    return smallest_distance


if __name__ == '__main__':

    with open('day03_input.txt') as file:
        lines = file.readlines()

    moves1_str = lines[0].replace('\n', '')
    moves2_str = lines[1].replace('\n', '')

    manhattan_distance = run(moves1_str=moves1_str,moves2_str=moves2_str)
    print('Line1:%s' % moves1_str)
    print('Line2:%s' % moves2_str)
    print('Manhattan distance:%i' % manhattan_distance)


### Tests #################################
def test_record_moves():
    moves = [
        'R10',
        'R2',
        'L2',
        'U10',
        'D2',
    ]

    lines = record_moves(moves)

    line = lines[0]
    assert isinstance(line,HorizontalLine)
    assert line.xs == [0,10]
    assert line.ys == [0, 0]

    line = lines[1]
    assert isinstance(line, HorizontalLine)
    assert line.xs == [10,12]
    assert line.ys == [0, 0]

    line = lines[2]
    assert isinstance(line, HorizontalLine)
    assert line.xs == [12,10]
    assert line.ys == [0, 0]

    line = lines[-1]
    assert isinstance(line, VerticalLine)
    assert line.xs == [10,10]
    assert line.ys == [10, 8]

def test_line_verify():

    line = HorizontalLine(1, 0, 2, 0)
    with pytest.raises(ValueError):
        line = HorizontalLine(1, 2, 0, 1)


def test_crosses_horizontal_horizontal():

    line1 = HorizontalLine(1,0,2,0)
    line2 = HorizontalLine(1,1,2,1)
    assert not line1.crosses(line2)
    assert not line2.crosses(line1)

def test_crosses_vertical_vertical():

    line1 = VerticalLine(1,1,1,2)
    line2 = VerticalLine(2,2,2,3)
    assert not line1.crosses(line2)
    assert not line2.crosses(line1)

def test_crosses_horizontal_vertical():

    line1 = HorizontalLine(1,2,3,2)
    line2 = VerticalLine(2,1,2,3)
    assert line1.crosses(line2)

    line1 = HorizontalLine(2,2,1,2)
    line2 = VerticalLine(2,1,2,3)
    assert line1.crosses(line2)

    line1 = HorizontalLine(1,2,3,2)
    line2 = VerticalLine(2,-1,2,3)
    assert line1.crosses(line2)

    line1 = HorizontalLine(1, 2, 3, 2)
    line2 = VerticalLine(3, 1, 3, 3)
    assert line1.crosses(line2)

    line1 = HorizontalLine(1, 2, 3, 2)
    line2 = VerticalLine(4, 1, 4, 3)
    assert not line1.crosses(line2)

    line1 = HorizontalLine(1, 4, 3, 4)
    line2 = VerticalLine(3, 1, 3, 3)
    assert not line1.crosses(line2)

def test_crosses_vertical_horizontal():

    line2 = HorizontalLine(1,2,3,2)
    line1 = VerticalLine(2,1,2,3)
    assert line1.crosses(line2)

    line2 = HorizontalLine(1,2,3,2)
    line1 = VerticalLine(2,3,2,1)
    assert line1.crosses(line2)

    line1 = HorizontalLine(1, 2, 3, 2)
    line2 = VerticalLine(3, 1, 3, 3)
    assert line1.crosses(line2)

    line1 = HorizontalLine(1, 2, 3, 2)
    line2 = VerticalLine(4, 1, 4, 3)
    assert not line1.crosses(line2)

    line1 = HorizontalLine(1, 4, 3, 4)
    line2 = VerticalLine(3, 1, 3, 3)
    assert not line1.crosses(line2)

def test_get_crossing_point():

    line1 = HorizontalLine(1,2,3,2)
    line2 = VerticalLine(3,1,3,3)
    x,y = line1.get_crossing_point(line2)
    assert x == 3
    assert y == 2

def test_get_crossing_point2():

    line2 = HorizontalLine(1,2,3,2)
    line1 = VerticalLine(3,1,3,3)
    x,y = line1.get_crossing_point(line2)
    assert x == 3
    assert y == 2

def test_get_intersections():

    lines1 = [
        HorizontalLine(1, 2, 3, 2),
        HorizontalLine(1, 3, 3, 3),

        ]

    lines2 = [
        VerticalLine(3, 1, 3, 3),
        ]

    xs,ys = get_intersections(lines1=lines1, lines2=lines2)
    assert xs == [3,3]
    assert ys == [2,3]

def test_run():

    assert run('R75,D30,R83,U83,L12,D49,R71,U7,L72',
        'U62,R66,U55,R34,D71,R55,D58,R83') == 159

    assert run('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
        'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 135





