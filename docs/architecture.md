# Project Architecture

```text
Three-Address Code
        |
        v
     Parser
        |
        +----> USE / DEF
        |
        v
 Liveness Analysis
        |
        +----> LIVE-IN / LIVE-OUT
        |
        v
 Interference Graph
        |
        +----> Graph Statistics
        |
        v
   Graph Coloring
        |
        v
 Register Allocation
        |
        v
 Streamlit Dashboard
```

## Mathematical interpretation

Let `V` be the set of program variables. The interference graph is `G = (V, E)`.

A vertex represents a variable. An edge represents a conflict between variables that cannot share a register in the simplified model. A color represents one register. A valid coloring gives different colors to adjacent vertices.

The project uses NetworkX's greedy `largest_first` strategy. It produces a valid coloring and an upper bound on the minimum number of colors needed; it does not always calculate the exact chromatic number.

## Current simplification

The application assumes a straight-line sequence of simple assignment instructions. Branches, loops, control-flow graphs, spilling, assembly generation, and machine-specific register constraints can be added later.
