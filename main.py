import streamlit as st
import os

st.set_page_config(page_title="Agentcy Hub", layout="wide")

st.title("🤖 Agentcy Hub Dashboard")
st.markdown("Monitor and interact with agents in a unified interface.")

st.header("🧠 Active Agents")
agents = [d for d in os.listdir("..") if os.path.isdir(os.path.join("..", d)) and os.path.isfile(os.path.join("..", d, "main.py"))]

for agent in agents:
    with st.expander(f"Agent: {agent}"):
        st.write(f"📁 Located at `../{agent}/main.py`")
        st.code(open(f"../{agent}/main.py").read(), language='python')
