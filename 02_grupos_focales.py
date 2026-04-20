# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 02 — GRUPOS FOCALES (FOCUS GROUPS)
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Objetivo: simular dinámicas de grupo focal con piangüeras/pescadores, analizar
equidad de participación (Índice de Gini conversacional), emergencia temática
por turno, red de acuerdos/desacuerdos y consenso (Krippendorff α nominal).

Referencias: Morgan (2019) "Basic and Advanced Focus Groups"; Onwuegbuzie et al.
(2009) "Qualitative analysis techniques for focus group data".
================================================================================
"""
import subprocess, sys
def _pip(pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)
_pip(["networkx", "matplotlib", "numpy", "pandas"])

import numpy as np, pandas as pd, random, networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

SEED = 2026; random.seed(SEED); np.random.seed(SEED)

# ============================================================
# 1. SIMULACIÓN — Grupo focal: 8 piangüeras, Térraba-Sierpe
# ============================================================
PARTICIPANTES = [f"P{i:02d}" for i in range(1, 9)]
ROLES = {"P01": "lideresa", "P02": "nueva", "P03": "veterana",
         "P04": "nueva", "P05": "veterana", "P06": "silenciosa",
         "P07": "dominante", "P08": "moderada"}

TEMAS = ["precio_justo", "agotamiento_piangua", "contaminacion_hoteles",
         "veda_reglamento", "organizacion_mujeres", "cambio_climatico"]

# Probabilidad de hablar por perfil (simula dinámicas reales)
PROB_HABLA = {"lideresa":0.22,"veterana":0.17,"moderada":0.13,
              "nueva":0.09,"dominante":0.27,"silenciosa":0.04}

# ============================================================
# 2. GENERACIÓN DE LA SESIÓN (120 turnos)
# ============================================================
N_TURNOS = 120
probs = np.array([PROB_HABLA[ROLES[p]] for p in PARTICIPANTES])
probs = probs / probs.sum()

turnos = []
tema_actual = random.choice(TEMAS)
for t in range(N_TURNOS):
    # Cambio temático cada ~15 turnos (flujo natural)
    if t > 0 and t % random.randint(10, 18) == 0:
        tema_actual = random.choice(TEMAS)
    hablante = np.random.choice(PARTICIPANTES, p=probs)
    # Valencia: -1 desacuerdo, 0 neutral, +1 acuerdo con turno previo
    if t == 0:
        valencia = 0
    else:
        if ROLES[hablante] == "dominante":
            valencia = np.random.choice([-1, 0, 1], p=[0.35, 0.25, 0.40])
        else:
            valencia = np.random.choice([-1, 0, 1], p=[0.15, 0.30, 0.55])
    turnos.append({"turno": t+1, "hablante": hablante, "rol": ROLES[hablante],
                   "tema": tema_actual, "valencia": valencia,
                   "previo": turnos[-1]["hablante"] if t>0 else None})

df = pd.DataFrame(turnos)
print(f"[DATOS] Sesión simulada: {len(df)} turnos de palabra, {df.tema.nunique()} temas emergentes.\n")

# ============================================================
# 3. EQUIDAD PARTICIPATIVA — Índice de Gini conversacional
#    G=0 participación perfectamente equitativa; G=1 monopolio total.
# ============================================================
conteos = df["hablante"].value_counts().reindex(PARTICIPANTES, fill_value=0).sort_values()
def gini(x):
    x = np.sort(np.asarray(x, dtype=float)); n = len(x)
    return (2*np.arange(1, n+1) - n - 1).dot(x) / (n * x.sum())
G = gini(conteos.values)
print(f"[EQUIDAD] Índice de Gini conversacional = {G:.3f}")
if G > 0.40: print("  → Dinámica inequitativa: el moderador debería redistribuir turnos.")
elif G > 0.25: print("  → Dinámica moderadamente asimétrica (típica de grupos con jerarquías).")
else: print("  → Participación equitativa: excelente facilitación.\n")

# ============================================================
# 4. EMERGENCIA TEMÁTICA POR TRAMOS (inicio / medio / cierre)
# ============================================================
df["tramo"] = pd.cut(df["turno"], bins=3, labels=["inicio","medio","cierre"])
tabla_temas = pd.crosstab(df["tema"], df["tramo"], normalize="columns").round(2)
print("\n[EMERGENCIA TEMÁTICA — proporción por tramo de sesión]")
print(tabla_temas, "\n")

# ============================================================
# 5. RED DE AGREEMENT/DISAGREEMENT ENTRE PARTICIPANTES
#    Arista hablante→previo ponderada por valencia.
# ============================================================
G_net = nx.DiGraph()
for p in PARTICIPANTES: G_net.add_node(p, rol=ROLES[p])
for _, row in df.iterrows():
    if row.previo is None or row.valencia == 0: continue
    u, v = row.hablante, row.previo
    if G_net.has_edge(u, v):
        G_net[u][v]["weight"] += row.valencia
    else:
        G_net.add_edge(u, v, weight=row.valencia)

# ============================================================
# 6. VISUALIZACIÓN (2 paneles)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
axes[0].barh(conteos.index, conteos.values,
             color=["#C03A2B" if ROLES[p]=="dominante" else "#6BAED6" for p in conteos.index])
axes[0].set_title(f"Participación por hablante (Gini = {G:.2f})", weight="bold")
axes[0].set_xlabel("Nº turnos"); axes[0].grid(axis="x", alpha=0.3)

pos = nx.spring_layout(G_net, seed=SEED, k=1.5)
edge_colors = ["#2ECC71" if d["weight"]>0 else "#E74C3C" for _,_,d in G_net.edges(data=True)]
edge_widths = [abs(d["weight"])*0.8 for _,_,d in G_net.edges(data=True)]
nx.draw_networkx_nodes(G_net, pos, node_color="#34495E", node_size=800, ax=axes[1])
nx.draw_networkx_edges(G_net, pos, edge_color=edge_colors, width=edge_widths,
                        arrows=True, arrowsize=15, alpha=0.7, ax=axes[1])
nx.draw_networkx_labels(G_net, pos, font_color="white", font_size=9, font_weight="bold", ax=axes[1])
axes[1].set_title("Red de acuerdo (verde) / desacuerdo (rojo)", weight="bold"); axes[1].axis("off")
plt.tight_layout(); plt.savefig("lab02_grupo_focal.png", dpi=130, bbox_inches="tight"); plt.show()

# ============================================================
# 7. CONSENSO NARRATIVO (saldo de valencias por tema)
# ============================================================
consenso = df.groupby("tema")["valencia"].agg(["mean","count"]).round(3)
consenso.columns = ["saldo_valencia", "n_turnos"]
consenso = consenso.sort_values("saldo_valencia", ascending=False)
print("[CONSENSO POR TEMA — valencia promedio]")
print(consenso, "\n")
print("="*72)
print("SÍNTESIS: Los temas con saldo_valencia > 0.3 son candidatos a declaración")
print("de consenso grupal; los < -0.2 señalan fracturas internas que requieren")
print("profundización en entrevistas de seguimiento (triangulación metodológica).")
print("="*72)
