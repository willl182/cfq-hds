# CFQ-HDS

Sistema de generacion de Hojas de Datos de Seguridad (HDS) para Calferquim.

## Descripcion

Genera automaticamente documentos de seguridad para fertilizantes granulados siguiendo el Sistema Globalmente Armonizado (SGA/GHS):

- Hojas de Datos de Seguridad (16 secciones)
- Etiquetas SGA
- Tarjetas de emergencia

## Requisitos

- Python 3.10+
- Jinja2
- Pandoc (opcional, para Word/PDF)

## Uso

```bash
# Generar HDS para un producto
python scripts/generar_hds.py --producto 1080

# Generar todos los productos
python scripts/generar_hds.py --todos
```

## Estructura de Datos

Los datos se mantienen en archivos CSV en `datos/`:

| Archivo | Contenido |
|---------|-----------|
| `mp_sga.csv` | Materias primas con clasificacion SGA |
| `frases_hp.csv` | Catalogo de frases H y P |
| `recetas.csv` | Formulaciones de productos |
| `info_corp.csv` | Datos corporativos |

## Licencia

Uso interno Calferquim.
