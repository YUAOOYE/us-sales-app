import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. 页面配置与企业级专业 CSS 注入
# ==========================================
st.set_page_config(
    page_title="北美大零售全品类与气候销售决策系统 (Commercial & Engineering Pro)",
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
    .badge-diy {
        background-color: #dbeafe;
        color: #1e40af;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .badge-pro {
        background-color: #fef3c7;
        color: #92400e;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .badge-warning {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .badge-success {
        background-color: #dcfce7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 侧边栏：工程物理学标准库与商超财务试算
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shop.png", width=64)
    st.title("商超工程决策系统")
    st.caption("North American Retail & Climate Intelligence v4.0 Pro")
    st.markdown("---")
    
    st.markdown("### 💰 商超买手财务与毛利试算器")
    st.caption("模拟 Home Depot / Lowe's 买手审查时的单店流水与毛利标准：")
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
    
    st.caption(f"• 单件商超毛利额: **${gross_profit_per_unit:.2f}** | 单箱货值(FOB): **${fob_cost * case_pack:.2f}**")
    st.markdown("---")

    st.markdown("### 📚 北美工程物理与零售实战准则")
    with st.expander("1. ASHRAE 暖通与度日基准", expanded=False):
        st.markdown("""
        * **HDD (采暖度日)**：基准 65°F (18.3°C)。HDD > 5000 区域严寒，采暖风口与地暖长期全开，防结露要求极高。
        * **CDD (制冷度日)**：基准 65°F。CDD > 2000 属于酷热高湿，空调高频制冷，风口凝露发霉为头号客诉源。
        """)
    with st.expander("2. Frost Line 冻土深度与给排水", expanded=False):
        st.markdown("""
        * 北方各州冻土层深达 36~60 英寸，室外水管必须埋在冻土层以下。
        * 户外龙头必须具备 **长水阀 (Frost-Free Sillcock)** 防冻防裂结构。
        """)
    with st.expander("3. De-icing Salt 融雪盐与材质防腐", expanded=False):
        st.markdown("""
        * 降雪带冬季撒布巨量 NaCl / CaCl2 融雪盐。
        * 融雪水携带盐分附着于室内门厅，铸铁/普通碳钢会快速锈穿。
        * 必须采用 **阳极氧化铝 (Anodized 6063)**、**304/316 不锈钢** 或 **重防腐粉末喷涂**。
        """)
    with st.expander("4. California WUI 山火防飞烬规范", expanded=False):
        st.markdown("""
        * 加州 WUI (Wildland-Urban Interface) 规范强制要求：
        * 阁楼及爬行空间通风口必须具备 **1/8 英寸耐高温防飞烬金属网**，严禁使用易熔化塑料格栅。
        """)
    with st.expander("5. 托盘打托与物流包装规范 (TI/HI)", expanded=False):
        st.markdown("""
        * **GMA 标准木托盘**：48 × 40 英寸，四向进叉。
        * **限高与限重**：含托盘高度不得超过 52 英寸，整托重量不超过 2,000 磅。
        * **条码体系**：外箱必须打印 GS1-128 / ITF-14 箱唛，单品必须带扫描级 UPC-A。
        """)
    with st.expander("6. 💡 新增：POG 货架排面与 Facings 机制", expanded=False):
        st.markdown("""
        * **Planogram (POG)**：商超货架陈列图。每个 SKU 占用的货架横向宽度称为 **Facing**。
        * 单店月流速 > 15 件通常可争取 **Double Facings (双排面)**，视觉曝光翻倍；月流速 < 5 件会面临被降为下层冷门位甚至清仓下架（Discontinued）。
        """)
    with st.expander("7. 💡 新增：Defective Allowance 残损扣款", expanded=False):
        st.markdown("""
        * 美国家装大零售商合同中，常规会直接在发票中扣除 **2% ~ 4%** 作为残损与无理由退货备用金（Defective Allowance）。
        * 供应商在报价 FOB 时必须将这部分隐性扣款打入成本核算中。
        """)

# ==========================================
# 3. 核心数据库：全美 50 州工程物理、房龄与零售全景
# ==========================================
STATES_DATA = {
    "AL": {"name": "Alabama", "region": "美东南", "thd": 29, "lowes": 34, "menards": 0, "dc": "亚特兰大", "hdd": 2600, "cdd": 1900, "frost_depth": 5, "water_hardness": 4.5, "salt_risk": "低", "hazard": "龙卷风/高湿", "house_age": 36, "hazard_idx": 4},
    "AK": {"name": "Alaska", "region": "美西北", "thd": 7, "lowes": 5, "menards": 0, "dc": "西雅图外港", "hdd": 10500, "cdd": 0, "frost_depth": 72, "water_hardness": 6.0, "salt_risk": "中", "hazard": "极寒永冻", "house_age": 42, "hazard_idx": 8},
    "AZ": {"name": "Arizona", "region": "美西南", "thd": 58, "lowes": 33, "menards": 0, "dc": "凤凰城", "hdd": 1200, "cdd": 3500, "frost_depth": 0, "water_hardness": 16.5, "salt_risk": "极低", "hazard": "极端沙漠高温/硬水", "house_age": 30, "hazard_idx": 3},
    "AR": {"name": "Arkansas", "region": "美南", "thd": 15, "lowes": 20, "menards": 0, "dc": "孟菲斯", "hdd": 3200, "cdd": 1700, "frost_depth": 10, "water_hardness": 5.0, "salt_risk": "低", "hazard": "雷暴/龙卷风", "house_age": 39, "hazard_idx": 4},
    "CA": {"name": "California", "region": "美西", "thd": 234, "lowes": 112, "menards": 0, "dc": "洛杉矶/安大略", "hdd": 2100, "cdd": 1300, "frost_depth": 0, "water_hardness": 9.5, "salt_risk": "极低", "hazard": "WUI山火/地震", "house_age": 48, "hazard_idx": 7},
    "CO": {"name": "Colorado", "region": "山地大区", "thd": 47, "lowes": 28, "menards": 0, "dc": "丹佛", "hdd": 6200, "cdd": 600, "frost_depth": 36, "water_hardness": 7.5, "salt_risk": "高", "hazard": "高海拔紫外线/冻融循环", "house_age": 38, "hazard_idx": 5},
    "CT": {"name": "Connecticut", "region": "美东北", "thd": 30, "lowes": 16, "menards": 0, "dc": "纽瓦克/波士顿", "hdd": 5800, "cdd": 750, "frost_depth": 42, "water_hardness": 4.0, "salt_risk": "极高", "hazard": "老旧管道/融雪盐腐蚀", "house_age": 59, "hazard_idx": 6},
    "DE": {"name": "Delaware", "region": "美东", "thd": 9, "lowes": 6, "menards": 0, "dc": "费城", "hdd": 4600, "cdd": 1200, "frost_depth": 24, "water_hardness": 5.5, "salt_risk": "高", "hazard": "沿海盐雾", "house_age": 41, "hazard_idx": 4},
    "FL": {"name": "Florida", "region": "美东南", "thd": 155, "lowes": 110, "menards": 0, "dc": "奥兰多/迈阿密", "hdd": 500, "cdd": 3800, "frost_depth": 0, "water_hardness": 14.0, "salt_risk": "极低", "hazard": "HVHZ五级飓风/高湿凝露", "house_age": 34, "hazard_idx": 9},
    "GA": {"name": "Georgia", "region": "美东南", "thd": 91, "lowes": 65, "menards": 0, "dc": "亚特兰大", "hdd": 2700, "cdd": 1850, "frost_depth": 5, "water_hardness": 3.5, "salt_risk": "低", "hazard": "高湿热/暴雨", "house_age": 31, "hazard_idx": 5},
    "HI": {"name": "Hawaii", "region": "美西", "thd": 7, "lowes": 4, "menards": 0, "dc": "火奴鲁鲁", "hdd": 0, "cdd": 4200, "frost_depth": 0, "water_hardness": 3.0, "salt_risk": "低", "hazard": "极高海风盐雾腐蚀", "house_age": 47, "hazard_idx": 6},
    "ID": {"name": "Idaho", "region": "美西北", "thd": 13, "lowes": 8, "menards": 0, "dc": "盐湖城", "hdd": 6800, "cdd": 550, "frost_depth": 36, "water_hardness": 8.0, "salt_risk": "高", "hazard": "寒冬冻融", "house_age": 33, "hazard_idx": 4},
    "IL": {"name": "Illinois", "region": "美中", "thd": 81, "lowes": 43, "menards": 61, "dc": "芝加哥", "hdd": 6100, "cdd": 900, "frost_depth": 42, "water_hardness": 14.5, "salt_risk": "极高", "hazard": "极端暴雪/融雪盐腐蚀", "house_age": 56, "hazard_idx": 7},
    "IN": {"name": "Indiana", "region": "美中", "thd": 41, "lowes": 42, "menards": 39, "dc": "印第安纳波利斯", "hdd": 5500, "cdd": 1000, "frost_depth": 36, "water_hardness": 17.0, "salt_risk": "极高", "hazard": "重度硬水结垢/暴雪", "house_age": 48, "hazard_idx": 6},
    "IA": {"name": "Iowa", "region": "美中", "thd": 16, "lowes": 15, "menards": 22, "dc": "得梅因", "hdd": 6700, "cdd": 850, "frost_depth": 48, "water_hardness": 16.0, "salt_risk": "极高", "hazard": "深度冻土/强融雪盐", "house_age": 54, "hazard_idx": 6},
    "KS": {"name": "Kansas", "region": "美中", "thd": 18, "lowes": 14, "menards": 9, "dc": "堪萨斯城", "hdd": 5000, "cdd": 1350, "frost_depth": 30, "water_hardness": 13.5, "salt_risk": "高", "hazard": "大温差/龙卷风走廊", "house_age": 47, "hazard_idx": 5},
    "KY": {"name": "Kentucky", "region": "美南", "thd": 27, "lowes": 38, "menards": 9, "dc": "路易斯维尔", "hdd": 4400, "cdd": 1250, "frost_depth": 20, "water_hardness": 10.5, "salt_risk": "高", "hazard": "冻融交替", "house_age": 43, "hazard_idx": 4},
    "LA": {"name": "Louisiana", "region": "美南", "thd": 28, "lowes": 30, "menards": 0, "dc": "新奥尔良/休斯敦", "hdd": 1600, "cdd": 2600, "frost_depth": 0, "water_hardness": 4.5, "salt_risk": "极低", "hazard": "沿海飓风/极高湿度凝露", "house_age": 41, "hazard_idx": 8},
    "ME": {"name": "Maine", "region": "美东北", "thd": 11, "lowes": 10, "menards": 0, "dc": "波士顿", "hdd": 7800, "cdd": 300, "frost_depth": 54, "water_hardness": 3.0, "salt_risk": "极高", "hazard": "漫长严冬/海岸海风腐蚀", "house_age": 53, "hazard_idx": 6},
    "MD": {"name": "Maryland", "region": "美东", "thd": 43, "lowes": 30, "menards": 0, "dc": "巴尔的摩", "hdd": 4500, "cdd": 1300, "frost_depth": 24, "water_hardness": 6.5, "salt_risk": "高", "hazard": "沿海盐雾/老城区改建", "house_age": 46, "hazard_idx": 4},
    "MA": {"name": "Massachusetts", "region": "美东北", "thd": 45, "lowes": 29, "menards": 0, "dc": "波士顿", "hdd": 5900, "cdd": 700, "frost_depth": 48, "water_hardness": 3.5, "salt_risk": "极高", "hazard": "东北风暴/超长供暖结露", "house_age": 60, "hazard_idx": 6},
    "MI": {"name": "Michigan", "region": "美中", "thd": 70, "lowes": 43, "menards": 44, "dc": "底特律", "hdd": 6800, "cdd": 650, "frost_depth": 48, "water_hardness": 12.0, "salt_risk": "极高", "hazard": "大湖效应大暴雪/融雪盐", "house_age": 52, "hazard_idx": 7},
    "MN": {"name": "Minnesota", "region": "美中", "thd": 35, "lowes": 12, "menards": 38, "dc": "明尼阿波利斯", "hdd": 8500, "cdd": 550, "frost_depth": 60, "water_hardness": 14.0, "salt_risk": "极高", "hazard": "极地涡旋极寒/超深冻土", "house_age": 46, "hazard_idx": 8},
    "MS": {"name": "Mississippi", "region": "美南", "thd": 16, "lowes": 22, "menards": 0, "dc": "孟菲斯", "hdd": 2300, "cdd": 2100, "frost_depth": 0, "water_hardness": 3.5, "salt_risk": "极低", "hazard": "极度潮湿发霉", "house_age": 39, "hazard_idx": 5},
    "MO": {"name": "Missouri", "region": "美中", "thd": 39, "lowes": 33, "menards": 19, "dc": "圣路易斯", "hdd": 4800, "cdd": 1400, "frost_depth": 28, "water_hardness": 11.0, "salt_risk": "高", "hazard": "冻融交替/暴风雨", "house_age": 47, "hazard_idx": 5},
    "MT": {"name": "Montana", "region": "美西北", "thd": 8, "lowes": 5, "menards": 0, "dc": "盐湖城", "hdd": 7900, "cdd": 400, "frost_depth": 54, "water_hardness": 9.0, "salt_risk": "高", "hazard": "高寒/深冻土破管", "house_age": 45, "hazard_idx": 6},
    "NE": {"name": "Nebraska", "region": "美中", "thd": 11, "lowes": 7, "menards": 10, "dc": "奥马哈", "hdd": 6200, "cdd": 950, "frost_depth": 42, "water_hardness": 13.5, "salt_risk": "极高", "hazard": "暴风雪/融雪盐冲刷", "house_age": 49, "hazard_idx": 6},
    "NV": {"name": "Nevada", "region": "美西", "thd": 21, "lowes": 17, "menards": 0, "dc": "拉斯维加斯/里诺", "hdd": 2800, "cdd": 2600, "frost_depth": 12, "water_hardness": 18.0, "salt_risk": "极低", "hazard": "极重度硬水结垢/昼夜温差", "house_age": 28, "hazard_idx": 3},
    "NH": {"name": "New Hampshire", "region": "美东北", "thd": 17, "lowes": 11, "menards": 0, "dc": "波士顿", "hdd": 7100, "cdd": 450, "frost_depth": 50, "water_hardness": 2.5, "salt_risk": "极高", "hazard": "深度冻土/强酸雪融盐", "house_age": 48, "hazard_idx": 6},
    "NJ": {"name": "New Jersey", "region": "美东北", "thd": 65, "lowes": 40, "menards": 0, "dc": "纽瓦克/费城", "hdd": 4900, "cdd": 1200, "frost_depth": 30, "water_hardness": 6.5, "salt_risk": "极高", "hazard": "密集融雪盐/海风盐雾", "house_age": 57, "hazard_idx": 6},
    "NM": {"name": "New Mexico", "region": "美西南", "thd": 17, "lowes": 13, "menards": 0, "dc": "阿尔伯克基", "hdd": 3800, "cdd": 1500, "frost_depth": 18, "water_hardness": 13.0, "salt_risk": "低", "hazard": "强紫外线脆化/硬水", "house_age": 36, "hazard_idx": 3},
    "NY": {"name": "New York", "region": "美东北", "thd": 100, "lowes": 68, "menards": 0, "dc": "纽约/纽瓦克/水牛城", "hdd": 5900, "cdd": 800, "frost_depth": 48, "water_hardness": 5.5, "salt_risk": "极高", "hazard": "水牛城湖效应暴雪/老房改建", "house_age": 62, "hazard_idx": 7},
    "NC": {"name": "North Carolina", "region": "美东南", "thd": 72, "lowes": 105, "menards": 0, "dc": "夏洛特(Lowe's总部)", "hdd": 3400, "cdd": 1600, "frost_depth": 12, "water_hardness": 3.0, "salt_risk": "中", "hazard": "湿热气候/沿海飓风", "house_age": 33, "hazard_idx": 5},
    "ND": {"name": "North Dakota", "region": "美中", "thd": 4, "lowes": 3, "menards": 8, "dc": "法戈", "hdd": 9400, "cdd": 450, "frost_depth": 66, "water_hardness": 13.0, "salt_risk": "极高", "hazard": "全美最深冻土/极寒脆断", "house_age": 45, "hazard_idx": 8},
    "OH": {"name": "Ohio", "region": "美中", "thd": 71, "lowes": 73, "menards": 34, "dc": "哥伦布", "hdd": 5600, "cdd": 850, "frost_depth": 36, "water_hardness": 15.0, "salt_risk": "极高", "hazard": "极重硬水/融雪盐高腐蚀", "house_age": 54, "hazard_idx": 7},
    "OK": {"name": "Oklahoma", "region": "美南", "thd": 21, "lowes": 24, "menards": 0, "dc": "达拉斯/俄城", "hdd": 3400, "cdd": 1900, "frost_depth": 15, "water_hardness": 11.5, "salt_risk": "中", "hazard": "高频冰雹/龙卷风", "house_age": 40, "hazard_idx": 5},
    "OR": {"name": "Oregon", "region": "美西北", "thd": 27, "lowes": 18, "menards": 0, "dc": "波特兰", "hdd": 4600, "cdd": 400, "frost_depth": 12, "water_hardness": 2.0, "salt_risk": "低", "hazard": "漫长阴雨潮湿/苔藓霉菌", "house_age": 43, "hazard_idx": 4},
    "PA": {"name": "Pennsylvania", "region": "美东", "thd": 73, "lowes": 83, "menards": 0, "dc": "阿伦敦/费城", "hdd": 5400, "cdd": 900, "frost_depth": 38, "water_hardness": 8.5, "salt_risk": "极高", "hazard": "阿巴拉契亚冻融/重度融雪盐", "house_age": 58, "hazard_idx": 7},
    "RI": {"name": "Rhode Island", "region": "美东北", "thd": 7, "lowes": 5, "menards": 0, "dc": "波士顿", "hdd": 5600, "cdd": 750, "frost_depth": 40, "water_hardness": 3.5, "salt_risk": "极高", "hazard": "海岸盐雾/融雪盐", "house_age": 60, "hazard_idx": 6},
    "SC": {"name": "South Carolina", "region": "美东南", "thd": 37, "lowes": 48, "menards": 0, "dc": "哥伦比亚/萨凡纳", "hdd": 2400, "cdd": 2000, "frost_depth": 5, "water_hardness": 3.0, "salt_risk": "低", "hazard": "强飓风潮湿/白蚁风险", "house_age": 31, "hazard_idx": 6},
    "SD": {"name": "South Dakota", "region": "美中", "thd": 3, "lowes": 3, "menards": 5, "dc": "苏瀑", "hdd": 7600, "cdd": 700, "frost_depth": 54, "water_hardness": 16.5, "salt_risk": "极高", "hazard": "深冻土/重融雪盐", "house_age": 47, "hazard_idx": 7},
    "TN": {"name": "Tennessee", "region": "美南", "thd": 44, "lowes": 58, "menards": 0, "dc": "孟菲斯/纳什维尔", "hdd": 3500, "cdd": 1650, "frost_depth": 12, "water_hardness": 6.5, "salt_risk": "中", "hazard": "冻融交替/暴风雨", "house_age": 37, "hazard_idx": 4},
    "TX": {"name": "Texas", "region": "美南核心", "thd": 182, "lowes": 145, "menards": 0, "dc": "达拉斯/休斯敦", "hdd": 1600, "cdd": 3000, "frost_depth": 5, "water_hardness": 12.5, "salt_risk": "低", "hazard": "极端超高温/突发寒潮极寒破管", "house_age": 31, "hazard_idx": 6},
    "UT": {"name": "Utah", "region": "山地大区", "thd": 24, "lowes": 14, "menards": 0, "dc": "盐湖城", "hdd": 5800, "cdd": 1050, "frost_depth": 30, "water_hardness": 17.5, "salt_risk": "高", "hazard": "重度硬水结垢/干热大温差", "house_age": 32, "hazard_idx": 4},
    "VT": {"name": "Vermont", "region": "美东北", "thd": 5, "lowes": 4, "menards": 0, "dc": "奥尔巴尼", "hdd": 7600, "cdd": 350, "frost_depth": 54, "water_hardness": 4.5, "salt_risk": "极高", "hazard": "漫长高寒/深度冻土", "house_age": 51, "hazard_idx": 6},
    "VA": {"name": "Virginia", "region": "美东", "thd": 50, "lowes": 61, "menards": 0, "dc": "里士满/诺福克", "hdd": 3900, "cdd": 1450, "frost_depth": 18, "water_hardness": 5.0, "salt_risk": "高", "hazard": "沿海湿润/冻融交替", "house_age": 42, "hazard_idx": 4},
    "WA": {"name": "Washington", "region": "美西北", "thd": 48, "lowes": 38, "menards": 0, "dc": "西雅图/塔科马", "hdd": 4900, "cdd": 300, "frost_depth": 18, "water_hardness": 2.5, "salt_risk": "低", "hazard": "超长阴雨高湿/室内发霉", "house_age": 43, "hazard_idx": 4},
    "WV": {"name": "West Virginia", "region": "美东", "thd": 10, "lowes": 17, "menards": 1, "dc": "查尔斯顿", "hdd": 5000, "cdd": 950, "frost_depth": 30, "water_hardness": 7.0, "salt_risk": "高", "hazard": "山地冻融/强雪蚀", "house_age": 52, "hazard_idx": 5},
    "WI": {"name": "Wisconsin", "region": "美中(Menards大本营)", "thd": 28, "lowes": 14, "menards": 45, "dc": "欧克莱尔(Menards总部)", "hdd": 7400, "cdd": 550, "frost_depth": 54, "water_hardness": 14.5, "salt_risk": "极高", "hazard": "重度暴雪/融雪盐极速锈蚀", "house_age": 51, "hazard_idx": 7},
    "WY": {"name": "Wyoming", "region": "山地大区", "thd": 5, "lowes": 3, "menards": 2, "dc": "夏延/丹佛", "hdd": 7500, "cdd": 350, "frost_depth": 50, "water_hardness": 11.0, "salt_risk": "高", "hazard": "极高海拔寒冷/大风沙", "house_age": 42, "hazard_idx": 5}
}

df_states = pd.DataFrame.from_dict(STATES_DATA, orient="index")
df_states["total_stores"] = df_states["thd"] + df_states["lowes"] + df_states["menards"]

# ==========================================
# 4. 品类与工程规范元数据
# ==========================================
CATEGORY_CONFIG = {
    "HVAC": {
        "name": "暖通出风口 (Registers & Grilles)",
        "subtypes": [
            "4x10 地板风口 (标准热卖)", "4x12 地板风口 (大流量)", "2x10 窄条地板风口", 
            "2x12 窄条地板风口", "6x10/6x12 侧墙/天花格栅", "14x8 回风滤网门 (Filter Grille)",
            "Baseboard 踢脚线风口 (重度采暖专用)", "WUI 阁楼防飞烬金属通风口"
        ],
        "materials": ["冲压镀锌钢板 (廉价基准)", "铝合金阳极氧化 (耐腐防冷凝)", "铸铝哑光粉末喷涂 (重载防踩)", "实木/橡木复合 (豪华地板对齐)", "工程塑料 (轻量抗露)"],
        "finishes": ["哑光黑 (Matte Black 现代主流)", "拉丝镍 (Brushed Nickel 经典)", "油磨青铜 (Oil Rubbed Bronze 复古)", "极简白 (Glossy White)", "原木未上漆 (Unfinished Oak)"],
        "base_vel": 32.0,
        "compliance": [
            "ASHRAE Standard 70 (风量 CFM 与噪音 NC 评级测试)",
            "UL 94 (塑料部件阻燃等级 V-0 / HB 标准)",
            "Heel-Proof 细高跟鞋安全规范 (格栅镂空缝隙必须 < 9.5 mm)",
            "踩踏承重负荷测试 (商超标准静态踩压需承受 > 300 lbs 无塑性变形)"
        ]
    },
    "PLUMBING": {
        "name": "卫浴水暖与排水 (Drains & Plumbing)",
        "subtypes": [
            "4x4 淋浴点状地漏 (不锈钢防臭)", "24/36英寸 线性长条隐形地漏", 
            "防冻长水阀 (Frost-Free Sillcock)", "铜压接球阀 (ProPress / PEX)", 
            "铸铁防臭重力地漏"
        ],
        "materials": ["304 不锈钢拉丝", "316 不锈钢 (高氯盐雾级)", "无铅锻压黄铜 (C69300)", "ABS / PVC 工程塑料"],
        "finishes": ["不锈钢拉丝 (Brushed SS)", "哑光黑 (Matte Black)", "抛光镀铬 (Polished Chrome)", "拉丝黄铜 (Brushed Brass)"],
        "base_vel": 24.0,
        "compliance": [
            "cUPC 认证 (IAPMO 强制排水与管件认证)",
            "ASME A112.18.2 / CSA B125.2 (地漏结构与排水通量测试)",
            "NSF/ANSI 61 & 372 (接触饮用水无铅涉水安全标准)"
        ]
    },
    "FLOORING": {
        "name": "地面收口与过渡件 (Transitions & Trim)",
        "subtypes": [
            "T-Molding T型同高过渡条", "Reducer 高低减速差过渡条", 
            "Stair Nose 楼梯踏步扣条", "End Cap / Threshold 门槛收边条", 
            "Quarter Round 踢脚线防尘圆弧收条"
        ],
        "materials": ["6063-T5 阳极氧化铝合金", "实木贴皮/橡木实木", "PVC / SPC 石塑同步挤出", "高耐磨铜质收边条"],
        "finishes": ["香槟金 (Anodized Champagne)", "磨砂哑黑 (Matte Black)", "古铜深灰 (Dark Bronze)", "拉丝银白 (Clear Anodized)"],
        "base_vel": 28.0,
        "compliance": [
            "ADA Section 303 (残疾人轮椅无障碍过渡斜率必须 ≤ 1:2，防绊倒)",
            "ASTM C1028 (表面防滑摩擦系数测试)",
            "抗冲击弯曲载荷测试 (手推车过槛抗凹陷强度)"
        ]
    },
    "DOORS": {
        "name": "建筑门窗五金与密封 (Door & Window Hardware)",
        "subtypes": [
            "重载阻尼室内合页 4x4 (3片装)", "商用级闭门器 (Grade 1 Heavy Duty)", 
            "门底自升降自动气密条 (Door Bottom Sweep)", "高耐磨铝合金外门槛 (Sill & Threshold)", 
            "HVHZ 沿海抗飓风加固合页锚栓"
        ],
        "materials": ["304 不锈钢", "锻压实心黄铜", "压铸铝合金", "热浸镀锌结构钢"],
        "finishes": ["磨砂黑 (Matte Black)", "缎面拉丝镍 (Satin Nickel)", "抛光铬 (Bright Chrome)", "PVD 强耐磨物理气相沉积涂层"],
        "base_vel": 20.0,
        "compliance": [
            "ANSI/BHMA A156.1 (合页承重与 100 万次开合疲劳测试)",
            "ASTM E1886 / E1996 (佛罗里达迈阿密戴德县 HVHZ 抗飞弹风暴测试)",
            "UL 10C (90分钟正压防火门五金认证)"
        ]
    },
    "OUTDOOR": {
        "name": "户外景观与排水设施 (Outdoor & Drainage)",
        "subtypes": [
            "庭院线性线性树脂混凝土排水槽", "绿地雨水收集渗水井井盖 (Catch Basin)", 
            "重载铸铁车道排水格栅 (Driveway Grate)", "隐藏式露台甲板落水扣件 (Deck Drainage)"
        ],
        "materials": ["球墨铸铁 (Ductile Iron Class C)", "热浸镀锌钢板 (Hot-dip Galv)", "高密度聚乙烯 (HDPE 结构塑料)", "316 海洋级不锈钢"],
        "finishes": ["沥青防腐浸漆 (Bitumen Black)", "天然热镀锌亮银", "原色工程黑 (UV Stabilized)"],
        "base_vel": 16.0,
        "compliance": [
            "EN 1433 / ANSI A112.6.3 (A15行人 ~ C250载重汽车承压荷载等级)",
            "ASTM A123 (高厚度热浸镀锌耐盐雾防腐标准)",
            "ASTM G154 (户外高强度抗紫外线黄变及脆化测试)"
        ]
    }
}

# 物流港口航线映射字典
PORT_LOGISTICS_MATRIX = {
    "美西": {
        "port": "洛杉矶 / 长滩港 (LA / Long Beach)",
        "transit_sea": "快船 14~16 天直达",
        "inland_mode": "港口提柜后当地卡车短驳至安大略/奇诺仓 (Ontario/Chino)",
        "freight_level": "海运运费最低，提还箱最快，但旺季洛杉矶港有拥堵费风险。"
    },
    "美西北": {
        "port": "西雅图 / 塔科马港 (Seattle / Tacoma)",
        "transit_sea": "直达快船 15~18 天",
        "inland_mode": "直接覆盖华盛顿州、俄勒冈州及西雅图区域配送中心",
        "freight_level": "避开南加州塞港，西北高湿地区防锈包装需重点加强。"
    },
    "美东": {
        "port": "诺福克港 (Norfolk) / 萨凡纳港 (Savannah)",
        "transit_sea": "全水路经巴拿马运河 30~34 天",
        "inland_mode": "卡车直派弗吉尼亚、宾州及马里兰区域分拨仓",
        "freight_level": "零内陆火车，全水路综合成本低，时效稳定。"
    },
    "美东南": {
        "port": "萨凡纳港 (Savannah) / 查尔斯顿港 (Charleston)",
        "transit_sea": "全水路 28~32 天",
        "inland_mode": "直达 Lowe's 总部枢纽(夏洛特)及 Home Depot 东南亚特兰大总仓",
        "freight_level": "全美建材零售供应链第一大黄金出海航线，极其顺畅。"
    },
    "美南核心": {
        "port": "休斯敦港 (Houston)",
        "transit_sea": "全水路直达墨西哥湾 30~35 天",
        "inland_mode": "本地拖车直达达拉斯/休斯敦/奥斯汀仓储中心",
        "freight_level": "规避美西内陆铁路转运费(IPI)，单柜综合运费节省 $1,200+。"
    },
    "美中": {
        "port": "美西清关转内陆铁路 (IPI to Chicago / Joliet)",
        "transit_sea": "海运 15 天 + BNSF/UP 铁路班列 7~9 天",
        "inland_mode": "芝加哥约利埃特铁路堆场 (Rail Ramp) 提柜，短驳至中西部 DC",
        "freight_level": "需重点监控旺季铁路堆场滞期费及底盘车轮转 (Chassis Split)。"
    },
    "美东北": {
        "port": "纽约 / 新泽西港 (NY / NJ)",
        "transit_sea": "全水路 32~36 天",
        "inland_mode": "直达纽瓦克、宾州理海谷仓储带 (Lehigh Valley)",
        "freight_level": "直击全美最密集老宅翻新修缮市场，码头清关效率高。"
    },
    "山地大区": {
        "port": "长滩港提柜内陆转铁 (LA Ramp to Salt Lake / Denver)",
        "transit_sea": "海运 15 天 + 丹佛铁路班列 5 天",
        "inland_mode": "丹佛/盐湖城物流枢纽卡车分拨",
        "freight_level": "冬季暴风雪易导致落基山脉公路封闭，需留足安全库存。"
    }
}

# ==========================================
# 5. 主页面布局与交互控制器
# ==========================================
st.title("🏬 北美大零售全品类与气候销售决策系统")
st.markdown("""
本系统通过将 **ASHRAE 采暖/制冷度日 (HDD/CDD)**、**USGS 冻土层深度**、**水质硬度 (GPG)** 及 **融雪盐环境腐蚀指数**，
与 **The Home Depot (2,300+家)**、**Lowe's (1,700+家)**、**Menards (330+家中西部)** 真实全美门店网络和物流集散枢纽（DC）深度耦合，
为中国出海建材企业提供直击买手审查（Merchant Line Review）的精准决策模型。
""")

col_cat, col_season, col_channel = st.columns([1.2, 1, 1])

with col_cat:
    selected_cat_key = st.selectbox("1. 目标核心大品类：", options=list(CATEGORY_CONFIG.keys()), format_func=lambda x: CATEGORY_CONFIG[x]["name"])

with col_season:
    selected_season = st.selectbox("2. 季节性出货脉冲 (Seasonality Pulse)：", [
        "Q1 补货/春季庭院复苏季 (Spring Refresh)",
        "Q2-Q3 夏季制冷与建材工程旺季 (Summer Construction Peak)",
        "Q4 极寒采暖/暴雪防冻应急季 (Winter Weather Emergency)",
        "全年平销稳定期 (Balanced Baseline)"
    ], index=3)

with col_channel:
    selected_channel = st.selectbox("3. 目标商超零售渠道：", [
        "全部渠道综合总盘 (All Retailers)",
        "The Home Depot (工程Pro客户第一)",
        "Lowe's (家庭DIY与软装偏好)",
        "Menards (中西部大区专营)"
    ], index=0)

cat_cfg = CATEGORY_CONFIG[selected_cat_key]

# 二级属性筛选面板
st.markdown("#### 🎯 产品规格工程属性配置")
sub_col1, sub_col2, sub_col3 = st.columns(3)
with sub_col1:
    selected_subtype = st.selectbox("产品细分规格 (Subtype)：", cat_cfg["subtypes"])
with sub_col2:
    selected_material = st.selectbox("生产原材料 (Material)：", cat_cfg["materials"])
with sub_col3:
    selected_finish = st.selectbox("表面处理工艺 (Surface Finish)：", cat_cfg["finishes"])

# ==========================================
# 6. 物理气候与房龄加权算法引擎
# ==========================================
def calculate_physics_velocity(row, cat_key, subtype, material, season):
    v = cat_cfg["base_vel"]
    
    # 房龄加权（老房集中翻修，对修缮类产品带来 10%~30% 增益）
    if row["house_age"] >= 50:
        v *= 1.25
    elif row["house_age"] >= 40:
        v *= 1.10
        
    # 气候与物理参数加权
    if cat_key == "HVAC":
        if "地" in subtype or "Baseboard" in subtype:
            v *= (1.0 + (row["hdd"] / 7000.0) * 1.5)
        if "天花" in subtype or "Filter" in subtype:
            v *= (1.0 + (row["cdd"] / 2500.0) * 1.3)
        if "WUI" in subtype:
            if "CA" in row["name"] or "WUI" in str(row["hazard"]):
                v *= 4.5
            else:
                v *= 0.2
        if "铝" in material and row["cdd"] > 2000:
            v *= 1.35
        if "铸铝" in material and row["salt_risk"] in ["高", "极高"]:
            v *= 1.45
            
    elif cat_key == "PLUMBING":
        if "防冻" in subtype or "Frost-Free" in subtype:
            if row["frost_depth"] >= 36:
                v *= 3.8
            elif row["frost_depth"] >= 18:
                v *= 2.0
            else:
                v *= 0.3
        if "地漏" in subtype:
            v *= (1.0 + (row["cdd"] / 3000.0) * 0.8)
        if "黄铜" in material and row["water_hardness"] > 12.0:
            v *= 1.4
            
    elif cat_key == "FLOORING":
        if row["salt_risk"] in ["高", "极高"]:
            if "铝" in material:
                v *= 1.5
            elif "木" in material:
                v *= 0.65
        if row["frost_depth"] > 30:
            v *= 1.2
            
    elif cat_key == "DOORS":
        if "HVHZ" in subtype or "飓风" in str(row["hazard"]):
            if row["region"] in ["美东南", "美南", "美南核心"]:
                v *= 3.5
            else:
                v *= 0.3
        if "不锈钢" in material and (row["salt_risk"] in ["高", "极高"] or "沿海" in str(row["hazard"])):
            v *= 1.6
            
    elif cat_key == "OUTDOOR":
        if row["cdd"] > 1800 or "暴雨" in str(row["hazard"]):
            v *= 1.6
        if row["salt_risk"] in ["高", "极高"]:
            if "铸铁" in material:
                v *= 1.4
            elif "镀锌" in material:
                v *= 0.7
                
    # 季节脉冲加权
    if "Q4" in season:
        if row["hdd"] > 5500:
            v *= 1.6
        else:
            v *= 0.85
    elif "Q2-Q3" in season:
        if row["cdd"] > 1500 or cat_key == "OUTDOOR":
            v *= 1.55
        if row["hdd"] > 6000:
            v *= 1.25
    elif "Q1" in season:
        v *= 1.15
        
    return round(v, 1)

# 计算各州流速
df_res = df_states.copy()
df_res["calc_vel"] = df_res.apply(
    lambda r: calculate_physics_velocity(r, selected_cat_key, selected_subtype, selected_material, selected_season), 
    axis=1
)

# 渠道筛选计算有效门店数
if selected_channel == "The Home Depot (工程Pro客户第一)":
    df_res["active_stores"] = df_res["thd"]
elif selected_channel == "Lowe's (家庭DIY与软装偏好)":
    df_res["active_stores"] = df_res["lowes"]
elif selected_channel == "Menards (中西部大区专营)":
    df_res["active_stores"] = df_res["menards"]
else:
    df_res["active_stores"] = df_res["total_stores"]

df_res["calc_total"] = df_res["calc_vel"] * df_res["active_stores"]

# 财务销售额加权计算
df_res["calc_revenue_msrp"] = df_res["calc_total"] * retail_msrp
df_res["calc_fob_total"] = df_res["calc_total"] * fob_cost
df_res["calc_buyer_profit"] = df_res["calc_total"] * gross_profit_per_unit

# 排面建议算法（根据单店流速确定货架排面 Facing 建议）
def get_pog_recommendation(vel):
    if vel >= 35.0:
        return "🔥 建议双排面 (Double Facings, 24寸)"
    elif vel >= 15.0:
        return "✅ 标准单排面 (Single Facing, 12寸)"
    else:
        return "⚠️ 底层或下挂排面 (Bottom Shelf / Pegboard)"

df_res["pog_facings"] = df_res["calc_vel"].apply(get_pog_recommendation)

# 双视角排名
df_res["rank_vel"] = df_res["calc_vel"].rank(ascending=False, method="min").astype(int)
df_res["rank_total"] = df_res["calc_total"].rank(ascending=False, method="min").astype(int)

# ==========================================
# 7. 全网销售看板核心指标
# ==========================================
st.markdown("---")
m1, m2, m3, m4 = st.columns(4)

total_national_volume = int(df_res["calc_total"].sum())
total_national_revenue = df_res["calc_revenue_msrp"].sum()
total_fob_wholesale = df_res["calc_fob_total"].sum()

with m1:
    st.metric("📦 全美测算月总销量 (件)", f"{total_national_volume:,}")
with m2:
    st.metric("💵 全美月零售总流水 MSRP ($)", f"${total_national_revenue:,.0f}")
with m3:
    st.metric("🚢 出海工厂月 FOB 盘 ($)", f"${total_fob_wholesale:,.0f}")
with m4:
    top_throughput_state = df_res.sort_values("calc_total", ascending=False).iloc[0]["name"]
    st.metric("🏆 月度吞吐量冠军州", f"{top_throughput_state}")

# ==========================================
# 8. 核心决策呈现：双视角排行榜与单州深度透视
# ==========================================
st.markdown("---")
tab_table, tab_detail, tab_compliance = st.tabs(["📊 全美 50 州排行榜看板", "🔍 单州物理与海运供应链透视", "📜 商超买手合规与打托标准"])

with tab_table:
    view_type = st.radio(
        "选择榜单排序维度：", 
        ["全州渠道总出货盘 (Total Volume Units - 适合排产总盘计划)", "单店平均销售流速 (Velocity Units/Store - 适合精准选品与补货)"], 
        horizontal=True
    )
    
    if "Total" in view_type:
        sorted_df = df_res.sort_values("calc_total", ascending=False)
    else:
        sorted_df = df_res.sort_values("calc_vel", ascending=False)
        
    display_df = sorted_df[[
        "name", "region", "active_stores", "calc_vel", "calc_total", "calc_revenue_msrp", 
        "house_age", "pog_facings", "dc"
    ]].copy()
    
    max_vel_val = max(int(df_res["calc_vel"].max()), 1)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        column_config={
            "name": st.column_config.TextColumn("州名 (State)"),
            "region": st.column_config.TextColumn("大区 (Region)"),
            "active_stores": st.column_config.NumberColumn("有效门店数", format="%d"),
            "calc_vel": st.column_config.ProgressColumn("单店流速 (件/店/月)", min_value=0, max_value=max_vel_val, format="%.1f"),
            "calc_total": st.column_config.NumberColumn("月度总出货 (件)", format="%d"),
            "calc_revenue_msrp": st.column_config.NumberColumn("月零售总流水 ($)", format="$%d"),
            "house_age": st.column_config.NumberColumn("中位房龄 (年)", format="%d 年"),
            "pog_facings": st.column_config.TextColumn("POG 货架排面建议"),
            "dc": st.column_config.TextColumn("物流枢纽仓 (DC)")
        },
        height=480
    )

with tab_detail:
    st.markdown("### 🔎 目标州专属工程气象、物流港口与客群透视")
    target_state = st.selectbox(
        "选择要深入透视的目标州：", 
        options=list(STATES_DATA.keys()), 
        format_func=lambda x: f"{x} - {STATES_DATA[x]['name']} ({STATES_DATA[x]['region']})"
    )
    
    st_info = df_res.loc[target_state]
    col_info1, col_info2 = st.columns([1, 1.2])
    
    with col_info1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top:0;">{st_info['name']} ({target_state}) - 选品决策指标</h3>
            <p>• <b>全美流速排名 (Velocity Rank)</b>: 第 <b>#{st_info['rank_vel']}</b> 名 (单店 <b>{st_info['calc_vel']}</b> 件/店/月)</p>
            <p>• <b>全美总吞吐量排名 (Total Rank)</b>: 第 <b>#{st_info['rank_total']}</b> 名 (总盘 <b>{int(st_info['calc_total']):,}</b> 件/月)</p>
            <p>• <b>全美零售流水预估 (MSRP Volume)</b>: <b>${st_info['calc_revenue_msrp']:,.0f}</b> /月</p>
            <p>• <b>该州渠道门店数</b>: THD: <b>{st_info['thd']}</b> | Lowe's: <b>{st_info['lowes']}</b> | Menards: <b>{st_info['menards']}</b></p>
            <p>• <b>货架空间策略 (POG)</b>: <b>{st_info['pog_facings']}</b></p>
            <p>• <b>主力物流集散仓 (RDC)</b>: <b>{st_info['dc']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        region_logistics = PORT_LOGISTICS_MATRIX.get(st_info["region"], {
            "port": "美西基本港 (LA/LB) / 萨凡纳港",
            "transit_sea": "快船 16~25 天",
            "inland_mode": "全国区域干线中转",
            "freight_level": "通用标准航线"
        })
        
        st.markdown(f"""
        <div class="physics-card">
            <b>🚢 推荐出海口岸与清关物流路径</b><br>
            • <b>首选清关港口 (Port of Entry)</b>: <span style="color:#0369a1;font-weight:600;">{region_logistics['port']}</span><br>
            • <b>海上运输航程</b>: {region_logistics['transit_sea']}<br>
            • <b>内陆干线调度 (Inland Drayage)</b>: {region_logistics['inland_mode']}<br>
            • <b>成本与风控提示</b>: <span style="font-size:0.85rem;color:#475569;">{region_logistics['freight_level']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col_info2:
        st.markdown(f"""
        <div class="physics-card">
            <b>🌡️ 气候物理实测参数与住宅特征</b><br>
            • 采暖度日 (HDD): <b>{st_info['hdd']}</b> | 制冷度日 (CDD): <b>{st_info['cdd']}</b><br>
            • 房屋中位房龄: <b>{st_info['house_age']} 年</b> {'(⚠️ 50年以上老宅区，老规格翻新是主流)' if st_info['house_age']>=50 else ''}<br>
            • 冻土深度 (Frost Line): <b>{st_info['frost_depth']} 英寸</b> {'(⚠️ 极深冻土)' if st_info['frost_depth']>=42 else ''}<br>
            • 水质硬度: <b>{st_info['water_hardness']} GPG</b> {'(⚠️ 极重度硬水结垢)' if st_info['water_hardness']>=12 else ''}<br>
            • 融雪盐腐蚀等级: <b>{st_info['salt_risk']}</b> {'(⚠️ 严禁碳钢裸露)' if st_info['salt_risk'] in ['高','极高'] else ''}<br>
            • 极端气候标签: <span class="badge-warning">{st_info['hazard']} (灾害指数: {st_info['hazard_idx']}/10)</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 法律红线与强制准入
        st.markdown("<b>⚖️ 该州法定义务与商超准入红线：</b>", unsafe_allow_html=True)
        redlines = []
        if target_state == "CA":
            redlines.append("加州 Proposition 65 (加州65号提案)：必须附带致癌/生殖毒性警示黄标，否则面临职业赏金猎人高额诉讼。")
            redlines.append("Title 24 & WUI 规范：阁楼通风口必须附带 1/8 英寸防飞烬金属网。")
        elif target_state == "FL":
            redlines.append("Florida Building Code (HVHZ 迈阿密-戴德县认证)：门窗及户外五金必须耐受 140+ mph 强飓风飞弹冲击测试。")
        elif st_info["frost_depth"] >= 36:
            redlines.append("IPC 规范第 305.4 节：室外供水管线及龙头必须使用防冻自泄水阀 (Frost-Free Sillcock)，避免水管爆裂。")
        elif st_info["water_hardness"] >= 12.0:
            redlines.append("无铅黄铜红线：必须符合 NSF/ANSI 372 无铅标准，同时需耐脱锌腐蚀 (DZR)，防止管件内部被硬水析出物堵死。")
        else:
            redlines.append("通用 ASTM / ANSI 标准准入，无特殊极端强制地方法规阻碍。")
            
        for rl in redlines:
            st.markdown(f"- 🔴 <span style='font-size:0.88rem;color:#991b1b;'>{rl}</span>", unsafe_allow_html=True)

    st.markdown("---")
    # 客群画像与包装建议
    st.markdown("#### 👥 客群渗透模型与包装工程方案")
    p1, p2, p3 = st.columns(3)
    
    if "铸铝" in selected_material or "316" in selected_material or "ProPress" in selected_subtype or "HVHZ" in selected_subtype:
        diy_share, pro_share = 30, 70
        main_customer = "工程承包商与专业水电工 (Pro Contractors)"
    elif "塑料" in selected_material or "贴皮" in selected_material:
        diy_share, pro_share = 75, 25
        main_customer = "普通业主周末自装客 (DIY Homeowners)"
    else:
        diy_share, pro_share = 55, 45
        main_customer = "DIY 业主与小修缮杂工 (Handyman) 均衡"
        
    with p1:
        st.markdown(f"""
        **买家结构渗透：**
        * <span class="badge-diy">DIY 业主: {diy_share}%</span>
        * <span class="badge-pro">Pro 承包商: {pro_share}%</span>
        * 核心消费画像：**{main_customer}**
        """, unsafe_allow_html=True)
        
    with p2:
        return_rate_est = "2.5% ~ 3.5%" if "塑料" not in selected_material else "4.8% ~ 6.5%"
        st.markdown(f"""
        **退货率与质量预警：**
        * 预估综合退货率: **{return_rate_est}**
        * 头号退货原因: **开孔尺寸买错** (开孔尺寸 vs 外部面罩尺寸混淆)
        * 防退方案: 包装醒目印制 **1:1 开孔尺寸打孔定位卡纸**
        """)
        
    with p3:
        st.markdown(f"""
        **包装与美标托盘规范 (GMA Pallet)：**
        * **标准打托规格**: 48 × 40 英寸 GMA 木托盘
        * **推荐装箱配置**: {case_pack} 件/箱
        * **堆码规格 (TI/HI)**: 每层 6 箱 (TI=6) × 堆叠 8 层 (HI=8) = **48 箱/托**
        * **单托容纳总量**: **{case_pack * 48} 件/托盘** (高度控在 50 英寸内)
        * **外箱标签**: 必须打印 GS1-128 / ITF-14 物流仓储条码
        """)

with tab_compliance:
    st.markdown(f"### 📋 【{cat_cfg['name']}】商超买手必备行业标准与认证")
    st.caption("这是 The Home Depot、Lowe's 及 Menards 买手在做新供应商准入（Vendor Onboarding）审查时的一票否决合规项：")
    
    comp_col1, comp_col2 = st.columns([1.2, 1])
    with comp_col1:
        st.markdown("#### 1. 核心测试与强制认证标准")
        for idx, item in enumerate(cat_cfg["compliance"], 1):
            st.markdown(f"""
            <div style="background:#f8fafc;padding:10px 14px;border-left:4px solid #10b981;margin-bottom:8px;border-radius:4px;">
                <b>{idx}. {item}</b>
            </div>
            """, unsafe_allow_html=True)
            
    with comp_col2:
        st.markdown("#### 2. 商超买手审厂 (Factory Audit) 重点")
        st.markdown("""
        * **社会责任与人权审核**: 通过 Sedex (SMETA) 或 amfori BSCI 审核。
        * **质量管理体系**: ISO 9001 认证及出厂盐雾测试报告 (ASTM B117)。
        * **EDI 电子数据交换能力**: 必须支持 ANSI X12 格式（EDI 850 订单、EDI 856 发货通知 ASN、EDI 810 电子发票）。
        * **产品缺陷责任险 (Product Liability Insurance)**: 针对商超渠道必须购买保额不低于 **$5,000,000 美元** 的全球产品责任险，并在保单中追加零售商为附加被保险人。
        * **Chargeback 罚款防范机制**: 熟悉商超入库条码扫描率要求（必须达到 99.5% 以上，否则每单面临 $250~$500 罚款）。
        """)

# ==========================================
# 9. 决策数据导出与闭环建议
# ==========================================
st.markdown("---")
exp_col1, exp_col2 = st.columns([1, 3])

with exp_col1:
    csv_data = df_res.to_csv(index=True).encode("utf-8")
    st.download_button(
        label="📥 导出全美选品与物理销售预测 CSV",
        data=csv_data,
        file_name=f"NA_Retail_Decision_{selected_cat_key}_{selected_season[:2]}.csv",
        mime="text/csv"
    )

with exp_col2:
    st.caption("💡 **买手谈判战略备忘**: 在向 Home Depot / Lowe's 提报该产品时，重点强调材质在极端气象下的寿命优势（如 6063 阳极氧化抗高湿冷凝、304/316 材质抵御北方融雪盐），并以本模型单店流速数据支撑初始货架占位宽度（POG Facings）。")
