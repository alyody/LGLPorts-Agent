import streamlit as st
import pandas as pd

# Load Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQp1YVzX0T3bqdtBw7wVMspdhocnc0Db7FmC-WiI-o203YyoZMtJlytRGcC7727Utz7Aw08Xr1JmZbk/pub?gid=0&single=true&output=csv"
df = pd.read_csv(sheet_url)

# Custom CSS for modern UI
st.markdown("""
    <style>
        .main {
            background-color: #f0f4f8;
        }
        .stChatMessage {
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stButton>button {
            background-color: #e0f0ff;
            color: #003366;
            border-radius: 8px;
            padding: 8px 16px;
            margin: 4px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #cce4ff;
        }
        .info-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        .sidebar .sidebar-content {
            background-color: #e6f2ff;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar with logo and navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Globe_icon.svg/1024px-Globe_icon.svg.png", width=100)
st.sidebar.title("LGL Navigation")
st.sidebar.markdown("Navigate through AREA → COUNTRY → PORT to view logistics details.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.stage = "start"
    st.session_state.area = None
    st.session_state.country = None
    st.session_state.port = None

st.title("🌍 LGL Info Bot")

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Reset function
def reset_bot():
    st.session_state.stage = "start"
    st.session_state.area = None
    st.session_state.country = None
    st.session_state.port = None
    st.session_state.messages = []

# Stage 1: Start
if st.session_state.stage == "start":
    user_input = st.chat_input("Type 'LGL' to begin:")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        if user_input.strip().lower() == "lgl":
            st.session_state.stage = "area"
            st.session_state.messages.append({"role": "assistant", "content": "Great! Please select an AREA:"})
            st.rerun()
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Please type 'LGL' to begin."})
            st.rerun()

# Stage 2: AREA selection
elif st.session_state.stage == "area":
    areas = df["AREA"].dropna().unique()
    st.chat_message("assistant").markdown("Select an AREA:")
    for area in areas:
        if st.button(area):
            st.session_state.area = area
            st.session_state.stage = "country"
            st.session_state.messages.append({"role": "assistant", "content": f"You selected **{area}**. Now choose a COUNTRY:"})
            st.rerun()

# Stage 3: COUNTRY selection
elif st.session_state.stage == "country":
    countries = df[df["AREA"] == st.session_state.area]["COUNTRY"].dropna().unique()
    st.chat_message("assistant").markdown("Select a COUNTRY:")
    for country in countries:
        if st.button(country):
            st.session_state.country = country
            st.session_state.stage = "port"
            st.session_state.messages.append({"role": "assistant", "content": f"You selected **{country}**. Now choose a PORT:"})
            st.rerun()

# Stage 4: PORT selection
elif st.session_state.stage == "port":
    ports = df[
        (df["AREA"] == st.session_state.area) &
        (df["COUNTRY"] == st.session_state.country)
    ]["PORT"].dropna().unique()
    st.chat_message("assistant").markdown("Select a PORT:")
    for port in ports:
        if st.button(port):
            st.session_state.port = port
            st.session_state.stage = "details"
            st.session_state.messages.append({"role": "assistant", "content": f"You selected **{port}**. Here are the details:"})
            st.rerun()

# Stage 5: Show details
elif st.session_state.stage == "details":
    row = df[
        (df["AREA"] == st.session_state.area) &
        (df["COUNTRY"] == st.session_state.country) &
        (df["PORT"] == st.session_state.port)
    ].iloc[0]

    details = f"""
<div class="info-card">
    <h4>📍 Port Details</h4>
    <ul>
        <li><strong>AREA:</strong> {row['AREA']}</li>
        <li><strong>COUNTRY:</strong> {row['COUNTRY']}</li>
        <li><strong>PORT:</strong> {row['PORT']}</li>
        <li><strong>IMPORT:</strong> {row.get('IMPORT', 'N/A')}</li>
        <li><strong>EXPORT:</strong> {row.get('EXPORT', 'N/A')}</li>
        <li><strong>TRANSHIPMET:</strong> {row.get('TRANSHIPMET', 'N/A')}</li>
        <li><strong>AGENT COMPANY:</strong> {row.get('AGENT COMPANY', 'N/A')}</li>
        <li><strong>LGL AGENT NAME:</strong> {row.get('LGL AGENT NAME', 'N/A')}</li>
        <li><strong>MOBILE:</strong> {row.get('MOBILE', 'N/A')}</li>
        <li><strong>EMAIL:</strong> {row.get('EMAIL', 'N/A')}</li>
        <li><strong>LGL WEBSITE:</strong> {row.get('LGL WEBSITE', 'N/A')}</li>
        <li><strong>Notes:</strong> {row.get('Notes', 'None')}</li>
    </ul>
</div>
"""
    st.markdown(details, unsafe_allow_html=True)

    if st.button("🔁 Start Over"):
        reset_bot()
        st.rerun()
