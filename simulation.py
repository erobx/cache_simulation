import time

def main():
    hex = read_file()
    binary = convert_hex_to_binary(hex)


def read_file():
    f = open("input/read01.trace", "r")
    lines = [line.split(' ') for line in f]
    f.close()
    hex = [i[1][2:] for i in lines]
    return hex
    

def convert_hex_to_binary(hex):
    result = []
    for i in hex:
        integer = int(i, 16)
        binary = format(integer, '0>42b')
        result.append(binary)
    return result


def init_cache():
    return

main()