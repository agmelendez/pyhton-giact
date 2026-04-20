# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 03 — ENCUESTAS DE PERCEPCIÓN
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Objetivo: simular encuesta mixta (ítems Likert + preguntas abiertas),
calcular Alfa de Cronbach por dimensión, realizar Análisis Factorial
Exploratorio, codificar respuestas abiertas, y construir matriz
Importancia-Desempeño (IPA) para priorización de intervenciones.

Referencias: Tavakol & Dennick (2011) Cronbach's α; Hair et al. (2019) EFA;
Martilla & James (1977) Importance-Performance Analysis.
================================================================================
"""
import subprocess, sys
def _pip(pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)
_pip(["numpy", "pandas", "matplotlib", "scikit-learn", "scipy"])

import numpy as np, pandas as pd, random
import matplotlib.pyplot as plt
from sklearn.decomposition import FactorAnalysis
from scipy.stats import pearsonr

SEED = 2026; random.seed(SEED); np.random.seed(SEED)

# ============================================================
# 1. GENERACIÓN — Encuesta a N=400 residentes costeros
#    5 dimensiones x 4 ítems + 2 abiertas + IPA (importancia/desempeño)
# ============================================================
N = 400
DIMENSIONES = {
    "CALIDAD_AGUA":   ["el agua del mar está limpia","veo algas anormales","huelo mal olor en la costa","hay desechos visibles"],
    "GESTION_PUBLICA":["las autoridades responden","hay vigilancia efectiva","las normas se aplican","se consulta a la comunidad"],
    "RECURSO_PESQUERO":["hay suficiente pescado","las tallas son adecuadas","la veda funciona","se respetan las artes legales"],
    "TURISMO_SOSTENIBLE":["el turismo respeta la cultura","los hoteles cumplen normas","hay empleo local digno","se cuidan las playas"],
    "PARTICIPACION":  ["me invitan a decidir","conozco los planes","mi voz es escuchada","hay espacios reales de diálogo"],
}
# Perfiles latentes (5 clusters de residentes)
perfiles = np.random.choice(["optimista","crítico","ambivalente","desinformado","activista"],
                             size=N, p=[0.20, 0.30, 0.25, 0.15, 0.10])

def likert(perfil, dimension):
    """Respuesta 1–5 con estructura latente + ruido gaussiano (truncado)."""
    base = {"optimista":4.0,"crítico":2.0,"ambivalente":3.0,"desinformado":3.0,"activista":2.3}[perfil]
    # Las dimensiones 'críticas' bajan para el crítico/activista (coherencia factorial)
    ajuste = {"CALIDAD_AGUA":0,"GESTION_PUBLICA":-0.3,"RECURSO_PESQUERO":-0.1,
              "TURISMO_SOSTENIBLE":0.2,"PARTICIPACION":-0.2}[dimension]
    r = base + ajuste + np.random.normal(0, 0.7)
    return int(np.clip(round(r), 1, 5))

filas = []
for i in range(N):
    fila = {"ID": i+1, "perfil": perfiles[i],
            "edad": np.random.randint(18, 75),
            "sexo": np.random.choice(["F","M"], p=[0.52,0.48]),
            "zona": np.random.choice(["Pacifico_N","Pacifico_C","Pacifico_S","Caribe"])}
    for dim, items in DIMENSIONES.items():
        for k, it in enumerate(items):
            fila[f"{dim}_{k+1}"] = likert(perfiles[i], dim)
    # Respuesta abierta
    plantillas = {"optimista":"en general me siento satisfecho con la playa y las autoridades",
                  "crítico":"hay mucha basura y la municipalidad no hace nada efectivo",
                  "ambivalente":"algunas cosas mejoran pero otras empeoran con el tiempo",
                  "desinformado":"no sé bien qué está pasando con las normas de pesca",
                  "activista":"necesitamos que se escuche a la comunidad organizada ya"}
    fila["respuesta_abierta"] = plantillas[perfiles[i]]
    filas.append(fila)

df = pd.DataFrame(filas)
print(f"[DATOS] Encuesta simulada: N={N}, {len(DIMENSIONES)*4} ítems Likert + 1 abierta.\n")

# ============================================================
# 2. ALFA DE CRONBACH POR DIMENSIÓN
# ============================================================
def cronbach_alpha(items_df):
    k = items_df.shape[1]
    var_items = items_df.var(axis=0, ddof=1).sum()
    var_total = items_df.sum(axis=1).var(ddof=1)
    return (k/(k-1)) * (1 - var_items/var_total)

print("[FIABILIDAD — Alfa de Cronbach por dimensión]")
alphas = {}
for dim, items in DIMENSIONES.items():
    cols = [f"{dim}_{k+1}" for k in range(len(items))]
    alphas[dim] = cronbach_alpha(df[cols])
    estado = "✓ aceptable" if alphas[dim] >= 0.70 else "⚠ revisar ítems"
    print(f"  {dim:<22s} α = {alphas[dim]:.3f}  [{estado}]")
print()

# ============================================================
# 3. ANÁLISIS FACTORIAL EXPLORATORIO
# ============================================================
items_cols = [c for c in df.columns if any(c.startswith(d+"_") for d in DIMENSIONES)]
X = df[items_cols].values
fa = FactorAnalysis(n_components=5, rotation="varimax", random_state=SEED)
fa.fit(X)
loadings = pd.DataFrame(fa.components_.T, index=items_cols,
                        columns=[f"F{i+1}" for i in range(5)])
print("[AFE — cargas factoriales rotadas (|carga|>0.30 en negrita conceptual)]")
print(loadings.round(2), "\n")

# ============================================================
# 4. CODIFICACIÓN DE RESPUESTA ABIERTA (emula codificación temática)
# ============================================================
LEXICO = {"SATISFACCION":["satisfecho","bien","mejora"], "QUEJA":["basura","no hace","mala"],
          "AMBIVALENCIA":["algunas","pero","empeoran"], "DESCONOCIMIENTO":["no sé","no conozco"],
          "DEMANDA_PARTICIPATIVA":["escuche","comunidad","organizada","voz"]}
def codificar(txt):
    codigos = [c for c, kws in LEXICO.items() if any(k in txt for k in kws)]
    return codigos[0] if codigos else "OTRO"
df["codigo_abierta"] = df["respuesta_abierta"].apply(codificar)
print("[CODIFICACIÓN DE RESPUESTA ABIERTA]")
print(df["codigo_abierta"].value_counts().to_string(), "\n")

# ============================================================
# 5. MATRIZ IMPORTANCIA-DESEMPEÑO (IPA)
#    Importancia = |correlación| del ítem con satisfacción global (suma Likert)
#    Desempeño  = media del ítem
# ============================================================
df["satisfaccion_global"] = df[items_cols].mean(axis=1)
ipa = []
for dim, items in DIMENSIONES.items():
    col = f"{dim}_1"  # ítem representativo
    r, _ = pearsonr(df[col], df["satisfaccion_global"])
    ipa.append({"dimension": dim, "importancia": abs(r), "desempeno": df[col].mean()})
ipa_df = pd.DataFrame(ipa)
print("[MATRIZ IPA — diagnóstico estratégico]")
print(ipa_df.round(3).to_string(index=False), "\n")

# ============================================================
# 6. VISUALIZACIÓN
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Alfas
axes[0].barh(list(alphas.keys()), list(alphas.values()), color="#1F6FB2")
axes[0].axvline(0.70, color="red", linestyle="--", label="umbral α=0.70")
axes[0].set_title("Fiabilidad por dimensión (Cronbach α)", weight="bold")
axes[0].legend(); axes[0].grid(axis="x", alpha=0.3)

# Cuadrante IPA
ax = axes[1]
ax.scatter(ipa_df["desempeno"], ipa_df["importancia"], s=300, c="#D9662C", alpha=0.8, edgecolor="black")
for _, r in ipa_df.iterrows():
    ax.annotate(r["dimension"], (r["desempeno"], r["importancia"]),
                xytext=(5,5), textcoords="offset points", fontsize=8)
ax.axvline(ipa_df["desempeno"].mean(), color="gray", linestyle=":")
ax.axhline(ipa_df["importancia"].mean(), color="gray", linestyle=":")
ax.set_xlabel("Desempeño (media Likert)"); ax.set_ylabel("Importancia (|r| con satisfacción global)")
ax.set_title("Matriz Importancia-Desempeño (IPA)", weight="bold")
# Etiquetas de cuadrantes
ax.text(0.02, 0.98, "Concentrar esfuerzos", transform=ax.transAxes, fontsize=8, va="top", alpha=0.5)
ax.text(0.98, 0.98, "Mantener",            transform=ax.transAxes, fontsize=8, va="top", ha="right", alpha=0.5)
ax.text(0.02, 0.02, "Baja prioridad",      transform=ax.transAxes, fontsize=8, alpha=0.5)
ax.text(0.98, 0.02, "Posible sobreinversión", transform=ax.transAxes, fontsize=8, ha="right", alpha=0.5)
plt.tight_layout(); plt.savefig("lab03_encuesta.png", dpi=130, bbox_inches="tight"); plt.show()

print("="*72)
print("SÍNTESIS: Las dimensiones en cuadrante superior-izquierdo (alta importancia,")
print("bajo desempeño) son prioridades de política pública costera.")
print("="*72)
