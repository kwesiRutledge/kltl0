"""
ltl.py
Description:
    A module for LTL formulae.
"""

from typing import List, Tuple, Union

# from kltl.types import AtomicProposition #########################################

AtomicProposition = str

# Define Operators
NextSymbol = 'X'
UntilSymbol = 'U'
AlwaysSymbol = 'G'
EventuallySymbol = 'F'

class LTLFormula:
    def __init__(self, ap_or_operator: Union[AtomicProposition, 'LTLFormula'], subformulae: List['LTLFormula'] = []):
        self.ap_or_operator = ap_or_operator
        self.subformulae = subformulae



""" Functions """
def Next(phi: Union[AtomicProposition, LTLFormula]) -> LTLFormula:
    return LTLFormula(NextSymbol, [phi])

def Until(phi1: Union[AtomicProposition, LTLFormula], phi2: Union[AtomicProposition, LTLFormula]) -> LTLFormula:
    return LTLFormula(UntilSymbol, [phi1, phi2])

def Always(phi: Union[AtomicProposition, LTLFormula]) -> LTLFormula:
    return LTLFormula(AlwaysSymbol, [phi])

def Eventually(phi: Union[AtomicProposition, LTLFormula]) -> LTLFormula:
    return LTLFormula(EventuallySymbol, [phi])

# Need an AND function (and OR?)


# If we pass a TransitionSystem object to the functions, could check absolute/in-depth satisfaction

def satisfies_next(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert len(trace_in) >= 2 # How to check next function for length 1?
    assert formula_in.ap_or_operator == NextSymbol, 'LTL formula must begin with "Next" operator to check for satisfaction thereof'
    
    phis = formula_in.subformulae
    satisfies = True
    
    for p in phis:
        if p not in trace_in[1]: satisfies = False
        
    return satisfies
    
def satisfies_until(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert len(trace_in) >= 2
    assert formula_in.ap_or_operator == UntilSymbol, 'LTL formula must begin with "Until" operator to check for satisfaction thereof'
    
    ap1, ap2 = formula_in.subformulae
    for i in range(len(trace_in)):
        if (ap1 in trace_in[i] and ap2 not in trace_in[i]): continue
        elif (i > 0 and ap2 in trace_in[i]): return True
        else: return False
    
def satisfies_always(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert formula_in.ap_or_operator == AlwaysSymbol, 'LTL formula must begin with "Always" operator to check for satisfaction thereof'
    
    phis = formula_in.subformulae
    
    for t in trace_in:
        for p in phis:
            if p not in t: return False
    return True
    
def satisfies_eventually(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert formula_in.ap_or_operator == EventuallySymbol, 'LTL formula must begin with "Eventually" operator to check for satisfaction thereof'
    
    for t in trace_in:
        if formula_in.subformulae[0] in t: return True
    return False

function_map = {
    
    NextSymbol:satisfies_next,
    UntilSymbol:satisfies_until,
    AlwaysSymbol:satisfies_always,
    EventuallySymbol:satisfies_eventually
    
}

# def satisfies_full(formula_in:LTLFormula, trace_in:List[List[str]]):
#     # Base case
#     if all(type(sub) == str for sub in formula_in.subformulae):
#         return function_map[formula_in.ap_or_operator](LTLFormula, trace_in)
#     else:
#         #TODO
#         pass