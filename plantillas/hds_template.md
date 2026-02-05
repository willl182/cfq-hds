# HOJA DE DATOS DE SEGURIDAD
## Sistema Globalmente Armonizado (SGA/GHS)

---

## SECCION 1: IDENTIFICACION DEL PRODUCTO Y DE LA EMPRESA

| Campo | Información |
|-------|-------------|
| **Nombre del producto** | {{ producto.nombre }} |
| **Código interno** | {{ producto.codigo }} |
| **Uso identificado** | Fertilizante granulado para uso agrícola |
| **Restricciones de uso** | Solo para uso profesional agrícola |

### Datos del proveedor
| Campo | Información |
|-------|-------------|
| **Razón social** | {{ empresa.razon_social }} |
| **Dirección** | {{ empresa.direccion }} |
| **País** | {{ empresa.pais }} |
| **Teléfono emergencia 24h** | {{ empresa.telefono_emergencia }} |
| **Correo de contacto** | {{ empresa.email_contacto }} |

---

## SECCION 2: IDENTIFICACION DE PELIGROS

### 2.1 Clasificación de la mezcla
{% if clasificacion.peligros %}
{% for peligro in clasificacion.peligros %}
- {{ peligro }}
{% endfor %}
{% else %}
Esta mezcla física no está clasificada como peligrosa según los criterios SGA.
{% endif %}

### 2.2 Elementos de la etiqueta
| Elemento | Descripción |
|----------|-------------|
| **Pictogramas** | {{ clasificacion.pictogramas if clasificacion.pictogramas else "Ninguno" }} |
| **Palabra de advertencia** | {{ clasificacion.palabra_senal }} |

### 2.3 Indicaciones de peligro (Frases H)
{% if frases_h %}
{% for frase in frases_h %}
- **{{ frase.codigo }}**: {{ frase.texto }}
{% endfor %}
{% else %}
No aplica.
{% endif %}

### 2.4 Consejos de prudencia (Frases P)
{% if frases_p %}
{% for frase in frases_p %}
- **{{ frase.codigo }}**: {{ frase.texto }}
{% endfor %}
{% else %}
Mantener fuera del alcance de los niños.
{% endif %}

### 2.5 Otros peligros
No se conocen otros peligros.

---

## SECCION 3: COMPOSICION/INFORMACION SOBRE LOS COMPONENTES

### 3.1 Composición de la mezcla

| Componente | No. CAS | Fórmula | Concentración (%) | Clasificación |
|------------|---------|---------|-------------------|---------------|
{% for comp in componentes %}
| {{ comp.nombre }} | {{ comp.cas }} | {{ comp.formula }} | {{ comp.porcentaje }} | {{ comp.clasificacion }} |
{% endfor %}

---

## SECCION 4: PRIMEROS AUXILIOS

### 4.1 Descripción de medidas de primeros auxilios

| Vía de exposición | Medida de primeros auxilios |
|-------------------|----------------------------|
| **Inhalación** | {{ primeros_auxilios.inhalacion }} |
| **Contacto con la piel** | {{ primeros_auxilios.piel }} |
| **Contacto con los ojos** | {{ primeros_auxilios.ojos }} |
| **Ingestión** | {{ primeros_auxilios.ingestion }} |

### 4.2 Síntomas y efectos principales
Puede causar irritación leve en piel, ojos y vías respiratorias en caso de exposición prolongada.

### 4.3 Indicación de atención médica inmediata
En caso de síntomas persistentes, consultar a un médico.

---

## SECCION 5: MEDIDAS DE LUCHA CONTRA INCENDIOS

### 5.1 Medios de extinción
- **Apropiados**: Agua pulverizada, espuma, CO2, polvo químico seco
- **No apropiados**: No utilizar chorro de agua directo

### 5.2 Peligros específicos
El producto no es inflamable. A altas temperaturas puede descomponerse liberando gases tóxicos.

### 5.3 Equipo de protección para bomberos
Equipo de respiración autónomo (ERA) y traje de protección completo.

---

## SECCION 6: MEDIDAS EN CASO DE VERTIDO ACCIDENTAL

### 6.1 Precauciones personales
Utilizar equipo de protección personal. Evitar el polvo.

### 6.2 Precauciones ambientales
Evitar que el producto llegue a desagües, cursos de agua o suelo.

### 6.3 Métodos de limpieza
Recoger mecánicamente en contenedores adecuados. Lavar el área con agua abundante.

---

## SECCION 7: MANIPULACION Y ALMACENAMIENTO

### 7.1 Precauciones para manipulación segura
- Evitar formación de polvo
- Lavarse las manos después de manipular
- No comer, beber ni fumar durante la manipulación

### 7.2 Condiciones de almacenamiento seguro
{{ almacenamiento if almacenamiento else "Almacenar en lugar fresco y seco, alejado de la luz solar directa." }}

### 7.3 Incompatibilidades
{{ incompatibles if incompatibles else "Mantener alejado de oxidantes fuertes." }}

---

## SECCION 8: CONTROLES DE EXPOSICION/PROTECCION PERSONAL

### 8.1 Parámetros de control
No se han establecido límites de exposición ocupacional específicos para este producto.

### 8.2 Controles de ingeniería
Ventilación local adecuada en áreas de trabajo cerradas.

### 8.3 Equipo de protección personal

| Tipo de protección | Especificación |
|-------------------|----------------|
| **Protección respiratoria** | {{ ppe.respiratoria }} |
| **Protección de manos** | {{ ppe.manos }} |
| **Protección ocular** | {{ ppe.ojos }} |
| **Protección corporal** | Ropa de trabajo apropiada |

---

## SECCION 9: PROPIEDADES FISICAS Y QUIMICAS

| Propiedad | Valor |
|-----------|-------|
| **Estado físico** | Sólido granulado |
| **Color** | Variable según formulación |
| **Olor** | Característico |
| **pH** | 6-8 (solución acuosa) |
| **Punto de fusión** | {{ propiedades.punto_fusion if propiedades.punto_fusion else "No determinado" }} |
| **Densidad aparente** | {{ propiedades.densidad if propiedades.densidad else "1.0-1.5 g/cm³" }} |
| **Solubilidad en agua** | {{ propiedades.solubilidad if propiedades.solubilidad else "Parcialmente soluble" }} |

---

## SECCION 10: ESTABILIDAD Y REACTIVIDAD

### 10.1 Reactividad
Estable bajo condiciones normales de uso.

### 10.2 Estabilidad química
Producto estable.

### 10.3 Posibilidad de reacciones peligrosas
No se conocen.

### 10.4 Condiciones a evitar
Temperaturas extremas, humedad excesiva.

### 10.5 Materiales incompatibles
{{ incompatibles if incompatibles else "Oxidantes fuertes" }}

### 10.6 Productos de descomposición peligrosos
A altas temperaturas puede liberar óxidos de nitrógeno.

---

## SECCION 11: INFORMACION TOXICOLOGICA

### 11.1 Información sobre efectos toxicológicos

| Vía de exposición | Efecto |
|-------------------|--------|
| **Toxicidad aguda oral** | Baja toxicidad |
| **Toxicidad aguda dérmica** | Baja toxicidad |
| **Toxicidad aguda inhalatoria** | Puede causar irritación |
| **Irritación cutánea** | Irritación leve posible |
| **Irritación ocular** | Irritación posible |
| **Sensibilización** | No conocida |

---

## SECCION 12: INFORMACION ECOLOGICA

### 12.1 Toxicidad
{{ ecotoxicidad if ecotoxicidad else "Puede causar eutrofización en cuerpos de agua si se libera en grandes cantidades." }}

### 12.2 Persistencia y degradabilidad
Los componentes son biodegradables.

### 12.3 Potencial de bioacumulación
Bajo potencial de bioacumulación.

### 12.4 Movilidad en el suelo
Alta movilidad debido a la solubilidad.

---

## SECCION 13: CONSIDERACIONES RELATIVAS A LA ELIMINACION

### 13.1 Métodos de tratamiento de residuos
- Eliminar conforme a la normativa local vigente
- No verter en desagües ni cursos de agua
- Los envases vacíos deben enjuagarse tres veces y disponerse según regulación local

---

## SECCION 14: INFORMACION RELATIVA AL TRANSPORTE

| Regulación | Información |
|------------|-------------|
| **ONU** | No regulado como mercancía peligrosa |
| **Clase ADR/RID** | No aplica |
| **Clase IMDG** | No aplica |
| **Clase IATA** | No aplica |

---

## SECCION 15: INFORMACION REGLAMENTARIA

### 15.1 Normatividad aplicable
- Resolución 1514 de 2012 (Colombia) - Listado de plaguicidas
- NTC 4435 - Transporte de mercancías peligrosas
- Decreto 1609 de 2002 - Transporte de mercancías peligrosas
- Sistema Globalmente Armonizado (SGA/GHS) Rev. 8

---

## SECCION 16: OTRA INFORMACION

| Campo | Información |
|-------|-------------|
| **Fecha de elaboración** | {{ fecha_elaboracion }} |
| **Versión** | {{ version }} |
| **Elaborado por** | {{ elaborado_por }} |

### Texto completo de frases H citadas
{% if frases_h %}
{% for frase in frases_h %}
- {{ frase.codigo }}: {{ frase.texto }}
{% endfor %}
{% else %}
No aplica.
{% endif %}

### Abreviaturas
- SGA: Sistema Globalmente Armonizado
- GHS: Globally Harmonized System
- CAS: Chemical Abstracts Service
- PPE: Personal Protective Equipment
- ADR: Acuerdo europeo sobre transporte de mercancías peligrosas por carretera

---

**EXENCIÓN DE RESPONSABILIDAD**: La información contenida en esta Hoja de Datos de Seguridad se basa en los datos disponibles a la fecha de elaboración y se proporciona de buena fe. Es responsabilidad del usuario determinar la idoneidad de esta información para sus propósitos específicos.
