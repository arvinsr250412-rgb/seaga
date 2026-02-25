import streamlit as st
from key_system import key_check_gate

# 管理员固定凭据 (建议后续移至 st.secrets)
ADMIN_USER = "arvin"
ADMIN_PWD = "Srbm1121"

def apply_contents_settings():
    # 1. 统一多巴胺 CSS 样式 (保留并优化)
    st.markdown("""
        <style>
        /* 隐藏默认导航 */
        [data-testid="stSidebarNav"] ul { display: none !important; }
        [data-testid="stSidebarNav"] { display: block !important; }

        /* 侧边栏背景：粉嫩多巴胺渐变 */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFF5F7 0%, #FFE4E9 100%) !important;
            border-right: 2px solid #FF99AC;
        }

        /* 侧边栏文字全局样式 */
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span {
            color: #FF4B4B !important;
            font-weight: 800 !important;
            font-size: 1.05rem !important;
        }

        /* 移除 Expander 的默认黑边 (管理员入口样式) */
        [data-testid="stExpander"] {
            border: none !important;
            box-shadow: none !important;
            background-color: transparent !important;
        }
        [data-testid="stExpander"] summary {
            outline: none !important;
            color: #FF9F43 !important;
        }

        /* 输入框聚焦时的光晕效果 */
        .stTextInput input:focus {
            border-color: #FF6A88 !important;
            box-shadow: 0 0 10px rgba(255, 106, 136, 0.2) !important;
        }
        
        /* 侧边栏按钮微调 */
        [data-testid="stSidebar"] .stButton > button {
            border-radius: 20px !important;
            font-weight: 700 !important;
        }
        div[data-baseweb="input"], 
        div[data-baseweb="base-input"],
        .stTextInput input,
        .stPasswordInput input {
            background-color: #FFF9F2 !important; /* 奶油底色，拒绝黑色 */
            color: #FF8B3D !important;            /* 多巴胺橙色文字 */
            -webkit-text-fill-color: #FF8B3D !important;
            border: 2px solid #FFD8A8 !important;
        }

        /* 2. 强制侧边栏未选中按钮的样式（拒绝黑字/黑背景） */
        [data-testid="stSidebar"] .stButton > button {
            background-color: #ffffff !important;
            border: 2px solid #FFE4E9 !important;
        }
        
        /* 强制侧边栏按钮里面的文字颜色 */
        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button span {
            color: #FF6A88 !important; 
            font-weight: 800 !important;
        }

        /* 侧边栏按钮悬停效果 */
        [data-testid="stSidebar"] .stButton > button:hover {
            border-color: #FF99AC !important;
            background-color: #FFF0F5 !important;
        }
        /* 新增：移除悬停黑框 */
        [data-testid="stSidebarNav"] ul li div:hover {
            background-color: rgba(255, 255, 255, 0.5) !important; /* 或者完全 transparent */
            border-radius: 10px;
        }

        /* 新增：移除 Press Enter 提示 */
        div[data-testid="InputInstructions"] {
            visibility: hidden;
        }

        /* 移除管理员入口点击后的高亮 */
        .st-emotion-cache-16idsys p {
            background: none !important;
        }
                 /* --- 彻底移除管理员入口 (st.expander) 的所有背景与边框 --- */
        
        
                /* 1. 移除外层容器边框 */
        [data-testid="stExpander"] {
            border: none !important;
            box-shadow: none !important;
            background-color: transparent !important;
        }
        /* 2. 移除点击、悬停、聚焦时的所有背景色 (核心：针对 summary 标签) */
        [data-testid="stExpander"] summary, 
        [data-testid="stExpander"] summary:hover, 
        [data-testid="stExpander"] summary:focus, 
        [data-testid="stExpander"] summary:active {
            background-color: transparent !important;
            background: transparent !important;
            color: #FF9F43 !important; /* 保持你的多巴胺橙色 */
            outline: none !important;
            box-shadow: none !important;
        }
        
        /* 3. 移除鼠标移开后可能残留的黑色/灰色高亮矩形 (Emotion Cache 覆盖) */
        [data-testid="stExpander"] summary:focus-visible {
            background-color: transparent !important;
            box-shadow: none !important;
        }
        
        /* 4. 针对 Expander 内部展开后的容器内容也做透明处理 */
        [data-testid="stExpander"] [data-testid="stVerticalBlock"] {
            background-color: transparent !important;
            border: none !important;
        }
        
        /* 5. 针对侧边栏导航按钮点击后的残留黑影（你原本代码的补充） */
        div[role="button"]:focus, 
        div[role="button"]:active,
        .st-emotion-cache-16idsys:focus:not(:active) {
            background-color: transparent !important;
            box-shadow: none !important;
            outline: none !important;
        }
        
        /* 6. 隐藏输入框下方的指令 (Press Enter to apply) */
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. 侧边栏内容构建
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#FF1493;'>🌈 Spectrum</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # 获取管理员状态
        is_admin = st.session_state.get("admin_logged_in", False)
        
        # --- 1. 定义锁屏函数 (注意缩进) ---
        def reset_and_lock_all():
            """销毁所有测试记录、重置进度、强制上锁"""
            # 1. 定义需要清理的变量名（请根据你 food_test.py 里的实际变量名调整）
            keys_to_clear = [
                'dish_step',      # 题目进度
                'needs_auth',     # 正在进行的验证状态
                'unlocked_SoulCity', 
                'unlocked_Orientation', 
                'unlocked_FoodTest'
            ]
            
            # 2. 执行清理
            for key in keys_to_clear:
                if key in st.session_state:
                    # 特殊处理：如果是布尔值锁，设为 False；如果是进度，设为 0
                    if "unlocked" in key:
                        st.session_state[key] = False
                    else:
                        st.session_state[key] = None if key == 'needs_auth' else 0
        
            # 3. 强制清除可能残存的结果（如果有直接存结果变量）
            if 'result_dish' in st.session_state:
                del st.session_state['result_dish']

        # --- 2. 导航菜单 ---
        
        # A. 首页按钮
        if st.button("🏠 首页中心", key="btn_home", use_container_width=True):
            reset_and_lock_all()
            st.session_state.target_page = "Home"
            st.session_state.needs_auth = None
            st.rerun()

        # B. 灵魂城市按钮
        is_soul_unlocked = st.session_state.get("unlocked_SoulCity", False) or is_admin
        soul_label = "🌆 灵魂城市测试" + (" ✅" if is_soul_unlocked else " 🔒")
        
        if st.button(soul_label, key="btn_soul", use_container_width=True):
            if is_soul_unlocked:
                st.session_state.target_page = "SoulCity"
                st.session_state.needs_auth = None
            else:
                reset_and_lock_all()
                st.session_state.needs_auth = "SoulCity"
            st.rerun()

        # C. 性取向探索按钮
        is_orient_unlocked = st.session_state.get("unlocked_Orientation", False) or is_admin
        orient_label = "🌈 性取向探索" + (" ✅" if is_orient_unlocked else " 🔒")
        
        if st.button(orient_label, key="btn_orient", use_container_width=True):
            if is_orient_unlocked:
                st.session_state.target_page = "Orientation"
                st.session_state.needs_auth = None
            else:
                reset_and_lock_all()
                st.session_state.needs_auth = "Orientation"
            st.rerun()

        # D. 灵魂味觉测试按钮
        is_food_unlocked = st.session_state.get("unlocked_FoodTest", False) or is_admin
        food_label = "🍲 测测你是哪盘菜" + (" ✅" if is_food_unlocked else " 🔒")
        
        if st.button(food_label, key="btn_food", use_container_width=True):
            if is_food_unlocked:
                st.session_state.target_page = "FoodTest"
                st.session_state.needs_auth = None
            else:
                reset_and_lock_all()
                # 这里不要调用 lock_all()，直接设置需要认证的目标
                st.session_state.needs_auth = "FoodTest" 
                # 同时可以把 target_page 设为这个目标，让主屏幕显示“请认证”
                st.session_state.target_page = "FoodTest" 
            st.rerun()
            
        # --- 🔐 密钥验证动态区 ---
        # 只有在点击了锁定的项目时才显示
        if st.session_state.get("needs_auth"):
            st.markdown("---")
            st.markdown(f"<p style='text-align:center; color:#FF4B4B;'>激活项目: {st.session_state.needs_auth}</p>", unsafe_allow_html=True)
            
            # 调用密钥系统逻辑
            if key_check_gate(st.session_state.needs_auth):
                # 如果 key_check_gate 返回 True，代表验证通过
                st.session_state.target_page = st.session_state.needs_auth
                st.session_state.needs_auth = None # 验证成功后关闭验证区
                st.rerun()

        st.markdown("---")

        # --- 👑 管理员入口 ---
        if not st.session_state.get("admin_logged_in", False):
            with st.expander("🔐 管理员入口"):
                adm_u = st.text_input("账号", key="adm_u", placeholder="Admin ID")
                adm_p = st.text_input("密码", key="adm_p", type="password", placeholder="Password")
                if st.button("登录后台 💥", key="adm_login_btn", use_container_width=True):
                    if adm_u == ADMIN_USER and adm_p == ADMIN_PWD:
                        st.session_state.admin_logged_in = True
                        st.session_state.target_page = "Admin" # 登录成功自动跳转后台
                        st.success("欢迎回来，主理人！")
                        st.rerun()
                    else:
                        st.error("身份校验失败")
        else:
            st.success("✨ 管理员在线 ✨")
            if st.button("🚀 进入后台管理", key="go_admin_btn", use_container_width=True):
                st.session_state.target_page = "Admin"
                st.rerun()
            if st.button("👋 退出登录", key="logout_btn", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.session_state.target_page = "Home"
                st.rerun()

        st.caption("© 2026 Spectrum | Stay Colorful.")
