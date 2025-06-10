from typing import Set, Dict
from .af import AF
from .formatter import AutomataFormatter


class AFN(AF):
    def __init__(
        self,
        Q: Set[str],
        Sigma: Set[str],
        delta: Dict[str, Dict[str, Set[str]]],
        q0: str,
        F: Set[str]
    ):
        super().__init__(Q, Sigma, delta, q0, F)

    def __repr__(self):
        return AutomataFormatter.format_afn(self)
    
    def print_transition_table(self):
        AutomataFormatter.print_afn_transition_table(self)