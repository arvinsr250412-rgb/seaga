import streamlit as st

# ==========================================
# 1. 题库与多维权重配置 (30道科学评估题)
# 算法逻辑：每个症状可能关联多种维生素缺乏，赋予不同权重
# ==========================================
VITAMIN_QUESTIONS = [
    {"q": "1. 在夜间或光线昏暗的地方，你是否感觉视力明显下降？", "weights": {"A": 3}},
    {"q": "2. 眼睛是否经常感到干涩、疲劳，甚至有异物感？", "weights": {"A": 2, "B_basic": 1}},
    {"q": "3. 皮肤是否容易干燥、起皮，或有“鸡皮肤”（毛囊角化）？", "weights": {"A": 2, "E": 1}},
    {"q": "4. 你的呼吸道是否脆弱，换季容易咳嗽或过敏？", "weights": {"A": 2, "C": 1}},
    {"q": "5. 嘴角是否经常发炎、干裂，或频繁长口腔溃疡？", "weights": {"B_basic": 3, "C": 1}},
    {"q": "6. 头发是否容易油腻，或者常有头皮屑、脂溢性皮炎？", "weights": {"B_basic": 2, "A": 1}},
    {"q": "7. 即使睡眠充足，白天是否依然经常感到疲劳、缺乏精力？", "weights": {"B_basic": 2, "D": 1, "B_neuro": 1}},
    {"q": "8. 消化能力是否较弱，容易出现消化不良或食欲不振？", "weights": {"B_basic": 2}},
    {"q": "9. 指甲是否脆弱、容易折断或起剥离层？", "weights": {"B_basic": 2, "A": 1}},
    {"q": "10. 头发是否干枯毛躁，或者近期掉发明显增多？", "weights": {"B_basic": 2, "E": 1}},
    {"q": "11. 手脚是否有过莫名的麻木感、刺痛感？", "weights": {"B_neuro": 3, "B_basic": 1}},
    {"q": "12. 情绪是否容易无端烦躁，或出现莫名的低落抑郁？", "weights": {"B_neuro": 2, "D": 2, "B_basic": 1}},
    {"q": "13. 是否感觉记忆力下降，或者经常处于“脑雾”状态？", "weights": {"B_neuro": 2, "E": 1, "D": 1}},
    {"q": "14. 蹲下站起时，是否容易感到头晕，或者面色经常苍白？", "weights": {"B_neuro": 3}}, # 针对叶酸/B12贫血
    {"q": "15. 刷牙或咬硬物时，牙龈是否经常出血或红肿？", "weights": {"C": 3, "K": 1}},
    {"q": "16. 身体遇到轻微碰撞就容易出现淤青，且很久才消退？", "weights": {"C": 2, "K": 2}},
    {"q": "17. 皮肤出现伤口时，愈合速度是否比别人慢？", "weights": {"C": 2, "A": 1}},
    {"q": "18. 是否觉得自己免疫力低下，换季或周围有人感冒极易被传染？", "weights": {"C": 2, "D": 2, "A": 1}},
    {"q": "19. 关节和肌肉是否经常有隐隐的酸痛感？", "weights": {"C": 1, "D": 2}},
    {"q": "20. 骨骼、腰背是否经常感到酸痛（尤其在冬季或久坐后）？", "weights": {"D": 3}},
    {"q": "21. 你是否很少晒太阳，且大部分时间都在室内？", "weights": {"D": 3}},
    {"q": "22. 睡眠质量是否较差，入睡困难或处于浅睡眠？", "weights": {"D": 2, "B_basic": 1}},
    {"q": "23. 阴雨天或缺乏阳光的季节，情绪是否会明显低落？", "weights": {"D": 3, "B_neuro": 1}},
    {"q": "24. 皮肤是否容易出现色斑，或感觉失去弹性、加速老化？", "weights": {"E": 3, "C": 1}},
    {"q": "25. 剧烈运动后，肌肉酸痛的恢复时间是否特别漫长？", "weights": {"E": 2, "C": 1}},
    {"q": "26. 肌肉是否有时会感到莫名的震颤或无力感？", "weights": {"E": 2, "D": 1}},
    {"q": "27. 受伤流血时，血液凝固止住的时间是否比常人长？", "weights": {"K": 3, "C": 1}},
    {"q": "28. 身上是否会出现不明原因的微小皮下出血点？", "weights": {"K": 3, "C": 1}},
    {"q": "29. (女性适用，男性选没有) 生理期出血量是否异常偏多？", "weights": {"K": 2, "A": 1}},
    {"q": "30. 你的骨密度检测是否有偏低倾向，或曾有骨折史？", "weights": {"D": 2, "K": 2}}
]

# 自动计算每种维生素可能的最大权重总和
MAX_SCORES = {"A": 0, "B_basic": 0, "B_neuro": 0, "C": 0, "D": 0, "E": 0, "K": 0}
for q in VITAMIN_QUESTIONS:
    for vit, weight in q["weights"].items():
        MAX_SCORES[vit] += weight * 2  # 假设最高选项得分为 权重 * 2

# ==========================================
# 2. 结果分析与补充建议 (扩展为 7 大类)
# ==========================================
VITAMIN_ANALYSIS = {
    "A": {
        "name": "维生素 A (视黄醇)", "icon": "👀",
        "analysis": "你的黏膜屏障和视觉系统正在报警！维生素 A 掌管着视力、免疫第一道防线和皮肤平滑度。缺乏它会导致暗适应能力下降（夜盲）、干眼症，以及毛囊过度角化（鸡皮肤）。",
        "diet": "多吃深色蔬菜和动物内脏。首选：胡萝卜、南瓜、红薯（含β-胡萝卜素），及猪肝等。",
        "supplement": "建议选择含 β-胡萝卜素的补剂，身体会按需转化为维A，避免直接补过量导致毒性。随含脂餐服用。"
    },
    "B_basic": {
        "name": "基础 B 族 (B1/B2/B3/B6)", "icon": "🔥",
        "analysis": "你的身体可能处于“能量代谢卡壳”状态！基础 B 族是细胞的“火花塞”，负责将碳水化合物转化为能量，并维持皮肤黏膜健康。缺乏易导致慢性疲劳、口腔溃疡、唇炎和脂溢性皮炎。",
        "diet": "增加全谷物摄入。首选：燕麦、糙米、瘦肉、鸡蛋、大豆及坚果。",
        "supplement": "B族维生素在体内协同作战，建议直接服用“复合维生素 B 族”。水溶性维生素多余会排出，建议早午饭后服用，晚间服用可能影响睡眠。"
    },
    "B_neuro": {
        "name": "造血与神经 B 族 (B12 & 叶酸)", "icon": "🧠",
        "analysis": "你的神经传导和红细胞生成可能遇到了瓶颈。维生素 B12 和叶酸深度参与DNA合成与神经髓鞘的保护。缺乏它们不仅容易导致巨幼红细胞性贫血（头晕、面色苍白），还会引发手脚麻木和情绪抑郁。",
        "diet": "叶酸来源：深绿色绿叶蔬菜（菠菜、羽衣甘蓝）。B12 仅存在于动物性食物（肉、蛋、奶）中。",
        "supplement": "素食主义者、老年人或长期肠胃不佳者必须额外补充 B12。孕期或备孕女性需重点补充叶酸。"
    },
    "C": {
        "name": "维生素 C (抗坏血酸)", "icon": "🛡️",
        "analysis": "你的胶原蛋白网络和抗氧化防线出现了漏洞！维C是合成胶原蛋白的必需辅酶。缺乏时，微血管变脆弱（牙龈出血、易淤青），同时免疫系统白细胞的战斗力会显著下降。",
        "diet": "新鲜果蔬是王者。首选：猕猴桃、草莓、柑橘类、彩椒。注意避免长时间高温烹饪。",
        "supplement": "日常补充 100-200mg 即可，感冒高发期可增加。推荐选择含有生物类黄酮的天然提取维C，吸收率更高。"
    },
    "D": {
        "name": "维生素 D (阳光维生素)", "icon": "☀️",
        "analysis": "你的骨代谢开关和情绪调节器可能处于低电量。维 D 本质是激素，决定肠道对钙的吸收，并影响血清素分泌。缺乏会导致骨痛、肌肉无力、易感冒和季节性抑郁。",
        "diet": "食物来源极少！仅在深海鱼、蘑菇和蛋黄中有微量存在。",
        "supplement": "这是现代“室内人”最需要补充的营养素！建议每日补充 1000-2000 IU 的 D3。因其为脂溶性，务必随正餐（含脂肪）服用。"
    },
    "E": {
        "name": "维生素 E (生育酚)", "icon": "🥑",
        "analysis": "你的细胞正承受较高的氧化应激压力。维 E 是细胞膜的“保安”，专门中和自由基，延缓衰老。缺乏它会导致红细胞脆弱、肌肉恢复缓慢以及皮肤暗沉长斑。",
        "diet": "多摄入优质油脂。首选：葵花籽、杏仁、牛油果和初榨橄榄油。",
        "supplement": "优先选择天然形式的 d-α-生育酚（吸收率高于合成型 dl-α）。通常通过日常饮食和复合维生素即可满足。"
    },
    "K": {
        "name": "维生素 K (凝血与引钙入骨)", "icon": "🩸",
        "analysis": "你的凝血系统及骨骼“水泥”储备偏低。维 K 负责合成凝血因子（止血），并在维D的配合下，把血液中的钙精准“搬运”进骨骼，防止血管钙化。",
        "diet": "首选：羽衣甘蓝、菠菜（富含K1），以及纳豆、发酵乳制品（富含K2）。",
        "supplement": "如果正在服用高剂量维D和钙片，强烈建议搭配维生素 K2 (MK-7形式) 同服。服用抗凝血药者请遵医嘱。"
    }
}

# ==========================================
# 3. 核心视图渲染函数 (保留你的多巴胺UI)
# ==========================================
def show_vitamin_test():
    st.markdown("""
        <style>
        .stApp { background-color: #fafaf9; color: #1c1917; font-family: 'Noto Sans SC', 'Poppins', sans-serif; }
        #MainMenu, footer {visibility: hidden;}
        .stProgress > div > div > div > div { background: linear-gradient(90deg, #fdba74 0%, #f97316 100%); border-radius: 1rem; }
        div.stButton > button {
            background: white; color: #44403c; border: 1px solid #e7e5e4;
            border-radius: 1.25rem !important; padding: 0.8rem 1.5rem !important;
            font-size: 1.1rem !important; font-weight: 500 !important;
            transition: all 0.2s ease !important; box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
            display: block; width: 100%; text-align: center !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px); border-color: #f97316 !important;
            color: #f97316 !important; box-shadow: 0 10px 15px -3px rgba(249, 115, 22, 0.1) !important;
            background-color: #fff7ed !important;
        }
        div.stButton > button:active { transform: scale(0.98) !important; background-color: #ffedd5 !important; }
        button[key="back_btn"], button[key="reset_btn"] {
            height: 2.5rem !important; border-radius: 20px !important; color: #a8a29e !important;
        }
        .result-card {
            background-color: white; border-radius: 2.5rem; padding: 2.5rem;
            box-shadow: 0 25px 50px -12px rgba(249, 115, 22, 0.15); border: 1px solid rgba(255,255,255,0.8);
        }
        .tag-pill {
            display: inline-block; background-color: #fff7ed; color: #ea580c;
            font-size: 0.85rem; font-weight: bold; padding: 0.35rem 1rem;
            border-radius: 9999px; border: 1px solid #ffedd5; margin: 0.2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'vitamin_step' not in st.session_state:
        st.session_state.vitamin_step = 0
        st.session_state.vit_scores = {k: 0.0 for k in MAX_SCORES.keys()}

    step = st.session_state.vitamin_step
    total_q = len(VITAMIN_QUESTIONS)

    if step < total_q:
        st.markdown(f"<h3 style='text-align: center; color: #f97316;'>🧬 潜意识身体扫锚中... ({step+1}/{total_q})</h3>", unsafe_allow_html=True)
        st.progress((step + 1) / total_q)
        st.write("---")
        
        current_q = VITAMIN_QUESTIONS[step]
        st.markdown(f"<h2 style='text-align: center; margin: 2rem 0; color: #2D3748;'>{current_q['q']}</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            # 选项逻辑：计算权重乘数 (经常=2, 偶尔=1, 没有=0)
            def record_answer(multiplier):
                for vit, weight in current_q["weights"].items():
                    st.session_state.vit_scores[vit] += weight * multiplier
                st.session_state.vitamin_step += 1
                st.rerun()

            if st.button("🔴 经常如此", key=f"q_{step}_2"): record_answer(2.0)
            if st.button("🟡 偶尔这样", key=f"q_{step}_1"): record_answer(1.0)
            if st.button("🟢 几乎没有", key=f"q_{step}_0"): record_answer(0.0)

        st.write("")
        if step > 0:
            _, col_b2, _ = st.columns([1,1,1])
            with col_b2:
                # 为了防止分数错乱，在这个简单架构中，建议隐藏返回按钮，或重新开始。
                # 此处保留原逻辑，但注意如果追求极端精确，返回上一题需要扣减上一题已加的分数。
                if st.button("🔄 重新开始测验", key="back_btn", use_container_width=True):
                    st.session_state.vitamin_step = 0
                    st.session_state.vit_scores = {k: 0.0 for k in MAX_SCORES.keys()}
                    st.rerun()

    else:
        # 计算相对缺乏度 (得分 / 理论最高分)
        deficiency_rates = {}
        for vit, score in st.session_state.vit_scores.items():
            rate = score / MAX_SCORES[vit] if MAX_SCORES[vit] > 0 else 0
            deficiency_rates[vit] = rate
        
        # 排序找出最缺乏的一项
        max_vit = max(deficiency_rates, key=deficiency_rates.get)
        max_rate = deficiency_rates[max_vit]
        
        if max_rate == 0:
            result_data = {
                "name": "全面健康！毫无缺乏", "icon": "🌟",
                "analysis": "完美！你的身体机能运转得像一台精密的瑞士钟表。你目前的饮食结构和作息习惯非常优秀。",
                "diet": "保持现在的多元化饮食习惯，继续摄入五颜六色的蔬菜和优质蛋白。",
                "supplement": "目前不需要任何额外的维生素补剂，大自然就是你最好的营养师！"
            }
        else:
            result_data = VITAMIN_ANALYSIS[max_vit]

        st.markdown("<h1 style='text-align: center; color: #f97316; font-size: 3rem;'>分析报告生成完毕 📋</h1>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown(f"""
            <div class="result-card">
                <div style="text-align:center; font-size: 5rem; margin-bottom: -1rem;">{result_data['icon']}</div>
                <h2 style="text-align: center; color: #f97316; font-size: 2.2rem;">你目前最需要补充：<br>{result_data['name']}</h2>
                
                <div style="margin-top: 2rem;">
                    <span class="tag-pill">🩺 症状追踪解析</span>
                    <p style="margin-top: 0.5rem; line-height: 1.8;">{result_data['analysis']}</p>
                </div>
                
                <div style="margin-top: 1.5rem;">
                    <span class="tag-pill">🥗 多巴胺饮食处方</span>
                    <p style="margin-top: 0.5rem; line-height: 1.8;">{result_data['diet']}</p>
                </div>
                
                <div style="margin-top: 1.5rem;">
                    <span class="tag-pill">💊 科学补剂指南</span>
                    <p style="margin-top: 0.5rem; line-height: 1.8;">{result_data['supplement']}</p>
                </div>
                
                <div style="margin-top: 1.5rem; font-size: 0.85rem; color: #9ca3af; border-top: 1px solid #f3f4f6; padding-top: 1rem;">
                    <strong>Spectrum 医学免责声明：</strong>本测试基于加权统计算法设计，用于发现潜在的营养短板，不构成医疗诊断。如果有严重不适，请及时就医进行全血微量元素检测。
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        _, col_r2, _ = st.columns([1,1,1])
        with col_r2:
            if st.button("🔄 重新测试", key="reset_btn", use_container_width=True):
                st.session_state.vitamin_step = 0
                st.session_state.vit_scores = {k: 0.0 for k in MAX_SCORES.keys()}
                st.rerun()
