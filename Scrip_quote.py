import mysql.connector
from mysql.connector import Error
from colorama import Fore, init
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from log import log_to_database, create_log_connection
from datetime import datetime

# Inicializar colorama
init(autoreset=True)

# Cargar variables de entorno desde un archivo .env
load_dotenv()

def create_connection():
    """Crea y retorna una conexión a la base de datos."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database='spider',  # Base de datos 'spider'
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def insert_quotes():
    connection = create_connection()
    if not connection:
        print("No se pudo establecer la conexión a la base de datos.")
        log_to_database('ERROR', "No se pudo establecer la conexión a la base de datos.")
        return
    
    try:
        cursor = connection.cursor()
        log_to_database('INFO', "Conexión a la base de datos establecida.")
        base_url = " https://quotes.toscrape.com/page/"
        for page_num in range(1, 11):
            url = base_url + str(page_num) + '/'
            result = requests.get(url)
            if result.status_code == 200:
                content = result.text
                soup = BeautifulSoup(content, 'html.parser')
                spans = soup.find_all('span', class_='text', itemprop='text')
                if spans:
                    yellow = Fore.YELLOW
                    magenta = Fore.LIGHTMAGENTA_EX
                    green = Fore.GREEN
                    blue = Fore.LIGHTBLUE_EX
                    for span in spans:
                        phrase = span.get_text(strip=True)
                        quote_div = span.find_parent('div', class_='quote')
                        author_name = quote_div.find('small', class_='author').get_text(strip=True)
                        about_link = quote_div.find('a', href=True)['href']
                        about_url = "https://quotes.toscrape.com" + about_link

                        cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
                        author = cursor.fetchone()
                        if author:
                            author_id = author[0]
                        else:
                            cursor.execute("INSERT INTO authors (name, about_url) VALUES (%s, %s)", (author_name, about_url))
                            connection.commit()
                            author_id = cursor.lastrowid

                        print(yellow + "Frase extraída: " + phrase)
                        print(magenta + "Autor: " + author_name)
                        print(blue + "About link: " + about_url)
                        log_to_database('INFO', f"Frase extraída: {phrase}")
                        log_to_database('INFO', f"Autor: {author_name}")
                        log_to_database('INFO', f"About link: {about_url}")

                        cursor.execute("SELECT id FROM quotes WHERE quote = %s", (phrase,))
                        quote = cursor.fetchone()
                        if quote:
                            quote_id = quote[0]
                        else:
                            cursor.execute("INSERT INTO quotes (quote, author_id) VALUES (%s, %s)", (phrase, author_id))
                            connection.commit()
                            quote_id = cursor.lastrowid

                        tags = quote_div.find_all('a', class_='tag')
                        if tags:
                            tags_text = [tag.get_text(strip=True) for tag in tags]
                            print(green + "Tags: " + ', '.join(tags_text))
                            log_to_database('INFO', f"Tags: {', '.join(tags_text)}")
                            for tag_text in tags_text:
                                cursor.execute("SELECT id FROM tags WHERE name = %s", (tag_text,))
                                tag = cursor.fetchone()
                                if tag:
                                    tag_id = tag[0]
                                else:
                                    cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag_text,))
                                    connection.commit()
                                    tag_id = cursor.lastrowid
                                cursor.execute("SELECT * FROM quote_tags WHERE quote_id = %s AND tag_id = %s", (quote_id, tag_id))
                                quote_tag = cursor.fetchone()
                                if not quote_tag:
                                    cursor.execute("INSERT INTO quote_tags (quote_id, tag_id) VALUES (%s, %s)", (quote_id, tag_id))
                                    connection.commit()
                        else:
                            print("No se encontraron etiquetas para la frase.")
                            log_to_database('WARNING', "No se encontraron etiquetas para la frase.")
                else:
                    print("No se encontraron citas en la página.")
                    log_to_database('WARNING', "No se encontraron citas en la página.")
            else:
                print(f"Error al realizar la solicitud: {result.status_code}")
                log_to_database('ERROR', f"Error al realizar la solicitud: {result.status_code}")

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        log_to_database('ERROR', f"Error al conectar a MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            Rojo = Fore.RED
            print(Rojo + 'Conexión cerrada')
            log_connection = create_log_connection()
            if log_connection:
                log_to_database('INFO', 'Conexión cerrada')
                log_connection.close()

# Llama a la función insert_quotes
insert_quotes()
