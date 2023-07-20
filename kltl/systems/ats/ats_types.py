from typing import Tuple, Set

ATSState = Tuple[str, Set[str]]
ATSTransition = Tuple[ATSState, str, ATSState]