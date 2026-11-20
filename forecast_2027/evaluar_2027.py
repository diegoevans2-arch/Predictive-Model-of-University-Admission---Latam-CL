# -*- coding: utf-8 -*-
"""Evaluación del pronóstico 2027 según el protocolo congelado (protocolo_evaluacion_2027.md, versión 2.1).

Autocontenido: sólo usa pandas, numpy y scipy. Se congela junto con los pronósticos (huella en SHA256SUMS.txt).

Uso:
    python evaluar_2027.py --sies <archivo crudo de matrícula del SIES> --paquete <carpeta forecast_2027> \
                           --salida <carpeta de resultados> [--anio 2027]

Qué hace (secciones del protocolo):
  §2 Reconstruye la matrícula real del año a nivel de celda desde el archivo crudo del SIES con las reglas de
     ingesta: pregrado, universidades (CRUCH, privadas y carreras en convenio), formato largo por género y
     condición (nuevo = primer año; antiguo = total − primer año), suma por la llave de celda. Sin winsorizar.
     Registra la huella SHA-256 del archivo y el total universitario de pregrado (control contra el informe oficial).
  §3 Emparejamiento principal por la llave de celda con el nombre de la carrera; secundario por código de carrera
     (institución + carrera, como cod_carrera_base). Informa programas cerrados, nuevos y cobertura.
  §4 Métricas N1-N8 por suma ascendente: WAPE, RelMAE (MAE / MAE de F0), skill (1 − (RMSE/RMSE F0)²),
     % de grupos dentro de ±10 %, error agregado. Intervalos: cobertura con IC de Wilson al 95 %, ancho mediano,
     interval score (α = 0,10), MSIS (escalada por el MAE de F0) y la referencia de conformal sin estratos.
  §5 Hipótesis H1-H5 con DM entre grupos y error estándar robusto por clúster de institución (CR1), bilaterales,
     α = 0,05; pérdida principal absoluta, secundaria cuadrática. H2 también por condición en N8.
  §6 Criterios (versión 2.2): fracaso frente a la persistencia si RelMAE N8 >= 1. Bandas, criterio asimétrico sobre
     la cobertura en N8: subcobertura (fracaso) < 88 %; calibradas 88-95 %; conservadoras (no es fracaso) > 95 %.
     Siempre se informan el IC de Wilson, el ancho mediano, la IS y la MSIS; N2-N7 con la misma clasificación,
     sólo descriptiva.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

MODELOS = ["C49", "Crez", "L49", "Lrez"]
KEYS = ["institucion", "carrera", "region", "jornada", "genero", "condicion"]
NIVELES = [
    ("N1 Nacional", []),
    ("N2 + Institución", ["institucion"]),
    ("N3 + Área", ["institucion", "area_conocimiento"]),
    ("N4 + Región", ["institucion", "area_conocimiento", "region"]),
    ("N5 + Carrera", ["institucion", "area_conocimiento", "region", "carrera"]),
    ("N6 + Condición", ["institucion", "area_conocimiento", "region", "carrera", "condicion"]),
    ("N7 + Género", ["institucion", "area_conocimiento", "region", "carrera", "condicion", "genero"]),
    ("N8 + Jornada", ["institucion", "area_conocimiento", "region", "carrera", "condicion", "genero", "jornada"]),
]
ALPHA = 0.10
UNIVERSIDADES = ["Universidades CRUCH", "Universidades Privadas", "Universidades (* Carrera en Convenio)"]


# ------------------------------------------------------------------ §2 dato real
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def real_desde_sies(path, anio):
    mat = ["TOTAL MATRÍCULA", "TOTAL MATRÍCULA MUJERES", "TOTAL MATRÍCULA HOMBRES",
           "TOTAL MATRÍCULA NO BINARIOS O INDEFINIDOS", "TOTAL MATRÍCULA PRIMER AÑO",
           "TOTAL MATRÍCULA MUJERES PRIMER AÑO", "TOTAL MATRÍCULA HOMBRES PRIMER AÑO",
           "TOTAL MATRÍCULA NO BINARIOS O INDEFINIDOS PRIMER AÑO"]
    ide = ["AÑO", "CLASIFICACIÓN INSTITUCIÓN NIVEL 2", "NOMBRE INSTITUCIÓN", "REGIÓN", "NOMBRE CARRERA",
           "NIVEL GLOBAL", "JORNADA", "CÓDIGO CARRERA"]
    df = pd.read_csv(path, sep=";", encoding="latin-1", usecols=ide + mat, low_memory=False)
    df = df[df["AÑO"].astype(str).str[-4:].astype(int) == anio].copy()
    df[mat] = df[mat].fillna(0)
    pre = df[df["NIVEL GLOBAL"] == "Pregrado"]
    u = pre[pre["CLASIFICACIÓN INSTITUCIÓN NIVEL 2"].isin(UNIVERSIDADES)].copy()
    u["MUJER|ANTIGUO"] = (u["TOTAL MATRÍCULA MUJERES"] - u["TOTAL MATRÍCULA MUJERES PRIMER AÑO"]).clip(lower=0)
    u["HOMBRE|ANTIGUO"] = (u["TOTAL MATRÍCULA HOMBRES"] - u["TOTAL MATRÍCULA HOMBRES PRIMER AÑO"]).clip(lower=0)
    u["NO_BINARIO|ANTIGUO"] = (u["TOTAL MATRÍCULA NO BINARIOS O INDEFINIDOS"]
                               - u["TOTAL MATRÍCULA NO BINARIOS O INDEFINIDOS PRIMER AÑO"]).clip(lower=0)
    u["MUJER|NUEVO"] = u["TOTAL MATRÍCULA MUJERES PRIMER AÑO"]
    u["HOMBRE|NUEVO"] = u["TOTAL MATRÍCULA HOMBRES PRIMER AÑO"]
    u["NO_BINARIO|NUEVO"] = u["TOTAL MATRÍCULA NO BINARIOS O INDEFINIDOS PRIMER AÑO"]
    u["cod_carrera_base"] = (u["CÓDIGO CARRERA"].astype(str).str.extract(r"^(I\d+).*?(C\d+)", expand=True)
                             .fillna("").agg("".join, axis=1).replace("", np.nan))
    cols = [c for c in u.columns if "|" in c]
    lg = u.melt(id_vars=["NOMBRE INSTITUCIÓN", "NOMBRE CARRERA", "REGIÓN", "JORNADA", "cod_carrera_base"],
                value_vars=cols, var_name="gc", value_name="real")
    lg = lg[lg.real > 0]
    lg[["genero", "condicion"]] = lg.gc.str.split("|", expand=True)
    lg = lg.rename(columns={"NOMBRE INSTITUCIÓN": "institucion", "NOMBRE CARRERA": "carrera",
                            "REGIÓN": "region", "JORNADA": "jornada"})
    fino = lg.groupby(KEYS, as_index=False).real.sum()
    cod = (lg.dropna(subset=["cod_carrera_base"]).groupby(KEYS + ["cod_carrera_base"], as_index=False).real.sum()
             .sort_values("real", ascending=False).drop_duplicates(KEYS)[KEYS + ["cod_carrera_base"]])
    fino = fino.merge(cod, on=KEYS, how="left")
    control = {"pregrado_todas_IES": float(pre["TOTAL MATRÍCULA"].sum()),
               "pregrado_universidades": float(u["TOTAL MATRÍCULA"].sum()),
               "suma_celdas_reconstruidas": float(fino.real.sum())}
    return fino, control


# ------------------------------------------------------------------ bandas congeladas
def _f(x):
    return np.inf if x == "inf" else (-np.inf if x == "-inf" else float(x))


def banda_celda(lag, tasa, cal):
    b = np.array([_f(x) for x in cal["bordes"]])
    e = pd.cut(pd.Series(lag), b, labels=False, include_lowest=True)
    tabla = {int(k): v for k, v in cal["estratos"].items()}
    glo, ghi = cal["global"]
    lo = np.array([tabla[int(x)]["q_lo"] if pd.notna(x) and int(x) in tabla else glo for x in e])
    hi = np.array([tabla[int(x)]["q_hi"] if pd.notna(x) and int(x) in tabla else ghi for x in e])
    return np.clip(lag * (1 + np.sinh(tasa + lo)), 0, None), lag * (1 + np.sinh(tasa + hi))


def banda_celda_sin_estratos(lag, tasa, cal):
    glo, ghi = cal["global"]
    return np.clip(lag * (1 + np.sinh(tasa + glo)), 0, None), lag * (1 + np.sinh(tasa + ghi))


def banda_nivel(pred, cfg, bordes, etq, sin_estratos=False):
    if cfg["lo"] is None:
        return np.full(len(pred), np.nan), np.full(len(pred), np.nan)
    t = pd.cut(pd.Series(pred), [_f(x) for x in bordes], labels=etq)
    lo, hi = [], []
    for p, s in zip(pred, t):
        c = None if sin_estratos else cfg["estratos"].get(str(s))
        c = c or {"lo": cfg["lo"], "hi": cfg["hi"]}
        lo.append(p * np.exp(-c["hi"]))
        hi.append(p * np.exp(-c["lo"]))
    return np.array(lo), np.array(hi)


def wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan
    p = k / n
    d = 1 + z ** 2 / n
    c = (p + z ** 2 / (2 * n)) / d
    m = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / d
    return (c - m) * 100, (c + m) * 100


def clasifica_cobertura(cob):
    """Protocolo v2.2, §6: criterio asimétrico (cob en %)."""
    if not np.isfinite(cob):
        return "sin dato"
    if cob < 88:
        return "subcobertura"
    if cob <= 95:
        return "calibradas"
    return "conservadoras"


def interval_score(l, u, y, a=ALPHA):
    return (u - l) + (2 / a) * (l - y) * (y < l) + (2 / a) * (y - u) * (y > u)


# ------------------------------------------------------------------ métricas y pruebas
def metricas(real, pred, f0):
    real, pred, f0 = (np.asarray(x, float) for x in (real, pred, f0))
    e, en = pred - real, f0 - real
    rm, rn = np.sqrt(np.mean(e ** 2)), np.sqrt(np.mean(en ** 2))
    ok = real > 0
    return {"n": int(len(real)), "WAPE_%": np.abs(e).sum() / real.sum() * 100,
            "RelMAE": np.mean(np.abs(e)) / np.mean(np.abs(en)) if np.mean(np.abs(en)) > 0 else np.nan,
            "skill_%": (1 - (rm / rn) ** 2) * 100 if rn > 0 else np.nan,
            "pct_10_%": np.mean(np.abs(e[ok]) / real[ok] <= 0.10) * 100,
            "error_agregado_%": (pred.sum() - real.sum()) / real.sum() * 100}


def dm_cluster(d, cl):
    d = np.asarray(d, float)
    n, dbar = len(d), d.mean()
    s = pd.Series(d - dbar).groupby(np.asarray(cl)).sum()
    G = len(s)
    if G < 2:
        return dbar, np.nan, np.nan, G
    se = np.sqrt(G / (G - 1) * np.sum(s.values ** 2)) / n
    t = dbar / se if se > 0 else np.nan
    return dbar, t, (2 * stats.t.sf(abs(t), G - 1) if np.isfinite(t) else np.nan), G


def agrega(d, keys, cols):
    if not keys:
        return d[cols].sum().to_frame().T.assign(institucion="nacional")
    g = d.groupby(keys, dropna=False)[cols].sum().reset_index()
    if "institucion" not in g.columns:
        g["institucion"] = "nacional"
    return g


# ------------------------------------------------------------------ main
def main():
    import sys
    try:  ## consolas de Windows sin UTF-8: no fallar al imprimir «−» o «·»
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--sies", required=True)
    ap.add_argument("--paquete", required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--anio", type=int, default=2027)
    a = ap.parse_args()
    paq, out, Y = Path(a.paquete), Path(a.salida), a.anio
    out.mkdir(parents=True, exist_ok=True)
    reg = {"anio": Y, "archivo_sies": Path(a.sies).name, "sha256_sies": sha256(a.sies)}

    fc = pd.read_csv(paq / f"predicciones_forecast_{Y}_2x2.csv", dtype={c: str for c in KEYS + ["area_conocimiento", "cod_carrera_base"]})
    f0 = pd.read_csv(paq / f"predicciones_forecast_{Y}_persistencia.csv", dtype={c: str for c in KEYS + ["area_conocimiento"]})
    fn = pd.read_csv(paq / f"forecast_{Y}_nacional_Comb.csv")
    cal = json.load(open(paq / f"calibracion_bandas_{Y}.json", encoding="utf-8"))
    fc = fc.merge(f0[KEYS + ["pred_persistencia"]], on=KEYS, how="left").rename(columns={"pred_persistencia": "pred_F0"})
    assert fc.pred_F0.notna().all()

    real, control = real_desde_sies(a.sies, Y)
    reg["control_total"] = control
    ## §3 emparejamiento principal
    m = fc.merge(real[KEYS + ["real"]], on=KEYS, how="left")
    cerr = m[m.real.isna()]
    ev = m[m.real.notna()].copy()
    nuevos = real.merge(fc[KEYS], on=KEYS, how="left", indicator=True)
    nuevos = nuevos[nuevos._merge == "left_only"]
    reg["emparejamiento"] = {
        "celdas_pronosticadas": int(len(fc)), "celdas_emparejadas": int(len(ev)),
        "celdas_cerradas": int(len(cerr)), "pred_C49_en_cerradas": float(cerr.pred_C49.sum()),
        "celdas_nuevas": int(len(nuevos)), "matricula_celdas_nuevas": float(nuevos.real.sum()),
        "real_emparejado": float(ev.real.sum()),
        "cobertura_%_pregrado_universidades": float(ev.real.sum() / control["pregrado_universidades"] * 100)}

    pk = {k: f"pred_{k}" for k in MODELOS + ["F0"]}
    ## §4 métricas por nivel
    filas = []
    for nombre, keys in NIVELES:
        g = agrega(ev, keys, ["real"] + list(pk.values()))
        g = g[g.real > 0]
        for k, c in pk.items():
            filas.append({"nivel": nombre, "modelo": k, **metricas(g.real, g[c], g.pred_F0)})
    metr = pd.DataFrame(filas)
    nac = ev[["real"] + list(pk.values())].sum()
    fila_fn = {"nivel": "N1 Nacional", "modelo": "FN", "n": 1, "WAPE_%": abs(fn.total.iloc[0] - nac.real) / nac.real * 100,
               "error_agregado_%": (fn.total.iloc[0] - nac.real) / nac.real * 100}
    metr = pd.concat([metr, pd.DataFrame([fila_fn])], ignore_index=True)
    metr.to_csv(out / "metricas_por_nivel.csv", index=False)

    ## §5 hipótesis
    contrastes = {"H1": [(k, "F0") for k in MODELOS], "H2": [("C49", "Crez"), ("L49", "Lrez")],
                  "H3": [("C49", "L49"), ("Crez", "Lrez")]}
    niveles_h = {"H1": ["N8 + Jornada", "N2 + Institución", "N5 + Carrera"],
                 "H2": ["N8 + Jornada", "N2 + Institución", "N5 + Carrera"],
                 "H3": ["N8 + Jornada", "N2 + Institución", "N5 + Carrera"]}
    principal = {"H1": {"N8 + Jornada"}, "H2": {"N8 + Jornada", "N2 + Institución"}, "H3": {"N8 + Jornada"}}
    hip = []
    for h, pares in contrastes.items():
        for nombre in niveles_h[h]:
            keys = dict(NIVELES)[nombre]
            g = agrega(ev, keys, ["real"] + list(pk.values()))
            g = g[g.real > 0]
            for x, y in pares:
                ex, ey = g[pk[x]] - g.real, g[pk[y]] - g.real
                fila = {"hipotesis": h, "nivel": nombre, "rol": "principal" if nombre in principal[h] else "secundario",
                        "contraste": f"{x} − {y}"}
                for L, f in [("absoluta", np.abs), ("cuadratica", np.square)]:
                    dbar, t, p, G = dm_cluster(f(ex).values - f(ey).values, g.institucion.astype(str).values)
                    fila.update({f"d_medio_{L}": dbar, f"DM_{L}": t, f"p_{L}": p})
                fila["clusteres"] = G
                hip.append(fila)
    ## H2 por condición en N8 (secundaria)
    for cond, dc in ev.groupby("condicion"):
        g = agrega(dc, dict(NIVELES)["N8 + Jornada"], ["real"] + list(pk.values()))
        g = g[g.real > 0]
        for x, y in contrastes["H2"]:
            ex, ey = g[pk[x]] - g.real, g[pk[y]] - g.real
            fila = {"hipotesis": "H2", "nivel": f"N8 + Jornada · {cond}", "rol": "secundario", "contraste": f"{x} − {y}"}
            for L, f in [("absoluta", np.abs), ("cuadratica", np.square)]:
                dbar, t, p, G = dm_cluster(f(ex).values - f(ey).values, g.institucion.astype(str).values)
                fila.update({f"d_medio_{L}": dbar, f"DM_{L}": t, f"p_{L}": p})
            fila["clusteres"] = G
            hip.append(fila)
    hip = pd.DataFrame(hip)
    hip.to_csv(out / "hipotesis_H1_H3.csv", index=False)
    h4 = metr[metr.nivel == "N1 Nacional"][["modelo", "error_agregado_%"]]
    h4.to_csv(out / "hipotesis_H4_nacional.csv", index=False)

    ## H5 · bandas
    bandas = []
    bord = cal["agregados_bordes"]
    etq = cal["agregados_etiquetas"]
    for k in MODELOS:
        ck = cal["modelos"][k]
        lag = ev[f"rezago_{k}"].values.astype(float)
        tasa = ev[f"tasa_pred_arcsinh_{k}"].values.astype(float)
        mae_f0 = np.mean(np.abs(ev.pred_F0 - ev.real))
        for etq_b, (lo, hi) in {"congeladas": (ev[f"pi90_lo_{k}"].values, ev[f"pi90_hi_{k}"].values),
                                "referencia sin estratos": banda_celda_sin_estratos(lag, tasa, ck["celda"])}.items():
            dentro = (ev.real.values >= lo) & (ev.real.values <= hi)
            ci = wilson(int(dentro.sum()), len(ev))
            IS = interval_score(lo, hi, ev.real.values)
            bandas.append({"modelo": k, "bandas": etq_b, "nivel": "N8 + Jornada (celda)", "grupos": len(ev),
                           "cobertura_%": dentro.mean() * 100, "IC95_lo_%": ci[0], "IC95_hi_%": ci[1],
                           "ancho_mediano": float(np.median(hi - lo)), "IS_medio": float(IS.mean()),
                           "MSIS": float(IS.mean() / mae_f0)})
        for nombre, keys in NIVELES[1:7]:
            g = agrega(ev, keys, ["real", pk[k], "pred_F0"])
            g = g[(g.real > 0) & (g[pk[k]] > 0)]
            for etq_b, sinest in [("congeladas", False), ("referencia sin estratos", True)]:
                lo, hi = banda_nivel(g[pk[k]].values, ck["agregados"][nombre], bord, etq, sin_estratos=sinest)
                dentro = (g.real.values >= lo) & (g.real.values <= hi)
                ci = wilson(int(dentro.sum()), len(g))
                IS = interval_score(lo, hi, g.real.values)
                bandas.append({"modelo": k, "bandas": etq_b, "nivel": nombre, "grupos": len(g),
                               "cobertura_%": dentro.mean() * 100, "IC95_lo_%": ci[0], "IC95_hi_%": ci[1],
                               "ancho_mediano": float(np.median(hi - lo)), "IS_medio": float(IS.mean()),
                               "MSIS": float(IS.mean() / np.mean(np.abs(g.pred_F0 - g.real)))})
    bandas = pd.DataFrame(bandas)
    bandas["clasificacion"] = bandas["cobertura_%"].map(clasifica_cobertura)
    bandas.to_csv(out / "hipotesis_H5_bandas.csv", index=False)

    ## §3 secundario: emparejamiento por código
    sec = []
    rc = real.dropna(subset=["cod_carrera_base"]).groupby(["institucion", "cod_carrera_base", "region", "jornada", "genero", "condicion"], as_index=False).real.sum()
    fcc = fc.dropna(subset=["cod_carrera_base"]).groupby(["institucion", "cod_carrera_base", "region", "jornada", "genero", "condicion"], as_index=False)[list(pk.values())].sum()
    mc = fcc.merge(rc, on=["institucion", "cod_carrera_base", "region", "jornada", "genero", "condicion"], how="inner")
    for k, c in pk.items():
        sec.append({"modelo": k, **metricas(mc.real, mc[c], mc.pred_F0)})
    pd.DataFrame(sec).to_csv(out / "sensibilidad_emparejamiento_por_codigo.csv", index=False)

    ## §6 criterios
    n8 = metr[metr.nivel == "N8 + Jornada"].set_index("modelo")
    b8 = bandas[(bandas.bandas == "congeladas") & (bandas.nivel == "N8 + Jornada (celda)")].set_index("modelo")
    crit = []
    for k in MODELOS:
        crit.append({"modelo": k, "RelMAE_N8": n8.loc[k, "RelMAE"], "supera_persistencia": bool(n8.loc[k, "RelMAE"] < 1),
                     "cobertura_N8_%": b8.loc[k, "cobertura_%"], "IC95": f"{b8.loc[k, 'IC95_lo_%']:.2f}-{b8.loc[k, 'IC95_hi_%']:.2f}",
                     "clasificacion_bandas": clasifica_cobertura(b8.loc[k, "cobertura_%"]),
                     "fracaso_bandas": bool(clasifica_cobertura(b8.loc[k, "cobertura_%"]) == "subcobertura")})
    crit = pd.DataFrame(crit)
    crit.to_csv(out / "criterios_exito_fracaso.csv", index=False)
    reg["salidas"] = sorted(p.name for p in out.glob("*.csv"))
    (out / "registro_evaluacion.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")

    pd.set_option("display.width", 220)
    print(json.dumps(reg["emparejamiento"], ensure_ascii=False))
    print(metr[metr.nivel.isin(["N1 Nacional", "N2 + Institución", "N8 + Jornada"])].round(4).to_string(index=False))
    print(hip[hip.rol == "principal"][["hipotesis", "nivel", "contraste", "DM_absoluta", "p_absoluta", "DM_cuadratica", "p_cuadratica"]].round(4).to_string(index=False))
    print(crit.round(4).to_string(index=False))
    print(bandas[bandas.bandas == "congeladas"][["modelo", "nivel", "cobertura_%", "IC95_lo_%", "IC95_hi_%", "clasificacion"]].round(2).to_string(index=False))


if __name__ == "__main__":
    main()
