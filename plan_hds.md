# Plan del Sistema de Hojas de Datos de Seguridad (HDS) - Calferquim

## 1. Visión General del Sistema

Este sistema permite generar Hojas de Seguridad (HDS/SDS) para materias primas y productos terminados de fertilizantes granulados a partir de una base de datos centralizada. El enfoque aprovecha que los productos terminados son mezclas físicas sin transformación química, por lo cual la HDS de un producto se deriva de la "suma" de las HDS de sus componentes según las reglas del Sistema Globalmente Armonizado (SGA/GHS).

```
                     ┌─────────────────────────────────────┐
                     │   BASE DE DATOS MAESTRA (Excel)   │
                     │ ┌─────────────────────────────────┐ │
                     │ │  Hoja: MP_SGA                  │ │
                     │ │  (Datos SGA por materia prima)    │ │
                     │ ├─────────────────────────────────┤ │
                     │ │  Hoja: Frases_HP                 │ │
                     │ │  (Catálogo de frases H y P)      │ │
                     │ ├─────────────────────────────────┤ │
                     │ │  Hoja: Recetas                   │ │
                     │ │  (Formulaciones con % de MP)     │ │
                     │ ├─────────────────────────────────┤ │
                     │ │  Hoja: Info_Corporativa            │ │
                     │ │  (Datos empresa, teléfonos)        │ │
                     │ └─────────────────────────────────┘ │
                     └─────────────────┬───────────────────┘
                                       │
                                       ▼
                     ┌─────────────────────────────────────┐
                     │        MOTOR DE GENERACIÓN           │
                     │  (Script Python + Jinja2 + Pandoc)  │
                     │                                     │
                     │  1. Lee receta del producto         │
                     │  2. Combina datos SGA de cada MP    │
                     │  3. Aplica reglas de mezcla GHS     │
                     │  4. Genera Markdown                 │
                     │  5. Convierte a Word/PDF            │
                     └─────────────────┬───────────────────┘
                                       │
                     ┌─────────────────┴───────────────────┐
                     │                                     │
                     ▼                 ▼                   ▼
              ┌───────────┐     ┌───────────┐      ┌───────────┐
              │    HDS    │     │  Etiqueta │      │  Tarjeta  │
              │   Word    │     │    SGA    │      │ Emergencia│
              │    PDF    │     │   Word    │      │   Word    │
              └───────────┘     └───────────┘      └───────────┘
```

---

## 2. Estructura de Archivos

```
sistema_hds/
├── datos/
│   └── base_hds.xlsx              # Base de datos maestra
│       ├── [Hoja] MP_SGA          # Datos SGA de materias primas
│       ├── [Hoja] Frases_HP       # Catálogo de frases H y P
│       ├── [Hoja] Recetas         # Formulaciones (COD, componentes, %)
│       ├── [Hoja] Info_Corp       # Datos corporativos
│       └── [Hoja] Config          # Textos estándar por sección
│
├── plantillas/
│   ├── template_hds_mp.md         # Plantilla HDS para materias primas
│   ├── template_hds_pt.md         # Plantilla HDS para productos terminados
│   ├── template_etiqueta.md       # Plantilla etiqueta SGA
│   ├── template_emergencia.md     # Plantilla tarjeta de emergencia
│   └── reference.docx             # Estilos Word para Pandoc
│
├── output/
│   ├── hds/                       # HDS generadas (Word/PDF)
│   ├── etiquetas/                 # Etiquetas SGA
│   └── emergencia/                # Tarjetas de emergencia
│
├── scripts/
│   ├── generar_hds.py             # Script principal de generación
│   ├── combinar_peligros.py       # Lógica de combinación GHS para mezclas
│   └── utils.py                   # Funciones auxiliares
│
└── docs/
    └── guia_usuario.md            # Documentación del sistema
```

---

## 3. Esquema de la Base de Datos (`base_hds.xlsx`)

### Hoja: `MP_SGA` (Materias Primas)

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| COD | Código de la MP | 12 |
| NOMBRE | Nombre comercial | Urea |
| CAS | Número CAS | 57-13-6 |
| FORMULA | Fórmula química | CH4N2O |
| CLASIFICACION | Clasificación GHS (texto libre) | - |
| FRASES_H | Códigos H separados por ; | - |
| FRASES_P | Códigos P separados por ; | P264;P280 |
| PICTOGRAMAS | Códigos GHS separados por ; | - |
| PALABRA_SEÑAL | Peligro/Atención/- | - |
| PUNTO_FUSION | Punto de fusión °C | 132-135 |
| DENSIDAD | Densidad g/cm³ | 1.32 |
| SOLUBILIDAD | Solubilidad en agua (g/L) | 1080 |
| PPE_RESP | EPP respiratorio | Polvo: mascarilla N95 |
| PPE_MANOS | EPP manos | Guantes de látex |
| PPE_OJOS | EPP ojos | Gafas de seguridad |
| PRIMEROS_AUX_ING | Primeros auxilios ingestión | Enjuagar boca, no inducir vómito |
| PRIMEROS_AUX_PIEL | Primeros auxilios piel | Lavar con agua y jabón |
| PRIMEROS_AUX_OJOS | Primeros auxilios ojos | Enjuagar 15 min |
| PRIMEROS_AUX_INH | Primeros auxilios inhalación | Aire fresco |
| ALMACENAMIENTO | Condiciones de almacenamiento | Lugar fresco y seco |
| INCOMPATIBLES | Materiales incompatibles | Oxidantes fuertes |
| ECOTOXICIDAD | Información ambiental | Bajo riesgo acuático |
| FUENTE_HDS | Referencia de la HDS original | Proveedor X, fecha |

### Hoja: `Frases_HP` (Catálogo)

| Campo | Descripción |
|-------|-------------|
| CODIGO | H200, H302, P280, etc. |
| TIPO | H, P, EUH |
| TEXTO_ES | Texto en español |
| CATEGORIA | Física, Salud, Ambiental, General, Prevención, Respuesta, Almacenamiento, Eliminación |

### Hoja: `Recetas`

| Campo | Descripción |
|-------|-------------|
| COD_PT | Código producto terminado |
| NOMBRE_PT | Nombre del producto |
| COD_MP1 | Código MP 1 |
| PORC_MP1 | Porcentaje MP 1 |
| COD_MP2 | Código MP 2 |
| PORC_MP2 | Porcentaje MP 2 |
| ... | (hasta 10 componentes) |

### Hoja: `Info_Corp`

| Campo | Descripción |
|-------|-------------|
| RAZON_SOCIAL | Nombre legal de la empresa |
| DIRECCION | Dirección física completa |
| TELEFONO_EMERGENCIA | Número 24/7 |
| EMAIL_CONTACTO | Email para consultas |
| PAIS | País de operación |
| ID_INTERNO | Identificador interno |

---

## 4. Reglas de Combinación para Mezclas (SGA/GHS)

Para productos terminados que son mezclas físicas sin transformación química:

### 4.1 Frases H (Peligros)

1. **Incluir todas las frases H** de componentes con concentración ≥ 1%
2. **Componentes CMR** (H340, H350, H360): reportar si ≥ 0.1%
3. **No duplicar** frases H idénticas en la mezcla
4. **Ordenar** por código de frase para consistencia

### 4.2 Frases P (Consejos de prudencia)

1. Seleccionar las frases P pertinentes a los peligros presentes
2. Máximo 6 frases P (priorizar las más relevantes)
3. Incluir mínimo: P102, P103, P261, P264, P270, P280 (si aplica)

### 4.3 Pictogramas

1. Unión de pictogramas de componentes peligrosos
2. Máximo 5 pictogramas por etiqueta
3. **Jerarquía de precedencia**:
   - GHS05 (Corrosión) > GHS07 (Advertencia)
   - GHS06 (Calavera y huesos) > GHS08 (Peligro para la salud)
   - GHS02 (Llama) tiene prioridad sobre otros de inflamabilidad

### 4.4 Palabra de Señal

- **PELIGRO**: Si algún componente tiene clasificación de "Peligro"
- **ATENCIÓN**: Si ningún componente tiene "Peligro" pero alguno tiene "Atención"
- **-**: Si no hay componentes clasificados

### 4.5 Sección 3 (Composición)

1. Listar componentes peligrosos ≥ 1%
2. Listar componentes CMR ≥ 0.1%
3. Usar rangos de concentración permitidos (ej: 10-20%)
4. Incluir nombre químico, CAS, y tipo de clasificación

---

## 5. Fases de Implementación

| Fase | Descripción | Entregables | Duración Estimada |
|------|-------------|-------------|-------------------|
| **1. Datos Base** | Crear estructura Excel, poblar catálogo de frases H/P | `base_hds.xlsx` con Frases_HP y estructura | 1 día |
| **2. MP Piloto** | Procesar 3-5 HDS de MP existentes, revisar esquema juntos | Datos de MP en Excel, validar campos | 2-3 días |
| **3. MP Principales** | Completar las ~20-30 MP más usadas (urea, KCl, DAP, MAP, kieserita, etc.) | Base de MP completa | 1-2 semanas |
| **4. Motor Generación** | Scripts Python para generar HDS desde la base | Scripts funcionales | 1 semana |
| **5. Plantillas** | Plantillas Markdown + estilos Word | Templates listos | 3-5 días |
| **6. PT Piloto** | Generar 5-10 HDS de productos terminados, revisar | HDS de prueba | 2-3 días |
| **7. Etiquetas** | Agregar generación de etiquetas SGA | Etiquetas funcionales | 2-3 días |
| **8. Tarjetas Emergencia** | Agregar generación de tarjetas | Tarjetas funcionales | 1-2 días |
| **9. Documentación** | Guía de uso del sistema | Manual de usuario | 2-3 días |

---

## 6. Productos de Mayor Riesgo a Evaluar

Basándome en el catálogo de materias primas y conocimiento de fertilizantes, estos productos requieren atención especial durante la carga de datos:

| Producto | Razón | Clasificación esperada | Prioridad |
|----------|-------|----------------------|-----------|
| **Sulfato de Zinc** | Toxicidad aguda, irritante, ecotoxicidad acuática | H302, H315, H319, H410 | Alta |
| **Ácido Bórico** | Toxicidad reproductiva | H360FD | Alta |
| **Sulfato de Cobre** | Irritante, tóxico acuático | H302, H315, H318, H410 | Media |
| **Sulfato de Manganeso** | Irritante | H302, H315, H319 | Media |
| **SAM (Sulfato de Amonio)** | Puede ser irritante en alta concentración | H319 | Baja |
| **Urea** | Generalmente no clasificada, verificar proveedor | - | Baja |
| **KCl** | Generalmente no clasificado, verificar proveedor | - | Baja |
| **DAP** | Puede tener irritación leve | H319 | Baja |
| **MAP** | Puede tener irritación leve | H319 | Baja |

**Nota**: La mayoría de las materias primas base (urea, KCl, DAP, MAP, carbonatos, silicatos, bentonitas) tienen bajo riesgo según el SGA, pero es crítico obtener las HDS oficiales de cada proveedor para confirmar su clasificación específica.

---

## 7. Características del Sistema

### 7.1 Idioma
- Todas las HDS se generarán en **español**
- Base de datos en español
- Textos estándar por sección en español
- Posibilidad futura de generar en inglés (opcional)

### 7.2 Formatos de Salida
- **Word (.docx)**: Para edición posterior (formato estándar comercial)
- **PDF**: Para distribución final
- Las plantillas Markdown se convierten a Word usando Pandoc

### 7.3 Funcionalidades Incluidas

1. **Generación de HDS**:
   - Materias primas: a partir de datos directos
   - Productos terminados: a partir de combinación de componentes

2. **Generación de Etiquetas SGA**:
   - Pictogramas
   - Palabra de señal
   - Frases H y P resumidas
   - Información de identificación

3. **Generación de Tarjetas de Emergencia**:
   - Información clave de identificación
   - Primeros auxilios principales
   - Medidas de contención
   - Formato portátil para operarios

### 7.4 Mantenimiento de la Base de Datos

- **Excel (.xlsx)**: Formato fácil de mantener y editar
- Múltiples hojas organizadas por función
- Fácil exportación a CSV si se requiere
- Compatible con herramientas de BI (Power BI, Excel estándar)

---

## 8. Secciones de las HDS Generadas

Todas las HDS incluirán las 16 secciones estándar del SGA:

1. Identificación de la sustancia y del fabricante
2. Identificación de los peligros
3. Composición/información sobre los componentes
4. Primeros auxilios
5. Medidas de lucha contra incendios
6. Medidas en caso de vertido accidental
7. Manipulación y almacenamiento
8. Controles de exposición/protección personal
9. Propiedades físicas y químicas
10. Estabilidad y reactividad
11. Información toxicológica
12. Información ecológica
13. Consideraciones relativas a la eliminación
14. Información relativa al transporte
15. Información reglamentaria
16. Otra información

Para fertilizantes de bajo riesgo, las secciones se simplificarán con textos estándar cuando aplique.

---

## 9. Próximos Pasos Inmediatos

1. **Suministrar las HDS de MP disponibles** (PDF/Word)
   - Empezar con 3-5 para piloto
   - Priorizar: urea, KCl, DAP, MAP, kieserita, sulfato de zinc

2. **Proporcionar datos corporativos** para la Sección 1
   - Razón social
   - Dirección física
   - Teléfono de emergencia 24/7
   - Email de contacto

3. **Lista de prioridad de productos terminados**
   - Orden por volumen de producción
   - Orden por ventas
   - Criterio de urgencia comercial

4. **Validación del esquema de base de datos**
   - Ajustar campos según HDS piloto
   - Confirmar reglas de combinación
   - Definir textos estándar por sección

---

## 10. Tecnología Propuesta

### 10.1 Lenguajes y Herramientas
- **Python 3.x**: Script principal de generación
- **Jinja2**: Motor de plantillas para Markdown
- **Pandoc**: Conversión Markdown → Word/PDF
- **openpyxl / pandas**: Lectura de base de datos Excel

### 10.2 Dependencias Principales
```
openpyxl>=3.1.0
pandas>=2.0.0
jinja2>=3.1.0
weasyprint>=60.0  # opcional para PDF directo
pypandoc>=1.13
```

### 10.3 Flujo de Generación (PT - Producto Terminado)

```
1. Leer receta de `Recetas` por COD_PT
2. Para cada componente en la receta:
   a. Buscar datos SGA en `MP_SGA` por COD_MP
   b. Acumular frases H, P y pictogramas
3. Aplicar reglas de combinación GHS:
   - Eliminar duplicados
   - Aplicar umbrales (1%, 0.1%)
   - Seleccionar top 5 pictogramas
   - Determinar palabra de señal
4. Renderizar plantilla `template_hds_pt.md` con datos
5. Convertir Markdown a Word con Pandoc
6. Guardar en `output/hds/`
```

---

## 11. Notas de Calidad y Compliance

### 11.1 Cumplimiento Regulatorio
- NOM-018-STPS-2015 (México): Estándar SGA en español
- SGA/GHS global: Clasificación armonizada
- REACH (Europa): Referencia para clasificaciones de componentes

### 11.2 Validación
- Cruzar CAS con ECHA/ESIS
- Verificar consistencia S2 ↔ S3 ↔ S8
- Confirmar pictogramas correctos
- Validar número de emergencia funcional

### 11.3 Trazabilidad
- Cada HDS generada debe incluir fecha de generación
- Versión de la base de datos utilizada
- Referencia a HDS de origen de cada MP

---

## 12. Oportunidades de Mejora Futura

1. **Bilingüismo**: Capacidad de generar HDS en inglés para exportación
2. **Validación automática**: Scripts para cruzar datos con ECHA
3. **Interfaz gráfica**: Aplicación web para facilitar uso no técnico
4. **Integración con ERP**: Importar recetas directamente del sistema de producción
5. **e-SDS**: Generación de SDS ampliadas con escenarios de exposición

---

## Apéndice A: Referencia de Frases H Principales para Fertilizantes

| Código | Texto | Categoría | Típico en Fertilizantes |
|-------|---------|------------|------------------------|
| H302 | Nocivo en caso de ingestión | Toxicidad aguda | Sulfato de zinc, ácido bórico |
| H315 | Provoca irritación cutánea | Irritación piel | Sulfatos de micronutrientes |
| H318 | Provoca lesiones oculares graves | Irritación ojos | Sulfatos de micronutrientes |
| H319 | Provoca irritación ocular | Irritación ojos | SAM, DAP, MAP |
| H360FD | Puede perjudicar a la fertilidad. Puede dañar al feto | Reproductividad | Ácido bórico |
| H410 | Muy tóxico para los organismos acuáticos, con efectos nocivos duraderos | Ambiental | Sulfato de zinc |

---

## Apéndice B: Referencia de Frases P Principales

| Código | Texto | Categoría | Uso recomendado |
|-------|---------|------------|-----------------|
| P102 | Mantener fuera del alcance de los niños | General | Siempre |
| P103 | Leer la etiqueta antes del uso | General | Siempre |
| P261 | Evitar respirar el polvo | Prevención | Sólidos granulados |
| P264 | Lavarse concienzudamente tras la manipulación | Prevención | Siempre |
| P270 | No comer, beber ni fumar durante su utilización | Prevención | Siempre |
| P280 | Llevar guantes/prendas/gafas/máscara de protección | Prevención | Según riesgo |
| P305 | EN CASO DE CONTACTO CON LOS OJOS | Respuesta | Si aplica H318 |
| P337 | Si persiste la irritación ocular | Respuesta | Si aplica H319 |

---

**Documento creado**: 2026-02-04
**Versión**: 1.0
**Estado**: Planificación inicial pendiente validación
