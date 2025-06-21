## Proyecto de Extracción de Coordenadas desde Imágenes

Este proyecto extrae coordenadas geográficas desde capturas de pantalla de WhatsApp o cualquier imagen que contenga información de geolocalización en formato texto. Utiliza OCR (Reconocimiento Óptico de Caracteres) para extraer el texto de las imágenes y luego procesa ese texto para identificar y formatear las coordenadas en un formato estándar.

## Contenido del Proyecto

- extraer_coordenadas.py: Script que utiliza EasyOCR para extraer texto de imágenes
- formatear_texto_ocr.py: Script que procesa el texto extraído para obtener coordenadas con formato estándar
- textos_easyocr.txt: Archivo que almacena el texto extraído de las imágenes
- coordenadas_formateadas.txt: Archivo que almacena las coordenadas ya formateadas
- imagenes: Carpeta que contiene las imágenes de origen

## Requisitos

Para ejecutar este proyecto necesitas:

```
python 3.6+
easyocr
re (incluido en Python)
```

Para instalar EasyOCR:

```bash
pip install easyocr
```

## Cómo Funciona

### 1. Extracción de Texto

El script extraer_coordenadas.py procesa todas las imágenes en la carpeta imagenes y extrae el texto utilizando EasyOCR. El texto extraído se guarda en textos_easyocr.txt.

### 2. Formateo de Coordenadas

El script formatear_texto_ocr.py analiza el texto extraído y utiliza expresiones regulares para:
- Identificar patrones de coordenadas geográficas
- Manejar diferentes formatos y errores típicos del OCR
- Convertir las coordenadas al formato estándar: `XX°XX'XX.XXXXX"N XX°XX'XX.XXXXX"W`

## Uso

1. Coloca las imágenes con coordenadas en la carpeta imagenes
2. Ejecuta el extractor de texto:
   ```bash
   python extraer_coordenadas.py
   ```
3. Ejecuta el formateador de coordenadas:
   ```bash
   python formatear_texto_ocr.py
   ```
4. Las coordenadas formateadas estarán disponibles en coordenadas_formateadas.txt

## Ejemplo de Salida

Para una imagen que contiene el texto OCR:
```
10079'59,47799"N.74926'38,0724"W +3,79m
```

La salida formateada será:
```
10°19'59.47799"N 74°26'38.0724"W
```

## Características

- **Robustez**: Maneja diferentes formatos y errores comunes de OCR
- **Patrones especiales**: Incluye casos específicos para manejar diferentes estilos de formato en el texto extraído
- **Normalización**: Convierte automáticamente todas las coordenadas a un formato estándar
- **Procesamiento por lotes**: Procesa múltiples imágenes en una sola ejecución

## Limitaciones

- El OCR puede tener problemas con imágenes de baja calidad o con texto poco claro
- Algunas coordenadas con formatos muy inusuales podrían no ser detectadas correctamente

## Consideraciones para Mejorar

- Agregar soporte para más formatos de coordenadas
- Implementar validación geográfica para coordenadas
- Crear una interfaz gráfica para facilitar el uso

---

Desarrollado para procesamiento automático de coordenadas desde imágenes de WhatsApp.
