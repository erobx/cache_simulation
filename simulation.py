

def read_file():
    f = open("input/read01.trace", "r")
    for i in f:
        print(i)
    f.close()



read_file()