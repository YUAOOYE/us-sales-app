import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 1. 页面配置与现代化高管 BI 科技蓝视觉规范
# ==============================================================================
st.set_page_config(
    page_title="宁波威霖住宅设施 · 北美大零售商业与工程决策系统",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* 全局 Slate 商务背景 */
    .stApp { background-color: #F8FAFC; color: #0F172A; }
    
    /* 顶部标题区 */
    .bi-header {
        background: white;
        padding: 16px 22px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .main-title { font-size: 1.55rem; font-weight: 700; color: #0F172A; margin-bottom: 4px; }
    .sub-title { font-size: 0.86rem; color: #475569; }
    
    /* 核心 KPI 卡片 */
    .kpi-card {
        background: linear-gradient(135deg, #1E40AF, #2563EB);
        color: white;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }
    .kpi-title { font-size: 0.82rem; opacity: 0.92; margin-bottom: 2px; font-weight: 500; }
    .kpi-val { font-size: 1.55rem; font-weight: 700; }
    
    /* 自适应高度卡片容器 (彻底根除截断) */
    .section-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 18px;
        margin-bottom: 12px;
        height: auto !important;
        min-height: fit-content;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        word-wrap: break-word;
    }
    
    /* 竞品对标专属卡片 (自适应撑开) */
    .competitor-card {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #64748B;
        border-radius: 6px;
        padding: 14px 16px;
        margin-bottom: 10px;
        height: auto !important;
        line-height: 1.6;
    }
    .willi-card {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-left: 4px solid #2563EB;
        border-radius: 6px;
        padding: 14px 16px;
        margin-bottom: 10px;
        height: auto !important;
        line-height: 1.6;
    }
    
    /* 徽章 Badge 体系 */
    .badge-tier1 { background-color: #DCFCE7; color: #166534; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier2 { background-color: #DBEAFE; color: #1E40AF; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier3 { background-color: #FEF3C7; color: #92400E; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier4 { background-color: #FEE2E2; color: #991B1B; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    
    .cert-pill { background-color: #F1F5F9; border: 1px solid #CBD5E1; color: #334155; padding: 3px 8px; border-radius: 4px; font-size: 0.78rem; margin-right: 4px; margin-bottom: 6px; display: inline-block; }
    .cert-pill-red { background-color: #FEF2F2; border: 1px solid #FCA5A5; color: #991B1B; padding: 3px 8px; border-radius: 4px; font-size: 0.78rem; margin-right: 4px; margin-bottom: 6px; display: inline-block; }
    
    .radar-box { border-left: 4px solid #EF4444; background-color: #FEF2F2; padding: 12px 16px; border-radius: 0 6px 6px 0; margin-top: 10px; }
    .advice-box { border-left: 4px solid #3B82F6; background-color: #EFF6FF; padding: 12px 16px; border-radius: 0 6px 6px 0; margin-top: 10px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. 侧边栏：威霖外贸买手财务核算器
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/factory.png", width=46)
    st.markdown("### 💰 威霖到岸财务与毛利试算")
    st.caption("宁波威霖住宅设施有限公司 (建霖家居 603408)")
    st.markdown("---")
    
    fob_cost = st.number_input("1. 威霖出厂供货价 FOB ($/件)：", min_value=0.5, max_value=200.0, value=3.80, step=0.2)
    ocean_freight = st.number_input("2. 单件美线分摊海运费 ($/件)：", min_value=0.0, max_value=50.0, value=0.65, step=0.05)
    tariff_pct = st.number_input("3. 关税税率 Tariff (%)：", min_value=0.0, max_value=100.0, value=7.5, step=0.5) / 100.0
    retail_msrp = st.number_input("4. 北美商超零售价 MSRP ($/件)：", min_value=1.0, max_value=500.0, value=12.98, step=0.5)
    case_pack = st.number_input("5. 标准箱装数 (Case Pack)：", min_value=1, max_value=100, value=10, step=1)
    
    landed_cost = fob_cost * (1 + tariff_pct) + ocean_freight
    buyer_margin = ((retail_msrp - landed_cost) / retail_msrp) * 100
    gross_profit_unit = retail_msrp - landed_cost
    
    st.markdown(f"""
    <div style='background:white;padding:12px 14px;border-radius:6px;border:1px solid #E2E8F0;'>
        <span style='font-size:0.82rem;color:#64748B;'>到岸完税成本 (Landed DDP)</span><br>
        <b style='font-size:1.25rem;color:#0F172A;'>${landed_cost:.2f}</b><br><br>
        <span style='font-size:0.82rem;color:#64748B;'>商超零售净毛利率 (Buyer Margin)</span><br>
        <b style='font-size:1.25rem;color:{'#166534' if buyer_margin>=42 else '#991B1B'};'>{buyer_margin:.1f}%</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("🏭 **威霖象山工业园制造能力标签**：\n• 14 万平米智能制造基地\n• 绿色环保PVD镀膜中心\n• 自动化连续冲压/精密注塑\n• cUPC / UL 认证目击实验室")

# ==============================================================================
# 3. 品类与竞品对家深度知识库（威霖产线完全对齐）
# ==============================================================================
CATEGORY_CONFIG = {
    "HVAC": {
        "name": "暖通风口与空气分配系统 (Registers & Grilles)",
        "willi_fit": "威霖主力核心板块：冲压冷轧钢、阳极氧化铝、压铸锌合金复古雕花、工程阻燃ABS出风口全系列。",
        "competitors": {
            "main_rival": "Accord Ventilation (全美风口第一品牌) / Deflecto (工程塑料霸主)",
            "shelf_share": "约 60% 黄金通道排面垄断",
            "rival_msrp": "$13.98 (高于威霖预估价)",
            "rival_margin": "38% ~ 42% (给买手留存毛利薄)",
            "rival_weakness": "传统冲压钢易生锈磕碰，缺少 PVD 和 AF 纳米防指纹等高端工艺，耐盐雾能力一般。",
            "willi_tactic": "以高质感阳极氧化铝与 PVD 哑光黑打高端改善型，给商超买手留出 52%+ 净毛利，以更高利润换取双排面陈列。"
        },
        "positions": ["Floor (地面出风口)", "Ceiling (天花板散流器)", "Baseboard (踢脚线出风口)", "Sidewall (侧墙回风格栅)"],
        "materials": ["Steel (冲压冷轧钢)", "Aluminum (铝合金阳极氧化)", "Plastic (ABS阻燃树脂)", "Cast Metal (铸铝/铸铁重载)", "Engineered Wood (多层实木复合-抗翘曲)", "Zinc Die-Cast (压铸锌合金雕花)"],
        "finishes": ["Matte Black (US19 哑光黑)", "Brushed Nickel (US15 拉丝镍)", "Glossy White (经典工程白)", "Oil Rubbed Bronze (US10B 油磨青铜)", "PVD Brushed Gold (轻奢拉丝金)", "AF Nano-Coating (纳米防指纹黑)", "Wood Grain Transfer (3D热转印木纹)"],
        "sizes": ["04X10 (全美走量王 65%)", "04X12 (主流换新大号 20%)", "02X12 (踢脚狭长缝 10%)", "06X10 (大排风量 5%)", "12X12 (天花方型大尺寸)"],
        "national_certs": ["ASHRAE Standard 70 (风量CFM与噪音NC评级测试)", "UL 94 (阻燃塑料V-0级认证)", "Heel-Proof (细高跟鞋防卡穿透安全测试)"]
    },
    "PLUMBING": {
        "name": "卫浴排水与长条隐形地漏 (Drains & Plumbing)",
        "willi_fit": "威霖主力核心板块：不锈钢冲压拉伸、长条隐形线性地漏、防臭下水器、防冻长水阀全系列。",
        "competitors": {
            "main_rival": "Oatey (全美水暖耗材统治级巨头) / Sioux Chief (本土工匠龙头)",
            "shelf_share": "约 65% 水暖通道排面垄断",
            "rival_msrp": "$49.99 (长条地漏) / $11.50 (点状地漏)",
            "rival_margin": "40% ~ 44%",
            "rival_weakness": "款式传统偏向单面格栅，较少配备当前流行的 Tile-in 瓷砖隐形双面翻转结构。",
            "willi_tactic": "推出 Tile-in 2合1 隐形面板（一面拉丝格栅，反面内嵌瓷砖），1个SKU满足两种装修风格，替买手省货架并降低备货风险。"
        },
        "positions": ["Linear Drain (长条隐形地漏)", "Tile-in Drain (2合1瓷砖隐形地漏)", "Floor Drain (方形点状地漏)", "Frost-Proof Valve (室外防冻长水阀)"],
        "materials": ["Stainless 304 (304拉丝不锈钢)", "Stainless 316 (316耐氯盐雾级)", "Solid Brass (无铅锻压黄铜)", "ABS/PVC (耐腐工程塑料)"],
        "finishes": ["Brushed Stainless (不锈钢拉丝)", "Matte Black (现代哑光黑)", "Polished Chrome (亮铬镜面)", "PVD Brushed Gold (PVD防磨金)"],
        "sizes": ["24-36 inch (长条隐形主力)", "4x4 inch (标准方形)", "1/2 inch (常规供水接口)", "3/4 inch (主水管接口)"],
        "national_certs": ["cUPC 认证 (IAPMO 强制排水与管件证书)", "ASME A112.18.2 / CSA B125.2 (通量试验)", "NSF/ANSI 61 & 372 (接触饮用水无铅涉水认证)"]
    },
    "HANGERS": {
        "name": "管道支吊架与抗震支撑系统 (Support & Hanger Systems)",
        "willi_fit": "威霖工程王牌业务：建筑管道吊卡、C型装配式槽钢构件、抗震紧固件、商用管道支撑。",
        "competitors": {
            "main_rival": "Superstrut (Thomas & Betts / ABB) / Unistrut (Atkore) / Erico (nVent CADDY)",
            "shelf_share": "约 70% 商用电气与管道五金排面垄断",
            "rival_msrp": "$18.50 (10尺槽钢) / $2.80 (2寸管卡)",
            "rival_margin": "35% ~ 38% (对家品牌溢价高，买手利薄)",
            "rival_weakness": "重型热浸镀锌件售价高昂；对家缺乏柔性冲压组件的快速定制配套能力。",
            "willi_tactic": "依托象山工业园连续冲压与热浸镀锌/达克罗能力，以商超自有品牌 (Store Brand) 切入，提供高毛利全套配件组合包。"
        },
        "positions": ["Strut Channel (C型装配式槽钢)", "Pipe Clamp (管道固定卡箍)", "Seismic Hanger (抗震斜撑加固组件)", "Beam Clamp (工字钢梁夹连接件)"],
        "materials": ["Carbon Steel (重载碳钢)", "Hot-Dip Galvanized Steel (热浸镀锌结构钢)", "Stainless 304 (不锈钢防腐型)", "Ductile Iron (球墨铸铁梁夹)"],
        "finishes": ["Clear Zinc (EG 冷电镀蓝白锌)", "Yellow Zinc (环保三价铬彩锌)", "Hot-Dip Galvanized (HDG 重型热浸镀锌)", "Dacromet (达克罗防腐涂层)", "Black E-Coating (阴极电泳黑)"],
        "sizes": ["1-5/8 inch (全美标准重载槽钢)", "13/16 inch (轻型槽深)", "1/2-2 inch (中小管径卡箍)", "3-6 inch (重载立管卡)"],
        "national_certs": ["MSS SP-58 (全美管道吊架设计制造通用标准)", "UL 203 (消防喷淋管道吊架强制认证)", "FM 1951 (抗震支撑组件认证)"]
    },
    "SHOWER_HARDWARE": {
        "name": "淋浴门与门窗五金构件 (Shower Door & Enclosures)",
        "willi_fit": "威霖优势产线：无框淋浴房精铸铰链、滚轮导轨、门底密封防风条、抗风暴加固角码。",
        "competitors": {
            "main_rival": "DreamLine (北美淋浴房零售霸主) / CRL (C.R. Laurence 玻璃工匠标杆) / Simpson Strong-Tie",
            "shelf_share": "展厅专区垄断",
            "rival_msrp": "$45.00 (精铸铰链) / $22.00 (门底扫风条)",
            "rival_margin": "42% ~ 45%",
            "rival_weakness": "对家零散配件单价极贵，缺乏面向 DIY 和工匠成套拿取的综合五金包。",
            "willi_tactic": "提供精铸无铅黄铜+无铅认证铰链，搭配 EPDM 耐候发泡门底密封条做套件包，主打零生锈与终身顺滑质保。"
        },
        "positions": ["Shower Hinge (无框玻璃重型合页)", "Door Sweep (门底防风挡水密封条)", "Hurricane Tie (建筑抗飓风加固角码)", "Heavy Duty Hinge (重载大门合页)"],
        "materials": ["Solid Brass (精铸无铅纯铜)", "Stainless 304 (304防锈不锈钢)", "Aluminum + EPDM (铝合金+耐候EPDM橡胶)", "Hot-Dip Galvanized Steel (热浸镀锌结构钢)"],
        "finishes": ["Matte Black (US19 哑光黑)", "Brushed Nickel (US15 缎面拉丝镍)", "Bright Chrome (US26 抛光亮铬)", "PVD Brushed Brass (US4 耐磨金)"],
        "sizes": ["36 inch (单门标准长)", "42 inch (大入户门底条)", "4x4 inch (重载大门合页)", "50 ft Roll (50英尺整卷工程条)"],
        "national_certs": ["ANSI/BHMA A156.1 (100万次开合疲劳测试)", "ANSI Z97.1 / CPSC 16 CFR 1201 (安全玻璃与五金承重标准)", "UL 10C (90分钟正压防火门认证)"]
    },
    "OUTDOOR_DRAIN": {
        "name": "户外排水与景观系统 (Outdoor Drainage & Grates)",
        "willi_fit": "威霖延伸产线：车道线性排水槽、重载钢格栅、防落叶天沟滤网、外墙通风百叶罩。",
        "competitors": {
            "main_rival": "NDS (全美住宅与商业雨水排水龙头) / ACO (高端聚合物排水沟标杆)",
            "shelf_share": "园艺与建材区 75% 排面垄断",
            "rival_msrp": "$38.00 (1米塑料沟槽带格栅)",
            "rival_margin": "45% ~ 48%",
            "rival_weakness": "对家主打普通塑料格栅，车压易破碎；重载铸铁与热镀锌盖板售价过高。",
            "willi_tactic": "主打热浸镀锌重钢格栅与耐暴晒 HDPE 沟体，以汽车级 C250 承重等级降维打击普通塑料款。"
        },
        "positions": ["Trench Drain (车道线性排水沟)", "Gutter Guard (天沟防落叶过滤网)", "Post Anchor (木露台立柱固定底座)", "Outdoor Vent (外墙防风雨冲压百叶)"],
        "materials": ["Polymer/HDPE (耐暴晒重型工程塑料)", "Hot-Dip Galvanized Steel (热浸镀锌重钢格栅)", "Ductile Cast Iron (球墨铸铁重载盖板)", "Cast Aluminum (耐候防腐铸铝)"],
        "finishes": ["Galvanized Silver (热镀锌亮银)", "Black Asphalt (沥青防腐黑)", "Natural Gray (工程水泥灰)"],
        "sizes": ["39 inch / 1 Meter (标准单段沟长)", "5-6 inch (标准屋檐天沟网)", "4x4 inch (木方柱底座)", "6x6 inch (重载立柱底座)"],
        "national_certs": ["EN 1433 / ANSI A112.6.3 (A15~C250汽车承载试验)", "ASTM A123 (热浸镀锌层附着力试验)", "ASTM G154 (抗UV黄变脆化试验)"]
    }
}

# ==============================================================================
# 4. 全美 50 州全字段深度数据库
# ==============================================================================
STATES_DATA = {
    "NC": {
        "cn": "北卡罗来纳州", "name": "North Carolina", "region": "美东南", "thd": 72, "lowes": 105, "menards": 0, "dc": "夏洛特(Lowe's大本营)",
        "foundation": "木结构架空层/地下室(75%+)", "climate": "Zone 4A/3A 混合湿润", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖地面出风口、实木高低压条、防潮五金", "avoid": "未做防锈处理冷轧薄铁件",
        "size_breakdown": "地面主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线狭窄区: 2x12 (10%); 回风: 6x10 (5%)",
        "channel_advice": "Lowe's全球总部大本营，THD门店流转极快，重度配置端架(Endcap)促销位。",
        "hdd": 3400, "cdd": 1600, "frost_depth": 12, "water_hardness": 3.0, "salt_risk": "中", "hazard": "沿海飓风/湿热雷暴", "house_age": 33, "hazard_idx": 5, "base_vel": 42.0,
        "state_certs": ["NC State Building Code (沿海风暴紧固标准)", "ASHRAE 90.1 通风能耗审计"]
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
        "state_certs": ["City of Chicago Building Code (芝加哥建筑法规)", "UL 203 吊架"]
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
        "foundation": "95%+混凝土实心大平板(Slab)", "climate": "Zone 1A/2A 极湿热高盐雾飓风", "flooring": "瓷砖 60%, 强化/LVP 25%, 地毯 15%",
        "best": "威霖天花散流器、不锈钢长条地漏、抗飓风角码", "avoid": "地面出风口 (实心水泥地无孔，绝对禁发货!)",
        "size_breakdown": "天花板主推: 6x6, 8x8, 12x12 (65%); 侧墙回风: 14x6, 20x20 (35%)",
        "channel_advice": "纯制冷市场，严禁发地面风口；主推 HVHZ 抗飓风门窗五金与防腐地漏。",
        "hdd": 500, "cdd": 3800, "frost_depth": 0, "water_hardness": 14.0, "salt_risk": "极低", "hazard": "HVHZ五级强飓风/极高盐雾", "house_age": 34, "hazard_idx": 9, "base_vel": 21.0,
        "state_certs": ["Miami-Dade NOA (迈阿密-戴德县抗飓风最高认证)", "FBC HVHZ 标准", "cUPC 淋浴地漏"]
    },
    "CA": {
        "cn": "加利福尼亚州", "name": "California", "region": "美西", "thd": 234, "lowes": 112, "menards": 0, "dc": "洛杉矶/安大略总仓",
        "foundation": "南加全平板/抗震高要求", "climate": "Zone 3B/4B 干燥温和干热", "flooring": "瓷砖 45%, LVP 35%, 地毯 20%",
        "best": "威霖 Title 24环保风口、抗震支架组件、WUI防飞烬百叶", "avoid": "高铅铸造件、普通易燃塑料",
        "size_breakdown": "天花主推: 6x6, 8x8, 10x10 (60%); 侧墙格栅: 14x6 (40%)",
        "channel_advice": "全美最大单一经济体，但加州 65 号提案（Prop 65 铅标）是法律诉讼雷区，必须贴标。",
        "hdd": 2100, "cdd": 1300, "frost_depth": 0, "water_hardness": 9.5, "salt_risk": "极低", "hazard": "WUI山火/高烈度地震/Prop 65铅标", "house_age": 48, "hazard_idx": 7, "base_vel": 20.0,
        "state_certs": ["加州 Prop 65 无铅警告贴标 (一票否决红线)", "加州 Title 24 气密性法案", "加州 HCAI/OSHPD 管道抗震支吊架预审批", "加州 WUI 防火防飞烬认证"]
    },
    "TX": {
        "cn": "德克萨斯州", "name": "Texas", "region": "美南核心", "thd": 182, "lowes": 145, "menards": 0, "dc": "达拉斯/休斯敦大仓",
        "foundation": "85%+混凝土实心大平板(Slab)", "climate": "Zone 2A/3A/3B 漫长干热湿热", "flooring": "瓷砖 50%, 抛光强化 30%, 地毯 20%",
        "best": "威霖天花散流器、回风百叶格栅、重型管道吊卡", "avoid": "地面下沉式出风口 (实心地基无孔可用!)",
        "size_breakdown": "天花散流器: 6x6, 8x8, 12x12 (70%); 墙面回风: 14x6, 20x20 (30%)",
        "channel_advice": "全美建材总盘第一大州，虽单店被门店密摊薄，但总吞吐量是工厂开工基本盘。",
        "hdd": 1600, "cdd": 3000, "frost_depth": 5, "water_hardness": 12.5, "salt_risk": "低", "hazard": "酷暑极干热/偶发寒潮破管", "house_age": 31, "hazard_idx": 6, "base_vel": 22.0,
        "state_certs": ["TDI 德州保险厅沿海防风认证", "ASHRAE 90.1 能耗审计", "MSS SP-58 承重测试"]
    }
}

# 补全其余 39 州
EXTRA_STATES = {
    "PA": ("宾夕法尼亚州", "Pennsylvania", "美东", 73, 83, 0, "老房全地下室比例高", 5400, 900, 38, 8.5, "极高", "老房融雪盐", 58, 28.5, ["ASTM B117 盐雾 480h", "cUPC 地漏"]),
    "NY": ("纽约州", "New York", "美东北", 100, 68, 0, "市区公寓无风管/独栋地下室", 5900, 800, 48, 5.5, "极高", "湖效应暴雪", 62, 26.0, ["NYSERDA 能源认证", "UL 94 阻燃"]),
    "WI": ("威斯康星州", "Wisconsin", "美中", 28, 14, 45, "全地下室普及率极高", 7400, 550, 54, 14.5, "极高", "暴雪融雪盐", 51, 25.5, ["Menards 质量验收标准", "MSS SP-58"]),
    "MN": ("明尼苏达州", "Minnesota", "美中", 35, 12, 38, "全地下室/深冻土水暖多", 8500, 550, 60, 14.0, "极高", "全美最深冻土(60寸)", 46, 24.5, ["IPC 305.4 超长防冻水阀规范", "UL 203 吊架"]),
    "CO": ("科罗拉多州", "Colorado", "山地大区", 47, 28, 0, "防冻全地下室", 6200, 600, 36, 7.5, "高", "高海拔强紫外线", 38, 24.0, ["WUI 山火防飞烬网", "ASHRAE 70"]),
    "WA": ("华盛顿州", "Washington", "美西北", 48, 38, 0, "架空层/现代高气密住宅", 4900, 300, 18, 2.5, "低", "长年阴雨高湿", 43, 23.5, ["WA State Energy Code", "ASTM G154 户外防霉"]),
    "AZ": ("亚利桑那州", "Arizona", "美西南", 58, 33, 0, "100%混凝土实心大平板(Slab)", 1200, 3500, 0, 16.5, "极低", "极端沙漠酷暑+极硬水", 30, 19.5, ["NSF 372 无铅涉水", "抗紫外线黄变测试"]),
    "AK": ("阿拉斯加州", "Alaska", "美西北", 7, 5, 0, "永久冻土抬升地基", 10500, 0, 72, 6.0, "中", "全美最高寒(HDD>10000)", 42, 25.0, ["极低温-40℃冲击韧性测试", "超耐寒密封"]),
    "HI": ("夏威夷州", "Hawaii", "美西", 7, 4, 0, "火山岩/架空防潮桩", 0, 4200, 0, 3.0, "低", "纯海岛极端高盐雾", 47, 18.0, ["ASTM B117 盐雾 1000h+ (强制316级)", "cUPC"]),
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
    "NJ": ("新泽西州", "New Jersey", "美东北", 65, 40, 0, "紧凑型地下室老房", 4900, 1200, 30, 6.5, "极高", "密集融雪盐腐蚀", 57, 27.5, ["NJ State Uniform Code", "cUPC"]),
    "NM": ("新墨西哥州", "New Mexico", "美西南", 17, 13, 0, "混凝土实心平板(Slab)为主", 3800, 1500, 18, 13.0, "低", "沙漠风沙强紫外线", 36, 22.5, ["NSF 372", "耐风沙磨蚀测试"]),
    "ND": ("北达科他州", "North Dakota", "美中", 4, 3, 8, "防冻深层全地下室", 9400, 450, 66, 13.0, "极高", "全美最高HDD极寒", 45, 24.5, ["IPC 305.4 超深防冻", "MSS SP-58"]),
    "OK": ("俄克拉荷马州", "Oklahoma", "美南", 21, 24, 0, "架空层与平板各半", 3400, 1900, 15, 11.5, "中", "龙卷风走廊风暴", 40, 26.0, ["FEMA P-361 避难室抗风压", "cUPC"]),
    "OR": ("俄勒冈州", "Oregon", "美西北", 27, 18, 0, "架空层木结构(Crawl)", 4600, 400, 12, 2.0, "低", "常年阴雨高湿霉菌", 43, 26.5, ["OR Energy Code", "ASTM G154 防霉"]),
    "RI": ("罗德岛州", "Rhode Island", "美东北", 7, 5, 0, "老房紧凑型地下室", 5600, 750, 40, 3.5, "极高", "海岸盐雾融雪盐", 60, 25.0, ["cUPC", "UL 94"]),
    "SD": ("南达科他州", "South Dakota", "美中", 3, 3, 5, "防冻深层地下室", 7600, 700, 54, 16.5, "极高", "深冻土极寒", 47, 25.0, ["IPC 305.4", "UL 203"]),
    "UT": ("犹他州", "Utah", "山地大区", 24, 14, 0, "大户型全地下室", 5800, 1050, 30, 17.5, "高", "大温差极硬水", 32, 25.5, ["NSF 372", "ASHRAE 70"]),
    "VT": ("佛蒙特州", "Vermont", "美东北", 5, 4, 0, "全地下室山地木屋", 7600, 350, 54, 4.5, "极高", "漫长积雪严寒", 51, 24.5, ["VT Energy Code", "UL 94"]),
    "WY": ("怀俄明州", "Wyoming", "山地大区", 5, 3, 2, "全地下室独栋", 7500, 350, 50, 11.0, "高", "极高海拔极寒狂风", 42, 23.5, ["MSS SP-58", "极温冲击测试"])
}

for k, v in EXTRA_STATES.items():
    if k not in STATES_DATA:
        STATES_DATA[k] = {
            "cn": v[0], "name": v[1], "region": v[2], "thd": v[3], "lowes": v[4], "menards": v[5],
            "dc": "大区核心集散仓", "foundation": v[6], "climate": "Zone 4A/5A 大陆气候", "flooring": "实木 40%, LVP 35%, 瓷砖 15%, 地毯 10%",
            "best": "威霖标准化出风口、装配式槽钢支架", "avoid": "非标冷门异形件",
            "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)",
            "channel_advice": "按大区 RDC 配送中心整托调拨备货，保持安全周转天数即可。",
            "hdd": v[7], "cdd": v[8], "frost_depth": v[9], "water_hardness": v[10], "salt_risk": v[11],
            "hazard": v[12], "house_age": v[13], "hazard_idx": 5, "base_vel": v[14], "state_certs": v[15]
        }

df_states_raw = pd.DataFrame.from_dict(STATES_DATA, orient="index")
df_states_raw["total_stores"] = df_states_raw["thd"] + df_states_raw["lowes"] + df_states_raw["menards"]
ALL_REGIONS = ["全部大区 (All Regions)"] + sorted(list(set(df_states_raw["region"].tolist())))

# ==============================================================================
# 5. 顶层控制器面板
# ==============================================================================
st.markdown("""
<div class="bi-header">
    <div class="main-title">🏢 宁波威霖住宅设施 · 北美大零售商业与工程决策系统 (Pro Edition)</div>
    <div class="sub-title">象山工业园产线对标 | 50 州工程物理环境测算 | 单州全景调研与对家横向对标 | 州级出口认证图谱</div>
</div>
""", unsafe_allow_html=True)

# 宏观控制排
c1, c2, c3, c4 = st.columns([1.3, 0.9, 1.0, 1.1])
with c1:
    selected_cat_key = st.selectbox("📂 1. 威霖核心业务线：", list(CATEGORY_CONFIG.keys()), format_func=lambda x: CATEGORY_CONFIG[x]["name"])
    cat_cfg = CATEGORY_CONFIG[selected_cat_key]
with c2:
    selected_region = st.selectbox("🗺️ 2. 地理大区筛选：", ALL_REGIONS, index=0)
with c3:
    selected_season = st.selectbox("📅 3. 出货节令脉冲：", [
        "Q1 春季复苏与翻新热潮 (3-5月)",
        "Q2 夏季空调制冷高峰 (6-8月)",
        "Q3 入冬防寒整备爆发季 (9-11月)",
        "Q4 深冬极寒与防冻抢修 (12-2月)",
        "全年平销基准期 (Annual Baseline)"
    ], index=2)
with c4:
    selected_channel = st.selectbox("🏬 4. 目标商超零售网络：", [
        "全部渠道综合总盘 (THD + Lowe's + Menards)",
        "The Home Depot (承包商Pro工匠第一)",
        "Lowe's (家庭DIY与软装换新偏好)",
        "Menards (中西部大区独立专营)"
    ], index=0)

# 工法与客群控制排
st.markdown("#### 🎯 威霖制造工法与目标客群属性联动")
f1, f2, f3, f4, f5 = st.columns(5)
with f1:
    pos_opts = ["(全部位置 / All)"] + cat_cfg["positions"]
    sel_pos = st.selectbox("位置形态：", pos_opts, index=1, key=f"{selected_cat_key}_pos").split(" ")[0]
with f2:
    mat_opts = ["(全部材质 / All)"] + cat_cfg["materials"]
    sel_mat = st.selectbox("原材料构件：", mat_opts, index=0, key=f"{selected_cat_key}_mat").split(" ")[0]
with f3:
    fin_opts = ["(全部工艺 / All)"] + cat_cfg["finishes"]
    sel_fin = st.selectbox("表面工艺/防腐：", fin_opts, index=0, key=f"{selected_cat_key}_fin").split(" ")[0]
with f4:
    size_opts = ["(全部尺寸 / All)"] + cat_cfg["sizes"]
    sel_size = st.selectbox("规格尺寸：", size_opts, index=1, key=f"{selected_cat_key}_size").split(" ")[0]
with f5:
    sel_persona = st.selectbox("👥 核心客群定位：", [
        "全客群综合基准",
        "DIY 个人散客 (重彩盒与自装图解)",
        "DIFM 改善型中产 (高客单/PVD/极简)",
        "Pro 专业工匠 (Contractor Pack/西语)",
        "B2B 物业房东 (ADA合规/极致性价比)"
    ], index=0)

# ==============================================================================
# 6. 计算引擎
# ==============================================================================
calc_rows = []

for abbr, s in STATES_DATA.items():
    base_v = s["base_vel"]
    weight = 1.0
    reasons = []
    
    # 地基与安装位置逻辑
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

    elif selected_cat_key == "PLUMBING":
        if "Linear" in sel_pos or "Tile-in" in sel_pos:
            if abbr in ["FL", "CA", "TX", "NC", "SC", "GA", "AZ"]:
                weight *= 2.2
                reasons.append("现代无门槛大板淋浴房改装爆发，威霖隐形地漏畅销")
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

    # 融雪盐与水质硬度
    if s["salt_risk"] in ["高", "极高"]:
        if sel_mat in ["Steel", "Carbon"]:
            weight *= 0.8
            reasons.append("⚠️ 融雪盐鞋底腐蚀严重，普通碳钢有生锈索赔隐患")
        elif sel_mat in ["Aluminum", "Stainless", "Hot-Dip"]:
            weight *= 1.25
            reasons.append("✅ 阳极氧化铝/热镀锌耐融雪盐侵蚀，大湖雪带好评度高")

    if s["water_hardness"] >= 13.0 and selected_cat_key == "PLUMBING":
        if sel_fin == "Polished":
            weight *= 0.85
            reasons.append("⚠️ 极重度硬水，抛光亮铬表面极易结顽固白斑水垢")
        elif sel_fin in ["Brushed", "Matte", "PVD"]:
            weight *= 1.25
            reasons.append("✅ 拉丝镍/PVD工艺在硬水区抗水垢残留表现优异")

    # 房龄加权
    if s["house_age"] >= 50:
        weight *= 1.2
        reasons.append(f"中位房龄达 {s['house_age']} 年，老旧建筑二次翻新动销活跃")

    # 节令脉冲
    if "Q3" in selected_season and selected_cat_key in ["SHOWER_HARDWARE", "HVAC"]:
        weight *= 1.4
        reasons.append("🍂 处于入冬防寒整备季（Fall Weatherization），销量脉冲式激增")
    elif "Q2" in selected_season and selected_cat_key == "HVAC" and sel_pos == "Ceiling":
        weight *= 1.7
        reasons.append("☀️ 酷暑制冷峰值，天花散流器换新需求强劲")
    elif "Q4" in selected_season and selected_cat_key == "PLUMBING" and "Frost" in sel_pos:
        weight *= 2.2
        reasons.append("❄️ 极寒深度冰封，爆管抢修更换进入最高峰")

    if sel_size in ["04X10", "36", "24-36", "1-5/8", "39"]:
        weight *= 1.15

    # 渠道有效门店
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
    upsw = round(calc_vel / 4.33, 1)
    
    tier_str = "Tier 1 (S级核心)" if calc_vel >= 38.0 else ("Tier 2 (A级主力)" if calc_vel >= 26.0 else ("Tier 3 (B级走量)" if calc_vel >= 14.0 else "Tier 4 (受限/避坑)"))
    pog = "🔥 双排面 (Double, 24寸)" if calc_vel >= 35.0 else ("✅ 单排面 (Single, 12寸)" if calc_vel >= 15.0 else "⚠️ 底层冷门位")

    row_data = dict(s)
    row_data["abbr"] = abbr
    row_data["calc_vel"] = calc_vel
    row_data["calc_tot"] = calc_tot
    row_data["upsw"] = upsw
    row_data["active_stores"] = active_stores
    row_data["tier"] = tier_str
    row_data["pog"] = pog
    row_data["calc_rev_msrp"] = calc_tot * retail_msrp
    row_data["calc_fob_tot"] = calc_tot * fob_cost
    row_data["reason_desc"] = "；".join(reasons) if reasons else "符合常规分销基线"
    calc_rows.append(row_data)

df_all = pd.DataFrame(calc_rows)

# 大盘基准线计算 (用于 Tab 2 横向对比)
national_avg_vel = round(df_all["calc_vel"].mean(), 1)
national_avg_upsw = round(df_all["upsw"].mean(), 1)

if selected_region != "全部大区 (All Regions)":
    df_res = df_all[df_all["region"] == selected_region].copy()
else:
    df_res = df_all.copy()

df_res["rank_vel"] = df_res["calc_vel"].rank(ascending=False, method="min").astype(int)
df_res["rank_tot"] = df_res["calc_tot"].rank(ascending=False, method="min").astype(int)
df_sorted = df_res.sort_values("calc_tot", ascending=False).reset_index(drop=True)
df_sorted["序号"] = df_sorted.index + 1

# ==============================================================================
# 7. 全网四大核心 KPI 看板
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
        <div class="kpi-title">单店月流速冠军 (平效之王)</div>
        <div class="kpi-val">{top_v_row['cn']} ({top_v_row['calc_vel']:.1f} 件/月)</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">渠道总吞吐量霸主 (排产核心)</div>
        <div class="kpi-val">{top_t_row['cn']} ({top_t_row['calc_tot']:,} 件/月)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 8. 五大结构化职能选项卡（Tabs）
# ==============================================================================
tab_rank, tab_deepdive, tab_persona, tab_channel, tab_cert = st.tabs([
    "📋 全美零售排行大盘",
    "🎯 威霖单州深度调研与竞品对标",
    "👥 客户人居习性与买家画像透视",
    "📊 Big 3 零售格局与海运分仓",
    "📜 威霖出海认证与法规红线雷达"
])

# ----------------- TAB 1: 全美排行榜 -----------------
with tab_rank:
    v_col1, v_col2 = st.columns([1.2, 1])
    with v_col1:
        view_mode = st.radio(
            "选择排行榜主排序维度：",
            ["全州渠道月总吞吐量 (件/月) - 适于工厂排产总盘计划", "单店平均月销售流速 (件/店/月) - 适于商超平效谈判与货架位申请"],
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
            "序号", "abbr", "cn", "region", "tier", "calc_vel", "upsw", "calc_tot", "calc_rev_msrp",
            "active_stores", "pog", "foundation"
        ]],
        use_container_width=True,
        column_config={
            "序号": st.column_config.NumberColumn(width=45),
            "abbr": st.column_config.TextColumn("州标", width=55),
            "cn": st.column_config.TextColumn("州全称", width=95),
            "region": st.column_config.TextColumn("大区", width=80),
            "tier": st.column_config.TextColumn("战略梯队", width=110),
            "calc_vel": st.column_config.ProgressColumn("单店月流速", min_value=0, max_value=max_vel_val, format="%.1f 件"),
            "upsw": st.column_config.NumberColumn("单店周流速(UPSW)", format="%.1f 件/周"),
            "calc_tot": st.column_config.NumberColumn("月总盘(件)", format="%d"),
            "calc_rev_msrp": st.column_config.NumberColumn("月零售流水($)", format="$%d"),
            "active_stores": st.column_config.NumberColumn("有效门店", width=70),
            "pog": st.column_config.TextColumn("POG货架排面建议", width=140),
            "foundation": st.column_config.TextColumn("典型地基基底", width=160)
        },
        height=520,
        hide_index=True
    )

# ----------------- TAB 2: 单州深度调研与竞品对标（彻底修复截断与参照系） -----------------
with tab_deepdive:
    st.markdown("### 🎯 威霖单州全景深度调研与竞品横向对标看板")
    st.caption("穿透分析单一州的自然建筑基底，对比全美大盘均值，并与北美在售头部竞品展开参数级对标。")
    
    target_abbr = st.selectbox("👉 选择要穿透调研的目标州：", df_sorted["abbr"].tolist(), index=0)
    cur = df_sorted[df_sorted["abbr"] == target_abbr].iloc[0]
    rival_info = cat_cfg["competitors"]
    
    # 计算与全美大盘对比指数
    vel_vs_nat = round(((cur['calc_vel'] - national_avg_vel) / national_avg_vel) * 100, 1)
    vel_delta_str = f"超出大盘 +{vel_vs_nat}%" if vel_vs_nat >= 0 else f"低于大盘 {vel_vs_nat}%"
    
    # 第一层：大盘对比与基本面
    col_d1, col_d2, col_d3 = st.columns([1, 1.1, 1])
    with col_d1:
        st.markdown(f"""
        <div class="section-card">
            <span class="badge-tier1">{cur['tier']}</span>
            <h3 style="margin:6px 0;">{cur['cn']} ({cur['abbr']})</h3>
            <p style="font-size:0.85rem;color:#475569;">所属大区：<b>{cur['region']}</b> | 房龄：<b>{cur['house_age']}年</b></p>
            <p style="font-size:0.9rem;line-height:1.7;">
            • 预估单店月流速: <b>{cur['calc_vel']:.1f}</b> 件/月<br>
            • 核心周流速 (UPSW): <b>{cur['upsw']:.1f}</b> 件/周<br>
            • <b>大盘基准比</b>: <b style="color:{'#166534' if vel_vs_nat>=0 else '#991B1B'};">{vel_delta_str}</b><br>
            • 该州全渠道月需求: <b>{cur['calc_tot']:,}</b> 件/月
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_d2:
        st.markdown(f"""
        <div class="section-card">
            <h4 style="margin-top:0;color:#0F172A;">🏠 地基物理与环境红线</h4>
            <p style="font-size:0.88rem;line-height:1.7;">
            • <b>地基基底</b>: {cur['foundation']}<br>
            • <b>地面偏好</b>: {cur['flooring']}<br>
            • <b>能耗度日</b>: HDD <b>{cur['hdd']:,}</b> | CDD <b>{cur['cdd']:,}</b><br>
            • <b>法定冻土</b>: <b>{cur['frost_depth']} 英寸</b><br>
            • <b>腐蚀与硬水</b>: 融雪盐 <b>{cur['salt_risk']}</b> | 水质硬度 <b>{cur['water_hardness']} GPG</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_d3:
        st.markdown(f"""
        <div class="section-card">
            <h4 style="margin-top:0;color:#0F172A;">🏬 渠道网点与货架位策略</h4>
            <p style="font-size:0.88rem;line-height:1.7;">
            • <b>商超覆盖</b>: THD: <b>{cur['thd']}</b> | Lowe's: <b>{cur['lowes']}</b> | Menards: <b>{cur['menards']}</b><br>
            • <b>货架排面 (POG)</b>: <b>{cur['pog']}</b><br>
            • <b>当地主推品</b>: <span style="color:#166534;font-weight:600;">{cur['best']}</span><br>
            • <b>当地避雷品</b>: <span style="color:#991B1B;font-weight:600;">{cur['avoid']}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    # 第二层：威霖 vs 竞品对家横向对标 (结构化弹性卡片，杜绝截断)
    st.markdown("#### ⚔️ 当前品类：宁波威霖 (Runner) VS 北美头部对家横向对标")
    
    comp_c1, comp_c2 = st.columns(2)
    with comp_c1:
        st.markdown(f"""
        <div class="competitor-card">
            <h4 style="margin-top:0;color:#334155;">🥊 货架主要对家：{rival_info['main_rival']}</h4>
            <p style="font-size:0.9rem;line-height:1.7;">
            • <b>对家货架占有率</b>: <b>{rival_info['shelf_share']}</b><br>
            • <b>对家零售挂牌价</b>: <b>{rival_info['rival_msrp']}</b><br>
            • <b>商超买手留存毛利</b>: <b>{rival_info['rival_margin']}</b> (成熟大牌给买手留利薄)<br>
            • <b>对家产品核心短板</b>:<br>
            <span style="color:#475569;">{rival_info['rival_weakness']}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with comp_c2:
        st.markdown(f"""
        <div class="willi-card">
            <h4 style="margin-top:0;color:#1E40AF;">🛡️ 宁波威霖 (Runner) 进攻策略与替代优势</h4>
            <p style="font-size:0.9rem;line-height:1.7;">
            • <b>威霖建议零售价</b>: <b>${retail_msrp:.2f}</b> (高性价比渗透)<br>
            • <b>威霖带给买手的净毛利</b>: <b style="color:#166534;">{buyer_margin:.1f}%</b> (留利极其丰厚，强动力换排面)<br>
            • <b>威霖单店预估周流速</b>: <b>{cur['upsw']:.1f} 件/周</b><br>
            • <b>威霖突围战术指引</b>:<br>
            <span style="color:#1E3A8A;">{rival_info['willi_tactic']}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    # 第三层：配比与渠道谈盘指引
    st.markdown(f"""
    <div class="advice-box">
        <b>📐 该州当地规格销售装箱配比依据 (Size Breakdown)：</b><br>
        {cur['size_breakdown']}<br><br>
        <b>💼 威霖外贸业务员与商超买手谈盘指引 (Buyer Pitch Advice)：</b><br>
        {cur['channel_advice']}
    </div>
    """, unsafe_allow_html=True)

# ----------------- TAB 3: 客户人居画像透视 -----------------
with tab_persona:
    st.markdown("### 👥 目标州人居生活方式、买家画像与防退包装策略")
    st.caption("针对美国家装消费者的真实生活习惯，指导外贸开发规避差评与退货。")
    
    p_col1, p_col2 = st.columns([1.1, 1])
    with p_col1:
        st.markdown("#### 1. 核心买家结构与行为画像")
        st.markdown(f"""
        <div class="section-card">
            <b>当前聚焦画像：{sel_persona}</b><br><br>
            • <b>DIY 个人散客 (占比约 55%)</b>：周末施工，极度害怕量错尺寸（常将 4x10 开孔内径与 5.5x11.5 外沿混淆）。包装必须带 <b>1:1 开孔打孔定位卡纸</b> 与免螺丝自锁结构。<br><br>
            • <b>Pro 专业工匠 (占比约 35%)</b>：早晨 6:00 进店，讲西班牙语的拉丁裔工人占 40%+。痛恨因质量差导致的二次返工（Callback）。必须提供 <b>Contractor Pack (10-20件工业包装)</b> 且外箱附带西语说明。<br><br>
            • <b>DIFM 改善型中产 (占比约 10%)</b>：追求极简美学，痛恨塑料踩踏异响，偏好 PVD 哑光黑与实木对齐款。
        </div>
        """, unsafe_allow_html=True)
        
    with p_col2:
        st.markdown("#### 2. 防退货包装与出海标签指引 (Anti-Return Packaging)")
        st.markdown(f"""
        <div class="section-card">
            <b>⚠️ 美国家庭“买3退2”试错退货对策：</b><br><br>
            • <b>尺寸防呆标示</b>：外盒正反面必须以 <b>大号粗体标明 Duct Opening (管道开孔内径)</b>，而非面罩外沿尺寸。<br><br>
            • <b>双语图解标语</b>：美南与沿海建议加印西班牙语 <i>"Fácil de instalar / Rejilla de piso"</i>。<br><br>
            • <b>核心功能图标</b>：高跟鞋防卡 (Heel-Proof)、宠物毛发防卡 (Pet-Safe) 等图标印于正面右上角。<br><br>
            • <b>防拆保护结构</b>：采用可二次复原的卡扣盒，避免消费者试装破损后被超市强制扣取 RTV 残损赔偿。
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 4: 渠道格局与港口供应链 -----------------
with tab_channel:
    st.markdown("#### 📊 Big 3 零售巨头渠道格局 (THD vs Lowe's vs Menards)")
    top15 = df_res.sort_values("calc_tot", ascending=False).head(15)
    chart_df = pd.DataFrame({
        "州": top15["cn"],
        "THD (家得宝)": top15["calc_vel"] * top15["thd"],
        "Lowe's (劳氏)": top15["calc_vel"] * top15["lowes"],
        "Menards (美纳斯)": top15["calc_vel"] * top15["menards"]
    }).set_index("州")
    st.bar_chart(chart_df, height=360)
    
    st.markdown("---")
    st.markdown("#### 🚚 全美大区配送中心 (RDC) 备货比例与 GMA 打托标准")
    s_col1, s_col2 = st.columns([1.1, 1.3])
    with s_col1:
        reg_summary = df_all.groupby("region").agg({
            "abbr": "count", "active_stores": "sum", "calc_tot": "sum", "calc_vel": "mean"
        }).reset_index()
        reg_summary.columns = ["大区", "州数", "总门店", "月度总盘(件)", "区均流速"]
        reg_summary["建议配货比例"] = (reg_summary["月度总盘(件)"] / reg_summary["月度总盘(件)"].sum() * 100).round(1).astype(str) + "%"
        reg_summary["区均流速"] = reg_summary["区均流速"].round(1)
        st.dataframe(reg_summary, use_container_width=True, hide_index=True)
    with s_col2:
        st.markdown(f"""
        <div class="physics-card">
            <b>📦 美标木托盘 (GMA Pallet 48×40") 打托规范：</b><br><br>
            • <b>标准装箱数</b>: {case_pack} 件/箱<br>
            • <b>堆码规格 (TI/HI)</b>: 每层 6 箱 × 堆叠 8 层 = <b>48 箱/托</b><br>
            • <b>单托总装载量</b>: <b>{case_pack * 48} 件/托盘</b> (总高度必须 ≤ 50 英寸，总重 ≤ 2000 磅)<br>
            • <b>外箱条码</b>: 打印扫描级 GS1-128 / ITF-14 箱唛，单品贴扫描级 UPC-A。
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 5: 认证图谱与合规雷达 -----------------
with tab_cert:
    st.markdown("### 📜 威霖产品出海：全美通用认证与各州极端法典清单")
    st.caption("这是 The Home Depot 与 Lowe's 买手进行 Vendor Onboarding 时的强制核验清单。")
    
    cert_col1, cert_col2 = st.columns(2)
    with cert_col1:
        st.markdown(f"#### 🏛️ 【{cat_cfg['name'].split(' ')[0]}】全美通用强制认证")
        for n_cert in cat_cfg["national_certs"]:
            st.markdown(f"""
            <div style="background:white;border:1px solid #CBD5E1;padding:10px 14px;border-radius:6px;margin-bottom:8px;">
                <b>✓ {n_cert}</b>
            </div>
            """, unsafe_allow_html=True)
            
    with cert_col2:
        st.markdown(f"#### 🔴 当前选中州【{cur['cn']}】地方强制法典与标准")
        for s_cert in cur["state_certs"]:
            st.markdown(f"""
            <div style="background:#FEF2F2;border:1px solid #FCA5A5;color:#991B1B;padding:10px 14px;border-radius:6px;margin-bottom:8px;">
                <b>⚠️ 地方红线：{s_cert}</b>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('<div class="radar-box">', unsafe_allow_html=True)
    st.markdown(f"""
    <b>🛡️ 威霖合规风控总备忘录：</b><br>
    • <b>加州 Prop 65</b>：出光剂与铅析出量必须符合限量，未取得无铅报告必须加印致癌黄标，否则面临赏金律师诉讼。<br>
    • <b>佛州与沿海 HVHZ</b>：淋浴门与户外紧固构件进入沿海区域必须具备迈阿密-戴德县 NOA 抗风暴飞弹撞击认证。<br>
    • <b>商业管道抗震</b>：威霖装配式槽钢支吊架在西海岸必须具备 HCAI / OSHPD 预审批编号，才能参与大型公建工程招投标。
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 9. 数据导出
# ==============================================================================
st.markdown("---")
csv_out = df_sorted[[
    "序号", "abbr", "cn", "name", "region", "tier", "calc_vel", "upsw", "calc_tot", "calc_rev_msrp",
    "calc_fob_tot", "active_stores", "pog", "foundation", "flooring", "best", "avoid",
    "size_breakdown", "channel_advice", "hdd", "cdd", "frost_depth", "water_hardness",
    "salt_risk", "house_age", "hazard", "state_certs", "reason_desc"
]].to_csv(index=False).encode('utf-8-sig')

st.download_button(
    label=f"📥 一键导出【{cat_cfg['name'].split(' ')[0]}】({selected_region}) 威霖全景决策报表 (.csv)",
    data=csv_out,
    file_name=f"Ningbo_Runner_Intelligence_{selected_cat_key}_{selected_region[:3]}.csv",
    mime="text/csv"
)
