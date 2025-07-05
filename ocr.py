import easyocr
import os

# Crear lector con idioma español
reader = easyocr.Reader(['es'], gpu=False)

carpeta = "imagenes"
archivo_salida = "textos_easyocr.txt"

with open(archivo_salida, "w", encoding="utf-8") as f_out:
    for archivo in os.listdir(carpeta):
        if not archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        ruta = os.path.join(carpeta, archivo)
        resultados = reader.readtext(ruta, detail=0)

        texto_extraido = '\n'.join(resultados)

        print(f"\n[{archivo}]:\n{texto_extraido}\n{'-'*60}")
        f_out.write(f"{archivo}:\n{texto_extraido}\n{'-'*60}\n")