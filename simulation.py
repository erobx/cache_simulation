import math

def main():
    hex = read_file()
    binary = convert_hex_to_binary(hex)
    direct_mapped(binary)


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
        binary = format(integer, '0>42b')[10:]
        result.append(binary)
    return result
    

def direct_mapped(binary):
    bytes = [512, 1024, 2048, 4096]
    line = [64, 128]
    num_lines = int(bytes[0] / line[0])
    num_line_bits = int(math.log(num_lines, 2))
    num_off_bits = int(math.log(line[0], 2))
    num_tag_bits = len(binary[0]) - num_line_bits - num_off_bits

    print(num_tag_bits)
    print(num_line_bits)
    print(num_off_bits)

    set = dict.fromkeys(range(num_lines))
    #tag = dict.fromkeys(range(num_lines))
    
    for i in binary:
        print(i[:num_tag_bits])
        #t = binary_to_decimal(i[:num_tag_bits])
        #l = binary_to_decimal(i[num_tag_bits+num_line_bits:num_line_bits+num_off_bits])
        #set[l] = t



def binary_to_decimal(n):
    return int(n,2)



main()