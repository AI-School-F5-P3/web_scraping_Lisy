#se importan las librerias a usar
import re
from colorama import Fore
import requests
import os
from dotenv import load_dotenv
# Cargar variables de entorno desde un archivo .env
load_dotenv()   

#se crea la variable que contiene el valor de la URL a usar en el web scripting
website = os.getenv('url')
#print(website)
if website:
    result = requests.get(website)

    if result.status_code == 200:
        content = result.text
#esto visualiza los datos de la peticiòn HTTP
#print(content) 
#obtener frase
        pattern = r'<span class="text" itemprop="text">(.*?)</span>'
        matches = re.findall(pattern,content, re.DOTALL)
        
        if matches:
            for phrase in matches:
                print("Frase extraída:", phrase.strip())
        else:
            print("No se encontraron citas en la página.")
    else:
        print("Error al realizar la solicitud:", result.status_code)
else:
    print("La variable de entorno 'url' no está definida.")