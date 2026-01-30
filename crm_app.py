import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import requests
import json
import re
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Growth CRM", page_icon="🚀", layout="wide")

# --- DATA PERSISTENCE ---
CONTACTS_FILE = "contacts.csv"
DEALS_FILE = "deals.csv"

def load_data():
    if not os.path.exists(CONTACTS_FILE):
        contacts = pd.DataFrame(columns=["Name", "Company", "Email", "Phone", "Status", "Last Contact"])
        contacts.to_csv(CONTACTS_FILE, index=False)
    else:
        contacts = pd.read_csv(CONTACTS_FILE)

    if not os.path.exists(DEALS_FILE):
        deals = pd.DataFrame(columns=["Deal Name", "Company", "Value", "Stage", "Close Date"])
        deals.to_csv(DEALS_FILE, index=False)
    else:
        deals = pd.read_csv(DEALS_FILE)
    
    return contacts, deals

def save_data(contacts, deals):
    contacts.to_csv(CONTACTS_FILE, index=False)
    deals.to_csv(DEALS_FILE, index=False)

# Load data locally
contacts_df, deals_df = load_data()

# --- SIDEBAR STYLE ---
st.sidebar.title("🚀 Growth CRM")
st.sidebar.markdown("---")
page = st.sidebar.radio("Go to", ["Dashboard", "Contacts", "Pipeline", "Analytics", "AI Assistant"])

# --- DASHBOARD PAGE ---
if page == "Dashboard":
    st.title("📊 Dashboard")
    st.markdown("Welcome back! Here's what's happening today.")

    # Top KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    total_pipeline_value = deals_df['Value'].sum() if not deals_df.empty else 0
    total_deals = len(deals_df)
    total_contacts = len(contacts_df)
    won_deals = len(deals_df[deals_df['Stage'] == 'Closed Won']) if not deals_df.empty else 0

    col1.metric("Pipeline Value", f"${total_pipeline_value:,.0f}")
    col2.metric("Active Deals", total_deals)
    col3.metric("Total Contacts", total_contacts)
    col4.metric("Won Deals", won_deals)

    st.markdown("---")

    # Recent Deals Table
    st.subheader("Recent Deals")
    if not deals_df.empty:
        st.dataframe(deals_df.tail(5), use_container_width=True)
    else:
        st.info("No deals found. Go to 'Pipeline' to add one.")

# --- CONTACTS PAGE ---
elif page == "Contacts":
    st.title("👥 Contacts")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        with st.popover("➕ Add Contact"):
            with st.form("new_contact"):
                name = st.text_input("Name")
                company = st.text_input("Company")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                status = st.selectbox("Status", ["Lead", "Customer", "Partner", "Inactive"])
                submitted = st.form_submit_button("Save Contact")
                
                if submitted:
                    new_contact = pd.DataFrame([{
                        "Name": name, "Company": company, "Email": email, 
                        "Phone": phone, "Status": status, 
                        "Last Contact": datetime.now().strftime("%Y-%m-%d")
                    }])
                    contacts_df = pd.concat([contacts_df, new_contact], ignore_index=True)
                    save_data(contacts_df, deals_df)
                    st.success("Contact Added!")
                    st.rerun()

    with col1:
        search = st.text_input("🔍 Search Contacts", placeholder="Search by name, company...")
    
    # Filter
    if search:
        filtered_df = contacts_df[
            contacts_df['Name'].str.contains(search, case=False, na=False) |
            contacts_df['Company'].str.contains(search, case=False, na=False)
        ]
        st.dataframe(
            filtered_df, 
            use_container_width=True, 
            column_config={
                "Email": st.column_config.LinkColumn("Email"),
                "Status": st.column_config.SelectboxColumn(
                    "Status", options=["Lead", "Customer", "Partner", "Inactive"]
                )
            },
            hide_index=True
        )
        st.info("Clear search to enable editing.")
    else:
        edited_contacts = st.data_editor(
            contacts_df,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Email": st.column_config.LinkColumn("Email"),
                "Status": st.column_config.SelectboxColumn(
                    "Status", options=["Lead", "Customer", "Partner", "Inactive"]
                )
            },
            hide_index=True,
            key="contacts_editor"
        )
        
        if not edited_contacts.equals(contacts_df):
            contacts_df = edited_contacts
            save_data(contacts_df, deals_df)
            st.rerun()

# --- PIPELINE PAGE ---
elif page == "Pipeline":
    st.title("💼 Deal Pipeline")
    
    with st.expander("➕ Add New Deal"):
        with st.form("new_deal"):
            deal_name = st.text_input("Deal Name")
            deal_company = st.selectbox("Company", contacts_df['Company'].unique()) if not contacts_df.empty else st.text_input("Company")
            value = st.number_input("Value ($)", min_value=0, step=100)
            stage = st.selectbox("Stage", ["New", "Discovery", "Proposal", "Negotiation", "Closed Won", "Closed Lost"])
            close_date = st.date_input("Expected Close Date")
            submitted_deal = st.form_submit_button("Create Deal")
            
            if submitted_deal:
                new_deal = pd.DataFrame([{
                    "Deal Name": deal_name, "Company": deal_company, 
                    "Value": value, "Stage": stage, 
                    "Close Date": close_date
                }])
                deals_df = pd.concat([deals_df, new_deal], ignore_index=True)
                save_data(contacts_df, deals_df)
                st.success("Deal Created!")
                st.rerun()

    # Visual Kanban Board (Simulated with Columns)
    stages = ["New", "Discovery", "Proposal", "Negotiation", "Closed Won"]
    cols = st.columns(len(stages))
    
    for i, stage in enumerate(stages):
        with cols[i]:
            st.markdown(f"### {stage}")
            stage_deals = deals_df[deals_df['Stage'] == stage]
            for _, deal in stage_deals.iterrows():
                with st.container(border=True):
                    st.markdown(f"**{deal['Deal Name']}**")
                    st.caption(f"{deal['Company']}")
                    st.markdown(f"💰 **${deal['Value']:,.0f}**")
                    
                    # Action Buttons
                    col_move, col_del = st.columns(2)
                    with col_move:
                        if st.button("➡", key=f"move_{deal['Deal Name']}_{i}", help="Move to next stage"):
                            if i < len(stages) - 1:
                                next_stage = stages[i+1]
                                deals_df.loc[deals_df['Deal Name'] == deal['Deal Name'], 'Stage'] = next_stage
                                save_data(contacts_df, deals_df)
                                st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_{deal['Deal Name']}_{i}", help="Delete Deal"):
                            deals_df = deals_df[deals_df['Deal Name'] != deal['Deal Name']]
                            save_data(contacts_df, deals_df)
                            st.rerun()

    st.markdown("---")
    st.subheader("📋 Deals Management (Add/Edit/Delete)")
    st.info("You can add new rows at the bottom, or select rows and press 'Delete' to remove them.")
    edited_deals = st.data_editor(
        deals_df,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Stage": st.column_config.SelectboxColumn(
                "Stage", options=["New", "Discovery", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
            ),
            "Value": st.column_config.NumberColumn(
                "Value", format="$%d"
            )
        },
        hide_index=True,
        key="deals_editor"
    )
    
    if not edited_deals.equals(deals_df):
        deals_df = edited_deals
        save_data(contacts_df, deals_df)
        st.rerun()

# --- AI ASSISTANT PAGE ---
elif page == "AI Assistant":
    st.title("🤖 AI Sales Assistant")
    st.markdown("Use AI to analyze your pipeline, draft emails, and get sales advice.")

    # API key — prefer Streamlit Secrets (OPENROUTER_API_KEY) or fallback to env var
    API_KEY = ""
    try:
        API_KEY = st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
    
    def call_openrouter(prompt):
        # Warn if API key not configured
        if not API_KEY:
            return "⚠️ Muuu... No tengo la API key configurada. Añade `OPENROUTER_API_KEY` en Streamlit Secrets o en las variables de entorno."
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                },
                data=json.dumps({
                    "model": "google/gemini-2.0-flash-exp:free",
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error de conexión: {str(e)}"

    tab1, tab2, tab3 = st.tabs(["💡 Estrategia de Ventas", "📧 Redactor de Correos", "💬 Vaquita Chat"])

    with tab1:
        st.subheader("Análisis de Pipeline")
        if st.button("Generar Consejos de Venta"):
            with st.spinner("Analizando tus datos..."):
                # Prepare context
                deals_summary = deals_df.to_string() if not deals_df.empty else "No hay negocios activos."
                prompt = f"Eres un experto en ventas. Analiza estos negocios en mi CRM y dame 3 consejos clave para cerrar más ventas esta semana:\n\n{deals_summary}"
                
                advice = call_openrouter(prompt)
                st.markdown("### 📋 Recomendaciones de la IA")
                st.write(advice)

    with tab2:
        st.subheader("Redactor de Seguimiento")
        if not contacts_df.empty:
            contact_to_email = st.selectbox("Selecciona un contacto:", contacts_df['Name'].unique())
            selected_contact = contacts_df[contacts_df['Name'] == contact_to_email].iloc[0]
            
            tone = st.radio("Tono del correo:", ["Formal", "Amigable", "Persuasivo"])
            
            if st.button("Redactar Correo"):
                with st.spinner("Redactando..."):
                    prompt = f"Escribe un correo electrónico corto de seguimiento para {selected_contact['Name']} de la empresa {selected_contact['Company']}. El tono debe ser {tone}. El objetivo es agendar una reunión para hablar sobre nuestros productos lácteos artesanales."
                    
                    email_draft = call_openrouter(prompt)
                    st.markdown("### 📝 Borrador Sugerido")
                    st.text_area("Copia este texto:", email_draft, height=300)
        else:
            st.info("Agrega contactos primero para redactar correos.")

    # --- Vaquita Chat (estilo WhatsApp) ---
    with tab3:
        st.subheader("Chat con la Vaquita 🐮")

        # Initialize session state for chat history
        if 'vaquita_chat' not in st.session_state:
            st.session_state.vaquita_chat = [
                {"role": "bot", "content": "Muuu! Soy la Vaquita, ¿en qué te ayudo hoy? 🐄"}
            ]

        # Chat display area with fixed height and scroll
        chat_css = """
        <style>
        .chat-box {height:400px; overflow-y:auto; padding:12px; border:1px solid #e6e6e6; border-radius:8px; background:#fafafa}
        .msg {margin:8px 0; max-width:72%; padding:10px; border-radius:12px; clear:both}
        .msg.user {background:#dcf8c6; float:right}
        .msg.bot {background:#ffffff; float:left}
        .sender {font-size:11px; color:#888; margin-bottom:4px}
        </style>
        """

        messages_html = []
        for m in st.session_state.vaquita_chat:
            role = m.get('role', 'bot')
            cls = 'user' if role == 'user' else 'bot'
            sender = 'Tú' if role == 'user' else 'Vaquita'
            # Escape content for safety
            content = m.get('content', '')
            messages_html.append(f"<div class='msg {cls}'><div class='sender'>{sender}</div><div class='content'>{content}</div></div>")

        st.markdown(chat_css + "<div class='chat-box'>" + "".join(messages_html) + "</div>", unsafe_allow_html=True)

        # Input and send
        user_input = st.text_input("Escribe un mensaje...", key="vaquita_input")
        if st.button("Enviar", key="vaquita_send") or (user_input and user_input.endswith('\n')):
            prompt = user_input.strip()
            if prompt:
                st.session_state.vaquita_chat.append({"role": "user", "content": prompt})

                # Call OpenRouter or enhanced local fallback with expanded knowledge
                def call_openrouter_chat(prompt_text):
                    # Local knowledge about Sevilla, Valle del Cauca
                    sevilla_facts = {
                        "overview": (
                            "Sevilla es un municipio del departamento del Valle del Cauca, Colombia. "
                            "Está ubicado en la región Andina del suroeste colombiano y es conocido por su producción agrícola, especialmente café y caña de azúcar."
                        ),
                        "history": (
                            "Sevilla fue fundada en 1903 y ha crecido como un centro agrícola y comercial en la región. "
                            "Su historia incluye desarrollo ligado a la expansión del cultivo de café en el siglo XX y la construcción de infraestructura vial que conectó el municipio con otras ciudades del Valle del Cauca."
                        ),
                        "population": (
                            "La población de Sevilla es de decenas de miles de habitantes; para cifras exactas consulta el DANE o fuentes oficiales locales, ya que varían con censos y estimaciones."
                        ),
                        "economy": (
                            "La economía se basa en la agricultura (café, caña de azúcar, frutales), comercio local y servicios."
                        )
                    }

                    def local_vaquita_reply(text):
                        lower = text.lower()

                        # Historical / general queries about Sevilla
                        if any(k in lower for k in ["sevilla", "valle del cauca", "municipio"]):
                            if any(w in lower for w in ["historia", "fund", "fundó", "fundacion", "fundación"]):
                                return sevilla_facts['history']
                            if any(w in lower for w in ["poblacion", "habitantes", "cuantos"]):
                                return sevilla_facts['population']
                            if any(w in lower for w in ["econom", "economia", "trabajo", "actividad"]):
                                return sevilla_facts['economy']
                            return sevilla_facts['overview']

                        # Reuse CRM-specific local handlers from before
                        if re.search(r"\b(hola|buenas|hey|buenos)\b", lower):
                            return "¡Hola! Muuu... Soy la Vaquita. Puedo ayudarte con contactos, pipeline, redactar correos o responder preguntas generales."

                        m = re.search(r"(tel(e[fó]no|fono)|movil|móvil|telefono) de ([a-zA-Z\s]+)", lower)
                        if m:
                            name = m.group(3).strip()
                            matched = contacts_df[contacts_df['Name'].str.contains(name, case=False, na=False)]
                            if not matched.empty:
                                phone = matched.iloc[0].get('Phone', 'No registrado')
                                return f"El teléfono de {matched.iloc[0]['Name']} es: {phone}"
                            return f"No encuentro a {name} en tus contactos."

                        m2 = re.search(r"email de ([a-zA-Z\s]+)|correo de ([a-zA-Z\s]+)", lower)
                        if m2:
                            name = (m2.group(1) or m2.group(2) or "").strip()
                            matched = contacts_df[contacts_df['Name'].str.contains(name, case=False, na=False)]
                            if not matched.empty:
                                email = matched.iloc[0].get('Email', 'No registrado')
                                return f"El correo de {matched.iloc[0]['Name']} es: {email}"
                            return f"No encuentro a {name} en tus contactos."

                        if "redactar" in lower or "correo" in lower or "email" in lower:
                            names = contacts_df['Name'].tolist() if not contacts_df.empty else []
                            name_found = None
                            for n in names:
                                if n.lower() in lower:
                                    name_found = n
                                    break
                            tone = 'amigable'
                            if 'formal' in lower:
                                tone = 'formal'
                            if name_found:
                                company = contacts_df[contacts_df['Name'] == name_found].iloc[0].get('Company', '')
                                return (f"Asunto: Seguimiento - {name_found}\n\nHola {name_found},\n\n" \
                                        f"Quería hacer un seguimiento sobre nuestra conversación respecto a {company}. " \
                                        f"¿Tienes 20 minutos esta semana para una reunión?\n\nSaludos,\nTu equipo")
                            return "Puedo redactar un correo de seguimiento breve. Dime el nombre del contacto y el tono (Formal/Amigable)."

                        if any(w in lower for w in ['pipeline', 'deal', 'negocio', 'ventas', 'cierres']):
                            if deals_df.empty:
                                return "No veo deals en tu pipeline. Añade algunos para que pueda analizarlos."
                            df = deals_df.copy()
                            try:
                                df['Close Date'] = pd.to_datetime(df['Close Date'], errors='coerce')
                            except Exception:
                                pass
                            top = df.sort_values(by=['Value'], ascending=False).head(3)
                            bullets = []
                            for _, d in top.iterrows():
                                bullets.append(f"- {d.get('Deal Name','')} ({d.get('Company','')}) — ${d.get('Value',0):,.0f}")
                            return "Recomiendo priorizar estos deals:\n" + "\n".join(bullets)

                        if 'cuantos' in lower or 'total' in lower or 'cantidad' in lower:
                            total_contacts = len(contacts_df)
                            total_deals = len(deals_df)
                            total_value = deals_df['Value'].sum() if not deals_df.empty else 0
                            return (f"Tienes {total_contacts} contactos, {total_deals} deals en el CRM, " \
                                    f"con un valor total de ${total_value:,.0f} en pipeline.")

                        calc = re.search(r"(\d+[\.,]?\d*)\s*(\+|\-|\*|x|/|dividir|por)\s*(\d+[\.,]?\d*)", lower)
                        if calc:
                            a = float(calc.group(1).replace(',', '.'))
                            op = calc.group(2)
                            b = float(calc.group(3).replace(',', '.'))
                            if op in ['+', 'más', 'mas']:
                                return str(a + b)
                            if op in ['-', 'menos']:
                                return str(a - b)
                            if op in ['*', 'x', 'por']:
                                return str(a * b)
                            if op in ['/', 'dividir']:
                                return str(a / b if b != 0 else 'inf')

                        replies = [
                            "Muuu... cuéntame más sobre eso.",
                            "Interesante — ¿quieres que lo convierta en una tarea o un correo?",
                            "Puedo ayudarte a priorizar clientes y redactar mensajes cortos.",
                        ]
                        return random.choice(replies)

                    # If we have an API key, prefer the external model for broad/general knowledge
                    if API_KEY:
                        try:
                            payload = {
                                "model": "google/gemini-2.0-flash-exp:free",
                                "messages": [
                                    {"role": "system", "content": "Eres un asistente útil, preciso y conciso. Responde en español."},
                                    {"role": "user", "content": prompt_text}
                                ],
                                "temperature": 0.2,
                                "max_tokens": 800
                            }
                            response = requests.post(
                                url="https://openrouter.ai/api/v1/chat/completions",
                                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                                data=json.dumps(payload),
                                timeout=15
                            )
                            if response.status_code == 200:
                                j = response.json()
                                # Navigate possible response shapes
                                try:
                                    return j['choices'][0]['message']['content']
                                except Exception:
                                    return j.get('text', str(j))
                            else:
                                # Fallback to local if API returns error
                                return local_vaquita_reply(prompt_text) + f"\n\n(Nota: respuesta parcial debido a error API {response.status_code})"
                        except Exception:
                            return local_vaquita_reply(prompt_text) + "\n\n(Nota: respuesta local por fallo de conexión con la API)"

                    # No API key -> local
                    return local_vaquita_reply(prompt_text)

                with st.spinner("La Vaquita está pensando... 🐄"):
                    reply = call_openrouter_chat(prompt)
                    st.session_state.vaquita_chat.append({"role": "bot", "content": reply})
                    # Clear input field
                    st.session_state.vaquita_input = ""
                    # Rerun so the chat area scrolls (Streamlit will re-render)
                    st.experimental_rerun()

