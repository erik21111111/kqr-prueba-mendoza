# Parte 2 — ¿Configurar o desarrollar?

## 1. Fabricante de maquinaria: añadir un bloque al final del presupuesto
- **Módulo existente (OCA).** En Odoo 19 elegir una plantilla ejecuta `Command.clear()`: siempre reemplaza las líneas.
- `sale_multi_template_application` (OCA/sale-workflow, Tecnativa) aplica varias plantillas conservando las líneas existentes.
- Publicado para 17.0/18.0; en 19.0 su migración es un PR abierto (#4473): lo probaría y, si hace falta, completaría la migración.
- Si no encajara, el desarrollo sería pequeño: heredar ese onchange para añadir las líneas al final en vez de reemplazarlas.
- Preguntaría: ¿precio de la plantilla o de la tarifa del cliente?, ¿solo al final o en cualquier posición?, ¿cuántos bloques hay?

## 2. Alimentación con tiendas: que el TPV no pida lote
- **Configuración estándar.** El TPV solo pide lote si su tipo de operación ("PoS Orders") tiene activadas las opciones de lotes.
- Cómo: Inventario → Configuración → Tipos de operación → PoS Orders → desmarcar "usar lotes existentes" y "crear lotes nuevos".
- Recepciones y fabricación son otros tipos de operación, así que allí el lote sigue siendo obligatorio.
- Al vender, Odoo asigna el lote según la estrategia de retirada; para alimentación recomendaría FEFO (sale antes lo que caduca antes).
- Preguntaría: ¿les vale que el lote registrado sea el asignado por FEFO y no el físico? Importa si hay que retirar un lote.

## 3. Migración de CRM: NIF de Chile, México y Colombia rechazados
- **Ni desactivar la validación ni script: limpiar los datos e importar con la herramienta estándar.**
- `base_vat` valida cada NIF con el algoritmo oficial del país del contacto (sin país no valida): "correcto en origen" no basta.
- Lo típico: NIT colombiano o RUT chileno guardados sin dígito verificador, CURP o cédula de persona física en vez del NIF, país erróneo.
- Cómo: "Probar" en el importador para listar rechazos, corregirlos en el Excel y reimportar; `no_vat_validation` solo para excepciones.
- Preguntaría: ¿se les factura desde Odoo (el NIF debe ser válido en factura y declaraciones)?, ¿hay personas físicas?, ¿qué trae el Excel?
