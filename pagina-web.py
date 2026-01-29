import streamlit as st
from PIL import Image
import random
import urllib.parse
import requests
import json

# --- CONFIGURATION ---
st.set_page_config(page_title="Kumis del Balcón 🐮", page_icon="🐮", layout="wide")

# --- SESSION STATE (CART) ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

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


# --- SIDEBAR CART ---
st.sidebar.title("🛒 Tu Carrito")
if st.session_state.cart:
    total = sum(item['price'] for item in st.session_state.cart)
    
    for i, item in enumerate(st.session_state.cart):
        c1, c2 = st.sidebar.columns([3, 1])
        c1.markdown(f"**{item['name']}**")
        c2.markdown(f"${item['price']:,}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### Total: ${total:,}")
    
    if st.sidebar.button("🗑️ Vaciar Carrito"):
        st.session_state.cart = []
        st.rerun()

    st.sidebar.markdown("---")
    
    st.sidebar.markdown("---")
    
    # --- CHECKOUT FORM ---
    st.sidebar.subheader("� Finalizar Pedido")
    order_type = st.sidebar.selectbox("¿Dónde recibirás tu pedido?", ["🏠 A domicilio", "🪑 Para la mesa"])
    
    with st.sidebar.form("checkout_form"):
        client_name = st.text_input("Nombre Completo:")
        
        if order_type == "🏠 A domicilio":
            client_address = st.text_input("Dirección de Entrega:")
            table_info = ""
        else:
            table_info = st.text_input("Número de Mesa:")
            client_address = "Local - Mesa " + table_info
            
        client_phone = st.text_input("Teléfono / WhatsApp:")
        payment_method = st.radio("Método de Pago:", ["Nequi / Bancolombia", "Efectivo", "Wompi"])
        
        submitted = st.form_submit_button("Calculadora de Pedido")
    
    # --- WHATSAPP MESSAGE GENERATOR ---
    check_condition = client_name and client_phone and (client_address if order_type == "🏠 A domicilio" else table_info)
    
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
        
        st.sidebar.success("✅ ¡Datos listos!")
        st.sidebar.markdown(f"""
        <a href="{whatsapp_link}" target="_blank">
            <button style="background-color: #25D366; color: white; border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: bold; font-size: 1.1rem; cursor: pointer;">
                📲 Enviar Pedido por WhatsApp
            </button>
        </a>
        """, unsafe_allow_html=True)
        
        if payment_method == "Wompi":
             url_wompi = f"https://checkout.wompi.co/p/?public-key=pub_test_Q5yDA9xoKdePzhSGeVe9HAez74wxobRY&currency=COP&amount-in-cents={total*100}&reference=KB-{random.randint(10000,99999)}"
             st.sidebar.markdown(f"<br>", unsafe_allow_html=True)
             st.sidebar.link_button(f"💳 Ir a Pagar ${total:,} con Wompi", url_wompi)
        
        # Add Nequi QR for Eat-in orders
        if order_type == "🪑 Para la mesa" and payment_method == "Nequi / Bancolombia":
            st.sidebar.markdown("---")
            st.sidebar.subheader("📱 Pago Rápido Nequi")
            try:
                st.sidebar.image("nequi_qr.png", caption="Escanea para pagar tu pedido en mesa")
            except:
                st.sidebar.warning("⚠️ QR de Nequi no disponible en este momento.")
             
    else:
        warning_msg = "⚠️ Por favor completa tus datos para finalizar el pedido."
        if order_type == "🪑 Para la mesa" and not table_info:
            warning_msg = "⚠️ Por favor indica tu número de mesa."
        st.sidebar.warning(warning_msg)
    
else:
    st.sidebar.info("Tu carrito está vacío. ¡Antójate de algo delicioso! 😋")

# --- AI ASSISTANT (CHATBOT) ---
st.sidebar.markdown("---")
st.sidebar.subheader("🐮 Chat con la Vaquita (IA)")
st.sidebar.caption("¡Pregúntame sobre el menú o sobre Sevilla!")

API_KEY = "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"

def call_openrouter(prompt):
    try:
        # Contexto del negocio para la IA
        menu_ctx = "\n".join([f"- {k}: {', '.join([i['name'] + ' ($' + str(i['price']) + ')' for i in v])}" for k, v in menu_categories.items()])
        full_context = f"""
        Eres 'La Vaquita', la asistente virtual de 'Kumis del Balcón' en Sevilla, Valle del Cauca. 
        Eres amigable, campestre y usas muchos emojis de vacas y café 🐮☕.
        
        NUESTRO MENÚ ACTUAL:
        {menu_ctx}
        
        SOBRE SEVILLA:
        - Capital Cafetera de Colombia.
        - Patrimonio del Paisaje Cultural Cafetero.
        - Famosa por sus balcones, el Festival de la Bandola y la Basílica San Luis Gonzaga.
        
        REGLAS DE ORO:
        1. TOLERANCIA ORTOGRÁFICA: Responde a todo tipo de preguntas sobre el menú, NO importa la ortografía o si faltan tildes.
        2. ENTENDIMIENTO FLEXIBLE: Si el usuario escribe mal un producto (ej. 'cumis', 'pandebono', 'tortas'), identifica a qué se refiere y responde con la información correcta del menú.
        3. RECOMENDACIONES: Siempre recomienda maridajes (ej. Kumis con Pandebono o Torta de Almojábana).
        4. SEVILLA: Si preguntan por Sevilla, invítales a visitarnos frente al parque principal.
        5. ESTILO: Sé breve, cordial y usa términos cercanos ("vecino", "amigo", "claro que sí").
        """
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "https://kumis-del-balcon.streamlit.app", # Recomendado por OpenRouter
                "X-Title": "Kumis del Balcon",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "meta-llama/llama-3.2-3b-instruct:free",
                "messages": [
                    {"role": "system", "content": full_context},
                    {"role": "user", "content": prompt}
                ]
            })
        )
        if response.status_code == 200:
            res_json = response.json()
            if 'choices' in res_json and len(res_json['choices']) > 0:
                return res_json['choices'][0]['message']['content']
        return "Muuu... parece que mi conexión falló. ¡Prueba de nuevo! 🐮"
    except:
        return "Lo siento, la vaquita está descansando. Intenta en un momento. 🐮"

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
        response = call_openrouter(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.sidebar.button("Borrar Chat", key="clear_chat"):
    st.session_state.messages = []
    st.rerun()


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




