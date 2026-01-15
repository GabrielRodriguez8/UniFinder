# UniFinder
Página Web con IA integrada con Gen AI. UniFinder buscador de universidades en España. https://gabigoleador8.pythonanywhere.com
# 🎓 Recomendador de Grados Universitarios con IA

Una aplicación web inteligente que ayuda a futuros estudiantes a encontrar su carrera ideal. Utiliza la potencia de **Google Gemini AI** para analizar los intereses del usuario y recomendar grados universitarios, localizados por ciudad y filtrados por preferencias.

## 🚀 Características

-   **Búsqueda Inteligente:** El usuario describe sus intereses en lenguaje natural.
-   **Geolocalización:** Filtrado de universidades por ciudad o zona.
-   **Generación de Tarjetas:** Resultados visuales con información clave (Nota de corte, Universidad, Motivos).
-   **Planes de Estudio:** Visualización rápida de asignaturas principales.
-   **Motor AI:** Backend potenciado por `gemini-1.0-pro` (Google Generative AI).

## 🛠️ Tecnologías Utilizadas

-   **Backend:** Python 3, Flask.
-   **IA:** Google Gemini API (google-generativeai).
-   **Frontend:** HTML5, CSS3 (Diseño responsivo), JavaScript (Fetch API).
-   **Despliegue:** Compatible con PythonAnywhere.

## 📦 Instalación y Uso Local

Sigue estos pasos para probar el proyecto en tu máquina:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
    cd TU_REPOSITORIO
    ```

2.  **Crear un entorno virtual (Opcional pero recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la API Key:**
    - Abre el archivo `app.py`.
    - Busca la variable `MI_API_KEY`.
    - Pega tu propia API Key de Google AI Studio.
    *(Puedes conseguir una gratis en [Google AI Studio](https://aistudio.google.com/))*

5.  **Ejecutar la aplicación:**
    ```bash
    python app.py
    ```

6.  **Abrir en el navegador:**
    Ve a `http://127.0.0.1:5000`

## 📂 Estructura del Proyecto

```text
├── static/          # Archivos CSS, imágenes y JS estáticos
├── templates/       # Plantillas HTML (index.html)
├── app.py           # Lógica del servidor Flask y conexión con Gemini
├── requirements.txt # Lista de dependencias
└── README.md        # Documentación
