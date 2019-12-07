import numpy as np

def test_calculate_fuel_requirement():

    assert calculate_fuel_requirement(mass=1969) == 966
    assert calculate_fuel_requirement(mass=100756) == 50346




def calculate_fuel_requirement(mass:int)->int:
    """
    Calculate the required fuel for one module
    :param mass: Mass of module
    :return: required fuel for one module
    """

    required_fuel = 0
    part_fuel = _calculate_fuel_requirement(mass=mass)

    while(part_fuel>0):
        part_mass = part_fuel
        required_fuel += part_fuel
        part_fuel = _calculate_fuel_requirement(mass=part_mass)


    return required_fuel

def _calculate_fuel_requirement(mass:int)->int:
    """
    Calculate the required fuel for one module
    :param mass: Mass of module
    :return: required fuel for one module
    """
    required_fuel = int(np.floor(mass/3) - 2)

    return required_fuel

def calculate_total_fuel_requirement(inputs:list)->int:

    assert isinstance(inputs,list)

    total_fuel_requirement = 0
    for input in inputs:
        fuel_requirement = calculate_fuel_requirement(mass=int(input))
        total_fuel_requirement+=fuel_requirement

    return total_fuel_requirement

if __name__ == '__main__':

    with open('day01_input.txt') as file:
        inputs = file.readlines()

    total_fuel_requirement = calculate_total_fuel_requirement(inputs=inputs)
    print(total_fuel_requirement)
