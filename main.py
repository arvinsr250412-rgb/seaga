import streamlit as st
import json
import requests
import base64
import uuid
import pandas as pd

# --- 1. 页面配置 ---
st.set_page_config(page_title="我的测试集合", page_icon="✨", layout="centered")

# --- 2. 配置信息 (请在此处填入你的 GitHub 信息) ---
# 建议在 Streamlit Cloud 的 Secrets 中设置，而不是直接写在代码里
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "你的_GITHUB_TOKEN")
REPO_OWNER = "arvinsr250412-rgb"
REPO_NAME = "seaga"
FILE_PATH = "keys.json"

# 管理员账号
ADMIN_USER = "arvin"
ADMIN_PWD = "Srbm1121"

# --- 3. 样式美化 (Spectrum 风格) ---
st.markdown("""
    <style>
    /* 1. 强制全局正文文字、标签、Markdown 颜色为深色 */
    .stApp, .stMarkdown, p, span, label, h1, h2, h3 {
        color: #1f2937 !important; 
    }

    /* 2. 专门针对单选框（st.radio）的选项文字 */
    div[data-testid="stRadio"] label p {
        color: #1f2937 !important;
    }

    /* 3. 如果你使用了白色卡片，确保里面的文字也是深色 */
    .white-quiz-card, .glass-card {
        color: #1f2937 !important;
    }
    
    /* 4. 针对输入框的文字颜色 */
    .stTextInput input {
        color: #1f2937 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. GitHub API 逻辑 ---
def get_keys_from_github():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = r.json()
        decoded_data = base64.b64decode(content['content']).decode('utf-8')
        return json.loads(decoded_data), content['sha']
    return {}, None

def update_keys_to_github(new_data, sha=None):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    json_content = json.dumps(new_data, indent=4, ensure_ascii=False)
    encoded_content = base64.b64encode(json_content.encode('utf-8')).decode('utf-8')
    payload = {"message": "Update keys database", "content": encoded_content}
    if sha: payload["sha"] = sha
    r = requests.put(url, headers=headers, json=payload)
    return r.status_code in [200, 201]

# --- 5. 管理员功能模块 ---
def admin_panel():
    st.markdown("### 🔐 密钥管理后台")
    db, sha = get_keys_from_github()
    
    with st.expander("➕ 生成新密钥", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            count = st.number_input("生成数量", 1, 10, 1)
        with col2:
            uses = st.number_input("初始次数", 1, 10, 2)
        if st.button("立即生成并同步", use_container_width=True):
            for _ in range(count):
                new_key = str(uuid.uuid4()).upper()[:8]
                db[new_key] = uses
            if update_keys_to_github(db, sha):
                st.success("GitHub 数据库已更新！")
                st.rerun()

    if db:
        st.markdown("#### 当前有效密钥")
        df = pd.DataFrame(list(db.items()), columns=['密钥', '剩余次数'])
        st.dataframe(df, use_container_width=True)
        if st.button("清理次数已耗尽密钥"):
            db = {k: v for k, v in db.items() if v > 0}
            update_keys_to_github(db, sha)
            st.rerun()

# --- 6. 主界面逻辑 ---
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

# 侧边栏登录
with st.sidebar:
    st.markdown("### 🛠️ 系统管理")
    if not st.session_state.admin_logged_in:
        with st.expander("管理员登录"):
            u = st.text_input("账号")
            p = st.text_input("密码", type="password")
            if st.button("进入后台"):
                if u == ADMIN_USER and p == ADMIN_PWD:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("拒绝访问")
    else:
        st.info("已进入管理模式")
        if st.button("退出管理"):
            st.session_state.admin_logged_in = False
            st.rerun()

# 主页面显示
if st.session_state.admin_logged_in:
    admin_panel()
else:
    # 这里是你原来的主界面内容，包装在玻璃卡片里
    st.markdown('<div class="main-title">🌟 欢迎来到我的测试实验室</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        这里收集了我制作的所有趣味测试。<br>
        请从<b>左侧边栏</b>选择你想进行的测试项目！
    </div>
    """, unsafe_allow_html=True)

    st.info("👈 点击左侧菜单开始探索")

    # 你的介绍图片
    st.image("https://images.unsplash.com/photo-1518349619113-03114f06ac3a?auto=format&fit=crop&w=800&q=80", use_container_width=True)
    
    st.markdown("---")
    st.caption("© 2026 测试实验室 | 探索未知的自己")


