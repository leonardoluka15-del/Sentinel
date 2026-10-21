import math

def identifier(value,valid):
    if not isinstance(value,str) or value not in valid: raise ValueError('Unknown device')
    return value

def integer(value,minimum=1,maximum=1000000000):
    if isinstance(value,bool) or not isinstance(value,int) or not minimum<=value<=maximum:
        raise ValueError('Invalid integer')
    return value
