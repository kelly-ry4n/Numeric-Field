class Point:

    def __init__(self,x,y, charge=1):
        self.x = x
        self.y = y
        self.charge = charge

class Blob:

    def __init__(self):
        '''A temperary container for points which should be flattened into a list or
        array.'''
        self.xs = []
        self.ys = []
        self.charges = []

        ## self.math is a function object which should be created and bound by parsing
        self.math=lambda x,y : 1
        self.x_parameters = lambda t: 1
        self.y_parameters = lambda t: 1

    def __repr__(self):
        '''Print points in self'''
        print "BLOB"
        for x,y in zip(self.xs, self.ys):
            print x, y
        return 'END BLOB'

    def add_point(self,pt):
        self.xs.append(pt.x)
        self.ys.append(pt.y)

    def apply_math(self):
        '''If a parsed math expression describes the charge of the particle at a point,
        this numerically adds this value to self.chares'''
        for x,y in zip(self.xs,self.ys):
            self.charges.append(self.math(x,y))
            #self.math(x, y)

def blobs_to_lsts(blobs, outs):
    ''' 'Flatten' the list of blobs to the three output lists, applying math
    as we go.'''

    xs_out, ys_out, cs_out = outs[0], outs[1], outs[2]

    for blob in blobs:
        blob.apply_math()       ## blob.apply_math is defined at runtime by
                                ## parsing the last argument of a blob-creator
                                ## like rectangle into a math expression of
                                ## x and x

                                ## TODO: add time dependance (t?)

        for x,y,c in zip(blob.xs,blob.ys,blob.charges):   ## Construct output lists
            xs_out.append(x)                                
            ys_out.append(y)
            cs_out.append(c)

        ## TODO: convert to numpy arrays... shouldn't cause too many problems..
        ##       .. I think