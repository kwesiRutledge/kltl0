"""
ltl.py
Description:
    A module for LTL formulae.
"""

from typing import List, Tuple, Union

from kltl.types import AtomicProposition

# Define Operators
NextSymbol = 'X'
UntilSymbol = 'U'
AlwaysSymbol = 'G'
EventuallySymbol = 'F'
AndSymbol = 'A'
OrSymbol = 'O'
NotSymbol = 'N'

Symbols = [NextSymbol, UntilSymbol, AlwaysSymbol, EventuallySymbol, AndSymbol, OrSymbol] # Could make this/symbol declarations a dictionary

class LTLFormula:
    def __init__(self, ap_or_operator: Union[AtomicProposition, 'LTLFormula'], subformulae: List['LTLFormula'] = []):
        self.ap_or_operator = ap_or_operator
        self.subformulae = subformulae
    def __str__(self):
        return f"LTL Formula:\nAP/Operator: {self.ap_or_operator}\nSubformulae: {self.subformulae}"



""" Functions """
def Next(phi: Union[AtomicProposition, LTLFormula]) -> LTLFormula:
    return LTLFormula(NextSymbol, [phi])

def Until(phi1: Union[AtomicProposition, LTLFormula], phi2: Union[AtomicProposition, LTLFormula]) -> LTLFormula:
    return LTLFormula(UntilSymbol, [phi1, phi2])

def Always(phi: Union[AtomicProposition, LTLFormula]) -> LTLFormula:
    return LTLFormula(AlwaysSymbol, [phi])

def Eventually(phi: Union[AtomicProposition, LTLFormula]) -> LTLFormula:
    return LTLFormula(EventuallySymbol, [phi])

def And(phi1: Union[AtomicProposition, LTLFormula], phi2: Union[AtomicProposition, LTLFormula], *args: Union[AtomicProposition, LTLFormula]):
    phis = [phi1, phi2]
    phis.extend(args)
    return LTLFormula(AndSymbol, phis)

def Or(phi1: Union[AtomicProposition, LTLFormula], phi2: Union[AtomicProposition, LTLFormula], *args: Union[AtomicProposition, LTLFormula]):
    phis = [phi1, phi2]
    phis.extend(args)
    return LTLFormula(OrSymbol, phis)

# If we pass a TransitionSystem object to the functions, could check absolute/in-depth satisfaction

def satisfies_next(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert len(trace_in) >= 2, '"Next" operator not applicable to length 1 trace'
    assert formula_in.ap_or_operator == NextSymbol, 'LTL formula must begin with "Next" operator to check for satisfaction thereof'
    
    phis = formula_in.subformulae
            
    for phi in phis:
        if not eval(phi, trace_in[1:]): return False
    return True
        
def satisfies_until(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert len(trace_in) >= 2
    assert formula_in.ap_or_operator == UntilSymbol, 'LTL formula must begin with "Until" operator to check for satisfaction thereof'
    
    ap1, ap2 = formula_in.subformulae

    for i in range(len(trace_in)):
        if eval(ap1, trace_in[i:]) and not eval(ap2, trace_in[i:]): continue
        elif i > 0 and eval(ap2, trace_in[i:]): return True
        else: return False
            
def satisfies_always(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert formula_in.ap_or_operator == AlwaysSymbol, 'LTL formula must begin with "Always" operator to check for satisfaction thereof'
    
    phis = formula_in.subformulae
    
    for t in trace_in:
        for p in phis:
            if not eval(p, trace_in): return False
    return True
    
def satisfies_eventually(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert formula_in.ap_or_operator == EventuallySymbol, 'LTL formula must begin with "Eventually" operator to check for satisfaction thereof'
    
    phis = formula_in.subformulae
    satisfied = {phi:False for phi in phis}
    
    for i in range(len(trace_in)):
        for phi in phis:
            if eval(phi, trace_in[i:]): satisfied[phi] = True
    return all(satisfied.values())

def satisfies_and(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert formula_in.ap_or_operator == AndSymbol, 'LTL formula must begin with "And" operator to check for satisfaction thereof'
    
    phis = formula_in.subformulae
    
    for phi in phis:
        if not eval(phi, trace_in): return False
    return True

def satisfies_or(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert formula_in.ap_or_operator == OrSymbol, 'LTL formula must begin with "Or" operator to check for satisfaction thereof'
    
    phis = formula_in.subformulae
    
    for phi in phis:
        if eval(phi, trace_in): return True
    return False

def satisfies_not(formula_in:LTLFormula, trace_in:List[List[str]]):
    assert formula_in.ap_or_operator == NotSymbol, 'LTL formula must begin with "Not" operator to check for satisfaction thereof'
    return not eval(formula_in, trace_in)

function_map = {
    
    # NextSymbol:satisfies_next,
    UntilSymbol:satisfies_until,
    AlwaysSymbol:satisfies_always,
    EventuallySymbol:satisfies_eventually,
    AndSymbol:satisfies_and,
    OrSymbol:satisfies_or,
    NotSymbol:satisfies_not
    
}

# The "eval" method is an internal method.
def eval(phi, trace_in):
        if type(phi) == str:
            return evaluate(LTLFormula(phi, []), trace_in)
        if type(phi) != str:
            return evaluate(phi, trace_in)

def evaluate(formula_in:LTLFormula, trace_in:List[List[str]]):
    
    ap_or_op = formula_in.ap_or_operator
    sub = formula_in.subformulae
    
    if ap_or_op not in Symbols:
        assert sub == [], 'LTL formula cannot contain more than one AP without an operator'
        
        if ap_or_op in trace_in[0]: return True
        return False
    
    elif ap_or_op == NextSymbol:    
        return satisfies_next(formula_in, trace_in)
    
    elif ap_or_op in Symbols and all(isinstance(s, str) for s in sub):
        return function_map[ap_or_op](formula_in, trace_in)
    elif ap_or_op in Symbols and sub != []:
        return function_map[ap_or_op](formula_in, trace_in)
    
