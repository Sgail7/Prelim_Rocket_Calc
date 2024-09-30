# from math import *

def taylor_second_forward(x_1, x_2, x_3, x_4):
    h = x_2 - x_1  # Step size
    f = (-x_4 + 4*x_3 - 5*x_2 + 2*x_1)/(h**2)
    return f

def taylor_second_backward(x_1, x_2, x_3, x_4):
    h = x_2 - x_1 # Step size
    f = (2*x_4 - 5*x_3 + 4*x_2 - x_1)/(h**2)
    return f

