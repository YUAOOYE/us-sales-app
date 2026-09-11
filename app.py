import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 1. 页面配置与企业级专业 CSS
# ==============================================================================
st.set_page_config(
    page_title="北美大零售全品类与气候销售决策系统 (Grand Unified Pro)",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border-left: 5px solid #0284c7;
        padding: 14px 18px;
        margin-bottom: 12px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .physics-card {
        background-color: #f1f5f9;
        border: 1px solid #cbd5e1;
        padding: 12px 14px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1E40AF, #2563EB);
        color: white;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08);
    }
    .kpi-title { font-size: 0.84rem; opacity: 0.92; margin-bottom: 2px; font-weight: 500; }
    .kpi-val { font-size: 1.65rem; font-weight: 700; }
    .badge-diy { background-color: #dbeafe; color: #1e40af; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.82rem; }
    .badge-pro { background-color: #fef3c7; color: #92400e; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.82rem; }
    .badge-warning { background-color: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.82rem; }
    .badge-success { background-color: #dcfce7; color: #166534; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.82rem; }
    .radar-box { border-left: 4px solid #EF4444; background-color: #FEF2F2; padding: 10px 14px; border-radius: 0 6px 6px 0; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. 侧边栏：买手财务核算器与美国商业工程实战微百科
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shop.png", width=60)
    st.title("商超工程决策中台")
    st.caption("North American Retail & Climate Intelligence v5.0")
    st.markdown("---")
    
    st.markdown("### 💰 商超买手财务与毛利试算器")
    fob_cost = st.number_input("出厂供货成本 FOB ($/件)：", min_value=0.5, max_value=200.0, value=3.80, step=0.2)
    retail_msrp = st.number_input("商超建议零售价 MSRP ($/件)：", min_value=1.0, max_value=500.0, value=12.98, step=0.5)
    case_pack = st.number_input("标准外箱装箱数 (Case Pack)：", min_value=1, max_value=100, value=10, step=1)
    
    buyer_margin = ((retail_msrp - fob_cost) / retail_msrp) * 100
    gross_profit_per_unit = retail_msrp - fob_cost
    
    if buyer_margin < 42.0:
        st.markdown(f'<span class="badge-warning">⚠️ 商超毛利率：{buyer_margin:.1f}% (低于42%商超基准线)</span>', unsafe_allow_html=True)
    elif buyer_margin <= 55.0:
        st.markdown(f'<span class="badge-success">✅ 商超毛利率：{buyer_margin:.1f}% (符合42%~55%黄金区间)</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="badge-success">🌟 商超毛利率：{buyer_margin:.1f}% (超55%极具采购吸引力)</span>', unsafe_allow_html=True)
    
    st.caption(f"• 单件商超毛利: **${gross_profit_per_unit:.2f}** | 单箱货值(FOB): **${fob_cost * case_pack:.2f}**")
    st.markdown("---")

    st.markdown("### 📚 北美工程物理与零售实战百科")
    with st.expander("1. 地基形态：地下室 vs 水泥平板", expanded=False):
        st.write("""
        * **北方/中西部（全地下室）**：由于冻土层深，必须深挖地基建地下室。暖气炉在地下，**热空气自然上升**，地板出风口（Floor Register）是刚需。
        * **南方阳光带（水泥平板 Slab）**：地下水高或土质膨胀，直接浇筑实心水泥地，**地面无风管**！冷气由阁楼向下吹，出风口 100% 在天花板。
        """)
    with st.expander("2. ASHRAE 暖通与 HDD/CDD 度日", expanded=False):
        st.write("""
        * **HDD (采暖度日)**：> 5000 区域（如大湖雪带）长年烧暖气，风口承受 55℃~65℃ 干燥热风烘烤，防热变形是硬指标。
        * **CDD (制冷度日)**：> 2000 区域长夏高湿强冷气，天花散流器防结露防发霉是第一客诉源。
        """)
    with st.expander("3. Frost Line 冻土深度与长水阀", expanded=False):
        st.write("""
        北方冻土深达 36~60 英寸。去 Home Depot 买防冻龙头必须选 **8~12 英寸超长杆**，把阀芯送到室内保温区；南方 4 英寸短款即可。
        """)
    with st.expander("4. 融雪盐腐蚀与材质选择", expanded=False):
        st.write("""
        雪带冬季在道路狂撒融雪盐。靴底盐水带入玄关，冷轧钢风口和压条 2 年生锈烂穿。必须推**阳极氧化铝（6063）**或不锈钢。
        """)
    with st.expander("5. POG 货架排面（Facings）游戏规则", expanded=False):
        st.write("""
        商超货架按英寸计费。单店月流速 > 15 件可争取 **Double Facings (双排面 24寸)**，流速 < 5 件会面临下架或沦为底层冷门位。
        """)
    with st.expander("6. 美标托盘 (GMA) 与打托规范", expanded=False):
        st.write("""
        48 × 40 英寸木托盘，四向进叉。含托高度 ≤ 52 英寸，重 ≤ 2000 磅。外箱必须贴扫描级 GS1-128 / ITF-14 箱唛。
        """)
    with st.expander("7. Defective Allowance 残损扣款", expanded=False):
        st.write("""
        大商超合同常规定期在结算中扣取 **2% ~ 4%** 作为无理由退货与残损备用金。核算 FOB 成本必须计入此项。
        """)

# ==============================================================================
# 3. 核心全景数据库：全美 50 州（地基 + 气候 + 物理 + 门店 + 房龄 + 选品避雷）
# ==============================================================================
STATES_DATA = {
    "NC": {"cn": "北卡罗来纳州", "name": "North Carolina", "region": "美东南", "thd": 72, "lowes": 105, "menards": 0, "dc": "夏洛特(Lowe's大本营)", "foundation": "木结构架空层/地下室(75%+)", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "地面风口、实木高低压条、防潮五金", "avoid": "未做防腐冷轧薄铁件", "hdd": 3400, "cdd": 1600, "frost_depth": 12, "water_hardness": 3.0, "salt_risk": "中", "hazard": "沿海飓风/湿热雷暴", "house_age": 33, "hazard_idx": 5, "base_vel": 42.0},
    "TN": {"cn": "田纳西州", "name": "Tennessee", "region": "美南", "thd": 44, "lowes": 58, "menards": 0, "dc": "孟菲斯物流总仓", "foundation": "木结构架空层/地下室", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "重载地面风口、承重踏压件", "avoid": "天花专用下送风散流器", "hdd": 3500, "cdd": 1650, "frost_depth": 12, "water_hardness": 6.5, "salt_risk": "中", "hazard": "冻融交替/暴风雨", "house_age": 37, "hazard_idx": 4, "base_vel": 40.5},
    "KY": {"cn": "肯塔基州", "name": "Kentucky", "region": "美南", "thd": 27, "lowes": 38, "menards": 9, "dc": "路易斯维尔", "foundation": "全地下室占80%+", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "地下管道风口、复古铸铁件", "avoid": "无调节阀轻薄空框", "hdd": 4400, "cdd": 1250, "frost_depth": 20, "water_hardness": 10.5, "salt_risk": "高", "hazard": "冬季道路融雪盐结冰", "house_age": 43, "hazard_idx": 4, "base_vel": 38.0},
    "SC": {"cn": "南卡罗来纳州", "name": "South Carolina", "region": "美东南", "thd": 37, "lowes": 48, "menards": 0, "dc": "哥伦比亚/萨凡纳", "foundation": "架空层/沿海桩基", "flooring": "实木 40%, LVP 35%, 瓷砖 15%, 地毯 10%", "best": "工程ABS风口、耐盐雾构件", "avoid": "易锈金属、普通未防护碳钢", "hdd": 2400, "cdd": 2000, "frost_depth": 5, "water_hardness": 3.0, "salt_risk": "低", "hazard": "沿海强飓风/湿热腐蚀", "house_age": 31, "hazard_idx": 6, "base_vel": 36.0},
    "WV": {"cn": "西弗吉尼亚州", "name": "West Virginia", "region": "美东", "thd": 10, "lowes": 17, "menards": 1, "dc": "匹兹堡/查尔斯顿", "foundation": "山地深地基/全地下室", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "best": "抗重压地面风口、防冻五金", "avoid": "低温脆性塑料件", "hdd": 5000, "cdd": 950, "frost_depth": 30, "water_hardness": 7.0, "salt_risk": "高", "hazard": "山地积雪重融雪盐", "house_age": 52, "hazard_idx": 5, "base_vel": 34.0},
    "VA": {"cn": "弗吉尼亚州", "name": "Virginia", "region": "美东", "thd": 50, "lowes": 61, "menards": 0, "dc": "里士满仓", "foundation": "地下室/架空层老房多", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "中高端装饰风口、精工五金", "avoid": "粗糙廉价工程件", "hdd": 3900, "cdd": 1450, "frost_depth": 18, "water_hardness": 5.0, "salt_risk": "高", "hazard": "沿海湿润冻融交替", "house_age": 42, "hazard_idx": 4, "base_vel": 33.5},
    "OH": {"cn": "俄亥俄州", "name": "Ohio", "region": "美中", "thd": 71, "lowes": 73, "menards": 34, "dc": "哥伦布核心仓", "foundation": "100%全地下室为主", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "冲压金属/铝合金地面风口", "avoid": "薄脆塑料、天花散流器", "hdd": 5600, "cdd": 850, "frost_depth": 36, "water_hardness": 15.0, "salt_risk": "极高", "hazard": "暴雪融雪盐侵蚀+极硬水", "house_age": 54, "hazard_idx": 7, "base_vel": 32.0},
    "IN": {"cn": "印第安纳州", "name": "Indiana", "region": "美中", "thd": 41, "lowes": 42, "menards": 39, "dc": "印第安纳波利斯", "foundation": "全地下室占85%+", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "地面暖风风口、防结露件", "avoid": "天花专用风口", "hdd": 5500, "cdd": 1000, "frost_depth": 36, "water_hardness": 17.0, "salt_risk": "极高", "hazard": "重度硬水结垢/大雪盐蚀", "house_age": 48, "hazard_idx": 6, "base_vel": 31.5},
    "IL": {"cn": "伊利诺伊州", "name": "Illinois", "region": "美中", "thd": 81, "lowes": 43, "menards": 61, "dc": "大芝加哥枢纽", "foundation": "全地下室占绝大多数", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "重型地面出风口、阳极铝压条", "avoid": "轻薄无卡扣风口", "hdd": 6100, "cdd": 900, "frost_depth": 42, "water_hardness": 14.5, "salt_risk": "极高", "hazard": "芝加哥狂风暴雪融雪盐", "house_age": 56, "hazard_idx": 7, "base_vel": 30.0},
    "MI": {"cn": "密歇根州", "name": "Michigan", "region": "美中", "thd": 70, "lowes": 43, "menards": 44, "dc": "底特律仓", "foundation": "100%全地下室", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "经典地面金属风口、耐雪盐件", "avoid": "天花风口、薄铁喷漆", "hdd": 6800, "cdd": 650, "frost_depth": 48, "water_hardness": 12.0, "salt_risk": "极高", "hazard": "大湖雪带超长严冬", "house_age": 52, "hazard_idx": 7, "base_vel": 29.5},
    "PA": {"cn": "宾夕法尼亚州", "name": "Pennsylvania", "region": "美东", "thd": 73, "lowes": 83, "menards": 0, "dc": "阿伦敦/费城", "foundation": "老房地下室比例极高", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "复古雕花金属风口、铸铁件", "avoid": "现代极简无框塑料", "hdd": 5400, "cdd": 900, "frost_depth": 38, "water_hardness": 8.5, "salt_risk": "极高", "hazard": "阿巴拉契亚冻融融雪盐", "house_age": 58, "hazard_idx": 7, "base_vel": 28.5},
    "MO": {"cn": "密苏里州", "name": "Missouri", "region": "美中", "thd": 39, "lowes": 33, "menards": 19, "dc": "圣路易斯", "foundation": "传统全地下室木屋", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "best": "地面可调风口、管件辅料", "avoid": "纯热带建材", "hdd": 4800, "cdd": 1400, "frost_depth": 28, "water_hardness": 11.0, "salt_risk": "高", "hazard": "剧烈温差冰融循环", "house_age": 47, "hazard_idx": 5, "base_vel": 27.5},
    "GA": {"cn": "乔治亚州", "name": "Georgia", "region": "美东南", "thd": 91, "lowes": 65, "menards": 0, "dc": "亚特兰大(THD全球总部)", "foundation": "北架空层/南水泥平板", "flooring": "LVP 40%, 瓷砖 35%, 地毯 25%", "best": "天花与地面品类分推、防腐件", "avoid": "全推纯地面件", "hdd": 2700, "cdd": 1850, "frost_depth": 5, "water_hardness": 3.5, "salt_risk": "低", "hazard": "长夏湿热白蚁雷暴", "house_age": 31, "hazard_idx": 5, "base_vel": 27.0},
    "NY": {"cn": "纽约州", "name": "New York", "region": "美东北", "thd": 100, "lowes": 68, "menards": 0, "dc": "奥尔巴尼/水牛城", "foundation": "市区公寓无风管/郊区独栋地下室", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "郊区独栋地面件、复古暖气罩", "avoid": "对市区公寓推地板风管件", "hdd": 5900, "cdd": 800, "frost_depth": 48, "water_hardness": 5.5, "salt_risk": "极高", "hazard": "水牛城湖效应暴雪+老房改建", "house_age": 62, "hazard_idx": 7, "base_vel": 26.0},
    "WI": {"cn": "威斯康星州", "name": "Wisconsin", "region": "美中", "thd": 28, "lowes": 14, "menards": 45, "dc": "欧克莱尔(Menards大本营)", "foundation": "全地下室普及率极高", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "重型金属地板出风口、防冻五金", "avoid": "天花专用风口", "hdd": 7400, "cdd": 550, "frost_depth": 54, "water_hardness": 14.5, "salt_risk": "极高", "hazard": "漫长严冬暴雪强融雪盐", "house_age": 51, "hazard_idx": 7, "base_vel": 25.5},
    "MN": {"cn": "明尼苏达州", "name": "Minnesota", "region": "美中", "thd": 35, "lowes": 12, "menards": 38, "dc": "明尼阿波利斯", "foundation": "深层地下室但水暖暖气片多", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "best": "防冷凝风口、超长水阀(12寸)", "avoid": "易脆塑料、短水阀", "hdd": 8500, "cdd": 550, "frost_depth": 60, "water_hardness": 14.0, "salt_risk": "极高", "hazard": "全美最深冻土(60寸)极寒", "house_age": 46, "hazard_idx": 8, "base_vel": 24.5},
    "CO": {"cn": "科罗拉多州", "name": "Colorado", "region": "山地大区", "thd": 47, "lowes": 28, "menards": 0, "dc": "丹佛物流仓", "foundation": "防冻全地下室", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "best": "气密保温风口、实木嵌入风口", "avoid": "漏风劣质薄件", "hdd": 6200, "cdd": 600, "frost_depth": 36, "water_hardness": 7.5, "salt_risk": "高", "hazard": "WUI山火防飞烬/强紫外线", "house_age": 38, "hazard_idx": 5, "base_vel": 24.0},
    "TX": {"cn": "德克萨斯州", "name": "Texas", "region": "美南核心", "thd": 182, "lowes": 145, "menards": 0, "dc": "达拉斯/休斯敦大仓", "foundation": "85%+混凝土实心大平板(Slab)", "flooring": "瓷砖 50%, 抛光强化 30%, 地毯 20%", "best": "天花散流器、回风百叶格栅", "avoid": "地面下沉式出风口(无孔可用!)", "hdd": 1600, "cdd": 3000, "frost_depth": 5, "water_hardness": 12.5, "salt_risk": "低", "hazard": "酷暑极干热/偶发寒潮破管", "house_age": 31, "hazard_idx": 6, "base_vel": 22.0},
    "FL": {"cn": "佛罗里达州", "name": "Florida", "region": "美东南", "thd": 155, "lowes": 110, "menards": 0, "dc": "奥兰多/迈阿密", "foundation": "95%+混凝土平板地基(Slab)", "flooring": "瓷砖 60%, 强化/LVP 25%, 地毯 15%", "best": "天花散流器、铝/ABS防腐地漏", "avoid": "地面出风口(绝对禁发货!)", "hdd": 500, "cdd": 3800, "frost_depth": 0, "water_hardness": 14.0, "salt_risk": "极低", "hazard": "HVHZ五级强飓风/极高盐雾", "house_age": 34, "hazard_idx": 9, "base_vel": 21.0},
    "CA": {"cn": "加利福尼亚州", "name": "California", "region": "美西", "thd": 234, "lowes": 112, "menards": 0, "dc": "洛杉矶/安大略总仓", "foundation": "南加全平板/网点极密", "flooring": "瓷砖 45%, LVP 35%, 地毯 20%", "best": "Title 24环保风口、WUI防飞烬网", "avoid": "高铅铸造件、普通易燃塑料", "hdd": 2100, "cdd": 1300, "frost_depth": 0, "water_hardness": 9.5, "salt_risk": "极低", "hazard": "WUI山火/地震/Prop 65铅标", "house_age": 48, "hazard_idx": 7, "base_vel": 20.0},
    "WA": {"cn": "华盛顿州", "name": "Washington", "region": "美西北", "thd": 48, "lowes": 38, "menards": 0, "dc": "西雅图枢纽", "foundation": "架空层与现代高气密住宅", "flooring": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "best": "极简线形风口、哑光黑五金", "avoid": "过时粗糙件、易生锈铁", "hdd": 4900, "cdd": 300, "frost_depth": 18, "water_hardness": 2.5, "salt_risk": "低", "hazard": "长年阴雨高湿室内霉菌", "house_age": 43, "hazard_idx": 4, "base_vel": 23.5},
    "AZ": {"cn": "亚利桑那州", "name": "Arizona", "region": "美西南", "thd": 58, "lowes": 33, "menards": 0, "dc": "凤凰城", "foundation": "绝大多数为混凝土平板", "flooring": "瓷砖 50%, 强化地板 30%, 地毯 20%", "best": "天花散流器、遮阳与抗晒五金", "avoid": "地面出风口", "hdd": 1200, "cdd": 3500, "frost_depth": 0, "water_hardness": 16.5, "salt_risk": "极低", "hazard": "全美最高CDD沙漠酷暑+极硬水", "house_age": 30, "hazard_idx": 3, "base_vel": 19.5},
    "AK": {"cn": "阿拉斯加州", "name": "Alaska", "region": "美西北", "thd": 7, "lowes": 5, "menards": 0, "dc": "安克雷奇驳运仓", "foundation": "永久冻土抬升/深基保温仓", "flooring": "强化保温 50%, 实木 30%, 瓷砖 20%", "best": "超耐极温五金、重载保温出风件", "avoid": "常温薄脆塑料及冷轧薄铁", "hdd": 10500, "cdd": 0, "frost_depth": 72, "water_hardness": 6.0, "salt_risk": "中", "hazard": "永久冻土层+HDD突破10,000", "house_age": 42, "hazard_idx": 8, "base_vel": 25.0},
    "HI": {"cn": "夏威夷州", "name": "Hawaii", "region": "美西", "thd": 7, "lowes": 4, "menards": 0, "dc": "火奴鲁鲁海运仓", "foundation": "火山岩/架空防潮桩", "flooring": "耐水瓷砖 60%, 防水LVP 30%, 竹木 10%", "best": "316/304不锈钢、纯ABS防腐件", "avoid": "含铁电镀件、地面出风口", "hdd": 0, "cdd": 4200, "frost_depth": 0, "water_hardness": 3.0, "salt_risk": "低", "hazard": "纯海岛极端高盐雾高氧化", "house_age": 47, "hazard_idx": 6, "base_vel": 18.0}
}

# 补充其余各州的基础物理参数，确保 50 州完整
EXTRA_STATES = {
    "AL": {"cn": "阿拉巴马", "name": "Alabama", "reg": "美东南", "thd": 29, "low": 34, "men": 0, "dc": "伯明翰", "hdd": 2600, "cdd": 1900, "fd": 5, "wh": 4.5, "sr": "低", "haz": "雷暴", "age": 36, "v": 28.0},
    "AR": {"cn": "阿肯色", "name": "Arkansas", "reg": "美南", "thd": 15, "low": 20, "men": 0, "dc": "小石城", "hdd": 3200, "cdd": 1700, "fd": 10, "wh": 5.0, "sr": "低", "haz": "雷暴", "age": 39, "v": 27.0},
    "CT": {"cn": "康涅狄格", "name": "Connecticut", "reg": "美东北", "thd": 30, "low": 16, "men": 0, "dc": "哈特福德", "hdd": 5800, "cdd": 750, "fd": 42, "wh": 4.0, "sr": "极高", "haz": "老旧改建", "age": 59, "v": 26.0},
    "DE": {"cn": "特拉华", "name": "Delaware", "reg": "美东", "thd": 9, "low": 6, "men": 0, "dc": "费城", "hdd": 4600, "cdd": 1200, "fd": 24, "wh": 5.5, "sr": "高", "haz": "海盐", "age": 41, "v": 27.5},
    "ID": {"cn": "爱达荷", "name": "Idaho", "reg": "美西北", "thd": 13, "low": 8, "men": 0, "dc": "盐湖城", "hdd": 6800, "cdd": 550, "fd": 36, "wh": 8.0, "sr": "高", "haz": "冻融", "age": 33, "v": 29.0},
    "IA": {"cn": "爱荷华", "name": "Iowa", "reg": "美中", "thd": 16, "low": 15, "men": 22, "dc": "得梅因", "hdd": 6700, "cdd": 850, "fd": 48, "wh": 16.0, "sr": "极高", "haz": "雪盐", "age": 54, "v": 28.0},
    "KS": {"cn": "堪萨斯", "name": "Kansas", "reg": "美中", "thd": 18, "low": 14, "men": 9, "dc": "堪萨斯城", "hdd": 5000, "cdd": 1350, "fd": 30, "wh": 13.5, "sr": "高", "haz": "狂风", "age": 47, "v": 28.5},
    "LA": {"cn": "路易斯安那", "name": "Louisiana", "reg": "美南", "thd": 28, "low": 30, "men": 0, "dc": "新奥尔良", "hdd": 1600, "cdd": 2600, "fd": 0, "wh": 4.5, "sr": "极低", "haz": "飓风湿热", "age": 41, "v": 21.5},
    "ME": {"cn": "缅因", "name": "Maine", "reg": "美东北", "thd": 11, "low": 10, "men": 0, "dc": "波特兰", "hdd": 7800, "cdd": 300, "fd": 54, "wh": 3.0, "sr": "极高", "haz": "海雾严冬", "age": 53, "v": 25.0},
    "MD": {"cn": "马里兰", "name": "Maryland", "reg": "美东", "thd": 43, "low": 30, "men": 0, "dc": "巴尔的摩", "hdd": 4500, "cdd": 1300, "fd": 24, "wh": 6.5, "sr": "高", "haz": "湾区潮湿", "age": 46, "v": 28.0},
    "MA": {"cn": "马萨诸塞", "name": "Massachusetts", "reg": "美东北", "thd": 45, "low": 29, "men": 0, "dc": "波士顿", "hdd": 5900, "cdd": 700, "fd": 48, "wh": 3.5, "sr": "极高", "haz": "老房水暖", "age": 60, "v": 26.5},
    "MS": {"cn": "密西西比", "name": "Mississippi", "reg": "美南", "thd": 16, "low": 22, "men": 0, "dc": "杰克逊", "hdd": 2300, "cdd": 2100, "fd": 0, "wh": 3.5, "sr": "极低", "haz": "高湿热", "age": 39, "v": 22.0},
    "MT": {"cn": "蒙大拿", "name": "Montana", "reg": "美西北", "thd": 8, "low": 5, "men": 0, "dc": "比灵斯", "hdd": 7900, "cdd": 400, "fd": 54, "wh": 9.0, "sr": "高", "haz": "深冻土", "age": 45, "v": 25.5},
    "NE": {"cn": "内布拉斯加", "name": "Nebraska", "reg": "美中", "thd": 11, "low": 7, "men": 10, "dc": "奥马哈", "hdd": 6200, "cdd": 950, "fd": 42, "wh": 13.5, "sr": "极高", "haz": "雪蚀", "age": 49, "v": 26.5},
    "NV": {"cn": "内华达", "name": "Nevada", "reg": "美西", "thd": 21, "low": 17, "men": 0, "dc": "拉斯维加斯", "hdd": 2800, "cdd": 2600, "fd": 12, "wh": 18.0, "sr": "极低", "haz": "硬水高温", "age": 28, "v": 20.5},
    "NH": {"cn": "新罕布什尔", "name": "New Hampshire", "reg": "美东北", "thd": 17, "low": 11, "men": 0, "dc": "曼彻斯特", "hdd": 7100, "cdd": 450, "fd": 50, "wh": 2.5, "sr": "极高", "haz": "林区寒冬", "age": 48, "v": 25.5},
    "NJ": {"cn": "新泽西", "name": "New Jersey", "reg": "美东北", "thd": 65, "low": 40, "men": 0, "dc": "纽瓦克", "hdd": 4900, "cdd": 1200, "fd": 30, "wh": 6.5, "sr": "极高", "haz": "化冰盐腐蚀", "age": 57, "v": 27.5},
    "NM": {"cn": "新墨西哥", "name": "New Mexico", "reg": "美西南", "thd": 17, "low": 13, "men": 0, "dc": "阿尔伯克基", "hdd": 3800, "cdd": 1500, "fd": 18, "wh": 13.0, "sr": "低", "haz": "风沙硬水", "age": 36, "v": 22.5},
    "ND": {"cn": "北达科他", "name": "North Dakota", "reg": "美中", "thd": 4, "low": 3, "men": 8, "dc": "法戈", "hdd": 9400, "cdd": 450, "fd": 66, "wh": 13.0, "sr": "极高", "haz": "最高HDD极寒", "age": 45, "v": 24.5},
    "OK": {"cn": "俄克拉荷马", "name": "Oklahoma", "reg": "美南", "thd": 21, "low": 24, "men": 0, "dc": "达拉斯", "hdd": 3400, "cdd": 1900, "fd": 15, "wh": 11.5, "sr": "中", "haz": "龙卷风", "age": 40, "v": 26.0},
    "OR": {"cn": "俄勒冈", "name": "Oregon", "reg": "美西北", "thd": 27, "low": 18, "men": 0, "dc": "波特兰", "hdd": 4600, "cdd": 400, "fd": 12, "wh": 2.0, "sr": "低", "haz": "长年阴雨", "age": 43, "v": 26.5},
    "RI": {"cn": "罗德岛", "name": "Rhode Island", "reg": "美东北", "thd": 7, "low": 5, "men": 0, "dc": "普罗维登斯", "hdd": 5600, "cdd": 750, "fd": 40, "wh": 3.5, "sr": "极高", "haz": "海盐雪蚀", "age": 60, "v": 25.0},
    "SD": {"cn": "南达科他", "name": "South Dakota", "reg": "美中", "thd": 3, "low": 3, "men": 5, "dc": "苏瀑", "hdd": 7600, "cdd": 700, "fd": 54, "wh": 16.5, "sr": "极高", "haz": "深冻土", "age": 47, "v": 25.0},
    "UT": {"cn": "犹他", "name": "Utah", "reg": "山地大区", "thd": 24, "low": 14, "men": 0, "dc": "盐湖城", "hdd": 5800, "cdd": 1050, "fd": 30, "wh": 17.5, "sr": "高", "haz": "大温差硬水", "age": 32, "v": 25.5},
    "VT": {"cn": "佛蒙特", "name": "Vermont", "reg": "美东北", "thd": 5, "low": 4, "men": 0, "dc": "伯灵顿", "hdd": 7600, "cdd": 350, "fd": 54, "wh": 4.5, "sr": "极高", "haz": "漫长积雪", "age": 51, "v": 24.5},
    "WY": {"cn": "怀俄明", "name": "Wyoming", "reg": "山地大区", "thd": 5, "low": 3, "men": 2, "dc": "夏延", "hdd": 7500, "cdd": 350, "fd": 50, "wh": 11.0, "sr": "高", "haz": "极高寒", "age": 42, "v": 23.5}
}

for k, v in EXTRA_STATES.items():
    if k not in STATES_DATA:
        STATES_DATA[k] = {
            "cn": v["cn"] + "州", "name": v["name"], "region": v["reg"], "thd": v["thd"], "lowes": v["low"], "menards": v["men"],
            "dc": v["dc"], "foundation": "全地下室/标准木结构", "flooring": "实木 40%, LVP 35%, 瓷砖 15%",
            "best": "常规标准修缮件", "avoid": "非标异形件", "hdd": v["hdd"], "cdd": v["cdd"],
            "frost_depth": v["fd"], "water_hardness": v["wh"], "salt_risk": v["sr"],
            "hazard": v["haz"], "house_age": v["age"], "hazard_idx": 5, "base_vel": v["v"]
        }

df_states = pd.DataFrame.from_dict(STATES_DATA, orient="index")
df_states["total_stores"] = df_states["thd"] + df_states["lowes"] + df_states["menards"]

# 物流海运港口字典
PORT_LOGISTICS_MATRIX = {
    "美西": {"port": "洛杉矶 / 长滩港 (LA / Long Beach)", "transit_sea": "快船 14~16 天直达", "inland_mode": "港口短驳至安大略/奇诺仓 (Ontario/Chino)", "freight_level": "海运费最低，旺季塞港风险大。"},
    "美西北": {"port": "西雅图 / 塔科马港 (Seattle / Tacoma)", "transit_sea": "直达快船 15~18 天", "inland_mode": "直接覆盖华州、俄勒冈配送中心", "freight_level": "避开南加州塞港，西北高湿防潮包装需加强。"},
    "美东": {"port": "诺福克港 (Norfolk) / 萨凡纳港", "transit_sea": "巴拿马全水路 30~34 天", "inland_mode": "卡车派送弗吉尼亚、宾州分拨仓", "freight_level": "全水路综合成本低，时效稳定。"},
    "美东南": {"port": "萨凡纳港 (Savannah) / 查尔斯顿港", "transit_sea": "全水路 28~32 天", "inland_mode": "直达 Lowe's夏洛特总部及 Home Depot亚特兰大总仓", "freight_level": "全美建材出海第一黄金航线，极其顺畅。"},
    "美南核心": {"port": "休斯敦港 (Houston)", "transit_sea": "全水路直达墨西哥湾 30~35 天", "inland_mode": "拖车直达达拉斯/休斯敦仓储中心", "freight_level": "规避铁路转运费，单柜省 $1,200+。"},
    "美中": {"port": "美西清关转内陆铁路 (IPI to Chicago)", "transit_sea": "海运 15 天 + BNSF/UP 铁路班列 7 天", "inland_mode": "芝加哥铁路堆场提柜，短驳至中西部 DC", "freight_level": "监控旺季堆场滞期费及底盘车轮转。"},
    "美东北": {"port": "纽约 / 新泽西港 (NY / NJ)", "transit_sea": "全水路 32~36 天", "inland_mode": "直达纽瓦克、宾州理海谷仓储带", "freight_level": "直击老宅翻新修缮市场，码头清关效率高。"},
    "山地大区": {"port": "长滩港提柜内陆转铁 (Denver/Salt Lake)", "transit_sea": "海运 15 天 + 丹佛铁路 5 天", "inland_mode": "丹佛/盐湖城枢纽卡车分拨", "freight_level": "冬季暴雪易封路，留足安全库存。"}
}

# ==============================================================================
# 4. 品类与四维属性深度定义
# ==============================================================================
CATEGORY_CONFIG = {
    "HVAC": {
        "name": "暖通出风口与回风系统 (Registers & Grilles)",
        "positions": ["Floor (地面出风口)", "Ceiling (天花板散流器)", "Baseboard (踢脚线出风口)", "Sidewall (高侧墙回风格栅)"],
        "materials": ["Steel (冲压冷轧钢)", "Aluminum (铝合金阳极氧化)", "Cast Metal (铸铝粉末喷涂)", "Plastic (ABS阻燃工程塑料)", "Wood (橡木实木嵌入)"],
        "finishes": ["BL (Matte Black 哑光黑)", "BN (Brushed Nickel 拉丝镍)", "WH (White 经典工程白)", "AB (Antique Brass 仿古黄铜)", "ORB (Oil Rubbed Bronze 油磨青铜)"],
        "sizes": ["04X10 (全美走量王 65%)", "04X12 (主流换新大号 20%)", "02X12 (踢脚狭长缝 10%)", "06X10 (大排风量 5%)", "12X12 (天花板方型)"],
        "compliance": ["ASHRAE 70 (风量与噪音 NC 评级测试)", "UL 94 (塑料部件阻燃 V-0)", "Heel-Proof 细高跟鞋防卡规范 (<9.5mm)", "静态抗踩踏承重 > 300 lbs 测试"]
    },
    "PLUMBING": {
        "name": "卫浴水暖与排水构件 (Drains & Plumbing)",
        "positions": ["Floor Drain (方形地面地漏)", "Linear Drain (长条隐形淋浴地漏)", "Frost-Proof Valve (室外防冻长水阀)", "Wall Mount (墙面淋浴花洒五金)"],
        "materials": ["Stainless 304 (304不锈钢拉丝)", "Stainless 316 (316高盐雾海洋级)", "Solid Brass (无铅锻压黄铜)", "ABS/PVC (耐腐工程塑料)"],
        "finishes": ["BN (Brushed Nickel 经典拉丝镍)", "MB (Matte Black 现代哑光黑)", "CP (Chrome 抛光亮铬)", "BG (Brushed Gold 拉丝金)"],
        "sizes": ["4x4 inch (标准方形地漏)", "24-36 inch (长条形隐形地漏)", "1/2 inch (常规进水接口)", "3/4 inch (主水管接口)"],
        "compliance": ["cUPC 强制认证 (IAPMO)", "ASME A112.18.2 / CSA B125.2 (地漏通量测试)", "NSF/ANSI 61 & 372 (接触饮用水无铅安全标准)"]
    },
    "FLOORING": {
        "name": "地面收口与过渡压条 (Flooring Transitions & Trim)",
        "positions": ["T-Molding (同高平接T型条)", "Reducer (高低落差缓坡条)", "Tile Edge (瓷砖L型防崩角条)", "Stair Nosing (木楼梯踏步包角)"],
        "materials": ["Anodized Aluminum (阳极氧化铝合金)", "Stainless Steel (高耐磨不锈钢)", "Solid Hardwood (实木贴皮/原木)", "PVC/SPC (石塑自粘条)"],
        "finishes": ["Silver/Matte (哑光拉丝银)", "Titanium Black (现代钛黑)", "Champagne (香槟金)", "Dark Bronze (仿古深铜)"],
        "sizes": ["36 inch (单开门标准宽)", "72 inch (双开门大跨度)", "8mm-10mm (常规瓷砖收口)", "12mm-15mm (大理石厚板收口)"],
        "compliance": ["ADA Section 303 (轮椅无障碍过渡斜率 ≤ 1:2 防绊倒)", "ASTM C1028 (表面防滑摩擦系数)", "推车过槛抗凹陷强度测试"]
    },
    "DOORS": {
        "name": "建筑门窗五金与密封防暴 (Doors & Window Hardware)",
        "positions": ["Door Bottom Sweep (门底防风挡水密封条)", "Weatherstripping (门框隔音密封条)", "Hurricane Tie (建筑抗飓风加固角码)", "Heavy Hinge (重载轴承门合页)"],
        "materials": ["Aluminum + Silicone (铝合金+耐候硅胶)", "Hot-Dip Galvanized (重型热浸镀锌钢)", "304 Stainless (防锈不锈钢)", "Solid Brass (重型纯铜)"],
        "finishes": ["BL (Matte Black 哑光黑)", "Satin Nickel (缎面拉丝银)", "White (门框经典白)", "Zinc (工业镀锌银)"],
        "sizes": ["36 inch (标准单门底条)", "42 inch (大入户门底条)", "4x4 inch (重载大门合页)", "50 ft Roll (50英尺整卷密封条)"],
        "compliance": ["ANSI/BHMA A156.1 (100万次开合疲劳测试)", "ASTM E1886 / E1996 (迈阿密戴德县 HVHZ 抗飞弹飓风测试)", "UL 10C (90分钟防火门认证)"]
    },
    "OUTDOOR": {
        "name": "户外庭院、排水沟与景观构件 (Outdoor & Drainage)",
        "positions": ["Trench Drain (车道/泳池线性排水沟)", "Gutter Guard (屋檐排水天沟防落叶网)", "Post Anchor (木露台立柱固定底座)", "Outdoor Vent (外墙防风雨冲压罩)"],
        "materials": ["Polymer/HDPE (耐暴晒重型塑料)", "Hot-Dip Galvanized (镀锌重钢格栅)", "Ductile Cast Iron (球墨铸铁重载盖板)", "Cast Aluminum (耐候防腐铸铝)"],
        "finishes": ["Black Asphalt (沥青防腐黑)", "Galvanized Silver (热镀锌亮银)", "Natural Gray (水泥工程灰)"],
        "sizes": ["39 inch / 1 Meter (标准单段沟长)", "5-6 inch (全美标准屋檐天沟网)", "4x4 inch (木方柱底座)", "6x6 inch (重载立柱底座)"],
        "compliance": ["EN 1433 / ANSI A112.6.3 (A15行人 ~ C250车辆承重等级)", "ASTM A123 (热浸镀锌耐盐雾防腐)", "ASTM G154 (户外高强度抗紫外线黄变脆化测试)"]
    }
}

# ==============================================================================
# 5. 主页面布局与交互控制器
# ==============================================================================
st.markdown('<div class="main-title">🏬 北美大零售全品类与气候销售决策系统 (Grand Unified Pro)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">完整涵盖【50州地基结构 + 8大气候物理(HDD/CDD/冻土/硬水/盐蚀) + 房龄分布 + Big 3 门店网络 + 买手财务测算 + 法务避坑雷达】</div>', unsafe_allow_html=True)

col_cat, col_season, col_channel = st.columns([1.3, 1.1, 1.1])
with col_cat:
    selected_cat_key = st.selectbox("1. 目标产品大类 (Category)：", list(CATEGORY_CONFIG.keys()), format_func=lambda x: CATEGORY_CONFIG[x]["name"])
    cat_cfg = CATEGORY_CONFIG[selected_cat_key]

with col_season:
    selected_season = st.selectbox("2. 规划出货节令 (Seasonality Pulse)：", [
        "Q1 春季复苏与翻新热潮 (Spring Refresh: 3-5月)",
        "Q2 夏季空调制冷高峰 (Peak Cooling: 6-8月)",
        "Q3 入冬防寒整备爆发季 (Fall Weatherization: 9-11月)",
        "Q4 深冬极寒与防冻抢修 (Freeze Defense: 12-2月)",
        "全年平销基准期 (Annual Baseline)"
    ], index=2)

with col_channel:
    selected_channel = st.selectbox("3. 目标商超零售渠道：", [
        "全部渠道综合总盘 (THD + Lowe's + Menards)",
        "The Home Depot (承包商Pro工匠第一)",
        "Lowe's (家庭DIY与软装换新偏好)",
        "Menards (中西部大区独立专营)"
    ], index=0)

# 四维工程属性联动面板
st.markdown("#### 🎯 产品四维工程属性选择")
f1, f2, f3, f4 = st.columns(4)
with f1:
    sel_pos = st.selectbox("1. 安装位置 (Position)：", cat_cfg["positions"]).split(" ")[0]
with f2:
    sel_mat = st.selectbox("2. 生产原材料 (Material)：", cat_cfg["materials"]).split(" ")[0]
with f3:
    sel_fin = st.selectbox("3. 表面工艺/颜色 (Finish)：", cat_cfg["finishes"]).split(" ")[0]
with f4:
    sel_size = st.selectbox("4. 规格尺寸 (Size)：", cat_cfg["sizes"]).split(" ")[0]

# ==============================================================================
# 6. 全维多属性与物理气候计算引擎（含完整中文动态归因生成）
# ==============================================================================
calc_rows = []

for abbr, s in STATES_DATA.items():
    base_v = s["base_vel"]
    weight = 1.0
    reasons = []
    
    # 1. 地基形态与安装位置联动（核心因果）
    if selected_cat_key == "HVAC":
        if sel_pos == "Floor":
            if "地下室" in s["foundation"] or "架空" in s["foundation"]:
                weight *= 1.25
                reasons.append("全地下室/架空层主场，热风向上升对流刚需")
            elif "平板" in s["foundation"] or abbr in ["FL", "TX", "AZ", "NV", "HI", "LA"]:
                weight *= 0.12
                reasons.append("实心水泥大平板地基，地面无管道开孔，严禁铺地板款")
        elif sel_pos == "Ceiling":
            if s["cdd"] >= 2000 or abbr in ["FL", "TX", "AZ", "NV", "CA", "GA", "HI"]:
                weight *= 2.6
                reasons.append(f"长夏酷暑阳光带(CDD={s['cdd']:,})，冷气天花板下吹是全美标准")
            elif s["hdd"] >= 6000:
                weight *= 0.5
                reasons.append("极寒雪带一层以地面采暖为主，天花风口占比低")
        elif sel_pos == "Baseboard":
            if s["house_age"] >= 50 or abbr in ["PA", "NY", "MA", "CT", "OH", "NJ"]:
                weight *= 1.9
                reasons.append("高龄老宅水暖踢脚线与狭窄缝隙换新改装密集")

    elif selected_cat_key == "PLUMBING":
        if "Linear" in sel_pos or "Floor" in sel_pos:
            if abbr in ["FL", "CA", "TX", "NC", "SC", "GA", "AZ"]:
                weight *= 2.0
                reasons.append("现代无门槛大板淋浴房(Curbless Walk-in)改装爆发区")
        elif "Frost" in sel_pos:
            if s["frost_depth"] >= 36:
                weight *= 3.2
                reasons.append(f"冻土层深达 {s['frost_depth']} 英寸，防冻长水阀是防爆管建筑规范硬性要求")
            elif s["frost_depth"] == 0:
                weight *= 0.05
                reasons.append("常年无霜冻，室外防冻阀几乎零需求")

    elif selected_cat_key == "FLOORING":
        if "Tile" in sel_pos:
            if "瓷砖" in s["flooring"] or abbr in ["FL", "TX", "AZ", "CA", "NV"]:
                weight *= 2.5
                reasons.append("大面积通铺大理石/瓷砖，金属收边防崩角刚需")
        elif "T-Molding" in sel_pos or "Reducer" in sel_pos:
            if "实木" in s["flooring"]:
                weight *= 1.8
                reasons.append("实木地板与LVP木纹板主力存量区，房间交界压条标配")

    elif selected_cat_key == "DOORS":
        if "Sweep" in sel_pos or "Weatherstripping" in sel_pos:
            if s["hdd"] >= 5500:
                weight *= 2.3
                reasons.append("北方寒冬穿堂狂风剧烈，门底气密条是降采暖电费首选")
        elif "Hurricane" in sel_pos:
            if abbr in ["FL", "NC", "SC", "TX", "LA", "HI"]:
                weight *= 3.5
                reasons.append("沿海大西洋飓风带(HVHZ法规)强制要求高强度防风角码")

    elif selected_cat_key == "OUTDOOR":
        if "Trench" in sel_pos:
            if s["cdd"] >= 1800 or "暴雨" in s["hazard"] or "飓风" in s["hazard"]:
                weight *= 2.4
                reasons.append("强降雨量、多泳池及雨林环境，车道防倒灌依赖深沟")
        elif "Gutter" in sel_pos:
            if abbr in ["NC", "GA", "TN", "VA", "PA", "OH", "MI", "OR", "WA"]:
                weight *= 2.1
                reasons.append("森林树冠茂密，秋季落叶防堵塞天沟大面积换装")

    # 2. 融雪盐与水硬度物理微调
    if s["salt_risk"] in ["高", "极高"]:
        if sel_mat in ["Steel"]:
            weight *= 0.8
            reasons.append("⚠️ 融雪盐鞋底腐蚀严重，普通碳钢有生锈索赔隐患")
        elif sel_mat in ["Aluminum", "Stainless"]:
            weight *= 1.25
            reasons.append("✅ 阳极氧化铝/不锈钢耐融雪盐侵蚀，当地口碑偏好")

    if s["water_hardness"] >= 13.0 and selected_cat_key == "PLUMBING":
        if sel_fin == "CP":
            weight *= 0.85
            reasons.append("⚠️ 极重度硬水，亮铬表面极易留顽固白斑水垢")
        elif sel_fin in ["BN", "MB"]:
            weight *= 1.25
            reasons.append("✅ 拉丝镍/哑光黑在硬水区抗水垢视觉残留表现优异")

    # 3. 房龄加权（老房集中修缮）
    if s["house_age"] >= 50:
        weight *= 1.2
        reasons.append(f"中位房龄达 {s['house_age']} 年，老旧建筑二次换新动销活跃")

    # 4. 季节节令脉冲加权
    if "Q3" in selected_season:
        if selected_cat_key == "DOORS" and ("Sweep" in sel_pos or "Weatherstripping" in sel_pos):
            weight *= 1.6
            reasons.append("🍂 处于入冬防寒整备季（Fall Weatherization），销量脉冲式激增")
        elif selected_cat_key == "OUTDOOR" and "Gutter" in sel_pos:
            weight *= 1.8
            reasons.append("🍂 秋季落叶高峰期，天沟滤网迎来全美年度最高峰出货")
    elif "Q2" in selected_season:
        if selected_cat_key == "HVAC" and sel_pos == "Ceiling":
            weight *= 1.7
            reasons.append("☀️ 酷暑制冷峰值，天花散流器换新需求强劲")
    elif "Q4" in selected_season:
        if selected_cat_key == "PLUMBING" and "Frost" in sel_pos:
            weight *= 2.2
            reasons.append("❄️ 极寒深度冰封，爆管抢修更换进入最高峰")
    elif "Q1" in selected_season:
        if selected_cat_key in ["FLOORING", "PLUMBING"]:
            weight *= 1.3
            reasons.append("🌱 美国春季退税到账（Tax Refund），室内翻修小阳春")

    # 5. 尺寸超级通货加权
    if sel_size in ["04X10", "36", "4x4", "39"]:
        weight *= 1.15

    # 计算有效门店数
    if "Home Depot" in selected_channel:
        active_stores = s["thd"]
    elif "Lowe's" in selected_channel:
        active_stores = s["lowes"]
    elif "Menards" in selected_channel:
        active_stores = s["menards"]
    else:
        active_stores = s["total_stores"]

    calc_vel = max(round(base_v * weight, 1), 3.0)
    calc_tot = int(calc_vel * active_stores)
    
    # 货架排面建议
    pog = "🔥 双排面 (Double, 24寸)" if calc_vel >= 35.0 else ("✅ 单排面 (Single, 12寸)" if calc_vel >= 15.0 else "⚠️ 底层冷门位")

    row_data = dict(s)
    row_data["abbr"] = abbr
    row_data["calc_vel"] = calc_vel
    row_data["calc_tot"] = calc_tot
    row_data["active_stores"] = active_stores
    row_data["pog"] = pog
    row_data["calc_rev_msrp"] = calc_tot * retail_msrp
    row_data["calc_fob_tot"] = calc_tot * fob_cost
    row_data["reason_desc"] = "；".join(reasons) if reasons else "符合常规分销基线"
    calc_rows.append(row_data)

df_res = pd.DataFrame(calc_rows)
df_res["rank_vel"] = df_res["calc_vel"].rank(ascending=False, method="min").astype(int)
df_res["rank_tot"] = df_res["calc_tot"].rank(ascending=False, method="min").astype(int)

# ==============================================================================
# 7. 全网大卡片看板 (KPI Dashboard)
# ==============================================================================
st.markdown("---")
sum_stores = int(df_res["active_stores"].sum())
sum_units = int(df_res["calc_tot"].sum())
sum_rev = df_res["calc_rev_msrp"].sum()
top_v_row = df_res.sort_values("calc_vel", ascending=False).iloc[0]
top_t_row = df_res.sort_values("calc_tot", ascending=False).iloc[0]

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">分析渠道有效总门店</div>
        <div class="kpi-val">{sum_stores:,} 家</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">该节令·月总出货预估</div>
        <div class="kpi-val">{sum_units:,} 件</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">单店流速冠军 (平效之王)</div>
        <div class="kpi-val">{top_v_row['cn']} ({top_v_row['calc_vel']:.1f} 件/店)</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">渠道总吞吐量霸主 (排产核心)</div>
        <div class="kpi-val">{top_t_row['cn']} ({top_t_row['calc_tot']:,} 件)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 8. 核心呈现：四大 Tab 分页（排行大表、单州深度下钻、渠道图表、供应链分仓）
# ==============================================================================
tab_rank, tab_detail, tab_chart, tab_supply = st.tabs([
    "📋 全美 50 州零售排行主看板", 
    "🔍 州级商业归因与物理法务透视", 
    "📊 Big 3 零售巨头渠道吞吐量图表", 
    "🚚 供应链 RDC 分仓、港口与包装规范"
])

# ----------------- TAB 1: 50 州排行榜 -----------------
with tab_rank:
    view_mode = st.radio(
        "切换主排序依据：", 
        ["全州渠道总吞吐量 (件/月) - 工厂备货与海运整柜排产", "单店平均销售流速 (件/店/月) - 商超选品平效与货架位谈判"], 
        horizontal=True
    )
    sort_key = "rank_tot" if "吞吐量" in view_mode else "rank_vel"
    df_sorted = df_res.sort_values(sort_key, ascending=True).reset_index(drop=True)
    df_sorted["序号"] = df_sorted.index + 1
    
    max_vel_val = max(int(df_res["calc_vel"].max()), 1)
    
    st.dataframe(
        df_sorted[[
            "序号", "abbr", "cn", "region", "calc_vel", "calc_tot", "calc_rev_msrp",
            "active_stores", "house_age", "pog", "foundation"
        ]],
        use_container_width=True,
        column_config={
            "序号": st.column_config.NumberColumn(width=45),
            "abbr": st.column_config.TextColumn("简称", width=55),
            "cn": st.column_config.TextColumn("州全称", width=95),
            "region": st.column_config.TextColumn("大区", width=80),
            "calc_vel": st.column_config.ProgressColumn("单店流速(件/店)", min_value=0, max_value=max_vel_val, format="%.1f"),
            "calc_tot": st.column_config.NumberColumn("月总盘(件)", format="%d"),
            "calc_rev_msrp": st.column_config.NumberColumn("月零售流水($)", format="$%d"),
            "active_stores": st.column_config.NumberColumn("有效门店", width=70),
            "house_age": st.column_config.NumberColumn("房龄", format="%d年", width=65),
            "pog": st.column_config.TextColumn("POG货架排面建议", width=140),
            "foundation": st.column_config.TextColumn("典型地基基底", width=160)
        },
        height=540,
        hide_index=True
    )

# ----------------- TAB 2: 单州深度透视 -----------------
with tab_detail:
    st.markdown("### 🔎 目标州商业基底、物理气象与法务避坑雷达")
    target_abbr = st.selectbox("请选择要深度穿透剖析的目标州：", df_sorted["abbr"].tolist(), index=0)
    cur = df_sorted[df_sorted["abbr"] == target_abbr].iloc[0]
    
    c_info1, c_info2 = st.columns([1.1, 1.1])
    
    with c_info1:
        st.markdown(f"### 📍 {cur['cn']} ({cur['abbr']}) · {cur['region']}")
        m_a, m_b = st.columns(2)
        with m_a:
            st.metric("预估单店流速", f"{cur['calc_vel']:.1f} 件/店/月", f"全美单店排名: #{cur['rank_vel']}")
        with m_b:
            st.metric("该州月总需求", f"{cur['calc_tot']:,} 件/月", f"全美总盘排名: #{cur['rank_tot']}")
            
        st.info(f"**💡 算法与气候地基综合归因**：\n{cur['reason_desc']}")
        st.write(f"**🏠 房屋基底形态**：{cur['foundation']}")
        st.write(f"**🪵 地面材质偏好**：{cur['flooring']}")
        st.write(f"**🏬 区域门店网络**：THD: **{cur['thd']}** 家 | Lowe's: **{cur['lowes']}** 家 | Menards: **{cur['menards']}** 家 (有效覆盖: {cur['active_stores']} 家)")
        st.write(f"**📦 POG 货架位策略**：**{cur['pog']}**")
        st.success(f"**✅ 当地常规主推品**：{cur['best']}")
        st.warning(f"**⚠️ 当地谨慎进入品**：{cur['avoid']}")

    with c_info2:
        st.markdown(f"""
        <div class="physics-card">
            <b>🌡️ 气候物理实测与建筑物理参数</b><br>
            • 采暖度日 (HDD): <b>{cur['hdd']:,}</b> | 制冷度日 (CDD): <b>{cur['cdd']:,}</b><br>
            • 房屋中位房龄: <b>{cur['house_age']} 年</b> {'(⚠️ 50年以上老宅区，老规格翻新是绝对主力)' if cur['house_age']>=50 else ''}<br>
            • 法定冻土深度: <b>{cur['frost_depth']} 英寸</b> {'(⚠️ 极深冻土，严禁推短水阀)' if cur['frost_depth']>=36 else ''}<br>
            • 水质硬度: <b>{cur['water_hardness']} GPG</b> {'(⚠️ 极重度硬水，亮铬易留顽固白斑)' if cur['water_hardness']>=13 else ''}<br>
            • 融雪盐腐蚀风险: <b>{cur['salt_risk']}</b> {'(⚠️ 严禁冷轧碳钢裸露)' if cur['salt_risk'] in ['高','极高'] else ''}<br>
            • 极端自然灾害标签: <span class="badge-warning">{cur['hazard']} (灾害指数: {cur['hazard_idx']}/10)</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 法律红线与强制准入
        redlines = []
        if target_abbr == "CA":
            redlines.append("加州 Proposition 65（65号提案）：含微量铅必须附带致癌黄标警告，否则面临赏金律师高额索赔。")
            redlines.append("加州 Title 24 & WUI 规范：通风口必须内衬 1/8 英寸耐腐蚀防飞烬不锈钢网。")
        if target_abbr in ["FL", "NC", "SC", "TX", "LA", "HI"] and selected_cat_key in ["DOORS", "OUTDOOR"]:
            redlines.append("佛罗里达/沿海 HVHZ 飓风认证：门窗构件与户外固定件必须通过 Miami-Dade NOA 强风压抗飞弹冲击测试。")
        if cur["frost_depth"] >= 36 and selected_cat_key == "PLUMBING" and "Frost" in sel_pos:
            redlines.append(f"IPC 县级水暖规范：当地冻土层深达 {cur['frost_depth']} 寸，商超采购只接受 8~12 英寸以上超长杆防冻水阀！")
        if selected_cat_key == "FLOORING":
            redlines.append("联邦 ADA 残疾人无障碍法案：地面压条若落差超过 1/4 英寸（6.4mm），必须配备缓坡倒角（Beveled Edge）。")
        if selected_cat_key == "PLUMBING" and "Brass" in sel_mat:
            redlines.append("Safe Drinking Water Act / NSF 61：接触饮用水五金过水面含铅量必须严格加权低于 0.25%。")

        st.markdown('<div class="radar-box">', unsafe_allow_html=True)
        st.markdown("**🛡️ 美国法务准入与县级建筑规范红线 (Legal Radar)：**")
        if redlines:
            for rl in redlines:
                st.markdown(f"- 🔴 <span style='font-size:0.85rem;color:#991b1b;'>{rl}</span>", unsafe_allow_html=True)
        else:
            st.markdown("- 🟢 <span style='font-size:0.85rem;color:#166534;'>符合全美常规 ASTM / ANSI 准入标准，无特殊极端地方禁令。</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 3: 零售巨头渠道图表 -----------------
with tab_chart:
    st.markdown("#### 📊 全美 Top 15 吞吐量大州 Big 3 零售渠道出货结构")
    st.caption("注：The Home Depot 偏向工程 Pro 客户，Lowe's 偏向轻家装散客，Menards 在中西部农业大湖区统治力惊人。")
    
    top15 = df_res.sort_values("calc_tot", ascending=False).head(15)
    chart_df = pd.DataFrame({
        "州": top15["cn"],
        "THD (家得宝)": top15["calc_vel"] * top15["thd"],
        "Lowe's (劳氏)": top15["calc_vel"] * top15["lowes"],
        "Menards (美纳斯)": top15["calc_vel"] * top15["menards"]
    }).set_index("州")
    
    st.bar_chart(chart_df, height=380)

# ----------------- TAB 4: 供应链、港口与打托规范 -----------------
with tab_supply:
    st.markdown("#### 🚚 大零售供应链 RDC 分仓配比、海运港口与包装规范")
    
    s_col1, s_col2 = st.columns([1.1, 1.3])
    
    with s_col1:
        st.markdown("##### 1. 区域配送中心 (RDC) 备货权重")
        reg_summary = df_res.groupby("region").agg({
            "abbr": "count", "active_stores": "sum", "calc_tot": "sum", "calc_vel": "mean"
        }).reset_index()
        reg_summary.columns = ["大区", "州数", "总门店", "月度总盘(件)", "区均流速"]
        reg_summary["建议配货比例"] = (reg_summary["月度总盘(件)"] / reg_summary["月度总盘(件)"].sum() * 100).round(1).astype(str) + "%"
        reg_summary["区均流速"] = reg_summary["区均流速"].round(1)
        st.dataframe(reg_summary, use_container_width=True, hide_index=True)
        
    with s_col2:
        st.markdown("##### 2. 客群画像与 GMA 打托包装建议")
        
        # 动态客群画像判定
        if "Cast" in sel_mat or "Stainless 316" in sel_mat or "Hurricane" in sel_pos:
            diy_p, pro_p = 25, 75
            pkg_rec = "Contractor Pack (10-20件无印刷牛皮纸工程包装)"
            ret_rate = "1.5% ~ 2.5% (极低退货率)"
        elif "Plastic" in sel_mat or "WH" in sel_fin:
            diy_p, pro_p = 75, 25
            pkg_rec = "彩色挂卡 / 气泡热缩膜 (配安装螺丝与 1:1 测量卡纸)"
            ret_rate = "4.5% ~ 6.5% (中高退货率)"
        else:
            diy_p, pro_p = 50, 50
            pkg_rec = "零售标准彩盒包装"
            ret_rate = "3.0% ~ 4.0% (常规)"
            
        pa, pb, pc = st.columns(3)
        with pa:
            st.metric("DIY 散客占比", f"{diy_p}%")
        with pb:
            st.metric("Pro 工匠占比", f"{pro_p}%")
        with pc:
            st.metric("预估退货率", ret_rate)
            
        st.markdown(f"""
        <div class="physics-card">
            <b>📦 美标托盘 (GMA Pallet) 与包装标准：</b><br>
            • <b>推荐装箱数</b>: {case_pack} 件/箱<br>
            • <b>堆码规格 (TI/HI)</b>: 每层 6 箱 × 堆叠 8 层 = <b>48 箱/托</b><br>
            • <b>单托装载量</b>: <b>{case_pack * 48} 件/托盘</b> (含托盘高度控在 50 英寸以内)<br>
            • <b>外箱条码</b>: 必须打印扫描级 GS1-128 / ITF-14 箱唛，单品贴 UPC-A<br>
            • <b>包装防退策略</b>: <span style="color:#0369a1;">{pkg_rec}</span>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 9. 决策数据一键导出 CSV
# ==============================================================================
st.markdown("---")
csv_out = df_sorted[[
    "序号", "abbr", "cn", "name", "region", "calc_vel", "calc_tot", "calc_rev_msrp",
    "calc_fob_tot", "active_stores", "pog", "foundation", "flooring", "best", "avoid",
    "hdd", "cdd", "frost_depth", "water_hardness", "salt_risk", "house_age", "hazard", "reason_desc"
]].to_csv(index=False).encode('utf-8-sig')

st.download_button(
    label=f"📥 导出【{cat_cfg['name'].split(' ')[0]}】全美 50 州完整商业与物理决策模型报表 (.csv)",
    data=csv_out,
    file_name=f"NA_Retail_Master_Decision_{selected_cat_key}.csv",
    mime="text/csv"
)
