# KQR — Prueba técnica: SSCC en palets (Odoo 19)

## Decisiones
- `em_sscc_palet` añade `res.company.prefijo_gs1` (4–12 dígitos, GS1 GenSpecs §1.4.4) y `stock.package.sscc` (18 dígitos, solo lectura): extensión `0` + prefijo + serie + control mod-10 de GS1. Reutilizo `odoo.tools.barcode` (el dígito de control y el validador SSCC que ya usa el core) en vez de reimplementar el algoritmo.
- Una `ir.sequence` por compañía (`code = stock.package.sscc`), creada bajo demanda en el primer SSCC generado; la unicidad la garantiza `models.Constraint('UNIQUE(sscc)')` a nivel de base de datos, global entre compañías.
- La compañía del SSCC es la activa al crear el paquete (`package.company_id` se calcula desde el contenido y nace vacío). Sin prefijo configurado, `sscc` queda vacío para no bloquear los flujos estándar que crean paquetes.
- Suposición documentada: los prefijos del enunciado se solapan (8412345 ⊂ 841234567), así que una colisión es posible en teoría (serial 670000001 de A = serial 1 de B). La restricción la rechaza; si ocurriera en producción habría que confirmar los prefijos con el cliente.
- Código y textos del módulo en inglés; documentación en español.

## Uso de IA
Devin generó el módulo, los tests y esta documentación trabajando contra el código fuente local de Odoo 19, no desde memoria. Revisé las decisiones de diseño, el dígito de control contra el ejemplo oficial de GS1 y las respuestas de la Parte 2.

## Pendiente
Etiqueta PDF GS1-128 y asignación de SSCC a paquetes existentes (fuera de alcance); traducción es_ES; que `name` use el SSCC para aprovechar los informes estándar (`valid_sscc`); regenerar la serie ante una colisión en lugar de fallar.

## Tests
Comando (shell del build de Odoo.sh, Odoo 19.0+e): `odoo-bin -u em_sscc_palet --test-tags /em_sscc_palet --log-level=test --stop-after-init` → resultado: `0 failed, 0 error(s) of 5 tests` (test_company_a_sscc, test_company_b_sscc, test_gs1_public_example, test_sscc_empty_without_prefix, test_sscc_unique).
