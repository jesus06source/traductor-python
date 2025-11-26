import tkinter as tk
from tkinter import ttk, messagebox
from traductor import traducir

def traducir_texto():
    texto = entrada_texto.get("1.0", tk.END).strip()
    origen = combo_origen.get()
    destino = combo_destino.get()

    if not texto:
        messagebox.showwarning("Error", "Debe ingresar un texto para traducir.")
        return

    if origen == destino:
        messagebox.showinfo("Sin cambios", "El idioma de origen y destino son iguales.")
        return

    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, "⏳ Traduciendo...")
    ventana.update_idletasks()

    try:
        resultado = traducir(texto, origen, destino)
        salida_texto.delete("1.0", tk.END)
        salida_texto.insert(tk.END, resultado)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo traducir.\n{e}")

def limpiar_texto():
    entrada_texto.delete("1.0", tk.END)
    salida_texto.delete("1.0", tk.END)

def intercambiar_idiomas():
    idioma_origen = combo_origen.get()
    idioma_destino = combo_destino.get()
    combo_origen.set(idioma_destino)
    combo_destino.set(idioma_origen)

# ----------------- Ventana -----------------
ventana = tk.Tk()
ventana.title("Traductor Inteligente")
ventana.geometry("680x620")
ventana.config(bg="#e8ecf1")

ventana.update_idletasks()
w = 680
h = 620
x = (ventana.winfo_screenwidth() // 2) - (w // 2)
y = (ventana.winfo_screenheight() // 2) - (h // 2)
ventana.geometry(f"{w}x{h}+{x}+{y}")

# ----------------- Frame principal -----------------
frame = tk.Frame(
    ventana,
    bg="white",
    bd=3,
    relief="ridge",
    padx=15,
    pady=15
)
frame.pack(padx=25, pady=25, fill=tk.BOTH, expand=True)

tk.Label(
    frame,
    text="🌐 Traductor Inteligente",
    font=("Segoe UI", 18, "bold"),
    bg="white",
    fg="#333"
).pack(pady=10)

# ----------------- Caja de ENTRADA -----------------
tk.Label(frame, text="Texto a traducir:", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", padx=5, pady=5)

entrada_frame = tk.Frame(frame, bg="#f8f8f8", bd=2, relief="solid")
entrada_frame.pack(fill=tk.BOTH, padx=10, pady=5)

entrada_texto = tk.Text(entrada_frame, height=7, font=("Segoe UI", 11), bd=0, wrap="word")
entrada_texto.pack(fill=tk.BOTH, expand=True, padx=7, pady=7)

# ----------------- Selección de idiomas -----------------
idiomas_frame = tk.Frame(frame, bg="white")
idiomas_frame.pack(pady=10)

estilo = ttk.Style()
estilo.configure("TCombobox", padding=5, font=("Segoe UI", 10))

tk.Label(idiomas_frame, text="Origen:", font=("Segoe UI", 11), bg="white").grid(row=0, column=0, padx=10)
combo_origen = ttk.Combobox(idiomas_frame, values=["es", "en", "fr", "it"], width=8)
combo_origen.set("es")
combo_origen.grid(row=0, column=1)

# 🔄 Botón de intercambiar idiomas
boton_intercambiar = tk.Button(
    idiomas_frame,
    text="⇆",
    font=("Segoe UI", 12, "bold"),
    bg="#1976d2",
    fg="white",
    bd=0,
    padx=8, pady=2,
    activebackground="#1565c0",
    command=intercambiar_idiomas
)
boton_intercambiar.grid(row=0, column=2, padx=(10,0))

tk.Label(idiomas_frame, text="Destino:", font=("Segoe UI", 11), bg="white").grid(row=0, column=3, padx=10)
combo_destino = ttk.Combobox(idiomas_frame, values=["es", "en", "fr", "it"], width=8)
combo_destino.set("en")
combo_destino.grid(row=0, column=4)

# ----------------- Botones -----------------
boton = tk.Button(
    frame,
    text="🔄 Traducir",
    font=("Segoe UI", 12, "bold"),
    bg="#4caf50",
    fg="white",
    bd=0,
    pady=7,
    padx=12,
    activebackground="#43a047",
    command=traducir_texto
)
boton.pack(pady=8)

boton_limpiar = tk.Button(
    frame,
    text="🧹 Limpiar ",
    font=("Segoe UI", 12, "bold"),
    bg="#e53935",
    fg="white",
    bd=0,
    pady=7,
    padx=12,
    activebackground="#c62828",
    command=limpiar_texto
)
boton_limpiar.pack(pady=5)

# ----------------- Caja de SALIDA -----------------
tk.Label(frame, text="Traducción:", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", padx=5, pady=5)

salida_frame = tk.Frame(frame, bg="#f8f8f8", bd=2, relief="solid")
salida_frame.pack(fill=tk.BOTH, padx=10, pady=5)

salida_texto = tk.Text(salida_frame, height=7, font=("Segoe UI", 11), bd=0, wrap="word")
salida_texto.pack(fill=tk.BOTH, expand=True, padx=7, pady=7)

ventana.mainloop()
