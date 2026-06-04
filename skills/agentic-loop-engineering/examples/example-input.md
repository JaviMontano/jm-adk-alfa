# Example Input

Tengo un agente en Python sobre el SDK de Anthropic que a veces se queda colgado y otras veces termina antes de tiempo. El control actual lee el texto de la respuesta y sale cuando encuentra la palabra "done". Necesito reconstruir el bucle para que enrute por la señal de parada del modelo, despache las herramientas correctamente y nunca pueda quedarse en bucle infinito. El mapa de handlers es `{"search": run_search, "read_file": run_read_file}` y quiero un techo de 20 iteraciones.
