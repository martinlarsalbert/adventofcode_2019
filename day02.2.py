

def get_positions(raw_code:str):
    positions_str = raw_code.split(',')
    positions = [int(position) for position in positions_str]
    return positions

def get_code_block(positions:list,i:int):
    code_block = positions[i:i + 4]
    return code_block


def run_program_code(raw_code:str):

    positions = get_positions(raw_code=raw_code)

    functions = {
        1 : add,
        2 : multiply,
        99: None,
    }


    i=0
    new_positions = positions.copy()
    while(i<len(positions)):

        code_block = get_code_block(positions=new_positions, i=i)
        function_code = code_block[0]
        if function_code == 99:
            break

        function_argument1 = new_positions[code_block[1]]
        function_argument2 = new_positions[code_block[2]]
        function_return_destination = code_block[3]

        if not function_code in functions:
            raise ValueError('Unknown function code:%i' % function_code)

        the_function = functions.get(function_code)
        the_function(new_positions, function_argument1, function_argument2, function_return_destination)

        i+=4

    return new_positions

def positions_to_string(positions):
    s = ''
    for position in positions[0:]:
        s+='%s,' % position
    s += '%s' % positions[-1]
    return s



def add(positions, function_argument1, function_argument2, function_return_destination):
    result = function_argument1+function_argument2
    pass_result(positions=positions, function_return_destination=function_return_destination, result=result)

def multiply(positions, function_argument1, function_argument2, function_return_destination):
    result = function_argument1*function_argument2
    pass_result(positions=positions, function_return_destination=function_return_destination, result=result)

def pass_result(positions, function_return_destination, result):
    positions[function_return_destination] = result

def change_noun_verb(positions,noun,verb):
    positions[1] = noun
    positions[2] = verb


if __name__ == '__main__':

    with open('day02_input.txt') as file:
        inputs = file.read()

    positions = get_positions(raw_code=inputs)
    found = False
    for noun in range(100):
        for verb in range(100):
            guess_positions = positions.copy()
            change_noun_verb(positions=guess_positions, noun=noun, verb=verb)

            new_raw_code = positions_to_string(positions=guess_positions)

            new_positions = run_program_code(raw_code=new_raw_code)
            if new_positions[0] == 19690720:
                found = True
                break

        if found:
            break

    print(positions_to_string(new_positions))
    if found:
        print('noun:%i' % noun)
        print('verb:%i' % verb)
        print('100*noun+verb=%i' % (100*noun+verb))


## Testing:

def test_get_positions():
    assert get_positions(raw_code='1,0,0,0,99') == [1,0,0,0,99]

def test_get_code_block():
    assert get_code_block(positions=[1,0,0,0,99],i=0) == [1,0,0,0]


def test_run_program_code():

    assert run_program_code(raw_code='1,0,0,0,99') == [2,0,0,0,99]
    assert run_program_code(raw_code='2,3,0,3,99') == [2,3,0,6,99]
    assert run_program_code(raw_code='2,4,4,5,99,0') == [2,4,4,5,99,9801]
    assert run_program_code(raw_code='1,1,1,4,99,5,6,0,99') == [30,1,1,4,2,5,6,0,99]

