#se importan las librerias a usar
import re
from colorama import Fore
import requests
#import beautifulsoup4
import os
from dotenv import load_dotenv
# Cargar variables de entorno desde un archivo .env
load_dotenv()

#se crea la variable que contiene el valor de la URL a usar en el web scripting
website = os.getenv(url)
result = requests.get(website)
content = result.text
#esto visualiza los datos de la peticiòn HTTP
print(content) 
#obtener el nombre de cada maquina despues del entry, lo busque al inspeccionar la pagina y lo guarda en la variable patron
