import streamlit as st
import plotly.graph_objects as go
import os
import time
import base64
import random
def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ==========================================
# 1. 题库与结果数据字典 (5维度均衡版)
# ==========================================
# 维度说明：A(酸-敏感/文艺) B(甜-治愈/温柔) C(苦-深沉/理智) D(辣-热烈/勇敢) E(咸-踏实/现实/烟火气)
# 全库包含：20个A，20个B，20个C，20个D，20个E，做到绝对的数学均衡。
DISH_QUESTIONS = [
    # 1-5题：将原有的 D 替换为 E
    {"id": 1, "text": "如果你变成了一只狗，你会？", "options": [{"dim": "A", "text": "坐在窗边看雨想心事"}, {"dim": "B", "text": "疯狂向路人摇尾索抱"}, {"dim": "C", "text": "躲在桌下观察人类"}, {"dim": "E", "text": "找个舒服的窝先睡一觉"}]},
    {"id": 2, "text": "你希望你的墓志铭写着？", "options": [{"dim": "A", "text": "他曾来过"}, {"dim": "B", "text": "世界很好，下次还来"}, {"dim": "C", "text": "加载失败，用户已注销"}, {"dim": "E", "text": "此人已结账离店"}]},
    {"id": 3, "text": "如果记忆可以买卖，你最想买回？", "options": [{"dim": "A", "text": "某个蝉鸣的夏日午后"}, {"dim": "B", "text": "初恋时笨拙的告白"}, {"dim": "C", "text": "某个顿悟的人生瞬间"}, {"dim": "E", "text": "小时候兜里的一块糖"}]},
    {"id": 4, "text": "镜子里的人突然对你笑，你？", "options": [{"dim": "A", "text": "感到一阵莫名的悲伤"}, {"dim": "B", "text": "觉得它终于活过来了"}, {"dim": "C", "text": "思考这是否是平行时空"}, {"dim": "E", "text": "默默擦干净镜子上的水渍"}]},
    {"id": 5, "text": "所谓的“爱”，在你看来更像？", "options": [{"dim": "A", "text": "潮湿天气里长出的青苔"}, {"dim": "B", "text": "照进深海里的一束光"}, {"dim": "C", "text": "止痛片过后的副作用"}, {"dim": "E", "text": "一顿准时准点的热饭"}]},
    
    # 6-10题：将原有的 C 替换为 E
    {"id": 6, "text": "人生落幕前60秒，你最后一件事是？", "options": [{"dim": "A", "text": "闭上眼回忆某个人的脸"}, {"dim": "B", "text": "拥抱身边最柔软的东西"}, {"dim": "E", "text": "清空浏览器历史记录"}, {"dim": "D", "text": "向上帝竖起中指"}]},
    {"id": 7, "text": "如果情绪有味道，遗憾的味道是？", "options": [{"dim": "A", "text": "没熟透的青柠檬"}, {"dim": "B", "text": "冬天玻璃上凝结的窗花"}, {"dim": "E", "text": "隔夜变硬的冷馒头"}, {"dim": "D", "text": "呛出眼泪的干辣椒粉"}]},
    {"id": 8, "text": "你发现世界是一场模拟游戏，你会？", "options": [{"dim": "A", "text": "寻找那个最初的漏洞"}, {"dim": "B", "text": "寻找游戏里的快乐 NPC"}, {"dim": "E", "text": "该干嘛干嘛，明天还要上班"}, {"dim": "D", "text": "试图黑掉这个系统的后台"}]},
    {"id": 9, "text": "必须住进一幅画里，你会选择？", "options": [{"dim": "A", "text": "莫奈的《睡莲》"}, {"dim": "B", "text": "梵高的《向日葵》"}, {"dim": "E", "text": "清明上河图里的包子铺"}, {"dim": "D", "text": "毕加索的《格尔尼卡》"}]},
    {"id": 10, "text": "深夜电台播放了一首没听过的歌，你？", "options": [{"dim": "A", "text": "猜测写词人的暗恋故事"}, {"dim": "B", "text": "跟着旋律轻轻摇晃身体"}, {"dim": "E", "text": "查一下这首歌的版权和原唱"}, {"dim": "D", "text": "想要立刻学会并在街头大唱"}]},
    
    # 11-15题：将原有的 B 替换为 E
    {"id": 11, "text": "假如你可以拥有一种超能力？", "options": [{"dim": "A", "text": "能够看到别人的梦境"}, {"dim": "E", "text": "每天多出两个小时睡眠"}, {"dim": "C", "text": "能看透所有谎言"}, {"dim": "D", "text": "随时可以引发一场爆炸"}]},
    {"id": 12, "text": "如果你是一个标点符号，你会是？", "options": [{"dim": "A", "text": "……"}, {"dim": "E", "text": "，"}, {"dim": "C", "text": "。"}, {"dim": "D", "text": "——"}]},
    {"id": 13, "text": "你会选择如何度过“永恒的一天”？", "options": [{"dim": "A", "text": "独自写一本没人看的日记"}, {"dim": "E", "text": "把家里彻底打扫一遍"}, {"dim": "C", "text": "坐在图书馆看书直到日落"}, {"dim": "D", "text": "在无人区进行一场流浪"}]},
    {"id": 14, "text": "此时此刻，你的灵魂颜色是？", "options": [{"dim": "A", "text": "忧郁且透明的淡紫"}, {"dim": "E", "text": "大地般朴实的卡其色"}, {"dim": "C", "text": "沉稳压抑的深矿黑"}, {"dim": "D", "text": "极具侵略性的金黄色"}]},
    {"id": 15, "text": "森林里出现了一扇不该存在的门，门后是？", "options": [{"dim": "A", "text": "堆满旧玩具的童年房间"}, {"dim": "E", "text": "一家24小时营业的便利店"}, {"dim": "C", "text": "一面映照真实的镜子"}, {"dim": "D", "text": "巨大的原始火山口"}]},
    
    # 16-20题：将原有的 A 替换为 E
    {"id": 16, "text": "暴雨中陌生人给你递伞后离去，你会？", "options": [{"dim": "E", "text": "赶紧回家洗个热水澡防感冒"}, {"dim": "B", "text": "觉得世界充满爱"}, {"dim": "C", "text": "思考对方是否别有用心"}, {"dim": "D", "text": "想要追上去认识对方"}]},
    {"id": 17, "text": "如果沉默有颜色，那会是？", "options": [{"dim": "E", "text": "斑驳的旧墙皮色"}, {"dim": "B", "text": "奶糖般的温润白"}, {"dim": "C", "text": "浓郁到化不开的灰"}, {"dim": "D", "text": "极其扎眼的电光紫"}]},
    {"id": 18, "text": "假如人生是一场电影，你希望结局是？", "options": [{"dim": "E", "text": "平平淡淡的流水账"}, {"dim": "B", "text": "所有人都在笑的大团圆"}, {"dim": "C", "text": "戛然而止的黑屏"}, {"dim": "D", "text": "壮烈且震撼的爆炸"}]},
    {"id": 19, "text": "看到流星划过，你的第一反应是？", "options": [{"dim": "E", "text": "算算是不是会有极端天气"}, {"dim": "B", "text": "闭眼虔诚许愿"}, {"dim": "C", "text": "思考陨石的化学成分"}, {"dim": "D", "text": "想要伸手去抓住那道光"}]},
    {"id": 20, "text": "最后一顿饭，你只想吃？", "options": [{"dim": "E", "text": "妈妈做的那道家常菜"}, {"dim": "B", "text": "一块酱料丰富合你口味的蛋糕"}, {"dim": "C", "text": "一杯不加奶糖的浓缩"}, {"dim": "D", "text": "最重口味的街边摊"}]},
    
    # 21-25题：保留原始 ABCD
    {"id": 21, "text": "如果你是一棵树，你希望长在？", "options": [{"dim": "A", "text": "终年大雾的悬崖边"}, {"dim": "B", "text": "充满笑声的公园中心"}, {"dim": "C", "text": "无人踏足的原始深山"}, {"dim": "D", "text": "车水马龙的CBD"}]},
    {"id": 22, "text": "你发现自己能听懂猫说话，它第一句是？", "options": [{"dim": "A", "text": "别再为那个人难过了"}, {"dim": "B", "text": "嘿，你要来点小鱼干吗"}, {"dim": "C", "text": "人类的行为逻辑真愚蠢"}, {"dim": "D", "text": "跟我去毁灭这个世界吧"}]},
    {"id": 23, "text": "走入一间空的艺术展厅，正中间放着？", "options": [{"dim": "A", "text": "一面破碎的落地镜"}, {"dim": "B", "text": "一个不断旋转的八音盒"}, {"dim": "C", "text": "一张写满数学公式的纸"}, {"dim": "D", "text": "一个巨大的红色拳击球"}]},
    {"id": 24, "text": "如果时间是一条河，你选择？", "options": [{"dim": "A", "text": "坐在岸边看它流逝"}, {"dim": "B", "text": "潜入水底摸索石头"}, {"dim": "C", "text": "逆流而上寻找源头"}, {"dim": "D", "text": "顺流而下直到入海"}]},
    {"id": 25, "text": "世界末日前最后 5 秒，你最后一句话是？", "options": [{"dim": "A", "text": "fucking this world"}, {"dim": "B", "text": "谢谢，我很开心。"}, {"dim": "C", "text": "让我自此长眠"}, {"dim": "D", "text": "来吧，让这一切更响亮！"}]}
]

# 5x4=20种维度组合 + 1种均衡，完美映射21道菜
DISH_RESULTS = [
    {"name": "老坛酸菜鱼", "portrait": "清醒、敏感、真诚", "goldSentence": "够酸够辣，但也够真。", "match": ["A_EXTREME"], "description": "测出这个结果的你，灵魂里住着一个带着刺的诗人。酸菜鱼的底色是酸，正如你对世界天然的敏锐与“防备”。你总是能精准地捕捉到空气里微小的冷热变化，甚至是社交场上那些不易察觉的虚伪。人们觉得你有时显得“刺儿头”或是不合群，但那是因为你拒绝为了廉价的共鸣而稀释真实的自我。你的温柔是“无骨”的鱼肉，极其鲜嫩，却只留给穿过酸辣汤底、真正走进你心里的人。你习惯用毒舌和疏离保护内心的柔软，这种不迎合，是你对生命最后的坚持。即便身处酸楚的汤底，你仍要记得自己是一条跃龙门的鱼。"},
    {"name": "广式白斩鸡", "portrait": "纯粹、治愈、理想主义", "goldSentence": "拒绝包装，原汁原味。", "match": ["B_EXTREME"], "description": "在这个人人都在给自己加滤镜的时代，你是一道拒绝包装的白斩鸡。你的性格里有一种近乎偏执的‘真’。你讨厌弯弯绕绕的职场政治，也不屑于在社交网络上营造虚假的人设。对你来说，好就是好，坏就是坏，这种‘原汁原味’的理想主义让你在复杂的世界里显得既孤独又珍贵。你其实很聪明，能看穿所有的套路，但你选择不参与。你的治愈感来自于这种透明性——和你相处不需要猜谜，不需要设防。你是那种即使被误解，也会选择‘不解释、只做自己’的人，因为你深知，懂你的人自然懂那份皮爽肉滑下的赤诚真心。"},
    {"name": "99%浓黑咖啡", "portrait": "冷静、虚无、深刻", "goldSentence": "所有的热闹，都与我无关。", "match": ["C_EXTREME"], "description": "你是那个深夜里最清醒的旁观者。99%的浓苦不是生活的毒药，而是你对抗平庸的解药。你拥有一种近乎冷酷的理智，能够轻易剥离掉情感的伪装去直视事物的本质。这让你在人群中显得有些‘局外人’。你并不排斥社交，你只是觉得大部分的喧嚣都没有意义。你的孤独是主动选择的避难所，在那里你可以自由地思考生而为人的虚无与深刻。你习惯了自己消解负面情绪，不需要廉价的安慰。这种极致的独立让你拥有一种不可侵犯的尊严感。你可能看起来有点苦，但那种回甘，只有真正拥有独立灵魂的人才能品出其中的高级感。"},
    {"name": "辣子鸡丁", "portrait": "热烈、勇敢、狂欢", "goldSentence": "在废墟里，找最火热的快乐。", "match": ["D_EXTREME"], "description": "你是一个天生的生命力泵发者。如果生活是一座废墟，你就是在那废墟上跳舞的狂欢者。辣子鸡丁的灵魂在于‘找’，正如你在琐碎平庸的日常里，总能精准地挖出那颗名为‘快乐’的小肉丁。你活得极其灿烂，甚至带点侵略性，那种灼热的能量常常让胆小的人退缩，却让志同道合的人疯狂。你讨厌温水煮青蛙的安稳，你渴望沸腾，渴望燃烧，渴望在每一场冒险中感受到心跳。即便被现实辣得流泪，你也会抹干眼泪大喊一声：‘爽！’ 这种不计后果的英勇，是你给这个灰扑扑的世界最响亮的回击。"},
    {"name": "番茄炒蛋", "portrait": "治愈、平凡、可靠", "goldSentence": "平凡生活里的唯一解药。", "match": ["A", "B"], "description": "在人人都想做‘硬菜’的时代，你选择成为那个最温暖的守望者。番茄炒蛋是你灵魂的隐喻：既有对生活小遗憾的‘酸’，也有对未来小确幸的‘甜’。你拥有极强的共情能力，习惯于照顾每个人的情绪，是朋友圈里的‘定海神针’。你并不平庸，你只是在看过世间的浮躁后，选择回归那种握在手里的、热气腾腾的踏实。你拥有一种能让悲伤消融的天赋，就像这道菜总能拌匀所有人的委屈。不需要惊天动地的登场，只要你在，身边的人就会觉得：‘嗯，日子还没那么糟。’"},
    {"name": "鱼香肉丝", "portrait": "复杂、机敏、浪漫", "goldSentence": "没有鱼，但我有戏。", "match": ["A", "B", "D"], "description": "你是一个拥有多副面孔的‘精明浪漫主义者’。鱼香肉丝的奇妙在于：明明没有鱼，却能通过酸、甜、辣、咸的精准配比，营造出一种丰富的幻觉。这正如你的为人处世——你极其机敏，能根据不同的场合切换不同的频道，在任何环境里都能游刃有余。但这绝非虚伪，而是一种高级的生存艺术。你的底色是浪漫的，你喜欢在平凡的生活里制造一些‘加戏’的小惊喜。你的内心世界极其丰富，甚至有些拥挤。你是一个复杂的多面手，既能冷静地搞定麻烦，也能感性地为一场电影落泪。懂你的人会觉得你像一部读不完的侦探小说，每一页都有新发现。"},
    {"name": "锅包肉", "portrait": "坚硬、甜心、直率", "goldSentence": "外表倔强，内心认甜。", "match": ["B", "D"], "description": "你是那种典型的‘反差萌’。锅包肉的第一口是硬的，甚至带着某种咄咄逼人的酥脆，那是你为了保护自己而穿上的厚重铠甲。你说话直接，甚至有时显得有些倔强，不肯轻易低头。但只要有人能耐心穿透那层金黄的伪装，就会发现里头包裹着一颗极其柔软、甚至有点‘认甜’的心。你是一个极度渴望被偏爱的人，虽然嘴上不说，但内心其实非常温顺。你的‘辣’和‘刚’是给世界看的，你的‘甜’和‘软’是留给家人的。这种外冷内热的特质让你拥有一种迷人的张力，让你身边的人既怕你的小脾气，又离不开你的小温暖。"},
    {"name": "麻婆豆腐", "portrait": "爆发、执行、利落", "goldSentence": "即使碎了，也要冒着热气。", "match": ["C", "D"], "description": "测出麻婆豆腐的你，生命力正处于极其旺盛的‘沸腾期’。你活得极具颗粒感，讨厌一切拖泥带水和虚情假意。豆腐的碎，象征着你曾经历过的那些足以让你崩溃的瞬间，但你最牛的一点在于：即使被生活揉碎了，你依然要冒着热气，依然要辣出存在感。你的生命里没有‘将就’，爱就爱死，恨就恨死。你是一个侠义心肠的理想主义者，为了朋友或公义，你可以瞬间炸裂。虽然偶尔会因为锋芒太露而灼伤别人，但大家还是忍不住靠近你，因为你身上那种炽热的能量，是这个冷冰冰的世界最缺的燃料。"},
    {"name": "佛跳墙", "portrait": "深沉、复杂、精英", "goldSentence": "别乱猜，我底牌厚着呢。", "match": ["C", "A"], "description": "你是一个巨大的、迷人的谜题。佛跳墙之所以名贵，不在于它的名号，而在于它能将几十种性格迥异的‘阅历’焖在同一个坛子里，却能做到和而不同。你拥有极高的情绪容纳度，生活给你的苦、职场给你的辣、旧时光给你的酸，都被你用一种名为‘理智’的慢火炖成了浓郁的汤汁。你很少向外人剖析自己的心路历程，因为懂你的人不需要解释，不懂你的人根本读不出你这道菜的厚度。你是一个长情且极其自律的精英，外表风平浪静，内心波澜万丈，拥有那种‘泰山崩于前而色不变’的顶级定力。"},
    {"name": "一碗白米饭", "portrait": "包容、大智若愚、万能", "goldSentence": "没标签，因为能容万物。", "match": ["BALANCED"], "description": "这是一个概率只有 1% 的天选结果。你已经不再需要任何味道来定义自己，因为你本身就是万味的基石。白米饭看似无味，实则拥有最强大的包容度——它可以搭配酸、甜、苦、辣中的任何一种。这说明你的性格已经达到了一种惊人的‘中庸’与平衡。你不是没有性格，而是你已经学会了与所有的极端和解。你是一个极其清醒的‘大玩家’，看透了规则却不戳穿，身处闹市却心有旷野。你不需要通过变得怪异来彰显个性，因为在这纷繁复杂的餐厅里，只有你，是所有人最后都离不开的必需品。"},
    {"name": "深夜车仔面", "portrait": "韧性、烟火、随性", "goldSentence": "加什么料，我自己说了算。", "match": ["D", "B"], "description": "你是一个生命韧性极强的‘随遇而安者’。深夜车仔面的魅力在于它的烟火气和极高的自由度——无论生活把你扔进什么样的碗里，你都能自备酱料，活出一份有滋有味。你并不迷信那些高大上的成功学，你更看重此时此刻的一碗面、一场觉、一个能让你笑的人。你的性格里有一种极其宝贵的‘接地气’，这让你在任何逆境中都能快速找回生活的节奏。你活得非常通透：生活是自己的，加什么料，该由自己说了算。你是那种即使在谷底，也能煮出一碗热汤来安慰自己的人，这种自愈能力是你最强大的底牌。"},
    {"name": "臭豆腐", "portrait": "特立、独特、芬芳", "goldSentence": "懂的人，自然闻得到香。", "match": ["A", "D"], "description": "你是那种‘爱者极爱，恨者极恨’的极致存在。臭豆腐的特立独行是你灵魂的旗帜。你从来不指望全世界都能理解你，事实上，你甚至有点享受这种‘不被理解’的孤独感。你的性格底色是坚硬且真实的，你拒绝为了合群而修剪掉身上的棱角。这种极致的个性在平庸的人看来是‘臭’（难以理解），但在懂你的人眼里，那是这世间最珍贵的‘奇香’。你拥有极高的自我认同感，你的快乐不需要建立在他人的评价之上。你是那种即便被孤立，也能在自己的小世界里活得有声有色的奇特灵魂。"},
    {"name": "莲藕排骨汤", "portrait": "时间、迷人、真情", "goldSentence": "不赶时间，我慢火熬真情。", "match": ["B", "C"], "description": "你是一个‘时间的朋友’。莲藕排骨汤的最高境界在于慢火细熬，正如你的性格——越老越迷人，越处越有味。你讨厌现代社会那种快进式的节奏，无论是社交还是恋爱，你都更倾向于一种‘慢调子’。你相信真正的好东西都是需要耐心去交换的。你的理性让你能够抵御短期的诱惑，你的治愈让你对身边的人充满长久的温情。你是一个极好的倾听者和陪伴者，虽然话不多，但总能在关键时刻给人一种厚实的依靠感。你是那种即便世界再乱，也能守住内心一锅温润清汤的人。"},
    {"name": "皮蛋瘦肉粥", "portrait": "治愈、细腻、守候", "goldSentence": "世界很吵，我只在深夜懂你。", "match": ["B_LEAN"], "description": "你是一个极其安静且细腻的‘治愈系灵魂’。皮蛋瘦肉粥从不争抢餐桌的主位，但它却是每个生病、疲惫或失意的时刻最被渴望的存在。你的温柔是润物无声的，你不擅长激昂的演讲，却极擅长沉默的守候。你总是能敏锐地察觉到身边人的不快乐，并用一种极其得体、不带压力的方式去安慰对方。你更喜欢深夜和雨天，因为那是你和灵魂对话的时间。你是一个‘懂事’到让人心疼的人，习惯于向内消化所有的负能量，只向外展示那一抹温热的白。你是这个嘈杂世界里，最让人安心的一处静谧。"},
    {"name": "避风塘炒蟹", "portrait": "护短、霸气、极简", "goldSentence": "披荆斩棘，只为护短。", "match": ["D", "C"], "description": "你是那种极具保护欲的‘霸道温柔’。避风塘炒蟹的特点是金黄酥脆的蒜茸下藏着极硬的壳和极鲜的肉，这完美复刻了你的性格。你对自己在意的人有着近乎‘护短’的霸气，谁要是动了你的人，你绝对会像带刺的蟹壳一样反击。但在强悍的外表下，你对生活有着极其清醒的认知。你明白弱肉强食的规则，所以你努力让自己变得强大，只是为了在风浪里给身边的人围起一个‘避风塘’。你是一个极其值得信赖的伙伴，你的爱是带有防御性的、充满力量感的。你不需要甜言蜜语，你的每一个动作都在说：‘别怕，有我在。’"},
    {"name": "干煸豆角", "portrait": "干练、利落、直率", "goldSentence": "废话少说，直接干脆。", "match": ["D_LEAN"], "description": "你是一个讨厌废话的‘高效执行者’。干煸豆角去除了多余的水分，只留下最纯粹的焦香，正如你的人生观——极简、利落、结果导向。你极度反感那些华而不实的修辞和拖拖拉拉的流程。在生活中，你总是那个第一个发现问题并动手解决的人。你的性格里有一种健康的‘自恋’，你相信自己的判断，并且行动力极强。虽然偶尔会因为太过直接而显得不够委婉，但你的真诚和高效让你在任何团队中都是不可或缺的核心。你是一个活得很‘烫’的人，拒绝平庸，拒绝模糊，喜欢那种颗粒分明的清脆感。"},
    {"name": "水煮肉片", "portrait": "沸腾、沧桑、鲜活", "goldSentence": "沸腾过，才叫活过。", "match": ["C", "D", "A"], "description": "你是一个‘底色是辣，活法是烫’的生命斗士。水煮肉片的精髓在于那层滚烫的明油，它封锁住了食材的鲜美，展示出最激烈的沸腾。测出这个结果的你，内心深处一定藏着些鲜为人知的过往，但你拒绝以此示弱。你选择用一种更火热、更积极的方式去面对生活给你的捶打。你是一个极其复杂且迷人的个体，辣的刺激让你察觉真相，烫的理智让你接纳现实，果敢让你冲破黑暗。你的一生都在不断地自我重组和自我超越，对你来说，人生最大的意义不是安稳，而是那种‘沸腾’的痛快感。"},
    {"name": "扬州炒饭", "portrait": "严谨、精致、分明", "goldSentence": "颗粒分明，清白自守。", "match": ["C", "B"], "description": "你是一个追求‘秩序感’的精致主义者。扬州炒饭讲究颗粒分明，配料精准，正如你的生活哲学——边界清晰，拒绝模糊。你极度重视个人空间和隐私，讨厌那种毫无界限感的冒犯。你拥有一种近乎强迫症的审美，无论是桌面还是人生轨迹，你都希望它们是井然有序的。这种‘颗粒感’让你在社交中保持着一种恰到好处的疏离和礼貌。你并不高冷，你只是更倾向于用一种克制的、文明的方式去表达情感。你是一个极其可靠的人，答应过的事一定会做到，你的世界里没有‘大概’ and ‘也许’，只有分毫必争的精准和清白。"},
    {"name": "东坡肉", "portrait": "稳重、丰盈、从容", "goldSentence": "厚积薄发，不紧不慢。", "match": ["B", "D"], "description": "你是一个拥有‘钝感力’的智者。东坡肉的成功在于‘慢火焖’，这正是你的人生节奏——稳重丰盈，从容不迫。在这个被焦虑感驱动的时代，你依然能保持那种‘厚积薄发’的定力。你拥有一种极具福报的性格，看淡名利，却能最终获得名利；不紧不慢，却总能走在前面。你的生命厚度来自于你对美好的感知力和对目标的坚持力。你是一个极其宽厚的人，能够包容他人的愚蠢或冒犯，就像这块肉总能包容调料的侵略。这种从容不迫的生命状态，是你对浮躁世界最优雅对抗。"},
    {"name": "开水白菜", "portrait": "极致、深厚、淡然", "goldSentence": "最高级的清淡，最深的底蕴。", "match": ["C_RARE"], "description": "这是一个极其稀有的灵魂。开水白菜看似清如白水，实则是用无数山珍海味提炼后的极简。测出这个结果的你，已经进入了那种‘返璞归真’的境界。你的外表极其平和，甚至有些寡淡，但你的内心世界却深邃如海。你已经不再需要向外界炫耀任何东西，因为你所有的底气都内化成了那种淡然自若的气场。你拥有一种高级的清醒，能看穿所有的浮华，却依然愿意拥抱生活最本质的平淡。你是那种‘大隐隐于市’的人物，看似平凡的一叶菜心，实则承载着整座森林的底蕴和智慧。"},
    {"name": "速冻水饺", "portrait": "蛰伏、沉稳、爆发", "goldSentence": "暂时休眠，待时沸腾。", "match": ["HIDDEN"], "description": "你是一个正处于‘潜伏期’的观察者。速冻水饺的特质是暂时休眠，将所有的能量和鲜香都包裹在冷峻的外皮下。这或许是你现在的状态——你可能感到自己正被生活‘冰冻’或忽略，但你深知，这只是为了等待那锅沸腾的水。你拥有极强的忍耐力和自律心，在孤独中默默积攒实力。你讨厌那种无意义的社交挥霍，你更喜欢在安静中磨练技能。你是一个典型的‘爆发型选手’，一旦机会来临，你就会瞬间解冻，展示出惊人的生命张力。别被眼前的冰冷吓到，因为你深知：沸腾的那一刻，才是你真正的盛宴开始。"}
]

# ==========================================
# 2. 逻辑计算与绘图函数 (重构为纯排列组合映射)
# ==========================================
def calculate_dish_result(scores):
    total = sum(scores.values()) or 1
    percentages = {k: round((v / total) * 100) for k, v in scores.items()}
    
    # 获取排序后的维度 (例如: [('D', 12), ('A', 5), ...])
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top1_dim, top1_score = sorted_scores[0]
    top2_dim, top2_score = sorted_scores[1]
    min_score = sorted_scores[-1][1]
    
    # 1. 判定【一碗白米饭】 (绝对均衡)
    if (top1_score - min_score) <= 2:
        return next(d for d in DISH_RESULTS if 'BALANCED' in d['match']), percentages

    # 2. 判定【极致单属性】 (如果第一名比第二名高出很多，触发 EXTREME/LEAN 菜品)
    # 这里的阈值设为 4 分（可调），即某属性遥遥领先
    if (top1_score - top2_score) >= 4:
        extreme_match = f"{top1_dim}_EXTREME"
        lean_match = f"{top1_dim}_LEAN"
        for dish in DISH_RESULTS:
            if extreme_match in dish['match'] or lean_match in dish['match']:
                return dish, percentages

    # 3. 判定【Top 2 组合】 (收集所有符合 Top1+Top2 的菜品，随机选一个防止“首位覆盖”)
    candidates = []
    for dish in DISH_RESULTS:
        # 情况 A: 严格匹配 [Top1, Top2]
        if len(dish['match']) == 2 and dish['match'][0] == top1_dim and dish['match'][1] == top2_dim:
            candidates.append(dish)
        # 情况 B: 某些复杂菜品匹配三个维度 [Top1, Top2, Any]
        elif len(dish['match']) == 3 and top1_dim in dish['match'] and top2_dim in dish['match']:
            candidates.append(dish)

    if candidates:
        return random.choice(candidates), percentages

    # 4. 判定【稀有/隐藏兜底】 (如果以上都没中，随机给一个带有当前 Top1 标签的稀有菜)
    rare_candidates = [d for d in DISH_RESULTS if top1_dim in str(d['match'])]
    return random.choice(rare_candidates) if rare_candidates else DISH_RESULTS[0], percentages

def draw_radar_chart(percentages):
    # 增加咸(E)维度
    categories = ['甜<br>(B)', '苦<br>(C)', '辣<br>(D)', '酸<br>(A)', '咸<br>(E)']
    values = [
        percentages.get('B', 0), 
        percentages.get('C', 0), 
        percentages.get('D', 0), 
        percentages.get('A', 0),
        percentages.get('E', 0)
    ]
    
    # 闭合五角星路径
    values.append(values[0])
    categories.append(categories[0])
    
    hover_texts = [f"{cat.replace('<br>', '')}占比: {val}%" for cat, val in zip(categories, values)]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(249, 115, 22, 0.35)', 
        line=dict(color='#ea580c', width=2.5), 
        marker=dict(
            size=6, 
            color='#ffffff', 
            line=dict(color='#ea580c', width=2) 
        ),
        hoverinfo='text',
        hovertext=hover_texts 
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(values) + 15, 40)], # 因为分成了5份，单项最高分理论在40左右 
                showticklabels=False,
                gridcolor='rgba(231, 229, 228, 0.7)', 
                linecolor='rgba(0,0,0,0)', 
            ),
            angularaxis=dict(
                tickfont=dict(
                    size=13, 
                    color='#78716c', 
                    family="Noto Sans SC, sans-serif",
                    weight='bold' 
                ),
                gridcolor='rgba(231, 229, 228, 0.7)',
                linecolor='rgba(0,0,0,0)', 
                rotation=90,
                direction="clockwise"
            ),
            bgcolor='#fafaf9' 
        ),
        showlegend=False,
        margin=dict(l=65, r=65, t=40, b=40), 
        height=350, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    
    return fig

# ==========================================
# 3. 核心视图渲染函数
# ==========================================
def show_dish_test():
    st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] button[key="back_btn"] {
            height: 2rem !important;        
            width: auto !important;         
            min-height: 0px !important;     
            padding: 0px 1rem !important;   
            font-size: 0.8rem !important;   
            background-color: transparent !important; 
            border: 1px solid #e7e5e4 !important;    
            color: #a8a29e !important;      
        }
        div[data-testid="stHorizontalBlock"] button[key="back_btn"]:hover {
            color: #f97316 !important;
            border-color: #f97316 !important;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp {
            background-color: #fafaf9; 
            color: #1c1917; 
            font-family: 'Noto Sans SC', sans-serif;
        }
        div.stButton > button {
            background: white;
            color: #44403c;
            border: 1px solid #e7e5e4;
            border-radius: 1.25rem !important; 
            padding: 0.8rem 1.5rem !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            border-color: #f97316 !important;
            color: #f97316 !important;
            box-shadow: 0 10px 15px -3px rgba(249, 115, 22, 0.1) !important;
            background-color: #fff7ed !important;
        }
        div.stButton > button:active {
            transform: scale(0.96) !important;
            background-color: #ffedd5 !important;
        }
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #fdba74 0%, #f97316 100%);
            border-radius: 1rem;
        }
        [data-testid="stMain"] .stButton > button {
            height: auto !important;
            min-height: 4.5rem !important; 
            margin-bottom: 0.5rem;
            text-align: left !important;
            padding-left: 2rem !important;
        }
        .btn-primary > div > button {
            background-color: #f97316 !important; 
            color: white !important;
            font-weight: bold !important;
            font-size: 1.125rem !important;
            border-radius: 9999px !important; 
            border: none !important;
            box-shadow: 0 20px 25px -5px rgba(254, 215, 170, 0.5) !important;
            text-align: center !important;
            padding-left: 0 !important;
        }
        .btn-primary > div > button:hover {
            background-color: #ea580c !important; 
        }
        .result-card {
            background-color: white;
            border-radius: 2.5rem;
            padding: 2rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.5);
        }
        .tag-pill {
            display: inline-block;
            background-color: #fff7ed;
            color: #ea580c;
            font-size: 0.75rem;
            font-weight: bold;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            border: 1px solid #ffedd5;
            margin: 0.2rem;
        }
        [data-testid="stMain"] img {
            max-width: 300px !important; 
            height: auto !important;
            margin: 0 auto;
            display: block;
        }
        </style>
    """, unsafe_allow_html=True)

    # 初始化包含 E 维度
    if 'dish_step' not in st.session_state:
        st.session_state.dish_step = 0 
    if 'dish_scores' not in st.session_state:
        st.session_state.dish_scores = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
    if 'dish_history' not in st.session_state:
        st.session_state.dish_history = []
        
    # 【首页视图】
    if st.session_state.dish_step == 0:
        st.write("<br><br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.markdown("""
                <div style="text-align: center; margin-bottom: 2rem;">
                    <div style="width: 6rem; height: 6rem; background-color: #ffedd5; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 3rem; margin: 0 auto 2rem auto;">🥘</div>
                    <h1 style="font-size: 3rem; font-weight: 900; letter-spacing: -0.05em; color: #292524;">你是哪盘菜？</h1>
                    <p style="color: #a8a29e; font-size: 0.875rem; margin-bottom: 3rem; font-weight: 500;">25道灵魂拷问，揭秘你的精神味觉占比</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("起锅烧火", key="dish_start_btn", use_container_width=True):
                st.session_state.dish_step = 1
                st.session_state.dish_scores = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # 【答题视图】
    elif 1 <= st.session_state.dish_step <= len(DISH_QUESTIONS):
        q_idx = st.session_state.dish_step - 1
        q_data = DISH_QUESTIONS[q_idx]
        
        st.progress(st.session_state.dish_step / len(DISH_QUESTIONS))
        
        st.markdown(f"""
            <div style="margin-top: 2.5rem; max-width: 32rem; margin-left: auto; margin-right: auto; text-align: center;">
                <div style="color: #fb923c; font-family: 'Courier New', monospace; font-size: 0.9rem; 
                            font-weight: bold; margin-bottom: 1rem; letter-spacing: 0.1em;">
                    STEP {q_idx + 1} / 25
                </div>
                <h2 style="font-size: 2rem; font-weight: 800; color: #292524; 
                           margin-bottom: 3.5rem; line-height: 1.4; min-height: 5rem;
                           letter-spacing: -0.02em; padding: 0 10px;">
                    {q_data['text']}
                </h2>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            for opt_idx, opt in enumerate(q_data['options']):
                if st.button(opt['text'], key=f"dish_btn_{q_idx}_{opt_idx}", use_container_width=True):
                    dim = opt['dim']
                    st.session_state.dish_scores[dim] += 1
                    st.session_state.dish_history.append(dim)
                    st.session_state.dish_step += 1
                    st.rerun()
            if 1 < st.session_state.dish_step <= len(DISH_QUESTIONS):
                st.write("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                sub_col1, sub_col2, sub_col3 = st.columns([1.5, 1, 1])
                with sub_col1:
                    if st.button("⬅️ 返回上题", key="back_btn"):
                        last_dim = st.session_state.dish_history.pop()
                        st.session_state.dish_scores[last_dim] -= 1
                        st.session_state.dish_step -= 1
                        st.rerun()
                        
    # 【结果与加载视图】
    elif st.session_state.dish_step > len(DISH_QUESTIONS):
        col1, col2, col3 = st.columns([1, 10, 1])
        with col2:
            with st.spinner('正在翻炒你的灵魂... 🔥'):
                time.sleep(1.5) 
            
            result_data, percentages = calculate_dish_result(st.session_state.dish_scores)
            
            tags_html = ""
            for tag in result_data['portrait'].split('、'):
                tags_html += f'<span class="tag-pill">{tag}</span>'

            st.markdown(f"""
                <div class="result-card">
                    <div style="font-size: 0.625rem; color: #a8a29e; letter-spacing: 0.3em; margin-bottom: 0.5rem; font-weight: bold; text-transform: uppercase;">Soul Profile</div>
                    <h1 style="font-size: 2.25rem; font-weight: 900; color: #1c1917; margin-bottom: 1rem;">{result_data['name']}</h1>
                    <div style="margin-bottom: 1.5rem;">{tags_html}</div>
            """, unsafe_allow_html=True)

            st.write("<br>", unsafe_allow_html=True)
            img_path = f"images_food/{result_data['name']}.jpg"
            
            if os.path.exists(img_path):
                sub_col1, sub_col2, sub_col3 = st.columns([0.1, 4, 0.1]) 
                with sub_col2:
                    img_base64 = get_image_base64(img_path)
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center; margin: 1.5rem 0;">
                            <img src="data:image/jpeg;base64,{img_base64}" 
                                 style="width: 100%; border-radius: 28px; 
                                        box-shadow: 0 20px 40px rgba(0,0,0,0.15); 
                                        border: 6px solid white;
                                        transition: transform 0.3s ease;">
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
            else:
                st.warning(f"🍱 正在为你摆盘... (缺少图片: {img_path})")

            st.write("<br>", unsafe_allow_html=True)
            st.markdown('<h3 style="font-size: 0.625rem; font-weight: 900; color: #d6d3d1; margin-top: 2rem; letter-spacing: 0.2em; text-transform: uppercase;">味觉灵魂雷达</h3>', unsafe_allow_html=True)
            
            st.write("<br>", unsafe_allow_html=True)
            st.plotly_chart(draw_radar_chart(percentages), use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False})
            
            st.markdown(f"""
                    <div style="text-align: left; margin-top: 1rem;">
                        <p style="color: #57534e; line-height: 1.625; font-size: 0.875rem; margin-bottom: 1.5rem;">{result_data['description']}</p>
                        <div style="padding-top: 1.5rem; border-top: 1px solid #f5f5f4; text-align: center;">
                            <p style="font-size: 1.125rem; font-weight: 900; color: #292524; font-style: italic; letter-spacing: -0.025em;">“{result_data['goldSentence']}”</p>
                        </div>
                    </div>
                </div> """, unsafe_allow_html=True)

            st.write("<br>", unsafe_allow_html=True)
            
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("🔥 重新翻炒", use_container_width=True):
                st.session_state.dish_step = 0
                st.session_state.unlocked_FoodTest = False 
                if 'result_dish' in st.session_state:
                    del st.session_state['result_dish']
                    
                st.session_state.target_page = "Home" 
                st.success("记录已清空，正在返回主页...")
                st.rerun()

if __name__ == "__main__":
    show_dish_test()

