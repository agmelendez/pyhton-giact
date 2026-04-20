# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 10 — RELATOS DE VIDA (HISTORIAS ORALES)
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Objetivo: simular historias de vida de pescadores y piangüeras mayores (n=10),
extraer eventos biográficos y ecológicos, construir líneas de tiempo
generacionales, detectar SHIFTING BASELINES (Pauly, 1995) en el conocimiento
ecológico tradicional y analizar la narrativa de cambio del ecosistema
a lo largo de 60 años.

Referencias: Pauly (1995) Shifting baselines; Bertaux (1981) biographies;
Berkes (2018) Sacred Ecology/TEK; Molnar et al. (2008) oral histories.
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
# 1. INFORMANTES — 10 relatos (nacidos 1945-1975)
# ============================================================
NOMBRES = [f"R{i:02d}" for i in range(1, 11)]
informantes = []
for n in NOMBRES:
    ano_nac = random.randint(1945, 1975)
    informantes.append({
        "informante": n,
        "ano_nacimiento": ano_nac,
        "edad_actual": 2026 - ano_nac,
        "sexo": random.choice(["F","M"]),
        "oficio": random.choice(["pescador","piangüera","pescador","buzo_artesanal"]),
        "zona": random.choice(["Golfo_Nicoya","Golfo_Dulce","Pacifico_Norte","Caribe_Sur"]),
    })
df_info = pd.DataFrame(informantes)
print("[INFORMANTES]")
print(df_info.to_string(index=False), "\n")

# ============================================================
# 2. EVENTOS BIOGRÁFICOS Y ECOLÓGICOS
#    Cada informante narra 10-18 eventos a lo largo de su vida.
# ============================================================
PLANTILLAS_BIO = [
    ("inicio_oficio",     "aprendí a pescar con mi padre"),
    ("matrimonio",        "me casé y formé familia aquí mismo en la costa"),
    ("migracion",         "me fui a trabajar al Pacífico Sur un tiempo"),
    ("retorno",           "volví al pueblo cuando murió mi padre"),
    ("liderazgo",         "fundé la asociación de pescadores de la zona"),
    ("lesion",            "tuve un accidente grave buceando"),
    ("jubilacion_parcial","ya no salgo todos los días, solo cuando hay buen tiempo"),
]
PLANTILLAS_ECO = [
    ("abundancia_historica","se sacaban cien pianguas grandes en una marea"),
    ("primera_disminucion","empezaron a no aparecer los camarones blancos"),
    ("cierre_banco",        "cerraron el banco de pepitona porque ya no había"),
    ("llegada_industrial",  "llegaron los barcos grandes y fue distinto"),
    ("extincion_local",     "ya no volvió a verse el pez sierra en el golfo"),
    ("restauracion",        "sembramos manglar y el camarón está volviendo"),
    ("evento_climatico",    "el Niño del 97 cambió todo el ecosistema"),
    ("contaminacion",       "se instaló la camaronera y el agua cambió"),
    ("especie_invasora",    "aparecieron los peces león en los arrecifes"),
    ("nueva_regulacion",    "vino la veda oficial y la gente no la acataba"),
]

eventos = []
for _, info in df_info.iterrows():
    # Edad mínima de evento = 12 años (inicio laboral); máxima = edad actual
    n_bio = random.randint(3, min(5, len(PLANTILLAS_BIO)))
    n_eco = random.randint(6, len(PLANTILLAS_ECO))  # máx = tamaño del banco
    for tipo, texto in random.sample(PLANTILLAS_BIO, n_bio):
        ano = info["ano_nacimiento"] + random.randint(12, info["edad_actual"])
        eventos.append({"informante":info["informante"], "ano":ano, "tipo":"bio",
                         "etiqueta":tipo, "narracion":texto,
                         "edad_informante":ano-info["ano_nacimiento"]})
    for tipo, texto in random.sample(PLANTILLAS_ECO, n_eco):
        ano = info["ano_nacimiento"] + random.randint(12, info["edad_actual"])
        eventos.append({"informante":info["informante"], "ano":ano, "tipo":"eco",
                         "etiqueta":tipo, "narracion":texto,
                         "edad_informante":ano-info["ano_nacimiento"]})
df_ev = pd.DataFrame(eventos).sort_values(["informante","ano"]).reset_index(drop=True)
print(f"[EVENTOS] {len(df_ev)} eventos narrados (bio+eco) entre {df_ev.ano.min()} y {df_ev.ano.max()}.\n")

# ============================================================
# 3. SHIFTING BASELINE SYNDROME
#    Para cada informante: percepción de "cantidad normal" de pianguas/día
#    a lo largo de cohortes. La hipótesis: cada generación normaliza un
#    nivel inferior al de la anterior.
# ============================================================
# Simulamos la baseline perceibida (depende de la edad del primer trabajo)
def baseline_perceibida(info):
    ano_inicio = info["ano_nacimiento"] + 14  # edad típica de inicio
    # Abundancia real objetiva (declina ~1.2% por año desde 1960)
    abundancia_real = 180 * np.exp(-0.012 * max(0, ano_inicio - 1960))
    # Lo que la persona recuerda como "normal" (perturbación modesta)
    return abundancia_real + np.random.normal(0, 15)

df_info["baseline_perceibida"] = df_info.apply(baseline_perceibida, axis=1)
df_info["cohorte"] = pd.cut(df_info["ano_nacimiento"],
                             bins=[1944,1955,1965,1975],
                             labels=["1945-1955","1956-1965","1966-1975"])
baseline_x_cohorte = df_info.groupby("cohorte", observed=True)["baseline_perceibida"].mean().round(1)
print("[SHIFTING BASELINE — pianguas/día percibidas como 'normal' por cohorte]")
print(baseline_x_cohorte.to_string(), "\n")

# Test de tendencia (Kendall τ entre año de nacimiento y baseline)
tau, pval = stats.kendalltau(df_info["ano_nacimiento"], df_info["baseline_perceibida"])
print(f"[KENDALL τ] año_nacimiento vs baseline_perceibida: τ={tau:.3f}, p={pval:.4f}")
if tau < -0.3 and pval < 0.05:
    print("  → Evidencia estadística de shifting baseline intergeneracional.\n")
else:
    print("  → Tendencia no concluyente (se requiere mayor n).\n")

# ============================================================
# 4. CATEGORIZACIÓN NARRATIVA POR DÉCADA
# ============================================================
df_ev["decada"] = (df_ev["ano"]//10)*10
por_decada = df_ev.groupby(["decada","etiqueta"]).size().unstack(fill_value=0)
print("[NARRATIVAS POR DÉCADA — eventos declarados]")
print(por_decada.to_string(), "\n")

# ============================================================
# 5. VISUALIZACIÓN
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 11))

# (1) Líneas de vida (timeline por informante)
ax = axes[0, 0]
for i, (_, info) in enumerate(df_info.iterrows()):
    ax.plot([info["ano_nacimiento"], 2026], [i, i], "-", color="lightgray", linewidth=1)
    ax.plot(info["ano_nacimiento"], i, "s", color="green", markersize=10)
    evs = df_ev[df_ev["informante"] == info["informante"]]
    bio = evs[evs["tipo"] == "bio"]; eco = evs[evs["tipo"] == "eco"]
    ax.scatter(bio["ano"], [i]*len(bio), color="#3498DB", s=45, alpha=0.8, label="bio" if i==0 else "")
    ax.scatter(eco["ano"], [i]*len(eco), color="#C0392B", s=45, alpha=0.8, marker="^", label="eco" if i==0 else "")
ax.set_yticks(range(len(df_info))); ax.set_yticklabels(df_info["informante"])
ax.set_xlabel("Año"); ax.set_title("Líneas de vida — eventos biográficos y ecológicos", weight="bold")
ax.legend(); ax.grid(alpha=0.3)

# (2) Shifting baseline
ax = axes[0, 1]
ax.scatter(df_info["ano_nacimiento"], df_info["baseline_perceibida"], s=100, color="#2E5C8A")
z = np.polyfit(df_info["ano_nacimiento"], df_info["baseline_perceibida"], 1)
xx = np.linspace(df_info["ano_nacimiento"].min(), df_info["ano_nacimiento"].max(), 50)
ax.plot(xx, z[0]*xx + z[1], "--", color="red", label=f"Tendencia (τ={tau:.2f})")
ax.set_title("Shifting Baseline: baseline de pianguas/día por año de nacimiento", weight="bold")
ax.set_xlabel("Año de nacimiento"); ax.set_ylabel("Pianguas/día percibidas como 'normales'")
ax.legend(); ax.grid(alpha=0.3)

# (3) Frecuencia de eventos ecológicos por década
ax = axes[1, 0]
eco_decada = df_ev[df_ev.tipo=="eco"].groupby(["decada","etiqueta"]).size().unstack(fill_value=0)
eco_decada.plot(kind="bar", stacked=True, ax=ax, colormap="tab20", width=0.8)
ax.set_title("Eventos ecológicos narrados por década", weight="bold")
ax.set_xlabel("Década"); ax.set_ylabel("Nº eventos")
ax.legend(fontsize=7, loc="center left", bbox_to_anchor=(1, 0.5))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)

# (4) Edad al narrar cada tipo de evento
ax = axes[1, 1]
data = [df_ev[df_ev.tipo==t]["edad_informante"].values for t in ["bio","eco"]]
ax.boxplot(data, labels=["Biográficos","Ecológicos"], patch_artist=True,
           boxprops=dict(facecolor="lightblue"))
ax.set_title("Edad del informante al momento del evento narrado", weight="bold")
ax.set_ylabel("Edad (años)"); ax.grid(alpha=0.3, axis="y")

plt.tight_layout(); plt.savefig("lab10_relatos_vida.png", dpi=130, bbox_inches="tight"); plt.show()

df_ev.to_csv("lab10_eventos_biograficos.csv", index=False)
print("[EXPORTADO] lab10_eventos_biograficos.csv\n")
print("="*72)
print("SÍNTESIS: Los relatos de vida permiten reconstruir una LÍNEA DE BASE")
print("HISTÓRICA del ecosistema que no aparece en registros oficiales. La")
print("detección del shifting baseline es crítica para no subestimar la")
print("magnitud de la degradación costera (Pauly, 1995).")
print("="*72)
