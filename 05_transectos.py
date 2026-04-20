# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 05 — TRANSECTOS CAMINADOS / NAVEGADOS
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Objetivo: simular un recorrido costero de 5 km con waypoints cada 250 m,
combinar variables ambientales cuantitativas (salinidad, turbidez, cobertura
de manglar) con observaciones cualitativas in-situ del guía local, detectar
quiebres espaciales (changepoints) y superponer las dos capas narrativas.

Referencias: Chambers (1994) PRA; Gillies & Macdonald (2018) transect walks;
Killick & Eckley (2014) PELT changepoint detection.
================================================================================
"""
import subprocess, sys
def _pip(pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)
_pip(["numpy","pandas","matplotlib","ruptures"])

import numpy as np, pandas as pd, random
import matplotlib.pyplot as plt
import ruptures as rpt

SEED = 2026; random.seed(SEED); np.random.seed(SEED)

# ============================================================
# 1. DISEÑO DEL TRANSECTO — 5 km, waypoints cada 250 m
# ============================================================
LONGITUD_KM = 5.0
PASO_KM    = 0.25
N = int(LONGITUD_KM / PASO_KM) + 1
distancias = np.linspace(0, LONGITUD_KM, N)

# ============================================================
# 2. VARIABLES AMBIENTALES SIMULADAS
#    El transecto cruza: (0-1.5km) manglar prístino → (1.5-3km) transición →
#    (3-4.2km) zona degradada por camaronera → (4.2-5km) estuario recuperado.
# ============================================================
def zona(d):
    if d < 1.5: return "manglar_pristino"
    elif d < 3.0: return "transicion"
    elif d < 4.2: return "degradado_camaronera"
    else: return "estuario_recuperado"

zonas = [zona(d) for d in distancias]

base_sal = {"manglar_pristino":22, "transicion":26, "degradado_camaronera":33, "estuario_recuperado":25}
base_tur = {"manglar_pristino":5,  "transicion":15, "degradado_camaronera":45, "estuario_recuperado":12}
base_man = {"manglar_pristino":85, "transicion":55, "degradado_camaronera":10, "estuario_recuperado":40}

salinidad = np.array([base_sal[z] + np.random.normal(0, 1.5) for z in zonas])
turbidez  = np.array([base_tur[z] + np.random.normal(0, 3.0) for z in zonas])
cob_mang  = np.clip([base_man[z] + np.random.normal(0, 5) for z in zonas], 0, 100)

# ============================================================
# 3. OBSERVACIONES CUALITATIVAS IN-SITU (narrativa del guía local)
# ============================================================
OBS = {
    "manglar_pristino": [
        "el manglar está sano, se ven cangrejos",
        "aquí hay pianguas grandes todavía",
        "los abuelos pescaban aquí mismo con atarraya"],
    "transicion": [
        "por acá antes era puro mangle, mira los troncos",
        "el agua ya no baja tan limpia en invierno",
        "la orilla se está comiendo la tierra"],
    "degradado_camaronera": [
        "aquí tumbaron todo para poner la camaronera",
        "el agua sale salada y sucia al estero",
        "ya no hay pianguas desde que cerraron el canal natural",
        "los niños no deben meterse en esta agua"],
    "estuario_recuperado": [
        "la asociación resembró este tramo hace 6 años",
        "está volviendo la garza rosada, buena señal",
        "ya empezamos a ver camarón otra vez"],
}
observaciones = [random.choice(OBS[z]) for z in zonas]

# Eventos puntuales destacados (hallazgos clave)
eventos = [
    (1.25, "MOJÓN COMUNITARIO — límite zona de no-entrada acordado 2023"),
    (3.10, "DESCARGA DE CAMARONERA — espuma visible, olor a amoníaco"),
    (3.85, "RESTO DE TORTUGA VARADA — hembra, carapacho ~70 cm"),
    (4.55, "VIVERO DE MANGLE — sembrado por mujeres ADIRSi, oct 2019"),
]

df = pd.DataFrame({
    "km": distancias, "zona_ecologica": zonas,
    "salinidad_ppt": salinidad.round(1),
    "turbidez_NTU":  turbidez.round(1),
    "cobertura_manglar_%": cob_mang.round(0),
    "observacion_guia": observaciones,
})
print(f"[DATOS] Transecto de {LONGITUD_KM} km, {N} waypoints, 4 eventos destacados.\n")
print(df.head(5).to_string(index=False), "\n")

# ============================================================
# 4. DETECCIÓN DE CHANGEPOINTS (quiebres ambientales)
#    Señal = z-score combinado de salinidad + turbidez - cob_manglar.
# ============================================================
signal = ((salinidad - salinidad.mean())/salinidad.std()
        + (turbidez  - turbidez.mean()) /turbidez.std()
        - (cob_mang  - cob_mang.mean()) /cob_mang.std())

algo = rpt.Pelt(model="rbf", min_size=2).fit(signal.reshape(-1,1))
bkps = algo.predict(pen=3)
print(f"[CHANGEPOINTS] Detectados en waypoints índice: {bkps[:-1]} "
      f"(km ≈ {[round(distancias[i],2) for i in bkps[:-1]]})\n")

# ============================================================
# 5. VISUALIZACIÓN — 3 paneles alineados
# ============================================================
fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# (a) Variables ambientales
ax = axes[0]
ax.plot(distancias, salinidad, "-o", label="Salinidad (ppt)", color="#1F6FB2")
ax.plot(distancias, turbidez,  "-s", label="Turbidez (NTU)",  color="#C0392B")
ax.set_ylabel("Salinidad / Turbidez")
ax.legend(loc="upper left"); ax.grid(alpha=0.3)
ax2 = ax.twinx()
ax2.fill_between(distancias, cob_mang, alpha=0.2, color="#27AE60", label="Manglar %")
ax2.set_ylabel("Cobertura manglar (%)", color="#27AE60")
ax.set_title("Transecto ambiental con changepoints (líneas verticales)", weight="bold")
for bk in bkps[:-1]:
    ax.axvline(distancias[bk], color="red", linestyle="--", alpha=0.7)

# (b) Zonas ecológicas
ax = axes[1]
colores_z = {"manglar_pristino":"#27AE60","transicion":"#F1C40F",
             "degradado_camaronera":"#C0392B","estuario_recuperado":"#3498DB"}
for i, (d, z) in enumerate(zip(distancias, zonas)):
    ax.barh(0, PASO_KM, left=d, color=colores_z[z], edgecolor="white")
ax.set_yticks([]); ax.set_xlabel("")
# Leyenda
for z, c in colores_z.items():
    ax.plot([], [], "s", color=c, label=z, markersize=12)
ax.legend(loc="upper right", fontsize=8); ax.set_title("Segmentación ecológica cualitativa", weight="bold")

# (c) Eventos comunitarios
ax = axes[2]
ax.scatter([e[0] for e in eventos], [1]*len(eventos), s=200, c="#8E44AD", zorder=3)
for km, txt in eventos:
    ax.annotate(txt, (km, 1), xytext=(0, 15), textcoords="offset points",
                fontsize=7, ha="center", rotation=20)
ax.set_ylim(0.5, 1.8); ax.set_yticks([])
ax.set_xlabel("Distancia recorrida (km)")
ax.set_title("Eventos y observaciones clave del guía local", weight="bold")
ax.grid(alpha=0.3, axis="x")
plt.tight_layout(); plt.savefig("lab05_transecto.png", dpi=130, bbox_inches="tight"); plt.show()

# ============================================================
# 6. EXPORTAR DIARIO DE CAMPO
# ============================================================
df.to_csv("lab05_diario_campo.csv", index=False)
print("[EXPORTADO] lab05_diario_campo.csv (protocolo de cuaderno de campo).\n")
print("="*72)
print("SÍNTESIS: Los changepoints físicos coinciden con fronteras narrativas del")
print("guía local (validación etnográfica del dato). La 'degradación camaronera'")
print("emerge tanto en el z-score ambiental como en el discurso del actor.")
print("="*72)
