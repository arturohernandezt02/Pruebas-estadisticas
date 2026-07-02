import customtkinter as ctk
from tkinter import messagebox

class AppGenerador(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración básica de la ventana principal
        self.title("Calculadora de Pruebas Estadísticas de Independencia")
        self.geometry("1024x660")
        self.minsize(960, 600)
        
        # ----------------------------------------------------
        # PALETA DE COLORES RETRO (Claros y Tenues)
        # ----------------------------------------------------
        self.COLOR_BG = "#F4EFE6"           # Fondo principal (crema/beige vintage)
        self.COLOR_CONTAINER = "#E9DFD0"    # Contenedores/tarjetas
        self.COLOR_FG = "#2E3532"           # Texto principal (antracita verdoso)
        self.COLOR_PRIMARY = "#9CAEA9"      # Botones secundarios (gris salvia)
        self.COLOR_SECONDARY = "#788585"    # Bordes/elementos de control
        self.COLOR_ACCENT = "#D4A373"       # Acción principal (ocre/arena tostado)
        
        # Estados para los Badges
        self.COLOR_SUCCESS = "#8A9A86"      # Aceptado/Pasó (verde salvia tenue)
        self.COLOR_ERROR = "#C98D83"        # Rechazado/Falló (terracota suave)
        self.COLOR_NEUTRAL = "#D8CFBD"      # Sin evaluar (gris cálido)
        
        # Colores de Hover
        self.COLOR_PRIMARY_HOVER = "#8B9D98"
        self.COLOR_SECONDARY_HOVER = "#677373"
        self.COLOR_ACCENT_HOVER = "#C39262"
        
        # Aplicar fondo principal
        self.configure(fg_color=self.COLOR_BG)
        
        # ----------------------------------------------------
        # FUENTES
        # ----------------------------------------------------
        self.FONT_TITLE = ("Segoe UI", 16, "bold")
        self.FONT_LABEL = ("Segoe UI", 12)
        self.FONT_LABEL_BOLD = ("Segoe UI", 12, "bold")
        self.FONT_MONO = ("Consolas", 11)
        self.FONT_MONO_BOLD = ("Consolas", 11, "bold")
        
        # ----------------------------------------------------
        # GRID LAYOUT PRINCIPAL (Responsivo)
        # ----------------------------------------------------
        self.grid_columnconfigure(0, weight=0, minsize=320) # Panel Izquierdo fijo
        self.grid_columnconfigure(1, weight=1)              # Panel Derecho expansible
        self.grid_rowconfigure(0, weight=1)
        
        self.create_widgets()

    def create_widgets(self):
        # ----------------------------------------------------
        # PANEL IZQUIERDO (Control de Parámetros)
        # ----------------------------------------------------
        self.left_panel = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_CONTAINER,
            corner_radius=10,
            border_width=1,
            border_color=self.COLOR_SECONDARY
        )
        self.left_panel.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="nsew")
        self.left_panel.grid_columnconfigure(0, weight=1)
        
        # Título del Panel
        lbl_title = ctk.CTkLabel(
            self.left_panel,
            text="Parámetros del Generador",
            font=self.FONT_TITLE,
            text_color=self.COLOR_FG
        )
        lbl_title.grid(row=0, column=0, padx=15, pady=(20, 15), sticky="w")
        
        # Contenedor interno de inputs
        params_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        params_frame.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
        params_frame.grid_columnconfigure(0, weight=0, minsize=110)
        params_frame.grid_columnconfigure(1, weight=1)
        
        # Campos de entrada individuales
        inputs = [
            ("Semilla (X0):", "entry_x0", "17"),
            ("Constante (a):", "entry_a", "121"),
            ("Incremento (c):", "entry_c", "0"),
            ("Módulo (m):", "entry_m", "1000")
        ]
        
        for i, (label_text, var_name, default_val) in enumerate(inputs):
            lbl = ctk.CTkLabel(params_frame, text=label_text, font=self.FONT_LABEL, text_color=self.COLOR_FG)
            lbl.grid(row=i, column=0, padx=(0, 5), pady=8, sticky="e")
            
            entry = ctk.CTkEntry(
                params_frame,
                font=self.FONT_MONO,
                text_color=self.COLOR_FG,
                fg_color=self.COLOR_BG,
                border_color=self.COLOR_SECONDARY,
                placeholder_text=default_val
            )
            entry.grid(row=i, column=1, padx=0, pady=8, sticky="ew")
            entry.insert(0, default_val)
            setattr(self, var_name, entry)
            
        # Botón principal: Generar y Evaluar
        self.btn_evaluar = ctk.CTkButton(
            self.left_panel,
            text="Generar y Evaluar",
            font=self.FONT_LABEL_BOLD,
            fg_color=self.COLOR_ACCENT,
            hover_color=self.COLOR_ACCENT_HOVER,
            text_color=self.COLOR_FG,
            height=36
        )
        self.btn_evaluar.grid(row=2, column=0, padx=15, pady=25, sticky="ew")
        
        # Espacio flexible vertical para empujar exportación hacia abajo
        self.left_panel.grid_rowconfigure(3, weight=1)
        
        # Apartado inferior de Exportación
        export_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        export_frame.grid(row=4, column=0, padx=15, pady=(15, 20), sticky="ew")
        export_frame.grid_columnconfigure(0, weight=1)
        
        lbl_export_path = ctk.CTkLabel(export_frame, text="Ruta de Exportación:", font=self.FONT_LABEL, text_color=self.COLOR_FG)
        lbl_export_path.grid(row=0, column=0, padx=0, pady=(0, 4), sticky="w")
        
        self.entry_export = ctk.CTkEntry(
            export_frame,
            font=self.FONT_MONO,
            text_color=self.COLOR_FG,
            fg_color=self.COLOR_BG,
            border_color=self.COLOR_SECONDARY
        )
        self.entry_export.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="ew")
        self.entry_export.insert(0, "config_ganadora.txt")
        
        self.btn_exportar = ctk.CTkButton(
            export_frame,
            text="Exportar Configuración",
            font=self.FONT_LABEL_BOLD,
            fg_color=self.COLOR_PRIMARY,
            hover_color=self.COLOR_PRIMARY_HOVER,
            text_color=self.COLOR_FG,
            state="disabled",
            height=30
        )
        self.btn_exportar.grid(row=2, column=0, padx=0, pady=0, sticky="ew")

        # ----------------------------------------------------
        # PANEL DERECHO (Resultados y Status Checklist)
        # ----------------------------------------------------
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, padx=(10, 15), pady=15, sticky="nsew")
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1) # Tabview ocupa la mayor parte
        self.right_panel.grid_rowconfigure(1, weight=0) # Panel inferior de estatus
        
        # Pestañas CTkTabview
        self.tabview = ctk.CTkTabview(
            self.right_panel,
            fg_color=self.COLOR_CONTAINER,
            segmented_button_fg_color=self.COLOR_CONTAINER,
            segmented_button_selected_color=self.COLOR_ACCENT,
            segmented_button_selected_hover_color=self.COLOR_ACCENT_HOVER,
            segmented_button_unselected_color=self.COLOR_CONTAINER,
            segmented_button_unselected_hover_color=self.COLOR_PRIMARY_HOVER,
            text_color=self.COLOR_FG
        )
        self.tabview.grid(row=0, column=0, padx=0, pady=(0, 15), sticky="nsew")
        
        # Creación de pestañas
        self.tab_numeros = self.tabview.add("Números (Ri)")
        self.tab_promedios = self.tabview.add("Promedios")
        self.tab_frecuencias = self.tabview.add("Frecuencias")
        self.tab_poker = self.tabview.add("Póquer")
        self.tab_corridas = self.tabview.add("Corridas")
        
        # Diccionario para asociar cada pestaña con su cuadro de texto scrollable
        self.textboxes = {}
        
        tabs_config = [
            (self.tab_numeros, "numeros", "Aquí se desplegará el conjunto de números pseudoaleatorios generados (Ri) en formato de tabla monospace.\n\nPresiona 'Generar y Evaluar' para comenzar."),
            (self.tab_promedios, "promedios", "Cálculo detallado de la prueba de Promedios:\n- Media aritmética (r-barra)\n- Estadístico Z0 calculado\n- Valor crítico Z_alpha/2 de la distribución normal."),
            (self.tab_frecuencias, "frecuencias", "Cálculo detallado de la prueba de Frecuencias:\n- Clases e intervalos\n- Frecuencias observadas vs esperadas\n- Estadístico Chi-cuadrada (Chi^2)."),
            (self.tab_poker, "poker", "Cálculo detallado de la prueba de Póquer (Clasificación de decimales):\n- Manos (todos diferentes, un par, dos pares, tercia, full, póquer, quintilla)\n- Frecuencias observadas vs esperadas\n- Estadístico Chi-cuadrada."),
            (self.tab_corridas, "corridas", "Cálculo detallado de la prueba de Corridas (Arriba y Abajo de la media):\n- Secuencia de signos (+ / -)\n- Cantidad de corridas observadas\n- Valor de Z calculado.")
        ]
        
        for tab_obj, key, placeholder in tabs_config:
            tab_obj.grid_columnconfigure(0, weight=1)
            tab_obj.grid_rowconfigure(0, weight=1)
            
            # Usamos CTkTextbox para permitir scroll y copia de texto estructurado de forma elegante
            tb = ctk.CTkTextbox(
                tab_obj,
                font=self.FONT_MONO,
                text_color=self.COLOR_FG,
                fg_color=self.COLOR_BG,
                border_color=self.COLOR_SECONDARY,
                border_width=1,
                corner_radius=6
            )
            tb.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
            tb.insert("1.0", placeholder)
            tb.configure(state="disabled")
            self.textboxes[key] = tb
            
        # Panel inferior "Status Checklist"
        self.status_panel = ctk.CTkFrame(
            self.right_panel,
            fg_color=self.COLOR_CONTAINER,
            corner_radius=10,
            border_width=1,
            border_color=self.COLOR_SECONDARY
        )
        self.status_panel.grid(row=1, column=0, padx=0, pady=0, sticky="ew")
        
        self.status_panel.grid_columnconfigure(0, weight=2)
        self.status_panel.grid_columnconfigure(1, weight=3)
        self.status_panel.grid_columnconfigure(2, weight=3)
        self.status_panel.grid_columnconfigure(3, weight=3)
        self.status_panel.grid_columnconfigure(4, weight=3)
        
        lbl_status_title = ctk.CTkLabel(
            self.status_panel,
            text="Estado de Pruebas:",
            font=self.FONT_LABEL_BOLD,
            text_color=self.COLOR_FG
        )
        lbl_status_title.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        # Inicialización de las 4 etiquetas/badges de pruebas
        self.badge_promedios = ctk.CTkLabel(
            self.status_panel,
            text="PROMEDIOS: ND",
            font=self.FONT_MONO_BOLD,
            text_color=self.COLOR_FG,
            fg_color=self.COLOR_NEUTRAL,
            corner_radius=6,
            height=28
        )
        self.badge_promedios.grid(row=0, column=1, padx=5, pady=15, sticky="ew")
        
        self.badge_frecuencias = ctk.CTkLabel(
            self.status_panel,
            text="FRECUENCIAS: ND",
            font=self.FONT_MONO_BOLD,
            text_color=self.COLOR_FG,
            fg_color=self.COLOR_NEUTRAL,
            corner_radius=6,
            height=28
        )
        self.badge_frecuencias.grid(row=0, column=2, padx=5, pady=15, sticky="ew")
        
        self.badge_poker = ctk.CTkLabel(
            self.status_panel,
            text="PÓQUER: ND",
            font=self.FONT_MONO_BOLD,
            text_color=self.COLOR_FG,
            fg_color=self.COLOR_NEUTRAL,
            corner_radius=6,
            height=28
        )
        self.badge_poker.grid(row=0, column=3, padx=5, pady=15, sticky="ew")
        
        self.badge_corridas = ctk.CTkLabel(
            self.status_panel,
            text="CORRIDAS: ND",
            font=self.FONT_MONO_BOLD,
            text_color=self.COLOR_FG,
            fg_color=self.COLOR_NEUTRAL,
            corner_radius=6,
            height=28
        )
        self.badge_corridas.grid(row=0, column=4, padx=(5, 15), pady=15, sticky="ew")

    # ----------------------------------------------------
    # MÉTODOS PÚBLICOS DE INTERFAZ (Para el Controlador)
    # ----------------------------------------------------
    
    def set_callbacks(self, on_evaluar, on_exportar):
        """Asigna los manejadores de eventos desde el controlador."""
        self.btn_evaluar.configure(command=on_evaluar)
        self.btn_exportar.configure(command=on_exportar)

    def obtener_valores_entradas(self):
        """Retorna un diccionario con los valores de los campos de texto."""
        return {
            "x0": self.entry_x0.get().strip(),
            "a": self.entry_a.get().strip(),
            "c": self.entry_c.get().strip(),
            "m": self.entry_m.get().strip(),
            "export_path": self.entry_export.get().strip()
        }

    def actualizar_resultados_tab(self, key, texto):
        """Actualiza el texto en una pestaña específica."""
        if key in self.textboxes:
            tb = self.textboxes[key]
            tb.configure(state="normal")
            tb.delete("1.0", "end")
            tb.insert("1.0", texto)
            tb.configure(state="disabled")

    def actualizar_badge(self, test_name, paso):
        """
        Actualiza el color y texto de un badge de estado.
        test_name: 'promedios', 'frecuencias', 'poker', 'corridas'
        paso: True (Pasó, verde), False (Falló, terracota), None (ND, neutro)
        """
        badge_map = {
            "promedios": (self.badge_promedios, "PROMEDIOS"),
            "frecuencias": (self.badge_frecuencias, "FRECUENCIAS"),
            "poker": (self.badge_poker, "PÓQUER"),
            "corridas": (self.badge_corridas, "CORRIDAS")
        }
        
        if test_name not in badge_map:
            return
            
        badge_widget, base_text = badge_map[test_name]
        
        if paso is True:
            badge_widget.configure(
                text=f"{base_text}: PASÓ",
                fg_color=self.COLOR_SUCCESS,
                text_color="#FFFFFF"
            )
        elif paso is False:
            badge_widget.configure(
                text=f"{base_text}: FALLÓ",
                fg_color=self.COLOR_ERROR,
                text_color="#FFFFFF"
            )
        else:
            badge_widget.configure(
                text=f"{base_text}: ND",
                fg_color=self.COLOR_NEUTRAL,
                text_color=self.COLOR_FG
            )

    def habilitar_exportacion(self, habilitar):
        """Habilita o deshabilita el botón de exportación."""
        state = "normal" if habilitar else "disabled"
        self.btn_exportar.configure(state=state)

    def mostrar_mensaje_error(self, titulo, mensaje):
        """Muestra un diálogo de error al usuario."""
        messagebox.showerror(titulo, mensaje)

    def mostrar_mensaje_exito(self, titulo, mensaje):
        """Muestra un diálogo de éxito al usuario."""
        messagebox.showinfo(titulo, mensaje)
