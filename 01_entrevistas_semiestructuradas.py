# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 01 — ENTREVISTAS SEMI-ESTRUCTURADAS
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Autor pedagógico: Diseñado para Google Colab (auto-ejecutable).
Objetivo: simular un corpus de entrevistas a actores costeros, implementar
codificación abierta/axial, calcular fiabilidad intercodificadores (Cohen's κ),
construir matriz de co-ocurrencia de códigos y visualizar red temática.

Marco epistemológico: Grounded Theory (Strauss & Corbin, 1990) con triangulación
de codificadores siguiendo Krippendorff (2019) y O'Connor & Joffe (2020).
================================================================================
"""

# ============================================================
# 0. INSTALACIÓN (Google Colab)
# ============================================================
import subprocess, sys
def _pip(pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)
_pip(["networkx", "matplotlib", "numpy", "pandas", "scikit-learn"])

# ============================================================
# 1. IMPORTACIONES
# ============================================================
import numpy as np
import pandas as pd
import random
import re
from collections import Counter, defaultdict
from itertools import combinations
from sklearn.metrics import cohen_kappa_score
import networkx as nx
import matplotlib.pyplot as plt

SEED = 2026
random.seed(SEED); np.random.seed(SEED)

# ============================================================
# 2. GENERACIÓN SINTÉTICA DE CORPUS
#    Simulamos 12 entrevistas a actores del litoral Pacífico de Costa Rica:
#    pescadores artesanales, líderes comunitarios, funcionarios de INCOPESCA/MINAE,
#    operadores turísticos. Cada entrevista tiene 8–14 segmentos temáticos.
# ============================================================
ACTORES = [
    ("E01", "pescador_artesanal", "Golfo_de_Nicoya"),
    ("E02", "pescador_artesanal", "Golfo_Dulce"),
    ("E03", "lider_comunitario",  "Puntarenas"),
    ("E04", "funcionario_INCOPESCA", "Central"),
    ("E05", "operador_turistico", "Manuel_Antonio"),
    ("E06", "piangüera",           "Terraba_Sierpe"),
    ("E07", "biologa_marina",      "Osa"),
    ("E08", "funcionario_MINAE",   "Central"),
    ("E09", "pescador_artesanal", "Cuajiniquil"),
    ("E10", "lider_comunitario",  "Barra_del_Colorado"),
    ("E11", "operador_turistico", "Tamarindo"),
    ("E12", "piangüera",           "Chomes"),
]

# Banco de segmentos por código temático (corpus verosímil)
BANCO = {
    "VEDA_INCUMPLIMIENTO": [
        "aquí la veda no se respeta porque la gente tiene que comer",
        "los barcos grandes entran aunque sea tiempo de veda",
        "uno cumple pero otros siguen pescando de noche",
    ],
    "CONOCIMIENTO_TRADICIONAL": [
        "mi abuelo me enseñó dónde estaban los bancos de camarón",
        "antes sabíamos por la luna cuándo había marea buena",
        "el manglar uno lo lee como un libro si uno creció aquí",
    ],
    "CAMBIO_CLIMATICO": [
        "el mar ha subido metros en mi vida, la playa ya no está",
        "los peces ya no llegan en las fechas de antes",
        "las lluvias están desordenadas, el estero se llena distinto",
    ],
    "CONFLICTO_TURISMO": [
        "los hoteles cerraron el acceso a la playa que usábamos",
        "los yates espantan el pescado con el ruido",
        "el turismo trajo plata pero también basura",
    ],
    "GOBERNANZA_DEBIL": [
        "uno denuncia y nadie viene, la guardacostas no alcanza",
        "las reuniones del consejo son en San José y uno no puede ir",
        "las leyes están pero nadie las aplica en la práctica",
    ],
    "ORGANIZACION_LOCAL": [
        "la asociación de pescadores nos ha unido mucho",
        "el comité de vigilancia lo formamos nosotros mismos",
        "las mujeres piangüeras nos organizamos para el precio justo",
    ],
    "DISMINUCION_RECURSO": [
        "antes sacábamos veinte kilos, ahora apenas tres",
        "las pianguas son cada vez más pequeñas",
        "el camarón blanco casi desapareció del golfo",
    ],
    "IDENTIDAD_CULTURAL": [
        "soy pescador, eso no lo voy a cambiar por nada",
        "el mar es de uno, es herencia de los abuelos",
        "esta es nuestra forma de vivir, no un trabajo cualquiera",
    ],
}
CODIGOS = list(BANCO.keys())

def generar_entrevista(actor_id, perfil, zona, min_seg=8, max_seg=14):
    n = random.randint(min_seg, max_seg)
    segmentos = []
    # Actores con sesgos temáticos diferenciados (validez ecológica)
    pesos = {c: 1.0 for c in CODIGOS}
    if "pescador" in perfil or "piangüera" in perfil:
        pesos["CONOCIMIENTO_TRADICIONAL"] *= 2.2
        pesos["DISMINUCION_RECURSO"]     *= 2.0
        pesos["IDENTIDAD_CULTURAL"]      *= 1.8
    if "funcionario" in perfil:
        pesos["GOBERNANZA_DEBIL"]        *= 1.6
        pesos["VEDA_INCUMPLIMIENTO"]     *= 1.6
    if "turistico" in perfil:
        pesos["CONFLICTO_TURISMO"]       *= 1.5
    probs = np.array(list(pesos.values())); probs = probs / probs.sum()
    for _ in range(n):
        codigo = np.random.choice(CODIGOS, p=probs)
        texto  = random.choice(BANCO[codigo])
        segmentos.append({"actor": actor_id, "perfil": perfil, "zona": zona,
                          "segmento": texto, "codigo_verdadero": codigo})
    return segmentos

corpus = []
for a in ACTORES:
    corpus.extend(generar_entrevista(*a))
df = pd.DataFrame(corpus)
print(f"[DATOS] Corpus generado: {len(df)} segmentos de {df.actor.nunique()} entrevistas.\n")
print(df.head(4).to_string(index=False), "\n")

# ============================================================
# 3. CODIFICACIÓN ABIERTA AUTOMATIZADA (codificador A)
#    Implementa un diccionario de términos-pista (keyword-in-context)
#    que emula la asignación de códigos por un investigador humano.
# ============================================================
PISTAS = {
    "VEDA_INCUMPLIMIENTO":     ["veda", "no se respeta", "barcos grandes", "de noche"],
    "CONOCIMIENTO_TRADICIONAL":["abuelo", "luna", "sabíamos", "lee como un libro"],
    "CAMBIO_CLIMATICO":        ["mar ha subido", "lluvias", "fechas", "estero"],
    "CONFLICTO_TURISMO":       ["hoteles", "yates", "turismo", "acceso"],
    "GOBERNANZA_DEBIL":        ["denuncia", "nadie", "leyes", "San José", "guardacostas"],
    "ORGANIZACION_LOCAL":      ["asociación", "comité", "nos organizamos"],
    "DISMINUCION_RECURSO":     ["kilos", "camarón", "pianguas", "pequeñas"],
    "IDENTIDAD_CULTURAL":      ["soy pescador", "herencia", "forma de vivir", "mar es de uno"],
}
def codificar_A(texto):
    for cod, keys in PISTAS.items():
        if any(k in texto for k in keys): return cod
    return "SIN_CODIGO"

# Codificador B: humano con ruido (10% de divergencia aleatoria → realismo empírico)
def codificar_B(texto, p_divergencia=0.10):
    c = codificar_A(texto)
    if random.random() < p_divergencia:
        return random.choice([x for x in CODIGOS if x != c])
    return c

df["codigo_A"] = df["segmento"].apply(codificar_A)
df["codigo_B"] = df["segmento"].apply(codificar_B)

# ============================================================
# 4. FIABILIDAD INTERCODIFICADORES — Cohen's κ
#    Interpretación Landis & Koch (1977):
#    κ<0.20 pobre; 0.21–0.40 débil; 0.41–0.60 moderada;
#    0.61–0.80 sustancial; >0.80 casi perfecta.
# ============================================================
kappa = cohen_kappa_score(df["codigo_A"], df["codigo_B"])
print(f"[FIABILIDAD] Cohen's κ (A vs B) = {kappa:.3f}")
if kappa < 0.41:
    print("  → Fiabilidad insuficiente: revisar libro de códigos y negociar consenso.")
elif kappa < 0.61:
    print("  → Fiabilidad moderada: aceptable para fase exploratoria.")
elif kappa < 0.81:
    print("  → Fiabilidad sustancial: codificación robusta.")
else:
    print("  → Fiabilidad casi perfecta: publicable sin reservas metodológicas.\n")

# ============================================================
# 5. FRECUENCIAS Y MATRIZ DE CO-OCURRENCIA
#    Dos códigos co-ocurren si aparecen en la MISMA entrevista (unidad-actor).
# ============================================================
print("\n[FRECUENCIA DE CÓDIGOS — codificador A]")
freq = df["codigo_A"].value_counts()
print(freq.to_string(), "\n")

coocurrencia = pd.DataFrame(0, index=CODIGOS, columns=CODIGOS, dtype=int)
for actor, grupo in df.groupby("actor"):
    presentes = set(grupo["codigo_A"]) & set(CODIGOS)
    for c1, c2 in combinations(presentes, 2):
        coocurrencia.loc[c1, c2] += 1
        coocurrencia.loc[c2, c1] += 1

print("[MATRIZ DE CO-OCURRENCIA POR ENTREVISTA]")
print(coocurrencia.to_string(), "\n")

# ============================================================
# 6. VISUALIZACIÓN — Red temática (codificación axial)
# ============================================================
G = nx.Graph()
for c in CODIGOS:
    G.add_node(c, size=int(freq.get(c, 0)))
for c1, c2 in combinations(CODIGOS, 2):
    w = coocurrencia.loc[c1, c2]
    if w > 0: G.add_edge(c1, c2, weight=int(w))

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Panel A: frecuencias
axes[0].barh(freq.index[::-1], freq.values[::-1], color="#2E5C8A")
axes[0].set_title("Frecuencia de códigos (codificador A)", fontsize=12, weight="bold")
axes[0].set_xlabel("Nº segmentos")
axes[0].grid(axis="x", alpha=0.3)

# Panel B: red axial
pos = nx.spring_layout(G, seed=SEED, k=1.2)
sizes  = [300 + G.nodes[n]["size"]*40 for n in G.nodes]
widths = [G[u][v]["weight"]*0.6 for u, v in G.edges]
nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color="#D9662C", alpha=0.85, ax=axes[1])
nx.draw_networkx_edges(G, pos, width=widths, alpha=0.4, ax=axes[1])
nx.draw_networkx_labels(G, pos, font_size=8, ax=axes[1])
axes[1].set_title("Red temática axial (co-ocurrencia por entrevista)", fontsize=12, weight="bold")
axes[1].axis("off")
plt.tight_layout(); plt.savefig("lab01_entrevistas.png", dpi=130, bbox_inches="tight"); plt.show()

# ============================================================
# 7. INTERPRETACIÓN GUIADA (salida docente)
# ============================================================
top2 = freq.head(2).index.tolist()
print("="*72)
print("SÍNTESIS INTERPRETATIVA")
print("="*72)
print(f"• Códigos dominantes en el corpus: {top2[0]} y {top2[1]}.")
print(f"• Cohen's κ = {kappa:.3f} → decide si procede consenso negociado (Campbell et al., 2013).")
print(f"• Nodos de alto grado en la red axial identifican categorías centrales candidatas")
print(f"  a categoría-núcleo en la codificación selectiva (tercera fase Grounded Theory).")
print("="*72)
