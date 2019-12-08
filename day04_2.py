import numpy as np

def verify(code):

    #Two adjacent digits are the same (like 22 in 122345).
    if not two_the_same(code=code):
        return False

    # never decrease
    if not never_decrese(code=code):
        return False

    return True

def two_the_same(code):
    code_str = str(code)
    unique = {}

    for digit in code_str:
        if digit in unique:
            unique[digit]+=1
        else:
            unique[digit] = 1

    two_counter = 0
    for digit,counter in unique.items():
        if counter == 2:
            return True

    return False


def never_decrese(code):
    code_str = str(code)
    old = 0
    for digit in code_str:
        if int(digit) < old:
            return False
        else:
            old = int(digit)

    return True

if __name__ == '__main__':
    start = 138241
    stop = 674034
    codes = np.arange(start,stop+1)
    assert codes[0] == start
    assert codes[-1] == stop

    counter = 0
    for code in codes:
        if verify(code):
            counter+=1

    print('Detected codes:%i' % counter)



### Tests ###

def test_two_the_same():
    assert two_the_same(112233)
    assert not two_the_same(123444)
    assert two_the_same(111122)


def test_never_decrease():

    assert never_decrese(111111)
    assert not never_decrese(223450)
    assert never_decrese(123789)

def test_verify():

    assert verify(112233)
    assert not verify(123444)
    assert verify(111122)
