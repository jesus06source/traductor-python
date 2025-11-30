from transformers import MarianMTModel, MarianTokenizer

# Modelos soportados
MODELOS = {
    "es->en": "Helsinki-NLP/opus-mt-es-en",
    "en->es": "Helsinki-NLP/opus-mt-en-es",
    "es->fr": "Helsinki-NLP/opus-mt-es-fr",
    "fr->es": "Helsinki-NLP/opus-mt-fr-es",
    "es->it": "Helsinki-NLP/opus-mt-es-it",
    "it->es": "Helsinki-NLP/opus-mt-it-es",
    "en->fr": "Helsinki-NLP/opus-mt-en-fr",
    "fr->en": "Helsinki-NLP/opus-mt-fr-en",
    "en->it": "Helsinki-NLP/opus-mt-en-it",
    "it->en": "Helsinki-NLP/opus-mt-it-en",
    "fr->it": "Helsinki-NLP/opus-mt-fr-it",
    "it->fr": "Helsinki-NLP/opus-mt-it-fr"
}

# Almacena modelos ya cargados para no recargar cada vez
cache_modelos = {}

def cargar_modelo(clave):
    if clave not in cache_modelos:
        modelo_nombre = MODELOS[clave]
        tokenizer = MarianTokenizer.from_pretrained(modelo_nombre)
        model = MarianMTModel.from_pretrained(modelo_nombre)
        cache_modelos[clave] = (tokenizer, model)
    return cache_modelos[clave]

def traducir(texto, origen, destino):
    clave = f"{origen}->{destino}"

    if clave not in MODELOS:
        return "Error: combinación de idiomas no soportada."

    tokenizer, model = cargar_modelo(clave)

    # Separar el texto para no cortar traducción
    oraciones = [s.strip() for s in texto.split(".") if s.strip()]
    traducciones = []

    for oracion in oraciones:
        tokens = tokenizer([oracion], return_tensors="pt", padding=True)
        traduccion_ids = model.generate(**tokens)
        traducciones.append(tokenizer.decode(traduccion_ids[0], skip_special_tokens=True))

    return " ".join(traducciones)

#probando el traductor