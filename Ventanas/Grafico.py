import customtkinter as ctk
from Ventanas.Ventana_interfaz import New_ventana
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3
from util.colores import *
from CTkMessagebox import CTkMessagebox

class Grafico(New_ventana):
    def __init__(self, panel_principal, color):
        super().__init__(panel_principal, color, 'graficos')
        self.panel_principal = panel_principal
        self.add_widget_graficos()
        self.mensage("Esta es la pestaña de Graficos, aqui podras ver graficamente el progreso que has tenido en los dias, podras ver graficos como Calorias vs Tiempo, Peso vs Tiempo, Aguas vs Tiempo", "Grafico")

        # Botón de ayuda
        self.boton_ayuda = ctk.CTkButton(self.panel_principal, text="i",
                                         command=self.mostrar_advertencia,
                                         corner_radius=15,
                                         width=30, height=30,
                                         font=("Times New Roman", 25, "italic"),
                                         text_color="white")
        self.boton_ayuda.place(relx=0.97, rely=0.04, anchor="ne")

    def mostrar_advertencia(self):
        CTkMessagebox(title="Grafico", message="Esta es la pestaña de Graficos, aqui podras ver graficamente el progreso que has tenido en los dias, podras ver graficos como Calorias vs Tiempo, Peso vs Tiempo, Aguas vs Tiempo.", icon='info', option_1="Ok")

    def add_widget_graficos(self):
        tabview = ctk.CTkTabview(self.panel_principal, width=800, height=550,
                                 fg_color=gris,
                                 bg_color=gris,
                                 segmented_button_fg_color=azul_medio_oscuro,
                                 segmented_button_selected_color=verde_claro,
                                 segmented_button_selected_hover_color=gris,
                                 segmented_button_unselected_color=azul_medio_oscuro,
                                 segmented_button_unselected_hover_color=verde_claro)
        tabview.place(relx=0.01, rely=0.005, relwidth=1, relheight=1)
        tab1 = tabview.add("Calorías vs Tiempo")
        tab2 = tabview.add("Peso vs Tiempo")
        tab3 = tabview.add("Agua vs Tiempo")
        self.crear_grafico_calorias(tab1)
        self.crear_grafico_peso(tab2)
        self.crear_grafico_agua(tab3)

    def crear_grafico_calorias(self, frame):
        fig = Figure(figsize=(8, 5), dpi=100, facecolor=gris)
        ax1 = fig.add_subplot(111)
        fecha, cantidad = self.datos_calorias()
        ax1.set_facecolor("gray")
        ax1.grid(True, which='both', axis='y', linestyle='--', linewidth=0.6, color='gray')
        ax1.set_title('Calorías vs Tiempo', color='white', fontsize=12)
        ax1.set_ylabel('Calorías', color='white', fontsize=10)
        ax1.set_xlabel('Fecha', color='white', fontsize=10)

        if len(cantidad) > 0:
            bars = ax1.bar(fecha, cantidad, color=verde_alegre, edgecolor='black', linewidth=1.5)
            for bar in bars:
                bar.set_linewidth(1.5)
                bar.set_edgecolor('white')
                bar.set_linestyle((0, (5, 1)))
            ax1.set_yticks(ax1.get_yticks())
        else:

            ax1.text(0.5, 0.5, 'No hay datos disponibles', horizontalalignment='center',
                     verticalalignment='center', transform=ax1.transAxes, color='white', fontsize=12)
            ax1.set_yticks([])

        # Ajuste de ticks y etiquetas
        ax1.set_xticks(range(len(fecha)))
        ax1.set_xticklabels(fecha, rotation=45, ha='right', fontsize=8, color='white')

        # Canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        widget_canvas = canvas.get_tk_widget()
        widget_canvas.pack(fill='both', expand=True)

    def crear_grafico_peso(self, frame):
        fig = Figure(figsize=(8, 5), dpi=100, facecolor=gris)
        ax2 = fig.add_subplot(111)
        fecha2, peso = self.datos_peso()
        ax2.set_facecolor("gray")
        ax2.grid(True, which='both', axis='y', linestyle='--', linewidth=0.6, color='gray')
        ax2.set_title('Peso vs Tiempo', color='white', fontsize=12)
        ax2.set_ylabel('Peso', color='white', fontsize=10)
        ax2.set_xlabel('Fecha', color='white', fontsize=10)

        if len(peso) > 0:
            bars = ax2.bar(fecha2, peso, color=verde_alegre, edgecolor='black', linewidth=1.5)
            for bar in bars:
                bar.set_linewidth(1.5)
                bar.set_edgecolor('white')
                bar.set_linestyle((0, (5, 1)))
            ax2.set_yticks(ax2.get_yticks())
        else:

            ax2.text(0.5, 0.5, 'No hay datos disponibles', horizontalalignment='center',
                     verticalalignment='center', transform=ax2.transAxes, color='white', fontsize=12)
            ax2.set_yticks([])

        # Ajuste de ticks y etiquetas
        ax2.set_xticks(range(len(fecha2)))
        ax2.set_xticklabels(fecha2, rotation=45, ha='right', fontsize=8, color='white')

        # Canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        widget_canvas = canvas.get_tk_widget()
        widget_canvas.pack(fill='both', expand=True)

    def crear_grafico_agua(self, frame):
        fig = Figure(figsize=(8, 5), dpi=100, facecolor=gris)
        ax3 = fig.add_subplot(111)
        fecha3, agua = self.datos_agua()
        ax3.set_facecolor("gray")
        ax3.grid(True, which='both', axis='y', linestyle='--', linewidth=0.6, color='gray')
        ax3.set_title('Agua vs Tiempo', color='white', fontsize=12)
        ax3.set_ylabel('Agua', color='white', fontsize=10)
        ax3.set_xlabel('Fecha', color='white', fontsize=10)

        if len(agua) > 0:
            bars = ax3.bar(fecha3, agua, color=verde_alegre, edgecolor='black', linewidth=1.5)
            for bar in bars:
                bar.set_linewidth(1.5)
                bar.set_edgecolor('white')
                bar.set_linestyle((0, (5, 1)))
            ax3.set_yticks(ax3.get_yticks())
        else:

            ax3.text(0.5, 0.5, 'No hay datos disponibles', horizontalalignment='center',
                     verticalalignment='center', transform=ax3.transAxes, color='white', fontsize=12)
            ax3.set_yticks([])

        # Ajuste de ticks y etiquetas
        ax3.set_xticks(range(len(fecha3)))
        ax3.set_xticklabels(fecha3, rotation=45, ha='right', fontsize=8, color='white')

        # Canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        widget_canvas = canvas.get_tk_widget()
        widget_canvas.pack(fill='both', expand=True)

    def datos_calorias(self):
        conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(total_cal), fecha FROM consumo_diario GROUP BY fecha ORDER BY strftime('%Y-%m-%d', substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2))")
        resultados = cursor.fetchall()
        conn.close()
        cantidad = [fila[0] for fila in resultados]
        fecha = [fila[1] for fila in resultados]
        return fecha, cantidad

    def datos_peso(self):
        conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fecha, peso FROM peso GROUP BY fecha ORDER BY strftime('%Y-%m-%d', substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2))")
        resultados = cursor.fetchall()
        conn.close()
        fecha2 = [fila[0] for fila in resultados]
        peso = [fila[1] for fila in resultados]
        return fecha2, peso

    def datos_agua(self):
        conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fecha, cant FROM agua GROUP BY fecha ORDER BY strftime('%Y-%m-%d', substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2))")
        resultados = cursor.fetchall()
        conn.close()
        fecha3 = [fila[0] for fila in resultados]
        agua = [fila[1] for fila in resultados]
        return fecha3, agua
