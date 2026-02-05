# Plan Sistema HDS (Calferquim)

## Contexto y alcance
- Productos: materias primas (MP) y productos terminados (PT) de fertilizantes granulados.
- Riesgo general: bajo; excepcion principal: sulfato de zinc.
- Norma: SGA/GHS, 16 secciones.
- Formato: Markdown -> Pandoc -> Word.
- Guia base: `guia_hds/` (secciones S1-S16 + frases H/P).

## Objetivo
1. Organizar HDS de materias primas base.
2. Derivar HDS de productos terminados a partir de formulaciones.

## Estructura del sistema
```
sistema_hs/
├── datos/
│   ├── materias_primas_sga.csv
│   ├── formulaciones.csv
│   └── frases_hp.csv
├── plantillas/
│   ├── template_hs_mp.md
│   ├── template_hs_pt.md
│   └── reference.docx
├── output/
│   ├── mp/
│   └── pt/
└── scripts/
    ├── generar_hs.py
    └── combinar_peligros.py
```

## Flujo de trabajo
1. Completar `materias_primas_sga.csv` con datos SGA de MP.
2. Cargar `formulaciones.csv` con % por MP para cada PT.
3. Generar HDS MP con plantilla Markdown (SGA 16 secciones).
4. Combinar peligros para PT y generar HDS PT.
5. Convertir Markdown a Word con Pandoc.

## Criterios de combinacion (mezclas)
- Reportar componentes >= 1% (salvo CMR u otros requisitos especiales).
- Frases H: union de las MP aplicables.
- Frases P: seleccionar las pertinentes a los peligros de la mezcla.
- Pictogramas: maximo 5, priorizando mayor severidad.

## Simplificacion para fertilizantes
- Mantener 16 secciones, con contenido simplificado donde aplique:
  - S2, S4, S5, S6, S7, S8, S11, S12 con texto estandar para solidos no peligrosos.
  - Detalle completo solo para MP con peligrosidad (ej. sulfato de zinc).

## Prioridades
1. HDS de MP base (urea, KCL, SAM, DAP, MAP, kieserita, carbonatos, bentonitas, silicatos, sulfatos, etc.).
2. HDS PT derivados segun lista priorizada de produccion/ventas.

## Insumos requeridos del usuario
- Archivo de formulaciones (Excel) con recetas por PT.
- Datos corporativos para Seccion 1 (empresa, direccion, correo, telefono emergencia).
- Lista priorizada de MP a documentar primero.

## Entregables
- Plantillas Markdown para MP y PT.
- HDS MP en Markdown/Word.
- HDS PT en Markdown/Word.
