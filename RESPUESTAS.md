# Parte 2 — ¿Configurar o desarrollar?

## 1. Presupuestos largos por secciones (fabricante de maquinaria)

Desarrollo a medida, pero pequeño. En Odoo 19 el onchange de `sale_order_template_id` hace `Command.clear()` sobre las líneas: la plantilla siempre sustituye, por eso les borra el presupuesto. Haría un botón/asistente en el pedido que elija una plantilla y *añada* sus líneas (con sus secciones) al final, sin tocar las existentes; `sale.order.template` se reutiliza como definición del bloque. Antes preguntaría: ¿los bloques varían por cliente/tarifa o son fijos?, ¿los precios salen de la plantilla o de la tarifa vigente?, ¿quién mantiene los bloques y cuántos hay? Si el bloque fuera siempre el mismo y el resultado no importara, valoraría un producto kit/combo.

## 2. Lotes en el TPV (alimentación con tiendas)

Configuración estándar. El TPV solo pide lote/serie si el tipo de operación del TPV ("PoS Orders") tiene activas "Usar lotes existentes" o "Crear nuevos lotes" (`use_existing_lots`/`use_create_lots`): basta desmarcarlas en Inventario → Tipos de operación. Las recepciones son otro tipo de operación y allí el lote sigue siendo obligatorio, igual que en producción. La salida de stock la resuelve Odoo por estrategia de retirada; recomendaría FEFO en las ubicaciones de tienda por la caducidad. Preguntaría: ¿aceptan no conocer el lote exacto vendido en tienda (trazabilidad/recalls) o lo necesitan también ahí?

## 3. Importación de 4.000 NIF rechazados

Ni desactivar la validación ni un script como primera opción. `base_vat` valida según el país del contacto (o el prefijo del NIF); si el Excel no trae `country_id`, se valida contra España y de ahí los rechazos masivos de CL/MX/CO. Solución: añadir la columna País a la importación, normalizar formatos (guiones, prefijos ISO) y reintentar; el remanente suele ser NIF realmente incorrectos o identificadores de persona física, que se tratan en una lista corta. Preguntaría una muestra de errores reales, si hay personas físicas (RUT/RFC/cédulas) y si facturan desde España (impacta en cómo se declara el ID: NIF-IVA vs IDOtro). Si aun así hubiera que cargar excepciones, existe el contexto `no_vat_validation`, pero para casos puntuales, no para los 4.000.
