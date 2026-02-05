#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "datos"
TEMPLATES_DIR = BASE_DIR / "plantillas"
OUTPUT_DIR = BASE_DIR / "output" / "hds"


def _slugify(value):
    value = value.strip().lower()
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n",
    }
    for src, dst in replacements.items():
        value = value.replace(src, dst)
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def _read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _read_info_corp():
    rows = _read_csv(DATA_DIR / "info_corp.csv")
    if not rows:
        return {
            "razon_social": "NA",
            "direccion": "NA",
            "telefono_emergencia": "NA",
            "email_contacto": "NA",
            "pais": "NA",
        }
    row = rows[0]
    return {
        "razon_social": row.get("RAZON_SOCIAL", "NA"),
        "direccion": row.get("DIRECCION", "NA"),
        "telefono_emergencia": row.get("TELEFONO_EMERGENCIA", "NA"),
        "email_contacto": row.get("EMAIL_CONTACTO", "NA"),
        "pais": row.get("PAIS", "NA"),
    }


def _read_frases():
    frases = _read_csv(DATA_DIR / "frases_hp.csv")
    lookup = {}
    for row in frases:
        codigo = row.get("CODIGO", "").strip()
        if codigo:
            lookup[codigo] = row.get("TEXTO_ES", "").strip()
    return lookup


def _split_codes(value):
    if not value:
        return []
    value = value.replace(",", ";")
    parts = [p.strip() for p in value.split(";") if p.strip()]
    return parts


def _build_frases(codes, lookup):
    frases = []
    for code in codes:
        texto = lookup.get(code, "NA")
        frases.append({"codigo": code, "texto": texto})
    return frases


def _build_clasificacion(row):
    clas = row.get("CLASIFICACION", "NA")
    peligros = []
    if clas and clas not in ["NA", "No clasificado"]:
        peligros = [clas]
    return {
        "peligros": peligros,
        "pictogramas": row.get("PICTOGRAMAS", "") or "Ninguno",
        "palabra_senal": row.get("PALABRA_SEÑAL", "NA"),
    }


def _build_componentes(row):
    nombre = row.get("NOMBRE", "NA")
    cas = row.get("CAS", "NA")
    formula = row.get("FORMULA", "")
    porcentaje = row.get("PORCENTAJE", "")
    if not porcentaje:
        porcentaje = "100" if cas not in ["", "NA"] else "NA"
    return [
        {
            "nombre": nombre,
            "cas": cas,
            "formula": formula or "NA",
            "porcentaje": porcentaje,
            "clasificacion": row.get("CLASIFICACION", "NA"),
        }
    ]


def _mp_lookup(mp_rows):
    lookup = {}
    for row in mp_rows:
        code = row.get("COD")
        if code:
            lookup[code] = row
    return lookup


def _build_componentes_from_receta(receta_row, mp_lookup):
    componentes = []
    for idx in range(1, 12):
        cod = receta_row.get(f"COD_MP{idx}")
        porc = receta_row.get(f"PORC_MP{idx}")
        if not cod:
            continue
        mp = mp_lookup.get(cod, {})
        componentes.append({
            "nombre": mp.get("NOMBRE", "NA"),
            "cas": mp.get("CAS", "NA"),
            "formula": mp.get("FORMULA", "NA"),
            "porcentaje": porc or "NA",
            "clasificacion": mp.get("CLASIFICACION", "NA"),
        })
    return componentes


def _collect_frases_from_componentes(receta_row, mp_lookup):
    h_codes = []
    p_codes = []
    for idx in range(1, 12):
        cod = receta_row.get(f"COD_MP{idx}")
        if not cod:
            continue
        mp = mp_lookup.get(cod, {})
        h_codes.extend(_split_codes(mp.get("FRASES_H", "")))
        p_codes.extend(_split_codes(mp.get("FRASES_P", "")))
    # dedupe preserving order
    h_seen = set()
    p_seen = set()
    h_unique = [code for code in h_codes if not (code in h_seen or h_seen.add(code))]
    p_unique = [code for code in p_codes if not (code in p_seen or p_seen.add(code))]
    return h_unique, p_unique


def _pick_dominant_component(receta_row, mp_lookup):
    best = None
    best_pct = -1.0
    for idx in range(1, 12):
        cod = receta_row.get(f"COD_MP{idx}")
        porc = receta_row.get(f"PORC_MP{idx}")
        if not cod or not porc:
            continue
        try:
            pct_val = float(porc)
        except ValueError:
            continue
        if pct_val > best_pct:
            best_pct = pct_val
            best = mp_lookup.get(cod)
    return best or {}


def _build_context(row, empresa, frases_lookup):
    frases_h = _build_frases(_split_codes(row.get("FRASES_H", "")), frases_lookup)
    frases_p = _build_frases(_split_codes(row.get("FRASES_P", "")), frases_lookup)

    return {
        "producto": {
            "nombre": row.get("NOMBRE", "NA"),
            "codigo": row.get("COD", "NA"),
        },
        "empresa": empresa,
        "clasificacion": _build_clasificacion(row),
        "frases_h": frases_h,
        "frases_p": frases_p,
        "componentes": _build_componentes(row),
        "primeros_auxilios": {
            "inhalacion": row.get("PRIMEROS_AUX_INH", "NA"),
            "piel": row.get("PRIMEROS_AUX_PIEL", "NA"),
            "ojos": row.get("PRIMEROS_AUX_OJOS", "NA"),
            "ingestion": row.get("PRIMEROS_AUX_ING", "NA"),
        },
        "ppe": {
            "respiratoria": row.get("PPE_RESP", "NA"),
            "manos": row.get("PPE_MANOS", "NA"),
            "ojos": row.get("PPE_OJOS", "NA"),
        },
        "propiedades": {
            "punto_fusion": row.get("PUNTO_FUSION", ""),
            "densidad": row.get("DENSIDAD", ""),
            "solubilidad": row.get("SOLUBILIDAD", ""),
        },
        "almacenamiento": row.get("ALMACENAMIENTO", ""),
        "incompatibles": row.get("INCOMPATIBLES", ""),
        "ecotoxicidad": row.get("ECOTOXICIDAD", ""),
        "fecha_elaboracion": "2026-02-04",
        "version": "1.0",
        "elaborado_por": empresa.get("razon_social", "NA"),
    }


def _build_context_from_receta(receta_row, mp_lookup, empresa, frases_lookup):
    dominant = _pick_dominant_component(receta_row, mp_lookup)
    h_codes, p_codes = _collect_frases_from_componentes(receta_row, mp_lookup)
    frases_h = _build_frases(h_codes, frases_lookup)
    frases_p = _build_frases(p_codes, frases_lookup)
    return {
        "producto": {
            "nombre": receta_row.get("NOMBRE_PT", "NA"),
            "codigo": receta_row.get("COD_PT", "NA"),
        },
        "empresa": empresa,
        "clasificacion": {
            "peligros": ["Mezcla con componentes clasificados"] if frases_h else [],
            "pictogramas": "Ninguno",
            "palabra_senal": "NA",
        },
        "frases_h": frases_h,
        "frases_p": frases_p,
        "componentes": _build_componentes_from_receta(receta_row, mp_lookup),
        "primeros_auxilios": {
            "inhalacion": dominant.get("PRIMEROS_AUX_INH", "NA"),
            "piel": dominant.get("PRIMEROS_AUX_PIEL", "NA"),
            "ojos": dominant.get("PRIMEROS_AUX_OJOS", "NA"),
            "ingestion": dominant.get("PRIMEROS_AUX_ING", "NA"),
        },
        "ppe": {
            "respiratoria": dominant.get("PPE_RESP", "NA"),
            "manos": dominant.get("PPE_MANOS", "NA"),
            "ojos": dominant.get("PPE_OJOS", "NA"),
        },
        "propiedades": {
            "punto_fusion": dominant.get("PUNTO_FUSION", ""),
            "densidad": dominant.get("DENSIDAD", ""),
            "solubilidad": dominant.get("SOLUBILIDAD", ""),
        },
        "almacenamiento": dominant.get("ALMACENAMIENTO", ""),
        "incompatibles": dominant.get("INCOMPATIBLES", ""),
        "ecotoxicidad": dominant.get("ECOTOXICIDAD", ""),
        "fecha_elaboracion": "2026-02-04",
        "version": "1.0",
        "elaborado_por": empresa.get("razon_social", "NA"),
    }


def _parse_args():
    parser = argparse.ArgumentParser(description="Generar HDS en Markdown")
    parser.add_argument(
        "--cods",
        help="Lista de COD separados por coma (ej: 13,14,15)",
        default="",
    )
    parser.add_argument(
        "--receta-cod",
        help="Codigo de receta (COD_PT) para generar HDS",
        default="",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    cods_filter = []
    if args.cods:
        cods_filter = [item.strip() for item in args.cods.split(",") if item.strip()]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    empresa = _read_info_corp()
    frases_lookup = _read_frases()
    mp_rows = _read_csv(DATA_DIR / "mp_sga.csv")
    mp_lookup = _mp_lookup(mp_rows)

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)
    template = env.get_template("hds_template.md")

    if args.receta_cod:
        recetas = _read_csv(DATA_DIR / "recetas.csv")
        receta = None
        for row in recetas:
            if row.get("COD_PT") == args.receta_cod:
                receta = row
                break
        if not receta:
            raise SystemExit(f"No se encontró receta con COD_PT={args.receta_cod}")
        context = _build_context_from_receta(receta, mp_lookup, empresa, frases_lookup)
        content = template.render(**context)
        codigo = receta.get("COD_PT", "NA")
        nombre = receta.get("NOMBRE_PT", "producto")
        filename = f"HDS_{codigo}_{_slugify(nombre)}.md"
        output_path = OUTPUT_DIR / filename
        output_path.write_text(content, encoding="utf-8")
    else:
        for row in mp_rows:
            if cods_filter and row.get("COD") not in cods_filter:
                continue
            context = _build_context(row, empresa, frases_lookup)
            content = template.render(**context)

            codigo = row.get("COD", "NA")
            nombre = row.get("NOMBRE", "producto")
            filename = f"HDS_{codigo}_{_slugify(nombre)}.md"
            output_path = OUTPUT_DIR / filename
            output_path.write_text(content, encoding="utf-8")

    if cods_filter:
        print(f"HDS generadas para CODs {', '.join(cods_filter)} en: {OUTPUT_DIR}")
    elif args.receta_cod:
        print(f"HDS generada para receta {args.receta_cod} en: {OUTPUT_DIR}")
    else:
        print(f"HDS generadas en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
