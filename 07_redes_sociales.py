# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 07 — ANÁLISIS DE REDES SOCIALES CUALITATIVO (GOBERNANZA)
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Objetivo: modelar el ecosistema de actores (gobierno central, gobierno local,
pesca artesanal, ONG, academia, sector privado), calcular centralidades
(grado, intermediación, vector propio, cercanía), detectar comunidades con
Louvain, identificar AGUJEROS ESTRUCTURALES (Burt) y cuellos de botella de
información entre escalas de gobernanza.

Referencias: Bodin & Crona (2009) networks in NRM; Bodin (2017) Science;
Prell et al. (2009) stakeholder analysis; Burt (2004) structural holes.
================================================================================
"""
import subprocess, sys
def _pip(pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)
_pip(["networkx","matplotlib","numpy","pandas","python-louvain"])

import numpy as np, pandas as pd, random
import networkx as nx, matplotlib.pyplot as plt
import community as community_louvain  # python-louvain

SEED = 2026; random.seed(SEED); np.random.seed(SEED)

# ============================================================
# 1. DEFINICIÓN DE ACTORES (niveles de gobernanza multinivel)
# ============================================================
ACTORES = {
    # Gobierno central
    "MINAE":       "central",  "INCOPESCA":   "central", "SINAC":       "central",
    "ICT":         "central",  "Guardacostas": "central","Congreso":    "central",
    # Gobierno local
    "Muni_Puntarenas": "local","Muni_Osa":    "local",   "ADI_Chomes":  "local",
    # Academia
    "UCR_CIMAR":   "academia", "UNA_IRET":    "academia","UNED_OMiPYME":"academia",
    # Sociedad civil / ONG
    "MarViva":     "ong",      "ConservaInt": "ong",     "COOPTRASMAR": "ong",
    # Sector pesca / comunitario
    "FECOP":       "pesca",    "Asoc_Pescadores_GN": "pesca",
    "Mujeres_Piangueras":"pesca",
    # Sector privado
    "Camara_Hotelera":"privado", "Atunes_SA":  "privado",
}
COLORES_NIVEL = {"central":"#C0392B","local":"#E67E22","academia":"#2ECC71",
                 "ong":"#9B59B6","pesca":"#3498DB","privado":"#F1C40F"}

# ============================================================
# 2. MATRIZ DE VÍNCULOS (frecuencia de comunicación, simulada)
#    Escala 0–3: 0=nulo, 1=esporádico, 2=regular, 3=frecuente/institucionalizado
# ============================================================
nombres = list(ACTORES.keys())
n = len(nombres)
M = np.zeros((n, n), dtype=int)

# Reglas plausibles (top-down bias típico en gobernanza centralista)
reglas = [
    ("MINAE","SINAC",3),("MINAE","INCOPESCA",2),("MINAE","ICT",2),
    ("INCOPESCA","FECOP",2),("INCOPESCA","Asoc_Pescadores_GN",1),
    ("SINAC","UCR_CIMAR",2),("SINAC","MarViva",2),
    ("Guardacostas","INCOPESCA",2),("Guardacostas","Muni_Puntarenas",1),
    ("Muni_Puntarenas","ADI_Chomes",2),("Muni_Puntarenas","Asoc_Pescadores_GN",1),
    ("Muni_Osa","ADI_Chomes",1),("ADI_Chomes","Mujeres_Piangueras",3),
    ("UCR_CIMAR","UNA_IRET",3),("UCR_CIMAR","UNED_OMiPYME",2),("UNED_OMiPYME","UNA_IRET",2),
    ("MarViva","ConservaInt",3),("MarViva","FECOP",2),("MarViva","UCR_CIMAR",2),
    ("COOPTRASMAR","FECOP",3),("FECOP","Asoc_Pescadores_GN",3),
    ("Camara_Hotelera","ICT",3),("Camara_Hotelera","Atunes_SA",1),
    ("Atunes_SA","INCOPESCA",2),
    ("Congreso","MINAE",2),("Congreso","ICT",1),
    ("Mujeres_Piangueras","Asoc_Pescadores_GN",2),
    ("UNED_OMiPYME","Mujeres_Piangueras",2),  # vínculo real del Observatorio
]
idx = {k:i for i,k in enumerate(nombres)}
for a, b, w in reglas:
    M[idx[a], idx[b]] = w
    M[idx[b], idx[a]] = w

# Ruido estructural: pequeñas conexiones aleatorias
for _ in range(25):
    i, j = random.sample(range(n), 2)
    if M[i, j] == 0:
        M[i, j] = M[j, i] = 1

print(f"[RED] {n} actores, {int((M>0).sum()/2)} vínculos, densidad = {(M>0).sum()/(n*(n-1)):.3f}\n")

# ============================================================
# 3. CONSTRUIR GRAFO Y CALCULAR CENTRALIDADES
# ============================================================
G = nx.Graph()
for name in nombres: G.add_node(name, nivel=ACTORES[name])
for i in range(n):
    for j in range(i+1, n):
        if M[i, j] > 0:
            G.add_edge(nombres[i], nombres[j], weight=int(M[i, j]))

centralidades = pd.DataFrame({
    "grado":      pd.Series(nx.degree_centrality(G)),
    "intermediacion": pd.Series(nx.betweenness_centrality(G, weight="weight")),
    "cercania":   pd.Series(nx.closeness_centrality(G)),
    "vector_propio": pd.Series(nx.eigenvector_centrality_numpy(G, weight="weight")),
}).round(3)
centralidades["nivel"] = [ACTORES[n] for n in centralidades.index]
centralidades = centralidades.sort_values("intermediacion", ascending=False)
print("[CENTRALIDADES — top-10 por intermediación (brokers de información)]")
print(centralidades.head(10).to_string(), "\n")

# ============================================================
# 4. DETECCIÓN DE COMUNIDADES (Louvain)
# ============================================================
part = community_louvain.best_partition(G, weight="weight", random_state=SEED)
modularidad = community_louvain.modularity(part, G, weight="weight")
print(f"[LOUVAIN] {len(set(part.values()))} comunidades detectadas, modularidad Q = {modularidad:.3f}")
comunidades = pd.Series(part).rename("comunidad").reset_index().rename(columns={"index":"actor"})
print(comunidades.groupby("comunidad")["actor"].apply(lambda s: ", ".join(s)).to_string(), "\n")

# ============================================================
# 5. AGUJEROS ESTRUCTURALES — puentes débiles entre comunidades
#    (enlaces cuyos extremos están en comunidades distintas)
# ============================================================
puentes = [(u, v) for u, v in G.edges() if part[u] != part[v]]
print(f"[AGUJEROS ESTRUCTURALES] {len(puentes)} puentes inter-comunidad.")
if puentes:
    print("  Ejemplos:", puentes[:5], "\n")

# ============================================================
# 6. VISUALIZACIÓN
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
pos = nx.spring_layout(G, seed=SEED, k=1.5, iterations=80)

# Panel 1: red por nivel institucional
ax = axes[0]
for nivel, color in COLORES_NIVEL.items():
    nodos = [n for n in G.nodes if ACTORES[n] == nivel]
    nx.draw_networkx_nodes(G, pos, nodelist=nodos, node_color=color, node_size=700,
                           label=nivel, ax=ax, edgecolors="black", linewidths=0.8)
edges_w = [G[u][v]["weight"] for u, v in G.edges]
nx.draw_networkx_edges(G, pos, width=edges_w, alpha=0.35, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)
ax.set_title("Red de gobernanza multinivel (por nivel institucional)", weight="bold")
ax.legend(loc="best", fontsize=8); ax.axis("off")

# Panel 2: comunidades Louvain
ax = axes[1]
palette = plt.cm.tab10(np.linspace(0, 1, max(part.values())+1))
for i, comm in enumerate(set(part.values())):
    nodos = [n for n, c in part.items() if c == comm]
    nx.draw_networkx_nodes(G, pos, nodelist=nodos, node_color=[palette[comm]],
                           node_size=700, ax=ax, edgecolors="black", linewidths=0.8)
nx.draw_networkx_edges(G, pos, width=1, alpha=0.3, ax=ax)
# Resaltar puentes
if puentes:
    nx.draw_networkx_edges(G, pos, edgelist=puentes, width=2.5, edge_color="red", ax=ax)
nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)
ax.set_title(f"Comunidades Louvain (Q={modularidad:.2f}) — rojo=puentes", weight="bold")
ax.axis("off")
plt.tight_layout(); plt.savefig("lab07_redes.png", dpi=130, bbox_inches="tight"); plt.show()

print("="*72)
print("SÍNTESIS CUALITATIVA:")
print("• Los actores con alta intermediación son brokers: eliminarlos")
print("  fragmenta la comunicación (dependencia estructural riesgosa).")
print("• Los agujeros estructurales (puentes inter-comunidad) son")
print("  oportunidades o vulnerabilidades: punto de apoyo para la innovación")
print("  o punto único de fallo para la implementación de política.")
print("• Modularidad Q > 0.30 sugiere silos de gobernanza: la articulación")
print("  multinivel es débil y requiere intervención institucional.")
print("="*72)
