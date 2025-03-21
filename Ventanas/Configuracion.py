import customtkinter as ctk
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
from Ventanas.Ventana_interfaz import New_ventana
import sqlite3
from datetime import datetime
from Ventanas.Recordatorio import Recordatorio
import os
import subprocess
import sys
import shutil
import tempfile
import time
from util.colores import *
import shutil

class Configuracion(New_ventana):
    def __init__(self, panel_principal, color):
        super().__init__(panel_principal, color, 'configuracion')
        self.panel_principal = panel_principal 
        self.recordatorio = Recordatorio(self.usuario) 
        self.ultimo_msj = None
        self.add_widget_config()
        self.mensage("Esta es la pestaña de configuracion, dentro podras configurar todo lo que es tu perfil como el objetivo de calorias y el nivel de actividad", "Configuracion")
        self.temp_dir = tempfile.mkdtemp()

    def mostrar_advertencia(self):
        CTkMessagebox(title="Configuracion", message="Esta es la pestaña de configuracion, dentro podras configurar todo lo que es tu perfil como el objetivo de calorias y el nivel de actividad.", icon='info', option_1="Ok")

    def add_widget_config(self):
        self.boton_ayuda = ctk.CTkButton(self.sub, text="i",
                                         command=self.mostrar_advertencia,
                                         corner_radius=15,
                                         width=30, height=30,
                                         font=("Times New Roman", 25, "italic"),
                                         text_color="white")
        self.boton_ayuda.place(relx=0.97, rely=0.04, anchor="ne")
        
        edad, genero, peso, nivel_actividad,meta_cal, estatura  = self.cargar_datos_usuario()

        # Fondo general de la configuración
        self.bg_fondo_config = ctk.CTkButton(self.sub, text='', bg_color=gris, state='disable', width=750, 
                                             height=500, corner_radius=40, fg_color=gris)
        self.bg_fondo_config.place(x=10, y=10)

        self.bg_fondo_verde= ctk.CTkButton(self.sub, text='', bg_color=gris, state='disable', width=390, 
                                             height=385, corner_radius=35, fg_color=gris)
        self.bg_fondo_verde.place(x=45, y=100)
        
        self.bg_fondo_claro= ctk.CTkButton(self.sub, text='', bg_color=gris, state='disable', width=215, 
                                             height=260, corner_radius=35, fg_color=segundo_label)
        self.bg_fondo_claro.place(x=475, y=100)
        
        self.bg_fondo_oscuro= ctk.CTkButton(self.sub, text='', bg_color=segundo_label, state='disable', width=195, 
                                             height=240, corner_radius=35, fg_color=gris)
        self.bg_fondo_oscuro.place(x=485, y=110)
        
        #self.bg_titulo_verde= ctk.CTkButton(self.sub, text='', bg_color=gris, state='disable', width=680, 
                                             #height=55, corner_radius=35, fg_color=primer_label)
        #self.bg_titulo_verde.place(x=45, y=25)
        
        #self.titulo_label= ctk.CTkLabel(self.sub, text="Configuración", text_color=negro_texto, bg_color= primer_label, font=("Arial", 27, "bold"))
        #self.titulo_label.place(x=295, y=35)
        
        self.nombre_label = ctk.CTkLabel(self.sub, text=f"Nombre: {self.usuario}", text_color="white")
        self.nombre_label.place(x=505, y=125)
        
        self.edad_label = ctk.CTkLabel(self.sub, text=f"Edad: {edad}", text_color="white")
        self.edad_label.place(x=505, y=155)

        self.genero_label = ctk.CTkLabel(self.sub, text=f"Género: {genero}", text_color="white")
        self.genero_label.place(x=505, y=185)
        
        self.peso_label = ctk.CTkLabel(self.sub, text=f"Peso: {peso} kg", text_color="white")
        self.peso_label.place(x=505, y=215)
        
        self.peso_label = ctk.CTkLabel(self.sub, text=f"Estatura: {estatura} cm", text_color="white")
        self.peso_label.place(x=505, y=245)

        self.obj_calorias_label = ctk.CTkLabel(self.sub, text=f"Objetivo de Calorías: {meta_cal}", text_color="white")
        self.obj_calorias_label.place(x=505, y=275)
        
        self.lvl_actividad_label = ctk.CTkLabel(self.sub, text=f"Nivel de Actividad: {nivel_actividad}", text_color="white")
        self.lvl_actividad_label.place(x=505, y=305)
        
        self.guardar_button = ctk.CTkButton(self.sub, text="Actualizar información", command=self.mostrar_interfaz_guardar, text_color=negro_texto, bg_color=gris
                                            , corner_radius=30, fg_color=verde_boton, width=335, height=55, font=("Arial",19, "bold"), hover_color=verde_oscuro)
        self.guardar_button.place(x=75, y=165)

        self.mostrar_contra_button = ctk.CTkButton(self.sub, text="Actualizar Contraseña", command=self.mostrar_formulario_contrasena,text_color=negro_texto, bg_color=gris
                                                   , corner_radius=30, fg_color=verde_boton, width=335, height=55, font=("Arial",19, "bold"), hover_color=verde_oscuro)
        self.mostrar_contra_button.place(x=75, y=265)
        
        self.config_peso_button = ctk.CTkButton(self.sub, text="Configurar Recordatorio Peso", command=self.mostrar_formulario_recordatorio, text_color=negro_texto, bg_color=gris
                                                , corner_radius=30, fg_color=verde_boton, width=310, height=55, font=("Arial",19, "bold"), hover_color=verde_oscuro)
        self.config_peso_button.place(x=75, y=365)
        
        self.cerrar_sesion_button = ctk.CTkButton(self.sub, text="Cerrar Sesión", text_color=negro_texto, bg_color=gris
                                                  , command=self.cerrar_sesion, corner_radius=20, fg_color=riesgo_medio, width=215, height=46, font=("Arial",16,"bold"), hover_color=riesgo_alto)
        self.cerrar_sesion_button.place(x=475, y=377)

        self.borrar_cuenta_button = ctk.CTkButton(self.sub, text="Borrar Cuenta", command=self.ventana_borrar_cuenta, text_color=negro_texto,bg_color=gris
                                                  , corner_radius=20, fg_color=riesgo_medio, width=215, height=46, font=("Arial", 16, "bold"), hover_color=riesgo_alto)
        self.borrar_cuenta_button.place(x=475, y=437)
        
    def mostrar_interfaz_guardar(self):
        edad, genero, peso, nivel_actividad,meta_cal, estatura  = self.cargar_datos_usuario()
        # Desactivar botones
        self.guardar_button.configure(state="disabled")
        self.mostrar_contra_button.configure(state="disabled")
        self.config_peso_button.configure(state="disabled")

        self.bg_boton_guardar = ctk.CTkButton(self.sub, text='', state="disabled", 
                                              bg_color=gris, fg_color=gris,
                                              corner_radius=35, width=390, height=385)
        self.bg_boton_guardar.place(x=45, y=100)
        
        # boton verde para la estatura
        self.bg_btn_estatura = ctk.CTkButton(self.sub, text='', bg_color=gris, state='disable', width=125, 
                                            height=40, corner_radius=20, fg_color=segundo_label)
        self.bg_btn_estatura.place(x=65, y=135)
        
        self.label_estatura = ctk.CTkLabel(self.sub, text="Estatura", text_color=negro_texto, bg_color=segundo_label, font=("Arial", 14, "bold"))
        self.label_estatura.place(x=82, y=140)
        
        # boton celeste para la estatura
        self.entry_estatura = ctk.CTkEntry(self.sub, fg_color=color_entry, bg_color=gris ,text_color=negro_texto, 
                                           width=210, height=40, corner_radius=20, font=("Arial", 14, "bold"))
        self.entry_estatura.insert(0, f"{estatura} cm") 
        self.entry_estatura.place(x=200, y=135)
        
        # boton verde para obj calorias
        self.bg_btn_obj = ctk.CTkButton(self.sub, text='', bg_color=gris, state='disable', width=125, 
                                            height=40, corner_radius=20, fg_color=segundo_label)
        self.bg_btn_obj.place(x=65, y=185)
        
        self.label_obj = ctk.CTkLabel(self.sub, text="Objetivo kcal", text_color=negro_texto, bg_color=segundo_label, font=("Arial", 14, "bold"))
        self.label_obj.place(x=82, y=190)
        
        # Entry para meta de calorías
        self.entry_obj = ctk.CTkEntry(self.sub, fg_color=color_entry, bg_color=gris ,text_color=negro_texto, 
                                      width=210, height=40, corner_radius=20, font=("Arial", 14, "bold"))
        self.entry_obj.insert(0, f"{meta_cal}")  # Mostrar valor actual
        self.entry_obj.place(x=200, y=185)
        
        # boton verde para el nivel de actividad
        self.bg_btn_nvl = ctk.CTkButton(self.sub, text='', bg_color=gris, state='disable', width=125, 
                                            height=40, corner_radius=20, fg_color=segundo_label)
        self.bg_btn_nvl.place(x=65, y=235)
        
        # label que muestra obj calorias
        self.label_nvl = ctk.CTkLabel(self.sub, text="Nivel act", text_color=negro_texto, bg_color=segundo_label, font=("Arial", 14, "bold"))
        self.label_nvl.place(x=82, y=240)
        
        # Combobox para nivel de actividad
        self.combobox_nvl = ctk.CTkComboBox(self.sub, values=["Sendatario", "Ligero", "Moderado","Intenso"], 
                                            fg_color=gris_label, bg_color=gris, text_color=negro_texto, 
                                            font=("Arial", 14, "bold"), corner_radius=20, width=210, height=40, button_color=verde_boton,
                                            button_hover_color=verde_oscuro)
        self.combobox_nvl.set(nivel_actividad)  # Mostrar valor actual
        self.combobox_nvl.place(x=200, y=235)
    
        self.boton_guardar = ctk.CTkButton(self.sub, text="Actualizar datos", 
                                           command=self.guardar,
                                           text_color=negro_texto, bg_color=gris,
                                           corner_radius=20, fg_color=verde_boton, 
                                           width=250, height=40, font=("Arial", 16, "bold"), hover_color=verde_oscuro)
        self.boton_guardar.place(x=120, y=350)

        self.boton_regresar = ctk.CTkButton(self.sub, text="Regresar", 
                                            command=self.restaurar_interfaz_actualizar_info,
                                            text_color=negro_texto, bg_color=gris,
                                            corner_radius=20, fg_color=riesgo_medio, 
                                            width=250, height=40, font=("Arial", 16, "bold"), hover_color=riesgo_alto)
        self.boton_regresar.place(x=120, y=410)

    def restaurar_interfaz_actualizar_info(self):
        if hasattr(self, 'bg_boton_guardar'):
            self.bg_boton_guardar.destroy()
        if hasattr(self, 'bg_btn_estatura'):
            self.bg_btn_estatura.destroy()
        if hasattr(self, 'label_estatura'):
            self.label_estatura.destroy()
        if hasattr(self, 'entry_estatura'):  
            self.entry_estatura.destroy()
        if hasattr(self, 'bg_btn_obj'):
            self.bg_btn_obj.destroy()
        if hasattr(self, 'label_obj'):
            self.label_obj.destroy()
        if hasattr(self, 'entry_obj'):  
            self.entry_obj.destroy()
        if hasattr(self, 'bg_btn_nvl'):
            self.bg_btn_nvl.destroy()
        if hasattr(self, 'label_nvl'):
            self.label_nvl.destroy()
        if hasattr(self, 'combobox_nvl'): 
            self.combobox_nvl.destroy()
        if hasattr(self, 'boton_guardar'):
            self.boton_guardar.destroy()
        if hasattr(self, 'boton_regresar'):
            self.boton_regresar.destroy()         
               
        # Reactivar los botones 
        self.guardar_button.configure(state="normal")
        self.mostrar_contra_button.configure(state="normal")
        self.config_peso_button.configure(state="normal")
        
    def cerrar_sesion(self):
        respuesta = CTkMessagebox(
            title="Cerrar Sesión", 
            message="¿Estás seguro de que deseas cerrar sesión?", 
            icon="warning", 
            option_1="Si", option_2="No"
        ).get()
        
        if respuesta == "Si":
            CTkMessagebox(title="Cerrar sesión", message="Sesión cerrada.") 
            self.panel_principal.after(2000, self.reiniciar_aplicacion)
    
    def ventana_borrar_cuenta(self):
        self.ventana_borrar = ctk.CTkToplevel(self.panel_principal)
        self.ventana_borrar.title("Confirmar Eliminación de Cuenta")
        self.ventana_borrar.geometry("400x250")
        self.ventana_borrar.attributes('-topmost', True)

        ctk.CTkLabel(self.ventana_borrar, text="Ingresa tu contraseña", font=("Arial", 20)).pack(padx=20, pady=(20, 10))

        self.contra_borrar_entry = ctk.CTkEntry(self.ventana_borrar, show="*", width=250, corner_radius=20, text_color="black")
        self.contra_borrar_entry.pack(padx=20, pady=(10, 20))

        self.btn_confirmar_borrar = ctk.CTkButton(self.ventana_borrar, text="Confirmar Eliminación", command=self.eliminar_cuenta, width=200, corner_radius=20, fg_color=riesgo_alto, hover_color=riesgo_alto, font=("Arial", 14, 'bold'))
        self.btn_confirmar_borrar.pack(pady=10)

        self.btn_cancelar_borrar = ctk.CTkButton(self.ventana_borrar, text="Cancelar", command=self.ventana_borrar.destroy, width=200, corner_radius=20, fg_color=riesgo_medio, hover_color=riesgo_alto, font=("Arial", 14, 'bold'))
        self.btn_cancelar_borrar.pack(pady=10)
        
    def reiniciar_aplicacion(self):
        # Close the current application
        self.panel_principal.quit()
        time.sleep(1)  # Give the application time to properly close

        # Reopen the application
        python = sys.executable
        script_path = os.path.abspath("main.py")
        subprocess.Popen([python, script_path])

        # Exit the current process
        sys.exit()
        
    def cargar_datos_usuario(self):
        """Obtiene la edad, el género, la meta de calorías, el nivel de actividad, la altura y el peso más reciente del usuario desde la base de datos."""
        try:
            conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
            cursor = conn.cursor()

            # Obtener datos del usuario, incluyendo la estatura
            cursor.execute("SELECT edad, genero, meta_cal, nivel_actividad, estatura FROM datos WHERE nombre = ?", (self.usuario,))
            user_data = cursor.fetchone()

            # Obtener el peso más reciente
            cursor.execute("SELECT peso, fecha FROM peso ORDER BY fecha DESC LIMIT 1")
            peso_data = cursor.fetchone()
            conn.close()

            if user_data and peso_data:
                edad, genero, meta_cal, nivel_actividad, estatura = user_data
                peso, fecha = peso_data  # Fecha y peso más recientes
                self.obj_calorias_original = meta_cal
                self.lvl_actividad_original = nivel_actividad
                return edad, genero, peso, nivel_actividad, meta_cal, estatura
            else:
                return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al acceder a la base de datos: {e}")
            return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"
        
    def mostrar_formulario_recordatorio(self):
        self.ventana_recordatorio = ctk.CTkToplevel(self.panel_principal, fg_color=gris)
        self.ventana_recordatorio.title("Configurar Recordatorio de Peso")
        self.ventana_recordatorio.geometry("400x230")
        self.ventana_recordatorio.attributes('-topmost', True)

        self.label_recordatorio = ctk.CTkLabel(self.ventana_recordatorio, text="Frecuencia de Recordatorio", fg_color=azul_medio_oscuro, font=("Arial", 20), width=250)
        self.label_recordatorio.configure(corner_radius=20)
        self.label_recordatorio.pack(pady=(20, 10))

        # ComboBox para seleccionar la frecuencia
        self.tiempo_recordatorio_combobox = ctk.CTkComboBox(
            self.ventana_recordatorio,
            values=["1 día", "3 días", "5 días", "1 semana", "1 mes"],
            width=250, border_width=0, corner_radius=20,
            fg_color=gris_label, button_color=verde_boton, button_hover_color=verde_oscuro, text_color=negro_texto
        )
        self.tiempo_recordatorio_combobox.pack(pady=5)

        # CheckBox para activar o desactivar el recordatorio
        self.activar_recordatorio_var = ctk.StringVar(value="on")
        self.activar_recordatorio_checkbox = ctk.CTkCheckBox(
            self.ventana_recordatorio, text="Activar Recordatorio", 
            variable=self.activar_recordatorio_var, onvalue="on", offvalue="off"
        )
        self.activar_recordatorio_checkbox.pack(anchor="w", padx=3, pady=5)

        # Botón para guardar la configuración
        ctk.CTkButton(
            self.ventana_recordatorio, text="Guardar Configuración", 
            command=self.guardar_configuracion_recordatorio, width=280,
            fg_color=verde_boton, hover_color=verde_oscuro, corner_radius=20, bg_color=gris, font=("Arial", 18, 'bold'), text_color=azul_medio_oscuro
        ).pack(pady=10)

        self.cargar_configuracion_recordatorio()
                      
    def cargar_configuracion_recordatorio(self):
        try:
            conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
            cursor = conn.cursor()

            cursor.execute("SELECT recordatorio, cantidad_dias FROM datos WHERE nombre = ?", (self.usuario,))
            config = cursor.fetchone()
            conn.close()

            if config:
                estado, frecuencia = config
                self.activar_recordatorio_var.set(estado)
                self.tiempo_recordatorio_combobox.set(frecuencia)
            else:
                self.activar_recordatorio_var.set("off")
                self.tiempo_recordatorio_combobox.set("1 día")
        except sqlite3.Error as e:
            CTkMessagebox(title="Error", message=f"Error al cargar configuración: {e}", icon="error", option_1="OK")

    def guardar_configuracion_recordatorio(self):
        estado = self.activar_recordatorio_var.get()
        frecuencia = self.tiempo_recordatorio_combobox.get()

        try:
            conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE datos 
                SET recordatorio = ?, cantidad_dias = ? 
                WHERE nombre = ?
            """, (estado, frecuencia, self.usuario))

            conn.commit()
            conn.close()

            CTkMessagebox(title="Confirmación", message="Configuración guardada correctamente.", icon="info", option_1="OK")
            self.ventana_recordatorio.destroy()
        except sqlite3.Error as e:
            CTkMessagebox(title="Error", message=f"Error al guardar configuración: {e}", icon="error", option_1="OK")

    def mostrar_formulario_contrasena(self):
        # Crea ventana contra
        self.nueva_ventana = ctk.CTkToplevel(self.panel_principal, fg_color=gris)
        self.nueva_ventana.title("Actualizar Contraseña")
        self.nueva_ventana.attributes('-topmost', True)
        self.nueva_ventana.geometry("400x400")  

        # muestra el nombre de usuario ingresado
        self.nombre_label = ctk.CTkLabel(self.nueva_ventana, text=f"Nombre de Usuario: {self.usuario}", width=280, fg_color=azul_medio_oscuro, font=("Arial", 20))
        self.nombre_label.configure(corner_radius=20)
        self.nombre_label.pack(pady=(20, 20))

        self.contra_anterior_label = ctk.CTkLabel(self.nueva_ventana, text="Contraseña Anterior", width=280, fg_color=azul_medio_oscuro, font=("Arial", 20))
        self.contra_anterior_label.configure(corner_radius=20)
        self.contra_anterior_label.pack(pady=(0, 4))

        self.contra_anterior_entry = ctk.CTkEntry(self.nueva_ventana, placeholder_text="Introduce tu contraseña anterior", width=280, show='*', corner_radius=20, border_width=0, fg_color=color_entry, text_color="black")
        self.contra_anterior_entry.pack(pady=(0, 20))

        self.nueva_contra_label = ctk.CTkLabel(self.nueva_ventana, text="Nueva Contraseña", width=280, fg_color=azul_medio_oscuro, font=("Arial", 20))
        self.nueva_contra_label.configure(corner_radius=20)
        self.nueva_contra_label.pack(pady=(0, 4))

        self.nueva_contra_entry = ctk.CTkEntry(self.nueva_ventana, placeholder_text="Introduce la nueva contraseña", width=280, show='*', corner_radius=20, border_width=0, fg_color=color_entry, text_color="black")
        self.nueva_contra_entry.pack(pady=(0, 20))

        self.confirmar_contra_label = ctk.CTkLabel(self.nueva_ventana, text="Confirmar Nueva Contraseña", width=280, fg_color=azul_medio_oscuro, font=("Arial", 20))
        self.confirmar_contra_label.configure(corner_radius=20)
        self.confirmar_contra_label.pack(pady=(0, 4))

        self.confirmar_contra_entry = ctk.CTkEntry(self.nueva_ventana, placeholder_text="Confirma la nueva contraseña", width=280, show='*', corner_radius=20, border_width=0, fg_color=color_entry, text_color="black")
        self.confirmar_contra_entry.pack(pady=(0, 20))

        self.actualizar_contra_button = ctk.CTkButton(self.nueva_ventana, text="Actualizar Contraseña", command=self.actualizar_contrasena, width=280,
                                                      fg_color=verde_boton, hover_color=verde_oscuro, corner_radius=20, bg_color=gris, font=("Arial", 18, 'bold'), text_color=azul_medio_oscuro)
        self.actualizar_contra_button.pack(pady=5)

    def guardar(self):
        
        edad, genero, peso, nivel_actividad,meta_cal, estatura  = self.cargar_datos_usuario()

        """Actualiza los datos de la base de datos con la nueva meta de calorías, estatura y nivel de actividad."""
        try:
            # Obtener valores de los campos
            nueva_estatura = self.entry_estatura.get().replace(" cm", "").strip()
            nueva_meta_calorias = self.entry_obj.get().strip()
            nuevo_nivel_actividad = self.combobox_nvl.get()

            # Validar cambios
            if nueva_estatura == str(estatura) and nueva_meta_calorias == str(meta_cal) and nuevo_nivel_actividad == nivel_actividad:
                CTkMessagebox(
                    title="Sin Cambios",
                    message="No se han realizado cambios en la información.",
                    icon="info",
                    option_1="OK"
                )
                return

            # Actualizar la base de datos
            conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE datos
                SET estatura = ?, meta_cal = ?, nivel_actividad = ?
                WHERE nombre = ?
            """, (nueva_estatura, nueva_meta_calorias, nuevo_nivel_actividad, self.usuario))
            conn.commit()
            conn.close()

            # Mensaje de confirmación
            CTkMessagebox(
                title="Confirmación",
                message="Los datos se actualizaron correctamente.",
                icon="info",
                option_1="OK"
            )
        except sqlite3.Error as e:
            CTkMessagebox(
                title="Error",
                message=f"Hubo un problema al guardar los datos en la base de datos: {e}",
                icon="warning",
                option_1="OK"
            )

    def actualizar_contrasena(self):
        nombre_usuario = self.usuario 
        contra_anterior = self.contra_anterior_entry.get()
        nueva_contra = self.nueva_contra_entry.get()
        confirmar_contra = self.confirmar_contra_entry.get()

        if not contra_anterior or not nueva_contra or not confirmar_contra:
            CTkMessagebox(title="Advertencia", message="Por favor, completa todos los campos.", icon="warning", option_1="Ok")
            return

        if nueva_contra != confirmar_contra:
            CTkMessagebox(title="Advertencia", message="La nueva contraseña y su confirmación no coinciden.", icon="warning", option_1="Ok")
            return

        try:
            conn = sqlite3.connect("./usuarios.db")
            cursor = conn.cursor()

            cursor.execute("SELECT contra FROM users WHERE nombre = ?", (nombre_usuario,))
            user = cursor.fetchone()

            if user and user[0] == contra_anterior:
                cursor.execute("UPDATE users SET contra = ? WHERE nombre = ?", (nueva_contra, nombre_usuario))
                conn.commit()
                CTkMessagebox(title="Confirmación", message="La contraseña ha sido actualizada correctamente.", icon="info", option_1="Ok")
            else:
                CTkMessagebox(title="Error", message="La contraseña anterior no es correcta.", icon="warning", option_1="Ok")

            conn.close()
        except sqlite3.Error as e:
            CTkMessagebox(title="Error", message=f"Error en la base de datos: {e}", icon="warning", option_1="Ok")

    def eliminar_cuenta(self):
        contra_ingresada = self.contra_borrar_entry.get()

        try:
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()

            query = "SELECT contra FROM users WHERE nombre = ?"
            cursor.execute(query, (self.usuario,))
            resultado = cursor.fetchone()

            if resultado and resultado[0] == contra_ingresada:
                respuesta_final = CTkMessagebox(
                    title="Última Confirmación", 
                    message="¿REALMENTE estás seguro de eliminar tu cuenta? Todos tus datos se perderán permanentemente.", 
                    icon="warning", 
                    option_1="Sí, eliminar", 
                    option_2="Cancelar"
                ).get()

                if respuesta_final != "Sí, eliminar":
                    conn.close()
                    return

                usuario_path = f'./users/{self.usuario}'
                if os.path.exists(usuario_path):
                    shutil.rmtree(usuario_path)

                query_eliminar = "DELETE FROM users WHERE nombre = ?"
                cursor.execute(query_eliminar, (self.usuario,))
                conn.commit()

                with open('usuario_actual.txt', 'w') as f:
                    f.write('')

                CTkMessagebox(title="Éxito", 
                            message="La cuenta se ha eliminado correctamente. La aplicación se cerrará.", 
                            icon="check", 
                            option_1="OK")
                
                self.ventana_borrar.destroy()
                
                # Llama a la función para reiniciar la aplicación
                self.reiniciar_aplicacion()

            else:
                CTkMessagebox(title="Error", 
                            message="La contraseña ingresada es incorrecta.", 
                            icon="warning", 
                            option_1="OK")

        except Exception as e:
            CTkMessagebox(title="Error", 
                        message=f"Error al eliminar la cuenta: {str(e)}", 
                        icon="warning", 
                        option_1="OK")

        finally:
            conn.close()
