# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 04 — MAPEO PARTICIPATIVO (CARTOGRAFÍA SOCIAL)
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Objetivo: simular polígonos/puntos que actores locales dibujan sobre el litoral
(zonas de pesca, turismo, sitios sagrados, conflicto), estimar densidad (KDE),
identificar ZONAS GRISES de conflicto por superposición e implementar mapa
interactivo en Folium.

Referencias: Chambers (2006) PRA; McCall (2021) Participatory GIS;
Brown & Fagerholm (2015) Public Participation GIS.
================================================================================
"""
import subprocess, sys
def _pip(pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)
_pip(["numpy", "pandas", "matplotlib", "scipy", "folium"])

import numpy as np, pandas as pd, random
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import folium
from folium.plugins import HeatMap

SEED = 2026; random.seed(SEED); np.random.seed(SEED)

# ============================================================
# 1. MARCO ESPACIAL — Costa simulada del Golfo de Nicoya, C.R.
# ============================================================
# Bounding box aproximado (lat, lon) del Golfo de Nicoya
LAT_MIN, LAT_MAX = 9.70, 10.15
LON_MIN, LON_MAX = -85.10, -84.70
CENTRO = [(LAT_MIN+LAT_MAX)/2, (LON_MIN+LON_MAX)/2]

USOS = ["pesca_artesanal","turismo_hotel","sitio_sagrado","conflicto","conservacion"]
COLORES = {"pesca_artesanal":"#1F6FB2","turismo_hotel":"#D9662C",
           "sitio_sagrado":"#8E44AD","conflicto":"#C0392B","conservacion":"#27AE60"}

# ============================================================
# 2. SIMULACIÓN DE PUNTOS DIBUJADOS POR ACTORES
#    Cada uso tiene "focos" espaciales (bancos, playas, manglares).
# ============================================================
FOCOS = {
    "pesca_artesanal":  [(9.85, -85.00), (9.95, -84.88), (10.05, -84.80)],
    "turismo_hotel":    [(9.75, -85.05), (9.90, -84.85)],
    "sitio_sagrado":    [(9.80, -85.02)],
    "conflicto":        [(9.90, -84.86), (9.76, -85.04)],
    "conservacion":     [(10.05, -84.80), (9.82, -85.00)],
}
N_PUNTOS = {"pesca_artesanal":60,"turismo_hotel":35,"sitio_sagrado":12,
            "conflicto":25,"conservacion":40}

filas = []
for uso, n in N_PUNTOS.items():
    for _ in range(n):
        foco = random.choice(FOCOS[uso])
        lat = np.clip(np.random.normal(foco[0], 0.025), LAT_MIN, LAT_MAX)
        lon = np.clip(np.random.normal(foco[1], 0.025), LON_MIN, LON_MAX)
        filas.append({"uso": uso, "lat": lat, "lon": lon,
                      "actor_id": f"A{random.randint(1,20):02d}",
                      "intensidad": random.randint(1,5)})
df = pd.DataFrame(filas)
print(f"[DATOS] {len(df)} puntos dibujados por {df.actor_id.nunique()} actores, {len(USOS)} usos.\n")
print(df.groupby("uso").size().rename("n").to_string(), "\n")

# ============================================================
# 3. KERNEL DENSITY ESTIMATION POR USO
# ============================================================
def kde_grid(lats, lons, nx=60, ny=60):
    xx, yy = np.mgrid[LON_MIN:LON_MAX:complex(0, nx),
                      LAT_MIN:LAT_MAX:complex(0, ny)]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    values    = np.vstack([lons, lats])
    kernel    = gaussian_kde(values, bw_method=0.30)
    Z = np.reshape(kernel(positions).T, xx.shape)
    return xx, yy, Z

kdes = {}
for uso in USOS:
    sub = df[df.uso == uso]
    if len(sub) >= 3:
        kdes[uso] = kde_grid(sub.lat.values, sub.lon.values)

# ============================================================
# 4. DETECCIÓN DE ZONAS DE CONFLICTO
#    Superposición alta de pesca_artesanal ∩ turismo_hotel.
# ============================================================
xx, yy, Z_pesca   = kdes["pesca_artesanal"]
_,  _,  Z_turismo = kdes["turismo_hotel"]
Z_norm_p = Z_pesca   / Z_pesca.max()
Z_norm_t = Z_turismo / Z_turismo.max()
Z_conflicto = np.minimum(Z_norm_p, Z_norm_t)   # ambos usos intensos = conflicto

umbral = 0.50
celdas_conflicto = (Z_conflicto > umbral).sum()
total = Z_conflicto.size
print(f"[SUPERPOSICIÓN] Celdas con conflicto pesca↔turismo (>{umbral}): "
      f"{celdas_conflicto}/{total} ({100*celdas_conflicto/total:.1f}%)\n")

# ============================================================
# 5. VISUALIZACIÓN ESTÁTICA — 4 paneles
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 11))

# Panel 1: Todos los puntos
ax = axes[0, 0]
for uso in USOS:
    sub = df[df.uso == uso]
    ax.scatter(sub.lon, sub.lat, c=COLORES[uso], label=uso, s=30, alpha=0.7, edgecolor="white")
ax.set_title("Cartografía social: usos declarados", weight="bold")
ax.set_xlabel("Longitud"); ax.set_ylabel("Latitud"); ax.legend(fontsize=8, loc="best")
ax.grid(alpha=0.3)

# Panel 2: KDE pesca
ax = axes[0, 1]
ax.contourf(xx, yy, Z_pesca, levels=15, cmap="Blues")
ax.scatter(df[df.uso=="pesca_artesanal"].lon, df[df.uso=="pesca_artesanal"].lat,
           s=10, c="navy", alpha=0.4)
ax.set_title("Densidad de zonas de pesca artesanal (KDE)", weight="bold")

# Panel 3: KDE turismo
ax = axes[1, 0]
ax.contourf(xx, yy, Z_turismo, levels=15, cmap="Oranges")
ax.scatter(df[df.uso=="turismo_hotel"].lon, df[df.uso=="turismo_hotel"].lat,
           s=10, c="darkred", alpha=0.4)
ax.set_title("Densidad de uso turístico (KDE)", weight="bold")

# Panel 4: Zonas de conflicto
ax = axes[1, 1]
cs = ax.contourf(xx, yy, Z_conflicto, levels=15, cmap="RdPu")
ax.contour(xx, yy, Z_conflicto, levels=[umbral], colors="black", linewidths=2)
plt.colorbar(cs, ax=ax, label="Intensidad de conflicto normalizada")
ax.set_title(f"ZONAS GRISES de conflicto (umbral > {umbral})", weight="bold")
plt.tight_layout(); plt.savefig("lab04_mapeo.png", dpi=130, bbox_inches="tight"); plt.show()

# ============================================================
# 6. MAPA INTERACTIVO FOLIUM (se guarda como HTML navegable)
# ============================================================
m = folium.Map(location=CENTRO, zoom_start=11, tiles="OpenStreetMap")
for _, r in df.iterrows():
    folium.CircleMarker(location=[r.lat, r.lon], radius=3+r.intensidad,
                        color=COLORES[r.uso], fill=True, fill_opacity=0.6,
                        popup=f"{r.uso} (int={r.intensidad})").add_to(m)
# Heatmap de conflicto
heat_pts = df[df.uso=="conflicto"][["lat","lon"]].values.tolist()
HeatMap(heat_pts, radius=25).add_to(folium.FeatureGroup(name="Conflicto").add_to(m))
folium.LayerControl().add_to(m)
m.save("lab04_mapa_interactivo.html")
print("[MAPA] Exportado: lab04_mapa_interactivo.html (abrir en navegador).\n")

print("="*72)
print("SÍNTESIS: Las zonas grises identificadas requieren mesas de concertación")
print("multi-actor. El KDE no reemplaza la validación comunitaria: los polígonos")
print("deben retornar a los dibujantes para 'ground-truthing' (McCall, 2021).")
print("="*72)
