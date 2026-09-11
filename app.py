import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# ==============================================================================
# 1. 页面配置与企业级高级 BI 科技蓝 CSS 注入
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
    
    /* 顶部标题栏 */
    .bi-header {
        background: white;
        padding: 18px 24px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .main-title { font-size: 1.6rem; font-weight: 700; color: #0F172A; margin-bottom: 4px; }
    .sub-title { font-size: 0.88rem; color: #475569; }
    
    /* KPI 指标卡 */
    .kpi-card {
        background: linear-gradient(135deg, #1E40AF, #2563EB);
        color: white;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }
    .kpi-title { font-size: 0.82rem; opacity: 0.92; margin-bottom: 2px; font-weight: 500; }
    .kpi-val { font-size: 1.5rem; font-weight: 700; }
    
    /* 自适应高度容器，彻底杜绝文字截断 */
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
    
    /* 徽章体系 */
    .badge-tier1 { background-color: #DCFCE7; color: #166534; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier2 { background-color: #DBEAFE; color: #1E40AF; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier3 { background-color: #FEF3C7; color: #92400E; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    .badge-tier4 { background-color: #FEE2E2; color: #991B1B; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.78rem; }
    
    .advice-box { border-left: 4px solid #3B82F6; background-color: #EFF6FF; padding: 12px 16px; border-radius: 0 6px 6px 0; margin-top: 10px; line-height: 1.6; }
    .radar-box { border-left: 4px solid #EF4444; background-color: #FEF2F2; padding: 12px 16px; border-radius: 0 6px 6px 0; margin-top: 10px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# 动态时间引擎，保证数据永不失效
current_dt = datetime.now()
curr_year = current_dt.year
curr_month = current_dt.month
curr_week = current_dt.isocalendar()[1]

# ==============================================================================
# 2. 侧边栏：完整找回并扩充【北美外贸与工程实战全景知识库】+ 财务核算
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/factory.png", width=46)
    st.markdown("### 💰 威霖到岸财务与毛利试算")
    st.caption(f"宁波威霖住宅设施有限公司 · {curr_year} 动态核价")
    
    fob_cost = st.number_input("1. 威霖出厂供货价 FOB ($/件)：", min_value=0.5, max_value=200.0, value=3.80, step=0.2)
    ocean_freight = st.number_input("2. 单件美线分摊海运费 ($/件)：", min_value=0.0, max_value=50.0, value=0.65, step=0.05)
    tariff_pct = st.number_input("3. 关税税率 Tariff (%)：", min_value=0.0, max_value=100.0, value=7.5, step=0.5) / 100.0
    retail_msrp = st.number_input("4. 北美商超零售价 MSRP ($/件)：", min_value=1.0, max_value=500.0, value=12.98, step=0.5)
    case_pack = st.number_input("5. 标准外箱装箱数 (Case Pack)：", min_value=1, max_value=100, value=10, step=1)
    
    landed_cost = fob_cost * (1 + tariff_pct) + ocean_freight
    buyer_margin = ((retail_msrp - landed_cost) / retail_msrp) * 100
    gross_profit_unit = retail_msrp - landed_cost
    
    st.markdown(f"""
    <div style='background:white;padding:10px 12px;border-radius:6px;border:1px solid #CBD5E1;margin-bottom:12px;'>
        <span style='font-size:0.8rem;color:#64748B;'>到岸完税成本 (Landed DDP)</span>: <b style='color:#0F172A;'>${landed_cost:.2f}</b><br>
        <span style='font-size:0.8rem;color:#64748B;'>商超单件毛利额</span>: <b style='color:#0F172A;'>${gross_profit_unit:.2f}</b><br>
        <span style='font-size:0.8rem;color:#64748B;'>零售净毛利率 (Buyer Margin)</span>: <b style='color:{'#166534' if buyer_margin>=42 else '#991B1B'};'>{buyer_margin:.1f}%</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📚 北美商超与工程实战全景词典")
    
    with st.expander("1. 房屋地基与对流原理 (Foundation)", expanded=False):
        st.write("""
        * **北方/中西部（全地下室 Basement）**：冻土线深，强制深挖地下室。暖气炉在地下，**热空气自然向上升**，地面出风口（Floor Register）是全屋标配。
        * **南方阳光带（水泥实心大平板 Slab）**：地下水高或地表膨胀土，直接浇筑实心水泥地，**地面绝对无管道**！冷气由阁楼向下吹，出风口 100% 在天花板。
        """)
        
    with st.expander("2. ASHRAE 暖通与 HDD/CDD 能耗度日", expanded=False):
        st.write("""
        * **HDD (采暖度日)**：基准 65°F。HDD > 5000 区域长年开暖气，出风口长年承受 55℃~65℃ 干燥热风烘烤，防热变形是硬指标。
        * **CDD (制冷度日)**：基准 65°F。CDD > 2000 区域长夏高湿开冷气，天花散流器防结露冷凝滴水是第一大客诉源。
        """)

    with st.expander("3. 冻土深度与融雪盐防腐红线", expanded=False):
        st.write("""
        * **冻土线 (Frost Depth)**：北方深达 36~60 英寸，室外防冻龙头必须选 **8~12 英寸超长杆**；南方 4 英寸短杆即可。
        * **融雪盐 (De-icing Salt)**：雪带冬季大量撒盐。鞋底盐水带入玄关，冷轧钢风口和压条 2 年即生锈烂穿，当地必须推**阳极氧化铝（6063）**或不锈钢。
        """)

    with st.expander("4. 北美三大零售商 (Big 3) 基因差异", expanded=False):
        st.write("""
        * **The Home Depot**：偏向 Pro 专业工匠承包商，客单大，看重工程大包装（Contractor Pack）与极限承重。
        * **Lowe's**：偏向家庭 DIY 散客与女性屋主，店面更明亮，注重彩色吊卡视觉颜值与软装搭配。
        * **Menards**：中西部农业大湖区地头蛇（330+大店），主打“全场 11% Rebate 返现”，工薪农场主死忠渠道。
        """)

    with st.expander("5. 商超买手合同潜规则 (Allowances)", expanded=False):
        st.write("""
        * **Defective Allowance (残损补贴)**：商超合同常规定期在发票中扣除 **2% ~ 4%** 作为无理由退货与破损补贴，报价 FOB 时必须计入成本。
        * **Buyback (库存回购)**：滞销清仓时零售商会强制要求供应商降价或买回滞销库存。
        * **Chargeback (物流罚款)**：外箱条码扫描率低于 99.5% 或送货迟到会面临单笔 $250~$500 罚款。
        """)

    with st.expander("6. GMA 托盘标准与 EDI 数据对接", expanded=False):
        st.write("""
        * **GMA 木托盘**：48 × 40 英寸，四向进叉，含托总高度 ≤ 52 英寸，总重 ≤ 2000 磅。
        * **EDI 电子数据交换**：入驻商超必须支持 ANSI X12 格式（EDI 850 采购订单、EDI 856 发货通知 ASN、EDI 810 发票）。
        """)

    with st.expander("7. 全美出口合规与环保红线清单", expanded=False):
        st.write("""
        * **加州 Prop 65**：无铅与塑化剂报告必须齐全，否则必须贴致癌黄标，防范赏金律师起诉。
        * **加州 Title 24 & WUI**：出风口低漏风率气密性测试与外墙 1/8 英寸防火防飞烬金属网。
        * **佛州 HVHZ**：迈阿密-戴德县 NOA 强飓风抗飞弹冲击测试。
        * **联邦 ADA**：地面高低差 ≤ 1/4 英寸并配缓坡，防范租客滑倒起诉。
        """)

# ==============================================================================
# 3. 核心品类与对家竞品版图（威霖五大产线对齐）
# ==============================================================================
CATEGORY_CONFIG = {
    "HVAC": {
        "name": "暖通风口与空气分配系统 (Registers & Grilles)",
        "willi_fit": "威霖主力核心板块：冲压冷轧钢、阳极氧化铝、压铸锌合金复古雕花、工程阻燃ABS出风口全系列。",
        "competitors": {
            "rival_name": "Accord Ventilation (全美第一巨头) / Deflecto",
            "shelf_share": "约 60% 黄金排面垄断",
            "rival_msrp": "$13.98",
            "rival_margin": "40.2%",
            "rival_gauge": "0.5mm ~ 0.6mm (24 Gauge 薄板冲压)",
            "willi_gauge": "0.8mm (20 Gauge 结构钢) / 6063-T5 阳极铝合金",
            "rival_salt": "中性盐雾 NSS 96 小时 (易起白锈/生斑)",
            "willi_salt": "中性盐雾 NSS 480 ~ 720 小时 (PVD/阳极氧化/电泳)",
            "rival_weakness": "传统冲压钢普通喷漆易刮花生锈，缺乏 AF 纳米防指纹等高端工艺，耐盐雾能力一般。",
            "willi_tactic": "以高质感阳极氧化铝与 PVD 哑光黑打高端改善型，给商超买手留出 52%+ 净毛利，换取双排面陈列。"
        },
        "positions": ["Floor (地面出风口)", "Ceiling (天花板散流器)", "Baseboard (踢脚线出风口)", "Sidewall (侧墙回风格栅)"],
        "materials": ["Steel (冲压冷轧钢)", "Aluminum (铝合金阳极氧化)", "Plastic (ABS阻燃树脂)", "Cast Metal (铸铝/铸铁重载)", "Engineered Wood (多层实木复合-抗翘曲)", "Zinc Die-Cast (压铸锌合金雕花)"],
        "finishes": ["Matte Black (US19 哑光黑)", "Brushed Nickel (US15 拉丝镍)", "Glossy White (经典工程白)", "Oil Rubbed Bronze (US10B 油磨青铜)", "PVD Brushed Gold (轻奢拉丝金)", "AF Nano-Coating (纳米防指纹黑)", "Wood Grain Transfer (3D热转印木纹)"],
        "sizes": ["04X10 (全美走量王 65%)", "04X12 (主流换新大号 20%)", "02X12 (踢脚狭长缝 10%)", "06X10 (大排风量 5%)", "12X12 (天花方型大尺寸)"],
        "national_certs": [
            {"code": "ASHRAE Standard 70", "item": "出风量 CFM 与噪音 NC 评级测试", "body": "AHRI / Intertek", "req": "主卧噪音 NC < 25"},
            {"code": "UL 94", "item": "塑料部件阻燃测试", "body": "Underwriters Laboratories", "req": "V-0 / HB 级阻燃安全"},
            {"code": "Heel-Proof", "item": "细高跟鞋防卡安全规范", "body": "ASTM", "req": "表面格栅镂空缝隙必须 < 9.5mm"}
        ]
    },
    "PLUMBING": {
        "name": "卫浴排水与长条隐形地漏 (Drains & Plumbing)",
        "willi_fit": "威霖主力核心板块：不锈钢冲压拉伸、长条隐形线性地漏、防臭下水器、防冻长水阀全系列。",
        "competitors": {
            "rival_name": "Oatey (全美水暖耗材霸主) / Sioux Chief",
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
            "rival_name": "Superstrut (Thomas & Betts / ABB) / Unistrut (Atkore)",
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
            "rival_name": "DreamLine (北美淋浴房霸主) / CRL (C.R. Laurence)",
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
            "rival_name": "NDS (全美雨水排水龙头) / ACO (聚合物混凝土标杆)",
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
        "national_certs": [
            {"code": "EN 1433 / ANSI", "item": "排水沟承压荷载试验", "body": "ANSI", "req": "A15 行人 ~ C250 载重汽车承重"},
            {"code": "ASTM A123", "item": "热浸镀锌层附着力试验", "body": "ASTM", "req": "锌层附着力与厚度检验"},
            {"code": "ASTM G154", "item": "户外抗紫外线脆化试验", "body": "ASTM", "req": "强光照射 2000h 无粉化"}
        ]
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
        "size_breakdown_dict": {"4x10 (地面主力)": 65, "4x12 (换新大号)": 20, "2x12 (踢脚狭长缝)": 10, "6x10 (回风大排量)": 5},
        "channel_advice": "Lowe's全球总部大本营，THD门店流转极快，重度配置端架(Endcap)促销位。",
        "hdd": 3400, "cdd": 1600, "frost_depth": 12, "water_hardness": 3.0, "salt_risk": "中", "hazard": "沿海飓风/湿热雷暴", "house_age": 33, "hazard_idx": 5, "base_vel": 42.0,
        "state_certs": ["NC State Building Code (沿海风暴紧固标准)", "ASHRAE 90.1 通风能耗审计"]
    },
    "TN": {
        "cn": "田纳西州", "name": "Tennessee", "region": "美南", "thd": 44, "lowes": 58, "menards": 0, "dc": "孟菲斯全美物流中心",
        "foundation": "木结构架空层/地下室", "climate": "Zone 4A 混合温和", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖重载地面出风口、管道吊架卡箍", "avoid": "天花专用下送风散流器",
        "size_breakdown_dict": {"4x10 (地面主力)": 65, "4x12 (换新大号)": 20, "2x12 (踢脚狭长缝)": 10, "6x10 (回风大排量)": 5},
        "channel_advice": "孟菲斯与纳什维尔物流核心区，全美出货中枢，适宜设总仓辐射美中南与美东。",
        "hdd": 3500, "cdd": 1650, "frost_depth": 12, "water_hardness": 6.5, "salt_risk": "中", "hazard": "冻融交替/暴风雨", "house_age": 37, "hazard_idx": 4, "base_vel": 40.5,
        "state_certs": ["MSS SP-58 管道支吊架标准", "cUPC 地漏排水认证"]
    },
    "KY": {
        "cn": "肯塔基州", "name": "Kentucky", "region": "美南", "thd": 27, "lowes": 38, "menards": 9, "dc": "路易斯维尔",
        "foundation": "全地下室占80%+", "climate": "Zone 4A 四季鲜明多雪", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖地下管道风口、铸铝复古格栅", "avoid": "无调节阀轻薄空框",
        "size_breakdown_dict": {"4x10 (地面主力)": 65, "4x12 (换新大号)": 20, "2x12 (踢脚狭长缝)": 10, "6x10 (回风大排量)": 5},
        "channel_advice": "老房翻修与自建房比例高，Pro工匠批量成箱采购占比较大。",
        "hdd": 4400, "cdd": 1250, "frost_depth": 20, "water_hardness": 10.5, "salt_risk": "高", "hazard": "冬季道路融雪盐结冰", "house_age": 43, "hazard_idx": 4, "base_vel": 38.0,
        "state_certs": ["UL 94 阻燃测试", "IPC 县级水暖抗冻裂标准"]
    },
    "SC": {
        "cn": "南卡罗来纳州", "name": "South Carolina", "region": "美东南", "thd": 37, "lowes": 48, "menards": 0, "dc": "哥伦比亚/萨凡纳",
        "foundation": "架空层/沿海桩基", "climate": "Zone 3A 亚热带湿热", "flooring": "实木 40%, LVP 35%, 瓷砖 15%, 地毯 10%",
        "best": "威霖工程ABS风口、耐盐雾不锈钢地漏", "avoid": "未做防腐普通冷轧铁件",
        "size_breakdown_dict": {"4x10 (地面主力)": 65, "4x12 (换新大号)": 20, "2x12 (踢脚狭长缝)": 10, "6x10 (回风大排量)": 5},
        "channel_advice": "沿海重度防腐耐盐雾，内陆侧重地板防潮收口五金。",
        "hdd": 2400, "cdd": 2000, "frost_depth": 5, "water_hardness": 3.0, "salt_risk": "低", "hazard": "沿海强飓风/高湿热腐蚀", "house_age": 31, "hazard_idx": 6, "base_vel": 36.0,
        "state_certs": ["ASTM B117 盐雾 500h 测试", "ASTM A153 热浸镀锌层检验"]
    },
    "OH": {
        "cn": "俄亥俄州", "name": "Ohio", "region": "美中", "thd": 71, "lowes": 73, "menards": 34, "dc": "哥伦布核心仓",
        "foundation": "100%全地下室为主", "climate": "Zone 5A 寒冷多雪长冬", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖冲压金属/铝合金地面风口、槽钢支吊架", "avoid": "薄脆塑料、天花专用下送风散流器",
        "size_breakdown_dict": {"4x10 (地面主力)": 65, "4x12 (换新大号)": 20, "2x12 (踢脚狭长缝)": 10, "6x10 (回风大排量)": 5},
        "channel_advice": "五金和建材传统大州，老旧翻新是第一驱动力，Menards 与 THD 竞争激烈。",
        "hdd": 5600, "cdd": 850, "frost_depth": 36, "water_hardness": 15.0, "salt_risk": "极高", "hazard": "暴雪融雪盐侵蚀+极硬水", "house_age": 54, "hazard_idx": 7, "base_vel": 32.0,
        "state_certs": ["UL 203 消防管道吊架认证", "ASHRAE 70 风量与静音评级"]
    },
    "IN": {
        "cn": "印第安纳州", "name": "Indiana", "region": "美中", "thd": 41, "lowes": 42, "menards": 39, "dc": "印第安纳波利斯",
        "foundation": "全地下室占85%+", "climate": "Zone 5A 严寒多雪", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖地面暖风风口、C型槽钢支架", "avoid": "天花专用风口",
        "size_breakdown_dict": {"4x10 (地面主力)": 65, "4x12 (换新大号)": 20, "2x12 (踢脚狭长缝)": 10, "6x10 (回风大排量)": 5},
        "channel_advice": "工业底子扎实，家庭 DIY 普及率高，Menards 渗透极深。",
        "hdd": 5500, "cdd": 1000, "frost_depth": 36, "water_hardness": 17.0, "salt_risk": "极高", "hazard": "重度硬水结垢/大雪盐蚀", "house_age": 48, "hazard_idx": 6, "base_vel": 31.5,
        "state_certs": ["MSS SP-58 承重强度验证", "NSF 372 无铅涉水认证"]
    },
    "IL": {
        "cn": "伊利诺伊州", "name": "Illinois", "region": "美中", "thd": 81, "lowes": 43, "menards": 61, "dc": "大芝加哥枢纽",
        "foundation": "全地下室占绝大多数", "climate": "Zone 5A 大陆性严寒大风", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖重型地面风口、装配式槽钢支架", "avoid": "轻薄无卡扣风口",
        "size_breakdown_dict": {"4x10 (地面主力)": 65, "4x12 (换新大号)": 20, "2x12 (踢脚狭长缝)": 10, "6x10 (回风大排量)": 5},
        "channel_advice": "大芝加哥商超网络极其密集，单店流转稳定，总盘吞吐量位列全美第一梯队。",
        "hdd": 6100, "cdd": 900, "frost_depth": 42, "water_hardness": 14.5, "salt_risk": "极高", "hazard": "芝加哥狂风暴雪融雪盐", "house_age": 56, "hazard_idx": 7, "base_vel": 30.0,
        "state_certs": ["City of Chicago Building Code (芝加哥建筑法规)", "UL 203 吊架"]
    },
    "MI": {
        "cn": "密歇根州", "name": "Michigan", "region": "美中", "thd": 70, "lowes": 43, "menards": 44, "dc": "底特律仓",
        "foundation": "100%全地下室", "climate": "Zone 5A/6A 大湖雪带漫长冬", "flooring": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%",
        "best": "威霖经典地面金属风口、耐融雪盐涂层构件", "avoid": "天花风口、薄铁喷漆",
        "size_breakdown_dict": {"4x10 (地面主力)": 65, "4x12 (换新大号)": 20, "2x12 (踢脚狭长缝)": 10, "6x10 (回风大排量)": 5},
        "channel_advice": "底特律周边老房基数庞大，换新频次极高，融雪盐耐受是选品第一红线。",
        "hdd": 6800, "cdd": 650, "frost_depth": 48, "water_hardness": 12.0, "salt_risk": "极高", "hazard": "大湖雪带超长严冬", "house_age": 52, "hazard_idx": 7, "base_vel": 29.5,
        "state_certs": ["ASTM B117 盐雾测试 480h+", "ASHRAE 70 通风评级"]
    },
    "FL": {
        "cn": "佛罗里达州", "name": "Florida", "region": "美东南", "thd": 155, "lowes": 110, "menards": 0, "dc": "奥兰多/迈阿密",
        "foundation": "95%+混凝土实心大平板(Slab)", "climate": "Zone 1A/2A 极湿热高盐雾飓风", "flooring": "瓷砖 60%, 强化/LVP 25%, 地毯 15%",
        "best": "威霖天花散流器、不锈钢长条地漏、抗飓风角码", "avoid": "地面出风口 (实心水泥地无孔，绝对禁发货!)",
        "size_breakdown_dict": {"6x6/8x8散流器": 40, "12x12天花格栅": 25, "14x6侧墙回风": 20, "20x20回风门": 15},
        "channel_advice": "纯制冷市场，严禁发地面风口；主推 HVHZ 抗飓风门窗五金与防腐地漏。",
        "hdd": 500, "cdd": 3800, "frost_depth": 0, "water_hardness": 14.0, "salt_risk": "极低", "hazard": "HVHZ五级强飓风/极高盐雾", "house_age": 34, "hazard_idx": 9, "base_vel": 21.0,
        "state_certs": ["Miami-Dade NOA (迈阿密-戴德县抗飓风最高认证)", "FBC HVHZ 标准", "cUPC 淋浴地漏"]
    },
    "CA": {
        "cn": "加利福尼亚州", "name": "California", "region": "美西", "thd": 234, "lowes": 112, "menards": 0, "dc": "洛杉矶/安大略总仓",
        "foundation": "南加全平板/抗震高要求", "climate": "Zone 3B/4B 干燥温和干热", "flooring": "瓷砖 45%, LVP 35%, 地毯 20%",
        "best": "威霖 Title 24环保风口、抗震支架组件、WUI防飞烬百叶", "avoid": "高铅铸造件、普通易燃塑料",
        "size_breakdown_dict": {"6x6/8x8散流器": 35, "10x10天花口": 25, "14x6回风口": 25, "线形隐藏风口": 15},
        "channel_advice": "全美最大单一经济体，但加州 65 号提案（Prop 65 铅标）是法律诉讼雷区，必须贴标。",
        "hdd": 2100, "cdd": 1300, "frost_depth": 0, "water_hardness": 9.5, "salt_risk": "极低", "hazard": "WUI山火/高烈度地震/Prop 65铅标", "house_age": 48, "hazard_idx": 7, "base_vel": 20.0,
        "state_certs": ["加州 Prop 65 无铅警告贴标 (一票否决红线)", "加州 Title 24 气密性法案", "加州 HCAI/OSHPD 管道抗震支吊架预审批", "加州 WUI 防火防飞烬认证"]
    },
    "TX": {
        "cn": "德克萨斯州", "name": "Texas", "region": "美南核心", "thd": 182, "lowes": 145, "menards": 0, "dc": "达拉斯/休斯敦大仓",
        "foundation": "85%+混凝土实心大平板(Slab)", "climate": "Zone 2A/3A/3B 漫长干热湿热", "flooring": "瓷砖 50%, 抛光强化 30%, 地毯 20%",
        "best": "威霖天花散流器、回风百叶格栅、重型管道吊卡", "avoid": "地面下沉式出风口 (实心地基无孔可用!)",
        "size_breakdown_dict": {"6x6/8x8散流器": 40, "12x12天花格栅": 30, "14x6回风口": 15, "20x20回风门": 15},
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
            "dc": "大区核心集散仓", "foundation": v[6], "climate": "Zone 4A/5A 大陆季风", "flooring": "实木 40%, LVP 35%, 瓷砖 15%, 地毯 10%",
            "best": "威霖标准化出风口、装配式槽钢支架", "avoid": "非标冷门异形件",
            "size_breakdown_dict": {"4x10 (通用主力)": 70, "4x12 (换新大号)": 15, "2x12 (狭长缝)": 10, "6x12 (大排风)": 5},
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
st.markdown(f"""
<div class="bi-header">
    <div class="main-title">🏢 宁波威霖住宅设施 · 北美大零售商业与工程决策系统 (Master Edition)</div>
    <div class="sub-title">实时日历基准：<b>{curr_year} 年第 {curr_week} 自然周</b> | 50 州工程物理环境测算 | 单州全景调研与对家横向对标 | 州级出口认证图谱</div>
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

# 属性控制排
st.markdown("#### 🎯 威霖制造工法与目标客群属性联动")
f1, f2, f3, f4, f5 = st.columns(5)
with f1:
    pos_opts = ["(全部位置 / All)"] + cat_cfg["positions"]
    sel_pos = st.selectbox("位置形态：", pos_opts, index=1, key=f"willi_{selected_cat_key}_pos").split(" ")[0]
with f2:
    mat_opts = ["(全部材质 / All)"] + cat_cfg["materials"]
    sel_mat = st.selectbox("原材料构件：", mat_opts, index=0, key=f"willi_{selected_cat_key}_mat").split(" ")[0]
with f3:
    fin_opts = ["(全部工艺 / All)"] + cat_cfg["finishes"]
    sel_fin = st.selectbox("表面工艺/防腐：", fin_opts, index=0, key=f"willi_{selected_cat_key}_fin").split(" ")[0]
with f4:
    size_opts = ["(全部尺寸 / All)"] + cat_cfg["sizes"]
    sel_size = st.selectbox("规格尺寸：", size_opts, index=1, key=f"willi_{selected_cat_key}_size").split(" ")[0]
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
    
    # 1. 地基与结构逻辑
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

    # 2. 融雪盐与水质硬度
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

    # 3. 房龄与动态自然周脉冲
    if s["house_age"] >= 50:
        weight *= 1.2
        reasons.append(f"中位房龄达 {s['house_age']} 年，老旧建筑二次翻新动销活跃")

    if "实时自适应" in selected_season:
        if curr_month in [9, 10, 11] and selected_cat_key in ["SHOWER_HARDWARE", "HVAC"]:
            weight *= 1.45
            reasons.append(f"🍂 当前正值第 {curr_week} 周秋季防寒高峰，销量脉冲爆发")
        elif curr_month in [6, 7, 8] and selected_cat_key == "HVAC" and sel_pos == "Ceiling":
            weight *= 1.7
            reasons.append(f"☀️ 当前正值第 {curr_week} 周夏季酷暑制冷峰值，天花散流器畅销")
        elif curr_month in [12, 1, 2] and selected_cat_key == "PLUMBING" and "Frost" in sel_pos:
            weight *= 2.3
            reasons.append(f"❄️ 当前正值第 {curr_week} 周冬季深度冰封，爆管抢修达峰")
    elif "Q3" in selected_season and selected_cat_key in ["SHOWER_HARDWARE", "HVAC"]:
        weight *= 1.4
        reasons.append("🍂 处于入冬防寒整备季（Fall Weatherization），销量脉冲激增")
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

# 全美大盘基准
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
        <div class="kpi-title">全美大盘单店均值基准线</div>
        <div class="kpi-val">{national_avg_vel} 件/月 ({national_avg_upsw} 件/周)</div>
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
            "选择全美排行榜主排序维度：",
            ["全州渠道月总吞吐量 (件/月) - 适于工厂排产总盘计划", "单店平均月销售流速 (件/店/月) - 适于商超平效谈判与货架位申请"],
            horizontal=True
        )
    
    st.markdown("##### 🎚️ 互动数据过滤滑块 (Sliders)")
    slide_c1, slide_c2 = st.columns(2)
    with slide_c1:
        vel_min = st.slider("过滤单店最低月流速门槛 (件/店/月)：", min_value=0, max_value=80, value=0, step=5)
    with slide_c2:
        age_min = st.slider("过滤各州中位最低房龄门槛 (年)：", min_value=20, max_value=60, value=20, step=5)
        
    df_filtered = df_res[(df_res["calc_vel"] >= vel_min) & (df_res["house_age"] >= age_min)].copy()
    
    if "单店" in view_mode:
        df_display = df_filtered.sort_values("rank_vel", ascending=True).reset_index(drop=True)
    else:
        df_display = df_filtered.sort_values("rank_tot", ascending=True).reset_index(drop=True)
    df_display["序号"] = df_display.index + 1
    
    max_vel_val = max(int(df_all["calc_vel"].max()), 1)
    
    # 增加基准线相对比例列
    df_display["大盘相对指数"] = df_display["calc_vel"].apply(lambda x: f"{round(((x - national_avg_vel) / national_avg_vel)*100, 1):+0.1f}%")
    
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
            "calc_vel": st.column_config.ProgressColumn("单店月流速", min_value=0, max_value=max_vel_val, format="%.1f 件"),
            "upsw": st.column_config.NumberColumn("单店周流速(UPSW)", format="%.1f 件/周"),
            "大盘相对指数": st.column_config.TextColumn("大盘基准比", width=90),
            "calc_tot": st.column_config.NumberColumn("月总盘(件)", format="%d"),
            "calc_rev_msrp": st.column_config.NumberColumn("月零售流水($)", format="$%d"),
            "active_stores": st.column_config.NumberColumn("有效门店", width=70),
            "house_age": st.column_config.NumberColumn("房龄", format="%d年", width=65),
            "pog": st.column_config.TextColumn("POG货架排面建议", width=140),
            "foundation": st.column_config.TextColumn("典型地基基底", width=160),
            "climate": st.column_config.TextColumn("气候带", width=120),
            "frost_depth": st.column_config.NumberColumn("冻土(寸)", format="%d寸", width=70),
            "salt_risk": st.column_config.TextColumn("融雪盐", width=70)
        },
        height=480,
        hide_index=True
    )
    
    st.markdown("#### 📊 全美 50 州战略梯队（Tier 1 ~ 4）分布图")
    tier_counts = df_all["tier"].value_counts().reset_index()
    tier_counts.columns = ["战略梯队", "州数量"]
    
    # 强制水平条形图，文字绝不旋转
    tier_chart = alt.Chart(tier_counts).mark_bar(color="#2563EB").encode(
        x=alt.X("州数量:Q", title="覆盖州数量"),
        y=alt.Y("战略梯队:N", sort=None, axis=alt.Axis(labelAngle=0, title=None)),
        tooltip=["战略梯队", "州数量"]
    ).properties(height=160)
    st.altair_chart(tier_chart, use_container_width=True)

# ----------------- TAB 2: 单州深度调研与对家横向对标大盘 -----------------
with tab_deepdive:
    st.markdown("### 🎯 威霖单州全景深度调研与竞品横向对标大盘")
    st.caption("穿透分析单一州的自然建筑基底，对比全美大盘均值，并与北美在售头部竞品展开参数级对标。")
    
    target_abbr = st.selectbox("👉 选择要穿透调研的目标州：", df_sorted["abbr"].tolist(), index=0)
    cur = df_sorted[df_sorted["abbr"] == target_abbr].iloc[0]
    rival_info = cat_cfg["competitors"]
    
    vel_vs_nat = round(((cur['calc_vel'] - national_avg_vel) / national_avg_vel) * 100, 1)
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
        
    # 第二层：核心对家参数对比大表 (彻底解决截断，指标化细致对标)
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
        sz_month_cases = int(sz_month_units / case_pack)
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

# ----------------- TAB 3: 渠道网络与货架策略大盘 -----------------
with tab_channel_pog:
    st.markdown("### 🏬 渠道网络渗透与货架策略大盘 (Channel & POG Merchandising)")
    st.caption("穿透各大零售商在各州的网点分布、货架陈列位（Facings）及商超买手审核（Line Review）策略。")
    
    st.markdown("#### 1. 该州三大零售商渗透与货架位置规划矩阵")
    pog_matrix_df = pd.DataFrame([
        {"陈列货架区域": "主通道黄金视线排面 (Eye-Level 12-24寸)", "适合威霖产品": "高流速 4x10/4x12 阳极氧化铝/拉丝镍款", "抢夺对家目标": "抢夺 Accord / Oatey 既有平销排面", "买手说服理由": "同等排面下，威霖提供 52%+ 毛利，单店坪效提升 25%"},
        {"陈列货架区域": "促销端架堆头 (Endcap Feature)", "适合威霖产品": "Q3入冬防寒季套件包 / 门底密封条多件装", "抢夺对家目标": "抢占入秋促销黄金曝光期", "买手说服理由": "结合季节性脉冲，以 Contractor Pack 形式做堆头走量，拉升单次客单价"},
        {"陈列货架区域": "侧挂网架吊袋 (Clip-Strip / Side-Wing)", "适合威霖产品": "地漏防臭硅胶芯、替换螺丝包、防滑贴条", "抢夺对家目标": "无固定排面，创造冲动交叉购买", "买手说服理由": "零货架占位成本，挂在主通道货架侧边，毛利率超 65%"},
        {"陈列货架区域": "地台整托平铺 (Pallet Drop / Base Deck)", "适合威霖产品": "C型装配槽钢、重载管道固定管夹大包装", "抢夺对家目标": "对标 Superstrut 散货陈列区", "买手说服理由": "Pro 承包商推平板车直接拉走整箱，降低理货人工成本"}
    ])
    st.dataframe(pog_matrix_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### 2. Big 3 零售巨头渠道格局 (THD vs Lowe's vs Menards)")
    top15 = df_res.sort_values("calc_tot", ascending=False).head(15)
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
    pal_freight_unit = round(6500.0 / pal_total_units, 2)
    
    fl_total_cases = int(pal_total_cases * 1.20)
    fl_total_units = fl_total_cases * case_pack
    fl_fob = fl_total_units * fob_cost
    fl_freight_unit = round(6500.0 / fl_total_units, 2)
    
    container_compare_df = pd.DataFrame([
        {"出运测算参数": "出运装载方式", "模式A：美标打托 (Palletized)": "整柜装 20 个 GMA 托盘 (商超RDC偏好)", "模式B：散装平铺 (Floor-Loaded)": "纸箱从底码到顶 (海外仓偏好)"},
        {"出运测算参数": "40HQ 装箱总量", "模式A：美标打托 (Palletized)": f"{pal_total_cases:,} 箱", "模式B：散装平铺 (Floor-Loaded)": f"{fl_total_cases:,} 箱 (+20% 容积)"},
        {"出运测算参数": "40HQ 装载总件数", "模式A：美标打托 (Palletized)": f"{pal_total_units:,} 件", "模式B：散装平铺 (Floor-Loaded)": f"{fl_total_units:,} 件"},
        {"出运测算参数": "单柜出厂总货值 (FOB)", "模式A：美标打托 (Palletized)": f"${pal_fob:,.2f}", "模式B：散装平铺 (Floor-Loaded)": f"${fl_fob:,.2f}"},
        {"出运测算参数": "单件分摊海运费 (估算)", "模式A：美标打托 (Palletized)": f"${pal_freight_unit:.2f}/件", "模式B：散装平铺 (Floor-Loaded)": f"${fl_freight_unit:.2f}/件 (更省运费)"},
        {"出运测算参数": "美方码头卸柜时效", "模式A：美标打托 (Palletized)": "叉车 30 分钟速卸 (无额外人工费)", "模式B：散装平铺 (Floor-Loaded)": "人工搬运 3~4 小时 (产生卸柜费)"}
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
# 9. 完整决策数据一键导出 CSV
# ==============================================================================
st.markdown("---")
csv_out = df_sorted[[
    "序号", "abbr", "cn", "name", "region", "tier", "calc_vel", "upsw", "calc_tot", "calc_rev_msrp",
    "calc_fob_tot", "active_stores", "pog", "foundation", "flooring", "best", "avoid",
    "channel_advice", "hdd", "cdd", "frost_depth", "water_hardness",
    "salt_risk", "house_age", "hazard", "state_certs", "reason_desc"
]].to_csv(index=False).encode('utf-8-sig')

st.download_button(
    label=f"📥 一键导出【{cat_cfg['name'].split(' ')[0]}】({selected_region}) 威霖全景决策报表 (.csv)",
    data=csv_out,
    file_name=f"Ningbo_Runner_Intelligence_{selected_cat_key}_{selected_region[:3]}.csv",
    mime="text/csv"
)
