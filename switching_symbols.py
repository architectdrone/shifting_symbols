import random
import time
import copy

symbols = ['<', '>', '^', '/', '#']
STARTING_TAPE = [random.choice(symbols) for i in range(10)]

def inc_wrap(pos, list):
    return (pos+1)%(len(list))

def dec_wrap(pos, list):
    return (pos-1)%(len(list))

def char_list_print(list):
    for i in list:
        print(i, end="")
    print("")

class ShiftingSymbols():
    def __init__(self, tape, max_iterations = 50):
        self.max_iterations = max_iterations
        self.tape = tape
        self.initial_tape = copy.copy(tape)

    def run(self, show = True):
        global symbols
        head = 0
        exec = 0
        exec_place = 0
        runs = 0

        while True:
            runs+=1
            if self.tape[head] == '<':
                exec = dec_wrap(exec, self.tape)
            elif self.tape[head] == '>':
                exec = inc_wrap(exec, self.tape)
            elif self.tape[head] == '^':
                exec_place = inc_wrap(exec_place, symbols)
            elif self.tape[head] == '/':
                exec_place = dec_wrap(exec_place, symbols)
            elif self.tape[head] == '#':
                self.tape[exec] = symbols[exec_place]
            
            head = inc_wrap(head, self.tape)
            
            stasis_result = self.stasis_check(self.tape)
            if stasis_result['found']:
                return stasis_result
            elif runs >= self.max_iterations:
                stasis_result['initial'] = self.initial_tape
                return stasis_result

            if show:
                to_place_indicator = [(" " if i != exec else symbols[exec_place]) for i in range(len(self.tape))]
                arm_indicator = [" " for i in range(len(self.tape))]
                arm_indicator[head] = 'H'
                arm_indicator[exec] = 'E'
            
                char_list_print(to_place_indicator)
                char_list_print(arm_indicator)
                char_list_print(self.tape)
                input(". ")
                print('\x1bc')
    
    def stasis_check(self, tape):
        '''
        Perform known checks for stasis
        '''

        stasis_result = {}

        #Type 0
        simple = '#' not in tape
        homogenous = len(set(tape)) == 1
        type0 = simple or homogenous

        #Type 1
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
        
        type1 = x_axis == 0 and y_axis == 0

        if (type0):
            stasis_result['found'] = True
            stasis_result['type'] = 0
            stasis_result['simple'] = simple
            stasis_result['homogenous'] = homogenous
        elif (type1):
            stasis_result['found'] = True
            stasis_result['type'] = 1
        else:
            stasis_result['found'] = False
        
        return stasis_result

myTest = ShiftingSymbols(STARTING_TAPE, max_iterations=500)
results = myTest.run(show=False)
print(results)
