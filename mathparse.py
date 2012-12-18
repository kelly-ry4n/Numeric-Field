from __future__ import division
from collections import deque

def math_parse(expression):
    return parse(deque(expression.split()))

def parse(tokens):
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
    else:
            # must be a number or variable

        return token



if __name__=='__main__':
        expression="/ - + 2 2 3 4"
        print math_parse(expression)