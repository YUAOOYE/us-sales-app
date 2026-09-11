import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 1. 页面配置与威霖定制视觉规范
# ==============================================================================
st.set_page_config(
    page_title="宁波威霖住宅设施 · 北美大零售全品类与气候销售决策系统",
    page_icon="🏭",
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
    
    .badge-tier1 { background-color: #dcfce7; color: #166534; padding: 2px 7px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier2 { background-color: #dbeafe; color: #1e40af; padding: 2px 7px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier3 { background-color: #fef3c7; color: #92400e; padding: 2px 7px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier4 { background-color: #fee2e2; color: #991b1b; padding: 2px 7px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    
    .radar-box { border-left: 4px solid #EF4444; background-color: #FEF2F2; padding: 10px 14px; border-radius: 0 6px 6px 0; margin-top: 10px; }
    .advice-box { border-left: 4px solid #3B82F6; background-color: #EFF6FF; padding: 10px 14px; border-radius: 0 6px 6px 0; margin-top: 10px; }
    .cert-badge { background-color: #f1f5f9; border: 1px solid #cbd5e1; color: #0f172a; padding: 3px 6px; border-radius: 4px; font-size: 0.75rem; margin-right: 4px; display: inline-block; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. 侧边栏：威霖出海财务与买手测算器
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/factory.png", width=54)
    st.title("威霖制造 · 出海决策中台")
    st.caption("宁波威霖住宅设施有限公司 (建霖家居 603408)")
    st.markdown("---")
    
    st.markdown("### 💰 威霖外贸买手核价与到岸毛利试算")
    fob_cost = st.number_input("1. 威霖出厂供货价 FOB ($/件)：", min_value=0.5, max_value=200.0, value=3.80, step=0.2)
    ocean_freight = st.number_input("2. 单件美线分摊海运费 ($/件)：", min_value=0.0, max_value=50.0, value=0.65, step=0.05)
    tariff_pct = st.number_input("3. 关税税率 Tariff (%)：", min_value=0.0, max_value=100.0, value=7.5, step=0.5) / 100.0
    retail_msrp = st.number_input("4. 北美商超零售价 MSRP ($/件)：", min_value=1.0, max_value=500.0, value=12.98, step=0.5)
    case_pack = st.number_input("5. 标准箱外箱装数 (Case Pack)：", min_value=1, max_value=100, value=10, step=1)
    
    landed_cost = fob_cost * (1 + tariff_pct) + ocean_freight
    buyer_margin = ((retail_msrp - landed_cost) / retail_msrp) * 100
    gross_profit_unit = retail_msrp - landed_cost
    
    st.markdown(f"• **到岸完税成本 (Landed DDP)**: **${landed_cost:.2f}**")
    st.markdown(f"• **商超单件毛利额**: **${gross_profit_unit:.2f}**")
    
    if buyer_margin < 40.0:
        st.markdown(f'<span class="badge-tier4">⚠️ 零售到岸毛利率：{buyer_margin:.1f}% (偏低，低于40%采购门槛)</span>', unsafe_allow_html=True)
    elif buyer_margin <= 55.0:
        st.markdown(f'<span class="badge-tier1">✅ 零售到岸毛利率：{buyer_margin:.1f}% (商超黄金采购区间)</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="badge-tier1">🌟 零售到岸毛利率：{buyer_margin:.1f}% (超55%极具采购竞争力)</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏭 威霖象山工业园制造能力标签")
    st.caption("""
    • **占地面积**：14 万平方米智能制造基地  
    • **核心工艺**：自动化冲压、智能注塑、绿色PVD镀膜、重防腐电泳、精密模具研发  
    • **合规体系**：ISO 9001 / ISO 14001 / cUPC 实验室 / UL 认证实验室
    """)

# ==============================================================================
# 3. 核心品类配置（100% 对标宁波威霖实际产线）
# ==============================================================================
CATEGORY_CONFIG = {
    "HVAC": {
        "name": "暖通风口与空气分配末端 (Registers & Diffusers)",
        "willi_fit": "威霖主力核心板块：冲压冷轧钢、阳极氧化铝、工程阻燃塑料出风口全系列。",
        "positions": ["Floor (地面出风口)", "Ceiling (天花板散流器)", "Baseboard (踢脚线出风口)", "Sidewall (侧墙回风格栅)"],
        "materials": ["Steel (冲压冷轧钢)", "Aluminum (铝合金阳极氧化)", "Plastic (ABS阻燃树脂)", "Cast Metal (铸铝/铸铁重载)"],
        "finishes": ["BL (Matte Black 哑光黑)", "BN (Brushed Nickel 拉丝镍)", "WH (White 经典白)", "AB (Antique Brass 仿古铜)", "ORB (Oil Rubbed Bronze 油磨青铜)"],
        "sizes": ["04X10 (全美走量王 65%)", "04X12 (主流换新大号 20%)", "02X12 (踢脚狭长缝 10%)", "06X10 (大出风量 5%)", "12X12 (天花板方型)"],
        "national_certs": ["ASHRAE 70 (风量CFM与噪音NC评级测试)", "UL 94 (塑料阻燃V-0级认证)", "Heel-Proof (细高跟鞋防卡穿透试验)"]
    },
    "PLUMBING": {
        "name": "卫浴排水与长条隐形地漏 (Drains & Plumbing)",
        "willi_fit": "威霖主力核心板块：不锈钢冲压拉伸、长条隐形线性地漏、防臭下水器全系列。",
        "positions": ["Floor Drain (方形地面地漏)", "Linear Drain (长条隐形淋浴地漏)", "Tile-in (瓷砖双面隐形地漏)", "Frost-Proof (室外防冻水阀)"],
        "materials": ["Stainless 304 (304拉丝不锈钢)", "Stainless 316 (316耐氯盐雾级)", "Solid Brass (无铅锻压黄铜)", "ABS/PVC (耐腐工程塑料)"],
        "finishes": ["BN (Brushed Nickel 经典拉丝镍)", "MB (Matte Black 现代哑光黑)", "CP (Chrome 抛光亮铬)", "BG (Brushed Gold PVD拉丝金)"],
        "sizes": ["4x4 inch (标准方形地漏)", "24-36 inch (长条隐形地漏)", "1/2 inch (常规接口)", "3/4 inch (主水管接口)"],
        "national_certs": ["cUPC 认证 (IAPMO 强制排水与管件证书)", "ASME A112.18.2 / CSA B125.2 (地漏通量测试)", "NSF/ANSI 61 & 372 (接触饮用水无铅涉水安全认证)"]
    },
    "HANGERS": {
        "name": "管道支吊架与抗震支撑系统 (Support & Hanger Systems)",
        "willi_fit": "威霖特色工程王牌：建筑管道吊卡、C型槽钢构件、抗震连接件、商用管道支撑。",
        "positions": ["Strut Channel (C型装配式槽钢系统)", "Pipe Clamp (重载管道固定卡箍)", "Seismic Hanger (抗震斜撑加固组件)", "Beam Clamp (工字钢梁夹连接件)"],
        "materials": ["Carbon Steel (重载碳钢镀锌)", "Hot-Dip Galvanized (重型热浸镀锌钢)", "Stainless 304 (不锈钢防腐型)", "Ductile Iron (球墨铸铁梁夹)"],
        "finishes": ["Clear Zinc (冷电镀蓝白锌 EG)", "Yellow Zinc (环保三价铬彩锌)", "HDG (热浸镀锌厚层防腐)", "Black E-Coat (阴极电泳底漆)"],
        "sizes": ["13/16 inch (轻型槽深)", "1-5/8 inch (全美标准重载槽钢)", "1/2-2 inch (小管径管卡)", "3-6 inch (重型主立管卡)"],
        "national_certs": ["MSS SP-58 (全美管道吊架与支撑设计制造通用标准)", "UL 203 (消防喷淋管道吊架强制认证)", "FM 1951 (抗震支撑组件认证)"]
    },
    "SHOWER_HARDWARE": {
        "name": "淋浴门与门窗五金构件 (Shower Door & Enclosures)",
        "willi_fit": "威霖主力核心板块：淋浴房铰链、滚轮滑轨、不锈钢合页、门底挡风防水条。",
        "positions": ["Shower Hinge (无框玻璃淋浴房合页)", "Door Sweep (门底防风挡水密封条)", "Hurricane Tie (建筑抗飓风加固角码)", "Heavy Duty Hinge (重型承重门合页)"],
        "materials": ["Solid Brass (精铸无铅纯铜)", "Stainless 304 (304防锈不锈钢)", "Aluminum + Silicone (铝合金托底+耐候硅胶)", "Hot-Dip Galvanized (热浸镀锌结构钢)"],
        "finishes": ["Matte Black (US19 现代黑)", "Brushed Nickel (US15 缎面拉丝镍)", "Bright Chrome (US26 抛光亮铬)", "PVD Brushed Brass (US4 耐磨金)"],
        "sizes": ["36 inch (单门标准长)", "42 inch (大入户门底条)", "4x4 inch (重载大门合页)", "50 ft Roll (50英尺整卷密封条)"],
        "national_certs": ["ANSI/BHMA A156.1 (100万次开合疲劳测试)", "ANSI Z97.1 / CPSC 16 CFR 1201 (安全玻璃与五金承重规范)", "UL 10C (90分钟正压防火门认证)"]
    },
    "OUTDOOR_DRAIN": {
        "name": "户外排水与景观系统 (Outdoor Drainage & Grates)",
        "willi_fit": "威霖延伸产线：庭院车道线性排水槽、重载钢格栅、外墙通风百叶罩。",
        "positions": ["Trench Drain (车道/泳池线性排水沟)", "Gutter Guard (屋檐排水天沟防叶滤网)", "Post Anchor (木露台立柱固定底座)", "Outdoor Vent (外墙防风雨冲压罩)"],
        "materials": ["Polymer/HDPE (耐暴晒重型塑料)", "Hot-Dip Galvanized (热镀锌重钢格栅)", "Ductile Cast Iron (球墨铸铁重载盖板)", "Cast Aluminum (耐候防腐铸铝)"],
        "finishes": ["Black Asphalt (沥青防腐黑)", "Galvanized Silver (热镀锌亮银)", "Natural Gray (水泥工程灰)"],
        "sizes": ["39 inch / 1 Meter (标准单段沟长)", "5-6 inch (标准屋檐天沟网)", "4x4 inch (木方柱底座)", "6x6 inch (重载立柱底座)"],
        "national_certs": ["EN 1433 / ANSI A112.6.3 (A15行人 ~ C250汽车承重等级)", "ASTM A123 (热浸镀锌耐盐雾防腐标准)", "ASTM G154 (户外高强度抗紫外线黄变及脆化测试)"]
    }
}

# ==============================================================================
# 4. 全美 50 州精准工程与物理数据库（含地基结构与州级认证红线）
# ==============================================================================
STATES_DATA = {
    "NC": {
        "cn": "北卡罗来纳州", "name": "North Carolina", "region": "美东南", "thd": 72, "lowes": 105, "menards": 0, "dc": "夏洛特(Lowe's大本营)",
        "foundation": "架空层/地下室(75%+)", "climate": "Zone 4A/3A 混合湿润", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖地面出风口、实木高低压条、防潮五金", "avoid": "未做防锈处理冷轧薄铁件",
        "size_breakdown": "地面主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线狭窄区: 2x12 (10%); 回风: 6x10 (5%)",
        "channel_advice": "Lowe's全球总部大本营，THD门店流转极快，重度配置端架(Endcap)促销位。",
        "hdd": 3400, "cdd": 1600, "frost_depth": 12, "water_hardness": 3.0, "salt_risk": "中", "hazard": "沿海飓风/湿热雷暴", "house_age": 33, "hazard_idx": 5, "base_vel": 42.0,
        "state_certs": ["NC State Building Code (沿海风暴锚固)", "ASHRAE 90.1 通风能效审计"]
    },
    "TN": {
        "cn": "田纳西州", "name": "Tennessee", "region": "美南", "thd": 44, "lowes": 58, "menards": 0, "dc": "孟菲斯全美物流中心",
        "foundation": "木结构架空层/地下室", "climate": "Zone 4A 混合温和", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖重载地面出风口、管道吊架卡箍", "avoid": "天花专用下送风散流器",
        "size_breakdown": "地面主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)",
        "channel_advice": "孟菲斯与纳什维尔物流核心区，全美出货中枢，适宜设总仓辐射美中南与美东。",
        "hdd": 3500, "cdd": 1650, "frost_depth": 12, "water_hardness": 6.5, "salt_risk": "中", "hazard": "冻融交替/暴风雨", "house_age": 37, "hazard_idx": 4, "base_vel": 40.5,
        "state_certs": ["MSS SP-58 管道支吊架标准", "cUPC 地漏排水认证"]
    },
    "KY": {
        "cn": "肯塔基州", "name": "Kentucky", "region": "美南", "thd": 27, "lowes": 38, "menards": 9, "dc": "路易斯维尔",
        "foundation": "全地下室占80%+", "climate": "Zone 4A 四季鲜明多雪", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖地下管道风口、铸铝复古格栅", "avoid": "无调节阀轻薄空框",
        "size_breakdown": "地面主力: 4x10 (65%); 换新大号: 4x12 (20%); 踢脚线: 2x12 (10%); 回风: 6x10 (5%)",
        "channel_advice": "老房翻修与自建房比例高，Pro工匠批量成箱采购占比较大。",
        "hdd": 4400, "cdd": 1250, "frost_depth": 20, "water_hardness": 10.5, "salt_risk": "高", "hazard": "冬季道路融雪盐结冰", "house_age": 43, "hazard_idx": 4, "base_vel": 38.0,
        "state_certs": ["UL 94 阻燃测试", "IPC 县级水暖抗冻裂标准"]
    },
    "SC": {
        "cn": "南卡罗来纳州", "name": "South Carolina", "region": "美东南", "thd": 37, "lowes": 48, "menards": 0, "dc": "哥伦比亚/萨凡纳",
        "foundation": "架空层/沿海桩基", "climate": "Zone 3A 亚热带湿热", "flooring": "实木 40%, LVP 35%, 瓷砖 15%, 地毯 10%",
        "best": "威霖工程ABS风口、耐盐雾不锈钢地漏", "avoid": "未做防腐普通冷轧铁件",
        "size_breakdown": "标准通用型: 4x10 (65%); 4x12 (20%); 2x12 (10%); 回风: 6x10 (5%)",
        "channel_advice": "沿海重度防腐耐盐雾，内陆侧重地板防潮收口五金。",
        "hdd": 2400, "cdd": 2000, "frost_depth": 5, "water_hardness": 3.0, "salt_risk": "低", "hazard": "沿海强飓风/高湿热腐蚀", "house_age": 31, "hazard_idx": 6, "base_vel": 36.0,
        "state_certs": ["ASTM B117 盐雾 500h 测试", "ASTM A153 热浸镀锌层检验"]
    },
    "OH": {
        "cn": "俄亥俄州", "name": "Ohio", "region": "美中", "thd": 71, "lowes": 73, "menards": 34, "dc": "哥伦布核心仓",
        "foundation": "100%全地下室为主", "climate": "Zone 5A 寒冷多雪长冬", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖冲压金属/铝合金地面风口、槽钢支吊架", "avoid": "薄脆塑料、天花专用下送风散流器",
        "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%); 回风: 6x10 (5%)",
        "channel_advice": "五金和建材传统大州，老旧翻新是第一驱动力，Menards 与 THD 竞争激烈。",
        "hdd": 5600, "cdd": 850, "frost_depth": 36, "water_hardness": 15.0, "salt_risk": "极高", "hazard": "暴雪融雪盐侵蚀+极硬水", "house_age": 54, "hazard_idx": 7, "base_vel": 32.0,
        "state_certs": ["UL 203 消防管道吊架认证", "ASHRAE 70 风量与静音评级"]
    },
    "IN": {
        "cn": "印第安纳州", "name": "Indiana", "region": "美中", "thd": 41, "lowes": 42, "menards": 39, "dc": "印第安纳波利斯",
        "foundation": "全地下室占85%+", "climate": "Zone 5A 严寒多雪", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖地面暖风风口、C型槽钢支架", "avoid": "天花专用风口",
        "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%); 回风: 6x10 (5%)",
        "channel_advice": "工业底子扎实，家庭 DIY 普及率高，Menards 渗透极深。",
        "hdd": 5500, "cdd": 1000, "frost_depth": 36, "water_hardness": 17.0, "salt_risk": "极高", "hazard": "重度硬水结垢/大雪盐蚀", "house_age": 48, "hazard_idx": 6, "base_vel": 31.5,
        "state_certs": ["MSS SP-58 承重强度验证", "NSF 372 无铅涉水认证"]
    },
    "IL": {
        "cn": "伊利诺伊州", "name": "Illinois", "region": "美中", "thd": 81, "lowes": 43, "menards": 61, "dc": "大芝加哥枢纽",
        "foundation": "全地下室占绝大多数", "climate": "Zone 5A 大陆性严寒大风", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖重型地面风口、装配式槽钢支架", "avoid": "轻薄无卡扣风口",
        "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%); 回风: 6x10 (5%)",
        "channel_advice": "大芝加哥商超网络极其密集，单店流转稳定，总盘吞吐量位列全美第一梯队。",
        "hdd": 6100, "cdd": 900, "frost_depth": 42, "water_hardness": 14.5, "salt_risk": "极高", "hazard": "芝加哥狂风暴雪融雪盐", "house_age": 56, "hazard_idx": 7, "base_vel": 30.0,
        "state_certs": ["City of Chicago Building Code (芝加哥防火及建筑严格标准)", "UL 203 吊架"]
    },
    "MI": {
        "cn": "密歇根州", "name": "Michigan", "region": "美中", "thd": 70, "lowes": 43, "menards": 44, "dc": "底特律仓",
        "foundation": "100%全地下室", "climate": "Zone 5A/6A 大湖雪带漫长冬", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖经典地面金属风口、耐融雪盐涂层构件", "avoid": "天花风口、薄铁喷漆",
        "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%); 回风: 6x10 (5%)",
        "channel_advice": "底特律周边老房基数庞大，换新频次极高，融雪盐耐受是选品第一红线。",
        "hdd": 6800, "cdd": 650, "frost_depth": 48, "water_hardness": 12.0, "salt_risk": "极高", "hazard": "大湖雪带超长严冬", "house_age": 52, "hazard_idx": 7, "base_vel": 29.5,
        "state_certs": ["ASTM B117 盐雾测试 480h+", "ASHRAE 70 通风评级"]
    },
    "FL": {
        "cn": "佛罗里达州", "name": "Florida", "region": "美东南", "thd": 155, "lowes": 110, "menards": 0, "dc": "奥兰多/迈阿密",
        "foundation": "95%+混凝土平板地基(Slab)", "climate": "Zone 1A/2A 极湿热高盐雾飓风", "flooring": "瓷砖 60%, 强化/LVP 25%, 地毯 15%",
        "best": "威霖天花散流器、不锈钢长条地漏、抗飓风门窗五金", "avoid": "地面出风口 (实心水泥地，绝对禁发货!)",
        "size_breakdown": "天花板主推: 6x6, 8x8, 12x12 (65%); 侧墙回风: 14x6, 20x20 (35%)",
        "channel_advice": "纯制冷市场，严禁发地面风口；主推 HVHZ 抗飓风门窗五金与防腐地漏。",
        "hdd": 500, "cdd": 3800, "frost_depth": 0, "water_hardness": 14.0, "salt_risk": "极低", "hazard": "HVHZ五级强飓风/极高盐雾", "house_age": 34, "hazard_idx": 9, "base_vel": 21.0,
        "state_certs": ["Miami-Dade NOA (迈阿密-戴德县抗飞弹飓风最高认证)", "FBC (Florida Building Code) HVHZ标准", "cUPC 耐盐雾淋浴地漏认证"]
    },
    "CA": {
        "cn": "加利福尼亚州", "name": "California", "region": "美西", "thd": 234, "lowes": 112, "menards": 0, "dc": "洛杉矶/安大略总仓",
        "foundation": "南加全平板/抗震高要求", "climate": "Zone 3B/4B 干燥温和干热", "flooring": "瓷砖 45%, LVP 35%, 地毯 20%",
        "best": "威霖 Title 24环保风口、抗震支架组件、WUI防飞烬外墙罩", "avoid": "高铅铸造件、普通易燃塑料",
        "size_breakdown": "天花主推: 6x6, 8x8, 10x10 (60%); 侧墙格栅: 14x6 (40%)",
        "channel_advice": "全美最大单一经济体，但加州 65 号提案（Prop 65 铅标）是法律诉讼雷区，必须贴标。",
        "hdd": 2100, "cdd": 1300, "frost_depth": 0, "water_hardness": 9.5, "salt_risk": "极低", "hazard": "WUI山火/高烈度地震/Prop 65铅标", "house_age": 48, "hazard_idx": 7, "base_vel": 20.0,
        "state_certs": ["加州 Proposition 65 无铅环保警告标签 (极严强制)", "加州 Title 24 气密性能源审计法案", "加州 HCAI/OSHPD 管道抗震支吊架预审批", "加州 WUI (Wildland-Urban Interface) 1/8寸防火防飞烬认证"]
    },
    "TX": {
        "cn": "德克萨斯州", "name": "Texas", "region": "美南核心", "thd": 182, "lowes": 145, "menards": 0, "dc": "达拉斯/休斯敦大仓",
        "foundation": "85%+混凝土实心大平板(Slab)", "climate": "Zone 2A/3A/3B 漫长干热湿热", "flooring": "瓷砖 50%, 抛光强化 30%, 地毯 20%",
        "best": "威霖天花散流器、回风百叶格栅、重型管道吊架", "avoid": "地面下沉式出风口 (实心地基无孔可用!)",
        "size_breakdown": "天花散流器: 6x6, 8x8, 12x12 (70%); 墙面回风: 14x6, 20x20 (30%)",
        "channel_advice": "全美建材总盘第一大州，虽单店被门店密摊薄，但总吞吐量是工厂开工基本盘。",
        "hdd": 1600, "cdd": 3000, "frost_depth": 5, "water_hardness": 12.5, "salt_risk": "低", "hazard": "酷暑极干热/偶发寒潮破管", "house_age": 31, "hazard_idx": 6, "base_vel": 22.0,
        "state_certs": ["TDI (Texas Dept of Insurance) 沿海防风认证", "ASHRAE 90.1 能耗标准", "MSS SP-58 吊架承重测试"]
    }
}

# 补充其余 39 州基础数据库，保证全美 50 州完整
EXTRA_STATES_CONFIG = {
    "PA": ("宾夕法尼亚州", "Pennsylvania", "美东", 73, 83, 0, "全地下室占85%+", 5400, 900, 38, 8.5, "极高", "老房融雪盐", 58, 28.5, ["ASTM B117 盐雾 480h", "cUPC 地漏"]),
    "NY": ("纽约州", "New York", "美东北", 100, 68, 0, "市区公寓无风管/郊区独栋地下室", 5900, 800, 48, 5.5, "极高", "湖效应暴雪", 62, 26.0, ["NYSERDA 能源认证", "UL 94 阻燃"]),
    "WI": ("威斯康星州", "Wisconsin", "美中", 28, 14, 45, "全地下室普及率极高", 7400, 550, 54, 14.5, "极高", "暴雪融雪盐", 51, 25.5, ["Menards 供应商标准", "MSS SP-58"]),
    "MN": ("明尼苏达州", "Minnesota", "美中", 35, 12, 38, "全地下室/水暖多", 8500, 550, 60, 14.0, "极高", "全美最深冻土(60寸)", 46, 24.5, ["IPC 305.4 超长防冻水阀规范", "UL 203 吊架"]),
    "CO": ("科罗拉多州", "Colorado", "山地大区", 47, 28, 0, "防冻全地下室", 6200, 600, 36, 7.5, "高", "高海拔强紫外线", 38, 24.0, ["WUI 山火防飞烬网", "ASHRAE 70"]),
    "WA": ("华盛顿州", "Washington", "美西北", 48, 38, 0, "架空层/现代高气密住宅", 4900, 300, 18, 2.5, "低", "长年阴雨高湿", 43, 23.5, ["WA State Energy Code", "ASTM G154 户外防霉测试"]),
    "AZ": ("亚利桑那州", "Arizona", "美西南", 58, 33, 0, "100%混凝土平板地基(Slab)", 1200, 3500, 0, 16.5, "极低", "极端沙漠酷暑+极硬水", 30, 19.5, ["NSF 372 无铅涉水", "抗紫外线黄变测试"]),
    "AK": ("阿拉斯加州", "Alaska", "美西北", 7, 5, 0, "永久冻土抬升/保温地基", 10500, 0, 72, 6.0, "中", "全美最高寒(HDD>10000)", 42, 25.0, ["极低温-40℃冲击韧性测试", "超耐寒密封"]),
    "HI": ("夏威夷州", "Hawaii", "美西", 7, 4, 0, "火山岩/防潮桩", 0, 4200, 0, 3.0, "低", "纯海岛极端高盐雾", 47, 18.0, ["ASTM B117 盐雾 1000h+ (强制316级)", "cUPC"]),
    "MO": ("密苏里州", "Missouri", "美中", 39, 33, 19, "传统全地下室木屋", 4800, 1400, 28, 11.0, "高", "冰融循环", 47, 27.5, ["ASHRAE 70", "MSS SP-58"]),
    "AL": ("阿拉巴马州", "Alabama", "美东南", 29, 34, 0, "平原浅架空", 2600, 1900, 5, 4.5, "低", "雷暴雨林", 36, 28.0, ["ASTM A153 镀锌", "cUPC"]),
    "AR": ("阿肯色州", "Arkansas", "美南", 15, 20, 0, "林区架空层木屋", 3200, 1700, 10, 5.0, "低", "雷暴高湿", 39, 27.0, ["ASTM A123 防腐", "cUPC"]),
    "CT": ("康涅狄格州", "Connecticut", "美东北", 30, 16, 0, "老房地下室翻修多", 5800, 750, 42, 4.0, "极高", "老旧改建融雪盐", 59, 26.0, ["CT Building Code", "UL 94"]),
    "DE": ("特拉华州", "Delaware", "美东", 9, 6, 0, "地下室/浅架空", 4600, 1200, 24, 5.5, "高", "海风盐雾", 41, 27.5, ["cUPC", "ASHRAE 70"]),
    "ID": ("爱达荷州", "Idaho", "美西北", 13, 8, 0, "深层地下室(85%+)", 6800, 550, 36, 8.0, "高", "寒冬冻融", 33, 29.0, ["MSS SP-58", "IPC 305.4"]),
    "IA": ("爱荷华州", "Iowa", "美中", 16, 15, 22, "全地下室占主流", 6700, 850, 48, 16.0, "极高", "重度融雪盐", 54, 28.0, ["Menards 质检认证", "UL 203"]),
    "KS": ("堪萨斯州", "Kansas", "美中", 18, 14, 9, "100%全地下室独立屋", 5000, 1350, 30, 13.5, "高", "龙卷风走廊风暴", 47, 28.5, ["FEMA P-361 避难室风压", "ASHRAE 70"]),
    "LA": ("路易斯安那州", "Louisiana", "美南", 28, 30, 0, "防洪高架柱/水泥平板", 1600, 2600, 0, 4.5, "极低", "飓风极度湿热内涝", 41, 21.5, ["HVHZ 沿海抗飓风", "cUPC 耐腐蚀"]),
    "ME": ("缅因州", "Maine", "美东北", 11, 10, 0, "传统石基与岩基地下室", 7800, 300, 54, 3.0, "极高", "沿海湿冷大雪", 53, 25.0, ["ASTM B117 盐雾 500h", "UL 94"]),
    "MD": ("马里兰州", "Maryland", "美东", 43, 30, 0, "联排镇屋/地下室", 4500, 1300, 24, 6.5, "高", "切萨皮克湾盐雾", 46, 28.0, ["cUPC", "MSS SP-58"]),
    "MA": ("马萨诸塞州", "Massachusetts", "美东北", 45, 29, 0, "老房水暖暖气片多", 5900, 700, 48, 3.5, "极高", "东北风暴近海大雪", 60, 26.5, ["MA State Plumbing Code", "UL 203"]),
    "MS": ("密西西比州", "Mississippi", "美南", 16, 22, 0, "浅架空层木屋", 2300, 2100, 0, 3.5, "极低", "极度闷热高湿", 39, 22.0, ["cUPC", "ASTM A153"]),
    "MT": ("蒙大拿州", "Montana", "美西北", 8, 5, 0, "防冻全地下室", 7900, 400, 54, 9.0, "高", "高寒深冻土", 45, 25.5, ["MSS SP-58", "极低温防脆裂测试"]),
    "NE": ("内布拉斯加州", "Nebraska", "美中", 11, 7, 10, "全地下室独立屋", 6200, 950, 42, 13.5, "极高", "暴风雪融雪盐", 49, 26.5, ["UL 203", "ASHRAE 70"]),
    "NV": ("内华达州", "Nevada", "美西", 21, 17, 0, "100%混凝土实心大平板(Slab)", 2800, 2600, 12, 18.0, "极低", "沙漠极端干旱酷热+极硬水", 28, 20.5, ["NSF 372 无铅涉水", "抗紫外线脆化"]),
    "NH": ("新罕布什尔州", "New Hampshire", "美东北", 17, 11, 0, "全地下室石基木屋", 7100, 450, 50, 2.5, "极高", "林区寒冬融雪盐", 48, 25.5, ["ASHRAE 70", "UL 94"]),
    "NJ": {"cn": "新泽西州", "name": "New Jersey", "reg": "美东北", "thd": 65, "low": 40, "men": 0, "fd_str": "紧凑型地下室老房", "hdd": 4900, "cdd": 1200, "fd": 30, "wh": 6.5, "sr": "极高", "haz": "密集融雪盐腐蚀", "age": 57, "v": 27.5, "certs": ["NJ State Uniform Code", "cUPC"]},
    "NM": {"cn": "新墨西哥州", "name": "New Mexico", "reg": "美西南", "thd": 17, "low": 13, "men": 0, "fd_str": "混凝土平板(Slab)为主", "hdd": 3800, "cdd": 1500, "fd": 18, "wh": 13.0, "sr": "低", "haz": "沙漠风沙强紫外线", "age": 36, "v": 22.5, "certs": ["NSF 372", "耐风沙磨蚀测试"]},
    "ND": {"cn": "北达科他州", "name": "North Dakota", "reg": "美中", "thd": 4, "low": 3, "men": 8, "fd_str": "防冻深层全地下室", "hdd": 9400, "cdd": 450, "fd": 66, "wh": 13.0, "sr": "极高", "haz": "全美最高HDD极寒", "age": 45, "v": 24.5, "certs": ["IPC 305.4 超深防冻", "MSS SP-58"]},
    "OK": {"cn": "俄克拉荷马州", "name": "Oklahoma", "reg": "美南", "thd": 21, "low": 24, "men": 0, "fd_str": "架空层与平板各半", "hdd": 3400, "cdd": 1900, "fd": 15, "wh": 11.5, "sr": "中", "haz": "龙卷风走廊风暴", "age": 40, "v": 26.0, "certs": ["FEMA P-361 避难室抗风压", "cUPC"]},
    "OR": {"cn": "俄勒冈州", "name": "Oregon", "reg": "美西北", "thd": 27, "low": 18, "men": 0, "fd_str": "架空层木结构(Crawl)", "hdd": 4600, "cdd": 400, "fd": 12, "wh": 2.0, "sr": "低", "haz": "常年阴雨高湿霉菌", "age": 43, "v": 26.5, "certs": ["OR Energy Code", "ASTM G154 防霉"]},
    "RI": {"cn": "罗德岛州", "name": "Rhode Island", "reg": "美东北", "thd": 7, "low": 5, "men": 0, "fd_str": "老房紧凑型地下室", "hdd": 5600, "cdd": 750, "fd": 40, "wh": 3.5, "sr": "极高", "haz": "海岸盐雾融雪盐", "age": 60, "v": 25.0, "certs": ["cUPC", "UL 94"]},
    "SD": {"cn": "南达科他州", "name": "South Dakota", "reg": "美中", "thd": 3, "low": 3, "men": 5, "fd_str": "防冻深层地下室", "hdd": 7600, "cdd": 700, "fd": 54, "wh": 16.5, "sr": "极高", "haz": "深冻土极寒", "age": 47, "v": 25.0, "certs": ["IPC 305.4", "UL 203"]},
    "UT": {"cn": "犹他州", "name": "Utah", "reg": "山地大区", "thd": 24, "low": 14, "men": 0, "fd_str": "大户型全地下室", "hdd": 5800, "cdd": 1050, "fd": 30, "wh": 17.5, "sr": "高", "haz": "大温差极硬水", "age": 32, "v": 25.5, "certs": ["NSF 372", "ASHRAE 70"]},
    "VT": {"cn": "佛蒙特州", "name": "Vermont", "reg": "美东北", "thd": 5, "low": 4, "men": 0, "fd_str": "全地下室山地木屋", "hdd": 7600, "cdd": 350, "fd": 54, "wh": 4.5, "sr": "极高", "haz": "漫长积雪严寒", "age": 51, "v": 24.5, "certs": ["VT Energy Code", "UL 94"]},
    "WY": {"cn": "怀俄明州", "name": "Wyoming", "reg": "山地大区", "thd": 5, "low": 3, "men": 2, "fd_str": "全地下室独栋", "hdd": 7500, "cdd": 350, "fd": 50, "wh": 11.0, "sr": "高", "haz": "极高海拔极寒狂风", "age": 42, "v": 23.5, "certs": ["MSS SP-58", "极温冲击测试"]}
}

for k, v in EXTRA_STATES_CONFIG.items():
    if k not in STATES_DATA:
        if isinstance(v, tuple):
            STATES_DATA[k] = {
                "cn": v[0], "name": v[1], "region": v[2], "thd": v[3], "lowes": v[4], "menards": v[5],
                "dc": "大区核心集散仓", "foundation": v[6], "climate": "Zone 4A/5A 大陆季风", "flooring": "实木 40%, LVP 35%, 瓷砖 15%, 地毯 10%",
                "best": "威霖标准化出风口、装配式槽钢支架", "avoid": "非标冷门异形件",
                "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)",
                "channel_advice": "按大区 RDC 配送中心整托调拨备货，保持安全周转天数即可。",
                "hdd": v[7], "cdd": v[8], "frost_depth": v[9], "water_hardness": v[10], "salt_risk": v[11],
                "hazard": v[12], "house_age": v[13], "hazard_idx": 5, "base_vel": v[14], "state_certs": v[15]
            }
        else:
            STATES_DATA[k] = {
                "cn": v["cn"], "name": v["name"], "region": v["reg"], "thd": v["thd"], "lowes": v["low"], "menards": v["men"],
                "dc": "大区核心集散仓", "foundation": v["fd_str"], "climate": "Zone 4A/5A 大陆季风", "flooring": "实木 40%, LVP 35%, 瓷砖 15%, 地毯 10%",
                "best": "威霖标准化出风口、装配式槽钢支架", "avoid": "非标冷门异形件",
                "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)",
                "channel_advice": "按大区 RDC 配送中心整托调拨备货，保持安全周转天数即可。",
                "hdd": v["hdd"], "cdd": v["cdd"], "frost_depth": v["fd"], "water_hardness": v["wh"], "salt_risk": v["sr"],
                "hazard": v["haz"], "house_age": v["age"], "hazard_idx": 5, "base_vel": v["v"], "state_certs": v["certs"]
            }

df_states_raw = pd.DataFrame.from_dict(STATES_DATA, orient="index")
df_states_raw["total_stores"] = df_states_raw["thd"] + df_states_raw["lowes"] + df_states_raw["menards"]
ALL_REGIONS = ["全部大区 (All Regions)"] + sorted(list(set(df_states_raw["region"].tolist())))

# ==============================================================================
# 5. 顶层控制器（大区、节令、渠道与四维属性）
# ==============================================================================
st.markdown('<div class="main-title">🏭 宁波威霖住宅设施 · 北美大零售销售决策系统</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">完整涵盖【威霖产线对标 + 全美50州地基与8大物理特征 + Big 3 门店网络 + 州级出口认证清单 + 买手核价到岸财务】</div>', unsafe_allow_html=True)

col_cat, col_region, col_season, col_channel = st.columns([1.3, 0.9, 1.0, 1.1])

with col_cat:
    selected_cat_key = st.selectbox("1. 威霖目标产线 (Category)：", list(CATEGORY_CONFIG.keys()), format_func=lambda x: CATEGORY_CONFIG[x]["name"])
    cat_cfg = CATEGORY_CONFIG[selected_cat_key]

with col_region:
    selected_region = st.selectbox("2. 目标地理大区 (Region Filter)：", ALL_REGIONS, index=0)

with col_season:
    selected_season = st.selectbox("3. 规划出货节令 (Seasonality Pulse)：", [
        "Q1 春季复苏与翻新热潮 (Spring Refresh: 3-5月)",
        "Q2 夏季空调制冷高峰 (Peak Cooling: 6-8月)",
        "Q3 入冬防寒整备爆发季 (Fall Weatherization: 9-11月)",
        "Q4 深冬极寒与防冻抢修 (Freeze Defense: 12-2月)",
        "全年平销基准期 (Annual Baseline)"
    ], index=2)

with col_channel:
    selected_channel = st.selectbox("4. 目标商超零售渠道：", [
        "全部渠道综合总盘 (THD + Lowe's + Menards)",
        "The Home Depot (承包商Pro工匠第一)",
        "Lowe's (家庭DIY与软装换新偏好)",
        "Menards (中西部大区独立专营)"
    ], index=0)

# 动态绑定唯一定位键，彻底规避 Streamlit 下拉框幽灵状态冲突
st.markdown("#### 🎯 威霖制造属性与规格配置")
f1, f2, f3, f4 = st.columns(4)

with f1:
    pos_opts = ["(全部位置 / All)"] + cat_cfg["positions"]
    sel_pos_raw = st.selectbox("1. 安装位置 (Position)：", pos_opts, index=1, key=f"{selected_cat_key}_pos")
    sel_pos = sel_pos_raw.split(" ")[0]

with f2:
    mat_opts = ["(全部材质 / All)"] + cat_cfg["materials"]
    sel_mat_raw = st.selectbox("2. 生产原材料 (Material)：", mat_opts, index=0, key=f"{selected_cat_key}_mat")
    sel_mat = sel_mat_raw.split(" ")[0]

with f3:
    fin_opts = ["(全部工艺 / All)"] + cat_cfg["finishes"]
    sel_fin_raw = st.selectbox("3. 表面工艺与颜色 (Finish)：", fin_opts, index=0, key=f"{selected_cat_key}_fin")
    sel_fin = sel_fin_raw.split(" ")[0]

with f4:
    size_opts = ["(全部尺寸 / All)"] + cat_cfg["sizes"]
    sel_size_raw = st.selectbox("4. 规格尺寸 (Size)：", size_opts, index=1, key=f"{selected_cat_key}_size")
    sel_size = sel_size_raw.split(" ")[0]

# ==============================================================================
# 6. 计算引擎（彻底支持“(全选)”模式，杜绝假死）
# ==============================================================================
calc_rows = []

for abbr, s in STATES_DATA.items():
    base_v = s["base_vel"]
    weight = 1.0
    reasons = []
    
    # 1. 地基与安装位置逻辑 (全面支持全选与单选)
    if selected_cat_key == "HVAC":
        if sel_pos == "Floor":
            if "地下室" in s["foundation"] or "架空" in s["foundation"]:
                weight *= 1.25
                reasons.append("全地下室主场，暖气自地面向上自然对流刚需")
            elif "平板" in s["foundation"] or abbr in ["FL", "TX", "AZ", "NV", "HI", "LA"]:
                weight *= 0.12
                reasons.append("实心水泥大平板地基，地面无管道，严禁推地板出风口")
        elif sel_pos == "Ceiling":
            if s["cdd"] >= 2000 or abbr in ["FL", "TX", "AZ", "NV", "CA", "GA", "HI"]:
                weight *= 2.6
                reasons.append(f"长夏酷暑阳光带(CDD={s['cdd']:,})，天花散流器下吹冷气是全美标准")
            elif s["hdd"] >= 6000:
                weight *= 0.5
                reasons.append("北方极寒雪带一层以地面采暖为主，天花风口占比低")
        elif sel_pos == "Baseboard":
            if s["house_age"] >= 50 or abbr in ["PA", "NY", "MA", "CT", "OH", "NJ"]:
                weight *= 1.9
                reasons.append("老宅水暖踢脚线与狭窄缝隙换新改装需求极高")
        elif sel_pos.startswith("(全部"):
            if "地下室" in s["foundation"] and s["hdd"] >= 4000:
                weight *= 1.15
                reasons.append("采暖大区综合需求旺盛，地面与踢脚线出风口均衡出货")

    elif selected_cat_key == "PLUMBING":
        if "Linear" in sel_pos or "Tile-in" in sel_pos:
            if abbr in ["FL", "CA", "TX", "NC", "SC", "GA", "AZ"]:
                weight *= 2.2
                reasons.append("现代无门槛大板淋浴房(Curbless Walk-in)改装爆发，威霖隐形地漏畅销")
        elif "Frost" in sel_pos:
            if s["frost_depth"] >= 36:
                weight *= 3.2
                reasons.append(f"冻土层深达 {s['frost_depth']} 寸，威霖超长防冻水阀是防爆管刚需")
            elif s["frost_depth"] == 0:
                weight *= 0.05
                reasons.append("常年无霜冻，室外防冻阀几乎零需求")

    elif selected_cat_key == "HANGERS":
        if "Strut" in sel_pos or "Seismic" in sel_pos:
            if abbr in ["CA", "WA", "OR", "UT", "AK"]:
                weight *= 2.8
                reasons.append("处于高烈度地震带，威霖装配式槽钢与抗震支架属于建筑强制验收项")
            elif s["house_age"] <= 35:
                weight *= 1.4
                reasons.append("商业建筑与新房开工活跃，管道吊架大宗需求强劲")

    elif selected_cat_key == "SHOWER_HARDWARE":
        if "Hinge" in sel_pos:
            if abbr in ["FL", "CA", "TX", "AZ", "NC"]:
                weight *= 1.8
                reasons.append("精装无框玻璃淋浴房普及率全美领先，威霖重载铰链走货极快")
        elif "Sweep" in sel_pos:
            if s["hdd"] >= 5500:
                weight *= 2.0
                reasons.append("北方寒冬门底防冷风倒灌，节能降电费刚需")
        elif "Hurricane" in sel_pos:
            if abbr in ["FL", "NC", "SC", "TX", "LA", "HI"]:
                weight *= 3.5
                reasons.append("大西洋与海岛飓风带(HVHZ法规)强制要求高强度防风加固角码")

    elif selected_cat_key == "OUTDOOR_DRAIN":
        if "Trench" in sel_pos:
            if s["cdd"] >= 1800 or "暴雨" in s["hazard"] or "飓风" in s["hazard"]:
                weight *= 2.4
                reasons.append("热带强降雨及多泳池庭院普及，车道防内涝倒灌依赖线性深沟")

    # 2. 融雪盐与水质硬度物理微调
    if s["salt_risk"] in ["高", "极高"]:
        if sel_mat in ["Steel", "Carbon"]:
            weight *= 0.8
            reasons.append("⚠️ 融雪盐鞋底腐蚀严重，普通碳钢有生锈索赔隐患")
        elif sel_mat in ["Aluminum", "Stainless", "Hot-Dip"]:
            weight *= 1.25
            reasons.append("✅ 阳极氧化铝/热镀锌耐融雪盐侵蚀，大湖雪带好评度高")

    if s["water_hardness"] >= 13.0 and selected_cat_key == "PLUMBING":
        if sel_fin == "CP":
            weight *= 0.85
            reasons.append("⚠️ 极重度硬水，抛光亮铬表面极易结顽固白斑水垢")
        elif sel_fin in ["BN", "MB", "BG"]:
            weight *= 1.25
            reasons.append("✅ 拉丝镍/PVD工艺在硬水区抗水垢残留表现优异")

    # 3. 房龄加权
    if s["house_age"] >= 50:
        weight *= 1.2
        reasons.append(f"中位房龄达 {s['house_age']} 年，老旧建筑二次翻新动销活跃")

    # 4. 季节节令脉冲加权
    if "Q3" in selected_season:
        if selected_cat_key in ["SHOWER_HARDWARE", "HVAC"]:
            weight *= 1.4
            reasons.append("🍂 处于入冬防寒整备季（Fall Weatherization），销量脉冲式激增")
    elif "Q2" in selected_season:
        if selected_cat_key == "HVAC" and sel_pos == "Ceiling":
            weight *= 1.7
            reasons.append("☀️ 酷暑制冷峰值，天花散流器换新需求强劲")
    elif "Q4" in selected_season:
        if selected_cat_key == "PLUMBING" and "Frost" in sel_pos:
            weight *= 2.2
            reasons.append("❄️ 极寒深度冰封，爆管抢修更换进入最高峰")

    # 5. 走量规格加成
    if sel_size in ["04X10", "36", "4x4", "39", "1-5/8"]:
        weight *= 1.15

    # 渠道有效门店过滤
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
    
    tier_str = "Tier 1 (S级核心)" if calc_vel >= 38.0 else ("Tier 2 (A级主力)" if calc_vel >= 26.0 else ("Tier 3 (B级走量)" if calc_vel >= 14.0 else "Tier 4 (受限/避坑)"))
    pog = "🔥 双排面 (Double, 24寸)" if calc_vel >= 35.0 else ("✅ 单排面 (Single, 12寸)" if calc_vel >= 15.0 else "⚠️ 底层冷门位")

    row_data = dict(s)
    row_data["abbr"] = abbr
    row_data["calc_vel"] = calc_vel
    row_data["calc_tot"] = calc_tot
    row_data["active_stores"] = active_stores
    row_data["tier"] = tier_str
    row_data["pog"] = pog
    row_data["calc_rev_msrp"] = calc_tot * retail_msrp
    row_data["calc_fob_tot"] = calc_tot * fob_cost
    row_data["reason_desc"] = "；".join(reasons) if reasons else "符合常规分销基线"
    calc_rows.append(row_data)

df_all = pd.DataFrame(calc_rows)

# 执行大区筛选
if selected_region != "全部大区 (All Regions)":
    df_res = df_all[df_all["region"] == selected_region].copy()
else:
    df_res = df_all.copy()

df_res["rank_vel"] = df_res["calc_vel"].rank(ascending=False, method="min").astype(int)
df_res["rank_tot"] = df_res["calc_tot"].rank(ascending=False, method="min").astype(int)

# 统一排序表供全局调用
df_sorted = df_res.sort_values("calc_tot", ascending=False).reset_index(drop=True)
df_sorted["序号"] = df_sorted.index + 1

# ==============================================================================
# 7. 全网大卡片看板 (KPI Dashboard)
# ==============================================================================
st.markdown("---")
sum_stores = int(df_res["active_stores"].sum())
sum_units = int(df_res["calc_tot"].sum())
top_v_row = df_res.sort_values("calc_vel", ascending=False).iloc[0]
top_t_row = df_res.sort_values("calc_tot", ascending=False).iloc[0]

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">当前筛选·有效商超总店数</div>
        <div class="kpi-val">{sum_stores:,} 家</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">威霖出海月总销量预估</div>
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
# 8. 四大功能 Tab 呈现
# ==============================================================================
tab_rank, tab_detail, tab_chart, tab_supply = st.tabs([
    "📋 全美各州零售排行看板", 
    "🔍 威霖单州深度透视与出口认证清单", 
    "📊 Big 3 零售巨头渠道吞吐量图表", 
    "🚚 供应链港口物流、打托与商超标准"
])

# ----------------- TAB 1: 排行榜看板 -----------------
with tab_rank:
    view_mode = st.radio(
        "切换主排序依据：", 
        ["全州渠道总吞吐量 (件/月) - 适于威霖工厂海运整柜排产", "单店平均销售流速 (件/店/月) - 适于商超平效谈判与货架位申请"], 
        horizontal=True
    )
    
    if "单店" in view_mode:
        df_display = df_res.sort_values("rank_vel", ascending=True).reset_index(drop=True)
    else:
        df_display = df_res.sort_values("rank_tot", ascending=True).reset_index(drop=True)
    df_display["序号"] = df_display.index + 1
    
    max_vel_val = max(int(df_res["calc_vel"].max()), 1)
    
    st.dataframe(
        df_display[[
            "序号", "abbr", "cn", "region", "tier", "calc_vel", "calc_tot", "calc_rev_msrp",
            "active_stores", "house_age", "pog", "foundation"
        ]],
        use_container_width=True,
        column_config={
            "序号": st.column_config.NumberColumn(width=45),
            "abbr": st.column_config.TextColumn("简称", width=55),
            "cn": st.column_config.TextColumn("州全称", width=95),
            "region": st.column_config.TextColumn("大区", width=80),
            "tier": st.column_config.TextColumn("战略梯队", width=110),
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

# ----------------- TAB 2: 单州深度透视与认证清单 -----------------
with tab_detail:
    st.markdown("### 🔎 威霖对标：州级商业基底、物理气象与全美出口认证清单")
    
    # 增加严格的越界保护
    state_list = df_sorted["abbr"].tolist()
    target_abbr = st.selectbox("请选择要深度穿透剖析的目标州：", state_list, index=0)
    cur = df_sorted[df_sorted["abbr"] == target_abbr].iloc[0]
    
    c_info1, c_info2 = st.columns([1.1, 1.1])
    
    with c_info1:
        st.markdown(f"### 📍 {cur['cn']} ({cur['abbr']}) · {cur['region']} · `{cur['tier']}`")
        m_a, m_b = st.columns(2)
        with m_a:
            st.metric("预估单店流速", f"{cur['calc_vel']:.1f} 件/店/月", f"当前榜单排名: #{cur['rank_vel']}")
        with m_b:
            st.metric("该州月总需求", f"{cur['calc_tot']:,} 件/月", f"当前榜单排名: #{cur['rank_tot']}")
            
        st.info(f"**💡 算法与气候地基综合归因**：\n{cur['reason_desc']}")
        st.write(f"**🏠 房屋基底形态**：{cur['foundation']}")
        st.write(f"**🪵 地面材质偏好**：{cur['flooring']}")
        st.write(f"**🏬 区域门店网络**：THD: **{cur['thd']}** 家 | Lowe's: **{cur['lowes']}** 家 | Menards: **{cur['menards']}** 家 (有效覆盖: {cur['active_stores']} 家)")
        st.write(f"**📦 POG 货架位策略**：**{cur['pog']}**")
        st.success(f"**✅ 当地威霖对标主推品**：{cur['best']}")
        st.warning(f"**⚠️ 当地谨慎进入品**：{cur['avoid']}")
        
        st.markdown(f"""
        <div class="advice-box">
            <b>📐 该州当地规格销售配比 (威霖外销装箱比例依据)：</b><br>
            {cur['size_breakdown']}<br><br>
            <b>💼 威霖外贸业务与商超渠道实战建议：</b><br>
            {cur['channel_advice']}
        </div>
        """, unsafe_allow_html=True)

    with c_info2:
        st.markdown(f"""
        <div class="physics-card">
            <b>🌡️ 气候物理实测与建筑工程参数</b><br>
            • 采暖度日 (HDD): <b>{cur['hdd']:,}</b> | 制冷度日 (CDD): <b>{cur['cdd']:,}</b><br>
            • 房屋中位房龄: <b>{cur['house_age']} 年</b> {'(⚠️ 50年以上老宅区，老规格翻新是绝对主力)' if cur['house_age']>=50 else ''}<br>
            • 法定冻土深度: <b>{cur['frost_depth']} 英寸</b> {'(⚠️ 极深冻土，室外水阀必须≥10~12寸)' if cur['frost_depth']>=36 else ''}<br>
            • 水质硬度: <b>{cur['water_hardness']} GPG</b> {'(⚠️ 极重度硬水，抛光亮铬易结垢)' if cur['water_hardness']>=13 else ''}<br>
            • 融雪盐腐蚀风险: <b>{cur['salt_risk']}</b> {'(⚠️ 严禁普通冷轧铁裸露)' if cur['salt_risk'] in ['高','极高'] else ''}<br>
            • 极端自然灾害标签: <span class="badge-tier4">{cur['hazard']} (灾害指数: {cur['hazard_idx']}/10)</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 🌟 重点扩充：标注出口该州必须通过的认证体系
        st.markdown("#### 📜 威霖产品出口该州必查认证清单 (Certifications)")
        
        st.markdown("**1. 全美联邦通用强制认证 (National Baseline)：**")
        for n_cert in cat_cfg["national_certs"]:
            st.markdown(f'<span class="cert-badge">🏛️ {n_cert}</span>', unsafe_allow_html=True)
            
        st.markdown("**2. 该州/地方特有强制作法典与法规认证 (State Redlines)：**")
        for s_cert in cur["state_certs"]:
            st.markdown(f'<span class="cert-badge" style="background:#fee2e2;color:#991b1b;border-color:#fca5a5;">🔴 {s_cert}</span>', unsafe_allow_html=True)

        st.markdown('<div class="radar-box">', unsafe_allow_html=True)
        st.markdown("**🛡️ 威霖合规合规风控提醒：**")
        if target_abbr == "CA":
            st.markdown("• **加州 Prop 65** 铅迁移量与邻苯二甲酸酯检测报告必须齐全，外箱及内盒必须加印警告贴标。")
            st.markdown("• 若推抗震支吊架，须具备 **HCAI / OSHPD** 认证；若推外墙出风口，必须满足 **WUI** 1/8 英寸防飞烬要求。")
        elif target_abbr in ["FL", "TX"]:
            st.markdown("• 门窗五金与户外构件若进入沿海飓风县，必须通过 **Miami-Dade NOA / TDI** 风暴冲击检验。")
        elif cur["frost_depth"] >= 36 and selected_cat_key == "PLUMBING":
            st.markdown(f"• 依据 **IPC 规范**，当地冻土达 {cur['frost_depth']} 寸，水暖买手一票否决常规短水龙头，必须供 8~12 寸长杆阀。")
        else:
            st.markdown("• 满足 cUPC / ASHRAE / UL / MSS 基础标准即可，无特殊极端地方贸易禁令。")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 3: 零售巨头渠道图表 -----------------
with tab_chart:
    st.markdown("#### 📊 当前筛选区域内 Top 15 吞吐量大州 Big 3 零售渠道出货结构")
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
        reg_summary = df_all.groupby("region").agg({
            "abbr": "count", "active_stores": "sum", "calc_tot": "sum", "calc_vel": "mean"
        }).reset_index()
        reg_summary.columns = ["大区", "州数", "总门店", "月度总盘(件)", "区均流速"]
        reg_summary["建议配货比例"] = (reg_summary["月度总盘(件)"] / reg_summary["月度总盘(件)"].sum() * 100).round(1).astype(str) + "%"
        reg_summary["区均流速"] = reg_summary["区均流速"].round(1)
        st.dataframe(reg_summary, use_container_width=True, hide_index=True)
        
    with s_col2:
        st.markdown("##### 2. 客群画像与 GMA 打托包装建议")
        
        if "Cast" in sel_mat or "Hot-Dip" in sel_mat or "Carbon" in sel_mat:
            diy_p, pro_p = 20, 80
            pkg_rec = "Contractor Pack (10-20件无印刷牛皮纸工程包装)"
            ret_rate = "1.5% ~ 2.0% (极低退货率)"
        elif "Plastic" in sel_mat or "WH" in sel_fin:
            diy_p, pro_p = 75, 25
            pkg_rec = "彩色挂卡 / 气泡热缩膜 (配安装螺丝与 1:1 测量卡纸)"
            ret_rate = "4.5% ~ 6.0% (中高退货率)"
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
    "序号", "abbr", "cn", "name", "region", "tier", "calc_vel", "calc_tot", "calc_rev_msrp",
    "calc_fob_tot", "active_stores", "pog", "foundation", "flooring", "best", "avoid",
    "size_breakdown", "channel_advice", "hdd", "cdd", "frost_depth", "water_hardness",
    "salt_risk", "house_age", "hazard", "state_certs", "reason_desc"
]].to_csv(index=False).encode('utf-8-sig')

st.download_button(
    label=f"📥 导出【{cat_cfg['name'].split(' ')[0]}】({selected_region}) 威霖完整商业决策报表 (.csv)",
    data=csv_out,
    file_name=f"Ningbo_Runner_Retail_Decision_{selected_cat_key}_{selected_region[:3]}.csv",
    mime="text/csv"
)
