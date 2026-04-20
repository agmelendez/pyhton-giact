# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 09 — OBSERVACIÓN PARTICIPANTE
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Objetivo: simular diarios de campo de observación participante en reuniones
de un Consejo Local de Manejo Costero (COVIMAR) durante 12 sesiones,
estructurar el log con dimensiones (actor, tipo-evento, tópico, decisión,
duración, valencia), construir matriz de interacción, sociograma direccional
y mapa de ruta de toma de decisiones (event-sequence analysis).

Referencias: DeWalt & DeWalt (2011) Participant Observation; Spradley (1980);
Kawulich (2005) método y ética; Tilly (2008) contentious dynamics.
================================================================================
"""
import subprocess, sys
def _pip(pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)
_pip(["numpy","pandas","matplotlib","networkx"])

import numpy as np, pandas as pd, random
import networkx as nx, matplotlib.pyplot as plt

SEED = 2026; random.seed(SEED); np.random.seed(SEED)

# ============================================================
# 1. ACTORES HABITUALES DEL COVIMAR
# ============================================================
ACTORES = {
    "PRESIDENTE_Consejo":"local",
    "DELEGADO_MINAE":"central",
    "DELEGADO_INCOPESCA":"central",
    "DELEG_Muni":"local",
    "REP_Pescadores":"pesca",
    "REP_Piangueras":"pesca",
    "REP_Hoteleros":"privado",
    "ACADEMIA_UCR":"academia",
    "ONG_MarViva":"ong",
    "OBSERVADOR":"investigador",  # el investigador que realiza observación participante
}
TIPOS_EVENTO = ["intervencion","propuesta","objecion","acuerdo","voto","silencio_grupal"]
TOPICOS = ["veda_camaron","playa_publica","descargas_hotel","subsidio_combustible",
           "monitoreo_calidad_agua","conflicto_turismo_pesca","reglamento_interno"]

# ============================================================
# 2. SIMULACIÓN DE 12 SESIONES MENSUALES
# ============================================================
N_SESIONES = 12
eventos = []
for s in range(1, N_SESIONES+1):
    fecha = pd.Timestamp(2025, 1, 15) + pd.DateOffset(months=s)
    # Cada sesión tiene 25–45 eventos
    n_eventos = random.randint(25, 45)
    # Selección de 2-3 tópicos por sesión
    topicos_sesion = random.sample(TOPICOS, k=random.randint(2, 3))
    for e in range(n_eventos):
        actor = random.choices(list(ACTORES.keys()),
                               weights=[3,2,2,2,3,2,2,1,2,1])[0]  # presidente habla más
        tipo = np.random.choice(TIPOS_EVENTO, p=[0.40,0.15,0.12,0.15,0.05,0.13])
        topico = random.choice(topicos_sesion)
        # Duración (s) por tipo
        duracion = {"intervencion":90,"propuesta":180,"objecion":120,
                     "acuerdo":60,"voto":30,"silencio_grupal":40}[tipo]
        duracion += random.randint(-20, 60)
        # Dirigido a (para sociograma) — None si no es interacción diádica
        dirigido = None
        if tipo in ("objecion","propuesta","acuerdo"):
            otros = [a for a in ACTORES if a != actor]
            dirigido = random.choice(otros)
        valencia = {"acuerdo":+1,"propuesta":+0.5,"objecion":-1,
                     "intervencion":0,"voto":0,"silencio_grupal":0}[tipo]
        eventos.append({"sesion":s,"fecha":fecha,"orden":e+1,
                        "actor":actor,"tipo":tipo,"topico":topico,
                        "duracion_s":duracion,"dirigido_a":dirigido,
                        "valencia":valencia})
df = pd.DataFrame(eventos)
print(f"[DATOS] {len(df)} eventos registrados en {N_SESIONES} sesiones del COVIMAR.\n")
print(df.head(5).to_string(index=False), "\n")

# ============================================================
# 3. DISTRIBUCIÓN DE TIEMPO DE PALABRA POR ACTOR
# ============================================================
tiempo = df.groupby("actor")["duracion_s"].sum().sort_values(ascending=False)
tiempo_min = (tiempo/60).round(1)
print("[TIEMPO DE PALABRA ACUMULADO — minutos]")
print(tiempo_min.to_string(), "\n")

# ============================================================
# 4. MATRIZ DE INTERACCIÓN (actor → dirigido_a)
# ============================================================
inter = df.dropna(subset=["dirigido_a"])
matriz = pd.crosstab(inter["actor"], inter["dirigido_a"])
print("[MATRIZ DE INTERACCIÓN DIÁDICA — eventos dirigidos]")
print(matriz.to_string(), "\n")

# ============================================================
# 5. DECISIONES ALCANZADAS POR SESIÓN Y TÓPICO
# ============================================================
acuerdos = df[df["tipo"] == "acuerdo"].groupby(["sesion","topico"]).size().unstack(fill_value=0)
print("[ACUERDOS POR SESIÓN × TÓPICO]")
print(acuerdos.to_string(), "\n")

# ============================================================
# 6. SECUENCIA DE EVENTOS PARA UN TÓPICO CRÍTICO
#    Rastreo del 'camino a la decisión' sobre descargas_hotel.
# ============================================================
ruta = df[df["topico"] == "descargas_hotel"].sort_values(["sesion","orden"])
print(f"[RUTA DE DECISIÓN — tópico 'descargas_hotel']: {len(ruta)} eventos")
print(ruta[["sesion","actor","tipo","valencia"]].head(10).to_string(index=False), "\n")

# ============================================================
# 7. VISUALIZACIÓN
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 11))

# (1) Tiempo de palabra
ax = axes[0, 0]
colores = [{"local":"#E67E22","central":"#C0392B","pesca":"#3498DB",
             "privado":"#F1C40F","academia":"#2ECC71","ong":"#9B59B6",
             "investigador":"#7F8C8D"}[ACTORES[a]] for a in tiempo_min.index]
ax.barh(tiempo_min.index, tiempo_min.values, color=colores)
ax.set_title("Tiempo de palabra por actor (12 sesiones)", weight="bold")
ax.set_xlabel("Minutos acumulados"); ax.grid(axis="x", alpha=0.3)

# (2) Heatmap interacciones
ax = axes[0, 1]
im = ax.imshow(matriz.values, aspect="auto", cmap="YlOrRd")
ax.set_xticks(range(len(matriz.columns))); ax.set_xticklabels(matriz.columns, rotation=45, ha="right", fontsize=7)
ax.set_yticks(range(len(matriz.index))); ax.set_yticklabels(matriz.index, fontsize=7)
ax.set_title("Interacciones dirigidas (emisor → receptor)", weight="bold")
plt.colorbar(im, ax=ax)

# (3) Sociograma direccional
ax = axes[1, 0]
G = nx.DiGraph()
for a in ACTORES: G.add_node(a)
for i, r in inter.iterrows():
    if G.has_edge(r["actor"], r["dirigido_a"]):
        G[r["actor"]][r["dirigido_a"]]["weight"] += 1
    else:
        G.add_edge(r["actor"], r["dirigido_a"], weight=1)
pos = nx.circular_layout(G)
widths = [G[u][v]["weight"]*0.2 for u, v in G.edges]
nx.draw_networkx_nodes(G, pos, node_color="#34495E", node_size=900, ax=ax)
nx.draw_networkx_edges(G, pos, width=widths, alpha=0.5, arrows=True, arrowsize=12,
                        connectionstyle="arc3,rad=0.1", ax=ax)
nx.draw_networkx_labels(G, pos, font_color="white", font_size=6, font_weight="bold", ax=ax)
ax.set_title("Sociograma direccional del COVIMAR", weight="bold"); ax.axis("off")

# (4) Timeline de valencia acumulada por tópico crítico
ax = axes[1, 1]
for top in TOPICOS[:4]:
    sub = df[df["topico"] == top].sort_values(["sesion","orden"])
    if len(sub) > 0:
        vac = sub["valencia"].cumsum().values
        ax.plot(range(len(vac)), vac, label=top, linewidth=2)
ax.set_title("Trayectoria de valencia acumulada por tópico", weight="bold")
ax.set_xlabel("Secuencia de eventos"); ax.set_ylabel("Valencia acumulada")
ax.axhline(0, color="gray", linestyle="--"); ax.legend(fontsize=7); ax.grid(alpha=0.3)

plt.tight_layout(); plt.savefig("lab09_observacion.png", dpi=130, bbox_inches="tight"); plt.show()

# ============================================================
# 8. NOTAS DE CAMPO (reflexividad del observador)
# ============================================================
print("="*72)
print("REFLEXIVIDAD DEL INVESTIGADOR (diario de campo):")
print("• El OBSERVADOR registró 0 intervenciones en pleno, pero 3 preguntas")
print("  informales al PRESIDENTE durante los recesos (notas aparte).")
print("• Sesgo potencial: acceso privilegiado a la facción académico-ONG.")
print("• Triangulación recomendada con actas oficiales (análisis de contenido).")
print("="*72)
