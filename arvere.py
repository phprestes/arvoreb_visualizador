import struct

import matplotlib.pyplot as plt
import networkx as nx
import sys

nome_arquivo = sys.argv[1]
# nro_nos = int(input())

ORDEM = 3
TAM_CAMPO = 16
TAM_NO = TAM_CAMPO * (ORDEM - 1) + 12


def ler_header(headerBin):
    header = struct.unpack(f"<1s iii {TAM_NO - 13}s", headerBin)
    return {
        "status": header[0].decode("ascii"),
        "noRaiz": header[1],
        "proxRRN": header[2],
        "nroNos": header[3],
    }


def ler_no(noBin):
    formato = "<ii" + "iiq" * (ORDEM - 1) + "i"
    no = struct.unpack(formato, noBin)

    dicNo = {
        "tipoNo": no[0],
        "nroChaves": no[1],
    }

    for i in range(ORDEM - 1):
        dicNo[f"P{i+1}"] = no[3 * i + 2]
        value = no[3 * i + 3]
        if 0 <= value <= 0x10FFFF:
            dicNo[f"C{i+1}"] = value
        else:
            dicNo[f"C{i+1}"] = value
        dicNo[f"Pr{i+1}"] = no[3 * i + 4]

    dicNo[f"P{ORDEM}"] = no[-1]
    return dicNo


##################
G = nx.DiGraph()

with open(nome_arquivo, "rb") as f:
    headerBin = f.read(TAM_NO)
    header = ler_header(headerBin)
    print("Header:", header)

    nos = {}
    for i in range(header["nroNos"]):
        noBin = f.read(TAM_NO)
        nos[i] = ler_no(noBin)

print(nos)

# Adiciona nós e arestas ao grafo
for id_no, no in nos.items():
    label = str(id_no) + "\n"
    label += " | ".join(str(no[f"C{j+1}"]) for j in range(no["nroChaves"]))

    G.add_node(id_no, label=label)

    if no["tipoNo"] != -1:
        for j in range(1, ORDEM + 1):
            filho = no[f"P{j}"]
            if filho != -1 and filho in nos:
                G.add_edge(id_no, filho)

# Visualização
pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
labels = nx.get_node_attributes(G, "label")

node_colors = []
for node in G.nodes():
    no = nos[node]
    if no["tipoNo"] == 0:
        node_colors.append("lightcoral")  # Raiz
    elif no["tipoNo"] == 1:
        node_colors.append("lightblue")  # Intermediário
    elif no["tipoNo"] == -1:
        node_colors.append("lightgreen")  # Folha
    else:
        node_colors.append("red")  # ERRO

plt.figure(figsize=(12, 8))
nx.draw(
    G,
    pos,
    labels=labels,
    with_labels=True,
    node_shape="s",
    node_size=2000,
    node_color=node_colors,
    arrows=True,
    font_size=10,
)

plt.title(f"Árvore B de {nome_arquivo}")
plt.show()
