
def get_data(filename):
    with open(filename, 'r') as f:
        data = f.read()

    data = data.split('\n')
    data = (i.split(',') for i in data)
    data = zip(*data)

    return data[0],data[1],data[2]

def save_data(filename,xs,ys,cs):
    with open(filename, 'w') as f:
        for x,y,c in zip(xs[:-1],ys[:-1],cs[:-1]):
            f.write('%s,%s,%s\n' % (x,y,c))
        f.write('%s,%s,%s' % (x,y,c))

if __name__ == '__main__':
    print get_data('./Saves/test.figsave')