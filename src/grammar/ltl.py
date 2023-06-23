"""
ltl.py
Description:
    A module for LTL formulae.
"""

from typing import List, Tuple, Union

from kltl0.types import AtomicProposition

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