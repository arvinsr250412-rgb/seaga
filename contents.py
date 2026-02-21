# contents.py
import streamlit as st
from key_system import key_check_gate
def apply_contents_settings():
    # 1. 统一页面配置
    st.set_page_config(page_title="Spectrum", layout="wide")

    # 2. 统一多巴胺 CSS 样式
    st.markdown("""
        <style>

    
                /* 强行隐藏 Streamlit 默认生成的导航项 */
        [data-testid="stSidebarNav"] ul {
            display: none !important;
        }
        
        /* 但要保留侧边栏的顶部空白或其他手动添加的元素 */
        [data-testid="stSidebarNav"] {
            display: block !important;
        }
        /* 侧边栏背景渐变 */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFF5F7 0%, #FFE4E9 100%) !important;
            border-right: 2px solid #FF99AC;
        }
        
        /* 侧边栏导航文字加粗 */
        [data-testid="stSidebarNavItems"] span {
            font-size: 1.1rem !important;
            font-weight: 800 !important;
            color: #FF512F !important;
        }

        /* 主标题渐变效果 */
        .main-title {
            font-size: 4rem !important;
            font-weight: 900 !important;
            text-align: center;
            background: linear-gradient(45deg, #FF00CC, #3333FF, #00FFCC);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        
        /* 副标题样式 */
        .sub-title {
            text-align: center;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            color: #FF66B2;
            letter-spacing: 5px;
            margin-bottom: 30px;
        }

                /* 1. 修改侧边栏所有普通文本和手动 page_link 的文字颜色 */
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span {
            color: #FF4B4B !important; /* 经典多巴胺红色 */
            font-weight: 800 !important;
            font-size: 1.1rem !important;
        }
        
        /* 2. 专门针对 st.page_link 的美化（多巴胺圆角按钮感） */
        [data-testid="stSidebar"] a {
            background-color: rgba(255, 75, 75, 0.05) !important; /* 极淡的底色 */
            border-radius: 15px !important;
            margin: 5px 0 !important;
            transition: all 0.3s ease !important;
        }
        
        /* 3. 悬停效果：文字变色并产生位移，增加互动感 */
        [data-testid="stSidebar"] a:hover {
            background-color: #FF4B4B !important; /* 悬停时背景变红 */
            transform: translateX(5px); /* 轻轻向右滑动 */
        }
        
        [data-testid="stSidebar"] a:hover span {
            color: white !important; /* 悬停时文字变白 */
        }
        
        /* 4. 侧边栏底部的 Caption 文字（版本号等） */
        [data-testid="stSidebar"] .stCaption {
            color: #FF99AC !important; /* 柔和粉色 */
            font-weight: 400 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. 统一侧边栏内容
    # 3. 统一侧边栏内容
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#FF1493;'>🌈 Spectrum</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # --- 🚀 核心修改：导航逻辑 ---
        
        # 首页通常不需要密钥，直接跳转
        if st.button("🏠 首页中心", use_container_width=True):
            st.switch_page("main.py")

        st.markdown("<br>", unsafe_allow_html=True)

        # 🌆 灵魂城市测试
        if st.button("🌆 灵魂城市测试", use_container_width=True):
            st.session_state.pending_target = "pages/01_🌆_灵魂城市.py"
            st.session_state.target_id = "soul_city_v1" # 密钥系统识别ID

        # 🌈 性取向探索
        if st.button("🌈 性取向探索", use_container_width=True):
            st.session_state.pending_target = "pages/02_🌈_性取向探索.py"
            st.session_state.target_id = "sexual_orientation_v1"

        # --- 🔐 密钥拦截层 ---
        # 如果用户点击了某个测试（即 pending_target 有值）
        if "pending_target" in st.session_state and st.session_state.pending_target:
            # 只有当用户还没解锁这个特定测试时，才触发门禁
            unlock_key = f"unlocked_{st.session_state.target_id}"
            if not st.session_state.get(unlock_key, False):
                # 召唤门禁
                key_check_gate(st.session_state.target_id)
            
            # 如果程序能运行到这里，说明 key_check_gate 通过了（或已经解锁）
            target = st.session_state.pending_target
            # 清除意向，防止死循环刷新
            st.session_state.pending_target = None 
            st.switch_page(target)

        st.markdown("---")
        st.caption("© 2026 Spectrum")
