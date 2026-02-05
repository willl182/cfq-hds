# AGENTS.md

## Descripcion del Proyecto

Sistema de generacion automatica de Hojas de Datos de Seguridad (HDS) para Calferquim, empresa colombiana de fertilizantes granulados. El sistema aplica reglas del Sistema Globalmente Armonizado (SGA/GHS) para clasificar mezclas fisicas.

## Estructura del Proyecto

```
cfq_hds/
├── datos/              # Base de datos CSV
│   ├── mp_sga.csv      # Materias primas con datos SGA
│   ├── frases_hp.csv   # Catalogo de frases H y P
│   ├── recetas.csv     # Formulaciones de productos
│   └── info_corp.csv   # Datos de la empresa
├── scripts/            # Scripts Python de generacion
├── plantillas/         # Templates Jinja2 para HDS
├── output/             # Documentos generados
│   ├── hds/            # Hojas de Datos de Seguridad
│   ├── etiquetas/      # Etiquetas SGA
│   └── emergencia/     # Tarjetas de emergencia
├── red_hds/            # Insumos de referencia
│   └── guia_hds/       # Guias tecnicas por seccion
└── logs/               # Historial de sesiones
```

## Tecnologias

- Python 3.13 con modulo `csv` nativo
- Jinja2 para templates
- Pandoc para conversion a Word/PDF
- Git/GitHub CLI para versionamiento

## Contexto Regulatorio

- Sistema Globalmente Armonizado (SGA/GHS) Rev. 8
- NTC 4435 (Colombia)
- Decreto 1609 de 2002 (Transporte)
- Las mezclas fisicas se clasifican usando el metodo convencional

## Convenios de Codigo

- Idioma: Espanol (sin tildes en nombres de archivos)
- Rama principal: `main`
- CSVs usan coma como delimitador
- Plantillas usan sintaxis Jinja2

## Tareas Pendientes

1. Poblar datos de materias primas en mp_sga.csv
2. Crear script generar_hds.py
3. Implementar logica de clasificacion SGA para mezclas
4. Generar HDS de prueba
