from energysim.utils.scientific_format import scientific_format

if __name__ == '__main__':
    value: float = 1.0

    for i in range(21):
        print(f'Value = {value:.3g} : ' + scientific_format(value))
        value *= 10.0

    value = 1.0
    for i in range(21):
        print(f'Value = {value:.3g} : ' + scientific_format(value))
        value /= 10.0