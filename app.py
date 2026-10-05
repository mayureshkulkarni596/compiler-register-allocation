import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st

from src.coloring import color_graph, coloring_count
from src.interference import build_interference_graph, graph_statistics
from src.liveness import analyze_liveness
from src.parser import parse_program

st.set_page_config(page_title="Compiler Register Allocation", page_icon="🔢", layout="wide")
st.title("Compiler Register Allocation using Graph Coloring")
st.write("Enter simplified three-address code. The application parses it, performs liveness analysis, builds an interference graph, and assigns registers using greedy graph coloring.")

default_program = """a = b + c
d = a + e
f = d + c
g = f + a"""

program = st.text_area("Three-Address Code", value=default_program, height=180, help="Example: a = b + c")
register_count = st.number_input("Number of available registers", min_value=1, max_value=12, value=3, step=1)

if st.button("Analyze Program", type="primary"):
    try:
        instructions = parse_program(program)
        live_in, live_out = analyze_liveness(instructions)
        graph = build_interference_graph(instructions, live_in, live_out)
        stats = graph_statistics(graph)
        coloring = color_graph(graph)
        used_colors = coloring_count(coloring)

        st.subheader("1. Parsed Instructions")
        rows = [{"Instruction": x.number, "Code": x.text, "USE": ", ".join(sorted(x.use)) or "∅", "DEF": ", ".join(sorted(x.define)) or "∅"} for x in instructions]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        st.subheader("2. Liveness Analysis")
        rows = [{"Instruction": x.number, "Code": x.text, "LIVE-IN": ", ".join(sorted(live_in[i])) or "∅", "LIVE-OUT": ", ".join(sorted(live_out[i])) or "∅"} for i, x in enumerate(instructions)]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        st.subheader("3. Interference Graph")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Variables", stats["vertices"])
        c2.metric("Edges", stats["edges"])
        c3.metric("Maximum Degree", stats["max_degree"])
        c4.metric("Connected Components", stats["connected_components"])

        if graph.number_of_nodes():
            positions = nx.spring_layout(graph, seed=42)
            fig, ax = plt.subplots(figsize=(9, 6))
            nx.draw_networkx(graph, pos=positions, ax=ax, with_labels=True, node_size=1700, font_size=11)
            ax.set_axis_off()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.subheader("4. Graph Coloring and Register Allocation")
        rows = []
        for variable in sorted(graph.nodes()):
            color = coloring.get(variable)
            rows.append({"Variable": variable, "Color": color, "Register": f"R{color + 1}", "Degree": graph.degree(variable)})
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        st.write(f"Greedy coloring used **{used_colors} color(s)**.")
        if used_colors <= int(register_count):
            st.success(f"Allocation is possible with {register_count} register(s).")
        else:
            st.warning(f"This graph needs {used_colors} colors with the greedy strategy, but only {register_count} register(s) were provided.")
        st.info("DM interpretation: variables are vertices, interference is represented by edges, and registers are colors. Adjacent vertices cannot receive the same color.")
    except ValueError as exc:
        st.error(str(exc))
