# Parte 2 — ¿Configurar o desarrollar?

## 1. Fabricante de maquinaria: añadir un bloque al final del presupuesto
- **Desarrollo a medida, pequeño.** En Odoo 19 elegir una plantilla ejecuta `Command.clear()`: siempre reemplaza las líneas.
- Cómo: botón "Añadir bloque" que copia al final las líneas de una plantilla (sección + productos) sin tocar las existentes.
- Las plantillas (`sale.order.template`) siguen siendo el catálogo de bloques: sin modelos nuevos y las mantiene el cliente.
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
