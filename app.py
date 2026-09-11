import streamlit as st
import pandas as pd

# ==============================================================================
# 1. 页面配置与视觉样式
# ==============================================================================
st.set_page_config(
    page_title="北美大零售全品类与气候销售决策系统 (Engineering Edition)",
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
    .physics-card {
        background-color: #F1F5F9;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 10px 12px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏：北美建材与零售商业实战知识库
with st.sidebar:
    st.markdown("### 🇺🇸 美国商业与工程实战知识库")
    st.caption("真实反映美国建筑物理、县级法典与零售采销常识")
    
    with st.expander("❓ 什么是 HDD 与 CDD？为什么它是暖通圣经？"):
        st.write("""
        * **HDD (采暖度日数)**：气温低于 65°F(18.3°C) 的累积度数。HDD 越高的州（如 MN/ND），暖气开启月份越长，地面风口受高温热风烘烤时间越长，抗热变形是硬指标。
        * **CDD (制冷度日数)**：气温高于 65°F 的累积度数。CDD 越高的州（如 FL/TX），空调下吹风量巨大，天花散流器防结冰与防凝露滴水（Sweating）是考核核心。
        """)

    with st.expander("❓ 什么是冻土深度（Frost Line）与长水阀？"):
        st.write("""
        北方冬季地面泥土会深度结冰。水管如果不埋在冻土线以下就会爆裂。因此在明尼苏达（冻土深达 60 英寸），去 Home Depot 买防冻龙头必须选 10~12 英寸超长杆，才能把阀体送入室内暖气保温区；而在德州（冻土 0 英寸），4 英寸短杆就能用。
        """)

    with st.expander("❓ 融雪盐（De-icing Salt）如何腐蚀地表？"):
        st.write("""
        北方大湖雪带冬天会在路面撒巨量氯化钙/工业盐。人们靴底粘着盐雪踩进玄关，盐水融化滴在地面出风口与压条上。冷轧铁喷漆 2 年即起泡剥落生锈，当地极度偏好**阳极氧化铝（Anodized）**。
        """)

    with st.expander("❓ 什么是加州 WUI 山火防飞烬规范？"):
        st.write("""
        西海岸山火频繁，加州严格执行 **WUI (Wildland-Urban Interface)** 法规。所有外墙、屋檐出风口与排气百叶，内衬必须加装 1/8 英寸（3.2mm）耐火耐腐蚀不锈钢网，防止强风火星飞入阁楼引燃整栋房屋。
        """)

st.markdown('<div class="main-title">🏢 北美大零售全品类与气候销售决策系统 (Engineering Edition)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">融合【DOE法定 8 大气候带 + HDD/CDD能耗度日 + 冻土深度 + 水质硬度 + 融雪盐腐蚀 + Big 3 零售门店】</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. 全美 50 州深度数据库 (扩充硬核工程物理与气象数据)
# ==============================================================================
STATES_DATA = [
  {"abbr": "NC", "en": "North Carolina", "cn": "北卡罗来纳州", "region": "美东南", "velocity": 2946, "thd": 43, "lowes": 112, "menards": 0, "foundation": "架空层/地下室(75%+)", "climate": "Zone 4A/3A 混合湿润", "best": "地面出风口、地板耐磨五金", "avoid": "易锈冷轧薄铁件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "夏洛特枢纽", "hdd": 3400, "cdd": 1600, "frost_depth": 12, "water_hardness": 3.2, "salt_risk": "低", "hazard": "东南沿海热带风暴"},
  {"abbr": "TN", "en": "Tennessee", "cn": "田纳西州", "region": "美中南", "velocity": 2902, "thd": 31, "lowes": 62, "menards": 0, "foundation": "木结构架空层/地下室", "climate": "Zone 4A 混合温和", "best": "重载地面风口、承重踏压件", "avoid": "天花专用下送风口", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "孟菲斯全美总仓", "hdd": 3800, "cdd": 1500, "frost_depth": 12, "water_hardness": 6.8, "salt_risk": "低", "hazard": "春季强对流风暴"},
  {"abbr": "KY", "en": "Kentucky", "cn": "肯塔基州", "region": "美中", "velocity": 2579, "thd": 18, "lowes": 44, "menards": 5, "foundation": "全地下室占80%+", "climate": "Zone 4A 四季鲜明多雪", "best": "地下管道地面风口、复古风口", "avoid": "无调节阀空框", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "路易斯维尔", "hdd": 4400, "cdd": 1250, "frost_depth": 20, "water_hardness": 10.5, "salt_risk": "中", "hazard": "冬季道路结冰"},
  {"abbr": "SC", "en": "South Carolina", "cn": "南卡罗来纳州", "region": "美东南", "velocity": 2433, "thd": 28, "lowes": 52, "menards": 0, "foundation": "架空层/沿海桩基", "climate": "Zone 3A 亚热带湿热", "best": "工程ABS风口、耐盐雾构件", "avoid": "未做防锈处理普通铁件", "flooring": "实木 40%, LVP 35%, 瓷砖 15%, 地毯 10%", "dc": "夏洛特枢纽", "hdd": 2400, "cdd": 2100, "frost_depth": 4, "water_hardness": 2.5, "salt_risk": "极低", "hazard": "沿海飓风高湿热"},
  {"abbr": "WV", "en": "West Virginia", "cn": "西弗吉尼亚州", "region": "美东", "velocity": 2248, "thd": 7, "lowes": 19, "menards": 3, "foundation": "山地深地基/全地下室", "climate": "Zone 5A 湿润山地极寒", "best": "抗重压地面风口、防冻融五金", "avoid": "脆性塑料件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "匹兹堡分仓", "hdd": 5200, "cdd": 800, "frost_depth": 28, "water_hardness": 7.2, "salt_risk": "高", "hazard": "山地重积雪融雪剂"},
  {"abbr": "ID", "en": "Idaho", "cn": "爱达荷州", "region": "美西", "velocity": 2213, "thd": 12, "lowes": 14, "menards": 0, "foundation": "深层地下室(85%+)", "climate": "Zone 5B/6B 干燥高寒", "best": "强排暖风风口、防风密封件", "avoid": "湿热除霉配件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "盐湖城枢纽", "hdd": 6200, "cdd": 700, "frost_depth": 36, "water_hardness": 9.4, "salt_risk": "中", "hazard": "干燥开裂强阵风"},
  {"abbr": "VA", "en": "Virginia", "cn": "弗吉尼亚州", "region": "美东", "velocity": 2169, "thd": 46, "lowes": 68, "menards": 0, "foundation": "地下室/架空层老房多", "climate": "Zone 4A 四季湿润冬冷", "best": "中高端装饰风口、精工硬装", "avoid": "粗糙低端工程件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "里士满仓", "hdd": 3900, "cdd": 1400, "frost_depth": 18, "water_hardness": 5.1, "salt_risk": "中", "hazard": "四季交替潮湿"},
  {"abbr": "KS", "en": "Kansas", "cn": "堪萨斯州", "region": "美中大平原", "velocity": 2124, "thd": 16, "lowes": 18, "menards": 9, "foundation": "100%全地下室", "climate": "Zone 4A/5A 大陆性严寒大风", "best": "大风量地面风口、耐压风门", "avoid": "轻质易吹脱件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "堪萨斯城枢纽", "hdd": 5000, "cdd": 1450, "frost_depth": 30, "water_hardness": 14.8, "salt_risk": "中", "hazard": "龙卷风走廊狂风"},
  {"abbr": "DE", "en": "Delaware", "cn": "特拉华州", "region": "美东", "velocity": 2122, "thd": 6, "lowes": 7, "menards": 0, "foundation": "地下室/浅架空层", "climate": "Zone 4A 温和多潮", "best": "标准4x10尺寸风口、免税走量款", "avoid": "非标冷门异形件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "费城分仓", "hdd": 4200, "cdd": 1200, "frost_depth": 24, "water_hardness": 4.5, "salt_risk": "中", "hazard": "沿海湿气腐蚀"},
  {"abbr": "AL", "en": "Alabama", "cn": "阿拉巴马州", "region": "美东南", "velocity": 2095, "thd": 28, "lowes": 40, "menards": 0, "foundation": "山区架空层/平原混合", "climate": "Zone 3A 亚热带湿热", "best": "防潮ABS风口、通用通风罩", "avoid": "未保护易氧化金属", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "伯明翰仓", "hdd": 2600, "cdd": 2000, "frost_depth": 6, "water_hardness": 4.1, "salt_risk": "极低", "hazard": "春夏季热带强降雨"},
  {"abbr": "IN", "en": "Indiana", "cn": "印第安纳州", "region": "美中", "velocity": 2020, "thd": 34, "lowes": 47, "menards": 36, "foundation": "全地下室占85%+", "climate": "Zone 5A 严寒多雪", "best": "地面暖风风口、防结冰构件", "avoid": "天花板专用散流器", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "印第安纳波利斯", "hdd": 5600, "cdd": 1050, "frost_depth": 36, "water_hardness": 18.2, "salt_risk": "极高", "hazard": "大雪化冰盐侵蚀+极硬水"},
  {"abbr": "MO", "en": "Missouri", "cn": "密苏里州", "region": "美中", "velocity": 1958, "thd": 36, "lowes": 42, "menards": 20, "foundation": "传统全地下室木屋", "climate": "Zone 4A/5A 大陆季风冬冷", "best": "地面可调风口、管道连接件", "avoid": "纯热带建材", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "圣路易斯仓", "hdd": 4700, "cdd": 1400, "frost_depth": 26, "water_hardness": 11.5, "salt_risk": "中", "hazard": "温差剧烈冰融循环"},
  {"abbr": "MD", "en": "Maryland", "cn": "马里兰州", "region": "美东", "velocity": 1935, "thd": 41, "lowes": 31, "menards": 0, "foundation": "老房地下室/联排镇屋", "climate": "Zone 4A 四季湿润冬寒", "best": "静音地面风口、防卡脚配件", "avoid": "粗矿工业件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "巴尔的摩仓", "hdd": 4400, "cdd": 1200, "frost_depth": 24, "water_hardness": 5.8, "salt_risk": "中", "hazard": "切萨皮克湾高湿"},
  {"abbr": "OH", "en": "Ohio", "cn": "俄亥俄州", "region": "美中", "velocity": 1768, "thd": 68, "lowes": 82, "menards": 31, "foundation": "全地下室为主", "climate": "Zone 5A 寒冷多雪长冬", "best": "冲压金属/铸铝地面风口", "avoid": "薄脆塑料", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "哥伦布核心仓", "hdd": 5800, "cdd": 950, "frost_depth": 32, "water_hardness": 16.0, "salt_risk": "极高", "hazard": "雪带融雪盐+深冻土"},
  {"abbr": "UT", "en": "Utah", "cn": "犹他州", "region": "美西", "velocity": 1666, "thd": 22, "lowes": 12, "menards": 0, "foundation": "全地下室大户型", "climate": "Zone 5B/6B 高山干燥极寒", "best": "抗干裂ABS风口、密封防风件", "avoid": "湿热除湿件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "盐湖城枢纽", "hdd": 5700, "cdd": 1000, "frost_depth": 30, "water_hardness": 15.5, "salt_risk": "中", "hazard": "高海拔超干燥强紫外线"},
  {"abbr": "NE", "en": "Nebraska", "cn": "内布拉斯加州", "region": "美中大平原", "velocity": 1601, "thd": 11, "lowes": 9, "menards": 9, "foundation": "全地下室独立屋", "climate": "Zone 5A 极寒多暴风雪", "best": "大承重地面风口、加厚五金", "avoid": "精细易损件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "奥马哈仓", "hdd": 6100, "cdd": 1100, "frost_depth": 40, "water_hardness": 13.2, "salt_risk": "高", "hazard": "暴风雪严寒大风"},
  {"abbr": "CO", "en": "Colorado", "cn": "科罗拉多州", "region": "美西高地", "velocity": 1582, "thd": 44, "lowes": 30, "menards": 0, "foundation": "防冻全地下室", "climate": "Zone 5B/6B 高海拔强积雪", "best": "高气密保温风口、实木嵌入风口", "avoid": "漏风劣质件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "丹佛物流仓", "hdd": 6000, "cdd": 750, "frost_depth": 36, "water_hardness": 8.5, "salt_risk": "中", "hazard": "WUI山火防飞烬+强紫外线"},
  {"abbr": "OK", "en": "Oklahoma", "cn": "俄克拉荷马州", "region": "美中南", "velocity": 1543, "thd": 17, "lowes": 26, "menards": 0, "foundation": "架空层与平板各半", "climate": "Zone 3A/4A 极端温差风大", "best": "防风压配件、加固五金", "avoid": "非标冷门尺寸", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "达拉斯辐射仓", "hdd": 3700, "cdd": 1900, "frost_depth": 18, "water_hardness": 10.0, "salt_risk": "低", "hazard": "龙卷风走廊风压"},
  {"abbr": "AR", "en": "Arkansas", "cn": "阿肯色州", "region": "美中南", "velocity": 1514, "thd": 14, "lowes": 27, "menards": 0, "foundation": "林区架空层木屋多", "climate": "Zone 3A/4A 湿润森林温和", "best": "防潮耐水ABS风口、平价金属件", "avoid": "高价奢侈品", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "小石城分仓", "hdd": 3200, "cdd": 1800, "frost_depth": 12, "water_hardness": 4.8, "salt_risk": "极低", "hazard": "森林白蚁湿热"},
  {"abbr": "OR", "en": "Oregon", "cn": "俄勒冈州", "region": "美西北", "velocity": 1476, "thd": 26, "lowes": 15, "menards": 0, "foundation": "架空层木结构(Crawl)", "climate": "Zone 4C 海洋湿冷多雨", "best": "耐水防霉ABS风口、不锈钢配件", "avoid": "易锈生铁件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "波特兰仓", "hdd": 4600, "cdd": 450, "frost_depth": 18, "water_hardness": 2.1, "salt_risk": "极低", "hazard": "长达数月阴雨潮湿霉菌"},
  {"abbr": "MT", "en": "Montana", "cn": "蒙大拿州", "region": "美西北高寒", "velocity": 1436, "thd": 7, "lowes": 5, "menards": 0, "foundation": "深埋防冻全地下室", "climate": "Zone 6B 严寒多雪", "best": "超耐寒金属件、坚固大格栅", "avoid": "低温脆化塑料", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "比灵斯仓", "hdd": 7400, "cdd": 500, "frost_depth": 48, "water_hardness": 12.0, "salt_risk": "高", "hazard": "深冻土极寒(-30°F)"},
  {"abbr": "MI", "en": "Michigan", "cn": "密歇根州", "region": "美中大湖", "velocity": 1378, "thd": 70, "lowes": 43, "menards": 32, "foundation": "100%全地下室", "climate": "Zone 5A/6A 大湖雪带漫长冬", "best": "经典地面金属风口、防化雪盐件", "avoid": "天花专用风口", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "底特律仓", "hdd": 6600, "cdd": 700, "frost_depth": 42, "water_hardness": 14.5, "salt_risk": "极高", "hazard": "大湖效应暴雪融雪盐"},
  {"abbr": "GA", "en": "Georgia", "cn": "乔治亚州", "region": "美东南", "velocity": 1346, "thd": 89, "lowes": 63, "menards": 0, "foundation": "北架空层/南平板地基", "climate": "Zone 3A 亚热带长夏湿热", "best": "天花与地面品类分推、防腐五金", "avoid": "全推纯地面件", "flooring": "LVP 40%, 瓷砖 35%, 地毯 25%", "dc": "亚特兰大(THD全球总部)", "hdd": 2700, "cdd": 1950, "frost_depth": 6, "water_hardness": 2.8, "salt_risk": "极低", "hazard": "高湿热白蚁雷暴"},
  {"abbr": "WA", "en": "Washington", "cn": "华盛顿州", "region": "美西北", "velocity": 1340, "thd": 43, "lowes": 37, "menards": 0, "foundation": "架空层与现代住宅", "climate": "Zone 4C 阴湿多雾", "best": "极简线形风口、环保无味ABS件", "avoid": "过时粗糙件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "西雅图枢纽", "hdd": 4800, "cdd": 350, "frost_depth": 18, "water_hardness": 2.2, "salt_risk": "极低", "hazard": "常年阴雨腐蚀+霉菌"},
  {"abbr": "IL", "en": "Illinois", "cn": "伊利诺伊州", "region": "美中", "velocity": 1257, "thd": 82, "lowes": 38, "menards": 45, "foundation": "全地下室占多数", "climate": "Zone 5A 大陆性严寒冬风大", "best": "标准地面出风口、重型五金", "avoid": "薄型无卡槽风口", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "大芝加哥枢纽", "hdd": 6200, "cdd": 950, "frost_depth": 40, "water_hardness": 15.8, "salt_risk": "极高", "hazard": "芝加哥狂风严寒融雪盐"},
  {"abbr": "PA", "en": "Pennsylvania", "cn": "宾夕法尼亚州", "region": "美东北", "velocity": 1197, "thd": 69, "lowes": 84, "menards": 0, "foundation": "老房地下室比例高", "climate": "Zone 5A/6A 寒冷多雪老区", "best": "古典复古雕花风口、金属件", "avoid": "现代过于极简款", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "哈里斯堡仓", "hdd": 5500, "cdd": 900, "frost_depth": 36, "water_hardness": 9.2, "salt_risk": "高", "hazard": "融雪冻融老房水暖"},
  {"abbr": "SD", "en": "South Dakota", "cn": "南达科他州", "region": "美中大平原", "velocity": 1183, "thd": 4, "lowes": 3, "menards": 6, "foundation": "防冻深层地下室", "climate": "Zone 5B/6B 严寒干燥多风", "best": "耐低温防裂金属风口", "avoid": "易碎薄塑料", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "苏瀑仓", "hdd": 7200, "cdd": 800, "frost_depth": 48, "water_hardness": 16.5, "salt_risk": "高", "hazard": "深冻严寒干燥狂风"},
  {"abbr": "IA", "en": "Iowa", "cn": "爱荷华州", "region": "美中", "velocity": 1100, "thd": 18, "lowes": 17, "menards": 22, "foundation": "几乎全地下室", "climate": "Zone 5A 寒冷长冬大雪", "best": "高性价比金属与ABS风口", "avoid": "昂贵概念品", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "得梅因仓", "hdd": 6300, "cdd": 950, "frost_depth": 42, "water_hardness": 17.0, "salt_risk": "高", "hazard": "长冬冰冻融雪侵蚀"},
  {"abbr": "NJ", "en": "New Jersey", "cn": "新泽西州", "region": "美东北", "velocity": 1007, "thd": 64, "lowes": 41, "menards": 0, "foundation": "紧凑型地下室多", "climate": "Zone 4A/5A 海洋微寒密集居住", "best": "小巧精致风口、美观五金", "avoid": "粗矿工业件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "纽瓦克核心仓", "hdd": 4800, "cdd": 1100, "frost_depth": 30, "water_hardness": 7.0, "salt_risk": "高", "hazard": "近海盐雾冬季化冰盐"},
  {"abbr": "NY", "en": "New York", "cn": "纽约州", "region": "美东北", "velocity": 863, "thd": 102, "lowes": 68, "menards": 0, "foundation": "市区公寓无风管/郊区独栋地下室", "climate": "Zone 5A/6A 湿冷上州大雪", "best": "郊区独栋地面件、复古暖气罩", "avoid": "市区公寓推地板风管件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "奥尔巴尼仓", "hdd": 5800, "cdd": 800, "frost_depth": 42, "water_hardness": 6.5, "salt_risk": "极高", "hazard": "上州大雪带极强腐蚀"},
  {"abbr": "WY", "en": "Wyoming", "cn": "怀俄明州", "region": "美西高地", "velocity": 846, "thd": 4, "lowes": 2, "menards": 2, "foundation": "全地下室人口稀少", "climate": "Zone 6B/7 极寒干燥大风", "best": "超耐寒重型五金", "avoid": "轻质薄件", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "夏延仓", "hdd": 7500, "cdd": 400, "frost_depth": 48, "water_hardness": 11.0, "salt_risk": "中", "hazard": "极端严寒暴风雪"},
  {"abbr": "MA", "en": "Massachusetts", "cn": "马萨诸塞州", "region": "美东北", "velocity": 846, "thd": 46, "lowes": 26, "menards": 0, "foundation": "水暖暖气片(Radiator)多", "climate": "Zone 5A 寒冷多雪近海湿冷", "best": "踢脚线出风口、复古铸铁风口", "avoid": "强排风管专属塑料件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "波士顿分仓", "hdd": 5600, "cdd": 750, "frost_depth": 36, "water_hardness": 3.8, "salt_risk": "高", "hazard": "近海湿冷大雪老房"},
  {"abbr": "NM", "en": "New Mexico", "cn": "新墨西哥州", "region": "美西南", "velocity": 823, "thd": 13, "lowes": 14, "menards": 0, "foundation": "水泥平板地基(Slab)为主", "climate": "Zone 4B/5B 沙漠干旱多风沙", "best": "防尘百叶、耐晒高温五金", "avoid": "地面下沉式出风口", "flooring": "瓷砖 50%, 水泥抛光 30%, 地毯 20%", "dc": "阿尔伯克基仓", "hdd": 4100, "cdd": 1400, "frost_depth": 16, "water_hardness": 14.0, "salt_risk": "极低", "hazard": "沙漠强风沙干旱硬水"},
  {"abbr": "MN", "en": "Minnesota", "cn": "明尼苏达州", "region": "美中北高寒", "velocity": 771, "thd": 33, "lowes": 13, "menards": 33, "foundation": "深层地下室但水暖多", "climate": "Zone 6A/7 极寒雪原", "best": "重型防冷凝风口、耐寒五金", "avoid": "易脆塑料", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "明尼阿波利斯仓", "hdd": 8200, "cdd": 600, "frost_depth": 60, "water_hardness": 16.2, "salt_risk": "极高", "hazard": "全美最深冻土之一(60寸)"},
  {"abbr": "NH", "en": "New Hampshire", "cn": "新罕布什尔州", "region": "美东北", "velocity": 756, "thd": 19, "lowes": 12, "menards": 0, "foundation": "石基与木屋", "climate": "Zone 5A/6A 林区寒冷", "best": "实木配风口、自然金属件", "avoid": "廉价塑料件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "曼彻斯特仓", "hdd": 6800, "cdd": 500, "frost_depth": 48, "water_hardness": 2.8, "salt_risk": "高", "hazard": "林区寒冬深冻"},
  {"abbr": "MS", "en": "Mississippi", "cn": "密西西比州", "region": "美东南", "velocity": 737, "thd": 16, "lowes": 24, "menards": 0, "foundation": "平板地基与浅架空", "climate": "Zone 3A 闷热高湿无冬", "best": "高抗湿防生锈件、天花排风罩", "avoid": "高端奢侈品", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "杰克逊仓", "hdd": 2400, "cdd": 2200, "frost_depth": 4, "water_hardness": 3.9, "salt_risk": "极低", "hazard": "极度闷热高湿白蚁"},
  {"abbr": "VT", "en": "Vermont", "cn": "佛蒙特州", "region": "美东北", "velocity": 717, "thd": 4, "lowes": 2, "menards": 0, "foundation": "全地下室山地木屋", "climate": "Zone 6A 寒冬多雪", "best": "环保无味风口、铸铝盖板", "avoid": "劣质塑料感产品", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "伯灵顿仓", "hdd": 7300, "cdd": 400, "frost_depth": 48, "water_hardness": 4.5, "salt_risk": "高", "hazard": "漫长积雪严寒"},
  {"abbr": "ND", "en": "North Dakota", "cn": "北达科他州", "region": "美中北极寒", "velocity": 671, "thd": 4, "lowes": 3, "menards": 8, "foundation": "防冻深层地下室", "climate": "Zone 6A/7 极寒半年冰封", "best": "结实金属风口、保温构件", "avoid": "脆性塑料", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "dc": "法戈仓", "hdd": 8900, "cdd": 500, "frost_depth": 65, "water_hardness": 17.5, "salt_risk": "极高", "hazard": "全美本土最高HDD(8900)"},
  {"abbr": "CT", "en": "Connecticut", "cn": "康涅狄格州", "region": "美东北", "velocity": 658, "thd": 30, "lowes": 14, "menards": 0, "foundation": "老房地下室但定制工程多", "climate": "Zone 5A 海洋微寒多雪", "best": "高档定制级拉丝金属风口", "avoid": "低档大众通用塑料", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "哈特福德仓", "hdd": 5300, "cdd": 850, "frost_depth": 36, "water_hardness": 4.2, "salt_risk": "高", "hazard": "沿海湿冷老房翻修"},
  {"abbr": "ME", "en": "Maine", "cn": "缅因州", "region": "美东北", "velocity": 634, "thd": 11, "lowes": 8, "menards": 0, "foundation": "传统地下室与岩基", "climate": "Zone 6A 沿海湿冷多雾", "best": "防潮耐盐雾金属件", "avoid": "不耐湿五金", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "波特兰仓", "hdd": 7500, "cdd": 350, "frost_depth": 48, "water_hardness": 2.5, "salt_risk": "高", "hazard": "海洋湿冷大雾盐雾"},
  {"abbr": "RI", "en": "Rhode Island", "cn": "罗德岛州", "region": "美东北", "velocity": 532, "thd": 7, "lowes": 4, "menards": 0, "foundation": "老房紧凑型", "climate": "Zone 5A 海洋微寒", "best": "常规标准修缮件", "avoid": "异形大件", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "普罗维登斯仓", "hdd": 5200, "cdd": 800, "frost_depth": 30, "water_hardness": 3.9, "salt_risk": "高", "hazard": "近海海风湿气"},
  {"abbr": "LA", "en": "Louisiana", "cn": "路易斯安那州", "region": "美南沿海", "velocity": 495, "thd": 27, "lowes": 31, "menards": 0, "foundation": "防洪高架柱/水泥平板", "climate": "Zone 2A/3A 极端湿热易涝", "best": "天花排风口、高耐蚀铝合金防锈件", "avoid": "地面下沉式出风口", "flooring": "瓷砖 50%, 抛光强化 30%, 地毯 20%", "dc": "新奥尔良仓", "hdd": 1600, "cdd": 2800, "frost_depth": 0, "water_hardness": 6.2, "salt_risk": "极低", "hazard": "飓风内涝极度湿热"},
  {"abbr": "NV", "en": "Nevada", "cn": "内华达州", "region": "美西南沙漠", "velocity": 460, "thd": 19, "lowes": 14, "menards": 0, "foundation": "100%混凝土平板(Slab)", "climate": "Zone 3B 极端干旱酷热沙漠", "best": "天花板可调风口、抗紫外线塑料件", "avoid": "地面出风口", "flooring": "瓷砖 50%, 强化复合 30%, 地毯 20%", "dc": "拉斯维加斯仓", "hdd": 2900, "cdd": 2800, "frost_depth": 10, "water_hardness": 16.8, "salt_risk": "极低", "hazard": "极端沙漠高温紫外线+硬水"},
  {"abbr": "WI", "en": "Wisconsin", "cn": "威斯康星州", "region": "美中大湖", "velocity": 456, "thd": 28, "lowes": 13, "menards": 44, "foundation": "全地下室普及", "climate": "Zone 5A/6A 漫长严寒多雪", "best": "重型金属地板出风口、防冻五金", "avoid": "天花专用风口", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "dc": "密尔沃基仓", "hdd": 7400, "cdd": 600, "frost_depth": 48, "water_hardness": 15.0, "salt_risk": "极高", "hazard": "严寒长冬融雪盐重灾区"},
  {"abbr": "TX", "en": "Texas", "cn": "德克萨斯州", "region": "美南核心", "velocity": 332, "thd": 180, "lowes": 142, "menards": 0, "foundation": "80%+混凝土平板地基(Slab)", "climate": "Zone 2A/3A/3B 漫长干热湿热", "best": "天花散流器、回风滤网格栅", "avoid": "地面下沉式出风口", "flooring": "瓷砖 50%, 水泥抛光 30%, 地毯 20%", "dc": "达拉斯/休斯敦大仓", "hdd": 1800, "cdd": 3100, "frost_depth": 2, "water_hardness": 13.5, "salt_risk": "极低", "hazard": "膨胀黏土大平板+极高CDD"},
  {"abbr": "AZ", "en": "Arizona", "cn": "亚利桑那州", "region": "美西南沙漠", "velocity": 289, "thd": 58, "lowes": 33, "menards": 0, "foundation": "绝大多数为混凝土平板", "climate": "Zone 2B 纯沙漠干热长酷暑", "best": "天花板空调扩散器、遮阳建材", "avoid": "地面风口", "flooring": "瓷砖 50%, 强化地板 30%, 地毯 20%", "dc": "凤凰城枢纽", "hdd": 1200, "cdd": 3800, "frost_depth": 0, "water_hardness": 17.8, "salt_risk": "极低", "hazard": "全美最高CDD(3800)+极硬水"},
  {"abbr": "CA", "en": "California", "cn": "加利福尼亚州", "region": "美西海岸", "velocity": 253, "thd": 232, "lowes": 113, "menards": 0, "foundation": "南加全平板/网点全美最密", "climate": "Zone 3B/4B 干燥温和干热", "best": "Title 24环保合规风口、天花格栅", "avoid": "高铅普通锻造件", "flooring": "瓷砖 45%, LVP 35%, 地毯 20%", "dc": "安大略/洛杉矶总仓", "hdd": 2000, "cdd": 1600, "frost_depth": 0, "water_hardness": 11.2, "salt_risk": "极低", "hazard": "WUI山火防飞烬+Prop 65"},
  {"abbr": "FL", "en": "Florida", "cn": "佛罗里达州", "region": "美东南半岛", "velocity": 234, "thd": 154, "lowes": 128, "menards": 0, "foundation": "95%+混凝土平板地基(Slab)", "climate": "Zone 1A/2A 极湿热高盐雾飓风", "best": "天花出风口、防腐铝/ABS配件", "avoid": "地面出风口", "flooring": "瓷砖 60%, 强化/LVP 25%, 地毯 15%", "dc": "奥兰多枢纽", "hdd": 650, "cdd": 3600, "frost_depth": 0, "water_hardness": 12.5, "salt_risk": "极低", "hazard": "HVHZ强飓风+全美最低HDD(650)"},
  {"abbr": "AK", "en": "Alaska", "cn": "阿拉斯加州", "region": "非本土极寒", "velocity": 920, "thd": 7, "lowes": 5, "menards": 0, "foundation": "永久冻土抬升/深基岩保温仓", "climate": "Zone 7/8 全美最高寒", "best": "超耐冻极温五金、重载保温出风件", "avoid": "常温塑料及薄冷轧铁", "flooring": "强化保温地板 50%, 实木 30%, 瓷砖 20%", "dc": "安克雷奇驳运仓", "hdd": 10500, "cdd": 20, "frost_depth": 72, "water_hardness": 7.5, "salt_risk": "高", "hazard": "永久冻土层+HDD突破10,000"},
  {"abbr": "HI", "en": "Hawaii", "cn": "夏威夷州", "region": "非本土海岛", "velocity": 410, "thd": 7, "lowes": 4, "menards": 0, "foundation": "火山岩地基/架空防潮桩", "climate": "Zone 1 强热带高盐雾高腐蚀", "best": "316/304不锈钢、纯ABS高防腐构件", "avoid": "含铁电镀件、地面出风口", "flooring": "耐水瓷砖 60%, 纯防水LVP 30%, 竹木 10%", "dc": "火奴鲁鲁海运仓", "hdd": 0, "cdd": 4200, "frost_depth": 0, "water_hardness": 4.2, "salt_risk": "极低", "hazard": "纯海岛极端高盐雾高氧化"}
]

# ==============================================================================
# 3. 规避截断的集合常量
# ==============================================================================
COLD_BASEMENT_STATES = {"NC", "TN", "KY", "IN", "OH", "MI", "WV", "IL", "PA", "AK"}
SLAB_HOT_STATES = {"FL", "TX", "AZ", "NV", "LA", "HI"}
HOT_CEILING_STATES = {"FL", "TX", "AZ", "NV", "CA", "GA", "HI"}
COLD_NORTH_STATES = {"MI", "ND", "MN", "WI", "AK"}
BASEBOARD_STATES = {"PA", "NY", "MA", "CT", "OH", "NJ", "RI"}

CURBLESS_SHOWER_STATES = {"FL", "CA", "TX", "NC", "SC", "GA", "AZ"}
FROST_VALVE_STATES = {"MN", "WI", "MI", "ND", "SD", "IL", "OH", "AK"}
NO_FREEZE_STATES = {"FL", "TX", "AZ", "HI"}

TILE_POPULAR_STATES = {"FL", "TX", "AZ", "CA", "NV", "HI"}
HARDWOOD_STATES = {"NC", "TN", "KY", "OH", "IN", "PA", "MI", "VA"}

WIND_COLD_STATES = {"KS", "NE", "ND", "SD", "MN", "IL", "OH", "MI", "NY", "AK"}
HURRICANE_STATES = {"FL", "NC", "SC", "TX", "LA", "AL", "HI"}

TRENCH_RAIN_STATES = {"FL", "LA", "TX", "WA", "OR", "GA", "NC", "SC", "HI"}
GUTTER_FOREST_STATES = {"NC", "GA", "TN", "VA", "PA", "OH", "MI", "OR", "WA"}

COASTAL_HUMID_STATES = {"FL", "HI", "SC", "NC", "LA"}
MODERN_WEST_STATES = {"WA", "OR", "CA", "CO", "UT"}
WUI_FIRE_STATES = {"CA", "CO", "OR", "WA", "NV"}

# ==============================================================================
# 4. 品类与四维属性配置
# ==============================================================================
CATEGORY_CONFIG = {
    "1. 暖通通风与空气分配 (HVAC & Ventilation)": {
        "tag": "HVAC",
        "short_name": "暖通通风",
        "intro": "受【HDD采暖度日 vs CDD制冷度日】及【地下室 vs 水泥平板】物理铁律绝对支配。",
        "positions": ["(全选)", "Floor (地面出风口)", "Ceiling (天花板散流器)", "Baseboard (踢脚线出风口)", "Sidewall (高侧墙回风格栅)"],
        "materials": ["(全选)", "Steel (冲压冷轧钢)", "Aluminum (铝合金)", "Plastic (ABS阻燃树脂)", "Cast Metal (重型铸铝/铸铁)", "Wood (橡木实木)"],
        "finishes": ["(全选)", "WH (White 经典白)", "BL (Matte Black 哑光黑)", "BN (Brushed Nickel 拉丝镍)", "AB (Antique Brass 仿古黄铜)", "ORB (Oil Rubbed Bronze 仿古深铜)"],
        "sizes": ["(全选)", "04X10 (全美走量王)", "04X12 (主流换新大号)", "02X12 (狭长缝/踢脚线)", "06X10 (大排量)", "12X12 (天花板方型)"]
    },
    "2. 卫浴五金与地漏给排水 (Plumbing & Bath Hardware)": {
        "tag": "PLUMBING",
        "short_name": "卫浴给排水",
        "intro": "受【冻土层深度(外墙长水阀)】与【水质硬度(水垢沉积与表面抗氧化)】决定。",
        "positions": ["(全选)", "Floor Drain (方形地面地漏)", "Linear Drain (长条隐形淋浴地漏)", "Frost-Proof Valve (室外防冻水阀)", "Shower Fixture (墙面花洒五金)"],
        "materials": ["(全选)", "Stainless Steel 304 (304不锈钢)", "Solid Brass (精铸无铅铜)", "ABS/PVC (耐腐工程塑料)", "Zinc Alloy (锌合金)"],
        "finishes": ["(全选)", "CP (Chrome 抛光亮铬)", "MB (Matte Black 现代哑光黑)", "BN (Brushed Nickel 经典拉丝镍)", "BG (Brushed Gold 拉丝金)"],
        "sizes": ["(全选)", "4x4 inch (标准方形)", "24-36 inch (长条隐形地漏)", "1/2 inch (常规水管接口)", "3/4 inch (主进水管接口)"]
    },
    "3. 地面收口压条与瓷砖金属辅料 (Flooring & Tile Trim)": {
        "tag": "FLOORING",
        "short_name": "地面收口压条",
        "intro": "受【冬靴融雪盐腐蚀化学风险】与【瓷砖 vs 实木地板分布】决定，涉及残疾人 ADA 防绊倒规范。",
        "positions": ["(全选)", "T-Molding (同高地面平接T条)", "Reducer (高低不平缓坡减速条)", "Tile Edge Trim (瓷砖L型防崩角条)", "Stair Nosing (木楼梯防滑包角)"],
        "materials": ["(全选)", "Anodized Aluminum (阳极氧化铝合金)", "Solid Brass (高端装饰铜)", "Stainless Steel (高耐磨不锈钢)", "PVC (柔性自粘条)"],
        "finishes": ["(全选)", "Silver/Matte (哑光拉丝银)", "Titanium Black (现代钛黑)", "Dark Bronze (仿古深铜)", "Wood Grain (木纹覆膜)"],
        "sizes": ["(全选)", "36 inch (单开门标准宽)", "72 inch (双扇门大跨度)", "8mm-10mm (常规瓷砖收口)", "12mm-15mm (厚板收口)"]
    },
    "4. 门窗五金与密封防风防暴 (Doors, Windows & Hardware)": {
        "tag": "DOORS",
        "short_name": "门窗密封五金",
        "intro": "北方寒冬穿堂狂风节能与沿海【飓风带 HVHZ 强制抗风压五金】是全美两大极端法典驱动力。",
        "positions": ["(全选)", "Door Bottom Sweep (门底防风挡水条)", "Weatherstripping (门框隔音密封条)", "Hurricane Tie (建筑抗飓风加固角码)", "Heavy Hinge (重载轴承门合页)"],
        "materials": ["(全选)", "Aluminum + Silicone (铝合金托底+耐候硅胶)", "Hot-Dip Galvanized (重型热浸镀锌钢)", "Solid Brass (重型纯铜)", "Stainless Steel (防锈不锈钢)"],
        "finishes": ["(全选)", "BL (Matte Black 哑光黑)", "Satin Nickel (缎面拉丝银)", "White (门框经典白)", "Zinc (工业镀锌银)"],
        "sizes": ["(全选)", "36 inch (标准单门宽)", "42 inch (大入户门底条)", "4x4 inch (重载大门合页)", "50 ft Roll (整卷密封条)"]
    },
    "5. 户外庭院、排水沟与结构件 (Outdoor Drainage & Patio)": {
        "tag": "OUTDOOR",
        "short_name": "庭院户外排水",
        "intro": "受【暴雨排涝负荷、秋季落叶堵塞天沟及西海岸 WUI 山火防飞烬网】决定。",
        "positions": ["(全选)", "Trench Drain (车道/泳池线性排水沟)", "Gutter Guard (屋檐排水天沟防叶滤网)", "Post Anchor Base (木露台立柱固定底座)", "Outdoor Vent (外墙防风雨冲压罩)"],
        "materials": ["(全选)", "Polymer/HDPE (耐暴晒重型塑料)", "Hot-Dip Galvanized (镀锌重钢格栅)", "Cast Iron (球墨铸铁重载盖板)", "Cast Aluminum (耐候防腐铸铝)"],
        "finishes": ["(全选)", "Black Asphalt (沥青防腐黑)", "Galvanized Silver (热镀锌防腐银)", "Natural Gray (水泥工程灰)"],
        "sizes": ["(全选)", "39 inch / 1 Meter (标准单段沟长)", "5-6 inch (全美标准屋檐天沟网)", "4x4 inch (木方柱底座)", "6x6 inch (重载立柱底座)"]
    }
}

# ==============================================================================
# 5. 顶层筛选控制器
# ==============================================================================
st.markdown('<div class="cat-selector">', unsafe_allow_html=True)
col_c1, col_c2, col_c3 = st.columns([1.5, 1.2, 1.3])

with col_c1:
    chosen_cat_name = st.selectbox("📂 核心产品品类 (Category)：", list(CATEGORY_CONFIG.keys()), index=0)
    cur_cat_conf = CATEGORY_CONFIG[chosen_cat_name]

with col_c2:
    season_choice = st.selectbox(
        "📅 规划出货节令 (Seasonality Pulse)：",
        [
            "全年平均基准 (Annual Baseline)",
            "Q1 春季化冻与庭院翻新 (Spring Thaw: 3-5月)",
            "Q2 夏季空调制冷高峰 (Peak Cooling: 6-8月)",
            "Q3 秋季落叶与入冬防寒准备 (Fall Weatherization: 9-11月)",
            "Q4 深冬极寒与防冻抢修 (Freeze Defense: 12-2月)"
        ],
        index=3
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
# 6. 融入工程物理与气象的计算引擎
# ==============================================================================
calculated_states = []

for s in STATES_DATA:
    abbr = s["abbr"]
    base_velocity = s["velocity"]
    
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
    
    # -------- 1. 品类与安装位置 (结合 HDD / CDD 物理指标) --------
    if cur_cat_conf["tag"] == "HVAC":
        if sel_pos == "Floor":
            if abbr in COLD_BASEMENT_STATES:
                weight *= 1.25
                reasons.append(f"全地下室主场，HDD采暖度日高达{s['hdd']:,}，地面热气上升")
            elif abbr in SLAB_HOT_STATES:
                weight *= 0.12
                reasons.append(f"水泥实心平板地基，CDD制冷度日高达{s['cdd']:,}，地面无风管")
        elif sel_pos == "Ceiling":
            if abbr in HOT_CEILING_STATES:
                weight *= 2.8
                reasons.append(f"长夏酷暑阳光带(CDD={s['cdd']:,})，天花板下吹冷风普及率全美第一")
            elif abbr in COLD_NORTH_STATES:
                weight *= 0.45
                reasons.append(f"北方极寒带(HDD={s['hdd']:,})以地板供暖为主，天花散流器少")
        elif sel_pos == "Baseboard":
            if abbr in BASEBOARD_STATES:
                weight *= 1.9
                reasons.append("美东老房水暖踢脚线与狭窄缝隙换新密集")

    elif cur_cat_conf["tag"] == "PLUMBING":
        if sel_pos in ["Linear", "Floor"]:
            if abbr in CURBLESS_SHOWER_STATES:
                weight *= 2.1
                reasons.append("现代无门槛大板淋浴房(Curbless Shower)翻新热潮")
        elif sel_pos == "Frost-Proof":
            if abbr in FROST_VALVE_STATES:
                weight *= 3.0
                reasons.append(f"冻土层深达{s['frost_depth']}寸，室外防冻阀是防爆管建筑规范硬性要求")
            elif abbr in NO_FREEZE_STATES:
                weight *= 0.05
                reasons.append(f"常年无冻结(冻土{s['frost_depth']}寸)，防冻水龙头几乎零出货")

    elif cur_cat_conf["tag"] == "FLOORING":
        if "Tile" in sel_pos:
            if abbr in TILE_POPULAR_STATES:
                weight *= 2.6
                reasons.append("通铺瓷砖大板为主流，金属防撞收口条极高频走货")
        elif "T-Molding" in sel_pos or "Reducer" in sel_pos:
            if abbr in HARDWOOD_STATES:
                weight *= 1.8
                reasons.append("实木与LVP木纹地板最大存量区，房间交界处压条标配")

    elif cur_cat_conf["tag"] == "DOORS":
        if "Sweep" in sel_pos or "Weatherstripping" in sel_pos:
            if abbr in WIND_COLD_STATES:
                weight *= 2.4
                reasons.append("北方寒冬穿堂风剧烈，门底封堵是降低高额电费的第一步")
        elif "Hurricane" in sel_pos:
            if abbr in HURRICANE_STATES:
                weight *= 3.5
                reasons.append("大西洋与海岛飓风带(HVHZ法规)强制要求高强度防风角码")

    elif cur_cat_conf["tag"] == "OUTDOOR":
        if "Trench" in sel_pos:
            if abbr in TRENCH_RAIN_STATES:
                weight *= 2.5
                reasons.append("强降雨量及多泳池环境，车道防内涝倒灌依赖深沟")
        elif "Gutter" in sel_pos:
            if abbr in GUTTER_FOREST_STATES:
                weight *= 2.2
                reasons.append("森林覆盖率极高，秋季防止枯叶塞死屋檐水管是刚需")

    # -------- 2. 融雪盐侵蚀与水硬度交叉计算 --------
    if s["salt_risk"] in ["高", "极高"] and cur_cat_conf["tag"] in ["HVAC", "FLOORING"]:
        if sel_mat in ["Steel"]:
            weight *= 0.85
            reasons.append("⚠️ 融雪盐靴底侵蚀严重，普通铁件有生锈退货隐患")
        elif sel_mat in ["Aluminum", "Stainless"]:
            weight *= 1.25
            reasons.append("✅ 耐融雪盐水侵蚀，符合大湖雪带防腐口碑偏好")

    if s["water_hardness"] > 12.0 and cur_cat_conf["tag"] == "PLUMBING":
        if sel_fin in ["CP"]:
            weight *= 0.85
            reasons.append(f"⚠️ 水质极硬({s['water_hardness']} GPG)，亮铬极易结顽固白斑水垢")
        elif sel_fin in ["BN", "MB"]:
            weight *= 1.25
            reasons.append(f"✅ 抗硬水水垢视觉残留，拉丝镍/哑光黑在硬水区大受欢迎")

    # -------- 3. 季节性脉冲加权 --------
    if "Q3 秋季" in season_choice:
        if cur_cat_conf["tag"] == "DOORS" and ("Sweep" in sel_pos or "Weatherstripping" in sel_pos):
            weight *= 1.6
            reasons.append("🍂 入冬防寒整备季（Fall Weatherization），销量脉冲式激增")
        elif cur_cat_conf["tag"] == "OUTDOOR" and "Gutter" in sel_pos:
            weight *= 1.8
            reasons.append("🍂 秋季落叶高峰期，天沟滤网迎来全美年度最高峰出货")
        elif cur_cat_conf["tag"] == "HVAC" and sel_pos == "Floor":
            weight *= 1.3
            reasons.append("🍂 入冬供暖系统检修换新，老旧风口成套更新")

    elif "Q2 夏季" in season_choice:
        if cur_cat_conf["tag"] == "HVAC" and sel_pos == "Ceiling":
            weight *= 1.7
            reasons.append("☀️ 全美酷暑制冷峰值，天花板散流器换新需求旺盛")
        elif cur_cat_conf["tag"] == "OUTDOOR" and "Trench" in sel_pos:
            weight *= 1.4
            reasons.append("☀️ 泳池建设与户外露台施工旺季")

    elif "Q4 深冬" in season_choice:
        if cur_cat_conf["tag"] == "PLUMBING" and sel_pos == "Frost-Proof":
            weight *= 2.0
            reasons.append("❄️ 极寒深度冰封，水管冻裂紧急抢修更换")
        elif cur_cat_conf["tag"] == "OUTDOOR":
            weight *= 0.4
            reasons.append("❄️ 户外冻土积雪，土建与庭院施工大面积停工")

    elif "Q1 春季" in season_choice:
        if cur_cat_conf["tag"] in ["FLOORING", "PLUMBING"]:
            weight *= 1.3
            reasons.append("🌱 美国春季退税到账（Tax Refund），室内卫浴与地板翻修热潮")

    if sel_size in ["04X10", "36", "4x4", "39"]:
        weight *= 1.15

    calc_vel = max(int(base_velocity * weight), 30)
    calc_total = calc_vel * active_stores
    
    item = dict(s)
    item["calc_vel"] = calc_vel
    item["calc_total"] = calc_total
    item["active_stores"] = active_stores
    item["reason_desc"] = "；".join(reasons) if reasons else f"符合【{cur_cat_conf['short_name']}】常态流速基线"
    calculated_states.append(item)

df_res = pd.DataFrame(calculated_states)
df_res["rank_vel"] = df_res["calc_vel"].rank(ascending=False, method="min").astype(int)
df_res["rank_total"] = df_res["calc_total"].rank(ascending=False, method="min").astype(int)

# ==============================================================================
# 7. 大卡片 KPI 看板
# ==============================================================================
sum_stores = int(df_res["active_stores"].sum())
sum_units = int(df_res["calc_total"].sum())
top_vel = df_res.sort_values(by="calc_vel", ascending=False).iloc[0]
top_total = df_res.sort_values(by="calc_total", ascending=False).iloc[0]

c_k1, c_k2, c_k3, c_k4 = st.columns(4)
with c_k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">分析渠道有效总门店</div>
        <div class="kpi-val">{sum_stores:,} 家</div>
    </div>
    """, unsafe_allow_html=True)

with c_k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">该节令·全美总采购吞吐预估</div>
        <div class="kpi-val">{sum_units:,} 件</div>
    </div>
    """, unsafe_allow_html=True)

with c_k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">单店动销第一强州 (平效冠军)</div>
        <div class="kpi-val">{top_vel['cn']} ({top_vel['calc_vel']:,} 件/店)</div>
    </div>
    """, unsafe_allow_html=True)

with c_k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">出货绝对总量霸主 (排产核心)</div>
        <div class="kpi-val">{top_total['cn']} ({top_total['calc_total']:,} 件)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 8. 排行大表与深度物理工程透视
# ==============================================================================
col_main_table, col_deep_inspect = st.columns([1.15, 0.85])

with col_main_table:
    view_mode = st.radio("切换主视角：", ["单店平均流速视角 (件/店)", "全州渠道总吞吐量视角 (件)"], horizontal=True)
    sort_key = "rank_vel" if "单店" in view_mode else "rank_total"
    
    df_sorted = df_res.sort_values(by=sort_key, ascending=True).reset_index(drop=True)
    df_sorted["序号"] = df_sorted.index + 1

    st.dataframe(
        df_sorted[[
            "序号", "abbr", "cn", "calc_vel", "calc_total", "active_stores",
            "climate", "frost_depth", "water_hardness", "salt_risk"
        ]],
        height=580,
        use_container_width=True,
        column_config={
            "序号": st.column_config.NumberColumn(width=45),
            "abbr": st.column_config.TextColumn("州简称", width=65),
            "cn": st.column_config.TextColumn("州全称", width=90),
            "calc_vel": st.column_config.ProgressColumn(
                "单店流速 (件/店)",
                min_value=0,
                max_value=int(df_res["calc_vel"].max()),
                format="%d"
            ),
            "calc_total": st.column_config.NumberColumn("渠道总销量", format="%d"),
            "active_stores": st.column_config.NumberColumn("门店", width=60),
            "climate": st.column_config.TextColumn("气候分区", width=105),
            "frost_depth": st.column_config.NumberColumn("冻土深(寸)", width=80),
            "water_hardness": st.column_config.NumberColumn("硬度(GPG)", width=85),
            "salt_risk": st.column_config.TextColumn("融雪盐", width=70)
        },
        hide_index=True
    )

with col_deep_inspect:
    st.markdown("#### 🔬 州级气象物理与建筑规范深度透视")
    target_abbr = st.selectbox("选择要透视的州：", df_sorted["abbr"].tolist(), index=0)
    st_info = df_sorted[df_sorted["abbr"] == target_abbr].iloc[0]

    st.markdown(f"### 📍 {st_info['cn']} ({st_info['abbr']}) · {st_info['region']}")
    
    sc1, sc2 = st.columns(2)
    with sc1:
        st.metric("预估单店出货能力", f"{st_info['calc_vel']:,} 件/店", f"全美排名: #{st_info['rank_vel']}")
    with sc2:
        st.metric("全渠道总采购需求", f"{st_info['calc_total']:,} 件", f"全美排名: #{st_info['rank_total']}")

    # 深度物理卡片面板
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(f"""
        <div class="physics-card">
            <b>🌡️ 能耗度日数 (ASHRAE)</b><br>
            • 采暖度日 (HDD): <b>{st_info['hdd']:,}</b><br>
            • 制冷度日 (CDD): <b>{st_info['cdd']:,}</b><br>
            <span style='font-size:0.78rem;color:#64748B;'>{'🔥 属于高能耗供暖核心区' if st_info['hdd']>5000 else '❄️ 属于高能耗强空调核心区'}</span>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown(f"""
        <div class="physics-card">
            <b>🧊 地质与水质红线</b><br>
            • 法定冻土深度: <b>{st_info['frost_depth']} 英寸</b><br>
            • 水质硬度: <b>{st_info['water_hardness']} GPG</b><br>
            • 融雪盐腐蚀风险: <b>{st_info['salt_risk']}</b>
        </div>
        """, unsafe_allow_html=True)

    st.info(f"**💡 驱动归因与物理测试反馈**：\n{st_info['reason_desc']}")
    st.write(f"**🏠 房屋基底形态**：{st_info['foundation']}")
    st.write(f"**⚠️ 当地极端气象标签**：`{st_info['hazard']}`")
    st.write(f"**🏬 区域门店网络**：THD: **{st_info['thd']}** 家 | Lowe's: **{st_info['lowes']}** 家 | Menards: **{st_info['menards']}** 家")
    st.success(f"**✅ 当地常规主推品**：{st_info['best']}")
    st.warning(f"**⚠️ 当地谨慎进入品**：{st_info['avoid']}")

    # 法务合规与工程测试警示
    radar_alerts = []
    if target_abbr == "CA":
        radar_alerts.append("⚠️ **加州 Prop 65 铅标** 与 **Title 24** 气密性能源审计标准。")
    if target_abbr in WUI_FIRE_STATES and cur_cat_conf["tag"] == "OUTDOOR":
        radar_alerts.append("🔥 **西海岸 WUI 山火防飞烬规范**：外墙/屋檐通风孔必须加装 1/8 英寸耐腐蚀不锈钢防火网（Ember Mesh）。")
    if target_abbr in HURRICANE_STATES and cur_cat_conf["tag"] in ["DOORS", "OUTDOOR"]:
        radar_alerts.append("🌪️ **飓风高风压法典 (HVHZ / Miami-Dade NOA)**：必须具备抗风压与飞弹冲击认证。")
    if st_info['frost_depth'] >= 30 and cur_cat_conf["tag"] == "PLUMBING" and "Frost" in sel_pos:
        radar_alerts.append(f"❄️ **水阀长度红线**：当地冻土层深达 {st_info['frost_depth']} 寸，采购商只接受 8~12 英寸以上超长杆防冻水阀！")

    if radar_alerts:
        st.markdown('<div class="radar-box">', unsafe_allow_html=True)
        st.markdown("**🛡️ 美国法务准入与县级建筑规范红线 (Engineering Redlines)：**")
        for alert in radar_alerts:
            st.markdown(alert)
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 9. 客群画像与退货率控制
# ==============================================================================
st.markdown("---")
st.markdown("### 📦 采购客群画像 (DIY vs Pro) 与退货率控制建议")

pro_col1, pro_col2, pro_col3 = st.columns(3)

if sel_size in ["04X10", "36"] and sel_fin in ["WH", "BL"]:
    diy_pct, pro_pct = 70, 30
    ret_rate = "3% ~ 5% (常规低风险)"
    pkg_type = "标准彩色吊卡 / 气泡热缩膜 (配螺丝)"
    advice = "大众标准化尺寸，普通家庭屋主一把螺丝刀即可更换，注重吊卡陈列的美观性。"
elif sel_size in ["02X12", "12X12", "72"] or "Hurricane" in sel_pos:
    diy_pct, pro_pct = 20, 80
    ret_rate = "1.5% (极低退货率)"
    pkg_type = "Contractor Pack (10-20件整箱牛皮纸工程包装)"
    advice = "多属专业木工或承包商采购，看重结实度与装箱经济性，建议做多件装降成本。"
else:
    diy_pct, pro_pct = 50, 50
    ret_rate = "7% ~ 10% (高退货高风险!)"
    pkg_type = "带 1:1 测量卡尺的防错彩盒包装"
    advice = "细分或复杂规格，消费者经常量错尺寸。包装必须醒目印上测量图指导安装。"

with pro_col1:
    st.metric("预估 DIY 个人散客占比", f"{diy_pct}%")
    st.caption("重视颜值陈列，需要傻瓜式说明书与配件。")

with pro_col2:
    st.metric("预估 Pro 专业承包商占比", f"{pro_pct}%")
    st.caption("整箱整托盘拉走，对公差挑剔，看重单件均价。")

with pro_col3:
    st.metric("全美预估退货率 (Return Rate)", ret_rate)
    st.markdown(f"**建议包装规格**：`{pkg_type}`")
    st.caption(f"**运营注意**：{advice}")

# ==============================================================================
# 10. 数据导出
# ==============================================================================
st.markdown("---")
csv_out = df_sorted[[
    "序号", "abbr", "cn", "en", "region", "calc_vel", "calc_total",
    "active_stores", "climate", "hdd", "cdd", "frost_depth", "water_hardness", "salt_risk", "hazard", "reason_desc"
]].to_csv(index=False).encode('utf-8-sig')

st.download_button(
    label=f"📥 导出【{cur_cat_conf['short_name']}】全美 50 州工程物理与销售决策模型报表 (.csv)",
    data=csv_out,
    file_name=f"US_Retail_Engineering_{cur_cat_conf['tag']}.csv",
    mime="text/csv"
)
