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

    try:
        resultado = traducir(texto, origen, destino)
        salida_texto.delete("1.0", tk.END)
        salida_texto.insert(tk.END, resultado)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo traducir.\n{e}")


# ----------------- Ventana -----------------
ventana = tk.Tk()
ventana.title("Traductor Inteligente")
ventana.geometry("650x600")
ventana.config(bg="#f2f2f2")


# ----------------- Frame principal -----------------
frame = tk.Frame(ventana, bg="white", bd=2, relief="groove")
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)


# ----------------- Caja de ENTRADA -----------------
tk.Label(frame, text="Texto a traducir:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)

entrada_frame = tk.Frame(frame, bg="#ffffff", bd=2, relief="solid")
entrada_frame.pack(fill=tk.BOTH, padx=10, pady=5)

entrada_texto = tk.Text(entrada_frame, height=7, font=("Arial", 11), bd=0)
entrada_texto.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


# ----------------- Selección de idiomas -----------------
idiomas_frame = tk.Frame(frame, bg="white")
idiomas_frame.pack(pady=10)

tk.Label(idiomas_frame, text="Origen:", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=10)
combo_origen = ttk.Combobox(idiomas_frame, values=["es", "en", "fr", "it"], width=7)
combo_origen.set("es")
combo_origen.grid(row=0, column=1)

tk.Label(idiomas_frame, text="Destino:", font=("Arial", 11), bg="white").grid(row=0, column=2, padx=10)
combo_destino = ttk.Combobox(idiomas_frame, values=["es", "en", "fr", "it"], width=7)
combo_destino.set("en")
combo_destino.grid(row=0, column=3)


# ----------------- Botón traducir -----------------
boton = tk.Button(frame, text="🔄 Traducir", font=("Arial", 12, "bold"),
                bg="#4caf50", fg="white", pady=5, padx=10,
                command=traducir_texto)
boton.pack(pady=10)


# ----------------- Caja de SALIDA -----------------
tk.Label(frame, text="Traducción:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)

salida_frame = tk.Frame(frame, bg="#ffffff", bd=2, relief="solid")
salida_frame.pack(fill=tk.BOTH, padx=10, pady=5)

salida_texto = tk.Text(salida_frame, height=7, font=("Arial", 11), bd=0)
salida_texto.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


ventana.mainloop()
