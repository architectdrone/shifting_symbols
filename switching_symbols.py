import random
import time

symbols = ['<', '>', '^', '/', '#']

STARTING_HEAD = 0
STARTING_EXEC = 0
STARTING_TAPE = [random.choice(symbols) for i in range(5)]

head = STARTING_HEAD
exec = STARTING_EXEC
tape = STARTING_TAPE
exec_place = 0

def inc_wrap(pos, list):
    return (pos+1)%(len(list))

def dec_wrap(pos, list):
    return (pos-1)%(len(list))

def char_list_print(list):
    for i in list:
        print(i, end="")
    print("")

def simple_stasis(tape):
    '''
    Checks if simple stasis (no pound signs) has been acheived.
    '''
    return '#' not in tape

def homogenous_stasis(tape):
    '''
    Checks if homogenous stasis (all signs the same) has been acheived
    '''
    return len(set(tape)) == 1

def type1_stasis(tape):
    '''
    Checks if type 1 stasis (one section of pound signs, surrounded by symbols whose sums are 0) has been reached
    '''
    x_axis = 0
    y_axis = 0

    tape_without_pounds = []
    for i in tape:
        if i != '#':
            tape_without_pounds.append(i)

    for current_symbol in tape_without_pounds:
        if current_symbol == '>':
            x_axis+=1
        elif current_symbol == '<':
            x_axis-=1
        elif current_symbol == '/':
            y_axis-=1
        elif current_symbol == '^':
            y_axis+=1
    
    return x_axis == 0 and y_axis == 0    
    

while True:
    if tape[head] == '<':
        exec = dec_wrap(exec, tape)
    elif tape[head] == '>':
        exec = inc_wrap(exec, tape)
    elif tape[head] == '^':
        exec_place = inc_wrap(exec_place, symbols)
    elif tape[head] == '/':
        exec_place = dec_wrap(exec_place, symbols)
    elif tape[head] == '#':
        tape[exec] = symbols[exec_place]
    
    head = inc_wrap(head, tape)
    
    if simple_stasis(tape):
        print("Simple Stasis")
    if homogenous_stasis(tape):
        print("Homogenous Stasis")
    if type1_stasis(tape):
        print("Type 1")

    to_place_indicator = [(" " if i != exec else symbols[exec_place]) for i in range(len(tape))]
    arm_indicator = [" " for i in range(len(tape))]
    arm_indicator[head] = 'H'
    arm_indicator[exec] = 'E'
    
    char_list_print(to_place_indicator)
    char_list_print(arm_indicator)
    char_list_print(tape)

    input(". ")

    print('\x1bc')