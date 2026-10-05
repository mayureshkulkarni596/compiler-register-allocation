import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import networkx as nx
import pandas as pd
import streamlit as st

from src.coloring import color_graph, coloring_count
from src.interference import build_interference_graph, graph_statistics
from src.liveness import analyze_liveness
from src.parser import parse_program


st.set_page_config(page_title="Compiler Register Allocation", page_icon="🔢", layout="wide")

st.title("Compiler Register Allocation using Graph Coloring")
st.write(
    "Enter simplified three-address code. The application parses it, performs "
    "liveness analysis, builds an interference graph, and assigns registers "
    "using greedy graph coloring."
)

examples = {
    "Custom": "",
    "Multiplication and Division": """t1 = a * b
t2 = t1 / c
t3 = t2 + d
result = t3 - e""",
    "Modulo and Copy": """x = a % b
y = x
z = y * c
result = z + d""",
    "Mixed Operations": """t1 = a * b
t2 = c / d
t3 = t1 + t2
t4 = t3 % e
result = t4 - f""",
    "Longer Program": """p = a * b
q = p + c
r = q / d
s = r % e
t = s + p
result = t * f""",
}

example_name = st.selectbox(
    "Try an example",
    list(examples.keys()),
    help="Choose an example to see a different interference graph, or choose Custom.",
)

default_program = examples[example_name]
if example_name == "Custom":
    default_program = """a = b + c
d = a + e
f = d + c
g = f + a"""

program = st.text_area(
    "Three-Address Code",
    value=default_program,
    height=180,
    help="Supported expressions can contain variables, constants, +, -, *, / and %.",
)

register_count = st.number_input(
    "Number of available registers",
    min_value=1,
    max_value=12,
    value=3,
    step=1,
)

if st.button("Analyze Program", type="primary"):
    try:
        instructions = parse_program(program)
        live_in, live_out = analyze_liveness(instructions)
        graph = build_interference_graph(instructions, live_in, live_out)
        stats = graph_statistics(graph)
        coloring = color_graph(graph)
        used_colors = coloring_count(coloring)

        st.subheader("1. Parsed Instructions")
        rows = [
            {
                "Instruction": x.number,
                "Code": x.text,
                "USE": ", ".join(sorted(x.use)) or "∅",
                "DEF": ", ".join(sorted(x.define)) or "∅",
            }
            for x in instructions
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        st.subheader("2. Liveness Analysis")
        rows = [
            {
                "Instruction": x.number,
                "Code": x.text,
                "LIVE-IN": ", ".join(sorted(live_in[i])) or "∅",
                "LIVE-OUT": ", ".join(sorted(live_out[i])) or "∅",
            }
            for i, x in enumerate(instructions)
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        st.subheader("3. Interference Graph")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Variables", stats["vertices"])
        c2.metric("Edges", stats["edges"])
        c3.metric("Maximum Degree", stats["max_degree"])
        c4.metric("Connected Components", stats["connected_components"])

        if graph.number_of_nodes():
            positions = nx.spring_layout(graph, seed=42)

            # Node colors show the greedy graph-coloring result.
            cmap = plt.get_cmap("tab10")
            node_colors = [
                cmap(coloring[node] % 10)
                for node in graph.nodes()
            ]
            labels = {
                node: f"{node}\nR{coloring[node] + 1}"
                for node in graph.nodes()
            }

            fig, ax = plt.subplots(figsize=(10, 6))
            nx.draw_networkx_edges(
                graph,
                positions,
                ax=ax,
                edge_color="gray",
                width=1.6,
            )
            nx.draw_networkx_nodes(
                graph,
                positions,
                ax=ax,
                node_color=node_colors,
                node_size=1900,
                edgecolors="black",
                linewidths=1.0,
            )
            nx.draw_networkx_labels(
                graph,
                positions,
                labels=labels,
                ax=ax,
                font_size=10,
                font_weight="bold",
            )

            legend_handles = [
                Patch(
                    facecolor=cmap(i % 10),
                    edgecolor="black",
                    label=f"R{i + 1} / Color {i}",
                )
                for i in range(used_colors)
            ]
            ax.legend(
                handles=legend_handles,
                title="Register Allocation",
                loc="upper right",
            )
            ax.set_axis_off()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.subheader("4. Graph Coloring and Register Allocation")
        rows = []
        for variable in sorted(graph.nodes()):
            color = coloring.get(variable)
            rows.append(
                {
                    "Variable": variable,
                    "Color": color,
                    "Register": f"R{color + 1}",
                    "Degree": graph.degree(variable),
                }
            )
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Colors Required", used_colors)
        c2.metric("Registers Available", int(register_count))
        c3.metric(
            "Allocation",
            "Possible" if used_colors <= int(register_count) else "Insufficient",
        )

        if used_colors <= int(register_count):
            st.success(f"Allocation is possible with {register_count} register(s).")
        else:
            st.warning(
                f"This graph needs {used_colors} colors with the greedy strategy, "
                f"but only {register_count} register(s) were provided."
            )

        st.info(
            "DM interpretation: variables are vertices, interference is represented "
            "by edges, and registers are colors. Adjacent vertices cannot receive "
            "the same color."
        )

    except ValueError as exc:
        st.error(str(exc))
