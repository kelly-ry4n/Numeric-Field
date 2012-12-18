
def get_data(filename):
    with open(filename, 'r') as f:
        data = f.read()

    data = data.split('\n')
    data = (i.split(',') for i in data)
    data = zip(*data)
    return data[0],data[1],data[2]

if __name__ == '__main__':
    print get_data('./Saves/t1.txt')