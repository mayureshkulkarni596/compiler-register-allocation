# Compiler Register Allocation using Graph Coloring

A Discrete Mathematics project demonstrating how graph theory can be applied to simplified compiler register allocation.

## Project idea

Variables in a program are represented as vertices of an interference graph. If two variables are needed at the same time, they are connected by an edge and cannot use the same register. Registers are represented by colors, so register allocation becomes a graph-coloring problem.

## Features

- Simplified three-address code input
- Instruction parsing with USE and DEF sets
- Backward liveness analysis
- Interference graph construction
- Basic graph statistics
- Greedy graph coloring
- Register allocation table
- Interactive Streamlit dashboard
- Example programs

## Discrete Mathematics concepts

- Sets: USE, DEF, LIVE-IN, LIVE-OUT
- Relations: interference between variables
- Undirected graphs: interference graph
- Graph coloring: assigning registers
- Degree and connected components

## Tech stack

- Python
- Streamlit
- NetworkX
- Pandas
- Matplotlib

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
