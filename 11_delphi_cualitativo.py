# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 11 — MÉTODO DELPHI CUALITATIVO
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Objetivo: simular un panel Delphi de 15 expertos/as (academia, gobierno,
pesca, conservación) que priorizan 12 problemas críticos del manejo costero
a lo largo de 3 rondas iterativas. Medir consenso con Kendall's W, estabilidad
de rankings (correlación de Spearman entre rondas), reducción del IQR y
criterios de parada empíricos.

Referencias: Dalkey & Helmer (1963) foundational; Hasson et al. (2000)
research guidelines; Diamond et al. (2014) reporting standards;
Schmidt (1997) managing Delphi studies.
================================================================================
"""
import subprocess, sys
def _pip(pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)
_pip(["numpy","pandas","matplotlib","scipy"])

import numpy as np, pandas as pd, random
import matplotlib.pyplot as plt
from scipy import stats

SEED = 2026; random.seed(SEED); np.random.seed(SEED)

# ============================================================
# 1. PANEL Y PROBLEMAS CRÍTICOS
# ============================================================
SECTORES = ["academia","gobierno","pesca","conservacion","privado"]
EXPERTOS = []
for i in range(15):
    EXPERTOS.append({"id": f"E{i+1:02d}",
                     "sector": random.choice(SECTORES),
                     "anos_experiencia": random.randint(8, 35)})
df_expertos = pd.DataFrame(EXPERTOS)
print(f"[PANEL] N={len(df_expertos)} expertos.")
print(df_expertos["sector"].value_counts().to_string(), "\n")

PROBLEMAS = [
    "P01_Pesca_ilegal_arrastre",
    "P02_Descargas_aguas_residuales",
    "P03_Erosion_costera_climatica",
    "P04_Plasticos_marinos",
    "P05_Perdida_manglar",
    "P06_Sobrepesca_artesanal",
    "P07_Conflicto_turismo_comunidad",
    "P08_Debilidad_fiscalizacion",
    "P09_Cambio_uso_suelo",
    "P10_Falta_conocimiento_cientifico",
    "P11_Inequidad_genero_pesca",
    "P12_Especies_invasoras",
]
K = len(PROBLEMAS)

# ============================================================
# 2. RONDA 1 — valoración individual (escala 1-10 de importancia)
#    Cada experto tiene un sesgo sectorial leve.
# ============================================================
SESGO = {
    "academia":     {"P10_Falta_conocimiento_cientifico": +1.5},
    "gobierno":     {"P08_Debilidad_fiscalizacion": +1.2, "P09_Cambio_uso_suelo": +1.0},
    "pesca":        {"P01_Pesca_ilegal_arrastre": +1.5, "P06_Sobrepesca_artesanal": -1.0},
    "conservacion": {"P05_Perdida_manglar": +1.2, "P04_Plasticos_marinos": +1.0},
    "privado":      {"P07_Conflicto_turismo_comunidad": -1.2},
}
def valorar(experto, ronda, valores_previos=None, ruido_ronda=None):
    """Ronda 1: valoración base + sesgo + ruido alto.
       Rondas 2/3: el experto acerca su valor al mediano grupal (convergencia)."""
    valores = {}
    for p in PROBLEMAS:
        base = np.random.normal(6, 1.5)
        adj = SESGO[experto["sector"]].get(p, 0)
        valores[p] = base + adj + np.random.normal(0, ruido_ronda)
    if valores_previos is not None:
        # Ajuste hacia la mediana grupal (factor de convergencia)
        for p in PROBLEMAS:
            valores[p] = 0.6*valores[p] + 0.4*valores_previos[p]
    return {p: float(np.clip(v, 1, 10)) for p, v in valores.items()}

def ejecutar_ronda(medianas_previas=None, ruido=None):
    datos = []
    for _, e in df_expertos.iterrows():
        v = valorar(e, None, medianas_previas, ruido)
        v.update({"experto": e["id"], "sector": e["sector"]})
        datos.append(v)
    return pd.DataFrame(datos)

# Ejecutar 3 rondas
r1 = ejecutar_ronda(medianas_previas=None, ruido=2.0)
med1 = r1[PROBLEMAS].median()
r2 = ejecutar_ronda(medianas_previas=med1.to_dict(), ruido=1.2)
med2 = r2[PROBLEMAS].median()
r3 = ejecutar_ronda(medianas_previas=med2.to_dict(), ruido=0.7)
med3 = r3[PROBLEMAS].median()
rondas = {"R1": r1, "R2": r2, "R3": r3}

# ============================================================
# 3. KENDALL'S W (CONCORDANCIA ENTRE EVALUADORES POR RONDA)
#    W cercano a 1 = consenso total; W < 0.3 = débil.
# ============================================================
def kendall_w(df_valores):
    X = df_valores[PROBLEMAS].rank(axis=1).values   # ranks dentro de cada experto
    m = X.shape[0]; n = X.shape[1]
    Rj = X.sum(axis=0)
    S  = ((Rj - Rj.mean())**2).sum()
    W  = 12*S / (m**2 * (n**3 - n))
    # Prueba de chi2
    chi2 = m*(n-1)*W
    pval = 1 - stats.chi2.cdf(chi2, df=n-1)
    return W, chi2, pval

print("[KENDALL'S W — concordancia por ronda]")
Ws = {}
for nombre, df_r in rondas.items():
    W, chi2, pval = kendall_w(df_r)
    Ws[nombre] = W
    print(f"  {nombre}: W={W:.3f}  chi²={chi2:.1f}  p={pval:.4f}")
print()

# ============================================================
# 4. ESTABILIDAD DE RANKINGS (Spearman entre rondas)
#    Criterio de parada: ρ > 0.90 entre dos rondas consecutivas.
# ============================================================
rk1 = med1.rank(); rk2 = med2.rank(); rk3 = med3.rank()
rho_12, _ = stats.spearmanr(rk1, rk2)
rho_23, _ = stats.spearmanr(rk2, rk3)
print(f"[ESTABILIDAD]  Spearman ρ(R1,R2)={rho_12:.3f}   ρ(R2,R3)={rho_23:.3f}")
if rho_23 > 0.90:
    print("  → Criterio de parada alcanzado: rankings estabilizados.\n")
else:
    print("  → Se recomienda una 4ª ronda.\n")

# ============================================================
# 5. REDUCCIÓN DEL IQR (dispersión del panel)
# ============================================================
iqr = pd.DataFrame({
    n: d[PROBLEMAS].quantile(0.75) - d[PROBLEMAS].quantile(0.25)
    for n, d in rondas.items()
})
print("[IQR POR PROBLEMA Y RONDA — reducción = convergencia]")
print(iqr.round(2).to_string(), "\n")

# ============================================================
# 6. RANKING FINAL Y CLASIFICACIÓN DE CONSENSO
# ============================================================
final = pd.DataFrame({"mediana_R3": med3, "IQR_R3": iqr["R3"]})
final["consenso"] = np.where(final["IQR_R3"] <= 1.5, "✓ FUERTE",
                      np.where(final["IQR_R3"] <= 2.5, "~ MODERADO", "✗ BAJO"))
final = final.sort_values("mediana_R3", ascending=False)
print("[RANKING FINAL DE PRIORIDADES — R3]")
print(final.round(2).to_string(), "\n")

# ============================================================
# 7. VISUALIZACIÓN
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 11))

# (1) Evolución mediana por problema
ax = axes[0, 0]
df_med = pd.DataFrame({"R1":med1, "R2":med2, "R3":med3})
for p in PROBLEMAS:
    ax.plot([1,2,3], df_med.loc[p].values, "-o", alpha=0.7, label=p if df_med.loc[p].mean()>7 else None)
ax.set_xticks([1,2,3]); ax.set_xticklabels(["R1","R2","R3"])
ax.set_title("Evolución de la mediana por problema", weight="bold")
ax.set_ylabel("Importancia (1-10)"); ax.legend(fontsize=6, loc="lower right")
ax.grid(alpha=0.3)

# (2) Kendall's W por ronda
ax = axes[0, 1]
ax.bar(Ws.keys(), Ws.values(), color=["#F39C12","#27AE60","#2980B9"])
ax.axhline(0.5, color="red", linestyle="--", label="umbral consenso moderado")
ax.axhline(0.7, color="darkred", linestyle="--", label="umbral consenso fuerte")
ax.set_title("Kendall's W por ronda (concordancia del panel)", weight="bold")
ax.set_ylabel("W"); ax.set_ylim(0, 1); ax.legend(fontsize=8)

# (3) Reducción del IQR
ax = axes[1, 0]
iqr.T.plot(ax=ax, legend=False, linewidth=2, alpha=0.6)
ax.set_title("Reducción de IQR por problema (convergencia)", weight="bold")
ax.set_ylabel("IQR"); ax.set_xlabel("Ronda"); ax.grid(alpha=0.3)

# (4) Ranking final con marca de consenso
ax = axes[1, 1]
colors = {"✓ FUERTE":"#27AE60", "~ MODERADO":"#F39C12", "✗ BAJO":"#C0392B"}
ax.barh(final.index[::-1], final["mediana_R3"].values[::-1],
        color=[colors[c] for c in final["consenso"].values[::-1]])
ax.set_title("Ranking final de prioridades (color = nivel de consenso)", weight="bold")
ax.set_xlabel("Mediana R3"); ax.grid(alpha=0.3, axis="x")
# Leyenda manual
import matplotlib.patches as mpatches
ax.legend(handles=[mpatches.Patch(color=c, label=k) for k, c in colors.items()],
          loc="lower right", fontsize=8)

plt.tight_layout(); plt.savefig("lab11_delphi.png", dpi=130, bbox_inches="tight"); plt.show()

final.to_csv("lab11_ranking_delphi.csv")
print("[EXPORTADO] lab11_ranking_delphi.csv\n")
print("="*72)
print("SÍNTESIS: El Delphi cualitativo permite agregar juicio experto heterogéneo")
print("respetando la anonimidad (evita dominación de voces fuertes). Los problemas")
print("con consenso FUERTE y alta mediana R3 son candidatos a política prioritaria;")
print("los de consenso BAJO revelan disenso estructural que requiere deliberación.")
print("="*72)
