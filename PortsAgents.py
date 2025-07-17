import streamlit as st
import pandas as pd

# Load new Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQp1YVzX0T3bqdtBw7wVMspdhocnc0Db7FmC-WiI-o203YyoZMtJlytRGcC7727Utz7Aw08Xr1JmZbk/pub?gid=0&single=true&output=csv"
df = pd.read_csv(sheet_url)

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
- **AREA**: {row['AREA']}
- **COUNTRY**: {row['COUNTRY']}
- **PORT**: {row['PORT']}
- **IMPORT**: {row.get('IMPORT', 'N/A')}
- **EXPORT**: {row.get('EXPORT', 'N/A')}
- **TRANSHIPMET**: {row.get('TRANSHIPMET', 'N/A')}
- **AGENT COMPANY**: {row.get('AGENT COMPANY', 'N/A')}
- **LGL AGENT NAME**: {row.get('LGL AGENT NAME', 'N/A')}
- **MOBILE**: {row.get('MOBILE', 'N/A')}
- **EMAIL**: {row.get('EMAIL', 'N/A')}
- **LGL WEBSITE**: {row.get('LGL WEBSITE', 'N/A')}
- **Notes**: {row.get('Notes', 'None')}
"""
    st.chat_message("assistant").markdown(details)

    if st.button("🔁 Start Over"):
        reset_bot()
        st.rerun()
