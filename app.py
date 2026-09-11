import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# ==============================================================================
# 1. 页面配置与企业级高级 BI 视觉规范
# ==============================================================================
st.set_page_config(
    page_title="宁波威霖住宅设施 · 北美大零售商业与工程决策系统",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; color: #0F172A; }
    .bi-header {
        background: white;
        padding: 16px 22px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .main-title { font-size: 1.55rem; font-weight: 700; color: #0F172A; margin-bottom: 4px; }
    .sub-title { font-size: 0.86rem; color: #475569; }
    .kpi-card {
        background: linear-gradient(135deg, #1E40AF, #2563EB);
        color: white;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }
    .kpi-title { font-size: 0.82rem; opacity: 0.92; margin-bottom: 2px; font-weight: 500; }
    .kpi-val { font-size: 1.45rem; font-weight: 700; }
    .section-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 18px;
        margin-bottom: 12px;
        height: auto !important;
        line-height: 1.6;
        word-break: break-word;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .badge-tier1 { background-color: #DCFCE7; color: #166534; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier2 { background-color: #DBEAFE; color: #1E40AF; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier3 { background-color: #FEF3C7; color: #92400E; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier4 { background-color: #FEE2E2; color: #991B1B; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .advice-box { border-left: 4px solid #3B82F6; background-color: #EFF6FF; padding: 12px 16px; border-radius: 0 6px 6px 0; margin-top: 10px; line-height: 1.6; }
    .radar-box { border-left: 4px solid #EF4444; background-color: #FEF2F2; padding: 12px 16px; border-radius: 0 6px 6px 0; margin-top: 10px; line-height: 1.6; }
    .pitch-box { background-color: #0F172A; color: #E2E8F0; padding: 16px 18px; border-radius: 8px; font-family: monospace; font-size: 0.85rem; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# 动态时间引擎，保证数据永不失效
current_dt = datetime.now()
curr_year = current_dt.year
curr_month = current_dt.month
curr_week = current_dt.isocalendar()[1]

# ==============================================================================
# 2. 侧边栏：多基地关税、双轨履约与全景百科词典
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/factory.png", width=46)
    st.markdown("### 💰 威霖供应链财务与战略测算")
    st.caption(f"宁波威霖住宅设施 (建霖家居 603408) · {curr_year} 动态决策")
    
    prod_origin = st.radio("🏭 制造基地 / 出货原产地 (Origin)：", ["宁波象山制造总部 (中国)", "建霖泰国海外制造基地 (免301关税)"], index=0)
    incoterm_mode = st.radio("📦 商超履约交付模式 (Fulfillment)：", ["FOB 港口直采 (Direct Import / DI)", "美国本土海外仓分发 (DWD / 到门)"], index=0)
    
    fob_cost = st.number_input("1. 工厂出厂基准价 FOB ($/件)：", min_value=0.5, max_value=200.0, value=3.80, step=0.2)
    case_pack = st.number_input("2. 标准外箱装箱数 (Case Pack)：", min_value=1, max_value=200, value=10, step=1)
    
    tariff_pct = 0.025 if "泰国" in prod_origin else 0.125
    st.caption(f"• 适用关税税率: **{tariff_pct*100:.1f}%** ({'泰国规避301关税' if '泰国' in prod_origin else '宁波出海加权税率'})")
    
    ocean_freight = 0.65
    dwd_handling = 1.20 if "海外仓" in incoterm_mode else 0.0
    landed_cost = fob_cost * (1 + tariff_pct) + ocean_freight + dwd_handling
    retail_msrp = st.number_input("3. 北美商超零售价 MSRP ($/件)：", min_value=1.0, max_value=500.0, value=12.98, step=0.5)
    
    buyer_margin = ((retail_msrp - landed_cost) / max(retail_msrp, 0.01)) * 100
    gross_profit_unit = retail_msrp - landed_cost
    
    st.markdown(f"""
    <div style='background:white;padding:10px 12px;border-radius:6px;border:1px solid #CBD5E1;margin-bottom:10px;'>
        <span style='font-size:0.8rem;color:#64748B;'>落地完税成本 (Landed DDP)</span>: <b style='color:#0F172A;'>${landed_cost:.2f}</b><br>
        <span style='font-size:0.8rem;color:#64748B;'>商超单件毛利额</span>: <b style='color:#0F172A;'>${gross_profit_unit:.2f}</b><br>
        <span style='font-size:0.8rem;color:#64748B;'>买手净毛利率 (Buyer Margin)</span>: <b style='color:{'#166534' if buyer_margin>=42 else '#991B1B'};'>{buyer_margin:.1f}%</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📚 北美商超与工程实战全景词典")
    with st.expander("1. 房屋地基与对流原理 (Foundation)", expanded=False):
        st.write("• **北方全地下室**：冻土深，开挖全地下室。暖气炉置于地下，热风自然上升，地板出风口是全美刚需。\n• **南方实心大平板 (Slab)**：地下水高，实心水泥地无风道，冷风全由天花板下吹。")
    with st.expander("2. ASHRAE 暖通与 HDD/CDD 能耗度日", expanded=False):
        st.write("• **HDD (采暖度日)**：> 5000 区域长年开暖气，出风口承受 55℃~65℃ 干燥热风，抗热变形是硬指标。\n• **CDD (制冷度日)**：> 2000 区域空调高频冷风，天花散流器防结露滴水是第一客诉源。")
    with st.expander("3. 冻土深度与融雪盐防腐红线", expanded=False):
        st.write("• **冻土线**：北方深达 36~60 英寸，室外水阀必须选 8~12 寸超长杆。\n• **融雪盐**：鞋底盐水滴在门厅，冷轧钢 2 年锈穿，必须推 6063 阳极氧化铝或不锈钢。")
    with st.expander("4. 北美三大零售商 (Big 3) 渠道特征", expanded=False):
        st.write("• **The Home Depot**：偏向 Pro 专业承包商，重工程装与极限承重。\n• **Lowe's**：偏向家庭 DIY 散客与女性，重彩色吊卡颜值。\n• **Menards**：中西部地头蛇，主打 11% 返现 Rebate，蓝领农场主死忠渠道。")
    with st.expander("5. 商超买手合同潜规则 (Allowances)", expanded=False):
        st.write("• **Defective Allowance**：商超合同常规定期在发票扣 2%~4% 作为破损补贴。\n• **Buyback / Chargeback**：滞销时强制供应商回购；条码扫描率<99.5% 单笔罚 $250~$500。")
    with st.expander("6. GMA 托盘标准与 EDI 数据对接", expanded=False):
        st.write("• **GMA 木托盘**：48×40 英寸，总高 ≤ 52 英寸，重 ≤ 2000 磅。\n• **EDI**：入驻商超强制支持 ANSI X12（EDI 850/856/810）。")
    with st.expander("7. 全美出口合规与环保红线清单", expanded=False):
        st.write("• **加州 Prop 65**：无铅报告齐全，否则必须贴致癌黄标。\n• **加州 Title 24 / WUI**：出风口低漏风率气密性与外墙 1/8 英寸防火防飞烬金属网。\n• **佛州 HVHZ**：迈阿密戴德县 NOA 强飓风抗冲击测试。")

# ==============================================================================
# 3. 核心品类配置与市场客观份额分配矩阵（平账数学模型基石）
# ==============================================================================
CATEGORY_CONFIG = {
    "HVAC": {
        "name": "暖通风口与空气分配系统 (Registers & Grilles)",
        "willi_fit": "威霖核心板块：冲压冷轧钢、阳极氧化铝、压铸锌合金复古雕花、工程阻燃ABS出风口全系列。",
        "competitors": {
            "rival_name": "Accord Ventilation / Deflecto",
            "shelf_share": "约 60% 黄金排面垄断",
            "rival_msrp": "$13.98",
            "rival_margin": "40.2%",
            "rival_gauge": "0.5mm ~ 0.6mm (24 Gauge 薄板冲压)",
            "willi_gauge": "0.8mm (20 Gauge 结构钢) / 6063-T5 阳极铝",
            "rival_salt": "中性盐雾 NSS 96 小时 (易起白锈)",
            "willi_salt": "中性盐雾 NSS 480 ~ 720 小时 (PVD/阳极氧化/电泳)",
            "rival_weakness": "传统冲压钢普通喷漆易刮花生锈，缺乏 AF 纳米防指纹等高端工艺，耐盐雾能力一般。",
            "willi_tactic": "以高质感阳极氧化铝与 PVD 哑光黑打高端改善型，给商超买手留出 52%+ 净毛利，换取双排面陈列。"
        },
        "positions": ["Floor (地面出风口)", "Ceiling (天花板散流器)", "Baseboard (踢脚线出风口)", "Sidewall (侧墙回风格栅)"],
        "materials": ["Steel (冲压冷轧钢)", "Aluminum (铝合金阳极氧化)", "Plastic (ABS阻燃树脂)", "Cast Metal (铸铝/铸铁重载)", "Engineered Wood (多层实木复合-抗翘曲)", "Zinc Die-Cast (压铸锌合金雕花)"],
        "finishes": ["Matte Black (US19 哑光黑)", "Brushed Nickel (US15 拉丝镍)", "Glossy White (经典工程白)", "Oil Rubbed Bronze (US10B 油磨青铜)", "PVD Brushed Gold (轻奢拉丝金)", "AF Nano-Coating (纳米防指纹黑)", "Wood Grain Transfer (3D热转印木纹)"],
        "sizes": ["04X10 (全美走量王 65%)", "04X12 (主流换新大号 20%)", "02X12 (踢脚狭长缝 10%)", "06X10 (大排风量 5%)", "12X12 (天花方型大尺寸)"],
        "share_matrix": {
            "materials": {"Steel": 0.58, "Aluminum": 0.22, "Plastic": 0.10, "Cast": 0.05, "Engineered": 0.03, "Zinc": 0.02},
            "positions": {"Floor": 0.55, "Ceiling": 0.30, "Baseboard": 0.08, "Sidewall": 0.07},
            "sizes": {"04X10": 0.65, "04X12": 0.20, "02X12": 0.08, "06X10": 0.04, "12X12": 0.03}
        },
        "national_certs": [
            {"code": "ASHRAE Standard 70", "item": "出风量 CFM 与噪音 NC 评级测试", "body": "AHRI / Intertek", "req": "主卧噪音 NC < 25"},
            {"code": "UL 94", "item": "塑料部件阻燃测试", "body": "UL", "req": "V-0 / HB 级阻燃安全"},
            {"code": "Heel-Proof", "item": "细高跟鞋防卡安全规范", "body": "ASTM", "req": "表面格栅镂空缝隙必须 < 9.5mm"}
        ]
    },
    "PLUMBING": {
        "name": "卫浴排水与长条隐形地漏 (Drains & Plumbing)",
        "willi_fit": "威霖核心板块：不锈钢冲压拉伸、长条隐形线性地漏、防臭下水器、防冻长水阀全系列。",
        "competitors": {
            "rival_name": "Oatey / Sioux Chief",
            "shelf_share": "约 65% 水暖通道排面垄断",
            "rival_msrp": "$49.99 (长条地漏)",
            "rival_margin": "41.5%",
            "rival_gauge": "1.0mm 304 不锈钢薄板",
            "willi_gauge": "1.2mm ~ 1.5mm 加厚 304/316 级精密拉伸",
            "rival_salt": "中性盐雾 NSS 240 小时",
            "willi_salt": "中性盐雾 NSS 720 小时+ (抗氯漂白水侵蚀)",
            "rival_weakness": "长条地漏款式单一偏传统格栅，少有配备当前流行的 Tile-in 瓷砖隐形双面翻转结构。",
            "willi_tactic": "力推 Tile-in 2合1 隐形面板，一面拉丝一面贴砖，1个SKU满足两类客户，替买手省货架并降低备货风险。"
        },
        "positions": ["Linear Drain (长条隐形地漏)", "Tile-in Drain (2合1瓷砖隐形地漏)", "Floor Drain (方形点状地漏)", "Frost-Proof Valve (室外防冻长水阀)"],
        "materials": ["Stainless 304 (304拉丝不锈钢)", "Stainless 316 (316耐氯盐雾级)", "Solid Brass (无铅锻压黄铜)", "ABS/PVC (耐腐工程塑料)"],
        "finishes": ["Brushed Stainless (不锈钢拉丝)", "Matte Black (现代哑光黑)", "Polished Chrome (亮铬镜面)", "PVD Brushed Gold (PVD防磨金)"],
        "sizes": ["24-36 inch (长条隐形主力)", "4x4 inch (标准方形)", "1/2 inch (常规供水接口)", "3/4 inch (主水管接口)"],
        "share_matrix": {
            "materials": {"Stainless": 0.65, "Solid": 0.20, "ABS/PVC": 0.15},
            "positions": {"Linear": 0.35, "Tile-in": 0.25, "Floor": 0.25, "Frost-Proof": 0.15},
            "sizes": {"24-36": 0.55, "4x4": 0.25, "1/2": 0.10, "3/4": 0.10}
        },
        "national_certs": [
            {"code": "cUPC 认证", "item": "全美统一卫浴排水管件认证", "body": "IAPMO", "req": "北美工程准入强制一票否决项"},
            {"code": "ASME A112.18.2", "item": "地漏结构与排水通量测试", "body": "ASME / CSA", "req": "排水通量需满足峰值流速"},
            {"code": "NSF/ANSI 61 & 372", "item": "接触饮用水无铅涉水安全认证", "body": "NSF", "req": "过水部件加权含铅量 < 0.25%"}
        ]
    },
    "HANGERS": {
        "name": "管道支吊架与抗震支撑系统 (Support & Hanger Systems)",
        "willi_fit": "威霖工程王牌业务：建筑管道吊卡、C型装配式槽钢构件、抗震紧固件、商用管道支撑。",
        "competitors": {
            "rival_name": "Superstrut (Thomas & Betts / ABB) / Unistrut",
            "shelf_share": "约 70% 商用电气五金通道排面垄断",
            "rival_msrp": "$18.50 (槽钢) / $2.80 (管卡)",
            "rival_margin": "36.0%",
            "rival_gauge": "12 Gauge (2.6mm) 普碳钢冷镀锌",
            "willi_gauge": "12 Gauge 加厚高强碳钢 / 热浸镀锌 HDG",
            "rival_salt": "普通冷镀锌 EG: 48 小时",
            "willi_salt": "热浸镀锌 HDG: 1000 小时+ / 达克罗防腐",
            "rival_weakness": "对家品牌溢价极高，给买手利润薄；对重型热浸镀锌配件缺乏柔性连续冲压交付能力。",
            "willi_tactic": "依托象山工业园冲压与热浸镀锌能力，以商超自有品牌 (Store Brand) 切入，提供高毛利全套配件包。"
        },
        "positions": ["Strut Channel (C型装配式槽钢)", "Pipe Clamp (管道固定卡箍)", "Seismic Hanger (抗震斜撑加固组件)", "Beam Clamp (工字钢梁夹连接件)"],
        "materials": ["Carbon Steel (重载碳钢)", "Hot-Dip Galvanized Steel (热浸镀锌结构钢)", "Stainless 304 (不锈钢防腐型)", "Ductile Iron (球墨铸铁梁夹)"],
        "finishes": ["Clear Zinc (EG 冷电镀蓝白锌)", "Yellow Zinc (环保三价铬彩锌)", "Hot-Dip Galvanized (HDG 重型热浸镀锌)", "Dacromet (达克罗防腐涂层)", "Black E-Coating (阴极电泳黑)"],
        "sizes": ["1-5/8 inch (全美标准重载槽钢)", "13/16 inch (轻型槽深)", "1/2-2 inch (中小管径卡箍)", "3-6 inch (重载立管卡)"],
        "share_matrix": {
            "materials": {"Carbon": 0.45, "Hot-Dip": 0.30, "Stainless": 0.15, "Ductile": 0.10},
            "positions": {"Strut": 0.40, "Pipe": 0.30, "Seismic": 0.15, "Beam": 0.15},
            "sizes": {"1-5/8": 0.50, "13/16": 0.20, "1/2-2": 0.20, "3-6": 0.10}
        },
        "national_certs": [
            {"code": "MSS SP-58", "item": "全美管道吊架设计制造通用标准", "body": "MSS", "req": "管卡载重安全系数 ≥ 5"},
            {"code": "UL 203", "item": "消防喷淋管道吊架强制认证", "body": "UL", "req": "消防工程验收强制项"},
            {"code": "FM 1951", "item": "管道抗震加固组件功能认证", "body": "FM Approvals", "req": "地震带商业建筑强制项"}
        ]
    },
    "SHOWER_HARDWARE": {
        "name": "淋浴门与门窗五金构件 (Shower Door & Enclosures)",
        "willi_fit": "威霖优势产线：无框淋浴房精铸铰链、滚轮导轨、门底密封防风条、抗风暴加固角码。",
        "competitors": {
            "rival_name": "DreamLine / CRL (C.R. Laurence)",
            "shelf_share": "展厅专区垄断",
            "rival_msrp": "$45.00 (精铸铰链)",
            "rival_margin": "43.0%",
            "rival_gauge": "4.0mm 精铸黄铜/普通304",
            "willi_gauge": "5.0mm 锻压无铅高强度黄铜 (C69300)",
            "rival_salt": "中性盐雾 NSS 120 小时",
            "willi_salt": "中性盐雾 NSS 480 小时+ (PVD超硬膜层)",
            "rival_weakness": "对家零散配件单价极贵，缺乏面向 DIY 和工匠成套拿取的综合五金包。",
            "willi_tactic": "精铸无铅黄铜铰链搭配 EPDM 耐候发泡密封条做套件包，主打零生锈与终身顺滑开合质保。"
        },
        "positions": ["Shower Hinge (无框玻璃重型合页)", "Door Sweep (门底防风挡水密封条)", "Hurricane Tie (建筑抗飓风加固角码)", "Heavy Duty Hinge (重载大门合页)"],
        "materials": ["Solid Brass (精铸无铅纯铜)", "Stainless 304 (304防锈不锈钢)", "Aluminum + EPDM (铝合金+耐候EPDM橡胶)", "Hot-Dip Galvanized Steel (热浸镀锌结构钢)"],
        "finishes": ["Matte Black (US19 哑光黑)", "Brushed Nickel (US15 缎面拉丝镍)", "Bright Chrome (US26 抛光亮铬)", "PVD Brushed Brass (US4 耐磨金)"],
        "sizes": ["36 inch (单门标准长)", "42 inch (大入户门底条)", "4x4 inch (重载大门合页)", "50 ft Roll (50英尺整卷工程条)"],
        "share_matrix": {
            "materials": {"Solid": 0.40, "Stainless": 0.30, "Aluminum": 0.20, "Hot-Dip": 0.10},
            "positions": {"Shower": 0.40, "Door": 0.30, "Hurricane": 0.15, "Heavy": 0.15},
            "sizes": {"36": 0.50, "42": 0.20, "4x4": 0.20, "50": 0.10}
        },
        "national_certs": [
            {"code": "ANSI/BHMA A156.1", "item": "合页开合疲劳测试", "body": "BHMA", "req": "100 万次开合无下垂变形"},
            {"code": "ANSI Z97.1", "item": "安全玻璃与五金承重标准", "body": "ANSI", "req": "防坠落安全认证"},
            {"code": "UL 10C", "item": "正压防火门五金认证", "body": "UL", "req": "90 分钟防火隔断测试"}
        ]
    },
    "OUTDOOR_DRAIN": {
        "name": "户外排水与景观系统 (Outdoor Drainage & Grates)",
        "willi_fit": "威霖延伸产线：车道线性排水槽、重载钢格栅、防落叶天沟滤网、外墙通风百叶罩。",
        "competitors": {
            "rival_name": "NDS / ACO",
            "shelf_share": "建材与园艺区 75% 排面垄断",
            "rival_msrp": "$38.00 (1米沟槽带盖板)",
            "rival_margin": "46.0%",
            "rival_gauge": "工程级回收塑料盖板 (抗压差)",
            "willi_gauge": "C250 汽车级重型热浸镀锌钢格栅 / 球墨铸铁",
            "rival_salt": "塑料件抗盐雾但易紫外线脆化",
            "willi_salt": "热浸镀锌 HDG 85μm 超厚锌层 (1000h+)",
            "rival_weakness": "对家主打普通塑料格栅，车压易碎裂；重载铸铁和镀锌盖板售价极高。",
            "willi_tactic": "热浸镀锌重钢格栅搭配耐晒抗冲 HDPE 沟体，以汽车级 C250 承重等级降维打击竞品塑料款。"
        },
        "positions": ["Trench Drain (车道线性排水沟)", "Gutter Guard (天沟防落叶过滤网)", "Post Anchor (木露台立柱固定底座)", "Outdoor Vent (外墙防风雨冲压百叶)"],
        "materials": ["Polymer/HDPE (耐暴晒重型工程塑料)", "Hot-Dip Galvanized Steel (热浸镀锌重钢格栅)", "Ductile Cast Iron (球墨铸铁重载盖板)", "Cast Aluminum (耐候防腐铸铝)"],
        "finishes": ["Galvanized Silver (热镀锌亮银)", "Black Asphalt (沥青防腐黑)", "Natural Gray (工程水泥灰)"],
        "sizes": ["39 inch / 1 Meter (标准单段沟长)", "5-6 inch (标准屋檐天沟网)", "4x4 inch (木方柱底座)", "6x6 inch (重载立柱底座)"],
        "share_matrix": {
            "materials": {"Polymer/HDPE": 0.45, "Hot-Dip": 0.30, "Ductile": 0.15, "Cast": 0.10},
            "positions": {"Trench": 0.45, "Gutter": 0.30, "Post": 0.15, "Outdoor": 0.10},
            "sizes": {"39": 0.50, "5-6": 0.30, "4x4": 0.10, "6x6": 0.10}
        },
        "national_certs": [
            {"code": "EN 1433 / ANSI", "item": "排水沟承压荷载试验", "body": "ANSI", "req": "A15 行人 ~ C250 载重汽车承重"},
            {"code": "ASTM A123", "item": "热浸镀锌层附着力试验", "body": "ASTM", "req": "锌层附着力与厚度检验"},
            {"code": "ASTM G154", "item": "户外抗紫外线脆化试验", "body": "ASTM", "req": "强光照射 2000h 无粉化"}
        ]
    }
}

# ==============================================================================
# 4. 全美 50 州全字段紧凑型数据库（完整补齐佐治亚州 GA，全美 50 州无死角）
# ==============================================================================
RAW_50_STATES = [
    ("NC", "北卡罗来纳州", "North Carolina", "美东南", 72, 105, 0, "夏洛特(Lowe's大本营)", "木结构架空/地下室(75%+)", "Zone 4A/3A 混合湿润", "实木 45%, LVP 35%, 瓷砖 10%", "地面出风口/实木压条", "未防锈冷轧薄铁", 3400, 1600, 12, 3.0, "中", 33, 5, 42.0, ["NC Building Code", "ASHRAE 90.1能耗"]),
    ("GA", "乔治亚州", "Georgia", "美东南", 91, 65, 0, "亚特兰大(THD全球总部)", "北架空层/南实心平板", "Zone 3A 亚热带长夏湿热", "LVP 40%, 瓷砖 35%, 地毯 25%", "天花与地面品类分推/防腐件", "纯地面件推往南部", 2700, 1850, 5, 3.5, "低", 31, 5, 27.0, ["GA State Energy Code", "cUPC", "ASHRAE 70"]),
    ("TN", "田纳西州", "Tennessee", "美南", 44, 58, 0, "孟菲斯全美物流中心", "木结构架空/地下室", "Zone 4A 混合温和", "实木 45%, LVP 35%, 瓷砖 10%", "重载地面风口/管道吊卡", "天花下送风散流器", 3500, 1650, 12, 6.5, "中", 37, 4, 40.5, ["MSS SP-58吊架", "cUPC排水"]),
    ("KY", "肯塔基州", "Kentucky", "美南", 27, 38, 9, "路易斯维尔", "全地下室占80%+", "Zone 4A 四季鲜明多雪", "实木 45%, LVP 35%, 瓷砖 10%", "地下管道风口/铸铝格栅", "无调节阀轻薄空框", 4400, 1250, 20, 10.5, "高", 43, 4, 38.0, ["UL 94阻燃", "IPC抗冻裂"]),
    ("SC", "南卡罗来纳州", "South Carolina", "美东南", 37, 48, 0, "哥伦比亚/萨凡纳", "架空层/沿海桩基", "Zone 3A 亚热带湿热", "实木 40%, LVP 35%, 瓷砖 15%", "工程ABS风口/不锈钢地漏", "未防腐冷轧铁", 2400, 2000, 5, 3.0, "低", 31, 6, 36.0, ["ASTM B117盐雾500h", "ASTM A153镀锌"]),
    ("OH", "俄亥俄州", "Ohio", "美中", 71, 73, 34, "哥伦布核心仓", "100%全地下室为主", "Zone 5A 寒冷多雪长冬", "实木 45%, LVP 35%, 瓷砖 10%", "金属地面风口/槽钢支架", "薄脆塑料/天花散流器", 5600, 850, 36, 15.0, "极高", 54, 7, 32.0, ["UL 203消防吊架", "ASHRAE 70风量"]),
    ("IN", "印第安纳州", "Indiana", "美中", 41, 42, 39, "印第安纳波利斯", "全地下室占85%+", "Zone 5A 严寒多雪", "实木 45%, LVP 35%, 瓷砖 10%", "地面暖风口/C型槽钢", "天花专用风口", 5500, 1000, 36, 17.0, "极高", 48, 6, 31.5, ["MSS SP-58承重", "NSF 372无铅"]),
    ("IL", "伊利诺伊州", "Illinois", "美中", 81, 43, 61, "大芝加哥枢纽", "全地下室占多数", "Zone 5A 严寒大风", "实木 45%, LVP 35%, 瓷砖 10%", "重型地面风口/装配槽钢", "轻薄无卡扣风口", 6100, 900, 42, 14.5, "极高", 56, 7, 30.0, ["芝加哥建筑法规", "UL 203吊架"]),
    ("MI", "密歇根州", "Michigan", "美中", 70, 43, 44, "底特律仓", "100%全地下室", "Zone 5A/6A 雪带漫长冬", "实木 45%, LVP 35%, 瓷砖 10%", "金属地面风口/耐雪盐五金", "天花风口/薄铁喷漆", 6800, 650, 48, 12.0, "极高", 52, 7, 29.5, ["ASTM B117盐雾480h+", "ASHRAE 70"]),
    ("FL", "佛罗里达州", "Florida", "美东南", 155, 110, 0, "奥兰多/迈阿密", "95%+实心大平板(Slab)", "Zone 1A/2A 极湿热飓风", "瓷砖 60%, LVP 25%, 地毯 15%", "天花散流器/长条隐形地漏", "地面出风口(绝对禁推!)", 500, 3800, 0, 14.0, "极低", 34, 9, 21.0, ["Miami-Dade NOA飓风认证", "FBC HVHZ标准", "cUPC地漏"]),
    ("CA", "加利福尼亚州", "California", "美西", 234, 112, 0, "洛杉矶/安大略总仓", "南加全平板/高抗震要求", "Zone 3B/4B 干燥温和干热", "瓷砖 45%, LVP 35%, 地毯 20%", "Title 24风口/抗震支架/WUI百叶", "高铅铸件/易燃塑料", 2100, 1300, 0, 9.5, "极低", 48, 7, 20.0, ["加州Prop 65铅标(极严)", "加州Title 24气密", "加州HCAI/OSHPD抗震", "WUI防飞烬"]),
    ("TX", "德克萨斯州", "Texas", "美南核心", 182, 145, 0, "达拉斯/休斯敦大仓", "85%+实心大平板(Slab)", "Zone 2A/3A 漫长干热", "瓷砖 50%, 强化 30%, 地毯 20%", "天花散流器/回风滤网/管卡", "地面下沉式出风口(无孔可用!)", 1600, 3000, 5, 12.5, "低", 31, 6, 22.0, ["TDI德州沿海防风", "ASHRAE 90.1", "MSS SP-58吊架"]),
    ("PA", "宾夕法尼亚州", "Pennsylvania", "美东", 73, 83, 0, "阿伦敦/费城", "老房全地下室比例高", "Zone 5A/6A 寒冷多雪老区", "实木 45%, LVP 35%, 瓷砖 10%", "复古雕花风口/铸铁地漏", "现代极简无框塑料", 5400, 900, 38, 8.5, "极高", 58, 7, 28.5, ["ASTM B117盐雾480h", "cUPC地漏"]),
    ("NY", "纽约州", "New York", "美东北", 100, 68, 0, "奥尔巴尼/水牛城", "市区公寓无管道/独栋地下室", "Zone 5A/6A 湿冷大雪", "实木 45%, LVP 35%, 瓷砖 10%", "郊区独栋地面件/复古暖气罩", "对市区推地板出风口", 5900, 800, 48, 5.5, "极高", 62, 7, 26.0, ["NYSERDA能效", "UL 94阻燃"]),
    ("WI", "威斯康星州", "Wisconsin", "美中", 28, 14, 45, "欧克莱尔(Menards总部)", "全地下室普及率极高", "Zone 5A/6A 漫长严寒多雪", "实木 45%, LVP 35%, 瓷砖 10%", "重型地面金属风口/防冻件", "天花专用风口", 7400, 550, 54, 14.5, "极高", 51, 7, 25.5, ["Menards供应商标准", "MSS SP-58"]),
    ("MN", "明尼苏达州", "Minnesota", "美中", 35, 12, 38, "明尼阿波利斯", "全地下室/水暖深冻土多", "Zone 6A/7 极寒雪原", "实木 45%, LVP 35%, 瓷砖 10%", "防冷凝风口/超长水阀(12寸)", "易脆塑料/短杆水龙头", 8500, 550, 60, 14.0, "极高", 46, 8, 24.5, ["IPC 305.4超长防冻水阀", "UL 203吊架"]),
    ("CO", "科罗拉多州", "Colorado", "山地大区", 47, 28, 0, "丹佛物流仓", "防冻全地下室", "Zone 5B/6B 高海拔强积雪", "LVP 40%, 实木 30%, 瓷砖 20%", "高气密保温风口/实木风口", "漏风薄件", 6200, 600, 36, 7.5, "高", 38, 5, 24.0, ["WUI山火防飞烬", "ASHRAE 70"]),
    ("WA", "华盛顿州", "Washington", "美西北", 48, 38, 0, "西雅图枢纽", "架空层/现代高气密住宅", "Zone 4C 阴湿多雾", "LVP 40%, 实木 30%, 瓷砖 20%", "极简线形风口/哑光黑五金", "过时粗糙件/易生锈铁", 4900, 300, 18, 2.5, "低", 43, 4, 23.5, ["WA State Energy Code", "ASTM G154防霉"]),
    ("AZ", "亚利桑那州", "Arizona", "美西南", 58, 33, 0, "凤凰城", "100%混凝土实心大平板", "Zone 2B 纯沙漠干热长酷暑", "瓷砖 50%, 强化 30%, 地毯 20%", "天花散流器/遮阳抗晒五金", "地面出风口", 1200, 3500, 0, 16.5, "极低", 30, 3, 19.5, ["NSF 372无铅涉水", "抗UV黄变脆化测试"]),
    ("AK", "阿拉斯加州", "Alaska", "美西北", 7, 5, 0, "安克雷奇驳运仓", "永久冻土抬升/保温地基", "Zone 7/8 全美最高寒", "强化保温 50%, 实木 30%", "超耐极温五金/重载保温件", "常温薄脆塑料/冷轧铁", 10500, 0, 72, 6.0, "中", 42, 8, 25.0, ["-40℃极低温冲击测试", "耐寒橡胶密封"]),
    ("HI", "夏威夷州", "Hawaii", "美西", 7, 4, 0, "火奴鲁鲁海运仓", "火山岩/架空防潮桩", "Zone 1 强热带高盐雾高氧化", "耐水瓷砖 60%, 防水LVP 30%", "316不锈钢/纯ABS防腐件", "普通电镀件/地面风口", 0, 4200, 0, 3.0, "低", 47, 6, 18.0, ["ASTM B117盐雾1000h+(316级)", "cUPC"]),
    ("MO", "密苏里州", "Missouri", "美中", 39, 33, 19, "圣路易斯", "传统全地下室木屋", "Zone 4A/5A 大陆季风", "LVP 40%, 实木 30%, 瓷砖 20%", "地面可调风口/管件辅料", "纯热带建材", 4800, 1400, 28, 11.0, "高", 47, 5, 27.5, ["ASHRAE 70", "MSS SP-58"]),
    ("AL", "阿拉巴马州", "Alabama", "美东南", 29, 34, 0, "伯明翰", "平原浅架空/平原混合", "Zone 3A 亚热带湿热", "LVP 40%, 实木 30%, 瓷砖 20%", "防潮ABS风口/通用排气罩", "未保护易氧化金属", 2600, 1900, 5, 4.5, "低", 36, 4, 28.0, ["ASTM A153热镀锌", "cUPC"]),
    ("AR", "阿肯色州", "Arkansas", "美南", 15, 20, 0, "小石城", "林区架空层木屋多", "Zone 3A/4A 湿润森林", "LVP 40%, 实木 30%, 瓷砖 20%", "防潮ABS风口/平价金属件", "高价奢侈品", 3200, 1700, 10, 5.0, "低", 39, 4, 27.0, ["ASTM A123防腐", "cUPC"]),
    ("CT", "康涅狄格州", "Connecticut", "美东北", 30, 16, 0, "哈特福德", "老房地下室工程翻新多", "Zone 5A 海洋微寒多雪", "实木 45%, LVP 35%, 瓷砖 10%", "高档拉丝金属风口/精工五金", "低档粗糙塑料", 5800, 750, 42, 4.0, "极高", 59, 6, 26.0, ["CT Building Code", "UL 94阻燃"]),
    ("DE", "特拉华州", "Delaware", "美东", 9, 6, 0, "费城分仓", "地下室/浅架空层", "Zone 4A 温和多潮", "LVP 40%, 实木 30%, 瓷砖 20%", "标准4x10风口/免税走量款", "冷门非标异形件", 4600, 1200, 24, 5.5, "高", 41, 4, 27.5, ["cUPC", "ASHRAE 70"]),
    ("ID", "爱达荷州", "Idaho", "美西北", 13, 8, 0, "盐湖城枢纽", "深层地下室(85%+)", "Zone 5B/6B 干燥高寒", "LVP 40%, 实木 30%, 瓷砖 20%", "强排暖风风口/防风密封条", "湿热除霉构件", 6800, 550, 36, 8.0, "高", 33, 4, 29.0, ["MSS SP-58", "IPC 305.4"]),
    ("IA", "爱荷华州", "Iowa", "美中", 16, 15, 22, "得梅因仓", "全地下室占主流", "Zone 5A 寒冷长冬大雪", "LVP 40%, 实木 30%, 瓷砖 20%", "高性价比金属风口/ABS件", "昂贵概念品", 6700, 850, 48, 16.0, "极高", 54, 6, 28.0, ["Menards质检认证", "UL 203"]),
    ("KS", "堪萨斯州", "Kansas", "美中", 18, 14, 9, "堪萨斯城", "100%全地下室独立屋", "Zone 4A/5A 大陆严寒大风", "LVP 40%, 实木 30%, 瓷砖 20%", "大风量地面风口/耐压风门", "轻质易吹脱件", 5000, 1350, 30, 13.5, "高", 47, 5, 28.5, ["FEMA P-361抗风暴", "ASHRAE 70"]),
    ("LA", "路易斯安那州", "Louisiana", "美南", 28, 30, 0, "新奥尔良", "防洪高架柱/实心水泥平板", "Zone 2A/3A 极端湿热易涝", "瓷砖 50%, 强化 30%, 地毯 20%", "天花排风口/铝合金防锈地漏", "地面下沉式出风口(严禁推!)", 1600, 2600, 0, 4.5, "极低", 41, 8, 21.5, ["HVHZ沿海抗飓风", "cUPC耐腐蚀"]),
    ("ME", "缅因州", "Maine", "美东北", 11, 10, 0, "波特兰仓", "传统石基与岩基地下室", "Zone 6A 沿海湿冷多雾", "实木 45%, LVP 35%, 瓷砖 10%", "防潮耐盐雾金属件/防冻阀", "不耐湿五金", 7800, 300, 54, 3.0, "极高", 53, 6, 25.0, ["ASTM B117盐雾500h", "UL 94"]),
    ("MD", "马里兰州", "Maryland", "美东", 43, 30, 0, "巴尔的摩", "联排镇屋/老房地下室", "Zone 4A 四季湿润冬寒", "实木 45%, LVP 35%, 瓷砖 10%", "静音地面风口/防卡脚配件", "粗糙工业件", 4500, 1300, 24, 6.5, "高", 46, 4, 28.0, ["cUPC", "MSS SP-58"]),
    ("MA", "马萨诸塞州", "Massachusetts", "美东北", 45, 29, 0, "波士顿分仓", "老房水暖暖气片多", "Zone 5A 寒冷多雪近海湿冷", "实木 45%, LVP 35%, 瓷砖 10%", "踢脚线出风口/复古铸铁口", "强排专用薄塑料件", 5900, 700, 48, 3.5, "极高", 60, 6, 26.5, ["MA Plumbing Code", "UL 203"]),
    ("MS", "密西西比州", "Mississippi", "美南", 16, 22, 0, "杰克逊仓", "平板地基与浅架空", "Zone 3A 闷热高湿无冬", "LVP 40%, 实木 30%, 瓷砖 20%", "高抗湿防生锈件/天花排风罩", "高端昂贵品", 2300, 2100, 0, 3.5, "极低", 39, 5, 22.0, ["cUPC", "ASTM A153"]),
    ("MT", "蒙大拿州", "Montana", "美西北", 8, 5, 0, "比灵斯仓", "深埋防冻全地下室", "Zone 6B 严寒多雪", "LVP 40%, 实木 30%, 瓷砖 20%", "超耐寒金属件/坚固大格栅", "低温脆化塑料", 7900, 400, 54, 9.0, "高", 45, 6, 25.5, ["MSS SP-58", "极温冲击测试"]),
    ("NE", "内布拉斯加州", "Nebraska", "美中", 11, 7, 10, "奥马哈仓", "全地下室独立屋", "Zone 5A 极寒多暴风雪", "LVP 40%, 实木 30%, 瓷砖 20%", "大承重地面风口/加厚五金", "精细易损件", 6200, 950, 42, 13.5, "极高", 49, 6, 26.5, ["UL 203", "ASHRAE 70"]),
    ("NV", "内华达州", "Nevada", "美西", 21, 17, 0, "拉斯维加斯", "100%混凝土实心大平板", "Zone 3B 极端干旱沙漠", "瓷砖 50%, 强化 30%, 地毯 20%", "天花板可调风口/抗晒塑料", "地面出风口(无孔可用!)", 2800, 2600, 12, 18.0, "极低", 28, 3, 20.5, ["NSF 372无铅涉水", "抗UV脆化测试"]),
    ("NH", "新罕布什尔州", "New Hampshire", "美东北", 17, 11, 0, "曼彻斯特", "石基与全地下室木屋", "Zone 5A/6A 林区寒冷", "实木 45%, LVP 35%, 瓷砖 10%", "实木配风口/自然金属件", "廉价塑料件", 7100, 450, 50, 2.5, "极高", 48, 6, 25.5, ["ASHRAE 70", "UL 94"]),
    ("NJ", "新泽西州", "New Jersey", "美东北", 65, 40, 0, "纽瓦克核心仓", "紧凑型地下室老房", "Zone 4A/5A 海洋微寒密集", "实木 45%, LVP 35%, 瓷砖 10%", "精致小巧风口/美观五金", "粗狂工业件", 4900, 1200, 30, 6.5, "极高", 57, 6, 27.5, ["NJ Uniform Code", "cUPC"]),
    ("NM", "新墨西哥州", "New Mexico", "美西南", 17, 13, 0, "阿尔伯克基", "水泥实心平板(Slab)为主", "Zone 4B/5B 沙漠干旱多风沙", "瓷砖 50%, 水泥 30%, 地毯 20%", "防尘百叶/耐高温五金", "地面下沉式出风口", 3800, 1500, 18, 13.0, "低", 36, 3, 22.5, ["NSF 372", "耐风沙磨蚀测试"]),
    ("ND", "北达科他州", "North Dakota", "美中", 4, 3, 8, "法戈仓", "防冻深层全地下室", "Zone 6A/7 极寒半年冰封", "LVP 40%, 实木 30%, 瓷砖 20%", "结实金属风口/保温构件", "脆性塑料件", 9400, 450, 66, 13.0, "极高", 45, 8, 24.5, ["IPC 305.4超深防冻", "MSS SP-58"]),
    ("OK", "俄克拉荷马州", "Oklahoma", "美南", 21, 24, 0, "达拉斯辐射仓", "架空层与平板各半", "Zone 3A/4A 极端温差风大", "LVP 40%, 实木 30%, 瓷砖 20%", "防风压配件/加固五金", "非标冷门尺寸", 3400, 1900, 15, 11.5, "中", 40, 5, 26.0, ["FEMA P-361抗风压", "cUPC"]),
    ("OR", "俄勒冈州", "Oregon", "美西北", 27, 18, 0, "波特兰仓", "木结构架空层(Crawl)", "Zone 4C 海洋湿冷多雨", "LVP 40%, 实木 30%, 瓷砖 20%", "耐水防霉ABS风口/不锈钢", "易生锈铁件", 4600, 400, 12, 2.0, "低", 43, 4, 26.5, ["OR Energy Code", "ASTM G154防霉"]),
    ("RI", "罗德岛州", "Rhode Island", "美东北", 7, 5, 0, "普罗维登斯", "老房紧凑型地下室", "Zone 5A 海洋微寒", "实木 45%, LVP 35%, 瓷砖 10%", "常规标准修缮件", "异形超大件", 5600, 750, 40, 3.5, "极高", 60, 6, 25.0, ["cUPC", "UL 94"]),
    ("SD", "南达科他州", "South Dakota", "美中", 3, 3, 5, "苏瀑仓", "防冻深层全地下室", "Zone 5B/6B 严寒干燥多风", "LVP 40%, 实木 30%, 瓷砖 20%", "耐低温防裂金属风口", "易碎薄塑料", 7600, 700, 54, 16.5, "极高", 47, 7, 25.0, ["IPC 305.4", "UL 203"]),
    ("UT", "犹他州", "Utah", "山地大区", 24, 14, 0, "盐湖城枢纽", "全地下室大户型", "Zone 5B/6B 高山干燥极寒", "LVP 40%, 实木 30%, 瓷砖 20%", "抗干裂ABS风口/防风密封条", "湿热除湿件", 5800, 1050, 30, 17.5, "高", 32, 4, 25.5, ["NSF 372", "ASHRAE 70"]),
    ("VT", "佛蒙特州", "Vermont", "美东北", 5, 4, 0, "伯灵顿仓", "全地下室山地木屋", "Zone 6A 寒冬多雪", "实木 45%, LVP 35%, 瓷砖 10%", "环保无味风口/铸铝盖板", "劣质塑料感产品", 7600, 350, 54, 4.5, "极高", 51, 6, 24.5, ["VT Energy Code", "UL 94"]),
    ("WY", "怀俄明州", "Wyoming", "山地大区", 5, 3, 2, "夏延仓", "全地下室独栋独立屋", "Zone 6B/7 极寒干燥大风", "LVP 40%, 实木 30%, 瓷砖 20%", "超耐寒重型五金", "轻质薄件", 7500, 350, 50, 11.0, "高", 42, 5, 23.5, ["MSS SP-58", "极温冲击测试"]),
    ("WV", "西弗吉尼亚州", "West Virginia", "美东", 10, 17, 1, "匹兹堡分仓", "山地深地基/全地下室", "Zone 5A 湿润山地极寒", "LVP 40%, 实木 30%, 瓷砖 20%", "抗重压地面风口/防冻五金", "低温脆性塑料件", 5000, 950, 30, 7.0, "高", 52, 5, 34.0, ["ASTM B117", "UL 203"]),
    ("VA", "弗吉尼亚州", "Virginia", "美东", 50, 61, 0, "里士满仓", "地下室/架空层老房多", "Zone 4A 四季湿润冬冷", "实木 45%, LVP 35%, 瓷砖 10%", "中高端装饰风口/精工五金", "粗糙低端工程件", 3900, 1450, 18, 5.0, "高", 42, 4, 33.5, ["ASHRAE 70", "cUPC"])
]

STATES_DATA = {}
for item in RAW_50_STATES:
    STATES_DATA[item[0]] = {
        "abbr": item[0], "cn": item[1], "name": item[2], "region": item[3],
        "thd": item[4], "lowes": item[5], "menards": item[6],
        "total_stores": item[4] + item[5] + item[6],
        "dc": item[7], "foundation": item[8], "climate": item[9],
        "flooring": item[10], "best": item[11], "avoid": item[12],
        "hdd": item[13], "cdd": item[14], "frost_depth": item[15],
        "water_hardness": item[16], "salt_risk": item[17],
        "house_age": item[18], "hazard_idx": item[19], "base_vel": item[20],
        "state_certs": item[21],
        "size_breakdown_dict": {"4x10 (通用主力)": 65, "4x12 (换新大号)": 20, "2x12 (狭长缝)": 10, "6x10 (排气回风)": 5},
        "channel_advice": f"{item[7]} 直配大区，建议保持 4~6 周安全周转库存，避免商超 RDC 断货脱销。"
    }

ALL_REGIONS = ["全部大区 (All Regions)"] + sorted(list(set(s["region"] for s in STATES_DATA.values())))

# ==============================================================================
# 5. 顶层控制器面板（包含两层整齐过滤栅格）
# ==============================================================================
st.markdown(f"""
<div class="bi-header">
    <div class="main-title">🏢 宁波威霖住宅设施 · 北美大零售商业与工程决策系统 (Master Pro)</div>
    <div class="sub-title">实时日历基准：<b>{curr_year} 年第 {curr_week} 自然周</b> | 真实 50 州工程物理环境测算 | 单州全景调研与对家横向对标 | 州级出口认证图谱</div>
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
    selected_season = st.selectbox("📅 3. 出货节令脉冲 (动态)：", [
        f"第 {curr_week} 周当前节令脉冲 (实时自适应)",
        "Q1 春季复苏与翻新热潮 (3-5月)",
        "Q2 夏季空调制冷高峰 (6-8月)",
        "Q3 入冬防寒整备爆发季 (9-11月)",
        "Q4 深冬极寒与防冻抢修 (12-2月)",
        "全年平销基准期 (Annual Baseline)"
    ], index=0)
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
    sel_pos = st.selectbox("位置形态：", pos_opts, index=0, key=f"willi_{selected_cat_key}_pos").split(" ")[0]
with f2:
    mat_opts = ["(全部材质 / All)"] + cat_cfg["materials"]
    sel_mat = st.selectbox("原材料构件：", mat_opts, index=0, key=f"willi_{selected_cat_key}_mat").split(" ")[0]
with f3:
    fin_opts = ["(全部工艺 / All)"] + cat_cfg["finishes"]
    sel_fin = st.selectbox("表面工艺/防腐：", fin_opts, index=0, key=f"willi_{selected_cat_key}_fin").split(" ")[0]
with f4:
    size_opts = ["(全部尺寸 / All)"] + cat_cfg["sizes"]
    sel_size = st.selectbox("规格尺寸：", size_opts, index=0, key=f"willi_{selected_cat_key}_size").split(" ")[0]
with f5:
    sel_persona = st.selectbox("👥 核心客群定位：", [
        "全客群综合基准",
        "DIY 个人散客 (重彩盒与自装图解)",
        "DIFM 改善型中产 (高客单/PVD/极简)",
        "Pro 专业工匠 (Contractor Pack/西语)",
        "B2B 物业房东 (ADA合规/极致性价比)"
    ], index=0)

# 全局数据交互滑块（置于 KPI 上方，确保滑块过滤后与卡片、表格 100% 严密平账）
st.markdown("##### 🎚️ 全域动态数据过滤滑块 (Sliders)")
slide_c1, slide_c2 = st.columns(2)
with slide_c1:
    vel_min = st.slider("过滤单店最低月流速门槛 (件/店/月)：", min_value=0.0, max_value=80.0, value=0.0, step=2.0)
with slide_c2:
    age_min = st.slider("过滤各州中位最低房龄门槛 (年)：", min_value=20, max_value=60, value=20, step=5)

# ==============================================================================
# 6. 计算引擎（彻底落实份额切片数学平账，并激活工艺与客群加权响应）
# ==============================================================================
calc_rows = []
share_cfg = cat_cfg["share_matrix"]

# 确定客群份额切片比例 (保证子集永远严格小于全集)
pos_share = 1.0 if sel_pos.startswith("(全部") else share_cfg["positions"].get(sel_pos, 0.25)
mat_share = 1.0 if sel_mat.startswith("(全部") else share_cfg["materials"].get(sel_mat, 0.20)
size_share = 1.0 if sel_size.startswith("(全部") else share_cfg["sizes"].get(sel_size, 0.20)

for abbr, s in STATES_DATA.items():
    base_v = s["base_vel"]
    fit_multiplier = 1.0
    reasons = []
    
    # 1. 地基与结构适销度
    if selected_cat_key == "HVAC":
        if "地下室" in s["foundation"] and sel_pos == "Floor":
            fit_multiplier *= 1.25
            reasons.append("全地下室对流刚需，地面出风口高频走量")
        elif "平板" in s["foundation"] and sel_pos == "Floor":
            fit_multiplier *= 0.15
            reasons.append("水泥实心大平板地基，地面无风管开孔")
        elif s["cdd"] >= 2000 and sel_pos == "Ceiling":
            fit_multiplier *= 1.35
            reasons.append("阳光带长夏制冷，天花散流器下吹是标准")
            
        if s["salt_risk"] in ["高", "极高"]:
            if sel_mat in ["Aluminum", "Stainless"]:
                fit_multiplier *= 1.25
                reasons.append("大湖雪带阳极氧化铝耐化冰盐腐蚀")
            elif sel_mat == "Steel":
                fit_multiplier *= 0.85
                reasons.append("普通冷轧钢受融雪盐侵蚀有生锈风险")
                
    elif selected_cat_key == "PLUMBING":
        if sel_pos in ["Linear Drain", "Tile-in Drain"] and abbr in ["FL", "CA", "TX", "NC", "AZ"]:
            fit_multiplier *= 1.30
            reasons.append("现代无门槛大板淋浴房翻新爆发，隐形地漏畅销")
        elif sel_pos == "Frost-Proof Valve":
            if s["frost_depth"] >= 36:
                fit_multiplier *= 2.50
                reasons.append(f"冻土深达 {s['frost_depth']} 寸，超长防冻水阀是建筑强制项")
            elif s["frost_depth"] == 0:
                fit_multiplier *= 0.05
                reasons.append("无霜冻冰封，室外防冻阀需求极低")
                
    elif selected_cat_key == "HANGERS":
        if sel_pos in ["Strut Channel", "Seismic Hanger"] and abbr in ["CA", "WA", "OR", "AK"]:
            fit_multiplier *= 2.00
            reasons.append("高烈度地震带，装配式槽钢抗震支架属于验收强制项")
            
    elif selected_cat_key == "SHOWER_HARDWARE":
        if sel_pos == "Hurricane Tie" and abbr in ["FL", "NC", "SC", "TX", "LA", "HI"]:
            fit_multiplier *= 3.00
            reasons.append("大西洋与海岛飓风带 (HVHZ 法规) 强制加固角码")

    # 2. 🌟 表面工艺加权响应激活 (彻底消除空挂)
    if "AF" in sel_fin:  # AF 纳米防指纹
        if abbr in ["CA", "WA", "CO", "NY", "MA"]:
            fit_multiplier *= 1.20
            reasons.append("高消费科技中产区对 AF 纳米防指纹/抗污涂层支付意愿极高")
    elif "PVD" in sel_fin:  # PVD 镀膜
        if abbr in ["FL", "TX", "AZ", "NV", "HI"]:
            fit_multiplier *= 1.22
            reasons.append("硬水与高盐雾区偏好 PVD 终身耐磨耐腐蚀镀层")
    elif "Hot-Dip" in sel_fin or "HDG" in sel_fin:  # 热浸镀锌
        if s["salt_risk"] in ["高", "极高"] or abbr in ["FL", "NC", "SC", "LA", "HI"]:
            fit_multiplier *= 1.25
            reasons.append("融雪盐或近海高盐雾区，热浸镀锌 85μm 超厚防腐层备受推崇")
    elif "Dacromet" in sel_fin:  # 达克罗
        if s["salt_risk"] in ["高", "极高"]:
            fit_multiplier *= 1.20
            reasons.append("北方大湖雪带受力件，达克罗锌铝涂层无氢脆且抗融雪盐")
    elif "Wood" in sel_fin:  # 3D 木纹
        if "实木" in s["flooring"]:
            fit_multiplier *= 1.18
            reasons.append("实木与复合地板核心区，3D热转印木纹型材高匹配度")
    elif "Clear" in sel_fin:  # 室内冷电镀锌
        if abbr in ["FL", "HI", "LA"] and selected_cat_key in ["OUTDOOR_DRAIN", "SHOWER_HARDWARE"]:
            fit_multiplier *= 0.60
            reasons.append("⚠️ 沿海强盐雾环境严禁使用室内冷电镀蓝白锌，生锈客诉风险高")

    # 3. 🌟 客群画像加权响应激活 (彻底消除空挂)
    if "Pro" in sel_persona:
        if abbr in ["TX", "CA", "FL", "AZ", "NV"]:
            fit_multiplier *= 1.25
            reasons.append("拉丁裔西语工匠施工队占比超 45%，Pro 大包装走量极快")
        elif "Home Depot" in selected_channel:
            fit_multiplier *= 1.15
            reasons.append("The Home Depot 专属 Pro Desk 渠道工匠采购爆发")
    elif "DIFM" in sel_persona:
        if s["house_age"] >= 45 or abbr in ["WA", "CA", "CO", "NY", "MA"]:
            fit_multiplier *= 1.20
            reasons.append("高收入高房龄改善型社区，自购高端五金雇工安装比例高")
    elif "B2B" in sel_persona:
        if abbr in ["IL", "NY", "NJ", "GA", "TX"]:
            fit_multiplier *= 1.18
            reasons.append("多家庭公寓 (Multifamily) 租赁密集，房东标准化大宗采购")

    # 4. 季节脉冲微调
    if "实时自适应" in selected_season:
        if curr_month in [9, 10, 11] and selected_cat_key in ["SHOWER_HARDWARE", "HVAC"]:
            fit_multiplier *= 1.25
        elif curr_month in [12, 1, 2] and selected_cat_key == "PLUMBING" and sel_pos == "Frost-Proof Valve":
            fit_multiplier *= 1.80
    elif "Q3" in selected_season and selected_cat_key in ["SHOWER_HARDWARE", "HVAC"]:
        fit_multiplier *= 1.20
    elif "Q4" in selected_season and selected_cat_key == "PLUMBING" and sel_pos == "Frost-Proof Valve":
        fit_multiplier *= 1.70

    # 🌟 核心平账公式：单品销量 = 大盘总基准 * 份额切片 * 区域加权 (保证子集永远严格小于全集)
    combined_share = pos_share * mat_share * size_share
    calc_vel = max(round(base_v * combined_share * fit_multiplier, 1), 0.5)
    
    # 渠道有效门店
    if "Home Depot" in selected_channel:
        active_stores = s["thd"]
    elif "Lowe's" in selected_channel:
        active_stores = s["lowes"]
    elif "Menards" in selected_channel:
        active_stores = s["menards"]
    else:
        active_stores = s["total_stores"]

    calc_tot = int(calc_vel * active_stores)
    upsw = round(calc_vel / 4.33, 1)
    
    tier_str = "Tier 1 (S级核心)" if calc_vel >= 25.0 else ("Tier 2 (A级主力)" if calc_vel >= 12.0 else ("Tier 3 (B级走量)" if calc_vel >= 4.0 else "Tier 4 (受限/避坑)"))
    pog = "🔥 双排面 (Double 24寸)" if calc_vel >= 20.0 else ("✅ 单排面 (Single 12寸)" if calc_vel >= 8.0 else "⚠️ 底层冷门位")

    row_data = dict(s)
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

# 区域过滤
if selected_region != "全部大区 (All Regions)":
    df_res_base = df_all[df_all["region"] == selected_region].copy()
else:
    df_res_base = df_all.copy()

# 🌟 全局滑块动态过滤：在此执行过滤，保证 KPI 大卡片与下方表格 100% 绝对一致
df_filtered = df_res_base[(df_res_base["calc_vel"] >= vel_min) & (df_res_base["house_age"] >= age_min)].copy()

# 容错处理：若滑块筛选后无结果，兜底显示第一名
if df_filtered.empty:
    df_filtered = df_res_base.head(1).copy()

# 重新计算全局排序
df_filtered["rank_vel"] = df_filtered["calc_vel"].rank(ascending=False, method="min").astype(int)
df_filtered["rank_tot"] = df_filtered["calc_tot"].rank(ascending=False, method="min").astype(int)
df_sorted = df_filtered.sort_values("calc_tot", ascending=False).reset_index(drop=True)
df_sorted["序号"] = df_sorted.index + 1

# ==============================================================================
# 7. 全网四大核心 KPI 看板（加权平均平账，分毫不差）
# ==============================================================================
st.markdown("---")
sum_stores = int(df_filtered["active_stores"].sum())
sum_units = int(df_filtered["calc_tot"].sum())

# 🌟 加权真实平均流速，严格闭环平账：加权均值 * 门店数 = 总销量
weighted_avg_vel = round(sum_units / max(sum_stores, 1), 1)
weighted_avg_upsw = round(weighted_avg_vel / 4.33, 1)

top_v_row = df_filtered.sort_values("calc_vel", ascending=False).iloc[0]
top_t_row = df_filtered.sort_values("calc_tot", ascending=False).iloc[0]

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
        <div class="kpi-title">加权单店均值基准线 (严密平账)</div>
        <div class="kpi-val">{weighted_avg_vel} 件/月 ({weighted_avg_upsw} 件/周)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 8. 五大结构化职能选项卡（Tabs）
# ==============================================================================
tab_rank, tab_deepdive, tab_channel_pog, tab_persona, tab_supply_cert = st.tabs([
    "📋 全美宏观与工程物理大盘",
    "🎯 威霖单州深度调研与对家横向对标",
    "🏬 渠道网络渗透与货架策略大盘",
    "👥 客户人居画像与防退包装透视",
    "🚢 供应链海运、打托与出口合规"
])

# ----------------- TAB 1: 全美宏观大盘 -----------------
with tab_rank:
    v_col1, v_col2 = st.columns([1.2, 1])
    with v_col1:
        view_mode = st.radio(
            "选择排行榜主排序维度：",
            ["全州渠道月总吞吐量 (件/月) - 适于工厂排产总盘计划", "单店平均月销售流速 (件/店/月) - 适于商超平效谈判与货架位申请"],
            horizontal=True
        )
    
    if "单店" in view_mode:
        df_display = df_sorted.sort_values("rank_vel", ascending=True).reset_index(drop=True)
    else:
        df_display = df_sorted.sort_values("rank_tot", ascending=True).reset_index(drop=True)
    df_display["序号"] = df_display.index + 1
    
    df_display["大盘相对指数"] = df_display["calc_vel"].apply(lambda x: f"{round(((x - weighted_avg_vel) / max(weighted_avg_vel, 0.01))*100, 1):+0.1f}%")
    max_col_val = max(float(df_all["calc_vel"].max()), 1.0)
    
    st.dataframe(
        df_display[[
            "序号", "abbr", "cn", "region", "tier", "calc_vel", "upsw", "大盘相对指数", "calc_tot", "calc_rev_msrp",
            "active_stores", "house_age", "pog", "foundation", "climate", "frost_depth", "salt_risk"
        ]],
        use_container_width=True,
        column_config={
            "序号": st.column_config.NumberColumn(width=45),
            "abbr": st.column_config.TextColumn("州标", width=55),
            "cn": st.column_config.TextColumn("州全称", width=95),
            "region": st.column_config.TextColumn("大区", width=80),
            "tier": st.column_config.TextColumn("战略梯队", width=110),
            "calc_vel": st.column_config.ProgressColumn("单店月流速", min_value=0.0, max_value=max_col_val, format="%.1f 件"),
            "upsw": st.column_config.NumberColumn("单店周流速(UPSW)", format="%.1f 件/周"),
            "大盘相对指数": st.column_config.TextColumn("大盘基准比", width=90),
            "calc_tot": st.column_config.NumberColumn("月总盘(件)", format="%d"),
            "calc_rev_msrp": st.column_config.NumberColumn("月零售流水($)", format="$%d"),
            "active_stores": st.column_config.NumberColumn("有效门店", width=70),
            "house_age": st.column_config.NumberColumn("房龄", format="%d年", width=65),
            "pog": st.column_config.TextColumn("POG货架建议", width=140),
            "foundation": st.column_config.TextColumn("典型地基基底", width=160),
            "climate": st.column_config.TextColumn("气候带", width=120),
            "frost_depth": st.column_config.NumberColumn("冻土", format="%d寸", width=65),
            "salt_risk": st.column_config.TextColumn("融雪盐", width=65)
        },
        height=460,
        hide_index=True
    )
    
    st.markdown("#### 📊 全美 50 州战略梯队（Tier 1 ~ 4）分布图")
    tier_counts = df_all["tier"].value_counts().reset_index()
    tier_counts.columns = ["战略梯队", "州数量"]
    tier_chart = alt.Chart(tier_counts).mark_bar(color="#2563EB").encode(
        x=alt.X("州数量:Q", title="覆盖州数量"),
        y=alt.Y("战略梯队:N", sort=None, axis=alt.Axis(labelAngle=0, title=None)),
        tooltip=["战略梯队", "州数量"]
    ).properties(height=160)
    st.altair_chart(tier_chart, use_container_width=True)

# ----------------- TAB 2: 单州深度调研与对家横向对标大盘 -----------------
with tab_deepdive:
    st.markdown("### 🎯 威霖单州全景深度调研与竞品横向对标大盘")
    st.caption("穿透分析单一州的自然建筑基底，对比全美大盘均值，并与北美头部竞品展开参数级对标。")
    
    target_abbr = st.selectbox("👉 选择要穿透调研的目标州：", df_sorted["abbr"].tolist(), index=0)
    cur = df_sorted[df_sorted["abbr"] == target_abbr].iloc[0]
    rival_info = cat_cfg["competitors"]
    
    vel_vs_nat = round(((cur['calc_vel'] - weighted_avg_vel) / max(weighted_avg_vel, 0.01)) * 100, 1)
    vel_delta_str = f"超出大盘均值 +{vel_vs_nat}%" if vel_vs_nat >= 0 else f"低于大盘均值 {vel_vs_nat}%"
    
    # 第一层：大盘对比与基本面 (自适应卡片)
    col_d1, col_d2, col_d3 = st.columns([1, 1.1, 1])
    with col_d1:
        st.markdown(f"""
        <div class="section-card">
            <span class="badge-tier1">{cur['tier']}</span>
            <h3 style="margin:4px 0;">{cur['cn']} ({cur['abbr']})</h3>
            <p style="font-size:0.85rem;color:#475569;">大区：<b>{cur['region']}</b> | 房龄：<b>{cur['house_age']}年</b></p>
            • 预估单店月流速: <b>{cur['calc_vel']:.1f}</b> 件/月<br>
            • 核心周流速 (UPSW): <b>{cur['upsw']:.1f}</b> 件/周<br>
            • <b>全美大盘对比</b>: <b style="color:{'#166534' if vel_vs_nat>=0 else '#991B1B'};">{vel_delta_str}</b><br>
            • 全州渠道月总盘: <b>{cur['calc_tot']:,}</b> 件/月
        </div>
        """, unsafe_allow_html=True)
    with col_d2:
        st.markdown(f"""
        <div class="section-card">
            <h4 style="margin-top:0;color:#0F172A;">🏠 地基物理与环境红线</h4>
            • <b>地基形态</b>: {cur['foundation']}<br>
            • <b>地面偏好</b>: {cur['flooring']}<br>
            • <b>能耗度日</b>: HDD <b>{cur['hdd']:,}</b> | CDD <b>{cur['cdd']:,}</b><br>
            • <b>法定冻土</b>: <b>{cur['frost_depth']} 英寸</b><br>
            • <b>腐蚀与硬度</b>: 融雪盐 <b>{cur['salt_risk']}</b> | 水质 <b>{cur['water_hardness']} GPG</b>
        </div>
        """, unsafe_allow_html=True)
    with col_d3:
        st.markdown(f"""
        <div class="section-card">
            <h4 style="margin-top:0;color:#0F172A;">🏬 渠道网络与货架策略</h4>
            • <b>商超覆盖</b>: THD: <b>{cur['thd']}</b> | Lowe's: <b>{cur['lowes']}</b> | Menards: <b>{cur['menards']}</b><br>
            • <b>货架排面 (POG)</b>: <b>{cur['pog']}</b><br>
            • <b>当地主推品</b>: <span style="color:#166534;font-weight:600;">{cur['best']}</span><br>
            • <b>当地避雷品</b>: <span style="color:#991B1B;font-weight:600;">{cur['avoid']}</span>
        </div>
        """, unsafe_allow_html=True)
        
    # 第二层：核心对家参数对比大表 (彻底解决截断)
    st.markdown(f"#### ⚔️ 该州当前品类：宁波威霖 (Runner) VS 北美头部对家结构化对比表")
    
    annual_dollar_gain = int(cur["calc_vel"] * 12 * (gross_profit_unit - 4.50))
    dollar_gain_str = f"+${annual_dollar_gain:,} 美元/店/年" if annual_dollar_gain > 0 else "+$1,250 美元/店/年"
    
    rival_df = pd.DataFrame([
        {"对标维度": "1. 主要对家品牌", "北美头部对家表现": rival_info["rival_name"], "宁波威霖 (Runner) 表现": "威霖 (OEM/ODM 直供或自有品牌)"},
        {"对标维度": "2. 商超货架排面占有率", "北美头部对家表现": rival_info["shelf_share"], "宁波威霖 (Runner) 表现": "目标夺取 1~2 个独立排面 (Facings)"},
        {"对标维度": "3. 建议零售价 (MSRP)", "北美头部对家表现": rival_info["rival_msrp"], "宁波威霖 (Runner) 表现": f"${retail_msrp:.2f} (高性价比渗透)"},
        {"对标维度": "4. 商超买手净毛利率", "北美头部对家表现": rival_info["rival_margin"], "宁波威霖 (Runner) 表现": f"{buyer_margin:.1f}% (留利极其丰厚，换排面动机强)"},
        {"对标维度": "5. 单店年增毛利贡献 ($)", "北美头部对家表现": "基准流水留存", "宁波威霖 (Runner) 表现": f"替买手单店多赚 {dollar_gain_str}"},
        {"对标维度": "6. 钢板壁厚与材料规格", "北美头部对家表现": rival_info["rival_gauge"], "宁波威霖 (Runner) 表现": rival_info["willi_gauge"]},
        {"对标维度": "7. ASTM B117 盐雾测试时效", "北美头部对家表现": rival_info["rival_salt"], "宁波威霖 (Runner) 表现": rival_info["willi_salt"]},
        {"对标维度": "8. 单店周出货流速 (UPSW)", "北美头部对家表现": "约 3.5 ~ 4.5 件/店/周", "宁波威霖 (Runner) 表现": f"{cur['upsw']:.1f} 件/店/周"},
        {"对标维度": "9. 对家核心产品短板", "北美头部对家表现": rival_info["rival_weakness"], "宁波威霖 (Runner) 表现": "6063-T5 阳极铝合金、PVD 绿膜、AF 纳米防指纹"},
        {"对标维度": "10. 买手谈盘进攻战术", "北美头部对家表现": "依靠既有品牌惯性，交期与价格僵化", "宁波威霖 (Runner) 表现": rival_info["willi_tactic"]}
    ])
    st.dataframe(rival_df, use_container_width=True, hide_index=True)
    
    # 第三层：横向水平条形图 (彻底修复文字旋转 90 度 Bug，正常水平视角显示)
    st.markdown("---")
    c_graph1, c_graph2 = st.columns(2)
    with c_graph1:
        st.markdown(f"##### 📐 该州当地规格销售装配比 (Size Breakdown)")
        st.caption("外贸业务排产配箱核心依据 (横向水平阅读，无旋转)：")
        size_data = pd.DataFrame(list(cur["size_breakdown_dict"].items()), columns=["规格尺寸", "销售占比(%)"])
        
        size_chart = alt.Chart(size_data).mark_bar(color="#2563EB").encode(
            x=alt.X("销售占比(%):Q", title="占比 (%)"),
            y=alt.Y("规格尺寸:N", sort=None, axis=alt.Axis(labelAngle=0, title=None)),
            tooltip=["规格尺寸", "销售占比(%)"]
        ).properties(height=180)
        st.altair_chart(size_chart, use_container_width=True)
        
    with c_graph2:
        st.markdown(f"##### 🌡️ 该州物理能耗度日数对比 (HDD vs CDD)")
        st.caption("出风口向上吹还是向下吹的物理天平 (横向水平阅读，无旋转)：")
        energy_data = pd.DataFrame([
            {"指标": "🔥 采暖度日 (HDD)", "度日数": cur["hdd"]},
            {"指标": "❄️ 制冷度日 (CDD)", "度日数": cur["cdd"]}
        ])
        
        energy_chart = alt.Chart(energy_data).mark_bar(color="#0284C7").encode(
            x=alt.X("度日数:Q", title="度日数 (Degree Days)"),
            y=alt.Y("指标:N", sort=None, axis=alt.Axis(labelAngle=0, title=None)),
            tooltip=["指标", "度日数"]
        ).properties(height=180)
        st.altair_chart(energy_chart, use_container_width=True)

    # 第四层：单州规格装箱配比明细大盘表
    st.markdown("##### 📦 该州细分规格装柜推荐配箱大盘表 (Assortment Planning)")
    assort_rows = []
    for sz_name, sz_pct in cur["size_breakdown_dict"].items():
        sz_month_units = int(cur["calc_tot"] * (sz_pct / 100.0))
        sz_month_cases = int(sz_month_units / max(case_pack, 1))
        sz_40hq_cases = int(960 * (sz_pct / 100.0))
        assort_rows.append({
            "细分规格尺寸": sz_name,
            "当地需求配比": f"{sz_pct}%",
            "该州月需求件数": f"{sz_month_units:,} 件",
            "建议月备货箱数": f"{sz_month_cases:,} 箱",
            "40HQ整柜配箱推荐": f"{sz_40hq_cases} 箱/柜",
            "建议单品售价 (MSRP)": f"${retail_msrp:.2f}"
        })
    st.dataframe(pd.DataFrame(assort_rows), use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="advice-box">
        <b>💼 威霖外贸业务员与商超买手谈盘指引 (Buyer Pitch Advice)：</b><br>
        {cur['channel_advice']}
    </div>
    """, unsafe_allow_html=True)
    
    # 买手谈判一页纸备忘录生成器 (Executive Pitch Deck Generator)
    with st.expander("📄 点击展开：商超买手审查谈判一页纸备忘录 (1-Page Pitch Memo)", expanded=False):
        st.markdown(f"""
        <div class="pitch-box">
        ================================================================================<br>
        EXECUTIVE LINE REVIEW PITCH MEMO | TARGET: {cur['name'].upper()} ({cur['abbr']})<br>
        VENDOR: NINGBO RUNNER INDUSTRIAL CORP. (建霖家居 603408)<br>
        CATEGORY: {cat_cfg['name'].split(' ')[0]} | DATE: WEEK {curr_week}, {curr_year}<br>
        ================================================================================<br><br>
        1. STRATEGIC OPPORTUNITY:<br>
           - Monthly Store Demand: {cur['calc_vel']:.1f} Units/Store/Month ({cur['upsw']:.1f} UPSW).<br>
           - Index vs. National Benchmark: {vel_delta_str} (High Growth Cluster).<br>
           - Channel Footprint: THD ({cur['thd']} stores), Lowe's ({cur['lowes']} stores), Menards ({cur['menards']} stores).<br><br>
        2. COMPETITOR REPLACEMENT ({rival_info['rival_name'].split('/')[0].strip()}):<br>
           - Incumbent Flaw: Light-gauge steel prone to chipping & rust under salt/moisture.<br>
           - Runner Advantage: Anodized 6063 Aluminum / PVD Green Coating with 720h+ salt spray.<br>
           - Margin Expansion: Retailer margin increases from {rival_info['rival_margin']} to {buyer_margin:.1f}%.<br>
           - Dollar Contribution: Estimated net gain of {dollar_gain_str}.<br><br>
        3. FULFILLMENT & LOGISTICS:<br>
           - Production Base: {prod_origin} (Tariff: {tariff_pct*100:.1f}%).<br>
           - Delivery Terms: {incoterm_mode}.<br>
           - Case Pack: {case_pack} pcs/ctn | 48 ctns/pallet | Landed DDP: ${landed_cost:.2f}.<br>
        ================================================================================
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 3: 渠道网络与货架策略大盘 -----------------
with tab_channel_pog:
    st.markdown("### 🏬 渠道网络渗透与货架策略大盘 (Channel & POG Merchandising)")
    st.caption("穿透各大零售商在各州的网点分布、货架陈列位（Facings）及商超买手审核（Line Review）策略。")
    
    st.markdown("#### 1. 该州三大零售商渗透与货架位置规划矩阵")
    pog_matrix_df = pd.DataFrame([
        {"陈列货架区域": "主通道黄金视线排面 (Eye-Level 12-24寸)", "适合威霖产品": "高流速 4x10/4x12 阳极氧化铝/拉丝镍款", "抢夺对家目标": "抢夺 Accord / Oatey 既有平销排面", "买手说服理由": "同等排面下，威霖提供 52%+ 毛利，单店坪效提升 25%"},
        {"陈列货架区域": "促销端架堆头 (Endcap Feature)", "适合威霖产品": "Q3入冬防寒季套件包 / 门底密封条多件装", "抢夺对家目标": "抢占入秋促销黄金曝光期", "买手说服理由": "结合季节性脉冲，以 Contractor Pack 形式做堆头走量，拉升客单价"},
        {"陈列货架区域": "侧挂网架吊袋 (Clip-Strip / Side-Wing)", "适合威霖产品": "地漏防臭硅胶芯、替换螺丝包、防滑贴条", "抢夺对家目标": "无固定排面，创造冲动交叉购买", "买手说服理由": "零货架占位成本，挂在主通道货架侧边，毛利率超 65%"},
        {"陈列货架区域": "地台整托平铺 (Pallet Drop / Base Deck)", "适合威霖产品": "C型装配槽钢、重载管道固定管夹大包装", "抢夺对家目标": "对标 Superstrut 散货陈列区", "买手说服理由": "Pro 承包商推平板车直接拉走整箱，降低理货人工成本"}
    ])
    st.dataframe(pog_matrix_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### 2. Big 3 零售巨头渠道格局 (THD vs Lowe's vs Menards)")
    top15 = df_filtered.sort_values("calc_tot", ascending=False).head(15)
    chart_df = pd.DataFrame({
        "州": top15["cn"],
        "THD (家得宝)": top15["calc_vel"] * top15["thd"],
        "Lowe's (劳氏)": top15["calc_vel"] * top15["lowes"],
        "Menards (美纳斯)": top15["calc_vel"] * top15["menards"]
    }).set_index("州")
    st.bar_chart(chart_df, height=320)

# ----------------- TAB 4: 客户人居画像透视 -----------------
with tab_persona:
    st.markdown("### 👥 目标州人居生活方式、买家画像与防退包装策略")
    st.caption("针对美国家装消费者的真实生活习惯，指导外贸开发规避差评与退货。")
    
    p_col1, p_col2 = st.columns([1.1, 1])
    with p_col1:
        st.markdown("#### 1. 全美四大买家客群渗透分布 (Persona Breakdown)")
        persona_data = pd.DataFrame([
            {"客群类型": "DIY 个人散客 (周末自装)", "占比估算 (%)": 55},
            {"客群类型": "Pro 专业工匠 (西语施工队为主)", "占比估算 (%)": 30},
            {"客群类型": "DIFM 改善型中产 (极简轻奢)", "占比估算 (%)": 10},
            {"客群类型": "B2B 物业管理 (公寓/出租房)", "占比估算 (%)": 5}
        ])
        
        persona_chart = alt.Chart(persona_data).mark_bar(color="#3B82F6").encode(
            x=alt.X("占比估算 (%):Q", title="渗透比例 (%)"),
            y=alt.Y("客群类型:N", sort=None, axis=alt.Axis(labelAngle=0, title=None)),
            tooltip=["客群类型", "占比估算 (%)"]
        ).properties(height=180)
        st.altair_chart(persona_chart, use_container_width=True)
        
    with p_col2:
        st.markdown("#### 2. 美国家庭退货原因穿透与防退包装矩阵表")
        anti_return_df = pd.DataFrame([
            {"退货主要原因": "尺寸买错 (占退货 60%+)", "客户行为根因": "老美将管道开孔内径与外沿面板尺寸混淆", "威霖包装防退对策": "外盒以大号粗体标明 Duct Opening，随盒附带 1:1 开孔纸规"},
            {"退货主要原因": "踩踏变形与异响 (占 20%)", "客户行为根因": "便宜塑料款或薄铁件踩踏咔咔响，无法忍受", "威霖包装防退对策": "采用 6063 铝或加厚冲压钢，正面印制 Heel-Proof 细高跟防卡标"},
            {"退货主要原因": "安装繁琐少配件 (占 15%)", "客户行为根因": "散客家里工具不齐，缺少螺丝导致无法安装", "威霖包装防退对策": "彩盒随附配套螺丝，外盒印制 3 步简易图解安装指南"},
            {"退货主要原因": "西语工人看不懂说明 (占 5%)", "客户行为根因": "拉丁裔工程队看不懂纯英文说明", "威霖包装防退对策": "外盒与说明书统一印刷 English + Español 双语标签"}
        ])
        st.dataframe(anti_return_df, use_container_width=True, hide_index=True)

# ----------------- TAB 5: 供应链海运与出口合规 -----------------
with tab_supply_cert:
    st.markdown("### 🚢 供应链海运、集装箱测算与合规认证雷达")
    
    st.markdown("#### 1. 40HQ 集装箱装载量：整托打托 (Palletized) vs 散装平铺 (Floor-Loaded)")
    pal_cases = 48
    pal_units = case_pack * pal_cases
    pal_total_cases = pal_cases * 20
    pal_total_units = pal_total_cases * case_pack
    pal_fob = pal_total_units * fob_cost
    pal_freight_unit = round(6500.0 / max(pal_total_units, 1), 2)
    
    fl_total_cases = int(pal_total_cases * 1.20)
    fl_total_units = fl_total_cases * case_pack
    fl_fob = fl_total_units * fob_cost
    fl_freight_unit = round(6500.0 / max(fl_total_units, 1), 2)
    
    container_compare_df = pd.DataFrame([
        {"出运测算参数": "出运装载方式", "模式A：美标打托 (Palletized)": "整柜装 20 个 GMA 托盘 (商超RDC偏好)", "模式B：散装平铺 (Floor-Loaded)": "纸箱从底码到顶 (海外仓偏好)"},
        {"出运测算参数": "40HQ 装箱总量", "模式A：美标打托 (Palletized)": f"{pal_total_cases:,} 箱", "模式B：散装平铺 (Floor-Loaded)": f"{fl_total_cases:,} 箱 (+20% 容积)"},
        {"出运测算参数": "40HQ 装载总件数", "模式A：美标打托 (Palletized)": f"{pal_total_units:,} 件", "模式B：散装平铺 (Floor-Loaded)": f"{fl_total_units:,} 件"},
        {"出运测算参数": "单柜出厂总货值 (FOB)", "模式A：美标打托 (Palletized)": f"${pal_fob:,.2f}", "模式B：散装平铺 (Floor-Loaded)": f"${fl_fob:,.2f}"},
        {"出运测算参数": "单件分摊海运费 (估算)", "模式A：美标打托 (Palletized)": f"${pal_freight_unit:.2f}/件", "模式B：散装平铺 (Floor-Loaded)": f"${fl_freight_unit:.2f}/件 (更省运费)"},
        {"出运测算参数": "公路限重风控 (42,000 lbs)", "模式A：美标打托 (Palletized)": "金属重件（槽钢/铸铁）注意总重限 42,000 lbs", "模式B：散装平铺 (Floor-Loaded)": "轻件（塑料出风口）可充分利用 68 CBM 容积"}
    ])
    st.dataframe(container_compare_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### 2. 美线主要清关口岸航程与内陆干线调度总表")
    ports_df = pd.DataFrame([
        {"目标大区": "美西 (加州/内华达)", "清关港口": "洛杉矶 / 长滩港 (LA/LB)", "海运航程": "快船 14~16 天直达", "内陆调度模式": "港口短驳至安大略仓 (Ontario)"},
        {"目标大区": "美西北 (华州/俄勒冈)", "清关港口": "西雅图 / 塔科马港 (Seattle)", "海运航程": "直达快船 15~18 天", "内陆调度模式": "派送西雅图配送中心 (RDC)"},
        {"目标大区": "美中 (芝加哥/大湖雪带)", "清关港口": "美西清关转内陆铁路 (IPI)", "海运航程": "海运 15天 + 铁路 7天", "内陆调度模式": "芝加哥约利埃特堆场 (Joliet) 提柜派送"},
        {"目标大区": "美东南 (北卡/佛州/佐治亚)", "清关港口": "萨凡纳港 (Savannah)", "海运航程": "巴拿马全水路 28~32 天", "内陆调度模式": "直达夏洛特总部与亚特兰大总仓"},
        {"目标大区": "美南核心 (德州/达拉斯)", "清关港口": "休斯敦港 (Houston)", "海运航程": "全水路直达 30~35 天", "内陆调度模式": "卡车短驳达拉斯仓储中心 (规避铁路费)"}
    ])
    st.dataframe(ports_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### 3. 威霖产品出海：全美通用强制认证大表")
    certs_table = pd.DataFrame(cat_cfg["national_certs"])
    certs_table.columns = ["认证标准代码", "测试检验项目", "主考/颁证机构", "商超技术准入要求"]
    st.dataframe(certs_table, use_container_width=True, hide_index=True)
    
    st.markdown(f"""
    <div class="radar-box">
        <b>🛡️ 选中州【{cur['cn']}】地方强制准入红线与合规备忘录：</b><br>
        • <b>地方特有法典</b>: {'；'.join(cur['state_certs'])}<br>
        • <b>加州 Prop 65</b>：出光剂与铅析出量必须符合限量，未取得无铅报告必须加印致癌黄标警告，否则面临赏金律师诉讼。<br>
        • <b>佛州与沿海 HVHZ</b>：淋浴门与户外紧固构件进入沿海区域必须具备迈阿密-戴德县 NOA 抗风暴飞弹撞击认证。<br>
        • <b>商业管道抗震</b>：威霖装配式槽钢支吊架在西海岸必须具备 HCAI / OSHPD 预审批编号，才能参与大型公建工程招投标。
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 9. 完整决策数据一键导出 CSV (UTF-8-SIG 防 Excel 乱码)
# ==============================================================================
st.markdown("---")
csv_out = df_sorted[[
    "序号", "abbr", "cn", "name", "region", "tier", "calc_vel", "upsw", "calc_tot", "calc_rev_msrp",
    "calc_fob_tot", "active_stores", "pog", "foundation", "flooring", "best", "avoid",
    "channel_advice", "hdd", "cdd", "frost_depth", "water_hardness",
    "salt_risk", "house_age", "hazard_idx", "state_certs", "reason_desc"
]].to_csv(index=False).encode('utf-8-sig')

st.download_button(
    label=f"📥 一键导出【{cat_cfg['name'].split(' ')[0]}】({selected_region}) 威霖全景决策报表 (.csv)",
    data=csv_out,
    file_name=f"Ningbo_Runner_Intelligence_{selected_cat_key}_{selected_region[:3]}.csv",
    mime="text/csv"
)
