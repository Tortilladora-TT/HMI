import tkinter as tk
from tkinter import messagebox

# Función para cambiar de pantalla
def mostrar_modo_diagnostico():
    pantalla_principal.pack_forget()  # Ocultar pantalla principal
    pantalla_diagnostico.pack(fill="both", expand=True)  # Mostrar pantalla de diagnóstico

def regresar_a_principal():
    pantalla_diagnostico.pack_forget()  # Ocultar pantalla de diagnóstico
    pantalla_principal.pack(fill="both", expand=True)  # Mostrar pantalla principal

def opcion_dosificacion():
    messagebox.showinfo("Dosificación", "Verificando el sistema de dosificación...")

def opcion_corte():
    messagebox.showinfo("Corte", "Verificando el sistema de corte...")

def opcion_compresion():
    messagebox.showinfo("Compresión y Cocción", "Verificando el sistema de compresión y cocción...")

# Función para alternar pantalla completa
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Función para salir de pantalla completa
def salir_pantalla_completa(event=None):
    root.attributes("-fullscreen", False)

# Crear la ventana principal
root = tk.Tk()
root.title("Selección de Modos")
root.geometry("800x600")
root.config(bg="#f5f2d0")  # Color de fondo beige

# Activar pantalla completa al inicio
root.attributes("-fullscreen", True)

# Atajos de teclado para salir de pantalla completa
root.bind("<F11>", toggle_fullscreen)  # Presionar F11 para alternar pantalla completa
root.bind("<Escape>", salir_pantalla_completa)  # Presionar Escape para salir

# ------------------------- Pantalla Principal -------------------------
pantalla_principal = tk.Frame(root, bg="#f5f2d0")

titulo = tk.Label(pantalla_principal, text="Selección de Modos", font=("Arial Black", 24), bg="#f5f2d0")
titulo.pack(pady=20)

subtitulo = tk.Label(pantalla_principal, text="Selecciona el modo de operación deseado", font=("Arial", 14), bg="#f5f2d0")
subtitulo.pack(pady=10)

frame_botones = tk.Frame(pantalla_principal, bg="#f5f2d0")
frame_botones.pack(pady=50)

btn_automatico = tk.Button(
    frame_botones, 
    text="MODO\nAUTOMÁTICO", 
    font=("Arial", 16, "bold"), 
    bg="#c6e5ff", 
    fg="#000080", 
    width=20, 
    height=10, 
    command=lambda: messagebox.showinfo("Modo Automático", "Entrando en el Modo Automático...")
)
btn_automatico.grid(row=0, column=0, padx=20)

btn_diagnostico = tk.Button(
    frame_botones, 
    text="MODO\nDIAGNÓSTICO", 
    font=("Arial", 16, "bold"), 
    bg="#ffc6c6", 
    fg="#000080", 
    width=20, 
    height=10, 
    command=mostrar_modo_diagnostico
)
btn_diagnostico.grid(row=0, column=1, padx=20)

# ------------------------- Pantalla de Diagnóstico -------------------------
pantalla_diagnostico = tk.Frame(root, bg="#f5f2d0")

titulo_diag = tk.Label(pantalla_diagnostico, text="MODO DIAGNÓSTICO", font=("Arial Black", 24), bg="#f5f2d0")
titulo_diag.pack(pady=20)

subtitulo_diag = tk.Label(
    pantalla_diagnostico, 
    text="Selecciona la opción que le gustaría verificar.\nRecuerda: este modo NO NECESITA MASA.", 
    font=("Arial", 14), 
    bg="#f5f2d0"
)
subtitulo_diag.pack(pady=10)

frame_opciones = tk.Frame(pantalla_diagnostico, bg="#f5f2d0")
frame_opciones.pack(pady=50)

btn_dosificacion = tk.Button(
    frame_opciones, 
    text="DOSIFICACIÓN", 
    font=("Arial", 16, "bold"), 
    bg="#f7c6e6", 
    fg="black", 
    width=20, 
    height=5, 
    command=opcion_dosificacion
)
btn_dosificacion.grid(row=0, column=0, padx=20, pady=10)

btn_corte = tk.Button(
    frame_opciones, 
    text="CORTE", 
    font=("Arial", 16, "bold"), 
    bg="#f7c6e6", 
    fg="black", 
    width=20, 
    height=5, 
    command=opcion_corte
)
btn_corte.grid(row=0, column=1, padx=20, pady=10)

btn_compresion = tk.Button(
    frame_opciones, 
    text="COMPRESIÓN Y COCCIÓN", 
    font=("Arial", 16, "bold"), 
    bg="#d1c4e9", 
    fg="black", 
    width=45, 
    height=5, 
    command=opcion_compresion
)
btn_compresion.grid(row=1, column=0, columnspan=2, pady=10)

btn_regresar = tk.Button(
    pantalla_diagnostico, 
    text="↩️ Regresar", 
    font=("Arial", 14), 
    bg="#ccffcc", 
    fg="black", 
    command=regresar_a_principal
)
btn_regresar.pack(side="top", anchor="ne", padx=10, pady=10)

# Mostrar pantalla principal al inicio
pantalla_principal.pack(fill="both", expand=True)

# Ejecutar la aplicación
root.mainloop()
