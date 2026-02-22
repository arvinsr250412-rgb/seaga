import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from contents import apply_contents_settings

apply_contents_settings()

# --- 1. 页面配置 ---
st.set_page_config(page_title="Spectrum | 性取向探索", layout="centered")

def sexual_text():
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
    
    # --- 5. 渲染逻辑 (结果分析增强版) ---
    if st.session_state.finished:
        st.balloons()
        
        # 1. 精准计分逻辑
        total = sum([QUESTIONS[i]["scores"][QUESTIONS[i]["options"].index(st.session_state.answers[i])] for i in range(len(QUESTIONS))])
        
        # 2. 五大结果导向定义
        if total <= 35:
            res = {
                "title": "恒星引力 | 极纯异性向",
                "color": "#4f46e5",
                "gradient": "linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%)",
                "desc": "你的情感核心非常稳固，如同恒星般有着明确的轨道。你天然地被异性特质吸引，这种引力简单、直接且纯粹。",
                "advice": "在亲密关系中，你更看重传统的互补美学。建议在保持稳定的同时，偶尔也探索对方灵魂中不符合传统标签的惊喜部分。"
            }
        elif total <= 75:
            res = {
                "title": "流星轨迹 | 异性向兼性好奇",
                "color": "#6366f1",
                "gradient": "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)",
                "desc": "你主要在异性轨道上运行，但偶尔也会被星空中的其他光芒吸引。你对同性有着审美上的高度欣赏，甚至有过轻微的心灵悸动。",
                "advice": "不要害怕这种‘偶尔的偏离’，这说明你拥有极高的审美同理心。这种流动性让你比别人更懂人心。"
            }
        elif total <= 105:
            res = {
                "title": "双星系统 | 多元/泛性倾向",
                "color": "#8b5cf6",
                "gradient": "linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)",
                "desc": "性别在你的世界里不是一道选择题。你被‘人’本身吸引，而非他的标签。你可以在两种性别中找到同样深度的联结。",
                "advice": "你是天生的灵魂探测器。在恋爱中，‘聊得来’和‘灵魂共振’是你唯一的入场券，请坚持你的这份纯粹。"
            }
        elif total <= 135:
            res = {
                "title": "星云迷雾 | 同性向兼性包容",
                "color": "#d946ef",
                "gradient": "linear-gradient(135deg, #d946ef 0%, #f43f5e 100%)",
                "desc": "你的情感重心明显倾向于同性，那里有你渴望的深度共鸣。虽然你并不排斥异性的陪伴，但那更像是友谊而非炽热的爱。",
                "advice": "你拥有极强的共情能力。学会区分‘对异性的欣赏’和‘对同性的渴望’，能帮你更早找到那个对的人。"
            }
        else:
            res = {
                "title": "星系中心 | 坚定同性向",
                "color": "#ec4899",
                "gradient": "linear-gradient(135deg, #ec4899 0%, #fb7185 100%)",
                "desc": "你是光谱中色彩最鲜明的一端。同性之间的那种极致细腻、同频共振是你生命的能量来源。你对异性几乎没有浪漫引力。",
                "advice": "你的心之所向非常明确。勇敢地拥抱这份独特性，在同频的圈子里，你会绽放出最夺目的光芒。"
            }
    
        # 3. 界面渲染
        st.markdown('<div class="main-title">Spectrum 探索报告</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="white-quiz-card-anchor"></div>', unsafe_allow_html=True)
            
            # 结果头部：新颖的渐变卡片
            st.markdown(f"""
                <div style="background: {res['gradient']}; padding: 2rem; border-radius: 1.5rem; text-align: center; color: white;">
                    <p style="font-size: 0.8rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 2px;">Your Spectrum Identity</p>
                    <h1 style="color: white !important; font-size: 2.2rem; margin: 0.5rem 0;">{res['title']}</h1>
                    <p style="font-size: 1rem; opacity: 0.95; line-height: 1.6;">{res['desc']}</p>
                </div>
            """, unsafe_allow_html=True)
    
            st.write("")
            
            # 深度分析维度
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 💡 灵魂画像")
                st.info(res['advice'])
            
            with col2:
                st.markdown("#### 📊 潜在倾向分布")
                # 这里的比例是基于分数计算的示意图
                hetero_bias = max(5, 100 - (total / 1.5))
                homo_bias = min(95, (total / 1.5))
                fluid_bias = 100 - abs(hetero_bias - homo_bias)
                
                st.write(f"异性吸引力: {int(hetero_bias)}%")
                st.progress(int(hetero_bias)/100)
                st.write(f"同性吸引力: {int(homo_bias)}%")
                st.progress(int(homo_bias)/100)
                st.write(f"灵魂流动性: {int(fluid_bias)}%")
                st.progress(int(fluid_bias)/100)
    
            st.divider()
            
            # 底部文案
            st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <p style="color: #64748b; font-size: 0.85rem;">
                        “爱是人类最后的自由，而你是自由的掌舵者。”
                    </p>
                    <p style="color: {res['color']}; font-weight: bold; font-size: 1.1rem;">探索总分：{total} / 150</p>
                </div>
            """, unsafe_allow_html=True)
    
        # 按钮美化
        st.write("")
        if st.button("✨ 重新开始探索", use_container_width=True):
            st.session_state.q_idx = 0
            st.session_state.answers = {}
            st.session_state.finished = False
                if not st.session_state.get("admin_logged_in", False):
            st.session_state.unlocked_Orientation = False # 关键！
            st.rerun()
    
    else:
        # --- B. 答题主页面 ---
        curr = st.session_state.q_idx
        st.markdown('<div class="main-title">Spectrum Lab</div>', unsafe_allow_html=True)
        
        # 进度条展示
        progress_val = (curr + 1) / len(QUESTIONS)
        st.progress(progress_val)
        st.markdown(f"<p style='text-align:center;'>第 {curr+1} / {len(QUESTIONS)} 题</p>", unsafe_allow_html=True)
    
        with st.container():
            st.markdown('<div class="white-quiz-card-anchor"></div>', unsafe_allow_html=True)
            st.markdown(f"### {QUESTIONS[curr]['q']}")
            
            # 选项
            prev_val = st.session_state.answers.get(curr)
            st.radio(
                "Select",
                options=QUESTIONS[curr]["options"],
                key=f"radio_{curr}",
                index=QUESTIONS[curr]["options"].index(prev_val) if prev_val in QUESTIONS[curr]["options"] else None,
                on_change=handle_click,
                label_visibility="collapsed"
            )
    
        # --- 核心修改：导航按钮逻辑 ---
        # 仅在不是第一题时显示“返回”按钮
        if curr > 0:
            st.write("") # 增加一点间距
            if st.button("⬅️ 返回上一题", use_container_width=True):
                st.session_state.q_idx -= 1
                st.rerun()

if __name__ == "__main__":
    sexual_text()


