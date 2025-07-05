import re

def extraer_coordenadas(archivo_entrada, archivo_salida):
    """
    Extrae solo las coordenadas del archivo OCR y las guarda en un nuevo archivo.
    """
    with open(archivo_entrada, 'r', encoding='utf-8') as f_in, open(archivo_salida, 'w', encoding='utf-8') as f_out:
        nombre_imagen = ""
        procesando_nueva_imagen = False
        
        for linea in f_in:
            linea = linea.strip()
            
            # Detectar nombre de archivo de imagen
            if linea.lower().endswith(('.jpeg:', '.jpg:', '.png:')):
                nombre_imagen = linea.replace(':', '')
                procesando_nueva_imagen = True
                continue
            
            # Si estamos procesando una nueva imagen y la línea contiene coordenadas
            if procesando_nueva_imagen and re.search(r'\d+\.\d+[NnSs]\s+\d+\.\d+[WwEe]', linea):
                # Formatear la línea para tener solo las coordenadas
                coordenadas = linea.strip()
                f_out.write(f"{nombre_imagen}:\n{coordenadas}\n{'-'*60}\n")
                procesando_nueva_imagen = False
                
            # Detectar final de bloque
            if linea.startswith('-' * 10):
                procesando_nueva_imagen = False

if __name__ == "__main__":
    archivo_entrada = "textos_easyocr.txt"
    archivo_salida = "coordenadas_extraidas.txt"
    
    extraer_coordenadas(archivo_entrada, archivo_salida)
    print(f"Coordenadas extraídas correctamente y guardadas en {archivo_salida}")