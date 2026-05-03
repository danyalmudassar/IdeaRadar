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
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Cinematic Clean Base */
    html { scroll-behavior: smooth; }
    .stApp { 
        background: #020617; 
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 255, 135, 0.05) 0%, transparent 50%),
            radial-gradient(at 100% 0%, rgba(96, 239, 255, 0.05) 0%, transparent 50%),
            radial-gradient(at 50% 100%, rgba(15, 23, 42, 0.5) 0%, transparent 50%);
        font-family: 'Outfit', sans-serif; 
        color: #f8fafc;
        animation: aurora-bg 20s ease infinite;
    }
    @keyframes aurora-bg {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    /* Cinematic Floating Title */
    .flux-title { 
        font-size: 6.5rem !important; 
        font-weight: 900; 
        letter-spacing: -6px; 
        background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        margin-bottom: 0px !important; 
        filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.15));
        animation: float-title 6s ease-in-out infinite;
    }
    @keyframes float-title {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    /* Neon Pulse Bolt */
    .flux-bolt {
        text-align: center;
        margin-top: -50px;
        margin-bottom: 30px;
        animation: pulse-glow 4s ease-in-out infinite;
    }
    @keyframes pulse-glow {
        0%, 100% { filter: drop-shadow(0 0 10px rgba(0, 255, 135, 0.3)); transform: scale(1); }
        50% { filter: drop-shadow(0 0 30px rgba(0, 255, 135, 0.8)); transform: scale(1.05); }
    }

    .flux-tagline { 
        text-align: center; 
        color: #64748b; 
        font-size: 1.1rem; 
        font-weight: 400; 
        letter-spacing: 12px; 
        text-transform: uppercase; 
        margin-bottom: 100px !important; 
        opacity: 0.6;
    }

    /* Cinematic Clean Cards (Targeting Streamlit Forms and Containers) */
    div[data-testid="stForm"], .flux-card-wrap {
        background: rgba(15, 23, 42, 0.4) !important;
        backdrop-filter: blur(40px) saturate(150%) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 32px !important;
        padding: 60px !important;
        box-shadow: 0 80px 150px -30px rgba(0, 0, 0, 0.8) !important;
        transition: all 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
        margin-top: 20px !important;
    }
    div[data-testid="stForm"]:hover {
        border-color: rgba(0, 255, 135, 0.2) !important;
        transform: translateY(-5px);
    }

    /* Premium Cinematic Button */
    div.stButton > button { 
        background: linear-gradient(135deg, #00ff87 0%, #60efff 100%) !important; 
        color: #020617 !important; 
        font-weight: 800 !important; 
        font-size: 1.2rem !important; 
        padding: 1.2rem 4.5rem !important; 
        border-radius: 100px !important; 
        border: none !important; 
        box-shadow: 0 20px 40px rgba(0, 255, 135, 0.3) !important; 
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    div.stButton > button:hover { 
        transform: translateY(-10px) scale(1.05); 
        box-shadow: 0 40px 80px rgba(0, 255, 135, 0.6) !important; 
    }

    /* Terminal Console Aesthetic */
    .flux-terminal { 
        background: #010409 !important; 
        border: 1px solid rgba(255, 255, 255, 0.05) !important; 
        border-radius: 20px !important; 
        padding: 30px !important; 
        font-family: 'JetBrains Mono', monospace !important; 
        color: #60efff !important; 
        font-size: 0.95rem !important;
        line-height: 1.8; 
        box-shadow: inset 0 4px 20px rgba(0,0,0,0.8);
    }

    /* Luminous Inputs */
    .stTextInput > div > div > input { 
        background: rgba(15, 23, 42, 0.5) !important; 
        border-radius: 16px !important; 
        border: 1px solid rgba(255, 255, 255, 0.05) !important; 
        color: white !important; 
        padding: 20px 30px !important; 
        font-size: 1.3rem !important;
        transition: all 0.4s ease;
        backdrop-filter: blur(10px);
    }
    .stTextInput > div > div > input:focus {
        border-color: #00ff87 !important;
        box-shadow: 0 0 30px rgba(0, 255, 135, 0.2) !important;
        background: rgba(15, 23, 42, 0.8) !important;
    }

    /* Cinematic Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: transparent;
        border-radius: 12px;
        padding: 0 40px;
        color: #475569;
        font-weight: 600;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(30, 41, 59, 0.5) !important;
        color: #00ff87 !important;
        border-color: rgba(0, 255, 135, 0.3) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Elegant Quote */
    .flux-quote {
        background: rgba(15, 23, 42, 0.5);
        border-left: 5px solid #00ff87;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 25px;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ── Main Application ──────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; margin-bottom:80px;'>
    <h1 class='flux-title'>FLUXIDEAS</h1>
    <div class='flux-bolt'>
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" stroke="#00ff87" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="rgba(0,255,135,0.2)"/>
        </svg>
    </div>
    <p class='flux-tagline'>Advanced Multi-Agent Intelligence Synthesis</p>
</div>
""", unsafe_allow_html=True)

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
    log_html = f"<div class='log-entry'><span style='color:#475569'>[{timestamp}]</span> <span class='log-agent'>{agent.upper()}</span>: {message}</div>"
    st.session_state.live_logs.append(log_html)
    # Keep only last 20 logs
    if len(st.session_state.live_logs) > 20:
        st.session_state.live_logs.pop(0)
    
    # If a container handle is provided, update it live
    if container:
        with container:
            for l in st.session_state.live_logs[::-1]:
                st.markdown(l, unsafe_allow_html=True)

def generate_pitch_deck(p_name, dossier, market, risk):
    prs = Presentation()
    
    # Title Slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = p_name
    subtitle.text = f"Founder's Dossier & Market Strategy\nGenerated by FluxIdeas"

    # Problem Slide
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    title_shape.text = "The Problem & Market Gap"
    tf = body_shape.text_frame
    tf.text = dossier.get('market_gap_score', {}).get('rationale', 'Market gap identified.')
    
    # Solution Slide
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "The Solution: MVP Blueprint"
    tf = slide.shapes.placeholders[1].text_frame
    mvp = dossier.get('mvp_blueprint', {})
    for k, v in mvp.items():
        if isinstance(v, dict):
            p = tf.add_paragraph()
            p.text = f"{v.get('name')}: {v.get('description')}"
            p.level = 0

    # Market Size Slide
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Market Opportunity (TAM/SAM/SOM)"
    tf = slide.shapes.placeholders[1].text_frame
    if market:
        for k in ['tam', 'sam', 'som']:
            p = tf.add_paragraph()
            p.text = f"{k.upper()}: {market.get(k, 'N/A')}"
        p = tf.add_paragraph()
        p.text = f"Growth Rate: {market.get('growth_rate', 'N/A')}"

    # Risks Slide
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Risk Audit & Mitigation"
    tf = slide.shapes.placeholders[1].text_frame
    if risk:
        for k in ['technical_risk', 'market_risk', 'kill_switch_criteria']:
            p = tf.add_paragraph()
            p.text = f"{k.replace('_',' ').title()}: {risk.get(k, 'N/A')}"

    # Save to buffer
    pptx_io = BytesIO()
    prs.save(pptx_io)
    pptx_io.seek(0)
    return pptx_io

config = {"configurable": {"thread_id": st.session_state.thread_id}}

def process_stream(stream_generator, status_container, log_container=None):
    progress_bar = st.progress(0, text="⚡ Initializing Multi-Agent Flux...")
    agent_count = 0
    total_agents = 9 # Core pipeline agents
    
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
                if next_a != "END":
                    add_log(next_a, "Initializing agent systems... thinking...", log_container)
            elif key == "scout":
                status_container.update(label="🕵️‍♂️ Scout Agent: Crawling HackerNews...", state="running")
                sources = value.get('raw_sources', [])
                st.write(f"✓ **Scout** gathered {len(sources)} sources from HackerNews.")
                for s in sources[:3]: # Show top 3 live
                    st.caption(f"🔗 {s.get('story_title')}")
                add_log("scout", f"Scanned HN. Collected {len(sources)} source points.", log_container)
            elif key == "researcher":
                status_container.update(label="🔍 Researcher Agent: Running Tavily Hybrid Search...", state="running")
                notes = value.get("research_notes", [])
                st.write(f"✓ **Researcher** integrated {len(notes)} new findings.")
                for n in notes[:2]: # Show top 2 live
                    st.caption(f"📝 {n.split('\\n')[0]}")
                add_log("researcher", f"Deep search complete. Integrated {len(notes)} new findings via Tavily AI.", log_container)
            elif key == "reasoner":
                status_container.update(label="🧠 Reasoner Agent: Performing Deep Reasoning...", state="running")
                st.write("✓ **Reasoner** finished Chain-of-Thought pattern synthesis.")
                add_log("reasoner", "Pattern synthesis finished. Identifying market intensity.", log_container)
            elif key == "analyst":
                status_container.update(label="📊 Analyst Agent: Ranking Market Gaps...", state="running")
                problems = value.get("identified_problems", [])
                st.write(f"✓ **Analyst** identified {len(problems)} top-tier opportunities.")
                add_log("analyst", f"Analysis finished. Selected {len(problems)} high-potential gaps.", log_container)
            elif key == "strategist":
                status_container.update(label="📈 Strategist Agent: Drafting Business Plan...", state="running")
                st.write("✓ **Strategist** finalized the 7-point Founder's Dossier.")
                add_log("strategist", "Dossier drafting complete. Generated 7-point business plan.", log_container)
            elif key == "economist":
                status_container.update(label="💰 Economist Agent: Calculating TAM/SAM/SOM...", state="running")
                st.write("✓ **Economist** finalized market size projections.")
                add_log("economist", "TAM/SAM/SOM calculations finalized.", log_container)
            elif key == "designer":
                status_container.update(label="🎨 Designer Agent: Creating Visual Mockup...", state="running")
                st.write("✓ **Designer** generated the UI concept URL.")
                add_log("designer", "Visual identity and UI mockup constructed.", log_container)
            elif key == "critic":
                status_container.update(label="🕵️‍♂️ Critic Agent: Final Risk Audit...", state="running")
                st.write("✓ **Critic** finished stress-testing the model.")
                add_log("critic", "Red-team audit finished. Identified kill-switch criteria.", log_container)
                progress_bar.empty() # Clear at end

# ── Sidebar: Flux Library ──────────────────────────────────────────
with st.sidebar:
    st.markdown("### <span class='live-pulse'></span> 🖥️ Mission Control", unsafe_allow_html=True)
    st.caption("Live Multi-Agent Log")
    log_container = st.container(height=300)
    with log_container:
        if st.session_state.live_logs:
            for l in st.session_state.live_logs[::-1]: # Show newest first
                st.markdown(l, unsafe_allow_html=True)
        else:
            st.caption("Waiting for mission start...")
    
    st.markdown("---")
    st.markdown("### 🗄️ Flux Library")
    st.info("Your persisted Founder's Dossiers")
    
    archived_items = db.get_all_dossiers()
    if not archived_items:
        st.caption("No archived dossiers yet.")
    else:
        for item in archived_items:
            # Create a label with date and topic
            date_str = item['created_at'][:10]
            label = f"{date_str}: {item['problem_name']}"
            if st.button(label, key=f"arch_{item['id']}", use_container_width=True):
                st.session_state.archived_dossier = item
                st.session_state.app_stage = "view_archive"
                st.rerun()
    
    st.markdown("---")
    if st.button("➕ Start New Flux", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ── Main UI Logic ───────────────────────────────────────────────────
# Stage: INPUT
if st.session_state.app_stage == "input":
    with st.form("search_form", border=False):
        topic = st.text_input("Enter a Market or Topic (e.g. 'CI/CD tools', 'No-code for Shopify')", placeholder="What niche are we auditing today?")
        
        st.markdown("### 👤 Founder Profile & Constraints")
        st.caption("Tell the AI your background and target region to personalize the business opportunities.")
        
        c0 = st.columns(1)[0]
        with c0:
            target_location = st.text_input("🌍 Target Location", placeholder="e.g. Global, London, US, India", value="Global")
            
        c1, c2, c3 = st.columns(3)
        with c1:
            skills = st.text_input("My Skills", placeholder="e.g. Python, Marketing, Design")
        with c2:
            budget = st.selectbox("Monthly Budget", ["$0 - $100", "$100 - $1,000", "$1,000 - $1,0000", "$10,000+"])
        with c3:
            time_avail = st.selectbox("Weekly Time", ["5-10 hrs", "10-20 hrs", "20-40 hrs", "Full Time"])

        submit = st.form_submit_button("⚡ Launch Intelligence Scan", use_container_width=True)
        
        if submit and topic:
            st.session_state.topic = topic
            st.session_state.founder_profile = {
                "location": target_location,
                "skills": skills,
                "budget": budget,
                "time": time_avail
            }
            st.session_state.app_stage = "processing1"
            st.rerun()

# Stage: PROCESSING 1
if st.session_state.app_stage == "processing1":
    with st.status("⚡ FluxIdeas Intelligence Pipeline Active...", expanded=True) as status:
        initial_state = {"topic": st.session_state.topic, "founder_profile": st.session_state.founder_profile}
        try:
            process_stream(
                graph_app.stream(initial_state, config=config), 
                status,
                log_container 
            )
            
            # Check state to see if we hit the interrupt
            graph_state = graph_app.get_state(config)
            if graph_state.next and graph_state.next[0] == "ask_human":
                st.session_state.app_stage = "selection"
                status.update(label="✋ Paused for Human Input", state="complete")
                st.rerun()
            else:
                # If it finished without pausing (error case fallback)
                status.update(label="Pipeline finished without Human Node.", state="complete")
                st.session_state.app_stage = "done"
                st.rerun()
        except Exception as e:
            status.update(label=f"❌ Error: {str(e)}", state="error")

# Stage: SELECTION
if st.session_state.app_stage == "selection":
    # Ensure log container stays current on selection screen
    if st.session_state.live_logs:
        with log_container:
            for l in st.session_state.live_logs[::-1]:
                st.markdown(l, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Select a Market Gap to Build")
    st.markdown("Review each idea below — then hit **✅ Select & Build** on the one you want to pursue.")
    st.markdown("---")

    problems = []
    if st.session_state.current_state:
        problems = st.session_state.current_state.get("identified_problems", [])

    if not problems:
        st.error("No problems were identified. Please start over.")
        if st.button("🔄 Start New Scan"):
            st.session_state.clear()
            st.rerun()
    else:
        for idx, p in enumerate(problems):
            with st.container():
                hcol1, hcol2 = st.columns([5, 1])
                with hcol1:
                    st.markdown(f"<div class='problem-title'>{p.get('problem_name')}</div>", unsafe_allow_html=True)
                with hcol2:
                    if st.button("✅ Select & Build", key=f"sel_{idx}", use_container_width=True):
                        st.session_state.selected_problem = p
                        st.session_state.app_stage = "processing2"
                        st.rerun()
                
                st.markdown(f"**Market Gap:** {p.get('market_gap')}")
                st.markdown(f"**Target Customer:** {p.get('target_customer')}")
                
                # Metrics
                st.markdown(
                    f"<span class='metric-pill'>📊 Market Score: {p.get('market_score')}/10</span>"
                    f"<span class='metric-pill' style='background:#1e293b; color:#00ff87'>👤 Founder Fit: {p.get('founder_fit_score', '?')}/10</span>"
                    f"<span class='metric-pill'>🔥 Urgency: {p.get('urgency_score')}/10</span>", 
                    unsafe_allow_html=True
                )
                
                st.markdown(f"**The Problem:** {p.get('description')}")
                
                # Source references
                src_refs = p.get("source_refs", [])
                if src_refs:
                    st.markdown("**🔗 Sources:**")
                    ref_parts = []
                    for ref in src_refs:
                        title = ref.get("title", "Discussion")
                        url   = ref.get("url", "")
                        author = ref.get("author", "")
                        if url:
                            ref_parts.append(f"[{title}]({url}) by *{author}*")
                        else:
                            ref_parts.append(f"{title} by *{author}*")
                    st.markdown(" &nbsp;|&nbsp; ".join(ref_parts))

                st.markdown("---")


# Stage: PROCESSING 2
if st.session_state.app_stage == "processing2":
    with st.status("⚙️ Resuming Pipeline...", expanded=True) as status:
        # Update state with selected problem
        graph_app.update_state(config, {"selected_problem": st.session_state.selected_problem})
        
        try:
            # Resume stream by passing None
            process_stream(graph_app.stream(None, config=config), status)
            status.update(label="✅ Scan Complete!", state="complete", expanded=False)
            st.session_state.app_stage = "done"
            st.rerun()
        except Exception as e:
            status.update(label=f"❌ Error: {str(e)}", state="error")

# Stage: DONE
if st.session_state.app_stage == "done":
    sel_prob   = st.session_state.get("selected_problem", {})
    p_name     = sel_prob.get("problem_name", "N/A")
    p_score    = int(sel_prob.get("market_score", 0))
    p_sent     = sel_prob.get("sentiment", "N/A")
    dossier    = (st.session_state.current_state or {}).get("blueprint", {}) or {}

    score_color = "#00ff87" if p_score >= 75 else ("#ffb347" if p_score >= 50 else "#ff6b6b")

    # ── Header ──────────────────────────────────────────────────────────────
    st.success("✅ Founder's Dossier Ready")
    st.markdown(f"""
    <div style='background:#1e293b;padding:24px;border-radius:14px;border-left:6px solid {score_color};margin-bottom:24px'>
        <div style='font-size:1.6rem;font-weight:800;color:#f8fafc;margin-bottom:8px'>📄 {p_name}</div>
        <span style='background:#334155;color:{score_color};padding:4px 14px;border-radius:20px;font-size:0.95rem;font-weight:700;margin-right:8px'>🔥 Market Score: {p_score}/100</span>
        <span style='background:#334155;color:#a0aec0;padding:4px 14px;border-radius:20px;font-size:0.9rem;'>💬 {p_sent}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── 3 Tabs ───────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(["📊 The Insight", "💡 The MVP", "🛠️ The Build", "📉 Risk Audit"])

    # ── Tab 1: The Insight ───────────────────────────────────────────────────
    with tab1:
        # Signal Strength
        sig = dossier.get("signal_strength", {})
        st.markdown("### ⚡ Signal Strength (Validation)")
        scol1, scol2, scol3 = st.columns(3)
        scol1.metric("Mention Count", f"~{sig.get('mention_count', '?')} threads")
        scol2.metric("Signal Reliability", "✅ Confirmed")
        scol3.metric("Source", "HN / Reddit / Forums")
        st.info(f"**Where it shows up:** {sig.get('source_summary', '')}")
        st.caption(sig.get("validation", ""))

        st.markdown("---")

        # Market Gap Score
        mgs = dossier.get("market_gap_score", {})
        st.markdown("### 📈 Market Gap Score")
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Overall", f"{mgs.get('total', '?')}/10")
        mc2.metric("⚡ Urgency", f"{mgs.get('urgency', '?')}/10")
        mc3.metric("💰 Commercial", f"{mgs.get('commercial_potential', '?')}/10")
        mc4.metric("🔧 Feasibility", f"{mgs.get('feasibility', '?')}/10")
        st.markdown(f"> {mgs.get('rationale', '')}")

        st.markdown("---")

        # Market Size (Economist)
        mkt = (st.session_state.current_state or {}).get("market_size_analysis", {})
        if mkt:
            st.markdown("### 💰 Market Size Estimates")
            ec1, ec2, ec3 = st.columns(3)
            ec1.metric("TAM", mkt.get("tam", "N/A"))
            ec2.metric("SAM", mkt.get("sam", "N/A"))
            ec3.metric("SOM", mkt.get("som", "N/A"))
            st.write(f"**Growth Rate:** {mkt.get('growth_rate', 'N/A')}")
            st.success(f"**Economist Verdict:** {mkt.get('economist_verdict', '')}")
            st.markdown("---")

        # Reasoning Log
        reasoning_log = (st.session_state.current_state or {}).get("reasoning_log", "")
        if reasoning_log:
            with st.expander("🧠 View Deep Reasoning Analysis", expanded=False):
                try:
                    import json
                    parsed_log = json.loads(reasoning_log)
                    
                    st.markdown(f"**Quality Check:** `{parsed_log.get('quality_check', 'N/A')}`")
                    
                    st.markdown("**Reasoning Steps:**")
                    for step in parsed_log.get("reasoning_steps", []):
                        st.markdown(f"- {step}")
                        
                    st.markdown("**Core Clusters:**")
                    for cluster in parsed_log.get("core_clusters", []):
                        st.markdown(f"- {cluster}")
                        
                    st.markdown(f"**Market Intensity:**\n{parsed_log.get('market_intensity', '')}")
                    st.markdown(f"**Full Verdict:**\n{parsed_log.get('full_verdict', '')}")
                except Exception:
                    # Fallback if it's not valid JSON
                    st.markdown(f"```json\n{reasoning_log}\n```")
            st.markdown("---")

        # Voice of Customer
        voc = dossier.get("voice_of_customer", [])
        st.markdown("### 💬 Voice of the Customer")
        if voc:
            for item in voc:
                author = item.get('author', '')
                url    = item.get('url', '')
                source = item.get('source', 'Unknown source')
                # Build attribution line
                if url:
                    attribution = f'<a href="{url}" target="_blank" style="color:#60efff;text-decoration:none">@{author}</a> on {source}'
                elif author:
                    attribution = f'@{author} on {source}'
                else:
                    attribution = source

                st.markdown(f"""
                <div class='flux-quote'>
                    <span style='color:#f1f5f9; font-style:italic; font-size:1.1rem;'>"{item.get('quote','')}"</span><br>
                    <div style='margin-top:10px; font-size:0.9rem; color:#60efff;'>— {attribution}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No quotes captured.")

    # ── Tab 2: The MVP ───────────────────────────────────────────────────────
    with tab2:
        # Visual Mockup
        mock_url = (st.session_state.current_state or {}).get("mockup_url")
        if mock_url:
            st.markdown("### 🎨 Visual MVP Mockup")
            st.image(mock_url, caption=f"AI-Generated Mockup for {p_name}", use_container_width=True)
            st.markdown("---")

        mvp = dossier.get("mvp_blueprint", {})
        st.markdown("### 🚀 MVP Blueprint — The First 3 Features")
        for key, label, icon in [("feature_1","Core Utility","⚙️"), ("feature_2","The Hook","🪝"), ("feature_3","Admin Layer","🔐")]:
            feat = mvp.get(key, {})
            if feat:
                st.markdown(f"""
                <div style='background:#1e293b;border-radius:10px;padding:18px;margin-bottom:14px;border-left:4px solid #00ff87'>
                    <div style='font-weight:700;font-size:1.05rem;color:#f8fafc'>{icon} {feat.get('name','')}</div>
                    <div style='color:#94a3b8;margin-top:6px'>{feat.get('description','')}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        mono = dossier.get("monetization", {})
        st.markdown("### 💰 Monetization Hypothesis")
        m1, m2 = st.columns(2)
        m1.markdown(f"**Model:** {mono.get('model', 'N/A')}")
        m2.markdown(f"**Price Point:** {mono.get('price_point', 'N/A')}")
        st.info(mono.get("rationale", ""))

    # ── Tab 3: The Build ─────────────────────────────────────────────────────
    with tab3:
        comp = dossier.get("competitive_landscape", [])
        st.markdown("### ⚔️ Competitive Landscape")
        if comp:
            import pandas as pd
            df = pd.DataFrame(comp).rename(columns={
                "competitor": "Competitor",
                "weakness":   "Their Weakness",
                "your_edge":  "Your Edge"
            })
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.caption("No competitors identified.")

        st.markdown("---")
        tech = dossier.get("technical_roadmap", {})
        st.markdown("### 🛠️ Technical Roadmap")

        st.markdown(f"**🧱 Tech Stack:** `{tech.get('tech_stack', 'N/A')}`")
        st.markdown(f"**⏱️ Timeline:** {tech.get('timeline', 'N/A')}")

        dm = tech.get("data_model", [])
        if dm:
            st.markdown("**🗄️ Data Model (Key Tables):**")
            for table in dm:
                st.markdown(f"- `{table}`")

        week_plan = tech.get("week_plan", [])
        if week_plan:
            st.markdown("**📅 4-Week Sprint Plan:**")
            for w in week_plan:
                st.markdown(f"- **Week {w.get('week','')}:** {w.get('focus','')}")

    # ── Tab 4: Risk Audit ──────────────────────────────────────────────────
    with tab4:
        risk = (st.session_state.current_state or {}).get("risk_assessment", {})
        if risk:
            st.markdown("### 🕵️‍♂️ Red Team Analysis: Why this might fail")
            
            r1, r2 = st.columns(2)
            with r1:
                st.error(f"**🏗️ Technical Risk:**\n{risk.get('technical_risk','')}")
                st.error(f"**⚖️ Legal/IP Risk:**\n{risk.get('legal_risk','')}")
            with r2:
                st.error(f"**📈 Market Risk:**\n{risk.get('market_risk','')}")
                st.warning(f"**🛑 Kill-Switch Criteria:**\n{risk.get('kill_switch_criteria','')}")
            
            st.info(f"**🛡️ Survival Strategy:** {risk.get('survival_strategy','')}")
        else:
            st.caption("No risk audit data available.")

    # ── References & Sources ──────────────────────────────────────────────────
    st.markdown("### 📚 References & Sources")
    # Collect all cited URLs from voice_of_customer and selected problem source_refs
    all_refs = []
    for item in dossier.get("voice_of_customer", []):
        url = item.get("url", "")
        if url and url not in [r.get("url") for r in all_refs]:
            all_refs.append({"author": item.get("author", ""), "url": url, "source": item.get("source", "")})
    for ref in sel_prob.get("source_refs", []):
        url = ref.get("url", "")
        if url and url not in [r.get("url") for r in all_refs]:
            all_refs.append({"author": ref.get("author", ""), "url": url, "source": ref.get("title", "")})
    # Also gather raw_sources from session state
    for src in (st.session_state.current_state or {}).get("raw_sources", []):
        url = src.get("url", "")
        if url and url not in [r.get("url") for r in all_refs]:
            all_refs.append({"author": src.get("author", ""), "url": url, "source": src.get("story_title", "")})

    if all_refs:
        for i, ref in enumerate(all_refs, 1):
            st.markdown(f"{i}. [{ref.get('source', 'Source')}]({ref['url']}) — *{ref.get('author', 'Unknown')}*")
    else:
        st.caption("No external references were captured for this scan.")

    st.markdown("---")

    # ── Export ───────────────────────────────────────────────────────────────
    import json
    refs_md = "\n".join([f"- [{r.get('source','')}]({r['url']}) by {r.get('author','')}" for r in all_refs]) if all_refs else "No references."
    export_md = f"""# Founder's Dossier: {p_name}

## Signal Strength
- Mention Count: ~{dossier.get('signal_strength', {}).get('mention_count', '?')} threads
- {dossier.get('signal_strength', {}).get('source_summary', '')}

## Market Gap Score
{json.dumps(dossier.get('market_gap_score', {}), indent=2)}

## Voice of Customer
{chr(10).join(['> "' + q.get('quote','') + '" — @' + q.get('author','') + ' (' + q.get('url','') + ')' for q in dossier.get('voice_of_customer',[])])}

## MVP Blueprint
{json.dumps(dossier.get('mvp_blueprint', {}), indent=2)}

## Competitive Landscape
{json.dumps(dossier.get('competitive_landscape', []), indent=2)}

## Technical Roadmap
{json.dumps(dossier.get('technical_roadmap', {}), indent=2)}

## Monetization
{json.dumps(dossier.get('monetization', {}), indent=2)}

## References
{refs_md}
"""
    col_dl, col_pptx, col_save, col_back, col_new = st.columns(5)
    with col_dl:
        st.download_button(
            label="💾 Markdown",
            data=export_md,
            file_name=f"dossier_{p_name.replace(' ','_').lower()}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col_pptx:
        m_analysis = (st.session_state.current_state or {}).get('market_size_analysis', {})
        r_analysis = (st.session_state.current_state or {}).get('risk_assessment', {})
        pptx_data = generate_pitch_deck(p_name, dossier, m_analysis, r_analysis)
        st.download_button(
            label="📊 Pitch Deck",
            data=pptx_data,
            file_name=f"pitch_deck_{p_name.replace(' ','_').lower()}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True
        )
    with col_save:
        if st.button("🗄️ Archive to Library", use_container_width=True):
            m_url = (st.session_state.current_state or {}).get("mockup_url")
            risk_data = (st.session_state.current_state or {}).get("risk_assessment")
            db.save_dossier(st.session_state.topic, p_name, dossier, p_score, m_url, risk_data)
            st.success("Archived!")
            time.sleep(1)
            st.rerun()
    with col_back:
        if st.button("🔙 Back to Ideas", use_container_width=True):
            # Clear selection-specific state from graph
            graph_app.update_state(config, {
                "selected_problem": {},
                "blueprint": None,
                "market_size_analysis": None,
                "mockup_url": None,
                "risk_assessment": None
            })
            # Reset session state
            st.session_state.selected_problem = None
            if st.session_state.current_state:
                st.session_state.current_state.pop("blueprint", None)
                st.session_state.current_state.pop("market_size_analysis", None)
                st.session_state.current_state.pop("mockup_url", None)
                st.session_state.current_state.pop("risk_assessment", None)
            
            st.session_state.app_stage = "selection"
            st.rerun()
    with col_new:
        if st.button("🔄 New Scan", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("---")
    
    # ── Interactive Strategy Consultant Chat ─────────────────────────────────
    st.markdown("### 💬 Chat with your Strategy Consultant")
    st.caption("Ask follow-up questions about this blueprint, marketing tactics, or technical details.")

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("How should I market this? / What stack is best?"):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Consulting the strategist..."):
                try:
                    from langchain_community.chat_models import ChatOllama
                    from langchain_core.messages import HumanMessage, SystemMessage
                    
                    ollama_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
                    chat_llm = ChatOllama(model="nemotron-3-nano:30b-cloud", base_url=ollama_url)
                    
                    # Context for the AI
                    context = f"""
                    You are an elite AI Startup Consultant. You just generated this Founder's Dossier:
                    PROBLEM: {p_name}
                    BLUEPRINT: {json.dumps(dossier)}
                    MARKET: {json.dumps((st.session_state.current_state or {}).get('market_size_analysis', {}))}
                    RISKS: {json.dumps((st.session_state.current_state or {}).get('risk_assessment', {}))}
                    
                    Answer the user's questions about this specific idea. Be actionable, realistic, and insightful.
                    """
                    
                    messages = [SystemMessage(content=context)]
                    for m in st.session_state.chat_history[-5:]: # Keep last 5 for context
                        if m["role"] == "user":
                            messages.append(HumanMessage(content=m["content"]))
                        else:
                            # Not ideal but works for simple chat
                            messages.append(HumanMessage(content=m["content"])) 
                    
                    response = chat_llm.invoke(messages)
                    assistant_text = response.content
                    
                    st.markdown(assistant_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})
                except Exception as e:
                    st.error(f"Consultant Error: {e}")

# Stage: VIEW ARCHIVE
if st.session_state.app_stage == "view_archive":
    item = st.session_state.archived_dossier
    if not item:
        st.session_state.app_stage = "input"
        st.rerun()
    
    p_name = item['problem_name']
    p_score = item['market_score']
    dossier = json.loads(item['blueprint_json'])
    
    st.markdown(f"### 🗄️ Viewing Archived Dossier: {p_name}")
    
    # Reuse the display logic (Simplified for space)
    st.info(f"Originally created on {item['created_at']}")
    
    # ... (I'll extract the rendering to a function if I had more space, but for now I will just render it)
    # Actually, let's just use the same rendering block but with archived data
    
    score_color = "#00ff87" if p_score >= 75 else ("#ffb347" if p_score >= 50 else "#ff6b6b")

    st.markdown(f"""
    <div style='background:#1e293b;padding:24px;border-radius:14px;border-left:6px solid {score_color};margin-bottom:24px'>
        <div style='font-size:1.6rem;font-weight:800;color:#f8fafc;margin-bottom:8px'>📄 {p_name}</div>
        <span style='background:#334155;color:{score_color};padding:4px 14px;border-radius:20px;font-size:0.95rem;font-weight:700;margin-right:8px'>🔥 Market Score: {p_score}/100</span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 The Insight", "💡 The MVP", "🛠️ The Build", "📉 Risks"])
    
    with tab1:
        st.json(dossier.get("signal_strength", {}))
        st.json(dossier.get("market_gap_score", {}))
    
    with tab2:
        m_url = item.get("mockup_url")
        if m_url:
            st.image(m_url, caption="Archived Visual Mockup", use_container_width=True)
        st.json(dossier.get("mvp_blueprint", {}))
    
    with tab4:
        r_json = item.get("risk_json")
        if r_json:
            st.json(json.loads(r_json))
    
    if st.button("🔙 Back to Main", use_container_width=True):
        st.session_state.app_stage = "input"
        st.rerun()
