import streamlit as st
from PIL import Image
import random
import urllib.parse
import requests
import json
from utils import call_openrouter

# --- CONFIGURATION ---
st.set_page_config(page_title="Kumis del Balcón 🐮", page_icon="🐮", layout="wide", initial_sidebar_state="expanded")

# --- SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
# Generate a stable Wompi order reference valid for this session
if 'wompi_ref' not in st.session_state:
    st.session_state.wompi_ref = f"KB-{random.randint(10000, 99999)}"

# --- HELPERS ---
def get_wompi_key():
    """Reads Wompi public key from st.secrets or falls back to test key."""
    try:
        return st.secrets.get("WOMPI_PUBLIC_KEY", "pub_test_Q5yDA9xoKdePzhSGeVe9HAez74wxobRY")
    except Exception:
        return "pub_test_Q5yDA9xoKdePzhSGeVe9HAez74wxobRY"

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Nunito:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    @media (prefers-color-scheme: dark) {
        .footer, .sevilla-section {
            background-color: rgba(255, 255, 255, 0.05) !important;
        }
    }
    
    .main-title {
        font-family: 'Fredoka', sans-serif;
        color: #2c3e50;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 600;
        margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .slogan {
        font-family: 'Fredoka', sans-serif;
        color: #e67e22;
        text-align: center;
        font-size: 1.5rem;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    
    .category-title {
        font-family: 'Fredoka', sans-serif;
        color: #d35400;
        border-bottom: 2px solid #fad390;
        padding-bottom: 5px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .stButton button {
        background-color: #27ae60;
        color: white;
        border-radius: 20px;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #219150;
        transform: scale(1.05);
    }
    
    .footer, .sevilla-section {
        background-color: rgba(0, 0, 0, 0.05);
        padding: 40px;
        margin-top: 50px;
        border-top: 3px solid #e67e22;
        border-radius: 15px;
        text-align: center;
    }

    .intro-box {
        text-align: center;
        max-width: 800px;
        margin: 0 auto;
        font-size: 1.2rem;
        background-color: #fff9c4;
        color: #4a4a4a;
        padding: 15px;
        border-radius: 10px;
    }

    @media (prefers-color-scheme: dark) {
        .footer, .sevilla-section {
            background-color: rgba(255, 255, 255, 0.05) !important;
        }
        .intro-box {
            background-color: rgba(255, 249, 196, 0.15) !important;
            color: #eee !important;
        }
    }

    /* Target specific headings within sections for better contrast */
    .sevilla-section h2, .sevilla-section h3, .footer h3 {
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA: MENU ITEMS ---
menu_categories = {
    "🐮 Lácteos y Arroz con Leche": [
        {"name": "Kumis Tradicional (16oz)", "price": 8000, "desc": "Cremoso, dulce y delicioso. El favorito.", "img": "kumis.png"},
        {"name": "Kumis Litro", "price": 18000, "desc": "Para compartir en familia.", "img": "kumis.png"},
        {"name": "Yogurt de Frutas", "price": 9000, "desc": "Mora, Melocotón o Fresa.", "img": "yogurt.png"},
        {"name": "Arroz con Leche", "price": 6500, "desc": "Con canela, pasas y queso rallado.", "img": "arroz.png"},
        {"name": "Fresas con Crema", "price": 12000, "desc": "Fresas del campo con nuestra crema especial.", "img": "fresas.png"},
    ],
    "🥐 Panadería y Tradición": [
        {"name": "Torta de Almojábana", "price": 7000, "desc": "Esponjosa torta de queso y maíz.", "img": "torta_almojabana.png"},
        {"name": "Torta de Choclo", "price": 7000, "desc": "Dulce de maíz tierno con queso.", "img": "torta_choclo.png"},
        {"name": "Pandebono Valluno", "price": 3500, "desc": "Calientito y chicludo.", "img": "pandebono.png"},
        {"name": "Buñuelo Grande", "price": 3000, "desc": "Crocante por fuera, suave por dentro.", "img": "bunuelo.png"},
        {"name": "Empanada de Cambray", "price": 4000, "desc": "Rellena de dulce de guayaba y queso.", "img": "empanada.png"},
    ],
    "🍰 Repostería y Dulces": [
        {"name": "Cheesecake de Maracuyá", "price": 9500, "desc": "Postre frío con salsa natural.", "img": "cheesecake.png"},
        {"name": "Galleta de Chip", "price": 2500, "desc": "Galleta estilo americano.", "img": "galleta.png"},
        {"name": "Torta de Zanahoria", "price": 7500, "desc": "Con frosting de queso crema.", "img": "torta_zanahoria.png"},
    ],
    "☕ Bebidas y Algo más": [
        {"name": "Café de la Casa", "price": 4000, "desc": "Tinto campesino cultivado en Sevilla.", "img": "cafe.png"},
        {"name": "Chocolate Santafereno", "price": 6000, "desc": "En leche, espumoso y con clavos.", "img": "chocolate.png"},
        {"name": "Avena Helada", "price": 5000, "desc": "Espesa y refrescante.", "img": "avena.png"},
        {"name": "Sándwich Jamón y Queso", "price": 9000, "desc": "En pan artesanal.", "img": "sandwich.png"},
    ]
}


# --- SIDEBAR (CONFIG & CART) ---
with st.sidebar:
    # --- VISUALS ---
    st.title("🐮 Menú y Pedidos")
    
    # Check for developer mode via URL query parameter (?dev=true)
    is_dev = st.query_params.get("dev", "false").lower() == "true"

    st.markdown("### 🛒 Tu Carrito")

    if st.session_state.cart:
        total = sum(item['price'] for item in st.session_state.cart)
        
        for i, item in enumerate(st.session_state.cart):
            c1, c2 = st.columns([3, 1])
            c1.markdown(f"**{item['name']}**")
            c2.markdown(f"${item['price']:,}")
        
        st.markdown("---")
        st.markdown(f"### Total: ${total:,}")
        
        if st.button("🗑️ Vaciar Carrito"):
            st.session_state.cart = []
            st.rerun()

        st.markdown("---")
        
        # --- CHECKOUT FORM ---
        st.subheader("🛍️ Finalizar Pedido")
        order_type = st.selectbox("¿Dónde recibirás tu pedido?", ["🏠 A domicilio", "🪑 Para la mesa"])
        
        with st.form("checkout_form"):
            client_name = st.text_input("Nombre Completo:")
            
            if order_type == "🏠 A domicilio":
                client_address = st.text_input("Dirección de Entrega:")
                table_info = ""
            else:
                table_info = st.text_input("Número de Mesa:")
                client_address = "Local - Mesa " + table_info
                
            client_phone = st.text_input("Teléfono / WhatsApp:")
            payment_method = st.radio("Método de Pago:", ["Nequi / Bancolombia", "Efectivo", "Wompi"])
            
            submitted = st.form_submit_button("✅ Confirmar Datos")
        
        # --- WHATSAPP MESSAGE GENERATOR ---
        check_condition = submitted and client_name and client_phone and (client_address if order_type == "🏠 A domicilio" else table_info)
        
        if check_condition:
            # Create text for message
            items_list = ""
            for item in st.session_state.cart:
                items_list += f"- {item['name']} (${item['price']:,})\n"
                
            order_details = f"*Mesa:* {table_info}" if order_type == "🪑 Para la mesa" else f"*Dirección:* {client_address}"
            
            whatsapp_msg = f"""*¡Hola Kumis del Balcón!* 🐮
Quiero hacer el siguiente pedido (*{order_type}*):

{items_list}
💰 *TOTAL: ${total:,}*

📍 *Datos del Cliente:*
*Nombre:* {client_name}
{order_details}
*Tel:* {client_phone}
*Pago:* {payment_method}
"""
            whatsapp_encoded = urllib.parse.quote(whatsapp_msg)
            whatsapp_link = f"https://wa.me/573127321920?text={whatsapp_encoded}"
            
            st.success("✅ ¡Datos listos!")
            st.markdown(f"""
            <a href="{whatsapp_link}" target="_blank">
                <button style="background-color: #25D366; color: white; border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: bold; font-size: 1.1rem; cursor: pointer;">
                    📲 Enviar Pedido por WhatsApp
                </button>
            </a>
            """, unsafe_allow_html=True)
            
            if payment_method == "Wompi":
                wompi_key = get_wompi_key()
                url_wompi = (
                    f"https://checkout.wompi.co/p/"
                    f"?public-key={wompi_key}"
                    f"&currency=COP"
                    f"&amount-in-cents={total * 100}"
                    f"&reference={st.session_state.wompi_ref}"
                )
                st.markdown("<br>", unsafe_allow_html=True)
                st.link_button(f"💳 Ir a Pagar ${total:,} con Wompi", url_wompi)
            
            # Add Nequi QR for Eat-in orders
            if order_type == "🪑 Para la mesa" and payment_method == "Nequi / Bancolombia":
                st.markdown("---")
                st.subheader("📱 Pago Rápido Nequi")
                try:
                    st.image("nequi_qr.png", caption="Escanea para pagar tu pedido en mesa")
                except:
                    st.warning("⚠️ QR de Nequi no disponible en este momento.")
                 
        elif submitted:
            warning_msg = "⚠️ Por favor completa tus datos para finalizar el pedido."
            if order_type == "🪑 Para la mesa" and not table_info:
                warning_msg = "⚠️ Por favor indica tu número de mesa."
            st.warning(warning_msg)
        
    else:
        st.info("Tu carrito está vacío. ¡Antójate de algo delicioso! 😋")

# --- AI ASSISTANT (CHATBOT) ---
st.sidebar.markdown("---")
st.sidebar.subheader("🐮 Chat con la Vaquita (IA)")
st.sidebar.caption("¡Pregúntame sobre el menú o sobre Sevilla!")


def call_openrouter_assistant(prompt):
    try:
        # Contexto del negocio para la IA - Generado dinámicamente
        menu_ctx = ""
        for cat, items in menu_categories.items():
            menu_ctx += f"\n### {cat}:\n"
            for item in items:
                menu_ctx += f"- {item['name']}: ${item['price']:,} ({item['desc']})\n"

        full_context = f"""
        Eres 'La Vaquita', la asistente virtual experta de 'Kumis del Balcón', ubicado en Sevilla, Valle del Cauca, Colombia. 🐮☕
        Tu misión es antojar, informar y enamorar a los clientes con nuestros productos y con la riqueza cultural de Sevilla.
        Responde SIEMPRE en español, de forma cálida, detallada y con personalidad campesina amable.

        ══════════════════════════════════════════
        🐮 CONOCIMIENTO PROFUNDO DE PRODUCTOS
        ══════════════════════════════════════════

        LÁCTEOS:
        - Kumis Tradicional (16oz) / Kumis Litro: Bebida láctea fermentada de forma natural durante 24-48 horas.
          Ingredientes: leche fresca de vaca, azúcar y cultivos lácticos vivos (Lactobacillus). Textura cremosa
          y espesa, sabor suavemente ácido y dulce a la vez. Es el producto estrella del local. Ideal para
          personas con digestión delicada pues sus probióticos ayudan al intestino. Contiene lactosa y azúcar.
          Maridaje perfecto: Pandebono valluno o buñuelo recién hecho.

        - Yogurt de Frutas: Elaborado con leche entera, fermentado y mezclado con pulpa natural de mora,
          melocotón o fresa según disponibilidad. Espeso, sin colorantes artificiales. Contiene lactosa y azúcar.
          Maridaje: Galleta de chip o torta de zanahoria.

        - Arroz con Leche: Receta tradicional de la abuela. Arroz de grano largo cocido lentamente en leche
          entera con canela en rama, panela/azúcar, uvas pasas y coronado con queso rallado. Es un postre
          caliente y reconfortante. Contiene lácteos y azúcar. Maridaje: Café de la casa o chocolate santafereño.

        - Fresas con Crema: Fresas frescas de campo bañadas con nuestra crema de leche especial.
          Postre frío y ligero. Contiene lácteos. Maridaje: Avena helada o café.

        PANADERÍA:
        - Torta de Almojábana: Torta típica vallecaucana hecha con harina de maíz, queso blanco costeño y
          huevo. Textura esponjosa, levemente salada. Contiene lácteos y huevo. Maridaje: Café tinto o chocolate caliente.

        - Torta de Choclo: Elaborada con maíz tierno (choclo) molido, queso cuajada fresco, huevo y un toque
          de azúcar. Sabor a maíz fresco muy característico. Contiene lácteos y huevo. Maridaje: Kumis frío o café.

        - Pandebono Valluno: Ícono de la gastronomía vallecaucana. Hecho con almidón de yuca agria, queso
          costeño rallado, huevo y poca sal. Crocante por fuera y chicloso por dentro. Sin gluten (es de yuca).
          Contiene lácteos y huevo. Maridaje ideal: Kumis o chocolate santafereño.

        - Buñuelo Grande: Masa de queso blanco y maicena, frita en aceite caliente. Crocante por fuera,
          hueco y suave por dentro. Sin gluten. Contiene lácteos. Maridaje: Café tinto o chocolate.

        - Empanada de Cambray: Masa de maíz artesanal rellena de dulce de guayaba casero y queso blanco.
          Combinación dulce-salada muy típica del Valle. Contiene lácteos. Maridaje: Café o avena helada.

        REPOSTERÍA:
        - Cheesecake de Maracuyá: Postre frío con base de galleta, relleno cremoso de queso crema y salsa
          natural de maracuyá. Dulce con toque ácido tropical. Contiene gluten y lácteos.
          Maridaje: Café o avena helada.

        - Galleta de Chip: Galleta horneada estilo americano con chips de chocolate. Contiene gluten, lácteos
          y huevo. Maridaje: Yogurt o kumis.

        - Torta de Zanahoria: Bizcocho húmedo de zanahoria con especias (canela, clavo), coronado con
          frosting de queso crema. Contiene gluten, lácteos y huevo. Maridaje: Café de la casa.

        BEBIDAS:
        - Café de la Casa: Tinto campesino con granos cultivados en las montañas de Sevilla. Tostado medio,
          notas a chocolate y caramelo. Sin lácteos, sin gluten. Maridaje: Cualquier producto del menú.

        - Chocolate Santafereño: Chocolate de mesa en leche entera caliente, batido hasta producir espuma
          gruesa. Se sirve con clavos de olor. Con lácteos. Maridaje: Pandebono, almojábana o buñuelo.

        - Avena Helada: Bebida fría de avena, leche, canela y azúcar. Espesa y refrescante.
          Contiene gluten y lácteos. Maridaje: Empanada o fresas.

        - Sándwich Jamón y Queso: Pan artesanal con jamón cocido y queso derretido. Contiene gluten y lácteos.
          Maridaje: Café o avena.

        MENÚ COMPLETO Y PRECIOS:
        {menu_ctx}

        ══════════════════════════════════════════
        🌄 HISTORIA Y CULTURA DE SEVILLA, VALLE DEL CAUCA
        ══════════════════════════════════════════

        HISTORIA:
        - Sevilla fue fundada el 28 de octubre de 1903 por colonizadores antioqueños (paisas) que llegaron
          al norte del Valle del Cauca buscando tierras fértiles para café.
        - Su nombre fue inspirado en la ciudad española de Sevilla por la hermosura de sus paisajes.
        - Declarada municipio oficial en 1907. Es conocida como la 'Capital Cafetera de Colombia' y como
          la 'Ciudad de los Balcones' por sus coloridos balcones floridos, herencia de la arquitectura paisa.
        - Durante el siglo XX fue clave en el desarrollo agrícola del Valle, con cultivos de café, caña,
          plátano y frutales.

        GEOGRAFÍA:
        - Ubicada al norte del Valle del Cauca, a ~1.550 metros sobre el nivel del mar.
        - Clima templado agradable: entre 18°C y 24°C todo el año.
        - Rodeada de la cordillera central de los Andes, con paisajes cafeteros espectaculares.
        - A unas 3 horas de Cali y cerca de Cartago y Caicedonia.
        - Forma parte del 'Paisaje Cultural Cafetero de Colombia', declarado Patrimonio de la Humanidad
          por la UNESCO en 2011.

        CULTURA Y TRADICIONES:
        - Festival Nacional de la Bandola (agosto): El festival de bandola más importante de Colombia.
          Reúne músicos de todo el país que tocan música tradicional andina (bambuco, pasillo, torbellino).
          La bandola es un instrumento de cuerda típico de la zona andina, similar al laúd.
        - Basílica San Luis Gonzaga: Iglesia principal en el parque central, joya de arquitectura
          neogótica-republicana y símbolo del municipio.
        - Gastronomía local: kumis, pandebono, empanadas, buñuelos, arroz con leche, sancocho de gallina,
          tamales y en cada esquina: café de origen.
        - La gente sevillana es famosa por ser amable, hospitalaria y muy orgullosa de sus raíces.

        TURISMO:
        - Parque Principal: Corazón del municipio, rodeado de la Basílica y coloridos balcones.
        - Mirador El Morro: Vista panorámica espectacular de Sevilla y sus montañas.
        - Fincas cafeteras: Tours del café para conocer el proceso desde la mata hasta la taza.
        - Kumis del Balcón está ubicado frente al parque principal, en el corazón turístico del municipio.

        ══════════════════════════════════════════
        🐮 PERSONALIDAD DE LA VAQUITA
        ══════════════════════════════════════════
        - Eres una campesina sevillana amable, sabia y muy orgullosa de su tierra.
        - Usas emojis con moderación: 🐮 🥛 🌽 🧀 ☕ 🌄 🎸 🌺
        - Tratas al cliente de: "Vecino/a", "Corazón", "Mijo/a", "Paisano/a".
        - Usas expresiones colombianas naturales y espontáneas: "¡De una!", "¿Listo pues?", "¡Qué rico!".
        - Tus respuestas son cálidas, nunca frías ni robóticas.
        - Si alguien pregunta algo fuera de tu conocimiento, reconoces que no sabes y ofreces el teléfono: 📞 310 123 4567.

        ══════════════════════════════════════════
        📋 REGLAS DE RESPUESTA
        ══════════════════════════════════════════
        1. MENÚ: Responde sobre productos, ingredientes, precios, tamaños y preparación con detalle.
        2. MARIDAJES: SIEMPRE sugiere una combinación de productos al final de tu respuesta.
        3. DIETA: Para preguntas sobre gluten, lactosa, vegetariano o azúcar, usa la info real de los ingredientes.
        4. HISTORIA/TURISMO: Responde con detalle y orgullo sobre Sevilla, su historia, cultura y turismo.
        5. ORTOGRAFÍA: Entiende preguntas mal escritas (cumis, pan de bono, buñelo, almojabana). NUNCA corrijas.
        6. PEDIDOS: Si alguien quiere pedir, indícale que use el carrito de la izquierda 🛒 y el botón de WhatsApp.
        7. FUERA DE TEMA: Si la pregunta no tiene NADA que ver con el menú, Sevilla o gastronomía colombiana,
           dilo amablemente y redirige la conversación.
        8. LONGITUD: Sé completa y útil, pero concisa. Máximo 3-4 párrafos cortos por respuesta.
        """
        
        # Pass the history from session state
        return call_openrouter(prompt, system_context=full_context, messages=st.session_state.messages)
    except Exception as e:
        return f"Lo siento, amiguito, mi ubre se enredó (Error: {str(e)[:50]}). 🐮"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.sidebar.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.sidebar.chat_input("¿Qué me recomiendas?"):
    st.sidebar.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.sidebar.chat_message("assistant"):
        response = call_openrouter_assistant(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.sidebar.button("Borrar Chat", key="clear_chat"):
    st.session_state.messages = []
    st.rerun()

st.write("---")


# --- HEADER SECTION ---
col_logo, col_title = st.columns([1, 3])

with col_title:
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">Kumis del Balcón</h1>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">🐮 ¡El sabor de nuestra tierra! 🇨🇴</p>', unsafe_allow_html=True)

with col_logo:
    try:
        st.image("logo.png", width=220)
    except:
        st.markdown("# 🐮")

# --- INTRO ---
st.markdown("""
<div class="intro-box">
    Disfruta de la mejor tradición sevillana. Nuestros productos son 100% artesanales, 
    hechos con amor y los mejores ingredientes del <b>Valle del Cauca</b>.
</div>
<br>
""", unsafe_allow_html=True)

# --- RENDER MENU ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>Nuestra Carta</h2>", unsafe_allow_html=True)

tabs = st.tabs(menu_categories.keys())

for tab, (category, items) in zip(tabs, menu_categories.items()):
    with tab:
        st.markdown(f"<h3 class='category-title'>{category}</h3>", unsafe_allow_html=True)
        
        # Grid layout for items
        cols = st.columns(3)
        for i, item in enumerate(items):
            col = cols[i % 3]
            with col:
                with st.container(border=True):
                    # Image handling
                    if item["img"]:
                        try:
                            # Use Image.open to handle local files safely
                            st.image(item["img"], use_container_width=True)
                        except:
                            st.markdown(f"<div style='height: 150px; background: #eee; display: flex; align-items: center; justify-content: center; font-size: 3rem;'>🍽️</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='height: 150px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; font-size: 4rem;'>🍽️</div>", unsafe_allow_html=True)
                    
                    st.markdown(f"#### {item['name']}")
                    st.markdown(f"_{item['desc']}_")
                    st.markdown(f"**${item['price']:,}**")
                    
                    if st.button(f"Agregar al Carrito", key=f"btn_{category}_{i}"):
                        st.session_state.cart.append(item)
                        st.toast(f"✅ ¡{item['name']} agregado!")
                        st.rerun()

st.write("")
st.write("---")

# --- SEVILLA SECTION ---
st.markdown("<div class='sevilla-section'>", unsafe_allow_html=True)
st.markdown("<h2>🌄 Visita Sevilla, Valle del Cauca</h2>", unsafe_allow_html=True)
st.markdown("<h3>'Capital Cafetera de Colombia'</h3>", unsafe_allow_html=True)
st.write("Ven a conocer nuestro hermoso municipio, famoso por sus balcones, su gente amable y el mejor café del mundo.")

c1, c2, c3 = st.columns(3)
with c1:
    try:
        st.image("sevilla_plaza.png", use_container_width=True)
    except:
        st.write("📷")
    st.markdown("🏰 **Basílica San Luis Gonzaga**")
    st.write("Una joya arquitectónica en el corazón del parque principal.")
with c2:
    try:
        st.image("sevilla_paisaje.png", use_container_width=True)
    except:
        st.write("📷")
    st.markdown("☕ **Paisaje Cultural Cafetero**")
    st.write("Patrimonio de la humanidad. Vistas inigualables.")
with c3:
    try:
        st.image("logo.png", use_container_width=True) # Reuse logo or another img
    except:
        st.write("📷")
    st.markdown("🎉 **Festival de la Bandola**")
    st.write("Música, cultura y tradición cada agosto.")

st.info("¡Te esperamos en nuestro local frente al parque principal para que pruebes el verdadero Kumis!")
st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <h3>📍 Kumis del Balcón</h3>
    <p>Carrera 50 # 25-10, Sevilla, Valle del Cauca.</p>
    <p>📞 Domicilios y Reservas: 310 123 4567</p>
    <br>
    <div style="font-size: 1.5rem;">
        <a href="#" style="text-decoration: none;">📷</a> &nbsp;
        <a href="#" style="text-decoration: none;">📘</a> &nbsp;
        <a href="#" style="text-decoration: none;">💬</a>
    </div>
    <br>
    <small>© 2026 Kumis del Balcón. Hecho con ❤️ en Colombia.</small>
</div>
""", unsafe_allow_html=True)



