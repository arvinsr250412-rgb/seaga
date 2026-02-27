import streamlit as st
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm
from contents import apply_contents_settings


apply_contents_settings()

# --- 1. 页面配置 ---
st.set_page_config(page_title="Spectrum | 灵魂城市测试", layout="centered")

# 重点：这段逻辑能确保无论在本地还是云端，都能准确找到根目录的字体
def get_font():
    # 获取当前文件所在文件夹（pages）的父目录（根目录）
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(base_dir, "simhei.ttf")
    
    if os.path.exists(font_path):
        return fm.FontProperties(fname=font_path)
    else:
        st.error("字体文件丢失，请检查根目录是否有 simhei.ttf")
        return None

# 在 draw_radar 内部调用
prop = get_font()
# --- 1. 页面配置与视觉样式 ---
    # 复用主页的 hero-title，并加入副标题

    
    # 多巴胺糖果风格的契合度卡片 (高对比度，绝不会看不清字)
def show_soul_city():
  

    # 设置中文支持
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 维度名称定义
    D_NAMES = ["事业搞钱", "环境气候", "生活节奏", "人文底蕴", "自然景观", "社交活力"]
    # 缩写映射表（用于解析题目中的权重）
    KEY_MAP = {"E": "事业搞钱", "C": "环境气候", "P": "生活节奏", "V": "人文底蕴", "G": "自然景观", "S": "社交活力"}
    # --- 1. 样式配置 (多巴胺色彩增强) ---
    # --- 在 show_soul_city 的 st.markdown Style 块中替换 ---
    # --- 1. 样式配置 (清新多巴胺风格：白底彩边) ---
    st.markdown("""
        <style>
        :root {
            --dopamine-gradient: linear-gradient(45deg, #FF6B6B, #FF8E99, #FFAD7D);
        }
        /* 页面背景清爽白 */
        .stApp { background-color: #FFFFFF; }

        /* 题目文字：保持大号且清晰 */
        .q-text {
            font-size: 2.2rem !important; 
            font-weight: 800 !important;
            color: #2D3748 !important;
            margin-bottom: 30px !important;
            line-height: 1.4 !important;
        }

        /* 重点：白底+彩色边框按钮 */
        section[data-testid="stMain"] div.stButton > button {
            background-color: #FFFFFF !important; /* 白色背景 */
            border: 3px solid !important; /* 明显的边框 */
            border-color: #FF8E99 !important; /* 默认粉色边框 */
            border-radius: 20px !important;
            padding: 1.2rem 2rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(255, 142, 153, 0.1) !important;
        }

        /* 按钮文字：暖色调 */
        section[data-testid="stMain"] div.stButton > button p {
            color: #FF6B6B !important; /* 浅红字体 */
            font-size: 1.3rem !important;
            font-weight: 700 !important;
        }

        /* 悬停效果：边框变为橙色 */
        section[data-testid="stMain"] div.stButton > button:hover {
            border-color: #FFAD7D !important; /* 橙色边框 */
            background-color: #FFF9F9 !important; /* 极浅粉背景 */
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(255, 173, 125, 0.2) !important;
        }

        /* 结果页：超大城市名 */
        .massive-city-title {
            font-size: 100px !important; /* 极大字体 */
            font-weight: 900 !important;
            text-align: center;
            background: linear-gradient(45deg, #FF6B6B, #FF8E99, #FFAD7D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 40px 0 !important;
            line-height: 1.1;
        }

        /* 题目卡片：简化为白底微阴影 */
        .q-card {
            background: white;
            padding: 30px;
            border-radius: 30px;
            text-align: center;
            margin: 0 auto;
        }
        /* 选项按钮深度美化 */
        section[data-testid="stMain"] div.stButton > button {
            background-color: #FFFFFF !important;
            border: 2px solid #F0F2F6 !important; /* 初始淡色边框 */
            border-radius: 16px !important;
            padding: 1rem 2rem !important;
            min-height: 4rem !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }
        
        /* 悬停时边框变色并放大 */
        section[data-testid="stMain"] div.stButton > button:hover {
            border-color: #FF8E99 !important;
            color: #FF6B6B !important;
            transform: scale(1.02) translateY(-2px);
            box-shadow: 0 10px 20px rgba(255, 142, 153, 0.15) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    if 'history' not in st.session_state:
        st.session_state.history = []  # 用于存放每一题选择后的分数快照
    # --- 2. 核心初始化 ---
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'scores' not in st.session_state:
        st.session_state.scores = {n: 0 for n in D_NAMES}
    
    if 'quiz_data' not in st.session_state:
        raw_qs = [
        {"q": "1. 如果余生只能拥有一种天气，你选？", "a": [("永远干爽的晴天", {"C":3}), ("烟雨朦胧的湿润", {"C":-1, "V":2}), ("大雪纷飞的冬日", {"C":-3}), ("阳光灿烂的酷暑", {"C":1, "G":2})]},
        {"q": "2. 下班后，你最希望出现在哪种场景？", "a": [("灯火通明的CBD办公楼", {"E":3, "P":-2}), ("闹哄哄的街边大排档", {"S":3, "V":1}), ("空无一人的海边栈道", {"G":3, "P":2}), ("富有艺术气息的博物馆", {"V":3, "E":1})]},
        {"q": "3. 面对‘火锅’，你的第一反应是？", "a": [("热辣滚烫的社交聚会", {"S":3, "V":1}), ("精致清淡的养生局", {"C":2, "P":1}), ("一个人的孤独美食", {"P":2}), ("高端奢华的商务宴请", {"E":2})]},
        {"q": "4. 你理想的通勤方式是？", "a": [("走路或骑行 10 分钟", {"P":3, "G":1}), ("地铁里观察城市众生相", {"S":2, "V":1}), ("独自驾驶私家车", {"E":1, "P":-1}), ("随时随地远程办公", {"G":2, "P":3})]},
        {"q": "5. 关于‘搞钱’，你的真实想法是？", "a": [("卷死别人，追求财务巅峰", {"E":3, "P":-3}), ("生活第一，赚钱够花就行", {"P":3, "C":1}), ("追求稳定，最好是体制内", {"E":-1, "P":2}), ("靠兴趣变现，做独立个体", {"V":2, "G":1})]},
        {"q": "6. 你的社交频率通常是？", "a": [("没有局活不下去的社牛", {"S":3, "E":1}), ("三五知己小酌足矣", {"V":2, "S":1}), ("独自登山或冲浪的驴友", {"G":3, "P":1}), ("宅家即正义的深度社恐", {"P":3})]},
        {"q": "7. 你最爱的‘城市声音’是什么？", "a": [("车水马龙的繁忙喧嚣", {"E":2, "S":1}), ("清脆的鸟鸣与风铃声", {"G":2, "C":2}), ("菜市场的人间烟火气", {"V":3, "S":1}), ("夜晚寂静的小巷深处", {"P":3, "V":1})]},
        {"q": "8. 你对‘暖气/空调’的依赖度？", "a": [("命是恒温设备给的", {"C":4}), ("喜欢自然风，冷热都能扛", {"C":-2, "G":2}), ("只要空气好，温度不重要", {"G":2}), ("越极端越刺激（如极寒/酷热）", {"G":3, "C":-2})]},
        {"q": "9. 你理想中的邻里关系？", "a": [("点头之交，极度隐私", {"E":2, "P":1}), ("远亲不如近邻，经常串门", {"S":3, "V":1}), ("共享爱好的社群伙伴", {"S":2, "V":2}), ("方圆几里最好没邻居", {"G":3, "P":3})]},
        {"q": "10. 关于穿衣，你更倾向于？", "a": [("西装革履的精致职场风", {"E":3}), ("舒适第一的拖鞋短裤", {"P":3, "C":1}), ("潮牌或先锋艺术穿搭", {"V":3, "S":2}), ("全副武装的户外冲锋衣", {"G":3, "C":1})]},
    
        # --- 11-20 题：价值观与城市感知 ---
        {"q": "11. 发现一处隐藏的古迹，你会？", "a": [("拍照发朋友圈记录生活", {"S":3}), ("研究其历史变迁", {"V":3}), ("感叹城市发展的冲突", {"E":1, "V":1}), ("单纯享受那片刻的宁静", {"P":2, "G":1})]},
        {"q": "12. 你如何看待‘方言’？", "a": [("很有文化韵味，想学", {"V":3, "S":1}), ("听不懂，还是普通话方便", {"E":2}), ("生活气息的灵魂所在", {"V":2, "P":1}), ("无所谓，交流明白就行", {"P":2})]},
        {"q": "13. 你的居住空间偏好？", "a": [("俯瞰全城的云端公寓", {"E":3, "P":-1}), ("带小院的市井老房", {"V":3, "P":2}), ("面朝大海的海景房", {"G":3, "C":1}), ("极简主义的酒店公寓", {"E":2, "P":1})]},
        {"q": "14. 面对突如其来的‘慢生活’，你会？", "a": [("感到焦虑，总想找点事做", {"E":3, "P":-3}), ("如释重负，开启放空模式", {"P":3}), ("开始钻研厨艺或插花", {"V":2, "C":1}), ("立刻出发去野外徒步", {"G":3})]},
        {"q": "15. 你对‘网红打卡地’的态度？", "a": [("积极参与，体验潮流", {"S":3, "E":1}), ("嗤之以鼻，觉得肤浅", {"V":2}), ("如果风景确实好也会去", {"G":2}), ("完全不关注，避开人流", {"P":3})]},
        {"q": "16. 深夜两点，你认为城市应该是？", "a": [("灯火辉煌，夜生活刚开始", {"S":3, "E":2}), ("万籁俱寂，适合睡眠", {"P":3, "C":2}), ("路灯孤寂，适合沉思", {"V":2}), ("能听到远处的涛声或虫鸣", {"G":3})]},
        {"q": "17. 你的职业发展路径选择？", "a": [("去大厂/名企当一颗螺丝钉", {"E":3}), ("做个自由职业者/博主", {"S":2, "P":2}), ("回老家考公考编", {"E":-1, "P":3}), ("创业，开家自己喜欢的小店", {"V":2, "S":1})]},
        {"q": "18. 关于教育资源，你觉得？", "a": [("必须是全国最顶尖的", {"E":3, "V":1}), ("只要能正常升学就行", {"P":2}), ("更看重素质教育与大自然", {"G":3, "P":1}), ("还没考虑过这个问题", {"P":2})]},
        {"q": "19. 你对‘潮湿’环境的接受度？", "a": [("完全不行，必须干干爽爽", {"C":4}), ("很喜欢那种润润的感觉", {"C":-2, "V":1}), ("只要不发霉，潮点没事", {"C":1}), ("没感觉，空气好就行", {"G":2})]},
        {"q": "20. 什么是你眼中的‘成功’？", "a": [("坐拥财富与社会地位", {"E":3}), ("能按自己的意愿过一生", {"P":3}), ("作品被历史记住", {"V":3}), ("走过全世界的山川湖海", {"G":3, "V":1})]},
    
        # --- 21-30 题：细节抉择与灵魂底色 ---
        {"q": "21. 周末你想去哪里远足？", "a": [("古镇老街寻找灵感", {"V":3}), ("未开发的原始森林", {"G":3, "C":-1}), ("现代感十足的主题公园", {"E":2, "S":2}), ("近郊农家乐采摘", {"P":2, "S":1})]},
        {"q": "22. 你的饮食口味倾向？", "a": [("重口味，越辣越带劲", {"V":1, "S":2}), ("追求食材本味，极其清淡", {"C":3, "G":1}), ("喜欢精致甜点或下午茶", {"S":2, "E":1}), ("简单粗犷，能吃饱就行", {"P":2})]},
        {"q": "23. 你更喜欢哪种美感？", "a": [("钢筋水泥的几何美", {"E":3}), ("错落有致的山水画卷", {"G":3}), ("残缺斑驳的古城墙", {"V":3}), ("一尘不染的极简街道", {"C":3})]},
        {"q": "24. 如果放假一年，你会？", "a": [("去一线城市疯狂进修", {"E":3}), ("在某个海边小镇发呆", {"G":3, "P":3}), ("回乡下种菜养花", {"P":3, "C":1}), ("游遍全国吃美食", {"V":2, "S":2})]},
        {"q": "25. 你如何评价‘快节奏’生活？", "a": [("兴奋，这才是活着的感觉", {"E":3, "P":-3}), ("疲惫，每天都想逃离", {"P":3}), ("可以适应，但必须有休息", {"E":1, "P":1}), ("无所谓，我有自成体系的节奏", {"P":2, "V":1})]},
        {"q": "26. 你的娱乐首选是？", "a": [("万人合唱的演唱会", {"S":3, "E":1}), ("安静的小剧场话剧", {"V":3}), ("露营烧烤看星星", {"G":3, "P":1}), ("单机游戏或追剧", {"P":3})]},
        {"q": "27. 你对‘人口老龄化’城市的直观感受？", "a": [("太沉闷，喜欢年轻人多的地方", {"E":3, "S":2}), ("很有生活气息，安详舒缓", {"P":3, "V":1}), ("只要医疗条件好，没关系", {"E":1, "C":1}), ("没想过这个问题", {"P":2})]},
        {"q": "28. 面对交通拥堵，你会？", "a": [("焦虑暴躁，狂按喇叭", {"P":-3, "E":2}), ("听播客或音乐，享受独处", {"P":2, "V":1}), ("直接改骑自行车或步行", {"G":2, "C":1}), ("已经习惯了，这就是大城市", {"E":2, "S":1})]},
        {"q": "29. 你理想中的‘退休生活’？", "a": [("在繁华地段含饴弄孙", {"E":1, "S":2}), ("在深山老林里修禅", {"G":3, "P":3}), ("在全球各大城市旅居", {"V":2, "G":2}), ("继续发光发热，做志愿者", {"S":2, "V":2})]},
        {"q": "30. 最后，如果你要定义自己的一生，你会选？", "a": [("奋斗过，拥有过", {"E":3}), ("快乐过，自在过", {"P":3, "C":1}), ("见识过，记录过", {"G":2, "V":3}), ("被爱过，社交过", {"S":3})]}
        ]
        # 填充至30道（示例保留，实际应用中建议补充完整）
        while len(raw_qs) < 30:
            raw_qs.append({"q": "在陌生的城市街头，你更倾向于？", "a": [("探索现代商业中心", {"E":2}), ("寻找宁静的小巷", {"P":2}), ("观察当地人的生活", {"V":2}), ("去近郊徒步登山", {"G":2})]})
        
        random.shuffle(raw_qs)
        st.session_state.quiz_data = raw_qs
    
    # --- 3. 城市数据库 (保持不变) ---
    CITY_DB = {
       "上海": {
            "tag": "秩序、效率与边界感的巅峰",
            "soul": "你是一个典型的‘秩序构建者’。在你的世界观里，平庸的温情远不如清晰的规则来得可靠。你拥有极强的时间管理能力和目标导向思维，甚至在社交中也带着一种隐形的效率评估。你并不排斥压力，甚至在某种程度上，你享受这种被高强度节奏打磨出的精英感。你的情感表达是内敛且精准的，比起感性的誓言，你更相信契约精神。",
            "city": "上海不相信眼泪，但它绝对尊重专业。它是中国最接近‘文明游乐场’的地方，其核心魅力在于‘互不打扰的默契’。在这里，你不需要向邻居解释你的生活方式，也不需要为了合群而牺牲个人边界。陆家嘴的玻璃幕墙映照出你的野心，而梧桐区深处的咖啡馆则安放了你对精致生活的最后坚持。这是一座认钱、认才、认规则的城市，它能给像你这样清醒的逐利者提供最公平的赛道。它不强迫你融入，只提供你成长的土壤。",
            "advice": "建议住在具有历史感与现代感交织的街区（如徐汇区）。你的生命能量需要通过这种‘互不打扰的默契’来维持。建议你建立一套极度自律的早间仪式，在这座城市还没苏醒前，先完成与自我的对话。"
        },
        "成都": {
            "tag": "人间烟火里的松弛感哲学",
            "soul": "你是一个温柔的叛逆者。你拒绝被外部社会的‘成功学’逻辑绑架，在你的价值体系里，‘快乐’与‘自由’的权重远高于‘地位’与‘财富’。你拥有极高的感官敏感度，能从一碗茶的香气、一阵雨的节奏中提取出生命的真味。你看起来随和，但内心对于‘我想过什么样的生活’有着极强的防御机制，任何试图异化你生活的企图都会被你优雅地消解掉。",
            "city": "成都是一座能抚平集体焦虑的孤岛。它拥有某种‘消解宏大叙事’的力量。在这里，再大的事业也大不过晚上的那顿火锅。它适合你这种追求‘灵性生活’的灵魂。成都不需要你证明什么，它只想让你慢一点。这种安逸并非堕落，而是一种对生命的温柔尊重。你可以在玉林路的巷子里消磨一个下午，也可以在太古里的潮流中寻找灵感。",
            "advice": "选一个带露台的房子是必须的。你的灵魂需要接触‘地气’。不要去卷那些虚无的KPI，在这个城市，会生活才是真正的本事。建议多去周边的青城山静修，平衡你的感知力。"
        },
        "北京": {
            "tag": "帝都之巅的格局与孤独",
            "soul": "你的灵魂深处藏着一种‘宏大叙事’。你关心的往往超越了个体本身，带着一种天然的责任感或对权力的敏锐直觉。你拥有极强的韧性，能忍受极端的孤独与粗糙，只要你能感受到自己正处于某种旋涡的中心。你有一种骨子里的自傲，这种傲气来自于见多识广，也来自于对这种‘复杂秩序’的深度理解。",
            "city": "北京不是用来生活的，它是用来战斗和对话的。这是一座充满了‘门槛’的城市，厚重、干涩、甚至有时显得冷酷，但它给你的‘格局感’是其他任何城市无法替代的。你可以一边在什刹海的冰场上感受晚清的残晖，一边在工位上改写互联网的规则。这种巨大的割裂感反而是你创造力的来源。北京适合野心巨大或情怀深重的人，它会让你明白：在时代的洪流面前，个人是渺小的。",
            "advice": "你需要学会‘苦中作乐’。建议多结交一些有思想的‘北漂’老友，在这种灵魂的碰撞中，抵抗帝都的寒冷。多去故宫和胡同走走，那是这座城市最温柔的底色。"
        },
        "深圳": {
            "tag": "效率至上的硅谷蓝本",
            "soul": "你是一个纯粹的进化论者。你讨厌怀旧，认为沉溺于过去是效率的敌人。你拥有极强的适应能力和一种近乎冒险家的乐观主义。在你看来，阶层跃迁不是一种可能，而是一种必然的使命。你的社交圈通常基于价值共鸣，而非情感捆绑。",
            "city": "深圳是中国唯一没有‘爹味’的城市，它是年轻人的大型实验室。这里的空气里飘着金钱与汗水的味道，适合那些不问出身、只问前程的灵魂。你在这里可以随时推倒重来，没有人会因为你的失败而嘲笑你，因为每个人都在奔跑。这里的快节奏是你心跳的共振器。",
            "advice": "保持空杯心态。建议在南山区感受科技的脉动。你的生活提案是：尽可能缩短通勤，把省下的时间投资在自我的认知边界拓宽上。"
        },
        "西安": {
            "tag": "古墙下的千年回响",
            "soul": "你拥有一个怀旧且厚重的文人内核。你不追求那些转瞬即逝的热点，你追求的是某种穿越周期的、永恒的东西。你沉稳、内敛，内心深处有一种对文明与历史的敬畏感。你是一个极其念旧的人，习惯在旧物中寻找未来的线索。",
            "city": "西安是一座可以对话的城市。每一块砖、每一粒尘埃都带有历史的残韵。它适合你这种喜欢沉思、不愿随波逐流的人。在这里，你可以沿着城墙骑行，看着落日消失在钟楼的飞檐之后。这种历史的沉重感不会压抑你，反而会给你一种踏实的安全感。它提醒你，无论外界如何变幻，有些根基永远不会动摇。",
            "advice": "你需要偶尔去碑林或大雁塔静坐。在快节奏的时代，西安是你最好的‘减速带’。建议在这里建立自己的深度社交圈，这里的友情和这座城市一样，经得起时间的打磨。"
        },
        "杭州": {
            "tag": "山水与算法共生的新隐士",
            "soul": "你是一个矛盾的统一体。你既迷恋数字时代的效率，又渴望中国古典主义的优雅。你擅长在喧嚣中寻找宁静，在算法中植入情怀。你的性格中有一种‘儒商’的气质，既懂生存的逻辑，又不愿放弃灵魂的审美。",
            "city": "杭州的迷人之处在于：你在阿里巴巴的园区里敲完代码，转头就能走进西湖的烟雨中。它提供了一种‘入世’与‘出世’的完美切换。它适合那些既想搞钱，又不想把灵魂丢掉的人。这里的山色空蒙是你精神的避难所，而这里的创新活力则是你物质的保障。",
            "advice": "一定要住在能看到山或水的地方。你的能量场需要流动的景观。建议多去龙井茶园漫步，在满眼翠绿中消解掉工作带来的数字焦虑。"
        },
        "南京": {
            "tag": "六朝烟雨中的儒雅文士",
            "soul": "你是一个典型的‘慢性子智慧者’。你不急于表达，更倾向于观察。你的内心有一股不卑不亢的劲头，对权威不盲从，对浮华不艳羡。你的人生哲学更接近‘守拙’，在纷乱的世界里守住自己的一方天地。",
            "city": "南京有一种被历史洗礼后的宽容与淡然。它不像素州那样娇柔，也不像上海那样凌厉。秦淮河的水流淌着某种哀而不伤的情绪，这种情绪最契合你内心的柔软。这里不仅有浓厚的学术氛围，还有一种不急不躁的生活逻辑。你在灵谷寺的深林里，能找到真正的自我归属感。",
            "advice": "建议住在靠近城墙或高校的区域。你的生活提案是：每周读一本无用之书，去紫金山晨爬，在历史的呼吸中校准自己的生命时钟。"
        },
        "厦门": {
            "tag": "文艺海风里的精致漫步者",
            "soul": "你是一个典型的唯美主义者。你对生活质量的要求近乎苛刻，但这种苛刻不是针对金钱，而是针对‘美感’。你渴望一种清透的、不被物欲完全填满的生活。你的性格温和且细腻，像是一首轻盈的小诗。",
            "city": "厦门是海风与花香的实验室。这里的节奏快慢刚好够你呼吸。它适合那些不急于抵达终点，而想看清沿途每一朵花的灵魂。环岛路的骑行、沙坡尾的午后、以及鼓浪屿的老洋房，构成了你梦境的物理投影。这是一座被温柔包裹的城市，它能软化你所有的防备。",
            "advice": "你的生活不能缺少下午茶。选一个能看到海的窗户，保持你对美的敏感。你的生活提案是：在每一个日落时分，放下手机，去海边听听浪潮的频率。"
        },
        "长沙": {
            "tag": "不眠星城的生命力原力",
            "soul": "你是人间的一抹亮色，生命力在你身上呈现出一种近乎野蛮的爆发态。你热爱那种热气腾腾的混乱感，认为秩序是死亡的代名词。你是一个典型的‘直觉型社交家’，喜欢通过味觉、酒精和喧闹来确认存在的意义。你的情绪是辛辣且直接的，不矫揉造作。",
            "city": "长沙是中国最具‘不夜城’气质的城市。当其他城市开始入睡，长沙的派对才刚刚开始。这是一座充满了草莽气息和生命原力的城市。它不高级，但它极度鲜活。解放西路的灯火、五一广场的人潮、还有满街的湘味辛辣，共同构建了一个避开文明压抑的出口。如果你觉得生活变得灰暗窒息，长沙就是那剂强效肾上腺素。",
            "advice": "你的生活不应该有排班表。去拥抱长沙的深夜文化，在最嘈杂的街头找回你的灵感。你适合从事具有创造性且高强度的社交型工作，因为你的能量来自于人与人的连接。"
        },
        "大理": {
            "tag": "苍山洱海间的逃离主义者",
            "soul": "你是一个彻底的自由主义者，或者说，你是一个灵魂层面的‘异乡人’。你对主流社会的成功标准感到厌倦甚至窒息。你一直在寻找一种‘轻装上阵’的生活，渴望摆脱所有的身份标签。你的人生理想不是拥有更多，而是放下更多。",
            "city": "大理不是一座城市，它是一个巨大的疗愈场。它是所有‘内卷难民’的精神母港。这里的风花雪月不是形容词，而是真实的生活边界。你可以在洱海边无所事事地坐一个下午，没有人会问你的KPI。这里容纳所有的奇行怪癖，欢迎所有的流浪灵魂。大理给了你一种幻觉，也给了一种可能：生活可以完全由自己定义。",
            "advice": "别带任何目标去大理。选一个村落住下，学会和当地的云对话。你的提案是：切断所有的无效社交，在半农半学的状态中找回失落已久的纯真。"
        },
        "拉萨": {
            "tag": "雪域高原的精神信徒",
            "soul": "你拥有一个极度纯净且渴望‘神圣感’的内核。你对物质的欲望极低，对精神世界的广度有着近乎执着的追求。你适合在高海拔的稀薄空气中呼吸，因为那种孤独与辽阔能让你看清生命的本质。你有一种天生的虔诚感，无论你信仰什么，你都会全身心投入。",
            "city": "拉萨是离天空最近的圣地。这里的日光能洗净灵魂的尘垢。它适合那些想要彻底清算过去、重启人生的人。布达拉宫的红墙、八廓街的转经道、以及远处的雪山，共同构成了一个超越世俗的时间维度。在这里，时间是静止的，呼吸是有分量的。它不是用来旅游的，它是用来归宿的。",
            "advice": "在拉萨生活需要极大的勇气。建议你在高压生活的间歇去那里‘闭关’。你的提案是：学会沉默，在朝圣者的脚步声中，寻找你失散多年的信仰。"
        },
        "重庆": {
            "tag": "赛博朋克里的江湖豪侠",
            "soul": "你是一个极具反差感的人。外表粗犷、直接，内心却有一种极度细腻的柔情。你不怕困难，甚至喜欢挑战那些看似不可能的‘地形’。你的人生信条里有极强的江湖义气，认为‘诚’与‘义’比任何合同都管用。你是一个典型的体验派，喜欢大开大合的人生。",
            "city": "重庆是三维甚至四维的，它是真实版的《银翼杀手》。层叠的建筑、穿墙而过的轻轨、雾气朦胧的江面，共同构建了一个魔幻现实主义的舞台。这种硬朗与混乱交织的城市，最能激发你体内的野性。在这里，你不需要保持优雅，你只需要保持鲜活。火锅的雾气能掩盖你的眼泪，而南山的夜色能包容你所有的孤独。",
            "advice": "你适合在洪崖洞附近的嘈杂中寻找宁静。建议去爬那些数不清的梯坎，在肌肉的酸痛中感受生命的阻力与张力。你的提案是：活得痛快，爱得真切，不留遗憾。"
        },
        "苏州": {
            "tag": "园林深处的现代极简主义",
            "soul": "你是一个温润如玉、注重细节的人。你讨厌粗鲁和喧闹，向往一种有分寸感、有仪式感的生活。你的审美趋向于古典，但在逻辑上又非常现代。你是一个精致的打理者，擅长把微小的生活碎片拼成精美的挂毯。",
            "city": "苏州是水做的城市，它有一种‘隔代’的优雅。它在工业化的高新区与古朴的平江路之间找到了完美的平衡。它适合那些既需要现代设施，又无法割舍园林情怀的人。在这里，你可以穿着最时髦的衣服走在两千年的石板路上，这种时空交错感会让你着迷。苏州的‘慢’是有质量的慢，是慢而有序。",
            "advice": "一定要去听一曲评弹。你的提案是：建立一个极具审美的小空间，在这个空间里复刻某种失传的文人生活方式。记住，精致不是钱，是心境。"
        },
        "青岛": {
            "tag": "红瓦绿树间的豪爽绅士",
            "soul": "你是一个浪漫且大气的现实主义者。你既爱大海的辽阔，又爱啤酒的泡沫。你的性格中有一种北方人的豪爽，又有一种海洋文明带来的开阔与洋气。你对生活有一种天然的掌控力，不急功近利，也不得过且过。",
            "city": "青岛是带有海盐味的欧式梦境。红瓦、绿树、蓝天、碧海，这种配色是你灵魂的底色。它既有老城区的历史沉淀，又有新区的新潮活力。在八大关的林荫道上，你能感受到某种永恒的宁静。这里的空气是凉爽且带有活力的，它能激发你对生活最原始的热爱。",
            "advice": "一定要在盛夏喝袋装啤酒。你的生活提案是：每周末去海边走走，让负氧离子清理掉职场的负能量。在生活与工作之间，像大海一样保持自己的潮汐节奏。"
        },
        "广州": {
            "tag": "万商云集的务实生活家",
            "soul": "你是一个极致的务实主义者。你讨厌虚名，崇尚实干。在你看来，一顿好吃的早餐比一场华丽的演讲更有意义。你的人生信条是‘平平淡淡才是真’，但在赚钱和吃饭这两件事上，你绝不含糊。你拥有极强的包容心，能和各种阶层的人打成一片。",
            "city": "广州是中国最没有‘包袱’的一线城市。在这里，你可以开着劳斯莱斯吃路边摊，没有人会觉得违和。这是一座被‘胃’统治的城市，也是一座被‘商魂’驱动的城市。它市井且高效，平民且强大。它不需要你立人设，它只想让你活得舒服。这里的早茶文化是你精神的按摩器。",
            "advice": "建议住在靠近老城区的地段。你的提案是：钻进那些弯曲的小巷，在寻找地道美食的过程中，发现生活的真谛。记住，务实是你最大的武器。"
        },
        "武汉": {
            "tag": "大江大湖的爽朗拓荒者",
            "soul": "你是一个内心宽广、性格刚毅的人。你有一种不信邪、不服输的劲头。你的人生观里有一种‘码头文化’留下的爽快——行就行，不行就拉倒。你讨厌扭捏作态，喜欢直球对决。你的承受力极强，像武汉的夏天一样热烈。",
            "city": "武汉是庞大且狂放的。长江与汉江在这里交汇，把城市撕裂也把城市连接。这种大水大山的地理特征，塑造了这里的人，也塑造了这种充满野性的生命力。这里的过早是一种信仰，这里的江景是一种豪情。武汉适合那些有冲劲、有担当的灵魂，它会让你变得更加硬朗。",
            "advice": "一定要去江滩走走。你的提案是：在每一个重要的人生节点，去江边吹吹风，让大江大湖的开阔校正你的视野。保持你的爽朗，那是你最迷人的地方。"
        },
        "昆明": {
            "tag": "四季如春的温和派诗人",
            "soul": "你是一个性格温顺、内心充满阳光的人。你讨厌极端，渴望平衡。你的人生理想不是征服世界，而是与世界和平相处。你有一种天然的‘疗愈力’，身边的朋友总能从你这里获得能量。你是一个典型的‘知足常乐’者。",
            "city": "昆明是‘春城’，不仅是气候，更是心境。这里的生活没有大起大落，只有细水长流。它适合那些看透了都市虚荣，只想回归自然节律的人。翠湖的红嘴鸥、斗南的花市、以及永远灿烂的阳光，构成了你生活的舒适区。这是一座不会让人感到压力的城市。",
            "advice": "把你的阳台摆满鲜花。你的提案是：保持你的温和，不要被外界的焦虑所污染。每天晒半小时太阳，那是你灵魂的燃料。"
        },
        "哈尔滨": {
            "tag": "冰雪王国的浪漫极北",
            "soul": "你是一个外冷内热、具有极强仪式感的人。你喜欢冬日的肃杀，也热爱室内的温暖。你的性格中有一种‘铁汉柔情’，在粗糙的环境里能开出极度浪漫的花朵。你有一种天生的幽默感和豁达感，懂得在艰难中苦中作乐。",
            "city": "哈尔滨是远东的巴黎，它是冰与火的交响。中央大街的欧式建筑、圣索菲亚大教堂的穹顶，在雪中有一种神圣的忧郁美。这种美最契合你内心的深情。这里的冬天极长，但也因为长，才让温暖显得如此珍贵。它是北方人的浪漫巅峰。",
            "advice": "在最冷的冬天吃一支冰棍。你的提案是：学会欣赏寒冷带来的宁静。在生活的风雪中，守住你内心那炉跳动的炭火。"
        },
        "大连": {
            "tag": "北方之珠的清爽绅士",
            "soul": "你是一个追求体面、性格爽朗的人。你非常在意自己的形象和生活品质，有一种不自知的优越感（在好的意义上）。你喜欢干净、有序的环境，对新鲜事物保持着强烈的好奇心。你是一个典型的‘海洋型北方人’。",
            "city": "大连是北方的异类，它有一种清爽的‘海派’气息。广场、电车、欧式洋房，构成了它的城市肌理。它不臃肿，不沉重。这里的大海是深蓝色的，带有一种力量感。它适合那些既想保留北方人的豪迈，又想追求精致生活的灵魂。",
            "advice": "去滨海路徒步。你的提案是：保持你的清爽与自信。在海风的吹拂下，剔除掉生活中的所有杂质。"
        },
        "珠海": {
            "tag": "百岛之城的秩序与海风",
            "soul": "你是一个追求极致舒适与秩序的人。你讨厌混乱和拥堵，认为‘宜居’是人权的一部分。你的性格温和且理智，不随波逐流。你的人生观更接近于现代文明的典范——有序、干净、克制。",
            "city": "珠海是中国最不像工地的城市。情侣路的漫长是你对生活耐心的隐喻。这里的每一个海岛都是一个避难所。它适合那些已经完成了原始积累，想要安静享受生活成果的人。它的秩序感能给你极大的安全感。",
            "advice": "去离岛住几天。你的提案是：学会慢生活，在海平面上寻找人生的平衡点。记住，秩序就是自由。"
        },
        "三亚": {
            "tag": "北纬18度的海洋极乐者",
            "soul": "你是一个感官至上主义者。你热爱阳光、肉体、派对和一切能让多巴胺分泌的事物。你讨厌压抑和伪善，认为快乐是生命的唯一真谛。你有一种野性的魅力，不被世俗的条条框框所束缚。",
            "city": "三亚是中国唯一的真正热带天堂。它剥离了所有的严肃，只剩下娱乐和放松。它是所有疲惫灵魂的加油站。这里的海浪声是你心跳的鼓点。它不要求你进步，它只要求你爽。它是欲望的释放地，也是自由的试验田。",
            "advice": "买一件最鲜艳的沙滩裙/裤。你的提案是：彻底放空，去感受阳光对皮肤的灼烧感。在每一个当下，尽情燃烧。"
        },
        "扬州": {
            "tag": "烟花三月的精致慢活者",
            "soul": "你是一个典型的‘生活美学大师’。你认为生活是由无数个细节构成的：早茶的包子褶、修脚的力度、园林的窗棂。你有一种近乎匠人的执着，要把每一件平凡的小事都过成艺术。你的性格温婉、细腻，带有一种天然的江南底色。",
            "city": "扬州是用来养老的，也是用来养心的。这里的‘慢’是出了名的。早上的早茶，晚上的修脚，是这座城市的节奏。它适合那些看透了繁华，只想在细节中寻找意义的人。它有一种旧时代的风流，这种风流最契合你内心的风骨。",
            "advice": "一定要在阳春三月去。你的提案是：慢下来，慢到能看清茶杯里的叶子如何舒展。记住，快是别人的，慢才是你自己的。"
        },
        "天津": {
            "tag": "幽默知足的津门乐天派",
            "soul": "你是一个天生的乐天派。你拥有极强的化解困难的能力——通常是用一个段子。你的人生观非常通透：赚多赚少，吃饱就好。你讨厌装腔作势，喜欢接地气的交流。你是一个极具亲和力的人，是社交圈里的润滑剂。",
            "city": "天津是一座‘不争’的城市。它紧邻京城，却自成一格。这里的洋楼、海河、相声，构成了它的独特幽默。它适合那些追求安稳、知足常乐的人。在这里，你会发现生活其实没有那么多苦大仇深。它能软化你的棱角，让你笑出声来。",
            "advice": "一定要在五大道溜达。你的提案是：活得幽默一点。在遭遇生活的不顺时，去听场相声，或者自己在生活里找个包袱。乐呵，就是最大的成功。"
        },
        "郑州": {
            "tag": "坚韧踏实的黄河建设者",
            "soul": "你是一个极其坚韧、稳重的人。你的人生观是基石式的——一点一滴积累，不求捷径。你对家庭、对责任有着极强的担当。你可能不是最耀眼的，但你一定是最可靠的。你有一种像大地一样的包容力和生命力。",
            "city": "郑州是中原的心脏，它是坚实且厚重的。作为铁路枢纽，它见证了无数的迁徙与归来。这种流动的背景塑造了它的务实与勤奋。它适合那些脚踏实地、想要通过双手改变命运的人。它虽然没有那么精致，但它极具安全感，它是奋斗者的后盾。",
            "advice": "去省博看一看。你的提案是：保持你的踏实，在快速变动的时代里，做一颗最稳固的钉子。你的价值，时间会给出证明。"
        }
    }
    # 城市特征矩阵 (顺序对应 D_NAMES: 事业, 环境, 节奏, 人文, 景观, 社交)
    CITY_MATRIX = {
        "上海": [10, 5, 2, 8, 3, 9], "成都": [5, 6, 10, 8, 7, 9], "北京": [9, 3, 1, 10, 4, 8],
        "深圳": [10, 6, 1, 4, 5, 8], "西安": [5, 4, 7, 10, 5, 6], "杭州": [8, 8, 6, 9, 8, 7],
        "南京": [6, 6, 7, 9, 6, 5], "厦门": [4, 9, 8, 6, 10, 7], "长沙": [6, 5, 6, 7, 5, 10],
        "大理": [2, 8, 10, 7, 10, 6], "拉萨": [1, 5, 9, 10, 10, 3], "重庆": [7, 4, 6, 6, 8, 10],
        "苏州": [7, 7, 8, 9, 7, 5], "青岛": [6, 9, 7, 6, 9, 7], "武汉": [8, 5, 5, 7, 6, 8],
        "昆明": [4, 10, 9, 6, 9, 5], "哈尔滨": [5, 3, 7, 8, 7, 8], "大连": [6, 8, 7, 5, 9, 6],
        "珠海": [5, 9, 9, 4, 9, 5], "三亚": [3, 9, 10, 2, 10, 8], "扬州": [3, 7, 10, 9, 6, 4],
        "天津": [6, 6, 8, 7, 4, 7], "郑州": [7, 5, 6, 6, 4, 5], "广州": [9, 6, 4, 7, 5, 9]
    }
    # ==========================================
    # 4. 功能函数
    # ==========================================
    def draw_radar(s):
        import matplotlib.font_manager as fm
        import os
    
        # 尝试寻找云端环境下可用的中文字体
        font_path = "simhei.ttf" # 假设你把字体文件也传到了 GitHub 根目录
        if os.path.exists(font_path):
            prop = fm.FontProperties(fname=font_path)
        else:
            # 如果没传字体文件，尝试调用 Linux 系统自带的（虽然通常没有中文）
            prop = fm.FontProperties(family='sans-serif')
        
    
        labels = list(s.keys())
        values = list(s.values())
        
        # 数据闭合
        num_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        
        # 2. 创建画布 (背景透明，方便融入 Streamlit)
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True), facecolor='none')
        
        # --- 核心修改：将多边形变为圆形 ---
        ax.set_theta_offset(np.pi / 2) # 设置顶点从正上方开始
        ax.set_theta_direction(-1)     # 顺时针排列
        

        # 将 fill 和 plot 的颜色微调为更柔和的粉橙色
        ax.fill(angles, values, color='#FF8E99', alpha=0.3) # 增加透明度
        ax.plot(angles, values, color='#FF8E99', linewidth=3, marker='o', 
                markersize=8, markerfacecolor='white', markeredgecolor='#FF8E99')
                
        # 3. 圆形背景美化
        # 设置圆形网格线（关键步：使用 set_rgrids 指定圆圈）
        max_val = max(max(values), 10) # 确保有足够的空间
        ax.set_ylim(0, max_val * 1.1)
        
        # 隐藏极坐标的射线（多边形边框）
        ax.spines['polar'].set_visible(False)
        
        # 设置网格线样式
        ax.xaxis.grid(True, color='#D1D5DB', linestyle='--', linewidth=0.8) # 维度轴线
        ax.yaxis.grid(True, color='#E5E7EB', linestyle='-', linewidth=1)    # 圆形环绕线
        
        # 4. 修复坐标轴标签
        ax.set_xticks(angles[:-1])
        # 手动放置维度名称，增加间距以防重叠
        for angle, label in zip(angles[:-1], labels):
            # 计算文字位置：让文字稍微远离圆心
            alignment = 'left' if 0 <= angle < np.pi else 'right'
            ax.text(angle, max_val * 1.25, label, 
                    fontproperties=prop, size=12, weight='bold',
                    color='#1F2937', ha='center', va='center')
    
        # 隐藏默认的数字刻度
        ax.set_yticklabels([])
        ax.set_xticklabels([]) 
    
        return fig
    # ==========================================
    # 5. 流程控制
    # ==========================================
    # --- 5. 流程控制 (答题逻辑与结果展示) ---
    
    if st.session_state.step < 30:
    
        # --- 2. 彩色答题界面 UI 渲染 ---
        # --- 多巴胺色彩主副标题 ---
        st.markdown("""
            <div style="text-align: center; padding: 20px 0; margin-bottom: 10px;">
                <h1 style="
                    font-size: 4.5rem !important; 
                    font-weight: 900 !important; 
                    background: linear-gradient(45deg, #FF00CC, #3333FF, #00FFCC); 
                    -webkit-background-clip: text; 
                    -webkit-text-fill-color: transparent; 
                    margin-bottom: 5px;
                    text-shadow: 10px 10px 20px rgba(0,0,0,0.05);
                    font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
                ">
                    🌆 灵魂城市测试
                </h1>
            </div>
        """, unsafe_allow_html=True)
        if st.session_state.step < len(st.session_state.quiz_data):
            # --- 1. 数据预处理 ---
            curr_q = st.session_state.quiz_data[st.session_state.step]
            raw_q_text = curr_q.get('q', "题目载入中...")
            
            # 清洗题号逻辑
            display_q = raw_q_text.split(". ", 1)[-1] if ". " in raw_q_text else raw_q_text
            
            # 计算当前进度百分比
            progress_val = (st.session_state.step) / 30 # 使用 step 表现已完成比例
    
            
            
            
            # 彩色进度条
            st.progress(progress_val)
    
            # 答题卡片
            st.markdown(f"""
                <div class="q-card">
                    <div style="color: #3B82F6; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 2px;">
                        Step {st.session_state.step + 1} of 30
                    </div>
                    <div class="q-text">{display_q}</div>
                </div>
            """, unsafe_allow_html=True)
    
            # 选项按钮：垂直排列
            st.markdown('<div style="margin-top: -10px;"></div>', unsafe_allow_html=True)
            
            for idx, (ans_text, weight) in enumerate(curr_q.get("a", [])):
                if st.button(ans_text, key=f"ans_{st.session_state.step}_{idx}", use_container_width=True):
                    # 【新增逻辑】在变动分数前，备份当前状态
                    st.session_state.history.append(st.session_state.scores.copy())
                    
                    # 记录分数
                    for dim_key, score_val in weight.items():
                        full_dim_name = KEY_MAP.get(dim_key)
                        if full_dim_name in st.session_state.scores:
                            st.session_state.scores[full_dim_name] += score_val
                    
                    # 自动进入下一题
                    st.session_state.step += 1
                    st.rerun()
    
            # --- 3. 【新增】撤回功能区 ---
            # 仅在步数大于 0 时（即非第一题）显示
            if st.session_state.step > 0:
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("⬅ 上一题", key="undo_action"):
                        # 弹出历史栈顶的分数镜像
                        prev_scores = st.session_state.history.pop()
                        st.session_state.scores = prev_scores
                        # 进度回退
                        st.session_state.step -= 1
                        st.rerun()
    
            # 底部的视觉点缀
            st.markdown(f"""
                <div style="text-align: center; color: #BDC3C7; font-size: 0.8rem; margin-top: 30px;">
                    您的每一次选择，都在勾勒灵魂的轮廓
                </div>
            """, unsafe_allow_html=True)
    else:
        # --- 1. 核心计算：寻找首选与次选城市 ---
        st.balloons()
        user_scores = st.session_state.scores
        
        # 标准化用户向量 (1-10 范围)
        raw_values = np.array([user_scores[d] for d in D_NAMES])
        max_raw = max(raw_values) if max(raw_values) > 0 else 1
        user_vec = (raw_values / max_raw) * 10
        
        # 计算所有城市的欧氏距离并排序
        city_distances = []
        for city_name, city_vec in CITY_MATRIX.items():
            dist = np.linalg.norm(user_vec - np.array(city_vec))
            city_distances.append({"name": city_name, "dist": dist})
        
        city_distances.sort(key=lambda x: x["dist"])
        
        # 提取前两名
        match_1 = city_distances[0]
        match_2 = city_distances[1]
        
        # 契合度换算逻辑
        def calc_rate(dist):
            return int(max(min(100 - (dist * 5), 99), 60))
    
        rate_1 = calc_rate(match_1["dist"])
        rate_2 = calc_rate(match_2["dist"])
        
        res1 = CITY_DB.get(match_1["name"])
        res2 = CITY_DB.get(match_2["name"])
    
        # --- 2. 结果页顶部：标题与契合度 ---
        # --- 结果展示逻辑 ---
        st.markdown(f'<div class="massive-city-title">{match_1["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center; font-size:1.5rem; color:#FF8E99; font-weight:bold;">{res1["tag"]}</p>', unsafe_allow_html=True)

        
        st.markdown(f"""
            <div style="display: flex; justify-content: center; gap: 20px; margin: 20px 0;">
                <div style="background: linear-gradient(135deg, #FF9A8B 0%, #FF6A88 100%); padding: 20px 30px; border-radius: 30px; box-shadow: 0 15px 30px rgba(255,106,136,0.3); text-align: center; flex: 1;">
                    <div style="color: #FFFFFF; font-size: 1rem; font-weight: 800; opacity: 0.9; letter-spacing: 1px;">首选契合度</div>
                    <div style="color: #FFFFFF; font-size: 2.8rem; font-weight: 900; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">{rate_1}%</div>
                </div>
                <div style="background: white; padding: 20px 30px; border-radius: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 3px solid #FF99AC; text-align: center; flex: 1;">
                     <div style="color: #FF6A88; font-size: 1rem; font-weight: 800; letter-spacing: 1px;">次选参考</div>
                    <div style="color: #2D3748; font-size: 2.8rem; font-weight: 900;">{rate_2}%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        # --- 3. 灵魂画像 ---
        st.markdown(f"""
            <style>
            .soul-card {{
                padding: 35px 30px; 
                border-radius: 30px;
                background: #FFFFFF;
                border: 3px solid transparent;
                background-clip: padding-box;
                color: #2D3748;
                margin: 30px 0; 
                box-shadow: 0 20px 40px rgba(255, 106, 136, 0.12);
                position: relative;
            }}
            .soul-card::before {{
                content: ''; position: absolute; top: 0; right: 0; bottom: 0; left: 0;
                z-index: -1; margin: -3px; border-radius: inherit;
                background: var(--dopamine-gradient);
            }}
            .soul-title {{ 
                color: #DD2476; 
                font-weight: 900; 
                font-size: 1.3rem; 
                margin-bottom: 15px; 
                text-align: center;
                letter-spacing: 2px;
            }}
            .soul-text {{
                line-height: 1.8; 
                font-size: 1.1rem; 
                text-align: justify;
                font-weight: 500;
            }}
            </style>
            <div class="soul-card">
                <div class="soul-title">✨ 灵魂画像 · PORTRAIT</div>
                <div class="soul-text">{res1['soul']}</div>
            </div>
        """, unsafe_allow_html=True)
    
        # 展示雷达图
        st.pyplot(draw_radar(user_scores))
    
        # --- 4. 城市详情 (Tabs) ---
        st.markdown("""
            <style>
            .stTabs [data-baseweb="tab"] p { color: #9CA3AF !important; font-weight: 600 !important; transition: 0.3s; }
            .stTabs [data-baseweb="tab"][aria-selected="true"] p { color: #DD2476 !important; font-weight: 900 !important; }
            .stTabs [data-baseweb="tabHighlight"] { background-color: #DD2476 !important; }
            </style>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs([f"📍 首选：{match_1['name']}", f"🔍 次选：{match_2['name']}"])
    
        with tab1:
            st.markdown(f"""
                <div style="background: #FFF0F5; padding: 25px; border-radius: 20px; border-left: 6px solid #FF6A88; margin-top:20px;">
                    <b style="color:#DD2476; font-size: 1.1rem;">🏙️ 城市共鸣：</b>
                    <p style="color:#2D3748; margin-top:10px; line-height: 1.7;">{res1['city']}</p>
                </div>
                <div style="background: #FFF5EE; padding: 25px; border-radius: 20px; border-left: 6px solid #FF9A8B; margin-top:15px;">
                    <b style="color:#FF512F; font-size: 1.1rem;">🌿 生活提案：</b>
                    <p style="color:#2D3748; margin-top:10px; line-height: 1.7;">{res1['advice']}</p>
                </div>
            """, unsafe_allow_html=True)
    
        with tab2:
            st.markdown(f"""
                <div style="background: #FAFAFA; padding: 25px; border-radius: 20px; border-left: 6px solid #A0AEC0; margin-top:20px;">
                    <b style="color:#4A5568; font-size: 1.1rem;">🏙️ 城市共鸣：</b>
                    <p style="color:#2D3748; margin-top:10px; line-height: 1.7;">{res2['city']}</p>
                </div>
                <div style="background: #FFF5EE; padding: 25px; border-radius: 20px; border-left: 6px solid #FF9A8B; margin-top:15px;">
                    <b style="color:#FF512F; font-size: 1.1rem;">🌿 生活提案：</b>
                    <p style="color:#2D3748; margin-top:10px; line-height: 1.7;">{res2['advice']}</p>
                </div>
            """, unsafe_allow_html=True)
    
        # --- 5. 底部重置按钮 (这里是关键：必须保持缩进！) ---
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("✨ 重新开启灵魂之旅", use_container_width=True, key="reset_quiz"):
            if not st.session_state.get("admin_logged_in", False):
                st.session_state.unlocked_Orientation = False # 关键！
            for k in list(st.session_state.keys()): 
                del st.session_state[k]     
            st.rerun()
            
if __name__ == "__main__":
    show_soul_city()































