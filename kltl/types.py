from typing import Tuple
import numpy as np

State = str
Action = str
AtomicProposition = str

StateIndex = int
ActionIndex = int
AtomicPropositionIndex = int

Transition = Tuple[StateIndex, ActionIndex, StateIndex]
TransitionMatrix = np.array

Output = str