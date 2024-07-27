# Quotes Scraper 📝🔍

Este proyecto es un script de Python que realiza web scraping en el sitio web [Quotes to Scrape](https://quotes.toscrape.com/) y almacena las citas, autores y etiquetas en una base de datos MySQL. 🚀

## Tabla de Contenidos 📑

- [Instalación](#instalación)
- [Uso](#uso)
- [Contribución](#contribución)


## Instalación 🛠️

1. **Clona el repositorio:**
    ```sh
    git clone https://github.com/AI-School-F5-P3/web_scraping_Lisy.git
    cd quotes-scraper
    ```

2. **Configura tu entorno virtual:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. **Instala las dependencias:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Crea un archivo `.env` y añade las siguientes variables de entorno:**
    ```sh
    DB_HOST=tu_host
    DB_NAME=spider
    DB_USER=tu_usuario
    DB_PASSWORD=tu_contraseña
    ```

## Uso 🚀

1. **Asegúrate de que tu servidor MySQL esté en funcionamiento.**

2. **Ejecuta el script de creación de la base de datos:**
    ```sh
    mysql -u tu_usuario -p < create_database.sql
    ```

3. **Ejecuta el script de scraping:**
    ```sh
    python scrip_quote.py
    ```


## Contribución 🤝

¡Las contribuciones son bienvenidas! Por favor, sigue los pasos a continuación para contribuir:

1. Haz un fork del proyecto.
2. Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
3. Haz commit de tus cambios (git commit -am 'Añadir nueva funcionalidad').
4. Haz push a la rama (git push origin feature/nueva-funcionalidad).
5. Abre un Pull Request.
