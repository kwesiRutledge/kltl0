from typing import Tuple
from kltl.types import State, Action


Parameter = str
Transition = Tuple[State, Action, Parameter, State]
