# Session State: Sistema de Hojas de Datos de Seguridad (HDS) - Calferquim

**Last Updated**: 2026-02-04 23:33

## Session Objective

Generar HDS de productos a partir de MP y recetas, y completar la primera HDS de Camasi Gris 62.

## Current State

- [x] Extraer datos de 3 HDS existentes a JSON/CSV y ajustar parsers
- [x] Actualizar mp_sga.csv con MP 74/105/274 y datos base
- [x] Implementar generador de HDS en Markdown con Jinja2
- [x] Generar HDS para Camasi Gris 62 (receta)
- [ ] Revisar la plantilla HDS para ajustes de contenido/estilo
- [ ] Definir si se usa LISTA 4 o LISTA 0 para Camasi Gris 62

## Critical Technical Context

- Script de extracción: `scripts/extraer_hds.py` (lee Excel via zipfile/xml)
- Generador HDS: `scripts/generar_hds.py`
  - `--cods` genera por MP
  - `--receta-cod` genera por receta y suma frases H/P de todas las MP
- Archivos clave: `datos/mp_sga.csv`, `datos/recetas.csv`, `red_hds/listas.csv`
- HDS receta 62: `output/hds/HDS_62_62_nucleo_camasi_gris_calferquim_1_g.md`

## Next Steps

1. Revisar contenido de HDS receta 62 y ajustar plantilla si aplica.
2. Confirmar lista (4 vs 0) para Camasi Gris 62.
3. Generar HDS de otras recetas si se requiere.
