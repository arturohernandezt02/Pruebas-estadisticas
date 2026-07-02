import os
import motor_estadistico as me
from gui_app import AppGenerador

class Controlador:
    def __init__(self, view: AppGenerador):
        self.view = view
        self.view.set_callbacks(self.generar_y_evaluar, self.exportar_configuracion)
        self.numeros_generados = []
        self.params_guardados = {}

    def generar_y_evaluar(self):
        valores = self.view.obtener_valores_entradas()
        
        # Validar entradas
        try:
            x0 = int(valores["x0"])
            a = int(valores["a"])
            c = int(valores["c"])
            m = int(valores["m"])
        except ValueError:
            self.view.mostrar_mensaje_error(
                "Error de Validación",
                "Todos los parámetros del generador (X0, a, c, m) deben ser números enteros."
            )
            return

        if m <= 0:
            self.view.mostrar_mensaje_error(
                "Error de Validación",
                "El módulo (m) debe ser un número entero mayor que 0."
            )
            return
            
        if x0 < 0 or a < 0 or c < 0:
            self.view.mostrar_mensaje_error(
                "Error de Validación",
                "La semilla (X0), la constante (a) y el incremento (c) deben ser enteros no negativos."
            )
            return

        # Generar números
        # Limitamos a 10,000 para evitar que la UI se congele con módulos muy grandes
        self.numeros_generados = me.generar_numeros(x0, a, c, m)
        n = len(self.numeros_generados)

        if n == 0:
            self.view.mostrar_mensaje_error(
                "Error de Generación",
                "No se pudieron generar números con las configuraciones dadas."
            )
            return

        # Formatear la lista de números en columnas para la pestaña "Números (Ri)"
        # Mostraremos un formato de tabla limpio de hasta 5 columnas
        cols = 5
        lineas_numeros = [
            "=== CONJUNTO DE NÚMEROS GENERADOS (Ri) ===",
            f"Fórmula: X_{{i+1}} = ({a} * X_i + {c}) % {m}",
            f"Semilla inicial X0: {x0}",
            f"Cantidad de números generada: {n}\n",
        ]
        
        for i in range(0, n, cols):
            chunk = self.numeros_generados[i:i+cols]
            col_strs = [f"R[{i+idx+1:d}]: {val:.5f}" for idx, val in enumerate(chunk)]
            lineas_numeros.append(" | ".join(col_strs))
            
        texto_numeros = "\n".join(lineas_numeros)
        self.view.actualizar_resultados_tab("numeros", texto_numeros)

        # Ejecutar pruebas
        paso_prom, _, _, _, det_prom = me.prueba_promedios(self.numeros_generados)
        paso_frec, _, _, _, det_frec = me.prueba_frecuencias(self.numeros_generados)
        paso_pok, _, _, _, det_pok = me.prueba_poker(self.numeros_generados)
        paso_corr, _, _, _, _, _, _, _, det_corr = me.prueba_corridas(self.numeros_generados)

        # Actualizar las pestañas con los reportes detallados
        self.view.actualizar_resultados_tab("promedios", det_prom)
        self.view.actualizar_resultados_tab("frecuencias", det_frec)
        self.view.actualizar_resultados_tab("poker", det_pok)
        self.view.actualizar_resultados_tab("corridas", det_corr)

        # Actualizar Badges
        self.view.actualizar_badge("promedios", paso_prom)
        self.view.actualizar_badge("frecuencias", paso_frec)
        self.view.actualizar_badge("poker", paso_pok)
        self.view.actualizar_badge("corridas", paso_corr)

        # Guardar parámetros válidos si todas las pruebas pasan
        todas_pasan = paso_prom and paso_frec and paso_pok and paso_corr
        
        if todas_pasan:
            self.params_guardados = {
                "x0": x0,
                "a": a,
                "c": c,
                "m": m
            }
            self.view.habilitar_exportacion(True)
            print(">> ¡Éxito! Todas las pruebas pasaron. Botón 'Exportar Configuración' habilitado.")
        else:
            self.params_guardados = {}
            self.view.habilitar_exportacion(False)
            print(">> Al menos una prueba falló o no se evaluó. Botón 'Exportar Configuración' deshabilitado.")

    def exportar_configuracion(self):
        valores = self.view.obtener_valores_entradas()
        ruta = valores["export_path"]
        
        if not self.params_guardados:
            self.view.mostrar_mensaje_error(
                "Error al Exportar",
                "No hay una configuración ganadora válida guardada para exportar (todas las pruebas deben pasar)."
            )
            return

        if not ruta:
            self.view.mostrar_mensaje_error(
                "Error al Exportar",
                "Debe especificar una ruta de archivo válida para exportar."
            )
            return

        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("=== COMBINACIÓN GANADORA DE GENERADOR ===\n")
                f.write(f"Semilla (X0): {self.params_guardados['x0']}\n")
                f.write(f"Constante Multiplicativa (a): {self.params_guardados['a']}\n")
                f.write(f"Incremento (c): {self.params_guardados['c']}\n")
                f.write(f"Módulo (m): {self.params_guardados['m']}\n")
                f.write(f"Cantidad de Números Evaluados (N): {len(self.numeros_generados)}\n")
                f.write("Resultado: Aprobado por todas las pruebas de independencia (Promedios, Frecuencias, Póquer, Corridas).\n")
            
            abs_path = os.path.abspath(ruta)
            self.view.mostrar_mensaje_exito(
                "Exportación Exitosa",
                f"Configuración guardada correctamente en:\n{abs_path}"
            )
            print(f">> Archivo guardado correctamente en: {abs_path}")
        except Exception as e:
            self.view.mostrar_mensaje_error(
                "Error al Guardar",
                f"No se pudo escribir en el archivo:\n{e}"
            )

if __name__ == "__main__":
    import customtkinter as ctk
    # Configuración global de CustomTkinter
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    app = AppGenerador()
    controlador = Controlador(app)
    app.mainloop()