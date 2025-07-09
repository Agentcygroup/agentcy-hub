#!/usr/bin/env python3
import streamlit as st
import os, requests

st.set_page_config(page_title="Agentcy Hub", layout="wide")
st.title("🤖 Agentcy Hub Dashboard")
st.markdown("Monitor and interact with agents in a unified interface.")

st.sidebar.title("🔐 API Config")
api_token = st.sidebar.text_input("Enter API Token", type="password")

st.sidebar.markdown("---")
if st.sidebar.button("🔁 Refresh Agents"):
    st.experimental_rerun()

st.header("🧠 Active Agents")

agents = [d for d in os.listdir("..") if os.path.isdir(os.path.join("..", d)) and os.path.isfile(os.path.join("..", d, "main.py"))]

for agent in agents:
    agent_path = os.path.join("..", agent)
    with st.expander(f"🛰 Agent: {agent}"):
        st.write(f"📁 Located at `{agent_path}/main.py`")
        with open(f"{agent_path}/main.py") as f:
            st.code(f.read(), language='python')

        port = 8000 + (abs(hash(agent)) % 1000)
        try:
            resp = requests.get(f"http://localhost:{port}", timeout=1)
            status = resp.json().get("status", "❓ Unknown")
            st.success(f"✅ Ping Success: {status} at port {port}")
        except:
            st.error(f"❌ Agent not responding on port {port}")
