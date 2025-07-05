import re

def crear_kml_desde_coordenadas(archivo_entrada, archivo_salida):
    """
    Convierte un archivo de coordenadas a formato KML para visualización en Google Earth/Maps.
    """
    # Encabezado del archivo KML
    kml_header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>Coordenadas Extraídas</name>
  <description>Puntos de coordenadas extraídos de imágenes</description>
  <Style id="pointStyle">
    <IconStyle>
      <Icon>
        <href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href>
      </Icon>
      <scale>1.0</scale>
    </IconStyle>
  </Style>
"""
    
    # Pie del archivo KML
    kml_footer = """</Document>
</kml>"""
    
    # Abrir archivos de entrada y salida
    with open(archivo_entrada, 'r', encoding='utf-8') as f_in, open(archivo_salida, 'w', encoding='utf-8') as f_out:
        # Escribir encabezado KML
        f_out.write(kml_header)
        
        nombre_imagen = ""
        
        for linea in f_in:
            linea = linea.strip()
            
            # Extraer nombre de imagen
            if linea.endswith('.jpeg:') or linea.endswith('.jpg:') or linea.endswith('.png:'):
                nombre_imagen = linea.replace(':', '')
                continue
            
            # Extraer coordenadas
            if re.search(r'\d+\.\d+[NnSs]\s+\d+\.\d+[WwEe]', linea):
                # Extraer latitud y longitud
                match = re.search(r'(\d+\.\d+)[NnSs]\s+(\d+\.\d+)[WwEe]', linea)
                if match:
                    lat = float(match.group(1))
                    lon = float(match.group(2))
                    
                    # Ajustar signo para direcciones S y W
                    if 'S' in linea or 's' in linea:
                        lat = -lat
                    if 'W' in linea or 'w' in linea:
                        lon = -lon
                    
                    # Crear Placemark KML
                    placemark = f"""  <Placemark>
    <name>{nombre_imagen}</name>
    <styleUrl>#pointStyle</styleUrl>
    <Point>
      <coordinates>{lon},{lat},0</coordinates>
    </Point>
  </Placemark>
"""
                    f_out.write(placemark)
            
            # Ignorar líneas de separación
            if linea.startswith('-'):
                continue
        
        # Escribir pie de KML
        f_out.write(kml_footer)

if __name__ == "__main__":
    archivo_entrada = "coordenadas_extraidas.txt"
    archivo_salida = "coordenadas_mapa.kml"
    
    crear_kml_desde_coordenadas(archivo_entrada, archivo_salida)
    print(f"Archivo KML creado correctamente: {archivo_salida}")