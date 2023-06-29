"""

test_model_checker.py
Description:
    Test cases for the LTL model checker in ltl.py

"""

from kltl.grammar.ltl import And, Or, Next, Always, Until, Eventually, evaluate

""" Test Cases """

traces = {
    1: [['a'],['a'],['b', 'a']],
    2: [['a','h','e','f'],['a','h','f','g'],['a','h','f'],['b','c','f'],['d','a','f'],['c','f'],['c','f'],['b','f']],
    3: [['a','e','f'],['a','h','f','g'],['a','h','f'],['b','c','f'],['d','a','f'],['c','f'],['c','f'],['b','f']],
    4: [['a','h','e','f'],['a','h','f','g'],['a','h','f'],['c','f'],['b','d','a','f'],['c','f'],['c','f'],['b','f']],
    5: [['d','a','h','e','f'],['a','h','f','g'],['a','h','f'],['b','c','f'],['a','f'],['c','f'],['c','f'],['b','f']]
}

sub_1a = And(Next(And('b', 'a')), 'c')
formula_1 = Next(sub_1a)

sub_2a = Always('f')
sub_2b = Until(And('a','h'),'b')
sub_2c = Or('e','a')
sub_2d = Eventually('d')
sub_2e = Next('g')
formula_2 = And(sub_2a, sub_2b, sub_2c, sub_2d, sub_2e)

print('Evaluation of formula 1 with trace 1: ', evaluate(formula_1, traces[1])) # Should evaluate to False

for i in range(2,6):
    print(f'Evaluation of formula 2 with trace {i}: ', evaluate(formula_2, traces[i])) 
    
    # Should evaluate to True, False, False, True