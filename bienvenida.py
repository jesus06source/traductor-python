import tkinter as tk
import subprocess
import sys
import os

def abrir_main():
    ventana_bienvenida.destroy() 

    
    ruta_main = "main.py" 

    subprocess.Popen([sys.executable, ruta_main])



ventana_bienvenida = tk.Tk()
ventana_bienvenida.title("Bienvenido al Traductor")
ventana_bienvenida.geometry("450x260")
ventana_bienvenida.configure(bg="#dfe9ff")

ventana_bienvenida.eval('tk::PlaceWindow . center')


frame = tk.Frame(
    ventana_bienvenida,
    bg="white",
    padx=25,
    pady=25,
    relief="raised",
    bd=4
)
frame.place(relx=0.5, rely=0.5, anchor="center")


label_titulo = tk.Label(
    frame,
    text="Bienvenido al Traductor",
    font=("Segoe UI", 18, "bold"),
    bg="white"
)
label_titulo.pack(pady=(5, 10))


label_sub = tk.Label(
    frame,
    text="Haz clic en el botón para comenzar",
    font=("Segoe UI", 11),
    bg="white",
    fg="#555555"
)
label_sub.pack(pady=(0, 15))


boton_iniciar = tk.Button(
    frame,
    text="Iniciar",
    command=abrir_main,
    font=("Segoe UI", 14, "bold"),
    bg="#4a90e2",
    fg="white",
    padx=12,
    pady=6,
    activebackground="#357ABD",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)
boton_iniciar.pack(pady=10)

ventana_bienvenida.mainloop()
