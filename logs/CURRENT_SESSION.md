# Session State: Sistema de Hojas de Datos de Seguridad (HDS) - Calferquim

**Last Updated**: 2026-02-04 20:57

## Session Objective

Planificar, diseñar e implementar un sistema automatizado para generar Hojas de Seguridad (HDS/SDS) de fertilizantes granulados a partir de una base de datos de materias primas.

## Current State

- [x] Evaluar plan existente e insumos
- [x] Crear plan consolidado del sistema (`plan_hds.md`)
- [x] Generar guía práctica de GitHub CLI (`git_cli.md`)
- [x] Renombrar rama a `main` y configurar estándar
- [x] Crear repositorio privado en GitHub vía CLI
- [x] Implementar estructura de directorios del proyecto
- [x] Crear plantillas CSV base para la base de datos maestra

- [ ] Consolidar CSVs en un único archivo Excel `base_hds.xlsx`
- [ ] Poblar base de datos con información real de 3-5 MP piloto
- [ ] Desarrollar script principal de generación (`scripts/generar_hds.py`)
- [ ] Crear plantillas Jinja2 para Markdown

## Critical Technical Context

### Estructura de Datos
- Ubicación: `datos/`
- Archivos: `mp_sga.csv`, `frases_hp.csv`, `recetas.csv`, `info_corp.csv`
- Se recomienda unificar estos en un Excel con 4 pestañas para facilitar el mantenimiento.

### Repositorio GitHub
- URL: https://github.com/willl182/cfq-hds
- Protocolo: SSH
- Rama principal: `main`

## Next Steps

1. **Datos**: Unificar CSVs en `base_hds.xlsx`.
2. **Piloto**: Cargar datos de Urea, KCl y Sulfato de Zinc.
3. **Desarrollo**: Escribir script de lectura de Excel y combinación GHS.
4. **Plantillas**: Diseñar el layout de la HDS en Markdown.

