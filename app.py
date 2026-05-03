import streamlit as st
import sys
import os
import json
import uuid
import time
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt

# Add the project root to sys.path so we can import src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.graph import app as graph_app
from src.state import FluxIdeasState
from src.database import FluxIdeasDB

# Initialize Database
db = FluxIdeasDB()

st.set_page_config(page_title='FluxIdeas | AI Intelligence', page_icon='⚡', layout='wide', initial_sidebar_state='collapsed')

# Premium CSS for Flux Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

    .stApp { background: radial-gradient(circle at 50% 0%, #1e293b, #0f172a, #020617); font-family: 'Outfit', sans-serif; }
    .flux-title { font-size: 5.5rem !important; font-weight: 900; letter-spacing: -4px; background: linear-gradient(135deg, #60efff 0%, #00ff87 50%, #60efff 100%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0px !important; animation: shine 5s linear infinite; filter: drop-shadow(0 0 20px rgba(0, 255, 135, 0.2)); }
    @keyframes shine { to { background-position: 200% center; } }
    .flux-tagline { text-align: center; color: #94a3b8; font-size: 1.1rem; font-weight: 300; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 50px !important; }
    
    /* Glassmorphism Cards */
    div[data-testid='stVerticalBlock'] > div:has(div.flux-card) { 
        background: rgba(15, 23, 42, 0.4); 
        backdrop-filter: blur(12px); 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        border-radius: 30px; 
        padding: 40px; 
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4); 
        margin-bottom: 30px; 
    }
    
    div.stButton > button { 
        background: linear-gradient(135deg, #00ff87 0%, #60efff 100%) !important; 
        color: #020617 !important; 
        font-weight: 800 !important; 
        font-size: 1.2rem !important; 
        padding: 1rem 3rem !important; 
        border-radius: 100px !important; 
        border: none !important; 
        box-shadow: 0 10px 30px rgba(0, 255, 135, 0.3) !important; 
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; 
    }
    div.stButton > button:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0, 255, 135, 0.6) !important; }
    
    .flux-terminal { 
        background: #010409 !important; 
        border: 1px solid #1e293b !important; 
        border-radius: 20px !important; 
        padding: 25px !important; 
        font-family: 'JetBrains Mono', monospace !important; 
        color: #60efff !important; 
        line-height: 1.6; 
    }
    
    .stTextInput > div > div > input { 
        background: rgba(30, 41, 59, 0.7) !important; 
        border-radius: 20px !important; 
        border: 1px solid rgba(255,255,255,0.1) !important; 
        color: white !important; 
        padding: 20px !important; 
    }
    
    .problem-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #60efff;
        margin-bottom: 10px;
    }
    
    .metric-pill {
        background: rgba(30, 41, 59, 0.5);
        color: #94a3b8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-right: 8px;
        border: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────
st.markdown("<div style='text-align:center; margin-bottom: -30px;'><img src='https://img.icons8.com/nolan/256/lightning-bolt.png' width='128'></div>", unsafe_allow_html=True)
st.markdown("<h1 class='flux-title'>FLUXIDEAS</h1>", unsafe_allow_html=True)
st.markdown("<p class='flux-tagline'>Advanced Multi-Agent Intelligence Synthesis</p>", unsafe_allow_html=True)

# Initialize Session State
if 'app_stage' not in st.session_state:
    st.session_state.app_stage = "input"
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.current_state = None
    st.session_state.topic = ""
    st.session_state.selected_problem = None
    st.session_state.archived_dossier = None
    st.session_state.live_logs = []
    st.session_state.chat_history = []

def add_log(agent, message, container=None):
    timestamp = time.strftime("%H:%M:%S")
    log_html = f"<div class='log-entry'><span style='color:#475569'>[{timestamp}]</span> <span style='color:#00ff87; font-weight:bold;'>{agent.upper()}</span>: {message}</div>"
    st.session_state.live_logs.append(log_html)
    if len(st.session_state.live_logs) > 20:
        st.session_state.live_logs.pop(0)
    if container:
        with container:
            for l in st.session_state.live_logs[::-1]:
                st.markdown(l, unsafe_allow_html=True)

def generate_pitch_deck(p_name, dossier, market, risk):
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    slide.shapes.title.text = p_name
    slide.placeholders[1].text = f"Founder's Dossier & Market Strategy\nGenerated by FluxIdeas"
    
    pptx_io = BytesIO()
    prs.save(pptx_io)
    pptx_io.seek(0)
    return pptx_io

config = {"configurable": {"thread_id": st.session_state.thread_id}}

def process_stream(stream_generator, status_container, log_container=None):
    progress_bar = st.progress(0, text="⚡ Initializing Multi-Agent Flux...")
    agent_count = 0
    total_agents = 9
    
    for output in stream_generator:
        if "__interrupt__" in output:
            continue
        for key, value in output.items():
            if not isinstance(value, dict):
                continue
            agent_count += 1
            progress = min(agent_count / total_agents, 1.0)
            if st.session_state.current_state is None:
                st.session_state.current_state = value.copy()
            else:
                st.session_state.current_state.update(value)
            
            if key == "orchestrator":
                next_a = value.get('next_agent')
                status_container.update(label=f"🤖 Orchestrator: Routing to {next_a}...", state="running")
                progress_bar.progress(progress, text=f"Routing to {next_a.upper()}...")
                add_log("orchestrator", f"Decision: Handing over mission to {next_a.upper()}.", log_container)
            elif key == "analyst":
                status_container.update(label="📊 Analyst Agent: Ranking Market Gaps...", state="running")
                problems = value.get("identified_problems", [])
                st.write(f"✓ **Analyst** identified {len(problems)} top-tier opportunities.")
                add_log("analyst", f"Analysis finished. Selected {len(problems)} high-potential gaps.", log_container)
            elif key == "strategist":
                status_container.update(label="📈 Strategist Agent: Drafting Business Plan...", state="running")
                st.write("✓ **Strategist** finalized the 7-point Founder's Dossier.")
                add_log("strategist", "Dossier drafting complete.", log_container)
            elif key == "critic":
                status_container.update(label="🕵️‍♂️ Critic Agent: Final Risk Audit...", state="running")
                st.write("✓ **Critic** finished stress-testing the model.")
                add_log("critic", "Red-team audit finished.", log_container)
                progress_bar.empty()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🖥️ Mission Control")
    log_container = st.container(height=300)
    with log_container:
        if st.session_state.live_logs:
            for l in st.session_state.live_logs[::-1]:
                st.markdown(l, unsafe_allow_html=True)
        else:
            st.caption("Waiting for mission start...")
    
    st.markdown("---")
    st.markdown("### 🗄️ Flux Library")
    archived_items = db.get_all_dossiers()
    if not archived_items:
        st.caption("No archived dossiers yet.")
    else:
        for item in archived_items:
            date_str = item['created_at'][:10]
            if st.button(f"{date_str}: {item['problem_name']}", key=f"arch_{item['id']}", use_container_width=True):
                st.session_state.archived_dossier = item
                st.session_state.app_stage = "view_archive"
                st.rerun()
    
    st.markdown("---")
    if st.button("➕ Start New Flux", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ── Main UI Logic ───────────────────────────────────────────────────
if st.session_state.app_stage == "input":
    st.markdown("<div class='flux-card'>", unsafe_allow_html=True)
    with st.form("search_form", border=False):
        topic = st.text_input("Enter a Market or Topic", placeholder="What niche are we auditing today?")
        target_location = st.text_input("🌍 Target Location", value="Global")
        skills = st.text_input("My Skills", placeholder="e.g. Python, Marketing")
        budget = st.selectbox("Monthly Budget", ["$0 - $100", "$100 - $1,000", "$1,000+"])
        time_avail = st.selectbox("Weekly Time", ["5-10 hrs", "10-20 hrs", "Full Time"])
        submit = st.form_submit_button("⚡ Launch Intelligence Scan", use_container_width=True)
        if submit and topic:
            st.session_state.topic = topic
            st.session_state.founder_profile = {"location": target_location, "skills": skills, "budget": budget, "time": time_avail}
            st.session_state.app_stage = "processing1"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.app_stage == "processing1":
    with st.status("⚡ FluxIdeas Intelligence Pipeline Active...", expanded=True) as status:
        initial_state = {"topic": st.session_state.topic, "founder_profile": st.session_state.founder_profile}
        try:
            process_stream(graph_app.stream(initial_state, config=config), status, log_container)
            graph_state = graph_app.get_state(config)
            if graph_state.next and graph_state.next[0] == "ask_human":
                st.session_state.app_stage = "selection"
            else:
                st.session_state.app_stage = "done"
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

elif st.session_state.app_stage == "selection":
    st.markdown("### 🎯 Select a Market Gap to Build")
    problems = st.session_state.current_state.get("identified_problems", []) if st.session_state.current_state else []
    if not problems:
        st.error("No problems identified.")
    else:
        for idx, p in enumerate(problems):
            with st.container():
                st.markdown(f"<div class='problem-title'>{p.get('problem_name')}</div>", unsafe_allow_html=True)
                st.write(p.get('description'))
                if st.button("✅ Select & Build", key=f"sel_{idx}"):
                    st.session_state.selected_problem = p
                    st.session_state.app_stage = "processing2"
                    st.rerun()
                st.markdown("---")

elif st.session_state.app_stage == "processing2":
    with st.status("⚙️ Resuming Pipeline...", expanded=True) as status:
        graph_app.update_state(config, {"selected_problem": st.session_state.selected_problem})
        try:
            process_stream(graph_app.stream(None, config=config), status, log_container)
            st.session_state.app_stage = "done"
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

elif st.session_state.app_stage == "done":
    sel_prob = st.session_state.get("selected_problem", {})
    dossier = (st.session_state.current_state or {}).get("blueprint", {}) or {}
    st.success(f"✅ Founder's Dossier Ready: {sel_prob.get('problem_name')}")
    
    tab1, tab2, tab3 = st.tabs(["📊 The Insight", "💡 The MVP", "🛠️ The Build"])
    with tab1:
        st.markdown(f"**Market Score:** {sel_prob.get('market_score')}/10")
        st.write(sel_prob.get('market_gap'))
    with tab2:
        st.json(dossier.get("mvp_blueprint", {}))
    with tab3:
        st.json(dossier.get("technical_roadmap", {}))
    
    if st.button("🔄 Start New Scan"):
        st.session_state.clear()
        st.rerun()

elif st.session_state.app_stage == "view_archive":
    item = st.session_state.archived_dossier
    st.markdown(f"### 🗄️ Viewing Archived: {item['problem_name']}")
    st.json(json.loads(item['blueprint_json']))
    if st.button("🔙 Back"):
        st.session_state.app_stage = "input"
        st.rerun()
