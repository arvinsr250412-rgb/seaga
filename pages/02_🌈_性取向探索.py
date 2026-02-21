import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="Spectrum | 性取向探索", layout="centered")

# --- 2. 深度美化 CSS (修正版) ---
st.markdown("""
    <style>
    /* 全局背景 */
    .stApp {
        background-color: #f8fafc;
    }

    /* 强制所有文字颜色 */
    p, span, label, .stMarkdown, h3 {
        color: #1e293b !important;
    }

    /* 标题渐变 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(to right, #4f46e5, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }

    /* 【核心修复】让 st.container 变成白色圆角框 */
    /* 我们寻找包含特定的“锚点”div 的那个容器 */
    div[data-testid="stVerticalBlock"] > div:has(div.white-quiz-card-anchor) {
        background-color: #ffffff !important;
        border-radius: 2rem !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
        border: 1px solid #edf2f7 !important;
        margin: 1.5rem 0 !important;
    }

    /* 选项单选框美化 */
    div[data-testid="stRadio"] label {
        background: #ffffff !important;
        border: 2px solid #f1f5f9 !important;
        padding: 1rem 1.5rem !important;
        border-radius: 1.2rem !important;
        margin-bottom: 0.6rem !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stRadio"] label:hover {
        border-color: #8b5cf6 !important;
        background-color: #f5f3ff !important;
    }
    div[data-testid="stRadio"] [data-testid="stWidgetSelectionMarker"] {
        display: none;
    }

    /* 按钮样式 */
    button {
        background-color: #ffffff !important;
        color: #4f46e5 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 0.8rem !important;
    }
    </style>
""", unsafe_allow_html=True)

def get_prop():
    import matplotlib.font_manager as fm
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(base_dir, "simhei.ttf")
    if os.path.exists(font_path):
        return fm.FontProperties(fname=font_path)
    return None

prop = get_prop()

# --- 3. 完整 30 题题库 ---
# (为了代码简洁，这里展示 30 题逻辑，实际运行请确保 QUESTIONS 列表完整)
QUESTIONS = [
    {"q": "1. 在深夜感性时，你幻想的灵魂伴侣倾向于？", "options": ["显著异性", "较为中性", "显著同性", "跨越性别"], "scores": [0, 3, 5, 4]},
    {"q": "2. 对于‘柏拉图式’的同性亲密关系，你的接受度是？", "options": ["纯粹友谊", "偶尔会有模糊感", "渴望深度链接", "非常向往"], "scores": [0, 2, 4, 5]},
    {"q": "3. 看到感人的异性恋电影，你的共鸣程度？", "options": ["感同身受", "能理解但略有距离", "很难代入", "只看剧情不看性别"], "scores": [0, 2, 5, 3]},
    {"q": "4. 如果一个同性好友向你表达超越友谊的好感，你的第一反应？", "options": ["尴尬或排斥", "惊讶但想尝试理解", "内心泛起涟漪", "并不排斥任何性别的爱"], "scores": [0, 2, 4, 5]},
    {"q": "5. 你是否曾对某位同性产生过无法解释的占有欲？", "options": ["从未有过", "分不清是友情还是其他", "有过且很明确", "经常对优秀的人产生"], "scores": [0, 3, 5, 2]},
    {"q": "6. 想象一段共度余生的生活，对方的性别特征是否重要？", "options": ["非常重要，必须异性", "有倾向但非绝对", "性别是次要的", "完全不在意"], "scores": [0, 2, 4, 5]},
    {"q": "7. 你在寻找另一半时，更看重对方的？", "options": ["传统性别魅力", "独特的性格特质", "灵魂的契合度", "跨性别的共性"], "scores": [0, 3, 5, 4]},
    {"q": "8. 你是否觉得同性之间的理解力天生高于异性？", "options": ["不觉得", "有一点", "高度认可", "因人而异"], "scores": [0, 2, 4, 1]},
    {"q": "9. 在梦境中，你的浪漫对象通常是？", "options": ["总是异性", "多为异性偶尔中性", "经常出现同性", "面目模糊但感觉强烈"], "scores": [0, 2, 5, 3]},
    {"q": "10. 对于‘性别二元论’（非男即女），你的看法是？", "options": ["完全赞同", "基本认可", "认为世界是多元的", "性别只是标签"], "scores": [0, 1, 4, 5]},
    {"q": "11. 在街上看到极具魅力的同性，你的关注点在于？", "options": ["单纯欣赏美/模仿", "产生微妙的羞涩感", "有想要结识的冲动", "视觉冲击但无心理波动"], "scores": [1, 3, 5, 0]},
    {"q": "12. 对于肢体接触（如拥抱），你对同性的排斥感？", "options": ["完全不排斥", "仅限好友", "有一点心理边界", "非必要不接触"], "scores": [4, 2, 1, 0]},
    {"q": "13. 哪种类型的声音更容易让你产生‘酥麻’感？", "options": ["充满阳刚/柔美的异性声", "中性且磁性的声音", "富有张力的同性声", "好听就行"], "scores": [0, 3, 5, 2]},
    {"q": "14. 在青春期，你是否曾秘密关注过某位同性？", "options": ["没有", "有过短暂好奇", "有过深刻的好感", "对很多人都有好感"], "scores": [0, 2, 5, 3]},
    {"q": "15. 面对异性的追求，你内心最真实的反馈通常是？", "options": ["自然接受/喜悦", "有些压力", "渴望逃避", "视情况而定"], "scores": [0, 2, 5, 1]},
    {"q": "16. 你认为自己对同性身体的审美更偏向？", "options": ["客观欣赏", "带有一丝向往", "强烈的吸引", "无感"], "scores": [1, 3, 5, 0]},
    {"q": "17. 如果在一个只有同性的孤岛生活，你是否会建立亲密关系？", "options": ["不会", "可能会为了慰藉", "必然会", "不知道"], "scores": [0, 3, 5, 2]},
    {"q": "18. 对于流行的‘双性恋’话题，你的直觉反应？", "options": ["不能理解", "很酷但与我无关", "感觉在说我", "爱情本来就该这样"], "scores": [0, 2, 5, 4]},
    {"q": "19. 你在刷短视频时，更倾向于停留在哪种性别的颜值博主？", "options": ["异性", "平衡", "同性", "看内容"], "scores": [0, 3, 5, 1]},
    {"q": "20. 想象亲吻一个同性，你的内心感觉？", "options": ["无法接受", "好奇但不确定", "期待且心跳加快", "无所谓性别"], "scores": [0, 3, 5, 4]},
    {"q": "21. 如果可以重选性别，你希望自己是？", "options": ["现在的性别", "异性", "无性别/流动性", "无所谓"], "scores": [1, 3, 5, 4]},
    {"q": "22. 你是否觉得自己的性格中含有大量另一性别的成分？", "options": ["很少", "有一些", "很多", "我是融合的"], "scores": [1, 2, 4, 5]},
    {"q": "23. 对于同性婚姻合法化，你的态度？", "options": ["无感", "支持但不关注", "坚定支持", "认为这是必然趋势"], "scores": [1, 2, 5, 4]},
    {"q": "24. 你最向往的恋爱模式是？", "options": ["传统的互补", "两个独立的灵魂", "极度的同频共振", "无拘无束"], "scores": [0, 2, 5, 3]},
    {"q": "25. 你是否曾在醉酒或意识模糊时表现出对同性的依赖？", "options": ["从不", "很少", "经常", "我不喝酒"], "scores": [0, 3, 5, 1]},
    {"q": "26. 看到同性情侣秀恩爱，你的第一念头？", "options": ["奇怪", "真勇敢", "好甜/羡慕", "很正常"], "scores": [0, 2, 5, 3]},
    {"q": "27. 你是否怀疑过自己的性取向？", "options": ["从未", "偶尔一闪而过", "长期处于探索中", "已经确定为非纯异性"], "scores": [0, 2, 4, 5]},
    {"q": "28. 你更喜欢哪种类型的社交圈？", "options": ["异性较多", "性别均衡", "同性较多", "跨性别/亚文化圈"], "scores": [0, 2, 4, 5]},
    {"q": "29. 如果你的取向是小众的，你是否愿意为了真爱面对挑战？", "options": ["不愿意", "视情况", "愿意", "我已经这么做了"], "scores": [1, 2, 5, 4]},
    {"q": "30. 最后一个问题：此时此刻，你觉得自己最真实的颜色是？", "options": ["纯白（单一方向）", "渐变（正在流动）", "虹色（多元共存）", "透明（尚未定性）"], "scores": [0, 3, 5, 2]},
]

# --- 4. 状态管理 ---
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'finished' not in st.session_state: st.session_state.finished = False

def handle_click():
    key = f"radio_{st.session_state.q_idx}"
    val = st.session_state.get(key)
    if val:
        st.session_state.answers[st.session_state.q_idx] = val
        if st.session_state.q_idx < len(QUESTIONS) - 1:
            st.session_state.q_idx += 1
        else:
            st.session_state.finished = True

# --- 5. 渲染逻辑 ---
if st.session_state.finished:
    st.balloons()
    
    # 1. 计算总分
    total_score = sum([QUESTIONS[i]["scores"][QUESTIONS[i]["options"].index(st.session_state.answers[i])] for i in range(len(QUESTIONS))])
    
    # 2. 定义结果维度
    if total_score < 50:
        tag, color, gradient = "Indigo | 极光深蓝", "#4f46e5", "linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%)"
        summary = "你的情感频率如同深海，深沉且专注。在异性之间，你最能找到那种灵魂共振的安定感。"
        traits = ["传统审美的细腻捕捉", "异性引力的强指向性", "稳固的情感安全感"]
    elif total_score < 110:
        tag, color, gradient = "Prism | 棱镜幻彩", "#8b5cf6", "linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)"
        summary = "你的内心拥有一个多维的棱镜，光影交错。性别对你而言并非围墙，而是可以流动的色彩。"
        traits = ["跨越性别的审美感知", "对灵魂契合度的高度敏感", "自由且流动的爱情观"]
    else:
        tag, color, gradient = "Rose | 绯红迷雾", "#ec4899", "linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)"
        summary = "你站在色彩最瑰丽的一端。同性之间那种极致的共情与理解，是你心动信号最猛烈的来源。"
        traits = ["深度同频的共情力", "同性吸引力的极致敏锐", "突破传统的自由灵魂"]

    # 3. 渲染结果页
    st.markdown('<div class="main-title">Spectrum 探索报告</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="white-quiz-card-anchor"></div>', unsafe_allow_html=True)
        
        # 结果头部
        st.markdown(f"""
            <div style="text-align:center; padding: 1rem 0;">
                <p style="font-size: 0.9rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.1rem;">你的核心色域</p>
                <h1 style="background: {gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; margin: 0.5rem 0;">{tag}</h1>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # 维度分析
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### 🌈 情感底色")
            st.write(summary)
        with col2:
            st.markdown("#### ✨ 核心特质")
            for trait in traits:
                st.markdown(f"- **{trait}**")

        st.divider()

        # 图表分析：雷达图替代方案（使用条形图展示维度）
        st.markdown("#### 📊 多维引力场分析")
        
        # 模拟三个维度的得分
        # 这里可以根据题目权重细化，此处演示逻辑：
        dim_data = pd.DataFrame({
            '维度': ['传统引力', '灵魂契合', '流动感知'],
            '强度': [
                max(10, 100 - total_score * 0.6), 
                min(95, total_score * 0.8), 
                min(100, (total_score**1.2) / 10)
            ]
        })
        
        # 简单的百分比条展示
        for index, row in dim_data.iterrows():
            st.write(f"{row['维度']}")
            st.progress(int(row['强度'])/100)

        st.markdown(f"""
            <div style="background: #f1f5f9; padding: 1.5rem; border-radius: 1rem; margin-top: 1.5rem;">
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.6;">
                    <b>Spectrum 寄语：</b> 性取向是一个连续的光谱，而不是非黑即白的方块。
                    这份报告仅基于你此刻的直觉，它代表了你探索自我的一个锚点。
                    无论结果如何，去爱那个让你心跳加速的灵魂，才是唯一的真相。
                </p>
            </div>
        """, unsafe_allow_html=True)

    # 重新开始按钮
    st.write("")
    if st.button("✨ 重新开启探索", use_container_width=True):
        st.session_state.q_idx = 0
        st.session_state.answers = {}
        st.session_state.finished = False
        st.rerun()
