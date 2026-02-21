import streamlit as st
import sys
import os
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

        /* 保留侧边栏容器 */
        [data-testid="stSidebarNav"] {
            display: block !important;
        }

        /* 侧边栏背景渐变 */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFF5F7 0%, #FFE4E9 100%) !important;
            border-right: 2px solid #FF99AC;
        }

        /* 侧边栏导航文字美化 */
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span {
            color: #FF4B4B !important;
            font-weight: 800 !important;
            font-size: 1.1rem !important;
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

        /* 侧边栏底部 Caption */
        [data-testid="stSidebar"] .stCaption {
            color: #FF99AC !important;
            font-weight: 400 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. 统一侧边栏内容 (修复缩进)
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#FF1493;'>🌈 Spectrum</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # 1. 首页按钮
        if st.button("🏠 首页中心", key="btn_home", use_container_width=True):
            st.session_state.target_page = "Home"
            st.session_state.needs_auth = None
            st.rerun()

        # 2. 🌆 灵魂城市测试按钮
        is_soul_unlocked = st.session_state.get("unlocked_SoulCity", False)
        soul_label = "🌆 灵魂城市测试" + (" ✅" if is_soul_unlocked else " 🔒")
        if st.button(soul_label, key="btn_soul", use_container_width=True):
            if is_soul_unlocked:
                st.session_state.target_page = "SoulCity"
            else:
                st.session_state.needs_auth = "SoulCity"
            st.rerun()

        # 3. 🌈 性取向探索按钮
        is_orient_unlocked = st.session_state.get("unlocked_Orientation", False)
        orient_label = "🌈 性取向探索" + (" ✅" if is_orient_unlocked else " 🔒")
        if st.button(orient_label, key="btn_orient", use_container_width=True):
            if is_orient_unlocked:
                st.session_state.target_page = "Orientation"
            else:
                st.session_state.needs_auth = "Orientation"
            st.rerun()

        # --- 🔐 侧边栏专属验证区 ---
        if st.session_state.get("needs_auth"):
            st.markdown("---")
            st.warning(f"请在下方激活项目")
            
            # 调用 key_system.py 中的门禁函数
            # 注意：key_check_gate 内部包含 st.stop()，会在此处拦截
            if key_check_gate(st.session_state.needs_auth):
                st.session_state.target_page = st.session_state.needs_auth
                st.session_state.needs_auth = None
                st.rerun()

        st.markdown("---")
        st.caption("© 2026 Spectrum")
