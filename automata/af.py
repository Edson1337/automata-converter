from abc import ABC, abstractmethod
from typing import Set, Dict, Any

class AF(ABC):
    def __init__(
        self,
        Q: Set[Any],  # Pode ser Set[str] ou Set[Set[str]] dependendo da subclasse
        Sigma: Set[str],
        delta: Dict,
        q0: Any,  # Pode ser str ou Set[str]
        F: Set[Any]  # Pode ser Set[str] ou Set[Set[str]]
    ):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F