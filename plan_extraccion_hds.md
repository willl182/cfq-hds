# Plan de Extracción de Datos HDS

## Fecha
2026-02-04

## Objetivo
Extraer información estructurada de 3 archivos Excel existentes con HDS y generar datos compatibles con el sistema automatizado.

## Estado
**PENDIENTE DE IMPLEMENTACIÓN**

---

## 1. Contexto

### Archivos Disponibles
| Archivo | Producto | CAS | Secciones | Faltantes |
|---------|----------|-----|-----------|-----------|
| Kieserita_Secciones_V2.xlsx | Sulfato de magnesio monohidratado | 7487-88-9 | 15 | 13 |
| Carbonato_Secciones_V2.xlsx | Carbonato de calcio | 471-34-1 | 14 | 7, 13 |
| Silicato_Secciones_V2.xlsx | Silicato (no identificado) | ? | 11 | 1, 2, 3, 4, 7 |

### Limitación Técnica
El entorno no dispone de paquetes externos (pandas, openpyxl). Se usará `zipfile` + `xml.etree.ElementTree` para leer los archivos Excel.

---

## 2. Esquema de Datos

### Campos a Extraer por Sección

| Sección | Campos | Tipo de Extracción |
|---------|--------|---------------------|
| 1 (Identificación) | nombre, cas, proveedor, uso, telefono_emergencia | Regex |
| 2 (Peligros) | clasificacion, frases_h, frases_p, pictogramas, palabra_senal | Regex + parsing |
| 3 (Composición) | componentes (dict), pureza | Regex |
| 4 (Primeros auxilios) | aux_inhalacion, aux_piel, aux_ojos, aux_ingestion, aux_sintomas | Regex |
| 5 (Incendios) | medios_extincion, peligros_incendio | Texto libre |
| 6 (Vertido) | medidas_limpieza, precauciones_medio_ambiente | Texto libre |
| 7 (Manipulación) | almacenamiento, incompatibilidades | Texto libre |
| 8 (Exposición) | ppe_resp, ppe_manos, ppe_ojos, ppe_cuerpo | Regex |
| 9 (Propiedades) | estado, aspecto, color, olor, densidad, ph, punto_fusion, solubilidad | Regex |
| 10 (Estabilidad) | reactividad, productos_descomposicion | Texto libre |
| 11 (Toxicología) | dl50_oral, dl50_dermal, vias_exposicion, efectos_salud | Regex |
| 12 (Ecotoxicología) | toxicidad_acuatica, persistencia, bioacumulacion | Texto libre |
| 13 (Eliminación) | metodos_eliminacion | Texto libre |
| 14 (Transporte) | clasificacion_transporte, un_numero | Regex |
| 15 (Regulación) | normativas_aplicables | Texto libre |
| 16 (Otras) | fuentes_bibliograficas, notas_adicionales | Texto libre |

### Patrones Regex Principales

```python
# CAS
r"CAS[:\s]*(\d{1,7}-\d{2}-\d)"

# Frases H (ej: H302, H315, H360FD)
r"H\d{3}[A-Z]*"

# Frases P (ej: P261, P302+P335)
r"P\d{3}(?:\+P\d{3})*"

# DL50
r"DL50\s*(oral|dérmica|inhalación)[:\s>]*(\d+)\s*mg/kg"

# Densidad
r"[Dd]ensidad[^:]*:\s*([\d,.]+)\s*(kg/m³|g/cm³)?"

# pH
r"[Pp][Hh][:\s]*(\d+(?:[.,]\d+)?)"

# Punto de fusión
r"[Pp]unto\s+(?:de\s+)?(?:fusión|fusión)[:\s]*(\d+)\s*°C"

# Número ONU
r"[Nn]úmero\s+[Oo][Nn][Uu][:\s]*(\d+)"
```

---

## 3. Implementación

### Archivos a Crear/Modificar

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `scripts/extraer_hds.py` | CREAR | Script principal de extracción |
| `output/hds_extraidas.json` | CREAR | Datos completos en JSON |
| `output/mp_nuevas.csv` | CREAR | Datos en formato CSV |
| `datos/mp_sga.csv` | MODIFICAR | Agregar 3 nuevas materias primas |

### Estructura del Script

```python
#!/usr/bin/env python3

# scripts/extraer_hds.py

import zipfile
import xml.etree.ElementTree as ET
import re
import json
import csv
import html
from pathlib import Path

# Funciones principales:
# - leer_excel_xml(ruta_excel): dict {seccion: contenido}
# - parsear_seccion1(texto): {nombre, cas, proveedor, uso}
# - parsear_seccion2(texto): {clasificacion, frases_h, frases_p, pictogramas, palabra_senal}
# - parsear_seccion3(texto): {componentes, pureza}
# - parsear_seccion4(texto): {aux_inhalacion, aux_piel, aux_ojos, aux_ingestion, aux_sintomas}
# - parsear_seccion9(texto): {estado, aspecto, densidad, ph, punto_fusion}
# - parsear_seccion11(texto): {dl50_oral, vias_exposicion, efectos_salud}
# - extraer_producto(ruta_excel, nombre_archivo): dict con todos los campos
# - generar_json(productos, ruta_salida)
# - generar_csv(productos, ruta_salida)
# - main(): procesar 3 archivos, generar salidas, imprimir reporte
```

---

## 4. Flujos de Datos

### Flujo Principal
```
red_hds/hds_existentes/
├── Kieserita_Secciones_V2.xlsx
├── Carbonato_Secciones_V2.xlsx
└── Silicato_Secciones_V2.xlsx
         ↓
[extraer_hds.py] → lectura via zipfile+xml
         ↓
   parsing por sección (regex)
         ↓
   estructura de datos Python
         ↓
    ┌────┴────┐
    ↓         ↓
  JSON      CSV
    ↓         ↓
output/    output/
hds_extraidas.json  mp_nuevas.csv
               ↓
         datos/mp_sga.csv (merge)
```

### Manejo de Datos Faltantes

| Producto | Campos Faltantes | Valor en Salida |
|----------|------------------|----------------|
| Kieserita | Sección 13 | "No disponible" |
| Carbonato | Secciones 7, 13 | "No disponible" |
| Silicato | Secciones 1-4, 7 | "NA" (critical) |
| Todos | Campos no extraídos | Vacío o "NA" |

---

## 5. Salidas Esperadas

### output/hds_extraidas.json

```json
{
  "fecha_extraccion": "2026-02-04",
  "version": "1.0",
  "productos": [
    {
      "id": "MP002",
      "archivo_fuente": "Kieserita_Secciones_V2.xlsx",
      "nombre": "Kieserita - Sulfato de magnesio monohidratado",
      "cas": "7487-88-9",
      "proveedor": "PRECISAGRO S.A.S.",
      "clasificacion": {
        "peligroso": false,
        "descripcion": "No clasificado como peligroso",
        "frases_h": [],
        "frases_p": [],
        "pictogramas": [],
        "palabra_senal": "Ninguno"
      },
      "propiedades_fisicas": {
        "estado": "Sólido",
        "aspecto": "Granulado",
        "color": "No determinado",
        "densidad": "2650 kg/m³",
        "punto_fusion": "1127 °C"
      },
      "primeros_auxilios": {
        "inhalacion": "En caso de síntomas, trasladar al afectado al aire libre",
        "piel": "Limpiar la zona afecta con agua por arrastre y con jabón neutro",
        "ojos": "Enjuagar con agua hasta la eliminación del producto",
        "ingestion": "En caso de ingestión de grandes cantidades, solicitar asistencia médica"
      },
      "toxicologia": {
        "dl50_oral": ">5000 mg/kg (rata)",
        "vias_exposicion": ["inhalación", "piel", "ojos", "ingestión"],
        "efectos_agudos": "A la vista de los datos disponibles, no se cumplen los criterios de clasificación"
      },
      "secciones_disponibles": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16],
      "secciones_faltantes": [13],
      "campos_completos": true
    },
    {
      "id": "MP003",
      "archivo_fuente": "Carbonato_Secciones_V2.xlsx",
      "nombre": "Carbonato de calcio",
      "cas": "471-34-1",
      "proveedor": "Química Pima, S.A. de C.V.",
      "clasificacion": {
        "peligroso": false,
        "descripcion": "No clasificado como peligroso",
        "frases_h": ["H315", "H320", "H335"],
        "frases_p": ["P261", "P264", "P271", "P280"],
        "pictogramas": [],
        "palabra_senal": "Atención"
      },
      "secciones_disponibles": [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16],
      "secciones_faltantes": [7, 13],
      "campos_completos": true
    },
    {
      "id": "MP004",
      "archivo_fuente": "Silicato_Secciones_V2.xlsx",
      "nombre": "Silicato",
      "cas": "NA",
      "proveedor": "NA",
      "clasificacion": {
        "peligroso": false,
        "descripcion": "NA",
        "frases_h": [],
        "frases_p": [],
        "pictogramas": [],
        "palabra_senal": "NA"
      },
      "propiedades_fisicas": {
        "estado": "NA",
        "aspecto": "Verde Manzana",
        "color": "NA",
        "olor": "Inodoro"
      },
      "primeros_auxilios": {
        "inhalacion": "NA",
        "piel": "NA",
        "ojos": "NA",
        "ingestion": "NA"
      },
      "secciones_disponibles": [5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16],
      "secciones_faltantes": [1, 2, 3, 4, 7],
      "campos_completos": false
    }
  ]
}
```

### output/mp_nuevas.csv

```csv
COD,NOMBRE,CAS,FORMULA,CLASIFICACION,FRASES_H,FRASES_P,PICTOGRAMAS,PALABRA_SEÑAL,PUNTO_FUSION,DENSIDAD,SOLUBILIDAD,PPE_RESP,PPE_MANOS,PPE_OJOS,PRIMEROS_AUX_ING,PRIMEROS_AUX_PIEL,PRIMEROS_AUX_OJOS,PRIMEROS_AUX_INH,ALMACENAMIENTO,INCOMPATIBLES,ECOTOXICIDAD,FUENTE_HDS
MP002,Kieserita,7487-88-9,,No clasificado,,,,Ninguno,1127 °C,2650 kg/m³,,Mascarilla N95,,Gafas,En caso de ingestión de grandes cantidades, se recomienda solicitar asistencia médica,En caso de contacto se recomienda limpiar la zona afecta con agua por arrastre y con jabón neutro,Enjuagar con agua hasta la eliminación del producto,En caso de síntomas, trasladar al afectado al aire libre,Almacenar en lugar fresco, seco y ventilado,,No disponible,red_hds/hds_existentes/Kieserita_Secciones_V2.xlsx
MP003,Carbonato de calcio,471-34-1,,No clasificado,H315;H320;H335,P261;P264;P271;P280,,Atención,,,NA,,,No inducir al vómito a menos que lo indique expresamente el personal médico,Lavar la piel contaminada con agua y jabón,Enjuagar los ojos inmediatamente con mucha agua,Transportar la víctima al aire libre,Fresco y seco well ventilado,Monóxido de carbono, No disponible,red_hds/hds_existentes/Carbonato_Secciones_V2.xlsx
MP004,Silicato,NA,,NA,NA,NA,,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,red_hds/hds_existentes/Silicato_Secciones_V2.xlsx
```

---

## 6. Tareas Detalladas

| # | Tarea | Descripción | Tiempo Estimado |
|---|-------|-------------|-----------------|
| 1 | Crear script base `scripts/extraer_hds.py` | Estructura, imports, funciones vacías | 5 min |
| 2 | Implementar `leer_excel_xml()` | Parsear Excel via zipfile + xml.etree | 10 min |
| 3 | Implementar parsers de sección 1-4 | Regex para identificación, peligros, composición, primeros auxilios | 15 min |
| 4 | Implementar parsers de sección 8-12 | Regex para PPE, propiedades, toxicología | 15 min |
| 5 | Implementar `extraer_producto()` | Orquestar extracción completa por producto | 10 min |
| 6 | Implementar `generar_json()` | Exportar datos estructurados | 5 min |
| 7 | Implementar `generar_csv()` | Exportar datos en formato mp_sga.csv | 10 min |
| 8 | Implementar `main()` | Procesar 3 archivos, generar salidas, reporte | 10 min |
| 9 | Ejecutar script y validar | Verificar salidas, revisar errores | 10 min |
| 10 | Actualizar `datos/mp_sga.csv` | Agregar 3 nuevas filas | 5 min |
| **TOTAL** | | | **~95 min** |

---

## 7. Dependencias

- Python 3.x (disponible)
- Módulos estándar: `zipfile`, `xml.etree.ElementTree`, `re`, `json`, `csv`, `html`, `pathlib`
- Sin dependencias externas

---

## 8. Riesgos y Mitigaciones

| Riesgo | Impacto | Probabilidad | Mitigación |
|--------|---------|--------------|------------|
| Regex no captura todos los formatos | Medio | Alta | Probar con patrones múltiples, validar manualmente |
| Silicato tiene datos críticos faltantes | Alto | Segura | Marcar como "NA", recomendar buscar HDS completa |
| Diferencias de formato entre archivos | Bajo | Media | Validar cada parser con los 3 archivos |
| Casos especiales en texto (saltos de línea, codificación) | Bajo | Media | Sanitizar con html.unescape(), manejar whitespace |

---

## 9. Validación

### Checklist de Validación

- [ ] Script ejecuta sin errores
- [ ] JSON generado es válido (syntax check)
- [ ] CSV generado tiene correcto número de columnas (23)
- [ ] Kieserita tiene CAS extraído correctamente (7487-88-9)
- [ ] Carbonato tiene frases H extraídas (H315, H320, H335)
- [ ] Silicato tiene campos faltantes marcados como "NA"
- [ ] Densidad de Kieserita: 2650 kg/m³
- [ ] Punto de fusión de Kieserita: 1127 °C
- [ ] DL50 oral de Kieserita: >5000 mg/kg
- [ ] Campos de primeros auxilios no vacíos para Kieserita y Carbonato
- [ ] Reporte de secciones faltantes es correcto

---

## 10. Siguiente Paso

Una vez completado este plan:
1. Validar datos en `output/hds_extraidas.json`
2. Corregir campos que necesiten ajuste manual
3. Buscar HDS completa del Silicato para completar datos faltantes
4. Incorporar datos a `datos/mp_sga.csv`
5. Probar script de generación HDS con los nuevos datos
