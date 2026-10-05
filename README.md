# Compiler Register Allocation using Graph Coloring

A Discrete Mathematics project demonstrating simplified compiler register allocation through graph coloring.

## 60% milestone

This version includes simplified three-address code input, parsing into USE/DEF sets, backward liveness analysis, interference graph construction, graph statistics, greedy graph coloring, register allocation, and an interactive Streamlit dashboard.

The project intentionally does not implement a full compiler, assembly generation, register spilling, or complex control-flow analysis yet.

## Discrete Mathematics used

- Sets: USE, DEF, LIVE-IN, LIVE-OUT
- Relations: interference between variables
- Undirected graphs: interference graph
- Graph coloring: assigning registers
- Degree and connected components

## Tech stack

Python, Streamlit, NetworkX, Pandas, Matplotlib

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
