def 

def U_f(X,Y):
        '''Using expression strings from the function call, calculate U(X,Y) for each element of
        the meshgrid'''

        ## TODO: Change to numpy computation.
        ## TODO: Get rid of eval()... parse expressions externally
        out = []
        count = 0
        for X, Y in zip(X, Y):
            count += 1
            progress_q.put(int(count*100/float(res)))

            out.append(eval(Ustr))
        return array(out)

    def V_f(X,Y):
        '''Using expression strings from the function call, calculate V(X,Y) for each element of
        the meshgrid'''

        ## TODO: Change to numpy computations
        ## TODO: Get rid of eval()... parse expressions externally
        out = []
        count = 0
        for X, Y in zip(X, Y):
            #print count
            count += 1
            progress_q.put(int(count*100/float(res)))

            out.append(eval(Vstr))
        return array(out)