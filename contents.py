# contents.py
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
   with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#FF1493;'>🌈 Spectrum</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # 1. 首页按钮 (不需要密钥)
        if st.button("🏠 首页中心", use_container_width=True):
            st.session_state.target_page = "Home"
            st.session_state.needs_auth = None # 切换页面时清除验证状态
            st.rerun()

        # 2. 🌆 灵魂城市测试按钮
        is_soul_unlocked = st.session_state.get("unlocked_SoulCity", False)
        btn_label = "🌆 灵魂城市测试" + (" ✅" if is_soul_unlocked else " 🔒")
        if st.button(btn_label, use_container_width=True):
            if is_soul_unlocked:
                st.session_state.target_page = "SoulCity"
            else:
                st.session_state.needs_auth = "SoulCity" # 标记需要验证
            st.rerun()

        # 3. 🌈 性取向探索按钮
        is_orient_unlocked = st.session_state.get("unlocked_Orientation", False)
        btn_label_2 = "🌈 性取向探索" + (" ✅" if is_orient_unlocked else " 🔒")
        if st.button(btn_label_2, use_container_width=True):
            if is_orient_unlocked:
                st.session_state.target_page = "Orientation"
            else:
                st.session_state.needs_auth = "Orientation"
            st.rerun()

        # --- 🔐 侧边栏专属验证区 ---
        if st.session_state.get("needs_auth"):
            st.markdown("---")
            st.warning(f"请在下方激活项目")
            # 这里调用密钥系统
            # 注意：因为 key_check_gate 内部有 st.stop()，它会在这里拦截
            # 只有当 key_check_gate 返回 True（已解锁）时，才会继续往下走
            if key_check_gate(st.session_state.needs_auth):
                st.session_state.target_page = st.session_state.needs_auth
                st.session_state.needs_auth = None
                st.rerun()

        st.markdown("---")
        st.caption("© 2026 Spectrum")
