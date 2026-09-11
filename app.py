import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 1. 页面配置与大零售科技蓝视觉风格
# ==============================================================================
st.set_page_config(
    page_title="北美大零售全品类与气候销售决策系统 (Ultimate Pro)",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title { font-size: 1.85rem; font-weight: 700; color: #0F172A; margin-bottom: 0.2rem; }
    .sub-title { font-size: 0.92rem; color: #475569; margin-bottom: 1rem; }
    
    .kpi-card {
        background: linear-gradient(135deg, #1E40AF, #2563EB);
        color: white;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08);
    }
    .kpi-title { font-size: 0.84rem; opacity: 0.92; margin-bottom: 2px; font-weight: 500; }
    .kpi-val { font-size: 1.65rem; font-weight: 700; }
    
    .cat-selector {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
    }
    .radar-box {
        border-left: 4px solid #EF4444;
        background-color: #FEF2F2;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        margin-top: 10px;
    }
    .dict-term {
        font-weight: 600;
        color: #1D4ED8;
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏：北美建材与零售商业实战知识库（专为不熟悉美国国情准备）
with st.sidebar:
    st.markdown("### 🇺🇸 美国商业实地常识库")
    st.caption("理解美国零售的底层密码，避免中国工厂直觉陷阱")
    
    with st.expander("❓ 为什么美国冬天送风在地底，南方在天花？"):
        st.write("""
        * **北方/中西部**：冰冻线深（1米以上），房屋强制挖深做**全地下室（Full Basement）**。热泵/燃气炉都在地下室，**热空气自然向上升**，所以地面必须留出风孔（Floor Register）。
        * **南方阳光带（德州/佛州/加州）**：地下水高或土地膨胀，房屋直接浇筑**水泥大平板（Slab）**。实心水泥无法走管，空调主机只能放在隔热差的**阁楼（Attic）**，从天花板向下吹冷气（冷气自然下沉）。
        """)
        
    with st.expander("❓ 什么是 Menards？为什么不可忽视？"):
        st.write("""
        除了全国连锁的 Home Depot 和 Lowe's，美国中西部（大湖区与农业带）有一个极其强悍的区域霸主——**Menards**（330+超级大店）。中西部的蓝领农场主极度忠诚于 Menards 标志性的“全场 11% Rebate 返现”，在中西部做建材必须考虑它。
        """)

    with st.expander("❓ 为什么老美有极度狂热的 DIY 文化？"):
        st.write("""
        美国蓝领**人工极其昂贵**。请水工或暖通师傅上门，光进门诊断费（Trip Charge）就是 $150，按小时计费 $100+。换几个出风口或压条找工人要花几百美元，因此普通人宁可在超市买工具自己搞定。
        """)

    with st.expander("❓ 包装上的 Contractor Pack 是什么？"):
        st.write("""
        * **DIY 散装**：独立彩盒、附带安装螺丝、配 1:1 测量卡尺，单件卖给个人。
        * **Contractor Pack（工程装）**：牛皮纸无印刷工业箱，10件或20件一箱，专供 Pro 专业包工头，单件折算便宜 15%-20%，进店整箱整托盘拉走。
        """)

st.markdown('<div class="main-title">🏢 北美大零售全品类与气候销售决策系统 (Ultimate Pro)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">融合【50州地基结构 + 气象带 + 季节脉冲 + Big 3 零售门店 (THD/Lowe\'s/Menards) + 法务合规雷达】的智能决策中台</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. 全美 50 州基础数据库 (完整覆盖 Big 3 零售网络与区域物流归属)
# ==============================================================================
STATES_DATA = [
  {"abbr": "NC", "en": "North Carolina", "cn": "北卡罗来纳州", "region": "美东南", "velocity": 2946, "thd": 43, "lowes": 112, "menards": 0, "foundation": "架空层/地下室(75%+)", "climate": "Zone 4A/3A 混合湿润", "best": "地面出风口、地板耐磨五金", "avoid": "易锈冷轧薄铁件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "夏洛特枢纽"},
  {"abbr": "TN", "en": "Tennessee", "cn": "田纳西州", "region": "美中南", "velocity": 2902, "thd": 31, "lowes": 62, "menards": 0, "foundation": "木结构架空层/地下室", "climate": "Zone 4A 混合温和", "best": "重载地面风口、承重踏压件", "avoid": "天花专用下送风口", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "孟菲斯全美总仓"},
  {"abbr": "KY", "en": "Kentucky", "cn": "肯塔基州", "region": "美中", "velocity": 2579, "thd": 18, "lowes": 44, "menards": 5, "foundation": "全地下室占80%+", "climate": "Zone 4A 四季鲜明多雪", "best": "地下管道地面风口、复古风口", "avoid": "无调节阀空框", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "路易斯维尔"},
  {"abbr": "SC", "en": "South Carolina", "cn": "南卡罗来纳州", "region": "美东南", "velocity": 2433, "thd": 28, "lowes": 52, "menards": 0, "foundation": "架空层/沿海桩基", "climate": "Zone 3A 亚热带湿热", "best": "工程ABS风口、耐盐雾构件", "avoid": "未做防锈处理普通铁件", "flooring": "实木 40%, LVP 35%, 瓷砖 15%, 地毯 10%", "dc": "夏洛特枢纽"},
  {"abbr": "WV", "en": "West Virginia", "cn": "西弗吉尼亚州", "region": "美东", "velocity": 2248, "thd": 7, "lowes": 19, "menards": 3, "foundation": "山地深地基/全地下室", "climate": "Zone 5A 湿润山地极寒", "best": "抗重压地面风口、防冻融五金", "avoid": "脆性塑料件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "匹兹堡分仓"},
  {"abbr": "ID", "en": "Idaho", "cn": "爱达荷州", "region": "美西", "velocity": 2213, "thd": 12, "lowes": 14, "menards": 0, "foundation": "深层地下室(85%+)", "climate": "Zone 5B/6B 干燥高寒", "best": "强排暖风风口、防风密封件", "avoid": "湿热除霉配件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "盐湖城枢纽"},
  {"abbr": "VA", "en": "Virginia", "cn": "弗吉尼亚州", "region": "美东", "velocity": 2169, "thd": 46, "lowes": 68, "menards": 0, "foundation": "地下室/架空层老房多", "climate": "Zone 4A 四季湿润冬冷", "best": "中高端装饰风口、精工硬装", "avoid": "粗糙低端工程件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "里士满仓"},
  {"abbr": "KS", "en": "Kansas", "cn": "堪萨斯州", "region": "美中大平原", "velocity": 2124, "thd": 16, "lowes": 18, "menards": 9, "foundation": "100%全地下室", "climate": "Zone 4A/5A 大陆性严寒大风", "best": "大风量地面风口、耐压风门", "avoid": "轻质易吹脱件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "堪萨斯城枢纽"},
  {"abbr": "DE", "en": "Delaware", "cn": "特拉华州", "region": "美东", "velocity": 2122, "thd": 6, "lowes": 7, "menards": 0, "foundation": "地下室/浅架空层", "climate": "Zone 4A 温和多潮", "best": "标准4x10尺寸风口、免税走量款", "avoid": "非标冷门异形件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "费城分仓"},
  {"abbr": "AL", "en": "Alabama", "cn": "阿拉巴马州", "region": "美东南", "velocity": 2095, "thd": 28, "lowes": 40, "menards": 0, "foundation": "山区架空层/平原混合", "climate": "Zone 3A 亚热带湿热", "best": "防潮ABS风口、通用通风罩", "avoid": "未保护易氧化金属", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "伯明翰仓"},
  {"abbr": "IN", "en": "Indiana", "cn": "印第安纳州", "region": "美中", "velocity": 2020, "thd": 34, "lowes": 47, "menards": 36, "foundation": "全地下室占85%+", "climate": "Zone 5A 严寒多雪", "best": "地面暖风风口、防结冰构件", "avoid": "天花板专用散流器", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "印第安纳波利斯"},
  {"abbr": "MO", "en": "Missouri", "cn": "密苏里州", "region": "美中", "velocity": 1958, "thd": 36, "lowes": 42, "menards": 20, "foundation": "传统全地下室木屋", "climate": "Zone 4A/5A 大陆季风冬冷", "best": "地面可调风口、管道连接件", "avoid": "纯热带建材", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "圣路易斯仓"},
  {"abbr": "MD", "en": "Maryland", "cn": "马里兰州", "region": "美东", "velocity": 1935, "thd": 41, "lowes": 31, "menards": 0, "foundation": "老房地下室/联排镇屋", "climate": "Zone 4A 四季湿润冬寒", "best": "静音地面风口、防卡脚配件", "avoid": "粗矿工业件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "巴尔的摩仓"},
  {"abbr": "OH", "en": "Ohio", "cn": "俄亥俄州", "region": "美中", "velocity": 1768, "thd": 68, "lowes": 82, "menards": 31, "foundation": "全地下室为主", "climate": "Zone 5A 寒冷多雪长冬", "best": "冲压金属/铸铝地面风口", "avoid": "薄脆塑料", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "哥伦布核心仓"},
  {"abbr": "UT", "en": "Utah", "cn": "犹他州", "region": "美西", "velocity": 1666, "thd": 22, "lowes": 12, "menards": 0, "foundation": "全地下室大户型", "climate": "Zone 5B/6B 高山干燥极寒", "best": "抗干裂ABS风口、密封防风件", "avoid": "湿热除湿件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "盐湖城枢纽"},
  {"abbr": "NE", "en": "Nebraska", "cn": "内布拉斯加州", "region": "美中大平原", "velocity": 1601, "thd": 11, "lowes": 9, "menards": 9, "foundation": "全地下室独立屋", "climate": "Zone 5A 极寒多暴风雪", "best": "大承重地面风口、加厚五金", "avoid": "精细易损件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "奥马哈仓"},
  {"abbr": "CO", "en": "Colorado", "cn": "科罗拉多州", "region": "美西高地", "velocity": 1582, "thd": 44, "lowes": 30, "menards": 0, "foundation": "防冻全地下室", "climate": "Zone 5B/6B 高海拔强积雪", "best": "高气密保温风口、实木嵌入风口", "avoid": "漏风劣质件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "丹佛物流仓"},
  {"abbr": "OK", "en": "Oklahoma", "cn": "俄克拉荷马州", "region": "美中南", "velocity": 1543, "thd": 17, "lowes": 26, "menards": 0, "foundation": "架空层与平板各半", "climate": "Zone 3A/4A 极端温差风大", "best": "防风压配件、加固五金", "avoid": "非标冷门尺寸", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "达拉斯辐射仓"},
  {"abbr": "AR", "en": "Arkansas", "cn": "阿肯色州", "region": "美中南", "velocity": 1514, "thd": 14, "lowes": 27, "menards": 0, "foundation": "林区架空层木屋多", "climate": "Zone 3A/4A 湿润森林温和", "best": "防潮耐水ABS风口、平价金属件", "avoid": "高价奢侈品", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "小石城分仓"},
  {"abbr": "OR", "en": "Oregon", "cn": "俄勒冈州", "region": "美西北", "velocity": 1476, "thd": 26, "lowes": 15, "menards": 0, "foundation": "架空层木结构(Crawl)", "climate": "Zone 4C 海洋湿冷多雨", "best": "耐水防霉ABS风口、不锈钢配件", "avoid": "易锈生铁件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "波特兰仓"},
  {"abbr": "MT", "en": "Montana", "cn": "蒙大拿州", "region": "美西北高寒", "velocity": 1436, "thd": 7, "lowes": 5, "menards": 0, "foundation": "深埋防冻全地下室", "climate": "Zone 6B 严寒多雪", "best": "超耐寒金属件、坚固大格栅", "avoid": "低温脆化塑料", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "比灵斯仓"},
  {"abbr": "MI", "en": "Michigan", "cn": "密歇根州", "region": "美中大湖", "velocity": 1378, "thd": 70, "lowes": 43, "menards": 32, "foundation": "100%全地下室", "climate": "Zone 5A/6A 大湖雪带漫长冬", "best": "经典地面金属风口、防化雪盐件", "avoid": "天花专用风口", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "底特律仓"},
  {"abbr": "GA", "en": "Georgia", "cn": "乔治亚州", "region": "美东南", "velocity": 1346, "thd": 89, "lowes": 63, "menards": 0, "foundation": "北架空层/南平板地基", "climate": "Zone 3A 亚热带长夏湿热", "best": "天花与地面品类分推、防腐五金", "avoid": "全推纯地面件", "flooring": "LVP 40%, 瓷砖 35%, 地毯 25%", "dc": "亚特兰大(THD全球总部)"},
  {"abbr": "WA", "en": "Washington", "cn": "华盛顿州", "region": "美西北", "velocity": 1340, "thd": 43, "lowes": 37, "menards": 0, "foundation": "架空层与现代住宅", "climate": "Zone 4C 阴湿多雾", "best": "极简线形风口、环保无味ABS件", "avoid": "过时粗糙件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "西雅图枢纽"},
  {"abbr": "IL", "en": "Illinois", "cn": "伊利诺伊州", "region": "美中", "velocity": 1257, "thd": 82, "lowes": 38, "menards": 45, "foundation": "全地下室占多数", "climate": "Zone 5A 大陆性严寒冬风大", "best": "标准地面出风口、重型五金", "avoid": "薄型无卡槽风口", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "大芝加哥枢纽"},
  {"abbr": "PA", "en": "Pennsylvania", "cn": "宾夕法尼亚州", "region": "美东北", "velocity": 1197, "thd": 69, "lowes": 84, "menards": 0, "foundation": "老房地下室比例高", "climate": "Zone 5A/6A 寒冷多雪老区", "best": "古典复古雕花风口、金属件", "avoid": "现代过于极简款", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "哈里斯堡仓"},
  {"abbr": "SD", "en": "South Dakota", "cn": "南达科他州", "region": "美中大平原", "velocity": 1183, "thd": 4, "lowes": 3, "menards": 6, "foundation": "防冻深层地下室", "climate": "Zone 5B/6B 严寒干燥多风", "best": "耐低温防裂金属风口", "avoid": "易碎薄塑料", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "苏瀑仓"},
  {"abbr": "IA", "en": "Iowa", "cn": "爱荷华州", "region": "美中", "velocity": 1100, "thd": 18, "lowes": 17, "menards": 22, "foundation": "几乎全地下室", "climate": "Zone 5A 寒冷长冬大雪", "best": "高性价比金属与ABS风口", "avoid": "昂贵概念品", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "得梅因仓"},
  {"abbr": "NJ", "en": "New Jersey", "cn": "新泽西州", "region": "美东北", "velocity": 1007, "thd": 64, "lowes": 41, "menards": 0, "foundation": "紧凑型地下室多", "climate": "Zone 4A/5A 海洋微寒密集居住", "best": "小巧精致风口、美观五金", "avoid": "粗矿工业件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "纽瓦克核心仓"},
  {"abbr": "NY", "en": "New York", "cn": "纽约州", "region": "美东北", "velocity": 863, "thd": 102, "lowes": 68, "menards": 0, "foundation": "市区公寓无风管/郊区独栋地下室", "climate": "Zone 5A/6A 湿冷上州大雪", "best": "郊区独栋地面件、复古暖气罩", "avoid": "市区公寓推地板风管件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "奥尔巴尼仓"},
  {"abbr": "WY", "en": "Wyoming", "cn": "怀俄明州", "region": "美西高地", "velocity": 846, "thd": 4, "lowes": 2, "menards": 2, "foundation": "全地下室人口稀少", "climate": "Zone 6B/7 极寒干燥大风", "best": "超耐寒重型五金", "avoid": "轻质薄件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "夏延仓"},
  {"abbr": "MA", "en": "Massachusetts", "cn": "马萨诸塞州", "region": "美东北", "velocity": 846, "thd": 46, "lowes": 26, "menards": 0, "foundation": "水暖暖气片(Radiator)多", "climate": "Zone 5A 寒冷多雪近海湿冷", "best": "踢脚线出风口、复古铸铁风口", "avoid": "强排风管专属塑料件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "波士顿分仓"},
  {"abbr": "NM", "en": "New Mexico", "cn": "新墨西哥州", "region": "美西南", "velocity": 823, "thd": 13, "lowes": 14, "menards": 0, "foundation": "水泥平板地基(Slab)为主", "climate": "Zone 4B/5B 沙漠干旱多风沙", "best": "防尘百叶、耐晒高温五金", "avoid": "地面下沉式出风口", "flooring": "瓷砖 50%, 水泥抛光 30%, 地毯 20%", "dc": "阿尔伯克基仓"},
  {"abbr": "MN", "en": "Minnesota", "cn": "明尼苏达州", "region": "美中北高寒", "velocity": 771, "thd": 33, "lowes": 13, "menards": 33, "foundation": "深层地下室但水暖多", "climate": "Zone 6A/7 极寒雪原", "best": "重型防冷凝风口、耐寒五金", "avoid": "易脆塑料", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "明尼阿波利斯仓"},
  {"abbr": "NH", "en": "New Hampshire", "cn": "新罕布什尔州", "region": "美东北", "velocity": 756, "thd": 19, "lowes": 12, "menards": 0, "foundation": "石基与木屋", "climate": "Zone 5A/6A 林区寒冷", "best": "实木配风口、自然金属件", "avoid": "廉价塑料件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "曼彻斯特仓"},
  {"abbr": "MS", "en": "Mississippi", "cn": "密西西比州", "region": "美东南", "velocity": 737, "thd": 16, "lowes": 24, "menards": 0, "foundation": "平板地基与浅架空", "climate": "Zone 3A 闷热高湿无冬", "best": "高抗湿防生锈件、天花排风罩", "avoid": "高端奢侈品", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "杰克逊仓"},
  {"abbr": "VT", "en": "Vermont", "cn": "佛蒙特州", "region": "美东北", "velocity": 717, "thd": 4, "lowes": 2, "menards": 0, "foundation": "全地下室山地木屋", "climate": "Zone 6A 寒冬多雪", "best": "环保无味风口、铸铝盖板", "avoid": "劣质塑料感产品", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "伯灵顿仓"},
  {"abbr": "ND", "en": "North Dakota", "cn": "北达科他州", "region": "美中北极寒", "velocity": 671, "thd": 4, "lowes": 3, "menards": 8, "foundation": "防冻深层地下室", "climate": "Zone 6A/7 极寒半年冰封", "best": "结实金属风口、保温构件", "avoid": "脆性塑料", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "法戈仓"},
  {"abbr": "CT", "en": "Connecticut", "cn": "康涅狄格州", "region": "美东北", "velocity": 658, "thd": 30, "lowes": 14, "menards": 0, "foundation": "老房地下室但定制工程多", "climate": "Zone 5A 海洋微寒多雪", "best": "高档定制级拉丝金属风口", "avoid": "低档大众通用塑料", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "哈特福德仓"},
  {"abbr": "ME", "en": "Maine", "cn": "缅因州", "region": "美东北", "velocity": 634, "thd": 11, "lowes": 8, "menards": 0, "foundation": "传统地下室与岩基", "climate": "Zone 6A 沿海湿冷多雾", "best": "防潮耐盐雾金属件", "avoid": "不耐湿五金", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "波特兰仓"},
  {"abbr": "RI", "en": "Rhode Island", "cn": "罗德岛州", "region": "美东北", "velocity": 532, "thd": 7, "lowes": 4, "menards": 0, "foundation": "老房紧凑型", "climate": "Zone 5A 海洋微寒", "best": "常规标准修缮件", "avoid": "异形大件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "普罗维登斯仓"},
  {"abbr": "LA", "en": "Louisiana", "cn": "路易斯安那州", "region": "美南沿海", "velocity": 495, "thd": 27, "lowes": 31, "menards": 0, "foundation": "防洪高架柱/水泥平板", "climate": "Zone 2A/3A 极端湿热易涝", "best": "天花排风口、高耐蚀铝合金防锈件", "avoid": "地面下沉式出风口", "flooring": "瓷砖 50%, 抛光强化 30%, 地毯 20%", "dc": "新奥尔良仓"},
  {"abbr": "NV", "en": "Nevada", "cn": "内华达州", "region": "美西南沙漠", "velocity": 460, "thd": 19, "lowes": 14, "menards": 0, "foundation": "100%混凝土平板(Slab)", "climate": "Zone 3B 极端干旱酷热沙漠", "best": "天花板可调风口、抗紫外线塑料件", "avoid": "地面出风口", "flooring": "瓷砖 50%, 强化复合 30%, 地毯 20%", "dc": "拉斯维加斯仓"},
  {"abbr": "WI", "en": "Wisconsin", "cn": "威斯康星州", "region": "美中大湖", "velocity": 456, "thd": 28, "lowes": 13, "menards": 44, "foundation": "全地下室普及", "climate": "Zone 5A/6A 漫长严寒多雪", "best": "重型金属地板出风口、防冻五金", "avoid": "天花专用风口", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "密尔沃基仓"},
  {"abbr": "TX", "en": "Texas", "cn": "德克萨斯州", "region": "美南核心", "velocity": 332, "thd": 180, "lowes": 142, "menards": 0, "foundation": "80%+混凝土平板地基(Slab)", "climate": "Zone 2A/3A/3B 漫长干热湿热", "best": "天花散流器、回风滤网格栅", "avoid": "地面下沉式出风口", "flooring": "瓷砖 50%, 水泥抛光 30%, 地毯 20%", "dc": "达拉斯/休斯敦大仓"},
  {"abbr": "AZ", "en": "Arizona", "cn": "亚利桑那州", "region": "美西南沙漠", "velocity": 289, "thd": 58, "lowes": 33, "menards": 0, "foundation": "绝大多数为混凝土平板", "climate": "Zone 2B 纯沙漠干热长酷暑", "best": "天花板空调扩散器、遮阳建材", "avoid": "地面风口", "flooring": "瓷砖 50%, 强化地板 30%, 地毯 20%", "dc": "凤凰城枢纽"},
  {"abbr": "CA", "en": "California", "cn": "加利福尼亚州", "region": "美西海岸", "velocity": 253, "thd": 232, "lowes": 113, "menards": 0, "foundation": "南加全平板/网点全美最密", "climate": "Zone 3B/4B 干燥温和干热", "best": "Title 24环保合规风口、天花格栅", "avoid": "高铅普通锻造件", "flooring": "瓷砖 45%, LVP 35%, 地毯 20%", "dc": "安大略/洛杉矶总仓"},
  {"abbr": "FL", "en": "Florida", "cn": "佛罗里达州", "region": "美东南半岛", "velocity": 234, "thd": 154, "lowes": 128, "menards": 0, "foundation": "95%+混凝土平板地基(Slab)", "climate": "Zone 1A/2A 极湿热高盐雾飓风", "best": "天花出风口、防腐铝/ABS配件", "avoid": "地面出风口", "flooring": "瓷砖 60%, 强化/LVP 25%, 地毯 15%", "dc": "奥兰多枢纽"},
  {"abbr": "AK", "en": "Alaska", "cn": "阿拉斯加州", "region": "非本土极寒", "velocity": 920, "thd": 7, "lowes": 5, "menards": 0, "foundation": "永久冻土抬升/深基岩保温仓", "climate": "Zone 7/8 全美最高寒", "best": "超耐冻极温五金、重载保温出风件", "avoid": "常温塑料及薄冷轧铁", "flooring": "强化保温地板 50%, 实木 30%, 瓷砖 20%", "dc": "安克雷奇驳运仓"},
  {"abbr": "HI", "en": "Hawaii", "cn": "夏威夷州", "region": "非本土海岛", "velocity": 410, "thd": 7, "lowes": 4, "menards": 0, "foundation": "火山岩地基/架空防潮桩", "climate": "Zone 1 强热带高盐雾高腐蚀", "best": "316/304不锈钢、纯ABS高防腐构件", "avoid": "含铁电镀件、地面出风口", "flooring": "耐水瓷砖 60%, 纯防水LVP 30%, 竹木 10%", "dc": "火奴鲁鲁海运仓"}
]

# ==============================================================================
# 3. 品类与四维属性配置
# ==============================================================================
CATEGORY_CONFIG = {
    "1. 暖通通风与空气分配 (HVAC & Ventilation)": {
        "tag": "HVAC",
        "short_name": "暖通通风",
        "intro": "核心受【地下室 vs 水泥平板】与【冷热空气自然对流】决定。北方地暖向上升必须地面开孔，南方空调天花下吹。",
        "positions": ["(全选)", "Floor (地面出风口)", "Ceiling (天花板散流器)", "Baseboard (踢脚线出风口)", "Sidewall (高侧墙回风格栅)"],
        "materials": ["(全选)", "Steel (冲压冷轧钢)", "Aluminum (铝合金)", "Plastic (ABS阻燃树脂)", "Cast Metal (重型铸铝/铸铁)", "Wood (橡木实木)"],
        "finishes": ["(全选)", "WH (White 经典白)", "BL (Matte Black 哑光黑)", "BN (Brushed Nickel 拉丝镍)", "AB (Antique Brass 仿古黄铜)", "ORB (Oil Rubbed Bronze 仿古深铜)"],
        "sizes": ["(全选)", "04X10 (全美走量王)", "04X12 (主流换新大号)", "02X12 (狭长缝/踢脚线)", "06X10 (大排量)", "12X12 (天花板方型)"]
    },
    "2. 卫浴五金与地漏给排水 (Plumbing & Bath Hardware)": {
        "tag": "PLUMBING",
        "short_name": "卫浴给排水",
        "intro": "受【冬季极深冻土层防爆裂】与【南方瓷砖无门槛淋浴房翻新】双向驱动。",
        "positions": ["(全选)", "Floor Drain (方形地面地漏)", "Linear Drain (长条隐形淋浴地漏)", "Frost-Proof Valve (室外防冻水阀)", "Shower Fixture (墙面花洒五金)"],
        "materials": ["(全选)", "Stainless Steel 304 (304不锈钢)", "Solid Brass (精铸无铅铜)", "ABS/PVC (耐腐工程塑料)", "Zinc Alloy (锌合金)"],
        "finishes": ["(全选)", "CP (Chrome 抛光亮铬)", "MB (Matte Black 现代哑光黑)", "BN (Brushed Nickel 经典拉丝镍)", "BG (Brushed Gold 拉丝金)"],
        "sizes": ["(全选)", "4x4 inch (标准方形)", "24-36 inch (长条隐形地漏)", "1/2 inch (常规水管接口)", "3/4 inch (主进水管接口)"]
    },
    "3. 地面收口压条与瓷砖金属辅料 (Flooring & Tile Trim)": {
        "tag": "FLOORING",
        "short_name": "地面收口压条",
        "intro": "受【硬木/LVP普及率 vs 瓷砖大板偏好】决定。房间交界处与落差处刚需，涉及美国 ADA 防绊倒法案。",
        "positions": ["(全选)", "T-Molding (同高地面平接T条)", "Reducer (高低不平缓坡减速条)", "Tile Edge Trim (瓷砖L型防崩角条)", "Stair Nosing (木楼梯防滑包角)"],
        "materials": ["(全选)", "Anodized Aluminum (阳极氧化铝合金)", "Solid Brass (高端装饰铜)", "Stainless Steel (高耐磨不锈钢)", "PVC (柔性自粘条)"],
        "finishes": ["(全选)", "Silver/Matte (哑光拉丝银)", "Titanium Black (现代钛黑)", "Dark Bronze (仿古深铜)", "Wood Grain (木纹覆膜)"],
        "sizes": ["(全选)", "36 inch (单开门标准宽)", "72 inch (双扇门大跨度)", "8mm-10mm (常规瓷砖收口)", "12mm-15mm (厚板收口)"]
    },
    "4. 门窗五金与密封防风防暴 (Doors, Windows & Hardware)": {
        "tag": "DOORS",
        "short_name": "门窗密封五金",
        "intro": "北方冬季【狂风门底保暖节能】与沿海【飓风带 HVHZ 强制抗风压五金】是全美两大极端法典驱动力。",
        "positions": ["(全选)", "Door Bottom Sweep (门底防风挡水条)", "Weatherstripping (门框隔音密封条)", "Hurricane Tie (建筑抗飓风加固角码)", "Heavy Hinge (重载轴承门合页)"],
        "materials": ["(全选)", "Aluminum + Silicone (铝合金托底+耐候硅胶)", "Hot-Dip Galvanized (重型热浸镀锌钢)", "Solid Brass (重型纯铜)", "Stainless Steel (防锈不锈钢)"],
        "finishes": ["(全选)", "BL (Matte Black 哑光黑)", "Satin Nickel (缎面拉丝银)", "White (门框经典白)", "Zinc (工业镀锌银)"],
        "sizes": ["(全选)", "36 inch (标准单门宽)", "42 inch (大入户门底条)", "4x4 inch (重载大门合页)", "50 ft Roll (整卷密封条)"]
    },
    "5. 户外庭院、排水沟与结构件 (Outdoor Drainage & Patio)": {
        "tag": "OUTDOOR",
        "short_name": "庭院户外排水",
        "intro": "受【暴雨防内涝、融雪荷载与秋季落叶堵塞天沟】决定。独栋庭院车道与泳池边绝对刚需。",
        "positions": ["(全选)", "Trench Drain (车道/泳池线性排水沟)", "Gutter Guard (屋檐排水天沟防叶滤网)", "Post Anchor Base (木露台立柱固定底座)", "Outdoor Vent (外墙防风雨冲压罩)"],
        "materials": ["(全选)", "Polymer/HDPE (耐暴晒重型塑料)", "Hot-Dip Galvanized (镀锌重钢格栅)", "Cast Iron (球墨铸铁重载盖板)", "Cast Aluminum (耐候防腐铸铝)"],
        "finishes": ["(全选)", "Black Asphalt (沥青防腐黑)", "Galvanized Silver (热镀锌防腐银)", "Natural Gray (水泥工程灰)"],
        "sizes": ["(全选)", "39 inch / 1 Meter (标准单段沟长)", "5-6 inch (全美标准屋檐天沟网)", "4x4 inch (木方柱底座)", "6x6 inch (重载立柱底座)"]
    }
}

# ==============================================================================
# 4. 业务规划周期与四维属性筛选栏
# ==============================================================================
st.markdown('<div class="cat-selector">', unsafe_allow_html=True)
col_c1, col_c2, col_c3 = st.columns([1.5, 1.2, 1.3])

with col_c1:
    chosen_cat_name = st.selectbox("📂 核心产品品类 (Category)：", list(CATEGORY_CONFIG.keys()), index=0)
    cur_cat_conf = CATEGORY_CONFIG[chosen_cat_name]

with col_c2:
    # 扩充：美国家居零售高度依赖季度节令
    season_choice = st.selectbox(
        "📅 规划出货节令 (Seasonality Pulse)：",
        [
            "全年平均基准 (Annual Baseline)",
            "Q1 春季化冻与庭院翻新 (Spring Thaw: 3-5月)",
            "Q2 夏季空调制冷高峰 (Peak Cooling: 6-8月)",
            "Q3 秋季落叶与入冬防寒准备 (Fall Weatherization: 9-11月)",
            "Q4 深冬极寒与防冻抢修 (Freeze Defense: 12-2月)"
        ],
        index=3 # 默认选 Q3，最典型的建材旺季
    )

with col_c3:
    target_channel = st.selectbox(
        "🏬 目标核心分销渠道 (Target Retailer)：",
        ["全渠道混合统计 (THD + Lowe's + Menards)", "The Home Depot 专属网点", "Lowe's 专属网点", "Menards (中西部大区专营)"],
        index=0
    )

st.markdown('</div>', unsafe_allow_html=True)

# 四维属性选择
f_col1, f_col2, f_col3, f_col4 = st.columns(4)
with f_col1:
    selected_pos_raw = st.selectbox("1. 安装位置 (Position)：", cur_cat_conf["positions"], index=1)
    sel_pos = selected_pos_raw.split(" ")[0]
with f_col2:
    selected_mat_raw = st.selectbox("2. 材质构成 (Material)：", cur_cat_conf["materials"], index=0)
    sel_mat = selected_mat_raw.split(" ")[0]
with f_col3:
    selected_fin_raw = st.selectbox("3. 表面颜色 (Finish)：", cur_cat_conf["finishes"], index=0)
    sel_fin = selected_fin_raw.split(" ")[0]
with f_col4:
    selected_size_raw = st.selectbox("4. 规格尺寸 (Size)：", cur_cat_conf["sizes"], index=1)
    sel_size = selected_size_raw.split(" ")[0]

# ==============================================================================
# 5. 全维多属性与气象节令计算引擎
# ==============================================================================
calculated_states = []

for s in STATES_DATA:
    abbr = s["abbr"]
    base_velocity = s["velocity"]
    
    # 动态确定渠道门店总数
    if target_channel == "The Home Depot 专属网点":
        active_stores = s["thd"]
    elif target_channel == "Lowe's 专属网点":
        active_stores = s["lowes"]
    elif target_channel == "Menards (中西部大区专营)":
        active_stores = s["menards"]
    else:
        active_stores = s["thd"] + s["lowes"] + s["menards"]
        
    weight = 1.0
    reasons = []
    
    # -------- 1. 品类与安装位置 (Position) 逻辑 --------
    if cur_cat_conf["tag"] == "HVAC":
        if sel_pos == "Floor":
            if abbr in ["NC", "TN", "KY", "IN", "OH", "MI", "WV", "IL", "PA", "AK"]:
                weight *= 1.25
                reasons.append("全地下室主场，暖气必须自地面向上对流")
            elif abbr in ["FL", "TX", "AZ", "NV", "LA", "HI"]:
                weight *= 0.12
                reasons.append("水泥实心大平板，地面无开槽管道，严禁推地板款")
        elif sel_pos == "Ceiling":
            if abbr in ["FL",
