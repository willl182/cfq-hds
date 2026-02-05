#!/usr/bin/env python3
import csv
import html
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
HDS_DIR = BASE_DIR / "red_hds" / "hds_existentes"
OUTPUT_DIR = BASE_DIR / "output"


FILES = [
    "Kieserita_Secciones_V2.xlsx",
    "Carbonato_Secciones_V2.xlsx",
    "Silicato_Secciones_V2.xlsx",
]


def _normalize_text(value):
    if value is None:
        return ""
    text = html.unescape(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _collapse_spaces(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" \n", "\n", text)
    return text.strip()


def _read_sheet1_xml(xlsx_path):
    data = {}
    with zipfile.ZipFile(xlsx_path, "r") as zf:
        xml_bytes = zf.read("xl/worksheets/sheet1.xml")
    root = ET.fromstring(xml_bytes)
    ns = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    for row in root.findall(".//ns:row", ns):
        row_num = row.get("r")
        cells = {}
        for cell in row.findall(".//ns:c", ns):
            ref = cell.get("r")
            value_elem = cell.find(".//ns:t", ns)
            if value_elem is not None:
                cells[ref] = _normalize_text(value_elem.text)
        if cells:
            data[row_num] = cells
    return data


def _extract_sections(xlsx_path):
    rows = _read_sheet1_xml(xlsx_path)
    sections = {}
    for row_num in sorted(rows.keys(), key=lambda x: int(x)):
        label = rows[row_num].get(f"A{row_num}", "")
        content = rows[row_num].get(f"B{row_num}", "")
        if not label:
            continue
        match = re.match(r"Secci[oó]n\s*(\d+)", label, re.IGNORECASE)
        if match:
            sections[match.group(1)] = content
    return sections


def _first_line(value):
    for line in value.split("\n"):
        line = line.strip()
        if line:
            return line
    return ""


def _find_regex(pattern, text, flags=re.IGNORECASE):
    match = re.search(pattern, text, flags)
    if not match:
        return ""
    return match.group(1).strip()


def _find_all_regex(pattern, text, flags=re.IGNORECASE):
    return list(dict.fromkeys(re.findall(pattern, text, flags)))


def parse_section_1(text):
    result = {
        "nombre": "",
        "cas": "",
        "proveedor": "",
        "uso": "",
        "telefono_emergencia": "",
    }
    if not text:
        return result
    result["cas"] = _find_regex(r"CAS[:\s]*(\d{1,7}-\d{2}-\d)", text)
    name = _find_regex(r"Identificador\s+SGA\s+del\s+producto[:\s]*([^\n]+)", text)
    if not name:
        name = _find_regex(r"Nombre\s+de\s+la\s+sustancia[:\s]*([^\n]+)", text)
    result["nombre"] = name
    uso = _find_regex(r"Uso\s+recomendado[^:\n]*[:\s]*([^\n]+)", text)
    if not uso:
        uso = _find_regex(r"Uso\s+de\s+la\s+sustancia[:\s]*([^\n]+)", text)
    result["uso"] = uso
    prov = _find_regex(r"Datos\s+sobre\s+el\s+proveedor[:\s]*\n([^\n]+)", text)
    if not prov:
        prov = _find_regex(r"Datos\s+del\s+proveedor[^:\n]*[:\s]*([^\n]+)", text)
    result["proveedor"] = prov
    tel = _find_regex(r"Tel[eé]fono\s+de\s+emergencia[:\s]*([^\n]+)", text)
    if not tel:
        tel = _find_regex(r"N[uú]mero\s+de\s+tel[eé]fono\s+para\s+emergencias[:\s]*([^\n]+)", text)
    result["telefono_emergencia"] = tel
    return result


def parse_section_2(text):
    result = {
        "clasificacion": "",
        "frases_h": [],
        "frases_p": [],
        "pictogramas": [],
        "palabra_senal": "",
    }
    if not text:
        return result
    if re.search(r"no\s+est[aá]\s+clasificado|no\s+clasificado", text, re.IGNORECASE):
        result["clasificacion"] = "No clasificado"
    elif re.search(r"clasificaci[oó]n", text, re.IGNORECASE):
        result["clasificacion"] = "Clasificado"
    frases_h = _find_all_regex(r"H\d{3}[A-Z]*", text)
    frases_p = _find_all_regex(r"P\d{3}(?:\+P\d{3})*", text)
    expanded_p = []
    for item in frases_p:
        if "+" in item:
            expanded_p.extend(item.split("+"))
        else:
            expanded_p.append(item)
    result["frases_h"] = frases_h
    result["frases_p"] = list(dict.fromkeys(expanded_p))
    senal = _find_regex(r"Palabra\s+de\s+advertencia[:\s]*([^\n]+)", text)
    result["palabra_senal"] = senal
    result["pictogramas"] = _find_all_regex(r"GHS\d{2}", text)
    return result


def parse_section_3(text):
    result = {
        "componentes": "",
        "cas": "",
        "porcentaje": "",
    }
    if not text:
        return result
    cas = _find_regex(r"CAS[:\s]*(\d{1,7}-\d{2}-\d)", text)
    if not cas:
        cas = _find_regex(r"(\d{1,7}-\d{2}-\d)", text)
    percent = _find_regex(r"(\d{1,3})\s*%", text)
    if cas:
        result["componentes"] = cas
        result["cas"] = cas
    result["porcentaje"] = percent
    return result


def _extract_after_label(text, label):
    pattern = rf"{label}[:\s]*\n([^\n]+(?:\n[^\n]+){{0,2}})"
    return _find_regex(pattern, text)


def _strip_section_headers(text):
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            lines.append("")
            continue
        if re.search(r"CONTIN[UÚ]A", stripped, re.IGNORECASE):
            continue
        if re.search(r"^P[áa]gina\s+\d+", stripped, re.IGNORECASE):
            continue
        if re.search(r"Ficha de datos de seguridad", stripped, re.IGNORECASE):
            continue
        if re.search(r"^SECCI[ÓO]N\s+4", stripped, re.IGNORECASE):
            continue
        if re.search(r"seg[uú]n\s+Decreto", stripped, re.IGNORECASE):
            continue
        if re.search(r"Resoluci[oó]n\s+\d+", stripped, re.IGNORECASE):
            continue
        lines.append(stripped)
    return "\n".join(lines)


def _extract_block(text, label_pattern, stop_pattern):
    pattern = rf"{label_pattern}[:\s]*\n?(.*?)(?=\n(?:{stop_pattern})[:\s]|\Z)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    block = match.group(1)
    block = _collapse_spaces(block.replace("\n", " "))
    return block


def _extract_best_block(text, label_pattern, stop_pattern):
    pattern = rf"{label_pattern}[:\s]*\n?(.*?)(?=\n(?:{stop_pattern})[:\s]|\Z)"
    matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
    candidates = []
    for match in matches:
        block = match.group(1)
        block = _collapse_spaces(block.replace("\n", " "))
        if block:
            candidates.append(block)
    if not candidates:
        return ""
    return max(candidates, key=len)


def _clean_aux_text(value):
    if not value:
        return ""
    start_markers = ["En caso", "Lavar", "Enjuagar", "Transportar", "Acúdase"]
    indices = [value.find(marker) for marker in start_markers if value.find(marker) != -1]
    if indices:
        value = value[min(indices):]
    if "." in value:
        value = value[:value.rfind(".") + 1]
    return _collapse_spaces(value)


def parse_section_4(text):
    result = {
        "aux_inhalacion": "",
        "aux_piel": "",
        "aux_ojos": "",
        "aux_ingestion": "",
    }
    if not text:
        return result
    cleaned = _strip_section_headers(text)
    stop_labels = (
        r"Por\s+inhalaci[oó]n|"
        r"Inhalaci[oó]n|"
        r"Por\s+contacto\s+con\s+la\s+piel|"
        r"Contacto\s+con\s+la\s+piel|"
        r"Por\s+contacto\s+con\s+los\s+ojos|"
        r"Contacto\s+con\s+los\s+ojos|"
        r"Por\s+ingesti[oó]n(?:/aspiraci[oó]n)?|"
        r"Ingesti[oó]n|"
        r"\d+\.\d|"
        r"\d+\.\s+S[ií]ntomas"
    )
    result["aux_inhalacion"] = _extract_best_block(cleaned, r"Por\s+inhalaci[oó]n", stop_labels)
    if not result["aux_inhalacion"]:
        result["aux_inhalacion"] = _extract_best_block(cleaned, r"Inhalaci[oó]n", stop_labels)
    result["aux_piel"] = _extract_best_block(cleaned, r"Por\s+contacto\s+con\s+la\s+piel", stop_labels)
    if not result["aux_piel"]:
        result["aux_piel"] = _extract_best_block(cleaned, r"Contacto\s+con\s+la\s+piel", stop_labels)
    result["aux_ojos"] = _extract_best_block(cleaned, r"Por\s+contacto\s+con\s+los\s+ojos", stop_labels)
    if not result["aux_ojos"]:
        result["aux_ojos"] = _extract_best_block(cleaned, r"Contacto\s+con\s+los\s+ojos", stop_labels)
    result["aux_ingestion"] = _extract_best_block(cleaned, r"Por\s+ingesti[oó]n(?:/aspiraci[oó]n)?", stop_labels)
    if not result["aux_ingestion"]:
        result["aux_ingestion"] = _extract_best_block(cleaned, r"Ingesti[oó]n", stop_labels)
    for key in result:
        result[key] = _clean_aux_text(result[key])
    return result


def parse_section_7(text):
    result = {
        "almacenamiento": "",
        "incompatibles": "",
    }
    if not text:
        return result
    result["almacenamiento"] = _find_regex(r"Condiciones\s+de\s+almacenamiento[^:\n]*[:\s]*([^\n]+)", text)
    if not result["almacenamiento"]:
        result["almacenamiento"] = _find_regex(r"Almacenar[^\n]+", text)
    result["incompatibles"] = _find_regex(r"incompatib[^:\n]*[:\s]*([^\n]+)", text)
    return result


def parse_section_8(text):
    result = {
        "ppe_resp": "",
        "ppe_manos": "",
        "ppe_ojos": "",
    }
    if not text:
        return result
    cleaned = _normalize_text(text)
    stop = (
        r"Protecci[oó]n\s+respiratoria|Protecci[oó]n\s+de\s+las\s+manos|"
        r"Protecci[oó]n\s+de\s+los\s+ojos|Protecci[oó]n\s+cara/ojos|"
        r"Protecci[oó]n\s+de\s+la\s+piel|Protecci[oó]n\s+cut[áa]nea|Medidas\s+de\s+higiene|"
        r"Cuerpo|Pies|\u2022|"
    )
    result["ppe_resp"] = _extract_block(cleaned, r"Protecci[oó]n\s+respiratoria", stop)
    if not result["ppe_resp"]:
        result["ppe_resp"] = _extract_block(cleaned, r"Respirador", stop)
    result["ppe_manos"] = _extract_block(cleaned, r"Protecci[oó]n\s+de\s+las\s+manos", stop)
    if not result["ppe_manos"]:
        result["ppe_manos"] = _extract_block(cleaned, r"Guantes", stop)
    result["ppe_ojos"] = _extract_block(cleaned, r"Protecci[oó]n\s+cara/ojos", stop)
    if not result["ppe_ojos"]:
        result["ppe_ojos"] = _extract_block(cleaned, r"Protecci[oó]n\s+de\s+los\s+ojos", stop)
    if not result["ppe_ojos"]:
        result["ppe_ojos"] = _extract_block(cleaned, r"Gafas", stop)
    return result


def parse_section_9(text):
    result = {
        "punto_fusion": "",
        "densidad": "",
        "solubilidad": "",
    }
    if not text:
        return result
    cleaned = _normalize_text(text)
    cleaned = cleaned.replace("g/cm 3", "g/cm3").replace("kg/m 3", "kg/m3")
    lines = [line.strip() for line in cleaned.split("\n") if line.strip()]
    for line in lines:
        if not result["punto_fusion"] and re.search(r"Punto\s+de\s+fusi[oó]n", line, re.IGNORECASE):
            if ":" in line:
                target = line.split(":", 1)[1]
            else:
                target = line
            match = re.search(r"(\d+(?:[.,]\d+)?)\s*([°º]?\s*C)?", target)
            if match:
                value = match.group(1)
                unit = match.group(2) or ""
                result["punto_fusion"] = _collapse_spaces(f"{value} {unit}".strip())
        if not result["densidad"] and re.search(r"^Densidad\b|Densidad\s+a\s+\d+", line, re.IGNORECASE):
            if ":" in line:
                target = line.split(":", 1)[1]
            else:
                target = line
            matches = re.findall(r"(\d+(?:[.,]\d+)?)\s*([a-zA-Z/³0-9]+)?", target)
            if matches:
                value, unit = matches[-1]
                unit = unit or ""
                result["densidad"] = _collapse_spaces(f"{value} {unit}".strip())
        if not result["solubilidad"] and re.search(r"Solubilidad", line, re.IGNORECASE):
            sol = re.sub(r"Solubilidad[^:]*[:\s]*", "", line, flags=re.IGNORECASE)
            sol = sol.replace("No aplica", "").strip()
            if sol:
                result["solubilidad"] = sol
    return result


def parse_section_11(text):
    result = {
        "dl50_oral": "",
    }
    if not text:
        return result
    dl50 = _find_regex(r"DL50\s*oral[^\n>]*[>:\s]*([\d,.]+\s*mg/kg[^\n]*)", text)
    result["dl50_oral"] = dl50
    return result


def parse_section_12(text):
    result = {
        "ecotoxicidad": "",
    }
    if not text:
        return result
    result["ecotoxicidad"] = _first_line(text)
    return result


def _fill_na(value):
    return value if value else "NA"


def extract_product(xlsx_path, cod):
    sections = _extract_sections(xlsx_path)
    sec1 = parse_section_1(sections.get("1", ""))
    sec2 = parse_section_2(sections.get("2", ""))
    sec3 = parse_section_3(sections.get("3", ""))
    sec4 = parse_section_4(sections.get("4", ""))
    sec7 = parse_section_7(sections.get("7", ""))
    sec8 = parse_section_8(sections.get("8", ""))
    sec9 = parse_section_9(sections.get("9", ""))
    sec11 = parse_section_11(sections.get("11", ""))
    sec12 = parse_section_12(sections.get("12", ""))

    present_sections = sorted([int(k) for k in sections.keys()])
    missing_sections = sorted([i for i in range(1, 17) if str(i) not in sections])

    return {
        "cod": cod,
        "archivo_fuente": xlsx_path.name,
        "secciones": sections,
        "secciones_disponibles": present_sections,
        "secciones_faltantes": missing_sections,
        "nombre": _fill_na(sec1["nombre"]),
        "cas": _fill_na(sec1["cas"] or sec3["cas"]),
        "proveedor": _fill_na(sec1["proveedor"]),
        "uso": _fill_na(sec1["uso"]),
        "telefono_emergencia": _fill_na(sec1["telefono_emergencia"]),
        "clasificacion": _fill_na(sec2["clasificacion"]),
        "frases_h": sec2["frases_h"],
        "frases_p": sec2["frases_p"],
        "pictogramas": sec2["pictogramas"],
        "palabra_senal": _fill_na(sec2["palabra_senal"]),
        "componentes": _fill_na(sec3["componentes"]),
        "porcentaje": _fill_na(sec3["porcentaje"]),
        "aux_inhalacion": _fill_na(sec4["aux_inhalacion"]),
        "aux_piel": _fill_na(sec4["aux_piel"]),
        "aux_ojos": _fill_na(sec4["aux_ojos"]),
        "aux_ingestion": _fill_na(sec4["aux_ingestion"]),
        "almacenamiento": _fill_na(sec7["almacenamiento"]),
        "incompatibles": _fill_na(sec7["incompatibles"]),
        "ppe_resp": _fill_na(sec8["ppe_resp"]),
        "ppe_manos": _fill_na(sec8["ppe_manos"]),
        "ppe_ojos": _fill_na(sec8["ppe_ojos"]),
        "punto_fusion": _fill_na(sec9["punto_fusion"]),
        "densidad": _fill_na(sec9["densidad"]),
        "solubilidad": _fill_na(sec9["solubilidad"]),
        "dl50_oral": _fill_na(sec11["dl50_oral"]),
        "ecotoxicidad": _fill_na(sec12["ecotoxicidad"]),
    }


def write_json(products, output_path):
    payload = {
        "version": "1.0",
        "productos": products,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(products, output_path, headers):
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for item in products:
            writer.writerow(item)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    products = []
    cod_start = 13
    for idx, filename in enumerate(FILES):
        path = HDS_DIR / filename
        cod = str(cod_start + idx)
        products.append(extract_product(path, cod))

    json_path = OUTPUT_DIR / "hds_extraidas.json"
    write_json(products, json_path)

    headers = [
        "COD",
        "NOMBRE",
        "CAS",
        "FORMULA",
        "CLASIFICACION",
        "FRASES_H",
        "FRASES_P",
        "PICTOGRAMAS",
        "PALABRA_SEÑAL",
        "PUNTO_FUSION",
        "DENSIDAD",
        "SOLUBILIDAD",
        "PPE_RESP",
        "PPE_MANOS",
        "PPE_OJOS",
        "PRIMEROS_AUX_ING",
        "PRIMEROS_AUX_PIEL",
        "PRIMEROS_AUX_OJOS",
        "PRIMEROS_AUX_INH",
        "ALMACENAMIENTO",
        "INCOMPATIBLES",
        "ECOTOXICIDAD",
        "FUENTE_HDS",
    ]

    rows = []
    for item in products:
        rows.append({
            "COD": item["cod"],
            "NOMBRE": item["nombre"],
            "CAS": item["cas"],
            "FORMULA": "",
            "CLASIFICACION": item["clasificacion"],
            "FRASES_H": ";".join(item["frases_h"]),
            "FRASES_P": ";".join(item["frases_p"]),
            "PICTOGRAMAS": ";".join(item["pictogramas"]),
            "PALABRA_SEÑAL": item["palabra_senal"],
            "PUNTO_FUSION": item["punto_fusion"],
            "DENSIDAD": item["densidad"],
            "SOLUBILIDAD": item["solubilidad"],
            "PPE_RESP": item["ppe_resp"],
            "PPE_MANOS": item["ppe_manos"],
            "PPE_OJOS": item["ppe_ojos"],
            "PRIMEROS_AUX_ING": item["aux_ingestion"],
            "PRIMEROS_AUX_PIEL": item["aux_piel"],
            "PRIMEROS_AUX_OJOS": item["aux_ojos"],
            "PRIMEROS_AUX_INH": item["aux_inhalacion"],
            "ALMACENAMIENTO": item["almacenamiento"],
            "INCOMPATIBLES": item["incompatibles"],
            "ECOTOXICIDAD": item["ecotoxicidad"],
            "FUENTE_HDS": str((HDS_DIR / item["archivo_fuente"]).relative_to(BASE_DIR)),
        })

    csv_path = OUTPUT_DIR / "mp_nuevas.csv"
    write_csv(rows, csv_path, headers)

    print(f"JSON generado: {json_path}")
    print(f"CSV generado: {csv_path}")


if __name__ == "__main__":
    main()
