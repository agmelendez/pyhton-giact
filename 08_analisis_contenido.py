# -*- coding: utf-8 -*-
"""
================================================================================
LABORATORIO 08 — REVISIÓN DOCUMENTAL Y ANÁLISIS DE CONTENIDO
Gestión Marino-Costera | Métodos Cualitativos con Python
--------------------------------------------------------------------------------
Objetivo: simular un corpus documental costero (planes de manejo, leyes,
prensa, informes técnicos), aplicar TF-IDF, modelado temático LDA, análisis
de encuadre (conservación vs. desarrollo), y lectura diacrónica de discurso
dominante a lo largo de 20 años.

Referencias: Krippendorff (2019) Content Analysis; Blei et al. (2003) LDA;
Entman (1993) Framing; Hajer (1995) discourse analysis.
================================================================================
"""
import subprocess, sys
def _pip(pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)
_pip(["numpy","pandas","matplotlib","scikit-learn"])

import numpy as np, pandas as pd, random
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

SEED = 2026; random.seed(SEED); np.random.seed(SEED)

# ============================================================
# 1. GENERACIÓN DEL CORPUS — 60 documentos (2005-2026)
# ============================================================
TIPOS = ["plan_manejo","decreto","noticia_prensa","informe_ONG","tesis_academica"]

FRAGMENTOS = {
    "conservacion": [
        "protección del manglar y la biodiversidad costera",
        "restauración de humedales degradados",
        "creación de áreas marinas protegidas responsables",
        "conservación de especies bandera como la tortuga baula",
        "enfoque ecosistémico del manejo marino",
        "vedas estacionales para la recuperación del recurso",
    ],
    "desarrollo": [
        "crecimiento de la inversión hotelera en el litoral",
        "desarrollo de infraestructura portuaria moderna",
        "maricultura intensiva para exportación",
        "zonas francas en la costa para atraer capital",
        "turismo de alto valor agregado internacional",
        "rentabilidad del sector pesca industrial",
    ],
    "comunitario": [
        "participación de las comunidades pesqueras tradicionales",
        "conocimiento local y saberes ancestrales del mar",
        "consulta previa libre e informada a los pescadores",
        "derechos de las mujeres piangüeras del estero",
        "gestión comunitaria de los recursos marinos",
        "equidad territorial y justicia ambiental costera",
    ],
    "tecnico": [
        "capacidad de carga del ecosistema marino",
        "indicadores de calidad de agua costera",
        "modelado hidrodinámico de corrientes",
        "monitoreo satelital de la clorofila",
        "evaluación cuantitativa del stock pesquero",
        "análisis de riesgo por cambio climático",
    ],
}
# Evolución histórica del encuadre dominante (hipótesis)
# 2005-2010: desarrollo alto; 2011-2016: conservación sube; 2017-2026: comunitario fuerte
def pesos_ano(ano):
    if ano <= 2010: return {"desarrollo":0.45,"conservacion":0.25,"comunitario":0.10,"tecnico":0.20}
    elif ano <= 2016: return {"desarrollo":0.30,"conservacion":0.35,"comunitario":0.15,"tecnico":0.20}
    else:             return {"desarrollo":0.20,"conservacion":0.30,"comunitario":0.30,"tecnico":0.20}

docs = []
for i in range(60):
    ano = random.randint(2005, 2026)
    tipo = random.choice(TIPOS)
    pesos = pesos_ano(ano)
    n_frag = random.randint(8, 14)
    categorias = list(pesos.keys())
    probs = list(pesos.values())
    texto = " ".join(random.choice(FRAGMENTOS[np.random.choice(categorias, p=probs)])
                      for _ in range(n_frag))
    docs.append({"doc_id": f"D{i+1:03d}", "ano": ano, "tipo": tipo, "texto": texto})
df = pd.DataFrame(docs)
print(f"[CORPUS] {len(df)} documentos entre {df.ano.min()} y {df.ano.max()}, "
      f"{df.tipo.nunique()} tipologías.\n")

# ============================================================
# 2. TF-IDF — términos distintivos por tipo documental
# ============================================================
vect = TfidfVectorizer(max_features=50, ngram_range=(1,2), min_df=3)
X = vect.fit_transform(df["texto"])
terminos = vect.get_feature_names_out()
print("[TF-IDF] términos distintivos por tipo documental (top 6):")
for tipo in TIPOS:
    mask = (df["tipo"] == tipo).values
    if mask.sum() == 0: continue
    medias = np.asarray(X[mask].mean(axis=0)).flatten()
    top = medias.argsort()[::-1][:6]
    print(f"  {tipo:<18s}: {', '.join(terminos[top])}")
print()

# ============================================================
# 3. MODELADO TEMÁTICO LDA (k=4 tópicos latentes)
# ============================================================
cv = CountVectorizer(max_features=60, ngram_range=(1,2), min_df=3)
Xc = cv.fit_transform(df["texto"])
lda = LatentDirichletAllocation(n_components=4, random_state=SEED, max_iter=30)
doc_topic = lda.fit_transform(Xc)
terminos_cv = cv.get_feature_names_out()
print("[LDA — 4 tópicos latentes]")
etiquetas_topico = []
for k, comp in enumerate(lda.components_):
    top = comp.argsort()[::-1][:6]
    palabras = [terminos_cv[i] for i in top]
    print(f"  Tópico {k}: {', '.join(palabras)}")
    etiquetas_topico.append(f"T{k}: {palabras[0]}")
print()

df_topic = pd.DataFrame(doc_topic, columns=etiquetas_topico)
df = pd.concat([df.reset_index(drop=True), df_topic], axis=1)

# ============================================================
# 4. ANÁLISIS DE ENCUADRE DIACRÓNICO
#    Diccionario de encuadres → proporción de términos por año.
# ============================================================
ENCUADRES = {
    "CONSERVACIÓN": ["protección","manglar","biodiversidad","restauración","tortuga",
                      "protegidas","veda","conservación","ecosistémico"],
    "DESARROLLO":   ["crecimiento","inversión","infraestructura","portuaria","maricultura",
                      "zonas francas","turismo","rentabilidad","industrial"],
    "COMUNITARIO":  ["comunidades","conocimiento local","consulta","derechos",
                      "mujeres","saberes","equidad","justicia"],
}
def contar(texto, lista):
    return sum(texto.count(k) for k in lista)

for enc, lex in ENCUADRES.items():
    df[f"score_{enc}"] = df["texto"].apply(lambda t: contar(t, lex))

serie = df.groupby("ano")[[f"score_{e}" for e in ENCUADRES]].mean()
# Normalización fila a fila (proporciones)
serie_n = serie.div(serie.sum(axis=1), axis=0).fillna(0)
print("[ENCUADRE DISCURSIVO POR AÑO — proporciones]")
print(serie_n.round(3).to_string(), "\n")

# ============================================================
# 5. VISUALIZACIÓN
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Panel 1: evolución del encuadre
ax = axes[0]
for enc, color in zip(ENCUADRES, ["#27AE60","#C0392B","#3498DB"]):
    ax.plot(serie_n.index, serie_n[f"score_{enc}"], "-o", label=enc, color=color, linewidth=2)
ax.set_title("Evolución diacrónica del encuadre discursivo (2005-2026)", weight="bold")
ax.set_xlabel("Año"); ax.set_ylabel("Proporción del discurso")
ax.legend(); ax.grid(alpha=0.3)

# Panel 2: distribución de tópicos LDA por tipo
ax = axes[1]
topicos_por_tipo = df.groupby("tipo")[etiquetas_topico].mean()
topicos_por_tipo.plot(kind="bar", stacked=True, ax=ax, colormap="viridis", width=0.7)
ax.set_title("Mezcla temática LDA por tipo documental", weight="bold")
ax.set_xlabel(""); ax.set_ylabel("Proporción tópica")
ax.legend(fontsize=7, loc="center left", bbox_to_anchor=(1, 0.5))
plt.xticks(rotation=30, ha="right")
plt.tight_layout(); plt.savefig("lab08_contenido.png", dpi=130, bbox_inches="tight"); plt.show()

# ============================================================
# 6. EXPORTAR CORPUS CODIFICADO
# ============================================================
df.to_csv("lab08_corpus_codificado.csv", index=False)
print("[EXPORTADO] lab08_corpus_codificado.csv (incluye scores de encuadre y mezcla LDA).\n")
print("="*72)
print("SÍNTESIS: El análisis de encuadre revela el desplazamiento discursivo")
print("desde 'desarrollo' (dominante 2005-2010) hacia 'comunitario/conservación'")
print("(dominante post-2017). Este giro es simultáneo a la consolidación de la")
print("agenda de justicia ambiental en la política pública marino-costera de CR.")
print("="*72)
