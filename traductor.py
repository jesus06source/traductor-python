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

def traducir(texto, origen, destino):
    clave = f"{origen}->{destino}"

    if clave not in MODELOS:
        return "Error: combinación de idiomas no soportada."

    modelo_nombre = MODELOS[clave]

    tokenizer = MarianTokenizer.from_pretrained(modelo_nombre)
    model = MarianMTModel.from_pretrained(modelo_nombre)

    # Dividir texto por líneas o puntos para traducir todo
    oraciones = [s.strip() for s in texto.replace("?", ".").replace("!", ".").split(".") if s.strip()]
    traducciones = []
    for oracion in oraciones:
        tokens = tokenizer([oracion], return_tensors="pt", padding=True)
        traduccion_ids = model.generate(**tokens)
        traducciones.append(tokenizer.decode(traduccion_ids[0], skip_special_tokens=True))

    return " ".join(traducciones)
