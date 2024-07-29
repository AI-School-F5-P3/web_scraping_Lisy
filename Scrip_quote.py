import mysql.connector
from mysql.connector import Error
from colorama import Fore, init
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime

# Inicializar colorama
init(autoreset=True)

# Cargar variables de entorno desde un archivo .env
load_dotenv()

#Define una función log_to_database para registrar logs en la base de datos
def log_to_database(connection, level, message):
    try:
        cursor = connection.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT IGNORE INTO logs (timestamp, level, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (timestamp, level, message))
        connection.commit()
    except Error as e:
        print(f"Error al registrar log en la base de datos: {e}")
    finally:
        cursor.close()

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
#Define la función insert_quotes para extraer y almacenar citas
def insert_quotes():
    connection = create_connection()
    if not connection:
        print("No se pudo establecer la conexión a la base de datos.")
        return
    
    try:
        cursor = connection.cursor()
        # Primer log: conexión a la base de datos establecida
        log_to_database(connection, 'INFO', "Conexión a la base de datos establecida.")
        base_url = " https://quotes.toscrape.com/page/"
        #Itera a través de las primeras 10 páginas del sitio web
        for page_num in range(1, 11):
            url = base_url + str(page_num) + '/'
            result = requests.get(url)
            #Hace una solicitud HTTP GET a la URL., busca todas las citas
            if result.status_code == 200:
                content = result.text
                soup = BeautifulSoup(content, 'html.parser')
                spans = soup.find_all('span', class_='text', itemprop='text')
#Si se encuentran citas, define colores para imprimir diferentes tipos de información
                if spans:
                    yellow = Fore.YELLOW    # para las frases
                    magenta = Fore.LIGHTMAGENTA_EX    # para los autores
                    green = Fore.GREEN    # para las etiquetas
                    blue = Fore.LIGHTBLUE_EX    # para los about
#Itera sobre las citas, las extrae. Encuentra el autor y extrae el about, se crea el link del about
                    for span in spans:
                        phrase = span.get_text(strip=True)
                        quote_div = span.find_parent('div', class_='quote')
                        author_name = quote_div.find('small', class_='author').get_text(strip=True)
                        about_link = quote_div.find('a', href=True)['href']
                        about_url = "https://quotes.toscrape.com" + about_link
                       

                        # Insertar o obtener el autor
                        cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
                        author = cursor.fetchone()
                        if author:
                            author_id = author[0]
                        else:
                            cursor.execute("INSERT INTO authors (name, about_url) VALUES (%s, %s)", (author_name, about_url))
                            connection.commit()
                            author_id = cursor.lastrowid
#imprime en consola la frase, el autor, el link
                        print(yellow + "Frase extraída: " + phrase)
                        print(magenta + "Autor: " + author_name)
                        print(blue + "About link: " + about_url)
                        # Registrar logs
                        log_to_database(connection, 'INFO', f"Frase extraída: {phrase}")
                        log_to_database(connection, 'INFO', f"Autor: {author_name}")
                        log_to_database(connection, 'INFO', f"About link: {about_url}")

                        # Insertar o obtener la cita
                        cursor.execute("SELECT id FROM quotes WHERE quote = %s", (phrase,))
                        quote = cursor.fetchone()
                        if quote:
                            quote_id = quote[0]
                        else:
                            cursor.execute("INSERT INTO quotes (quote, author_id) VALUES (%s, %s)", (phrase, author_id))
                            connection.commit()
                            quote_id = cursor.lastrowid

                        # Insertar etiquetas
                        tags = quote_div.find_all('a', class_='tag')
                        if tags:
                            tags_text = [tag.get_text(strip=True) for tag in tags]
                            #imprime las etiquetas en consola
                            print(green + "Tags: " + ', '.join(tags_text))
                            log_to_database(connection, 'INFO', f"Tags: {', '.join(tags_text)}")
#Inicia un bucle que itera a través de cada texto de etiqueta en la lista tag_text
                            for tag_text in tags_text:
                                cursor.execute("SELECT id FROM tags WHERE name = %s", (tag_text,))
                                tag = cursor.fetchone()
#Si la etiqueta ya existe, se obtiene el id de la etiqueta existente y se almacena en tag_id
                                if tag:
                                    tag_id = tag[0]
                                else:
                                    cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag_text,))
                                    #se confirma la transaccion
                                    connection.commit()
                                    #Obtiene el id de la etiqueta recién insertada y lo almacena en tag_id
                                    tag_id = cursor.lastrowid
                                
                                # Verificar si la combinación de quote_id y tag_id ya existe en quote_tags
                                cursor.execute("SELECT * FROM quote_tags WHERE quote_id = %s AND tag_id = %s", (quote_id, tag_id))
                                quote_tag = cursor.fetchone()
                                if not quote_tag:
                                    cursor.execute("INSERT INTO quote_tags (quote_id, tag_id) VALUES (%s, %s)", (quote_id, tag_id))
                                    connection.commit()
#Esta parte se ejecuta si no se encontraron etiquetas para la frase actual
                        else:
                            print("No se encontraron etiquetas para la frase.")
                            log_to_database(connection, 'WARNING', "No se encontraron etiquetas para la frase.")
 #Esta parte se ejecuta si no se encontraron citas en la página actual
                else:
                    print("No se encontraron citas en la página.")
                    log_to_database(connection, 'WARNING', "No se encontraron citas en la página.")
#Esta parte se ejecuta si la solicitud HTTP no fue exitosa 200
            else:
                print(f"Error al realizar la solicitud: {result.status_code}")
                log_to_database(connection, 'ERROR', f"Error al realizar la solicitud: {result.status_code}")
#Captura las excepciones relacionadas con MySQL
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        log_to_database(connection, 'ERROR', f"Error al conectar a MySQL: {e}")
#Bloque que se ejecuta siempre, ya sea que ocurra una excepción o no.
   
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            Rojo = Fore.RED
            print(Rojo + 'Conexión cerrada')
            # Registrar el cierre de conexión
            # Utiliza un nuevo cursor para registrar el log ya que el cursor principal está cerrado.
            log_connection = create_connection()  # Reabre la conexión para el log final
            if log_connection:
                log_to_database(log_connection, 'INFO', 'Conexión cerrada')
                log_connection.close()  # Cierra la conexión después de registrar el log

# Llama a la función insert_quotes
insert_quotes()
