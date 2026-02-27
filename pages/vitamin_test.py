import streamlit as st
import copy

# ==========================================
# 1. 配置 30 道多维加权题库
# ==========================================
VITAMIN_QUESTIONS = [
    {"q": "1. 在夜间或光线昏暗的地方，你是否感觉视力明显下降？", "weights": {"A": 3}, "cat": "视觉与粘膜"},
    {"q": "2. 眼睛是否经常感到干涩、疲劳，甚至有异物感？", "weights": {"A": 2, "B_basic": 1}, "cat": "视觉与粘膜"},
    {"q": "3. 皮肤是否容易干燥、起皮，或有“鸡皮肤”？", "weights": {"A": 2, "E": 1}, "cat": "视觉与粘膜"},
    {"q": "4. 你的呼吸道是否脆弱，换季容易咳嗽或过敏？", "weights": {"A": 2, "C": 1}, "cat": "免疫屏障"},
    {"q": "5. 嘴角是否经常发炎、干裂，或频繁长口腔溃疡？", "weights": {"B_basic": 3, "C": 1}, "cat": "皮肤粘膜"},
    {"q": "6. 头发是否容易油腻，或者常有头皮屑？", "weights": {"B_basic": 2, "A": 1}, "cat": "皮肤粘膜"},
    {"q": "7. 即使睡眠充足，白天是否依然经常感到疲劳？", "weights": {"B_basic": 2, "D": 1, "B_neuro": 1}, "cat": "精力代谢"},
    {"q": "8. 消化能力是否较弱，容易出现消化不良或食欲不振？", "weights": {"B_basic": 2}, "cat": "精力代谢"},
    {"q": "9. 指甲是否脆弱、容易折断或起剥离层？", "weights": {"B_basic": 2, "A": 1}, "cat": "皮肤粘膜"},
    {"q": "10. 头发是否干枯毛躁，或者近期掉发明显增多？", "weights": {"B_basic": 2, "E": 1}, "cat": "皮肤粘膜"},
    {"q": "11. 手脚是否有过莫名的麻木感、刺痛感？", "weights": {"B_neuro": 3, "B_basic": 1}, "cat": "神经系统"},
    {"q": "12. 情绪是否容易无端烦躁，或出现莫名的低落？", "weights": {"B_neuro": 2, "D": 2, "B_basic": 1}, "cat": "神经系统"},
    {"q": "13. 是否感觉记忆力下降，或者经常处于“脑雾”状态？", "weights": {"B_neuro": 2, "E": 1, "D": 1}, "cat": "神经系统"},
    {"q": "14. 蹲下站起时，是否容易感到头晕，或者面色经常苍白？", "weights": {"B_neuro": 3}, "cat": "神经系统"},
    {"q": "15. 刷牙或咬硬物时，牙龈是否经常出血或红肿？", "weights": {"C": 3, "K": 1}, "cat": "血液循环"},
    {"q": "16. 身体遇到轻微碰撞就容易出现淤青，且很久才消退？", "weights": {"C": 2, "K": 2}, "cat": "血液循环"},
    {"q": "17. 皮肤出现伤口时，愈合速度是否比别人慢？", "weights": {"C": 2, "A": 1}, "cat": "修复能力"},
    {"q": "18. 是否觉得自己免疫力低下，换季极易感冒？", "weights": {"C": 2, "D": 2, "A": 1}, "cat": "免疫屏障"},
    {"q": "19. 关节和肌肉是否经常有隐隐的酸痛感？", "weights": {"C": 1, "D": 2}, "cat": "骨骼肌肉"},
    {"q": "20. 骨骼、腰背是否经常感到酸痛（尤其在冬季）？", "weights": {"D": 3}, "cat": "骨骼肌肉"},
    {"q": "21. 你是否很少晒太阳，且大部分时间都在室内？", "weights": {"D": 3}, "cat": "骨骼肌肉"},
    {"q": "22. 睡眠质量是否较差，入睡困难或处于浅睡眠？", "weights": {"D": 2, "B_basic": 1}, "cat": "神经系统"},
    {"q": "23. 阴雨天或缺乏阳光的季节，情绪会明显低落？", "weights": {"D": 3, "B_neuro": 1}, "cat": "神经系统"},
    {"q": "24. 皮肤是否容易出现色斑，或感觉失去弹性？", "weights": {"E": 3, "C": 1}, "cat": "皮肤粘膜"},
    {"q": "25. 剧烈运动后，肌肉酸痛的恢复时间特别漫长？", "weights": {"E": 2, "C": 1}, "cat": "修复能力"},
    {"q": "26. 肌肉是否有时会感到莫名的震颤或无力感？", "weights": {"E": 2, "D": 1}, "cat": "骨骼肌肉"},
    {"q": "27. 受伤流血时，血液凝固止住的时间比常人长？", "weights": {"K": 3, "C": 1}, "cat": "血液循环"},
    {"q": "28. 身上是否会出现不明原因的微小皮下出血点？", "weights": {"K": 3, "C": 1}, "cat": "血液循环"},
    {"q": "29. (女性适用) 生理期出血量是否异常偏多？", "weights": {"K": 2, "A": 1}, "cat": "血液循环"},
    {"q": "30. 你的骨密度检测是否有偏低倾向，或曾有骨折史？", "weights": {"D": 2, "K": 2}, "cat": "骨骼肌肉"}
]

# 预计算最大分值
MAX_SCORES = {"A": 0, "B_basic": 0, "B_neuro": 0, "C": 0, "D": 0, "E": 0, "K": 0}
for q in VITAMIN_QUESTIONS:
    for vit, weight in q["weights"].items():
        MAX_SCORES[vit] += weight * 2

VITAMIN_ANALYSIS = {
    "A": {"name": "维生素 A", "icon": "👀", "color": "#FF9F43", "analysis": "你的黏膜屏障和视觉系统正在报警！缺乏维 A 会导致暗适应能力下降（夜盲）、干眼症，以及毛囊过度角化（鸡皮肤）。", "diet": "深色蔬菜和动物内脏。首选：胡萝卜、南瓜、猪肝。", "supplement": "建议选择含 β-胡萝卜素的补剂，随含脂餐服用。"},
    "B_basic": {"name": "基础 B 族 (B1/B2/B6)", "icon": "🔥", "color": "#FF6B6B", "analysis": "你的能量代谢遇到瓶颈。缺乏基础 B 族易导致慢性疲劳、口腔溃疡、唇炎和脂溢性皮炎。", "diet": "全谷物、燕麦、糙米、瘦肉、大豆。", "supplement": "建议服用“复合维生素 B 族”，建议早午饭后服用。"},
    "B_neuro": {"name": "B12 & 叶酸", "icon": "🧠", "color": "#A29BFE", "analysis": "你的神经传导和造血功能需要关注。缺乏它们容易导致头晕、面色苍白，以及手脚麻木。", "diet": "绿叶蔬菜（叶酸）和动物性食物（B12）。", "supplement": "素食主义者必须额外补充 B12。备孕期需重点补叶酸。"},
    "C": {"name": "维生素 C", "icon": "🛡️", "color": "#FAB1A0", "analysis": "你的抗氧化防线出现了漏洞。缺乏维 C 会使微血管变脆弱（牙龈出血、易淤青），免疫力下降。", "diet": "猕猴桃、柑橘类、彩椒。避免高温烹饪。", "supplement": "日常补充 100-200mg 即可，感冒期可加量。"},
    "D": {"name": "维生素 D", "icon": "☀️", "color": "#FFE66D", "analysis": "你的骨代谢开关和情绪调节器电量低。缺乏会导致骨痛、肌肉无力、易感冒和季节性抑郁。", "diet": "食物来源极少。仅深海鱼、蘑菇中有微量。", "supplement": "建议每日补充 1000-2000 IU 的 D3，务必随餐服用。"},
    "E": {"name": "维生素 E", "icon": "🥑", "color": "#55EFC4", "analysis": "你的细胞正承受氧化压力。维 E 专门中和自由基，缺乏它会导致皮肤暗沉、肌肉恢复慢。", "diet": "葵花籽、杏仁、牛油果和橄榄油。", "supplement": "优先选择天然形式 d-α-生育酚。"},
    "K": {"name": "维生素 K", "icon": "🩸", "color": "#FF7675", "analysis": "你的凝血系统和钙沉淀逻辑偏低。维 K 负责止血，并将钙“引流”进骨骼。", "diet": "羽衣甘蓝、菠菜、纳豆。", "supplement": "若补钙，建议搭配维生素 K2 (MK-7)。"}
}

def show_vitamin_test():
    # 注入高级多巴胺 CSS
    st.markdown("""
        <style>
        /* 进度条美化 */
        .stProgress > div > div > div > div { background: linear-gradient(90deg, #FF9A8B 0%, #FF6A88 100%); border-radius: 10px; }
        
        /* 答题卡片 */
        .q-card {
            background: #ffffff;
            border-radius: 35px;
            padding: 2.5rem;
            border: 4px solid #FFF5F7;
            box-shadow: 0 20px 40px rgba(255, 106, 136, 0.1);
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .q-cat { color: #FF6A88; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
        
        /* 结果卡片 */
        .res-card {
            background: white; border-radius: 40px; padding: 3rem;
            border: 1px solid #FFE4E9; box-shadow: 0 25px 50px -12px rgba(255, 106, 136, 0.2);
        }
        .tag-pill {
            display: inline-block; background: #FFF0F3; color: #FF6A88;
            font-size: 0.85rem; font-weight: bold; padding: 0.4rem 1.2rem;
            border-radius: 999px; margin-bottom: 0.5rem; border: 1px solid #FFE4E9;
        }
        
        /* 自定义按钮容器 */
        .button-zone { margin-top: 2rem; }
        </style>
    """, unsafe_allow_html=True)

    # 初始化状态
    if 'vitamin_step' not in st.session_state:
        st.session_state.vitamin_step = 0
        st.session_state.vit_scores = {k: 0.0 for k in MAX_SCORES.keys()}
        st.session_state.vit_history = [] # 存储分数历史

    step = st.session_state.vitamin_step
    total_q = len(VITAMIN_QUESTIONS)

    # --- 答题界面 ---
    if step < total_q:
        q_data = VITAMIN_QUESTIONS[step]
        
        # 顶部进度
        st.markdown(f"<p style='text-align:center; color:#FF6A88; margin-bottom:0;'><b>Step {step+1} of {total_q}</b></p>", unsafe_allow_html=True)
        st.progress((step + 1) / total_q)
        
        # 问题卡片
        st.markdown(f"""
            <div class='q-card'>
                <p class='q-cat'>• {q_data['cat']} •</p>
                <h2 style='color: #2D3748; margin-top: 0.5rem;'>{q_data['q']}</h2>
            </div>
        """, unsafe_allow_html=True)

        # 选项按钮
        col1, col2, col3 = st.columns(3)
        
        def next_question(val):
            # 记录历史 (深拷贝当前分数)
            st.session_state.vit_history.append(copy.deepcopy(st.session_state.vit_scores))
            # 更新分数
            for vit, w in q_data["weights"].items():
                st.session_state.vit_scores[vit] += w * val
            st.session_state.vitamin_step += 1
            st.rerun()

        with col1:
            if st.button("🔴 经常如此", key=f"btn_{step}_2", use_container_width=True): next_question(2.0)
        with col2:
            if st.button("🟡 偶尔这样", key=f"btn_{step}_1", use_container_width=True): next_question(1.0)
        with col3:
            if st.button("🟢 几乎没有", key=f"btn_{step}_0", use_container_width=True): next_question(0.0)

        # 返回上一题按钮 (仅在第2题及以后出现)
        if step > 0:
            st.write("")
            _, back_col, _ = st.columns([1,1,1])
            with back_col:
                if st.button("⬅️ 返回上一题", key="back_prev", use_container_width=True):
                    # 恢复上一步的分数
                    st.session_state.vit_scores = st.session_state.vit_history.pop()
                    st.session_state.vitamin_step -= 1
                    st.rerun()

    # --- 结果界面 ---
    else:
        rates = {k: (st.session_state.vit_scores[k] / MAX_SCORES[k]) for k in MAX_SCORES.keys()}
        max_vit = max(rates, key=rates.get)
        res = VITAMIN_ANALYSIS[max_vit]
        rate_pct = int(rates[max_vit] * 100)

        st.markdown(f"<h1 style='text-align:center; color:#FF6A88;'>分析结果生成 🧬</h1>", unsafe_allow_html=True)

        st.markdown(f"""
            <div class='res-card'>
                <div style='text-align:center; font-size: 5rem; margin-bottom: 1rem;'>{res['icon']}</div>
                <h2 style='text-align:center; color:{res['color']}; margin-top:0;'>核心缺乏：{res['name']}</h2>
                
                <div style='margin: 2rem 0;'>
                    <div style='display:flex; justify-content:space-between; font-size:0.9rem; color:#666;'>
                        <span>缺乏程度评估</span>
                        <span>{rate_pct}%</span>
                    </div>
                    <div style="background:#F0F0F0; border-radius:20px; height:12px; margin-top:8px;">
                        <div style="background:{res['color']}; width:{rate_pct}%; height:12px; border-radius:20px; transition: 1s;"></div>
                    </div>
                </div>

                <div style='margin-top:2rem;'><span class='tag-pill'>🩺 症状追踪解析</span><p style='line-height:1.7;'>{res['analysis']}</p></div>
                <div style='margin-top:1.5rem;'><span class='tag-pill'>🥗 多巴胺饮食处方</span><p style='line-height:1.7;'>{res['diet']}</p></div>
                <div style='margin-top:1.5rem;'><span class='tag-pill'>💊 科学补剂指南</span><p style='line-height:1.7;'>{res['supplement']}</p></div>
                
                <div style="margin-top: 2rem; font-size: 0.8rem; color: #BBB; border-top: 1px solid #EEE; padding-top: 1rem;">
                    <strong>Spectrum 免责声明：</strong>算法基于加权统计，非医疗诊断。严重不适请咨询医师。
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        # 重新评估按钮仅出现在此处
        if st.button("🔄 重新评估身体状态", key="final_reset", use_container_width=True):
            st.session_state.vitamin_step = 0
            st.session_state.vit_scores = {k: 0.0 for k in MAX_SCORES.keys()}
            st.session_state.vit_history = []
            st.rerun()
