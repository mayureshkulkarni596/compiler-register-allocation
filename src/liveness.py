"""Backward liveness analysis for a linear instruction sequence."""

from typing import List, Set, Tuple
from .parser import Instruction


def analyze_liveness(instructions: List[Instruction]) -> Tuple[List[Set[str]], List[Set[str]]]:
    n = len(instructions)
    live_in = [set() for _ in range(n)]
    live_out = [set() for _ in range(n)]

    for i in range(n - 1, -1, -1):
        if i < n - 1:
            live_out[i] = live_in[i + 1].copy()
        live_in[i] = instructions[i].use | (live_out[i] - instructions[i].define)

    return live_in, live_out
