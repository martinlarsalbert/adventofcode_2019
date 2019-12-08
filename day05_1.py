

def get_positions(raw_code:str)->list:
    positions_str = raw_code.split(',')
    positions = [int(position) for position in positions_str]
    return positions

def get_opcode(positions:list,i:int):

    item = str(positions[i])
    assert len(item) == 4
    opcode = int(item[-2:])

    return opcode


class Operation():

    number_of_arguments = 2
    opcode = None

    def __init__(self,positions, header:int, i:int,verify=True):
        self.positions = positions
        self.header = header
        self.i=i
        if verify:
            opcode = get_opcode(positions=self.positions, i=self.i)
            assert opcode == self.opcode

        self.function_return_destination = self.positions[i+self.number_of_arguments+1]
        self.get_modes()
        self.get_arguments()


    def get_modes(self):
        header = str(self.header).zfill(self.number_of_arguments+3)
        self.modes = []
        for mode_str in header[::-1][2:]:  # Reversed string
            self.modes.append(int(mode_str))

    def get_arguments(self):
        i=self.i
        raw_arguments = self.positions[i + 1:i + self.number_of_arguments + 1]
        assert len(raw_arguments) < len(self.modes)
        modes = self.modes[0:len(raw_arguments)]

        self.arguments = []
        for raw_argument,mode in zip(raw_arguments,modes):
            if mode == 0:
                # Position mode:
                argument = self.positions[raw_argument]
            elif mode == 1:
                # immediate mode
                argument = raw_argument
            else:
                raise ValueError('Unknown mode:%i' % i)

            self.arguments.append(argument)


    def pass_result(self,result):
        self.positions[self.function_return_destination] = result

class Add(Operation):

    number_of_arguments = 2
    opcode = 1

    def run(self):
        result = self.arguments[0] + self.arguments[1]
        self.pass_result(result=result)

class Multiply(Operation):

    number_of_arguments = 2
    opcode = 2

    def run(self):
        result = self.arguments[0] * self.arguments[1]
        self.pass_result(result=result)

class Input(Operation):

    number_of_arguments = 1
    opcode = 3

    def run(self):
        result = self.arguments[0]
        self.pass_result(result=result)

class Output(Operation):

    number_of_arguments = 1
    opcode = 4

    def run(self):
        result = self.arguments[0]
        self.pass_result(result=result)


if __name__ == '__main__':

    with open('day05_input.txt') as file:
        inputs = file.read()


## Testing:

def test_get_positions():
    assert get_positions(raw_code='1,0,0,0,99') == [1,0,0,0,99]

def test_get_opcode():
    assert get_opcode(positions=[1002,4,3,4,33],i=0) == 2

def test_get_modes():
    positions = [1002, 4, 3, 4, 33]
    operation = Operation(positions=positions,header=1002,i=0, verify=False)
    assert operation.modes == [0,1,0]

def test_get_arguments():
    positions = [1002, 4, 3, 4, 33]
    operation = Operation(positions=positions, header=1002, i=0, verify=False)
    assert operation.arguments == [33, 3]




