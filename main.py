import streamlit as st
import json
import requests
import base64
import uuid
import pandas as pd
from contents import apply_contents_settings
from key_system import key_check_gate # 确保你已经修复了路径导入问题

# 应用统一配置和侧边栏
apply_contents_settings()

# --- 1. 页面配置 ---
st.set_page_config(page_title="Spectrum", page_icon="💥", layout="centered")

# --- 2. 多巴胺风格 CSS 大爆炸 ---
st.markdown("""
    <style>
    /* 引入更粗犷的潮流字体 */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;900&display=swap');

    :root {
        /* 定义多巴胺主题色变量 */
        --dopamine-gradient: linear-gradient(135deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%);
        --electric-gradient: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        --sunny-gradient: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        --text-primary: #2D3748; /* 深而不黑，更有质感 */
    }

    /* 全局设定 */
    .stApp { 
        background-color: #ffffff !important; /* 保持背景纯白，让色彩跳出来 */
        font-family: 'Poppins', sans-serif;
    }
    
    /* 强制提升所有文字的基础大小和颜色 */
    .stApp, .stMarkdown, p, span, label, li { 
        color: var(--text-primary) !important;
        font-size: 1.2rem !important; /* 正文变大 */
        line-height: 1.7 !important;
    }
    h1, h2, h3, h4 {
        color: var(--text-primary) !important;
        font-weight: 900 !important; /* 标题极粗 */
        letter-spacing: -1px;
    }

    /* --- 巨大的博客主标题 Hero Section --- */
    .hero-container {
        text-align: center;
        padding: 4rem 0 2rem 0;
    }
    .hero-title {
        font-size: 6rem !important; /* 超大标题 */
        line-height: 1.1;
        font-weight: 900;
        /* 使用极其鲜艳的夕阳红渐变 */
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 6px rgba(255, 126, 95, 0.2); /* 增加立体感 */
    }
    .hero-subtitle {
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #FF6A88 !important; /* 鲜艳的副标题色 */
    }

    /* --- 多巴胺糖果卡片 --- */
    .blog-card {
        background: #ffffff;
        padding: 3rem; /* 更大的内边距 */
        border-radius: 30px; /* 更圆润 */
        /* 使用 CSS Trick 实现渐变色边框 */
        position: relative;
        background-clip: padding-box;
        border: 5px solid transparent; /* 边框变粗 */
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 40px rgba(255, 106, 136, 0.15); /* 彩色光晕阴影 */
        transition: all 0.4s ease;
    }
    /* 给卡片加一个伪元素背景来实现渐变边框 */
    .blog-card::before {
        content: '';
        position: absolute;
        top: 0; right: 0; bottom: 0; left: 0;
        z-index: -1;
        margin: -5px; /* 与边框宽度匹配 */
        border-radius: inherit;
        background: var(--dopamine-gradient);
    }
    .blog-card:hover {
        transform: translateY(-10px) scale(1.02); /* 悬停时弹起更明显 */
        box-shadow: 0 30px 60px rgba(255, 106, 136, 0.3);
    }

    /* 卡片内的Emoji标题 */
    .card-emoji-title {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    /* --- 糖果按钮 --- */
    div.stButton > button {
        /* 彻底改变按钮风格为实体渐变 */
        background-image: linear-gradient(to right, #FF512F 0%, #DD2476 51%, #FF512F 100%) !important;
        background-size: 200% auto !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important; /* 药丸形状 */
        padding: 1rem 2.5rem !important; /* 更大更胖 */
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        box-shadow: 0 10px 20px rgba(221, 36, 118, 0.3) !important;
        transition: 0.5s !important;
    }
    div.stButton > button:hover {
        background-position: right center !important; /* 鼠标悬停时渐变流动 */
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(221, 36, 118, 0.5) !important;
    }

    /* --- 侧边栏与输入框微调 --- */
    [data-testid="stSidebar"] {
        background-color: #fff0f5; /* 侧边栏也用淡粉色背景 */
        border-right: none;
    }
    .stTextInput input {
        border-radius: 15px !important;
        border: 2px solid #FF99AC !important;
        padding: 1rem !important;
    }
        /* 隐藏输入框下方的 "Press enter to apply" 提示 */
    [data-testid="InputInstructions"] {
        display: none !important;
    }
    
    /* 针对特定手机端可能出现的提示进行二次隐藏 */
    .stTextInput small {
        display: none !important;
    }
     /* --- 柔和多巴胺输入框定制 --- */
    
    /* --- 彻底移除所有黑边的多巴胺输入框 --- */
    
    /* 1. 针对输入框本身：移除所有外轮廓 */
    .stTextInput input {
        border: 2px solid #FFD8A8 !important; /* 奶油橙边框 */
        background-color: #FFF9F2 !important;
        color: #FF8B3D !important;
        border-radius: 16px !important;
        box-shadow: none !important;
        outline: none !important; /* 核心：移除点击时的黑色外圈 */
    }
    
    /* 2. 针对点击状态：确保点击时没有任何系统强制的边框 */
    .stTextInput input:focus {
        border-color: #FFA94D !important;
        box-shadow: 0 0 10px rgba(255, 169, 77, 0.2) !important; /* 柔和橙光 */
        outline: none !important;
        -webkit-box-shadow: 0 0 10px rgba(255, 169, 77, 0.2) !important;
    }
    
    /* 3. 核心修改：移除 Streamlit 输入框外部容器的黑色投影和边框 */
    div[data-baseweb="input"] {
        border: none !important;
        outline: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }
    
    /* 4. 针对密码可见性按钮：移除点击时的黑色焦点方框 */
    .stTextInput button {
        outline: none !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* 5. 确保在输入时没有底部的蓝色或黑色装饰线（某些版本 Streamlit 的特征） */
    div[data-testid="stTextInput"] div::after {
        display: none !important;
    }
        /* --- 1. 彻底斩断 Expander (管理员入口) 的黑边 --- */
    [data-testid="stExpander"] {
        border: none !important; /* 移除外边框 */
        box-shadow: none !important;
        background-color: transparent !important;
    }
    
    [data-testid="stExpander"] summary {
        border: none !important; /* 移除折叠头部边框 */
        outline: none !important;
        color: #FF9F43 !important; /* 让标题也变橙色 */
    }
    
    /* 移除折叠框展开后的内容区边框 */
    [data-testid="stExpanderDetails"] {
        border: none !important;
        padding-top: 0 !important;
    }
    
    /* --- 2. 彻底移除输入框的所有包裹层边框 --- */
    
    /* 针对 BaseWeb 容器层 */
    div[data-baseweb="input"], 
    div[data-baseweb="base-input"] {
        border: none !important;
        outline: none !important;
        background-color: transparent !important;
    }
    
    /* 针对 Streamlit 内部多层 div 的边框清除 */
    div[data-testid="stTextInput"] > div {
        border: none !important;
        box-shadow: none !important;
    }
    
    /* 再次强化输入框本身，确保没有任何残留 */
    .stTextInput input {
        border: 2px solid #FFD8A8 !important; /* 只有这根奶油橙边框 */
        outline: 0 !important;
        box-shadow: none !important;
        -webkit-appearance: none !important;
    }
    
    /* 点击时的状态 */
    .stTextInput input:focus {
        outline: none !important;
        border-color: #FFA94D !important;
        box-shadow: 0 0 10px rgba(255, 169, 77, 0.2) !important;
    }
    
    /* --- 3. 移除侧边栏可能存在的默认线条 --- */
    [data-testid="stSidebar"] hr {
        border-top: 1px solid #FFD8A8 !important; /* 把黑线分割线换成奶油橙 */
        opacity: 0.3;
    }

        /* 1. 强制所有交互状态背景透明，移除所有边框和阴影 */
        [data-testid="stExpander"], 
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary:hover,
        [data-testid="stExpander"] summary:focus,
        [data-testid="stExpander"] summary:active,
        [data-testid="stExpander"] summary:focus-visible,
        [data-testid="stExpander"]:focus-within summary,
        [data-testid="stExpander"] summary div[role="button"] {
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            background-color: transparent !important;
            background: transparent !important;
            transition: all 0.3s ease;
        }
    
        /* 2. 移除展开后内容区的任何边框 */
        [data-testid="stExpanderDetails"] {
            border: none !important;
            padding-top: 0 !important;
        }
    
        /* 3. 保持管理员入口文字颜色始终为多巴胺橙 */
        [data-testid="stExpander"] summary p {
            color: #FF9F43 !important;
            font-weight: 800 !important;
        }
    
        /* 4. 可选：增加一个微小的文字缩放反馈，代替生硬的黑框 */
        [data-testid="stExpander"] summary:hover p {
            color: #FF6B35 !important;
            transform: scale(1.02);
        }
        /* --- 将数字输入框（生成数量、可用次数）的文字改为黑色 --- */
    
        /* 锁定数字输入框的 input 元素 */
        .stNumberInput input {
            color: #000000 !important; /* 纯黑色 */
            -webkit-text-fill-color: #000000 !important; /* 确保兼容性 */
            font-weight: 700 !important; /* 加粗一点更清晰 */
        }
    
        /* 如果你希望侧边栏的账号密码输入框文字还是橙色，但后台的变黑，
           可以使用这个更精准的选择器 */
        [data-testid="stSidebar"] .stTextInput input {
            color: #FF8B3D !important; /* 侧边栏保持柔和橙 */
        }
    
        div.stNumberInput div[data-baseweb="input"] {
            background-color: #ffffff !important; /* 背景改白，黑字更显眼 */
            border: 2px solid #FFD8A8 !important; /* 保持奶油橙边框 */
        }
            /* 针对清理按钮的特殊颜色（可选：青蓝色系，与制造按钮区分开） */
        /* 如果想完全一样，则不需要加这段 */
        div.stButton > button:contains("清理") {
            background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%) !important;
            box-shadow: 0 10px 20px rgba(79, 172, 254, 0.3) !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. 登录与后台逻辑 (保持不变) ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
REPO_OWNER = "arvinsr250412-rgb"
REPO_NAME = "seaga"
FILE_PATH = "keys.json"
ADMIN_USER = "arvin"
ADMIN_PWD = "Srbm1121"

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
    payload = {"message": "Update keys", "content": encoded_content}
    if sha: payload["sha"] = sha
    r = requests.put(url, headers=headers, json=payload)
    return r.status_code in [200, 201]

# --- 4. 侧边栏逻辑 ---
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

with st.sidebar:
    st.markdown("<h2 style='text-align:center; font-size:2rem;'>🍭 控制台</h2>", unsafe_allow_html=True)
    if not st.session_state.admin_logged_in:
        with st.expander("🔐 管理员入口"):
            u = st.text_input("账号")
            p = st.text_input("密码", type="password")
            if st.button("💥 登录后台", use_container_width=True):
                if u == ADMIN_USER and p == ADMIN_PWD:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else: st.error("验证失败")
    else:
        st.success("✨ 管理员在线 ✨")
        if st.button("👋 退出登录", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()

# --- 5. 页面渲染逻辑 ---

if st.session_state.admin_logged_in:
    # --- 后台 (也稍微沾点多巴胺风格) ---
    st.markdown("<h1 class='hero-title' style='font-size:4rem !important;'>Admin Panel 🚀</h1>", unsafe_allow_html=True)
    db, sha = get_keys_from_github()
    
    with st.container():
        st.markdown("""<div class='blog-card'><h2>🔑 密钥工厂</h2>""", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: count = st.number_input("生成数量", 1, 10, 1)
        with col2: uses = st.number_input("可用次数", 1, 10, 2)
        st.write("")
        if st.button("🎉 立即制造密钥"):
            for _ in range(count): db[str(uuid.uuid4()).upper()[:8]] = uses
            if update_keys_to_github(db, sha):
                st.success("云端同步成功！")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("🧹 清除已用完密钥", use_container_width=True):
                # 过滤掉次数为 0 的密钥
                filtered_db = {k: v for k, v in db.items() if v > 0}
                removed_count = len(db) - len(filtered_db)
                
                if removed_count > 0:
                    if update_keys_to_github(filtered_db, sha):
                        st.success(f"已成功清理 {removed_count} 个失效密钥！")
                        st.rerun()
                    else:
                        st.error("云端同步失败，请重试")
                else:
                    st.info("目前没有已用完的密钥哦~")
    if db:
        st.divider()
        st.dataframe(pd.DataFrame(list(db.items()), columns=['Key', 'Remaining']), use_container_width=True)

else:
    # --- 主界面 (多巴胺博客风格) ---
    
    # 1. 巨大的 Hero 标题区
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">SPECTRUM.</h1>
            <p class="hero-subtitle">🦄 探索潜意识的游乐场 ✨</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. 置顶博文风格的欢迎卡片
    st.markdown("""
        <div class="blog-card" style="text-align:center;">
            <div class="card-emoji-title">🚀</div>
            <h2 style="font-size: 2.5rem; margin-bottom: 1rem;">准备好起飞了吗？</h2>
            <p style="font-size: 1.4rem;">这里没有枯燥的问卷。我们收集了最酷、最有趣的性格探索工具，用算法解构你未知的另一面。</p>
            <br>
            <p style="font-weight: 900; color: #FF6A88; font-size: 1.3rem;">👇 快看左侧菜单选择一个项目！</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("") # 间距

    # 3. 博客特色区 (使用 Emoji 和大字体)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div style="text-align:center; padding: 1rem;">
                <span style="font-size: 4rem;">🧠</span>
                <h3>深度分析</h3>
                <p>不只是娱乐，背后是科学模型支撑。</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style="text-align:center; padding: 1rem;">
                <span style="font-size: 4rem;">🎨</span>
                <h3>视觉盛宴</h3>
                <p>沉浸在色彩与交互的愉悦体验中。</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div style="text-align:center; padding: 1rem;">
                <span style="font-size: 4rem;">🔥</span>
                <h3>阅后即焚</h3>
                <p>密钥机制确保你的探索绝对私密。</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    
    # 4. 大图展示 (增加圆角和彩色投影)
    st.markdown("""
        <div style="border-radius: 30px; overflow: hidden; box-shadow: 0 20px 50px rgba(255, 126, 95, 0.4);">
            <img src="https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80" width="100%">
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='text-align:center; font-weight:bold; color:#FF6A88;'>© 2026 Spectrum | Stay Colorful.</p>", unsafe_allow_html=True)
























