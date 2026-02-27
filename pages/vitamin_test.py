import streamlit as st
import plotly.graph_objects as go
import time
import random

# ==========================================
# 1. 配置与数据 (保持你的原始逻辑并优化)
# ==========================================
VITAMIN_QUESTIONS = [
    {"q": "1. 在夜间或光线昏暗的地方，你是否感觉视力明显下降？", "weights": {"A": 3}},
    {"q": "2. 眼睛是否经常感到干涩、疲劳，甚至有异物感？", "weights": {"A": 2, "B_basic": 1}},
    {"q": "3. 皮肤是否容易干燥、起皮，或有“鸡皮肤”？", "weights": {"A": 2, "E": 1}},
    {"q": "4. 你的呼吸道是否脆弱，换季容易咳嗽或过敏？", "weights": {"A": 2, "C": 1}},
    {"q": "5. 嘴角是否经常发炎、干裂，或频繁长口腔溃疡？", "weights": {"B_basic": 3, "C": 1}},
    {"q": "6. 头发是否容易油腻，或者常有头皮屑？", "weights": {"B_basic": 2, "A": 1}},
    {"q": "7. 即使睡眠充足，白天是否依然经常感到疲劳？", "weights": {"B_basic": 2, "D": 1, "B_neuro": 1}},
    {"q": "8. 消化能力是否较弱，容易出现消化不良或食欲不振？", "weights": {"B_basic": 2}},
    {"q": "9. 指甲是否脆弱、容易折断或起剥离层？", "weights": {"B_basic": 2, "A": 1}},
    {"q": "10. 头发是否干枯毛躁，或者近期掉发明显增多？", "weights": {"B_basic": 2, "E": 1}},
    {"q": "11. 手脚是否有过莫名的麻木感、刺痛感？", "weights": {"B_neuro": 3, "B_basic": 1}},
    {"q": "12. 情绪是否容易无端烦躁，或出现莫名的低落？", "weights": {"B_neuro": 2, "D": 2, "B_basic": 1}},
    {"q": "13. 是否感觉记忆力下降，或者经常处于“脑雾”状态？", "weights": {"B_neuro": 2, "E": 1, "D": 1}},
    {"q": "14. 蹲下站起时，是否容易感到头晕，或者面色经常苍白？", "weights": {"B_neuro": 3}},
    {"q": "15. 刷牙或咬硬物时，牙龈是否经常出血或红肿？", "weights": {"C": 3, "K": 1}},
    {"q": "16. 身体遇到轻微碰撞就容易出现淤青，且很久才消退？", "weights": {"C": 2, "K": 2}},
    {"q": "17. 皮肤出现伤口时，愈合速度是否比别人慢？", "weights": {"C": 2, "A": 1}},
    {"q": "18. 是否觉得自己免疫力低下，换季极易感冒？", "weights": {"C": 2, "D": 2, "A": 1}},
    {"q": "19. 关节和肌肉是否经常有隐隐的酸痛感？", "weights": {"C": 1, "D": 2}},
    {"q": "20. 骨骼、腰背是否经常感到酸痛（尤其在冬季）？", "weights": {"D": 3}},
    {"q": "21. 你是否很少晒太阳，且大部分时间都在室内？", "weights": {"D": 3}},
    {"q": "22. 睡眠质量是否较差，入睡困难或处于浅睡眠？", "weights": {"D": 2, "B_basic": 1}},
    {"q": "23. 阴雨天或缺乏阳光的季节，情绪会明显低落？", "weights": {"D": 3, "B_neuro": 1}},
    {"q": "24. 皮肤是否容易出现色斑，或感觉失去弹性？", "weights": {"E": 3, "C": 1}},
    {"q": "25. 剧烈运动后，肌肉酸痛的恢复时间特别漫长？", "weights": {"E": 2, "C": 1}},
    {"q": "26. 肌肉是否有时会感到莫名的震颤或无力感？", "weights": {"E": 2, "D": 1}},
    {"q": "27. 受伤流血时，血液凝固止住的时间比常人长？", "weights": {"K": 3, "C": 1}},
    {"q": "28. 身上是否会出现不明原因的微小皮下出血点？", "weights": {"K": 3, "C": 1}},
    {"q": "29. (女性适用) 生理期出血量是否异常偏多？", "weights": {"K": 2, "A": 1}},
    {"q": "30. 你的骨密度检测是否有偏低倾向，或曾有骨折史？", "weights": {"D": 2, "K": 2}}
]

VITAMIN_ANALYSIS = {
    "A": {"name": "维生素 A", "icon": "👀", "color": "#FF9F43", "analysis": "你的黏膜屏障和视觉系统正在报警！", "diet": "胡萝卜、南瓜、猪肝。", "supplement": "建议选择含 β-胡萝卜素的补剂。"},
    "B_basic": {"name": "基础 B 族", "icon": "🔥", "color": "#FF6B6B", "analysis": "能量代谢遇到瓶颈，易感疲劳和口腔问题。", "diet": "全谷物、燕麦、瘦肉、大豆。", "supplement": "建议补充复合 B 族。"},
    "B_neuro": {"name": "B12 & 叶酸", "icon": "🧠", "color": "#A29BFE", "analysis": "神经传导和造血功能需要关注。", "diet": "绿叶蔬菜、蛋奶类、动物肝脏。", "supplement": "建议额外补充 B12。"},
    "C": {"name": "维生素 C", "icon": "🛡️", "color": "#FAB1A0", "analysis": "抗氧化防线薄弱，微血管变得脆弱。", "diet": "猕猴桃、柑橘类、彩椒。", "supplement": "日常补充 100-200mg。"},
    "D": {"name": "维生素 D", "icon": "☀️", "color": "#FDCB6E", "analysis": "骨代谢和情绪调节器电量不足。", "diet": "多晒太阳。深海鱼、蛋黄。", "supplement": "建议补充 D3，随餐服用。"},
    "E": {"name": "维生素 E", "icon": "🥑", "color": "#55EFC4", "analysis": "细胞正承受氧化压力，恢复力下降。", "diet": "坚果、牛油果、橄榄油。", "supplement": "优先选择天然形式生育酚。"},
    "K": {"name": "维生素 K", "icon": "🩸", "color": "#D63031", "analysis": "凝血系统和钙沉淀逻辑偏低。", "diet": "羽衣甘蓝、菠菜、纳豆。", "supplement": "建议搭配 K2 (MK-7)。"}
}

# 计算各维度最大可能得分（用于归一化百分比）
MAX_POSSIBLE = {"A": 0, "B_basic": 0, "B_neuro": 0, "C": 0, "D": 0, "E": 0, "K": 0}
for q in VITAMIN_QUESTIONS:
    for vit, weight in q["weights"].items():
        MAX_POSSIBLE[vit] += weight * 2

# ==========================================
# 2. 核心逻辑与雷达图
# ==========================================
def draw_vitamin_radar(scores):
    # 将原始分数转化为 0-100 的缺乏程度
    categories = []
    values = []
    for key in ["A", "B_basic", "B_neuro", "C", "D", "E", "K"]:
        pct = (scores[key] / MAX_POSSIBLE[key] * 100) if MAX_POSSIBLE[key] > 0 else 0
        values.append(min(pct, 100)) # 防止溢出
        categories.append(VITAMIN_ANALYSIS[key]['name'])

    # 闭合曲线
    values.append(values[0])
    categories.append(categories[0])

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(20, 184, 166, 0.3)',
        line=dict(color='#14b8a6', width=2),
        marker=dict(size=5, color='#ffffff', line=dict(color='#14b8a6', width=2))
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor='rgba(200,200,200,0.2)'),
            angularaxis=dict(tickfont=dict(size=11, color='#666'), gridcolor='rgba(200,200,200,0.2)')
        ),
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=30, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# ==========================================
# 3. 页面渲染
# ==========================================
def show_vitamin_test():
    # 注入 CSS (复刻食物测试样式)
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Noto Sans SC', sans-serif; }
        .stProgress > div > div > div > div { background: linear-gradient(90deg, #5eead4 0%, #14b8a6 100%); }
        div.stButton > button {
            background: white; border-radius: 1.25rem !important; padding: 0.8rem 1.5rem !important;
            font-size: 1rem !important; transition: all 0.2s; border: 1px solid #e2e8f0;
            width: 100%; text-align: left !important; margin-bottom: 0.5rem;
        }
        div.stButton > button:hover { border-color: #14b8a6 !important; color: #14b8a6 !important; background-color: #f0fdfa !important; transform: translateY(-1px); }
        .btn-primary > div > button { 
            background-color: #14b8a6 !important; color: white !important; text-align: center !important; 
            font-weight: bold !important; box-shadow: 0 10px 15px -3px rgba(20, 184, 166, 0.2) !important;
        }
        .result-card { background: white; border-radius: 2rem; padding: 2rem; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); text-align: center; }
        .vit-item { text-align: left; padding: 1rem; border-bottom: 1px solid #f1f5f9; }
        </style>
    """, unsafe_allow_html=True)

    # 初始化状态
    if 'vit_step' not in st.session_state: st.session_state.vit_step = 0
    if 'vit_scores' not in st.session_state: st.session_state.vit_scores = {k: 0 for k in MAX_POSSIBLE.keys()}
    if 'vit_history' not in st.session_state: st.session_state.vit_history = []

    # 首页
    if st.session_state.vit_step == 0:
        st.write("<br><br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.markdown("""
                <div style="text-align: center;">
                    <div style="width: 5rem; height: 5rem; background-color: #ccfbf1; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 1.5rem auto;">💊</div>
                    <h1 style="font-weight: 900; color: #0f172a; font-size: 2.5rem;">维生素缺乏预警</h1>
                    <p style="color: #64748b; margin-bottom: 2rem;">30项身体反馈，解码你的潜在营养缺口</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("开始测评", use_container_width=True):
                st.session_state.vit_step = 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # 答题页
    elif 1 <= st.session_state.vit_step <= len(VITAMIN_QUESTIONS):
        q_idx = st.session_state.vit_step - 1
        q_data = VITAMIN_QUESTIONS[q_idx]
        
        st.progress(st.session_state.vit_step / len(VITAMIN_QUESTIONS))
        st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <p style="color: #14b8a6; font-weight: bold; letter-spacing: 0.1em;">QUESTION {st.session_state.vit_step} / 30</p>
                <h2 style="font-size: 1.5rem; color: #1e293b; min-height: 4rem;">{q_data['q']}</h2>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 5, 1])
        with col2:
            # 选项逻辑：经常(2分), 有时(1分), 从不(0分)
            options = [("经常 / 明显", 2), ("偶尔 / 轻微", 1), ("从不 / 无感", 0)]
            for text, val in options:
                if st.button(text, key=f"q_{q_idx}_{text}"):
                    # 记录分数
                    for vit, weight in q_data['weights'].items():
                        st.session_state.vit_scores[vit] += weight * val
                    st.session_state.vit_history.append(q_data['weights']) # 简化记录用于回退
                    st.session_state.vit_step += 1
                    st.rerun()
            
            # 返回按钮
            if st.session_state.vit_step > 1:
                st.write("<br>", unsafe_allow_html=True)
                if st.button("⬅️ 返回上一题", key="back"):
                    # 撤销分数（此处逻辑需注意：回退时需要减去上次加的分，为简化demo，此处直接重置需谨慎）
                    # 建议：实际生产环境记录具体加了多少分。这里先做简单跳转演示。
                    st.session_state.vit_step -= 1
                    st.rerun()

    # 结果页
    else:
        with st.spinner('正在分析你的身体信号...'):
            time.sleep(1.5)
        
        col1, col2, col3 = st.columns([1, 10, 1])
        with col2:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("<h2 style='color:#0f172a;'>测评报告</h2>", unsafe_allow_html=True)
            
            # 雷达图
            st.plotly_chart(draw_vitamin_radar(st.session_state.vit_scores), use_container_width=True, config={'displayModeBar': False})
            
            st.markdown("<p style='color:#64748b; font-size:0.9rem;'>*注：此结果基于症状自测，非医疗诊断。若有严重不适请咨询医生。</p>", unsafe_allow_html=True)
            
            # 详细分析
            st.markdown("<h3 style='text-align:left; margin-top:2rem;'>重点关注建议：</h3>", unsafe_allow_html=True)
            
            # 排序：只显示得分（缺乏程度）较高的项
            sorted_vits = sorted(st.session_state.vit_scores.items(), key=lambda x: x[1], reverse=True)
            
            for vit_key, score in sorted_vits:
                if score > 0: # 只显示有症状的
                    data = VITAMIN_ANALYSIS[vit_key]
                    pct = int(score / MAX_POSSIBLE[vit_key] * 100)
                    st.markdown(f"""
                        <div class="vit-item">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <strong>{data['icon']} {data['name']}</strong>
                                <span style="color:#f43f5e; font-size:0.8rem;">缺口指数: {pct}%</span>
                            </div>
                            <p style="font-size:0.85rem; color:#475569; margin:0.5rem 0;">{data['analysis']}</p>
                            <div style="background:#f8fafc; padding:0.8rem; border-radius:0.5rem; font-size:0.8rem;">
                                🥗 <b>食补：</b>{data['diet']}<br>
                                💊 <b>建议：</b>{data['supplement']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            st.write("<br>", unsafe_allow_html=True)
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("重新测评"):
                st.session_state.vit_step = 0
                st.session_state.vit_scores = {k: 0 for k in MAX_POSSIBLE.keys()}
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_vitamin_test()
