import streamlit as st
import json
import requests
import base64
import uuid
import pandas as pd
from contents import apply_contents_settings

# --- 1. 页面配置 (必须是 Streamlit 命令的第一条) ---
st.set_page_config(page_title="Spectrum", page_icon="💥", layout="wide")

# --- 2. 初始化 Session State ---
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "target_page" not in st.session_state:
    st.session_state.target_page = "Home"

if "needs_auth" not in st.session_state:
    st.session_state.needs_auth = None

# --- 3. 应用统一配置与侧边栏 (包含所有拦截逻辑) ---
apply_contents_settings()

# --- 4. 多巴胺风格 CSS 全局注入 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;900&display=swap');
    :root {
        --dopamine-gradient: linear-gradient(135deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%);
        --text-primary: #2D3748;
    }
    .stApp { background-color: #ffffff !important; font-family: 'Poppins', sans-serif; }
    .stApp, .stMarkdown, p, span, label, li { color: var(--text-primary) !important; font-size: 1.1rem !important; }
    h1, h2, h3 { font-weight: 900 !important; letter-spacing: -1px; }

    /* Hero Section */
    .hero-container { text-align: center; padding: 2rem 0; }
    .hero-title {
        font-size: 5rem !important;
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-subtitle { font-size: 1.5rem !important; color: #FF6A88 !important; font-weight: 700; }

    /* 多巴胺卡片 */
    .blog-card {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 30px;
        position: relative;
        background-clip: padding-box;
        border: 5px solid transparent;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(255, 106, 136, 0.1);
    }
    .blog-card::before {
        content: ''; position: absolute; top: 0; right: 0; bottom: 0; left: 0;
        z-index: -1; margin: -5px; border-radius: inherit;
        background: var(--dopamine-gradient);
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. 管理员专属函数 (对接 GitHub) ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
REPO_OWNER = "arvinsr250412-rgb"
REPO_NAME = "seaga"
FILE_PATH = "keys.json"

def get_keys_from_github():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            content = r.json()
            return json.loads(base64.b64decode(content['content']).decode('utf-8')), content['sha']
    except: pass
    return {}, None

def update_keys_to_github(new_data, sha=None):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    encoded_content = base64.b64encode(json.dumps(new_data, indent=4).encode('utf-8')).decode('utf-8')
    payload = {"message": "Admin update", "content": encoded_content}
    if sha: payload["sha"] = sha
    r = requests.put(url, headers=headers, json=payload)
    return r.status_code in [200, 201]

# --- 6. 页面分发路由 ---

# 页面 A: 管理员后台
if st.session_state.target_page == "Admin" and st.session_state.admin_logged_in:
    st.markdown("<h1 class='hero-title' style='font-size:3.5rem !important;'>Admin Panel 🚀</h1>", unsafe_allow_html=True)
    db, sha = get_keys_from_github()
    
    with st.container():
        st.markdown("<div class='blog-card'><h2>🔑 密钥工厂</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: count = st.number_input("生成数量", 1, 20, 5)
        with col2: uses = st.number_input("可用次数", 1, 100, 1)
        
        if st.button("🎉 立即制造批量密钥", use_container_width=True):
            for _ in range(count):
                db[str(uuid.uuid4()).upper()[:8]] = uses
            if update_keys_to_github(db, sha):
                st.success("密钥已同步至云端！")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if db:
        st.markdown("### 📊 实时库状态")
        df = pd.DataFrame(list(db.items()), columns=['Key', 'Remaining'])
        st.dataframe(df, use_container_width=True, height=400)
        if st.button("🧹 清理失效密钥", use_container_width=True):
            new_db = {k: v for k, v in db.items() if v > 0}
            update_keys_to_github(new_db, sha)
            st.rerun()

# 页面 B: 灵魂城市测试 (示例)
elif st.session_state.target_page == "SoulCity":
    st.markdown("<h1 class='hero-title' style='font-size:3.5rem !important;'>Soul City 🌆</h1>", unsafe_allow_html=True)
    st.markdown("<div class='blog-card'><h3>欢迎来到灵魂中心</h3><p>测试题目正在加载...</p></div>", unsafe_allow_html=True)
    if st.button("⬅️ 返回首页"):
        st.session_state.target_page = "Home"
        st.rerun()

# 页面 C: 性取向探索 (示例)
elif st.session_state.target_page == "Orientation":
    st.markdown("<h1 class='hero-title' style='font-size:3.5rem !important;'>Spectrum 🌈</h1>", unsafe_allow_html=True)
    st.markdown("<div class='blog-card'><h3>探索你的色彩</h3><p>深度解构模块准备就绪。</p></div>", unsafe_allow_html=True)
    if st.button("⬅️ 返回首页"):
        st.session_state.target_page = "Home"
        st.rerun()

# 默认页面: 首页
else:
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">SPECTRUM.</h1>
            <p class="hero-subtitle">🦄 探索潜意识的游乐场 ✨</p>
        </div>
        <div class="blog-card" style="text-align:center;">
            <h2 style="font-size: 2.2rem;">准备好起飞了吗？</h2>
            <p>这里没有枯燥的问卷。选择左侧项目并激活，开启你的探索。</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    features = [("🧠", "深度分析"), ("🎨", "视觉盛宴"), ("🔥", "阅后即焚")]
    for col, (icon, text) in zip([col1, col2, col3], features):
        with col:
            st.markdown(f"<div style='text-align:center;'><span style='font-size:3rem;'>{icon}</span><h4>{text}</h4></div>", unsafe_allow_html=True)

    st.markdown("<br><div style='border-radius:30px; overflow:hidden; box-shadow:0 15px 40px rgba(0,0,0,0.1);'><img src='https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1200' width='100%'></div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; opacity:0.6;'>© 2026 Spectrum | Stay Colorful.</p>", unsafe_allow_html=True)





















