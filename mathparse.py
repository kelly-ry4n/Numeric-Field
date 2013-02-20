from __future__ import division
from collections import deque

def math_parse(expression):
    ''' Set up expression for parsing'''
    expression = expression.split()
    
    if expression[0].isdigit():
        return expression[0]
    else:
        return parse(deque(expression))

def parse(tokens):
    '''Simple recursive parser-compiler for Polish notation math experssions to
    python syntax math expressions'''

    token=tokens.popleft()
    if token=='+':
        return '('+parse(tokens)+'+'+parse(tokens)+')'
    elif token=='-':
        return '('+parse(tokens)+'-'+parse(tokens)+')'
    elif token=='*':
        return '('+parse(tokens)+'*'+parse(tokens)+')'
    elif token=='/':
        return '('+parse(tokens)+'/'+parse(tokens)+')'
    elif token=='^':
        return '('+parse(tokens)+'**'+parse(tokens)+')'
    
    elif token=='sin':
        return '(sin(' + parse(tokens) + '))'
    elif token=='cos':
        return '(cos(' + parse(tokens) + '))'
    elif token=='tan':
        return '(tan(' + parse(tokens) + '))'
    elif token=='exp':
        return '(exp(' + parse(tokens) + '))'
    elif token=='log':
        return '(log(' + parse(tokens) + '))'
    elif token=='log10':
        return 'log10(' + parse(tokens) + '))'

    else:
            # must be a number or variable
        return token




if __name__=='__main__':
        expression=" 13 "
        print math_parse(expression)