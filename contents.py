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
        [data-testid="stSidebarNav"] ul { display: none !important; }
        [data-testid="stSidebarNav"] { display: block !important; }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFF5F7 0%, #FFE4E9 100%) !important;
            border-right: 2px solid #FF99AC;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
            color: #FF4B4B !important;
            font-weight: 800 !important;
            font-size: 1.1rem !important;
        }
        .main-title {
            font-size: 4rem !important;
            font-weight: 900 !important;
            text-align: center;
            background: linear-gradient(45deg, #FF00CC, #3333FF, #00FFCC);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. 统一侧边栏内容
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#FF1493;'>🌈 Spectrum</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # 首页按钮
        if st.button("🏠 首页中心", key="nav_home", use_container_width=True):
            st.session_state.target_page = "Home"
            st.session_state.needs_auth = None
            st.rerun()

        # 灵魂城市按钮
        is_soul_unlocked = st.session_state.get("unlocked_SoulCity", False)
        soul_label = "🌆 灵魂城市测试" + (" ✅" if is_soul_unlocked else " 🔒")
        if st.button(soul_label, key="nav_soul", use_container_width=True):
            if is_soul_unlocked:
                st.session_state.target_page = "SoulCity"
            else:
                st.session_state.needs_auth = "SoulCity"
            st.rerun()

        # 性取向探索按钮
        is_orient_unlocked = st.session_state.get("unlocked_Orientation", False)
        orient_label = "🌈 性取向探索" + (" ✅" if is_orient_unlocked else " 🔒")
        if st.button(orient_label, key="nav_orient", use_container_width=True):
            if is_orient_unlocked:
                st.session_state.target_page = "Orientation"
            else:
                st.session_state.needs_auth = "Orientation"
            st.rerun()

        # --- 🔐 侧边栏专属验证区 ---
        if st.session_state.get("needs_auth"):
            st.markdown("---")
            st.warning(f"正在激活项目")
            # 只有当点击了未解锁项目，才会运行到这里并被 key_check_gate 拦截
            key_check_gate(st.session_state.needs_auth)

        st.markdown("---")
        st.caption("© 2026 Spectrum")
