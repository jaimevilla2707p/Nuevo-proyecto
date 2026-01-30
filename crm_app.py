import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import requests
import json
from utils import call_openrouter

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
page = st.sidebar.radio("Go to", ["Dashboard", "Contacts", "Pipeline", "Analytics"])

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

# --- ANALYTICS PAGE ---
elif page == "Analytics":
    st.title("📈 Analytics & Insights")
    
    if not deals_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Pipeline by Stage")
            stage_counts = deals_df.groupby('Stage').size().reset_index(name='Deals')
            fig_pie = px.pie(stage_counts, values='Deals', names='Stage', hole=0.4,
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.subheader("Deal Value Distribution")
            fig_hist = px.histogram(deals_df, x="Value", nbins=10, 
                                    color_discrete_sequence=['#27ae60'])
            st.plotly_chart(fig_hist, use_container_width=True)
            
        st.markdown("---")
        
        st.subheader("Expected Close Dates")
        deals_df['Close Date'] = pd.to_datetime(deals_df['Close Date'])
        fig_timeline = px.scatter(deals_df, x="Close Date", y="Value", color="Stage",
                                  size="Value", hover_name="Deal Name",
                                  title="Deal Value Over Time")
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("Add some deals to see analytics!")

# --- END OF APP ---

