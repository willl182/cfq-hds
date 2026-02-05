# Session State: Sistema de Hojas de Datos de Seguridad (HDS) - Calferquim

**Last Updated**: 2026-02-04 20:08

## Session Objective

Planificar, diseñar e implementar un sistema automatizado para generar Hojas de Seguridad (HDS/SDS) de fertilizantes granulados a partir de una base de datos de materias primas, aplicando las reglas del Sistema Globalmente Armonizado (SGA/GHS) para mezclas físicas.

## Current State

- [x] Evaluar plan existente (`sistema_hs.md`)
- [x] Analizar archivos de datos (`listado_mp_pt.csv`, `listas.csv`)
- [x] Revisar guía HDS (16 secciones + frases H/P)
- [x] Crear plan consolidado del sistema (`plan_hds.md`)
- [x] Aplicar skill saver para seguimiento del proyecto

- [ ] Crear repositorio GitHub
- [ ] Implementar estructura de archivos
- [ ] Crear base de datos maestra (Excel)
- [ ] Desarrollar scripts de generación
- [ ] Generar plantillas Markdown
- [ ] Procesar HDS piloto de materias primas
- [ ] Validar sistema con productos terminados

## Critical Technical Context

### Datos Disponibles
- **listado_mp_pt.csv**: ~634 productos/MP con composición química (N, P, K, Ca, Mg, S, B, etc.)
- **listas.csv**: ~37 recetas de productos terminados con componentes y porcentajes
- **guia_hds/**: 18 archivos con guías de cada sección SGA + frases H/P
- **Materias Primas Principales**: Urea, KCl, DAP, MAP, Kieserita, carbonatos, bentonitas, silicatos, sulfatos

### Productos de Alto Riesgo
- **Sulfato de Zinc**: Clasificación esperada H302, H315, H319, H410
- **Ácido Bórico**: Clasificación esperada H360FD (toxicidad reproductiva)
- **Sulfatos de micronutrientes** (cobre, manganeso): Irritación piel/ojos

### Formato Preferido
- Base de datos: Excel (.xlsx) para mantenimiento por personal no técnico
- Salida HDS: Word (.docx) para edición + PDF para distribución
- Idioma: Español
- Documentos adicionales: HDS + Etiquetas SGA + Tarjetas de emergencia (paquete completo)

### Estrategia de Generación
- Productos terminados = mezclas físicas sin transformación química
- HDS PT = suma ponderada de HDS de componentes según reglas GHS
- Umbrales: componentes ≥1%, CMR ≥0.1%
- Pictogramas: máximo 5, aplicar jerarquía GHS05>GHS07, GHS06>GHS08

## Next Steps

1. **Inmediato**: Crear repositorio GitHub para control de versiones
2. **Fase 1**: Crear estructura de directorios del sistema
3. **Fase 2**: Crear archivo Excel base_hds.xlsx con hojas estructura
4. **Fase 3**: Poblar catálogo de frases H y P en Excel
5. **Fase 4**: Procesar 3-5 HDS piloto de materias primas (extraer datos de PDF existentes)
6. **Fase 5**: Desarrollar scripts Python (generar_hds.py, combinar_peligros.py)
7. **Fase 6**: Crear plantillas Markdown con Jinja2
8. **Fase 7**: Generar primeras HDS de prueba y validar

## Datos Corporativos Requeridos

Para iniciar el sistema se necesita:
- Razón social de Calferquim
- Dirección física completa
- Teléfono de emergencia 24/7
- Email de contacto para consultas HDS

## Proceso de Revisión

Enfoque **iterativo**:
1. Revisar 2-3 HDS de MP piloto juntos
2. Ajustar esquema de base de datos según feedback
3. Escalar a resto de materias primas
4. Implementar generación de productos terminados

## Notas sobre GitHub

Opciones para crear repositorio:
- Opción A: Usar comando `gh` si se tienen credenciales configuradas
- Opción B: Crear en web (github.com) y luego conectar vía git/ssh
- Opción C: Crear repositorio privado desde consola usando `gh repo create`
