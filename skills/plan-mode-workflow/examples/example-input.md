# Example Input

Entramos a un servicio de pagos que el agente no conoce. Hay que renombrar una columna de base de datos y ajustar tres handlers que la usan, pero el equipo exige aprobación firmada antes de cualquier escritura porque otro desarrollador tiene cambios sin commitear en el mismo módulo.

Solicitud: "Usa plan-mode-workflow para preparar el cambio en read-only, dame un plan firmable, y solo escribe cuando apruebe el plan exacto."
