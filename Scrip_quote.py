from colorama import Fore 
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Se crea la variable que contiene el valor de la URL a usar en el web scraping
website = os.getenv('url')

#A partir de un condicional se hacen las peticiones a la website
if website:
    result = requests.get(website)
    if result.status_code == 200:
        content = result.text
        soup = BeautifulSoup(content, 'html.parser')
        spans = soup.find_all('span', class_='text', itemprop='text')

        if spans:
            yellow = Fore. YELLOW
            for span in spans:
                phrase = span.get_text(strip=True)
                print(yellow + "Frase extraída: ", phrase)
        else:
            print("No se encontraron citas en la página.")
    else:
        print("Error al realizar la solicitud:", result.status_code)
else:
    print("La variable de entorno 'url' no está definida.")
