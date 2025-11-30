import tkinter as tk
from tkinter import ttk, messagebox
from traductor import traducir
import pyttsx3 # type: ignore

# ----- Lista global para historial -----
historial_traducciones = []

# ----- Función mejorada para buscar voz según idioma -----
def _buscar_voz_por_codigo(engine, codigo_iso):
    """
    Busca la mejor voz disponible según el código ISO del idioma.
    Prioriza voces que contengan el idioma exacto en name o id.
    Si no encuentra exacta, devuelve la primera voz que contenga el idioma.
    """
    voces = engine.getProperty("voices")
    busc = codigo_iso.lower()
    primera_opcion = None

    for v in voces:
        try:
            langs = getattr(v, "languages", None)
            if langs:
                for L in langs:
                    s = L.decode("utf-8").lower() if isinstance(L, bytes) else str(L).lower()
                    if busc in s:
                        return v.id  # voz exacta encontrada
        except:
            pass
        
        # Busca coincidencia parcial en name o id
        if busc in str(v.name).lower() or busc in str(v.id).lower():
            if not primera_opcion:
                primera_opcion = v.id

    # Si no se encontró exacta, retorna la primera parcial
    return primera_opcion


# 🔊 Nueva función de Texto a voz
def texto_a_voz():
    texto = salida_texto.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Error", "No hay texto para reproducir.")
        return

    idioma_destino = combo_destino.get()

    engine = pyttsx3.init()

    try:
        voz_id = _buscar_voz_por_codigo(engine, idioma_destino)
        if voz_id:
            engine.setProperty("voice", voz_id)
        else:
            messagebox.showinfo("Aviso", f"No se encontró voz específica para '{idioma_destino}'. Se usará la voz por defecto.")

        engine.setProperty("rate", 150)
        engine.setProperty("volume", 1.0)

        engine.say(texto)
        engine.runAndWait()

    except Exception as e:
        messagebox.showerror("Error TTS", f"No se pudo reproducir el audio.\n{e}")
    finally:
        try:
            engine.stop()
        except:
            pass


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

        # ----- Guardar en historial -----
        historial_traducciones.append({
            "origen": origen,
            "destino": destino,
            "texto_original": texto,
            "traduccion": resultado
        })

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


def mostrar_historial():
    if not historial_traducciones:
        messagebox.showinfo("Historial", "No hay traducciones aún.")
        return

    # Ventana emergente
    ventana_historial = tk.Toplevel(ventana)
    ventana_historial.title("Historial de Traducciones")
    ventana_historial.geometry("550x450")
    ventana_historial.config(bg="#f0f0f0")

    # Frame para scrollbar
    frame_hist = tk.Frame(ventana_historial, bg="#f0f0f0")
    frame_hist.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Scrollbar
    scrollbar = tk.Scrollbar(frame_hist)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Text con estilo
    text_historial = tk.Text(frame_hist, wrap="word", font=("Segoe UI", 10), yscrollcommand=scrollbar.set,
                            bg="white", fg="#333", bd=0, padx=10, pady=10)
    text_historial.pack(fill=tk.BOTH, expand=True)

    scrollbar.config(command=text_historial.yview)

    # Insertar traducciones con formato
    for idx, item in enumerate(historial_traducciones, start=1):
        text_historial.insert(tk.END, f"Traducción #{idx}\n", "titulo")
        text_historial.insert(tk.END, f"Idioma: {item['origen']} → {item['destino']}\n", "subtitulo")
        text_historial.insert(tk.END, f"Original: {item['texto_original']}\n", "contenido")
        text_historial.insert(tk.END, f"Traducción: {item['traduccion']}\n", "contenido")
        text_historial.insert(tk.END, "\n" + "-"*50 + "\n\n", "separador")

    # Configurar tags de estilo
    text_historial.tag_config("titulo", font=("Segoe UI", 11, "bold"), foreground="#1976d2")
    text_historial.tag_config("subtitulo", font=("Segoe UI", 10, "italic"), foreground="#555")
    text_historial.tag_config("contenido", font=("Segoe UI", 10), foreground="#333")
    text_historial.tag_config("separador", foreground="#999")

    text_historial.config(state="disabled")  # Solo lectura



# ---------- Ventana ----------
ventana = tk.Tk()
ventana.title("Traductor Inteligente")
ventana.geometry("680x620")
ventana.config(bg="#e8ecf1")
ventana.update_idletasks()
w = 680; h = 620
x = (ventana.winfo_screenwidth() // 2) - (w // 2)
y = (ventana.winfo_screenheight() // 2) - (h // 2)
ventana.geometry(f"{w}x{h}+{x}+{y}")


# ---------- Frame ----------
frame = tk.Frame(ventana, bg="white", bd=3, relief="ridge", padx=15, pady=15)
frame.pack(padx=25, pady=25, fill=tk.BOTH, expand=True)

tk.Label(frame, text="🌐 Traductor Inteligente", font=("Segoe UI", 18, "bold"), bg="white", fg="#333").pack(pady=10)


# ---------- Entrada ----------
tk.Label(frame, text="Texto a traducir:", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", padx=5, pady=5)

entrada_frame = tk.Frame(frame, bg="#f8f8f8", bd=2, relief="solid")
entrada_frame.pack(fill=tk.BOTH, padx=10, pady=5)

entrada_texto = tk.Text(entrada_frame, height=7, font=("Segoe UI", 11), bd=0, wrap="word")
entrada_texto.pack(fill=tk.BOTH, expand=True, padx=7, pady=7)


# ---------- Idiomas ----------
idiomas_frame = tk.Frame(frame, bg="white")
idiomas_frame.pack(pady=10)

estilo = ttk.Style()
estilo.configure("TCombobox", padding=5, font=("Segoe UI", 10))

tk.Label(idiomas_frame, text="Origen:", font=("Segoe UI", 11), bg="white").grid(row=0, column=0, padx=10)
combo_origen = ttk.Combobox(idiomas_frame, values=["es", "en", "fr", "it"], width=8)
combo_origen.set("es")
combo_origen.grid(row=0, column=1)

boton_intercambiar = tk.Button(idiomas_frame, text="⇆", font=("Segoe UI", 12, "bold"), bg="#1976d2",
                            fg="white", bd=0, padx=8, pady=2, activebackground="#1565c0",
                            command=intercambiar_idiomas)
boton_intercambiar.grid(row=0, column=2, padx=(10,0))

tk.Label(idiomas_frame, text="Destino:", font=("Segoe UI", 11), bg="white").grid(row=0, column=3, padx=10)
combo_destino = ttk.Combobox(idiomas_frame, values=["es", "en", "fr", "it"], width=8)
combo_destino.set("en")
combo_destino.grid(row=0, column=4)


# ---------- Botones ----------
tk.Button(frame, text="🔄 Traducir", font=("Segoe UI", 12, "bold"), bg="#4caf50", fg="white", bd=0,
        pady=7, padx=12, activebackground="#43a047", command=traducir_texto).pack(pady=8)

tk.Button(frame, text="🧹 Limpiar ", font=("Segoe UI", 12, "bold"), bg="#e53935", fg="white", bd=0,
        pady=7, padx=12, activebackground="#c62828", command=limpiar_texto).pack(pady=5)

tk.Button(frame, text="🔊 Escuchar", font=("Segoe UI", 12, "bold"), bg="#1976d2", fg="white", bd=0,
        pady=7, padx=12, activebackground="#1565c0", command=texto_a_voz).pack(pady=5)

tk.Button(frame, text="📜 Historial", font=("Segoe UI", 12, "bold"), bg="#ff9800", fg="white", bd=0,
        pady=7, padx=12, activebackground="#fb8c00", command=mostrar_historial).pack(pady=5)


# ---------- Salida ----------
tk.Label(frame, text="Traducción:", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", padx=5, pady=5)

salida_frame = tk.Frame(frame, bg="#f8f8f8", bd=2, relief="solid")
salida_frame.pack(fill=tk.BOTH, padx=10, pady=5)

salida_texto = tk.Text(salida_frame, height=7, font=("Segoe UI", 11), bd=0, wrap="word")
salida_texto.pack(fill=tk.BOTH, expand=True, padx=7, pady=7)


ventana.mainloop()
