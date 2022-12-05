import math
import matplotlib.pyplot as plt
import numpy as np

def main():
    hex = read_file()
    binary = convert_hex_to_binary(hex)
    cache_size = [512, 1024, 2048, 4096]

    dm = np.asarray([direct_mapped(binary,i) for i in cache_size])
    faf = np.asarray([fully_assocative_fifo(binary, i) for i in cache_size])
    fal = np.asarray([fully_assocative_lru(binary, i) for i in cache_size])
    saf2 = np.asarray([set_assocative_fifo(binary, i, assoc=2) for i in cache_size])
    sal2 = np.asarray([set_assocative_lru(binary, i, assoc=2) for i in cache_size])
    saf4 = np.asarray([set_assocative_fifo(binary, i, assoc=4) for i in cache_size])
    sal4 = np.asarray([set_assocative_lru(binary, i, assoc=4) for i in cache_size])
    saf8 = np.asarray([set_assocative_fifo(binary, i, assoc=8) for i in cache_size])
    sal8 = np.asarray([set_assocative_lru(binary, i, assoc=8) for i in cache_size])

    #print("Direct Mapped: ", dm)
    #print("Fully Assocative FIFO: ", faf)
    #print("Fully Assocative LRU: ", fal)
    #print("2-Way Set Assocative FIFO: ", saf2)
    #print("2-Way Set Assocative LRU: ", sal2)
    # print("4-Way Set Assocative FIFO: ", saf4)
    # print("4-Way Set Assocative LRU: ", sal4)
    # print("8-Way Set Assocative FIFO: ", saf8)
    # print("8-Way Set Assocative LRU: ", sal8)

    plt.plot(cache_size, dm, label='Direct Mapped')
    plt.plot(cache_size, faf, label='Fully Assocative FIFO')
    plt.plot(cache_size, fal, label='Fully Assocative LRU')
    plt.plot(cache_size, saf2, label='2-Way Set Assocative FIFO')
    plt.plot(cache_size, sal2, label='2-Way Set Assocative LRU')
    plt.plot(cache_size, saf4, label='4-Way Set Assocative FIFO')
    plt.plot(cache_size, sal4, label='4-Way Set Assocative LRU')
    plt.plot(cache_size, saf8, label='8-Way Set Assocative FIFO')
    plt.plot(cache_size, sal8, label='8-Way Set Assocative LRU')
    plt.ylabel('Hit ratio')
    plt.xlabel('Cache Size (Bytes)')
    plt.legend(loc='lower right')
    plt.show()

class Address:
    tag = None
    counter = None


def read_file():
    f = open("input/gcc.trace", "r")
    lines = [line.split(' ') for line in f]
    f.close()
    hex = [i[1][2:] for i in lines]
    return hex

def convert_hex_to_binary(hex):
    result = []
    for i in hex:
        integer = int(i, 16)
        binary = bin(integer)[2:].zfill(32)
        result.append(binary)
    return result

def direct_mapped(binary, cache_size):
    block_size = 64
    num_lines = int(cache_size / block_size)
    num_line_bits = int(math.log(num_lines, 2))
    num_off_bits = int(math.log(block_size, 2))
    num_tag_bits = len(binary[0]) - num_line_bits - num_off_bits

    cache = dict.fromkeys(range(num_lines))
    hits = 0
    total = 0
    for i in binary:
        t = binary_to_decimal(i[:num_tag_bits])
        l = binary_to_decimal(i[num_tag_bits:num_tag_bits+num_line_bits])
        if (cache[l] == None):
            cache[l] = t
        elif (cache[l] == t):
            hits += 1
        else:
            cache[l] = t
        
        total += 1

    hit_rate = hits/total
    return hit_rate

def fully_assocative_fifo(binary, cache_size):
    block_size = 64
    num_lines = int(cache_size / block_size)
    num_line_bits = int(math.log(num_lines, 2))
    num_off_bits = int(math.log(block_size, 2))
    num_tag_bits = len(binary[0]) - num_line_bits - num_off_bits

    cache = dict.fromkeys(range(num_lines))
    counts = [0] * num_lines
    hits = 0
    count = 0

    for i in binary:
        count += 1
        items = 0
        t = binary_to_decimal(i[:num_tag_bits])
        if (len(cache) == 0):
            cache[0] = t
            counts[0] = count
        else:
            lowest = counts[0]
            i = 0
            hit = False
            for key in cache:
                if (counts[key] < lowest):
                    lowest = counts[key]
                    i = key
                if (t == cache[key]):
                    hits += 1
                    hit = True
                if (cache[key] != None):
                    items += 1
                if (cache[key] == None):
                    next_index = key
            if (hit == True):
                continue
            if (items != num_lines):
                cache[next_index] = t
                counts[next_index] = count
            else:
                cache[i] = t
                counts[i] = count

    return hits/count

def fully_assocative_lru(binary, cache_size):
    block_size = 64
    num_lines = int(cache_size / block_size)
    num_line_bits = int(math.log(num_lines, 2))
    num_off_bits = int(math.log(block_size, 2))
    num_tag_bits = len(binary[0]) - num_line_bits - num_off_bits

    cache = dict.fromkeys(range(num_lines))
    counts = [0] * num_lines
    hits = 0
    count = 0

    for i in binary:
        count += 1
        items = 0
        t = binary_to_decimal(i[:num_tag_bits])
        if (len(cache) == 0):
            cache[0] = t
            counts[0] = count
        else:
            lowest = counts[0]
            i = 0
            hit = False
            for key in cache:
                if (counts[key] < lowest):
                    lowest = counts[key]
                    i = key
                if (t == cache[key]):
                    hits += 1
                    counts[key] = count
                    hit = True
                if (cache[key] != None):
                    items += 1
                if (cache[key] == None):
                    next_index = key
            if (hit == True):
                continue
            if (items != num_lines):
                cache[next_index] = t
                counts[next_index] = count
            else:
                cache[i] = t
                counts[i] = count

    return hits/count

def set_assocative_fifo(binary, cache_size, assoc):
    block_size = 64
    num_lines = int(cache_size / block_size)
    num_set_bits = int(math.log(num_lines, 2))-1
    num_off_bits = int(math.log(block_size, 2))
    num_tag_bits = len(binary[0]) - num_set_bits - num_off_bits

    num_sets = int(num_lines / assoc)
    hits = 0
    count = 0
    cache = [[Address]*num_sets for i in range(num_lines)]
    for i in binary:
        count += 1
        t = binary_to_decimal(i[:num_tag_bits])
        s = binary_to_decimal(i[num_tag_bits:num_tag_bits+num_set_bits])
        hit = False
        items = 0
        if (cache[s][0].tag == None):
            cache[s][0].tag = t
            cache[s][0].counter = count
        else:
            lowest = cache[s][0].counter
            index = 0
            for c in range(len(cache[s])):
                if (cache[s][c] != None):
                    if (cache[s][c].counter < lowest):
                        lowest = cache[s][c]
                        index = c
                    items += 1
                if (cache[s][c].tag == t):
                    hits += 1
                    hit = True
                    break
            if (hit == False):
                for c in range(len(cache[s])):
                    if (cache[s][c].tag == None):
                        cache[s][c].tag = t
                        cache[s][c].counter = count
                        break
            
            if (items == len(cache[s])):
                cache[s][index].tag = t
                cache[s][index].counter = count

    return hits/count

def set_assocative_lru(binary, cache_size, assoc):
    block_size = 64
    num_lines = int(cache_size / block_size)
    num_line_bits = int(math.log(num_lines, 2))
    num_off_bits = int(math.log(block_size, 2))
    num_tag_bits = len(binary[0]) - num_line_bits - num_off_bits

    num_sets = int(num_lines / assoc)

    hits = 0
    count = 0
    cache = [[Address]*num_sets for i in range(num_lines)]
    for i in binary:
        count += 1
        t = binary_to_decimal(i[:num_tag_bits])
        s = binary_to_decimal(i[num_tag_bits:num_tag_bits+num_line_bits])
        hit = False
        items = 0
        if (cache[s][0].tag == None):
            cache[s][0].tag = t
            cache[s][0].counter = count
        else:
            lowest = cache[s][0].counter
            index = 0
            for c in range(len(cache[s])):
                if (cache[s][c] != None):
                    if (cache[s][c].counter < lowest):
                        lowest = cache[s][c]
                        index = c
                    items += 1
                if (cache[s][c].tag == t):
                    hits += 1
                    hit = True
                    cache[s][c].counter = count
                    break
            if (hit == False):
                for c in range(len(cache[s])):
                    if (cache[s][c].tag == None):
                        cache[s][c].tag = t
                        cache[s][c].counter = count
                        break
            
            if (items == len(cache[s])):
                cache[s][index].tag = t
                cache[s][index].counter = count

    return hits/count

def binary_to_decimal(n):
    return int(n,2)


main()