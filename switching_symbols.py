import time
import copy
import itertools
import numpy as np

symbols = ['<', '>', '^', '/', '#']
STARTING_TAPE = []
NUMBER_OF_SYMBOLS = 10

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
            
            stasis_result = self.stasis_check(self.tape, head)
            if stasis_result['found']:
                stasis_result['convergence'] = runs
                return stasis_result
            elif runs >= self.max_iterations:
                stasis_result['initial'] = self.initial_tape
                stasis_result['final'] = self.tape
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
    
    def stasis_check(self, tape, head):
        '''
        Perform known checks for stasis
        '''

        stasis_result = {}

        #Type 0
        #The tape has no means to self modify.
        simple = '#' not in tape
        homogenous = len(set(tape)) == 1
        type0 = simple or homogenous

        #Type 1
        #The tape has the means to self modify, but cannot.
        type1 = False
        directional_vectors = self.get_all_directional_vectors(tape)
        all_zero_vectors = all(i == (0,0) for i in directional_vectors)
        
        loopsize = 0
        if all_zero_vectors: #Loop Size = 0
            type1 = True
        elif len(directional_vectors) == 1: #Higher Order Loops.
            shift_vector = directional_vectors[0]
            initial_position = self.get_position_vector(tape, head)
            current_shifted_position = initial_position
            while True:
                loopsize+=1
                current_shifted_position = self.convert_to_position_vector(shift_vector, current_shifted_position, tape)
                current_positon = self.get_position_vector(tape, current_shifted_position[0])
                if current_shifted_position != current_positon:
                    break
                elif current_shifted_position == initial_position:
                    type1 = True
                    break

        if (type0):
            stasis_result['found'] = True
            stasis_result['type'] = 0
            stasis_result['simple'] = simple
            stasis_result['homogenous'] = homogenous
        elif (type1):
            stasis_result['found'] = True
            stasis_result['type'] = 1
            stasis_result['loopsize'] = loopsize
        else:
            stasis_result['found'] = False
        
        return stasis_result

    def get_position_vector(self, tape, position):
        return (position, symbols.index(tape[position]))
    
    def convert_to_position_vector(self, vec1, vec2, tape):
        return ((vec1[0]+vec2[0])%len(tape), (vec1[1]+vec2[1])%len(tape))
    
    # def contiguous_pounds(self, tape):
    #     '''
    #     Returns true if there is one region of pound signs.
    #     '''

    #     grouped = [i[0] for i in itertools.groupby(tape)]
    #     if grouped.count('#') == 1:
    #         return True
    #     elif grouped.count('#') and grouped[0] == '#' and grouped[-1] == '#':
    #         return True
    #     else:
    #         return False
    
    def get_all_directional_vectors(self, tape):
        '''
        Extracts all directional vectors separated by pounds from the tape.
        '''

        x_axis = 0
        y_axis = 0
        reported_pound = False

        all_directional_vectors = []
        while True:
            current_symbol = tape[0]
            tape = tape[1:]

            if current_symbol == '>':
                reported_pound = False
                x_axis+=1
            elif current_symbol == '<':
                reported_pound = False
                x_axis-=1
            elif current_symbol == '/':
                reported_pound = False
                y_axis-=1
            elif current_symbol == '^':
                reported_pound = False
                y_axis+=1
            elif current_symbol == '#' and reported_pound == False:
                all_directional_vectors.append((x_axis,y_axis))
                x_axis = y_axis = 0
            
            if tape == []:
                if current_symbol != '#': #This means that the last directional vector is actually part of the first, wack I know
                    if all_directional_vectors == []: # Unless no directional vectors were ever added.
                        all_directional_vectors.append((x_axis,y_axis))
                    first_vector = all_directional_vectors[0]
                    all_directional_vectors[0] = (first_vector[0]+x_axis, first_vector[1]+y_axis)
                break
        
        return all_directional_vectors

class Tape():
    def __init__(self, inital_array):
        self.initial_array = inital_array

    def getTapePoint(self, x):
        global symbols
        y = symbols.index(self.initial_array[x])
        return TapeVector(x, y, self, position_vector=True)

    def getVectors(self):
        '''
        Returns shift vectors, the orienting vector, and whatever vector is next.
        '''
        up_vector = TapeVector(0, 1, self)
        down_vector = TapeVector(0, -1, self)
        left_vector = TapeVector(-1, 0, self)
        right_vector = TapeVector(1, 0, self)

    def getSize(self):
        return len(self.initial_array)

class TapeVector():
    def __init__(self, x, y, tape, symbol_size = 5, position_vector = False):
        self.vector = np.array([x, y])
        self.tape_size = tape.getSize()
        self.symbol_size = symbol_size
        self.position_vector = position_vector
        if self.position_vector:
            _convertToPosition()

    def _convertToPosition(self):
        self.vector[0,0] = self.vector[0,0]%self.tape_size
        self.vector[0,1] = self.vector[0,1]%self.symbol_size
        
    def __add__(self, tv2):
        new_vector = self.vector+tv2.vector
        if self.position_vector or tv2.position_vector:
            return TapeVector(new_vector[0,0], new_vector[0,1], self.tape, position_vector=True)
        else:
            return TapeVector(new_vector[0,0], new_vector[0,1], self.tape)

if STARTING_TAPE == []:
    type0_number = 0
    homogenous_number = 0
    simple_number = 0
    type1_number = 0
    unknown_number = 0
    unknowns = []
    total_convergence = 0
    total = 0

    for i in itertools.combinations_with_replacement(symbols, NUMBER_OF_SYMBOLS):
        total+=1
        myTest = ShiftingSymbols(list(i), max_iterations=5000)
        results = myTest.run(show=False)
        if results['found']:
            if results['type'] == 0:
                type0_number+=1
                if results['homogenous']:
                    homogenous_number+=1
                if results['simple']:
                    simple_number+=1
            elif results['type'] == 1:
                type1_number+=1
            if results['convergence'] != 1:
                total_convergence+=results['convergence']
        else:
            unknown_number+=1
            unknowns.append(results['final'])

    print("TEST COMPLETE")
    print(f"Average to non-trivial convergence: {total_convergence/total}")
    print(f"0: {type0_number/total}")
    print(f"1: {type1_number/total}")
    print(f"?: {unknown_number/total}")
    print(f"Unknowns: {unknowns}")

else:
    myTest = ShiftingSymbols(STARTING_TAPE, max_iterations=5000)
    print(myTest.run())