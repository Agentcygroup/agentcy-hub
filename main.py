#!/usr/bin/env python3
import streamlit as st
import os, requests, subprocess, psutil

st.set_page_config(page_title="Agentcy Hub", layout="wide")
st.title("🤖 Agentcy Hub Dashboard")
st.markdown("Monitor and interact with agents in a unified interface.")

st.sidebar.title("🔐 API Config")
token = st.sidebar.text_input("Enter API Token", type="password")
st.sidebar.markdown("---")
if st.sidebar.button("🔁 Refresh Agents"):
    st.experimental_rerun()

st.header("🧠 Active Agents")

def is_running(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            return True
    return False

agents = [d for d in os.listdir("..") if os.path.isdir(os.path.join("..", d)) and os.path.isfile(os.path.join("..", d, "main.py"))]

for agent in agents:
    agent_path = os.path.join("..", agent)
    port = 8000 + (abs(hash(agent)) % 1000)
    with st.expander(f"🛰 Agent: {agent}"):
        st.write(f"📁 `{agent_path}/main.py`")
        try:
            with open(f"{agent_path}/main.py") as f:
                st.code(f.read(), language='python')
        except:
            st.error("❌ Could not read file")

        if not is_running(port):
            try:
                subprocess.Popen(["python3", os.path.join(agent_path, "main.py")])
                st.warning(f"⚙️ Launched on port {port}")
            except:
                st.error("❌ Launch failed")

        try:
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            r = requests.get(f"http://localhost:{port}", headers=headers, timeout=1)
            st.success(f"✅ {r.json().get('status', 'OK')} on port {port}")
        except:
            st.error(f"❌ No response on port {port}")
