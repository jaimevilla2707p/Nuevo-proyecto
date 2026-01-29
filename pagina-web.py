import streamlit as st
from PIL import Image
import time
import random

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
        color: #4a4a4a;
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
    
    .footer {
        background-color: #f8f9fa;
        padding: 40px;
        margin-top: 50px;
        border-top: 3px solid #e67e22;
        text-align: center;
    }
    
    .sevilla-section {
        background-color: #ecf0f1;
        padding: 30px;
        border-radius: 15px;
        margin-top: 40px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

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
    
    if st.sidebar.button("Pagar con Nequi / Bancolombia (QR)", key="pay_qr"):
        with st.sidebar:
            st.success("¡Escanea para pagar!")
            try:
                st.image("nequi_qr.png", caption="Nequi / Bancolombia")
            except:
                st.warning("QR no cargado.")
            st.info("1. Escanea el código.\n2. Envía el comprobante al WhatsApp.")
            
            st.markdown(f"""
            <a href="https://wa.me/573127321920?text=Hola,%20adjunto%20comprobante%20del%20pedido%20{random.randint(1000,9999)}" target="_blank">
                <button style="background-color: #25D366; color: white; border: none; padding: 10px; width: 100%; border-radius: 5px; font-weight: bold;">
                    📲 Enviar Comprobante WhatsApp
                </button>
            </a>
            """, unsafe_allow_html=True)

    # Wompi Button Logic
    url_wompi = f"https://checkout.wompi.co/p/?public-key=pub_test_Q5yDA9xoKdePzhSGeVe9HAez74wxobRY&currency=COP&amount-in-cents={total*100}&reference=KB-{random.randint(10000,99999)}"
    st.sidebar.link_button("💳 Pagar con Wompi", url_wompi)
    
else:
    st.sidebar.info("Tu carrito está vacío. ¡Antójate de algo delicioso! 😋")


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
<div style="text-align: center; color: #4a4a4a; max-width: 800px; margin: 0 auto; font-size: 1.2rem; background-color: #fff9c4; padding: 15px; border-radius: 10px;">
    Disfruta de la mejor tradición sevillana. Nuestros productos son 100% artesanales, 
    hechos con amor y los mejores ingredientes del <b>Valle del Cauca</b>.
</div>
<br>
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
                        time.sleep(0.5)
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


