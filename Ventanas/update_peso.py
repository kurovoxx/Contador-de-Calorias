import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
from util.colores import *
import sqlite3


class Peso(ctk.CTkToplevel):
    def __init__(self, parent, user, callback=None):
        super().__init__(parent)
        self.parent = parent
        self.usuario = user
        self.callback = callback
        self.geometry('400x270')
        self.title('Actualizar peso')
        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.main_frame = ctk.CTkFrame(self, fg_color=gris, corner_radius=0)
        self.main_frame.pack(fill='both', expand=True)
        self.add_widget()

    def add_widget(self):
        self.peso_actual_label = ctk.CTkLabel(self.main_frame, text=self.get_peso(), font=("Arial", 20, 'bold'))
        self.peso_actual_label.pack(padx=3, pady=(40, 30))

        self.peso_label = ctk.CTkLabel(self.main_frame, text="Ingrese su peso actual", fg_color=azul_medio_oscuro, font=("Arial", 20), width=250)
        self.peso_label.configure(corner_radius=20)
        self.peso_label.pack(padx=3, pady=(10, 10))

        self.peso_entry = ctk.CTkEntry(
            self.main_frame, width=250, corner_radius=20, border_width=0, fg_color='white', text_color='black')
        self.peso_entry.pack(padx=3, pady=(0, 20))

        self.guardar_button = ctk.CTkButton(
            self.main_frame, text="Registrar", width=250, corner_radius=20,
            fg_color=verde_boton, hover_color=verde_oscuro, command=self.registrar_peso, text_color=azul_medio_oscuro, font=("Arial", 18, 'bold'))
        self.guardar_button.pack(pady=10)
    
    def registrar_peso(self):
        peso = self.peso_entry.get()
        if peso == '' or peso is None:
            CTkMessagebox(title="Advertencia", message="Ingrese un peso.",
                        icon='warning', option_1="Ok")
        else:
            try:
                # Reemplazar coma por punto para admitir formatos comunes de decimales
                peso = peso.replace(',', '.')
                # Intentar convertir el peso a decimal
                peso = float(peso)
                print(peso)

                try:
                    conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
                    cursor = conn.cursor()

                    if datetime.now().strftime('%d-%m-%Y') == self.get_fecha():
                        CTkMessagebox(title="Advertencia", message="Solo puedes registrar tu peso una ves al día.",
                                icon='warning', option_1="Ok")
                    
                    else:
                        query = "INSERT INTO peso (fecha, peso) VALUES (?, ?)"
                        cursor.execute(query, (datetime.now().strftime('%d-%m-%Y'), peso))

                        conn.commit()

                        CTkMessagebox(title="Exito", message="Peso actualizado",
                                    icon='check',
                                    option_1="Ok")

                except sqlite3.IntegrityError:
                    CTkMessagebox(title="Advertencia", message="Solo puedes registrar tu peso una ves al día.",
                                icon='warning', option_1="Ok")

                finally:
                    conn.close()
                
                if self.callback:
                    self.callback()

                self.destroy()
            except ValueError:
                CTkMessagebox(title="Advertencia", message="Ingrese un peso válido.",
                            icon='warning', option_1="Ok")
    
    def get_peso(self):
        conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
        cursor = conn.cursor()

        query = "SELECT peso FROM peso ORDER BY num DESC LIMIT 1;"
        cursor.execute(query)
        resultado = cursor.fetchone()

        if resultado:
            peso_str = resultado[0]  # Esto te dará la fecha como un string
            conn.commit()
            conn.close()
            return f'Su último peso registrado fue: {peso_str}'
        else:
            peso_str = None  # Si no hay registros en la tabla
            conn.commit()
            conn.close()
            return 'Aún no has registrado tu peso!'
    
    def get_fecha(self):
        conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
        cursor = conn.cursor()

        query = "SELECT fecha FROM peso ORDER BY num DESC LIMIT 1;"
        cursor.execute(query)
        resultado = cursor.fetchone()

        if resultado:
            fecha_str = resultado[0]  # Esto te dará la fecha como un string
            conn.commit()
            conn.close()
            return fecha_str
        else:
            conn.commit()
            conn.close()
            return
