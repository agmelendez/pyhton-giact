# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 06 — FOTO-VOZ (PHOTOVOICE)
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Objetivo: simular un proyecto PhotoVoice en una comunidad costera; cada
participante entrega fotos con metadatos (SHOWeD: See, Happening, Our lives,
Why, Doing about it), realizar clustering semántico de narrativas, generar
nube temática y red amenaza↔fortaleza por participante.

Referencias: Wang & Burris (1997) fundacional; Catalani & Minkler (2010)
revisión sistemática; Nykiforuk, Vallianatos & Nieuwendyk (2011) aplicaciones.
================================================================================
"""
import subprocess, sys
def _pip(pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)
_pip(["numpy","pandas","matplotlib","scikit-learn","networkx"])

import numpy as np, pandas as pd, random
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

SEED = 2026; random.seed(SEED); np.random.seed(SEED)

# ============================================================
# 1. SIMULACIÓN — 10 participantes × 6 fotos c/u = 60 fotos
# ============================================================
PARTICIPANTES = [f"PV{i:02d}" for i in range(1, 11)]
CATEGORIAS = ["AMENAZA", "FORTALEZA"]

NARRATIVAS = {
    "AMENAZA": {
        "basura_plastica":   "esta es la basura plástica que llega con la marea a nuestra playa",
        "erosion":           "aquí antes había tierra, el mar se la ha llevado en pocos años",
        "construccion_hotel":"el hotel cerró el acceso que siempre usamos para ir al mar",
        "desechos_hotel":    "la tubería del hotel descarga aguas grises al estero",
        "pesca_ilegal":      "estas redes de arrastre las dejan abandonadas y matan todo",
        "deforestacion":     "talaron el mangle para sembrar teca y ahora el estero está seco",
    },
    "FORTALEZA": {
        "vivero_manglar":    "este es el vivero de manglar que sembramos con las mujeres",
        "comite_vigilancia": "aquí nos reunimos los del comité de vigilancia costera cada sábado",
        "pesca_artesanal":   "esta es mi atarraya, la herencia que me dejó mi papá",
        "tortuga_nido":      "este nido lo protegimos nosotros, salieron 98 tortuguitas",
        "ninos_limpieza":    "los niños de la escuela vinieron a limpiar la playa ese día",
        "feria_pescadoras":  "esta feria la organizamos nosotras mismas para vender directo",
    },
}

filas = []
for p in PARTICIPANTES:
    # Cada persona entrega 3 amenazas + 3 fortalezas (protocolo común)
    for cat in CATEGORIAS:
        etiquetas = random.sample(list(NARRATIVAS[cat].keys()), 3)
        for e in etiquetas:
            filas.append({
                "participante": p, "categoria": cat, "etiqueta": e,
                "narrativa": NARRATIVAS[cat][e],
                "intensidad_emocional": random.randint(3, 10),  # escala 1–10
                "sesion_grupal": random.choice([1, 2, 3])      # ronda de discusión
            })
df = pd.DataFrame(filas)
print(f"[DATOS] PhotoVoice: {len(df)} fotos narradas, {df.participante.nunique()} participantes.\n")

# ============================================================
# 2. VECTORIZACIÓN TF-IDF + CLUSTERING SEMÁNTICO
# ============================================================
vect = TfidfVectorizer(max_features=80, ngram_range=(1,2), min_df=2)
X = vect.fit_transform(df["narrativa"]).toarray()
print(f"[TF-IDF] Matriz {X.shape[0]}x{X.shape[1]} sobre {len(vect.get_feature_names_out())} términos.\n")

K = 4
km = KMeans(n_clusters=K, random_state=SEED, n_init=10).fit(X)
df["cluster"] = km.labels_
pca = PCA(n_components=2, random_state=SEED).fit_transform(X)
df["pc1"] = pca[:, 0]; df["pc2"] = pca[:, 1]

# Términos dominantes por clúster
terminos = vect.get_feature_names_out()
print("[CLUSTERS TEMÁTICOS EMERGENTES]")
for c in range(K):
    top_idx = km.cluster_centers_[c].argsort()[::-1][:6]
    print(f"  Cluster {c}: {', '.join(terminos[top_idx])}")
print()

# ============================================================
# 3. RED AMENAZA↔FORTALEZA por participante
#    Nodo = foto; enlace si comparten participante.
# ============================================================
G = nx.Graph()
for i, r in df.iterrows():
    G.add_node(i, categoria=r.categoria, etiqueta=r.etiqueta,
               participante=r.participante)
for p in PARTICIPANTES:
    idxs = df[df.participante == p].index.tolist()
    for i in idxs:
        for j in idxs:
            if i < j and df.loc[i, "categoria"] != df.loc[j, "categoria"]:
                G.add_edge(i, j)

# ============================================================
# 4. MATRIZ DE INTENSIDAD EMOCIONAL POR ETIQUETA
# ============================================================
intens = df.groupby(["categoria","etiqueta"])["intensidad_emocional"].mean().round(2)
print("[INTENSIDAD EMOCIONAL MEDIA POR ETIQUETA]")
print(intens.to_string(), "\n")

# ============================================================
# 5. VISUALIZACIÓN — 3 paneles
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Panel 1: PCA + clusters
ax = axes[0]
for c in range(K):
    sub = df[df.cluster == c]
    ax.scatter(sub.pc1, sub.pc2, label=f"Cluster {c}", s=70, alpha=0.8)
ax.set_title("Mapa semántico PCA de narrativas PhotoVoice", weight="bold")
ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
ax.legend(); ax.grid(alpha=0.3)

# Panel 2: Heatmap amenaza/fortaleza por participante
ax = axes[1]
pivot = df.pivot_table(index="participante", columns="etiqueta",
                       values="intensidad_emocional", aggfunc="mean", fill_value=0)
im = ax.imshow(pivot.values, aspect="auto", cmap="RdYlGn_r")
ax.set_xticks(range(len(pivot.columns))); ax.set_xticklabels(pivot.columns, rotation=75, fontsize=7)
ax.set_yticks(range(len(pivot.index))); ax.set_yticklabels(pivot.index, fontsize=8)
ax.set_title("Intensidad emocional × etiqueta × participante", weight="bold")
plt.colorbar(im, ax=ax, label="Intensidad (1-10)")

# Panel 3: Red amenaza↔fortaleza
ax = axes[2]
pos = nx.spring_layout(G, seed=SEED)
colores = ["#C0392B" if G.nodes[n]["categoria"]=="AMENAZA" else "#27AE60" for n in G.nodes]
nx.draw_networkx_nodes(G, pos, node_color=colores, node_size=120, alpha=0.8, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.25, ax=ax)
ax.set_title("Red bimodal amenaza↔fortaleza por participante", weight="bold"); ax.axis("off")
plt.tight_layout(); plt.savefig("lab06_photovoice.png", dpi=130, bbox_inches="tight"); plt.show()

# ============================================================
# 6. CICLO SHOWeD (preguntas dialógicas de Wang)
# ============================================================
print("="*72)
print("PRÓXIMO PASO — Discusión grupal con protocolo SHOWeD (Wang, 1997):")
print("  S — What do you SEE here?")
print("  H — What's really HAPPENING here?")
print("  O — How does this relate to OUR lives?")
print("  W — WHY does this situation, concern or strength exist?")
print("  D — What can we DO about it?")
print("Las fotos de mayor intensidad emocional (≥8) guían la priorización")
print("de acciones comunitarias y la abogacía ante autoridades costeras.")
print("="*72)
