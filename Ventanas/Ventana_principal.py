import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from datetime import datetime
from util.colores import *
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from PIL import Image, ImageDraw
import json
import os
import shutil

from Ventanas.Alimentos import Alimentos
from Ventanas.Registro_Alimento import Registro_Alimento
from Ventanas.Agregar_Alimento import Agregar_Alimento
from Ventanas.Grafico import Grafico
from Ventanas.Historial import Historial
from Ventanas.Configuracion import Configuracion
from Ventanas.Log_In import Log_in
from Ventanas.Salud import Salud
from Ventanas.Recordatorio import Recordatorio
from Ventanas.Calendario import Calendario

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Contador de Calorias Pro 60Hz')
        self.geometry('1024x600')
        self.logo = self.load_image("./img/banner.png", (700, 500))
        self.config_window()
        self.esperando_login()
        self.log_in()
        
        self.botones_menu = []
    
    def load_image(self, path, size):
        return ctk.CTkImage(Image.open(path), size=size)
    
    def obtener_usuario(self):
        with open('usuario_actual.txt', 'r') as users:
                return users.readline()
        
    def config_window(self):
        self.iconbitmap("./img/logo.ico")
        w, h = 1024, 600
        util_ventana.centrar_ventana(self, w, h)

    def cargar_main(self):
        self.usuario = self.obtener_usuario()
        self.paneles()
        self.perfil = self.cargar_imagen_guardada()
        self.controles_barra_superior()
        self.controles_barra_lateral()
        self.controles_cuerpo()
        
        recordatorio = Recordatorio(self.usuario)
        recordatorio.recordatorio_por_defecto()
        recordatorio.recordar_actualizar_peso()

    def paneles(self):
        self.frame_tapar.destroy()
        # Crear paneles: Barra superior, Menu lateral y cuerpo principal
        self.barra_superior = tk.Frame(self, bg=azul_medio_oscuro, height=200)
        self.barra_superior.pack(side=tk.TOP, fill='both')
        
        self.menu_lateral = tk.Frame(self, bg=azul_medio_oscuro, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)
        
        self.cuerpo_principal = tk.Frame(self, bg=gris)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
        
    def controles_barra_superior(self):        
        #etiqueta de titulo
        self.labelTitutlo = tk.Label(self.barra_superior, text= "Contador de Calorías")
        self.labelTitutlo.config(fg="#fff",font=("Arial", 25), bg=azul_medio_oscuro, pady=20, padx=20, width=16)
        self.labelTitutlo.pack(side=tk.LEFT)
        
        #Etiqueta de información
        self.labelTitutlo = tk.Label(
            self.barra_superior, text='Hoy es: ' + datetime.now().strftime('%d-%m-%Y'))
        self.labelTitutlo.config(fg="#fff", font=("Arial", 25), bg=azul_medio_oscuro, padx=10, width=20)
        self.labelTitutlo.pack(side=tk.RIGHT)

    def existe_archivo(self, ruta_archivo, valor_predeterminado=None):
        if os.path.exists(ruta_archivo):
            return ruta_archivo
        else:
            return valor_predeterminado

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Imagen", "*.png .jpg .jpeg")])
        if archivo:
            print(f"Archivo seleccionado: {archivo}")
            nuevo_archivo = self.copiar_imagen_a_carpeta_usuario(archivo)
            imagen_perfil = Image.open(nuevo_archivo).resize((80, 80))
            imagen_perfil_circular = self.hacer_imagen_circular(imagen_perfil)
            self.perfil = ctk.CTkImage(imagen_perfil_circular, size=(80, 80))
            self.labelPerfil.configure(image=self.perfil)
            self.guardar_ruta_imagen(nuevo_archivo)

    def copiar_imagen_a_carpeta_usuario(self, ruta_origen):
        if not self.usuario:
            raise ValueError("El nombre del usuario no es válido.")
        carpeta_usuario = os.path.join('./users', self.usuario)
        os.makedirs(carpeta_usuario, exist_ok=True)
        _, extension = os.path.splitext(ruta_origen)
        ruta_destino = os.path.join(carpeta_usuario, f'perfil{extension}')
        shutil.copy2(ruta_origen, ruta_destino)
        return ruta_destino

    def toggle_submenu_alimentos(self):
        if self.alimentos_visible:
            self.submenu_alimentos.pack_forget()
            self.alimentos_visible = False
        else:
            self.submenu_alimentos.pack(side=ctk.TOP)
            self.alimentos_visible = True

    def toggle_submenu_salud_principal(self):
        if self.salud_principal_visible:
            self.submenu_salud_principal.pack_forget()
            self.salud_principal_visible = False
        else:
            self.submenu_salud_principal.pack(side=ctk.TOP)
            self.salud_principal_visible = True
    
    def guardar_ruta_imagen(self, ruta):
        ruta_json = os.path.join('./users', self.usuario, 'imagen_perfil.json')
        with open(ruta_json, "w") as f:
            json.dump({"ruta_imagen": ruta}, f)
    
    def cargar_imagen_guardada(self):
        try:
            ruta_json = os.path.join('./users', self.usuario, 'imagen_perfil.json')
            with open(ruta_json, 'r') as f:
                data = json.load(f)
                ruta_imagen = data.get("ruta_imagen")
        except (FileNotFoundError, json.JSONDecodeError):
            ruta_imagen = None

        if ruta_imagen and os.path.exists(ruta_imagen):
            img = Image.open(ruta_imagen).resize((80, 80))
        else:
            img = Image.open("./img/sin_imagen.png").resize((80, 80))
        
        img_circular = self.hacer_imagen_circular(img)
        return ctk.CTkImage(img_circular, size=(80, 80))

    def abrir_archivo_json(self):
        ruta_json = os.path.join('./users', self.usuario, 'imagen_perfil.json')
        try:
            with open(ruta_json, 'r') as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return None  
     
    def hacer_imagen_circular(self, imagen):
        mascarilla = Image.new("L", (80, 80), 0)
        dibujar = ImageDraw.Draw(mascarilla)
        dibujar.ellipse((0, 0, 80, 80), fill=255)

        imagen_circular = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
        imagen_circular.paste(imagen, (0, 0), mascarilla)

        return imagen_circular

    def controles_barra_lateral(self):
        self.labelPerfil = ctk.CTkLabel(self.menu_lateral, image=self.perfil, text='')
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        with open('usuario_actual.txt', 'r') as users:
            nombre_usuario = users.readline().strip()  # Leer y eliminar posibles saltos de línea
        
        self.labelNombre = tk.Label(self.menu_lateral, text=nombre_usuario, font=("Arial", 12, "bold"), bg=azul_medio_oscuro, fg="white")
        self.labelNombre.pack(side=tk.TOP, pady=5)

        self.btn_mas = tk.Button(self.menu_lateral, 
                        text="+", 
                        font=("Arial", 15), 
                        bg="#34A85A", 
                        fg="white", 
                        relief="flat", 
                        borderwidth=0,
                        command=self.seleccionar_archivo)
        self.btn_mas.place(x=175, y=100, width=25, height=25)

        self.iconos = util_img.cargar_imagenes(carpeta='./img/icon_img')

        # Contenedor para "Alimentos" y sus botones desplegables
        self.seccion_alimentos = ctk.CTkFrame(self.menu_lateral, fg_color="transparent")
        self.seccion_alimentos.pack(side=ctk.TOP, fill='x')

        # Botón principal "Alimentos" que despliega/oculta el submenú
        self.btn_alimentos = ctk.CTkButton(self.seccion_alimentos, text="Alimentos", image=self.iconos[7], compound='left',
                                        width=200, height=50, corner_radius=0, fg_color=azul_medio_oscuro,
                                        hover_color=verde_claro, command=self.toggle_submenu_alimentos)
        self.btn_alimentos.pack(side=ctk.TOP)

        # Crear el frame del submenú de Alimentos (inicialmente oculto)
        self.submenu_alimentos = ctk.CTkFrame(self.seccion_alimentos, fg_color="transparent")
        self.submenu_alimentos.pack_forget()  # Oculto al inicio

        # Bandera para saber si está visible o no
        self.alimentos_visible = False

        # Botones del submenú (dentro del frame)
        self.btn_registro = ctk.CTkButton(self.submenu_alimentos, text='Registrar Alimento', image=self.iconos[4], compound='left',
                                        width=200, height=40, corner_radius=0, fg_color=azul_medio_oscuro,
                                        hover_color=verde_claro, command=self.abrir_registro_alimento)
        self.btn_registro.pack(side=ctk.TOP)

        self.btn_agregar = ctk.CTkButton(self.submenu_alimentos, text="Agregar Alimento", image=self.iconos[0], compound='left',
                                        width=200, height=40, corner_radius=0, fg_color=azul_medio_oscuro,
                                        hover_color=verde_claro, command=self.abrir_agregar_alimento)
        self.btn_agregar.pack(side=ctk.TOP)

        self.btn_alimentos = ctk.CTkButton(self.submenu_alimentos, text="Admin-Alimentos", image=self.iconos[7], compound='left',
                                        width=200, height=40, corner_radius=0, fg_color=azul_medio_oscuro,
                                        hover_color=verde_claro, command=self.abrir_alimentos)
        self.btn_alimentos.pack(side=ctk.TOP)

        # === Submenú SALUD ===

        self.seccion_salud_principal = ctk.CTkFrame(self.menu_lateral, fg_color="transparent")
        self.seccion_salud_principal.pack(side=ctk.TOP, fill='x')

        self.btn_salud_principal = ctk.CTkButton(self.seccion_salud_principal, text="Salud", image=self.iconos[7], compound='left',
                                        width=200, height=50, corner_radius=0, fg_color=azul_medio_oscuro,
                                        hover_color=verde_claro, command=self.toggle_submenu_salud_principal)
        self.btn_salud_principal.pack(side=ctk.TOP)

        # Crear el frame del submenú de Alimentos (inicialmente oculto)
        self.submenu_salud_principal = ctk.CTkFrame(self.seccion_salud_principal, fg_color="transparent")
        self.submenu_salud_principal.pack_forget()  # Oculto al inicio

        # Bandera para saber si está visible o no
        self.salud_principal_visible = False


        # Botones del submenú (dentro del frame)
        self.btn_grafico = ctk.CTkButton(self.submenu_salud_principal, text="Gráfico", image=self.iconos[2], compound='left',
                                        width=200, height=40, corner_radius=0, fg_color=azul_medio_oscuro,
                                        hover_color=verde_claro, command=self.abrir_grafico)
        self.btn_grafico.pack(side=ctk.TOP)

        self.btn_salud = ctk.CTkButton(self.submenu_salud_principal, text="Salud", image=self.iconos[5], compound='left',
                                        width=200, height=40, corner_radius=0, fg_color=azul_medio_oscuro,
                                        hover_color=verde_claro, command=self.abrir_salud)
        self.btn_salud.pack(side=ctk.TOP)

        self.btn_calendario = ctk.CTkButton(self.submenu_salud_principal, text="Calendario", image=self.iconos[1], compound='left',
                                        width=200, height=40, corner_radius=0, fg_color=azul_medio_oscuro,
                                        hover_color=verde_claro, command=self.abrir_calendario)
        self.btn_calendario.pack(side=ctk.TOP)

        self.btn_historial = ctk.CTkButton(self.submenu_salud_principal, text="Historial", image=self.iconos[3], compound='left',
                                        width=200, height=40, corner_radius=0, fg_color=azul_medio_oscuro,
                                        hover_color=verde_claro, command=self.abrir_historial)
        self.btn_historial.pack(side=ctk.TOP)
        
        
    def controles_cuerpo(self):
        label = ctk.CTkLabel(self.cuerpo_principal, image=self.logo, text='')
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def bind_hover_events(self, button):
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))
        
    def on_enter(self, event, button):
        # Cambiar estilo al pasar el raton por encima
        button.config(bg= azul_mas_clarito, fg='white')
        
    def on_leave(self, event, button):
        # Restaurar el estilo al salir el raton
        button.config(bg=azul_medio_oscuro, fg='white')

        self.botones_menu = [self.btn_registro, self.btn_agregar, self.btn_grafico, self.btn_historial,
                             self.btn_en_contruccion, self.btn_salud, self.btn_alimentos]

    
    def resetear_colores_botones(self):
        for boton in self.botones_menu:
            boton.configure(fg_color=azul_medio_oscuro)
            boton.configure(hover_color=verde_claro)

    def abrir_registro_alimento(self):
        self.resetear_colores_botones()  
        self.btn_registro.configure(fg_color=negro_texto)  
        self.btn_registro.configure(hover_color=negro_texto)  
        self.limpiar_panel(self.cuerpo_principal)
        Registro_Alimento(self.cuerpo_principal, gris)

    def abrir_agregar_alimento(self):
        self.resetear_colores_botones()  
        self.btn_agregar.configure(fg_color=negro_texto)
        self.btn_agregar.configure(hover_color=negro_texto)
        self.limpiar_panel(self.cuerpo_principal)
        Agregar_Alimento(self.cuerpo_principal, gris)

    def abrir_grafico(self):
        self.resetear_colores_botones()  
        self.btn_grafico.configure(fg_color=negro_texto)
        self.btn_grafico.configure(hover_color=negro_texto)
        self.limpiar_panel(self.cuerpo_principal)
        Grafico(self.cuerpo_principal, gris)

    def abrir_historial(self):
        self.resetear_colores_botones()  
        self.btn_historial.configure(fg_color=negro_texto)
        self.btn_historial.configure(hover_color=negro_texto)
        self.limpiar_panel(self.cuerpo_principal)
        Historial(self.cuerpo_principal, gris)

    def abrir_configuracion(self):
        self.resetear_colores_botones()  
        self.btn_en_contruccion.configure(fg_color=negro_texto)
        self.btn_en_contruccion.configure(hover_color=negro_texto)        
        self.limpiar_panel(self.cuerpo_principal)
        Configuracion(self.cuerpo_principal, gris)

    def abrir_salud(self):
        self.resetear_colores_botones()  
        self.btn_salud.configure(fg_color=negro_texto)
        self.btn_salud.configure(hover_color=negro_texto)
        self.limpiar_panel(self.cuerpo_principal)
        Salud(self.cuerpo_principal, gris)   

    def abrir_calendario(self):
        self.resetear_colores_botones()  
        self.btn_calendario.configure(fg_color=negro_texto)
        self.btn_calendario.configure(hover_color=negro_texto)
        self.limpiar_panel(self.cuerpo_principal)
        Calendario(self.cuerpo_principal, gris)

    def abrir_alimentos(self):
        self.resetear_colores_botones()  
        self.btn_alimentos.configure(fg_color=negro_texto)
        self.btn_alimentos.configure(hover_color=negro_texto)
        self.limpiar_panel(self.cuerpo_principal)
        Alimentos(self.cuerpo_principal, gris)

        
    def log_in(self):
        Log_in(self)

    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def esperando_login(self):
        self.frame_tapar = ctk.CTkFrame(self, fg_color='black', corner_radius=0)
        self.frame_tapar.pack(expand=True, fill='both')
        image_path = "./img/banner_l.png"
        image_tapar = ctk.CTkImage(Image.open(image_path), size=(1024, 600))
        image_label = ctk.CTkLabel(self.frame_tapar, image=image_tapar, text='')
        image_label.place(x=0, y=0, relwidth=1, relheight=1)
        btn_reabrir_login = ctk.CTkButton(self.frame_tapar, text='Iniciar Sesión', command=self.log_in, width=150, height=75, corner_radius=20,
                                          fg_color=verde_boton, text_color=azul_medio_oscuro, hover_color=verde_oscuro)
        btn_reabrir_login.place(x=430, y=450)
