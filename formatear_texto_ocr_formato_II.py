import re

def normalizar_coordenada(texto):
    """Normaliza y extrae coordenadas en formato estándar del texto OCR"""
    # Normalizar texto
    texto = texto.replace('\n', ' ').strip()
    
    # Correcciones comunes para latitud
    correcciones_lat = {
        'N 00': 'N 10', 'N 100': 'N 10', 'N 109': 'N 10', 'N102': 'N 10', 
        'N1Os': 'N 10', 'N/0?': 'N 10', 'NFoe': 'N 10', 'N 700': 'N 10',
        'NTO?': 'N 10', 'N.1O?': 'N 10', 'N+09': 'N 10', 'Nadoes': 'N 10',
        'NJ00': 'N 10', 'no': 'N 10', 'IiO': 'N 10', 'N?': 'N 10', 'ao|4': 'N 10',
        '4-IO': 'N 10', '4-109': 'N 10', 'N510': 'N 10', 'NO29': 'N 10', 'N07': 'N 10'
    }
    
    # Correcciones comunes para longitud
    correcciones_lon = {
        'WE': 'W', 'WNi': 'W', 'We7A9': 'W 74', 'WA7': 'W 74',
        'W748': 'W 74', 'W749': 'W 74', 'W740': 'W 74'
    }
    
    # Aplicar correcciones
    for patron, reemplazo in correcciones_lat.items():
        texto = texto.replace(patron, reemplazo)
    
    for patron, reemplazo in correcciones_lon.items():
        texto = texto.replace(patron, reemplazo)
    
    # Reemplazar caracteres incorrectos
    texto = texto.replace('M', '1')  # OCR a menudo confunde M con 1
    texto = texto.replace('o', '0')   # OCR a menudo confunde o con 0
    texto = texto.replace('*', "'")   # OCR a menudo confunde * con '
    
    # Extraer componentes de latitud
    lat_match = re.search(r'N\s*(\d+)[^\d\w]*(\d+)[^\d\w]*(\d+)', texto)
    if not lat_match:
        lat_match = re.search(r'N\s*(\d+)[^\d\w]*(\d+)', texto)
    
    # Extraer componentes de longitud
    lon_match = re.search(r'W\s*(\d+)[^\d\w]*(\d+)[^\d\w]*(\d+)', texto)
    if not lon_match:
        lon_match = re.search(r'W\s*(\d+)[^\d\w]*(\d+)', texto)
    
    # Procesar coordenadas
    if lat_match and lon_match:
        # Extraer grupos de latitud
        lat_groups = lat_match.groups()
        lat_deg = lat_groups[0]
        lat_min = lat_groups[1]
        lat_sec = lat_groups[2] if len(lat_groups) > 2 else "00"
        
        # Extraer grupos de longitud
        lon_groups = lon_match.groups()
        lon_deg = lon_groups[0]
        lon_min = lon_groups[1]
        lon_sec = lon_groups[2] if len(lon_groups) > 2 else "00"
        
        # Correcciones específicas
        if lat_deg == '00' or lat_deg == '0': lat_deg = '10'
        if len(lat_deg) > 2: lat_deg = '10'
        if len(lon_deg) > 2: lon_deg = '74'
        
        # Formatear la salida en el formato requerido
        return f"N {lat_deg}° {lat_min}' {lat_sec}\", W {lon_deg}° {lon_min}' {lon_sec}\""
    
    return "Coordenadas no encontradas"

def procesar_archivo():
    archivo_entrada = "textos_easyocr.txt"
    archivo_salida = "coordenadas_formato_estandar.txt"
    
    with open(archivo_entrada, "r", encoding="utf-8") as f_in, open(archivo_salida, "w", encoding="utf-8") as f_out:
        nombre_imagen = ""
        lineas_coordenadas = []
        
        for linea in f_in:
            linea = linea.strip()
            
            # Detectar nombre de imagen
            if linea.lower().endswith((".jpeg:", ".jpg:", ".png:")):
                # Procesar imagen anterior si existe
                if nombre_imagen and lineas_coordenadas:
                    texto_coordenadas = " ".join(lineas_coordenadas)
                    coordenada = normalizar_coordenada(texto_coordenadas)
                    f_out.write(f"{nombre_imagen}:\n{coordenada}\n{'-'*60}\n")
                
                # Nueva imagen
                nombre_imagen = linea.replace(":", "")
                lineas_coordenadas = []
            
            # Detectar fin de coordenadas (cuando encontramos Pivijay)
            elif "Pivijay" in linea or "Altitud" in linea or "Velocidad" in linea:
                # No acumulamos más líneas para esta imagen
                pass
            
            # Acumular líneas que podrían contener coordenadas
            elif nombre_imagen and (linea.startswith("N") or linea.startswith("W") or "N " in linea or "W " in linea):
                lineas_coordenadas.append(linea)
            
            # Detectar fin de bloque
            elif "-" * 10 in linea:
                # Procesar imagen si existe
                if nombre_imagen and lineas_coordenadas:
                    texto_coordenadas = " ".join(lineas_coordenadas)
                    coordenada = normalizar_coordenada(texto_coordenadas)
                    f_out.write(f"{nombre_imagen}:\n{coordenada}\n{'-'*60}\n")
                    lineas_coordenadas = []
        
        # Procesar la última imagen si queda pendiente
        if nombre_imagen and lineas_coordenadas:
            texto_coordenadas = " ".join(lineas_coordenadas)
            coordenada = normalizar_coordenada(texto_coordenadas)
            f_out.write(f"{nombre_imagen}:\n{coordenada}\n{'-'*60}\n")

if __name__ == "__main__":
    procesar_archivo()
    print("Procesamiento completado. Las coordenadas han sido guardadas en 'coordenadas_formato_estandar.txt'")