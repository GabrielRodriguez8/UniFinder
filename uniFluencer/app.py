from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import json
import traceback

app = Flask(__name__, template_folder='templates')
CORS(app)

# --- TU API KEY ---
MI_API_KEY = "TU_CLAVE_API_AQUI"
genai.configure(api_key=MI_API_KEY)

# Configuración del modelo
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
except:
    model = genai.GenerativeModel('gemini-2.0-flash-001')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recomendar', methods=['POST'])
def recomendar():
    print("-------------------------------------------------")
    print(">>> NUEVA PETICIÓN RECIBIDA")
    
    try:
        data = request.json
        interes = data.get('interes')
        ciudad = data.get('ciudad')
        solo_publicas = data.get('solo_publicas', False)
        nota_raw = data.get('nota_usuario', None)
        
        print(f"Buscando: {interes} en {ciudad}. Nota: {nota_raw}")

        # --- CONSTRUCCIÓN DE FILTROS ---
        instrucciones_filtro = ""
        
        if solo_publicas:
            instrucciones_filtro += "- FILTRO ESTRICTO: Solo Universidades PÚBLICAS. Ignora privadas.\n"
        
        nota_usuario = None
        if nota_raw:
            try:
                nota_usuario = float(str(nota_raw).replace(',', '.'))
                instrucciones_filtro += f"""
                - FILTRO DE NOTA: El usuario tiene un {nota_usuario}.
                  Muestra carreras cuya nota de corte sea inferior o cercana a {nota_usuario}.
                  Si la nota de corte es mucho más alta (ej: usuario 8, corte 12), NO la incluyas.
                """
            except:
                pass

        # --- PROMPT MEJORADO ---
        prompt = f"""
        Actúa como un buscador universitario preciso en España.
        Búsqueda: Grado relacionado con "{interes}" en la zona de "{ciudad}".
        
        INSTRUCCIONES DE FILTRADO Y CANTIDAD:
        1. Analiza cuántas universidades cumplen REALMENTE los requisitos de "{instrucciones_filtro}".
        2. Genera 6 tarjetas. Dependiendo de las opciones viables:
           - Si  hay menos de 6 opciones viables, genera las que haya disponibles.
           - Si hay 10 opciones, selecciona las 6 mejores (las más prestigiosas o con mejor nota).
           - Si no hay ninguna opción viable, deja "html_tarjetas" vacío.
        
        INSTRUCCIONES DE URL (WEB):
        - Para cada universidad, busca su URL OFICIAL REAL (ej: 'https://www.ucm.es' o la web de la facultad).
        - Inserta esa URL en el href del botón 'Web'.

        IMPORTANTE FORMATO JSON:
        Responde ÚNICAMENTE con JSON válido.
        Usa COMILLAS SIMPLES (') dentro del HTML para atributos (class='btn', href='url') para no romper el JSON.
        
        Estructura JSON:
        {{
            "consejo": "Consejo personalizado sobre la nota o la ciudad (máx 30 palabras).",
            "html_tarjetas": "Código HTML de las tarjetas resultantes (puede ser 1, 2, ... hasta 6) dependiendo dee las universidades que hayan disponibles con los filtros seleccionados.",
            "carreras_similares": ["Alternativa 1", "Alternativa 2", "Alternativa 3"]
        }}

        --- PLANTILLA HTML EXACTA (Rellena los datos entre corchetes) ---
        <div class='uni-card'>
            <div class='card-header'>
                <h3>[NOMBRE UNIVERSIDAD]</h3>
                <span class='badge'>[CIUDAD]</span>
            </div>
            <div class='card-body'>
                <div class='datos-clave'>
                    <span class='nota-corte'><i class='fas fa-star'></i> Corte: [NOTA_CORTE_APROX]</span>
                </div>
                <p><strong>Grado:</strong> [NOMBRE GRADO]</p>
                <p class='motivo'>[MOTIVO BREVE]</p>
                
                <div class='acciones'>
                    <button class='btn-plan' onclick="verPlan('[NOMBRE UNIVERSIDAD]', '[NOMBRE GRADO]', '[5 ASIGNATURAS PRINCIPALES SEPARADAS POR COMAS]')">
                        <i class='fas fa-list-ul'></i> Ver Plan
                    </button>
                    
                    <a href='[INSERTA_AQUI_LA_URL_OFICIAL_REAL]' target='_blank' class='btn-visitar'>
                        Web <i class='fas fa-external-link-alt'></i>
                    </a>
                </div>
            </div>
        </div>
        """

        generation_config = {"response_mime_type": "application/json"}
        
        response = model.generate_content(prompt, generation_config=generation_config)
        
        texto_limpio = response.text.replace("```json", "").replace("```", "").strip()
        datos = json.loads(texto_limpio)
        
        return jsonify(datos)

    except Exception as e:
        print("!!! ERROR TÉCNICO:")
        traceback.print_exc()
        return jsonify({
            "consejo": "Error al conectar con el servidor. Intenta de nuevo.",
            "html_tarjetas": "",
            "carreras_similares": []
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)