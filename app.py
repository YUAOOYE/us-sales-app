import streamlit as st
import pandas as pd
import json
import os
import time

# ==============================================================================
# 1. 页面配置与美观样式
# ==============================================================================
st.set_page_config(
    page_title="全美地理气候与多品类销售决策系统",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 2.1rem; font-weight: 700; color: #0F172A; margin-bottom: 0.2rem; }
    .sub-header { font-size: 0.95rem; color: #475569; margin-bottom: 1.2rem; }
    .card-t1 { border-left: 5px solid #2563EB; background-color: #F8FAFC; padding: 16px; border-radius: 6px; margin-bottom: 12px; }
    .card-t5 { border-left: 5px solid #EF4444; background-color: #FEF2F2; padding: 16px; border-radius: 6px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🗺️ 全美地理气候与多品类销售决策系统</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">输入美国州缩写/名称或产品品类 | 智能反查全美 48 州单店销能、气候特征、地基形态与货架铺货建议</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. 全美 48 州内置权威数据库（基于真实地图单店数据与建筑气候统计）
# ==============================================================================
STATES_DATA = [
  {
    "abbr": "NC", "en": "North Carolina", "cn": "北卡罗来纳州", "sales": 2946, "tier": "T1 黄金走廊 (>2000)",
    "region": "东南大西洋区 (Southeast)", "climate": "Zone 4A/3A 混合湿润区，夏极闷热高湿，冬有冻雨积雪",
    "foundation": "架空层(Crawl Space)与局部地下室占主导(75%+)",
    "best_products": "地面出风口/出风口罩、实木与LVP地板衔接五金、耐温差防腐配件",
    "avoid_products": "未做防腐处理的普通冲压薄钢件（高湿易生锈）",
    "channel_advice": "Lowe's大本营核心州，THD门店流转极快，重度配置端架(Endcap)推广"
  },
  {
    "abbr": "TN", "en": "Tennessee", "cn": "田纳西州", "sales": 2902, "tier": "T1 黄金走廊 (>2000)",
    "region": "中东南内陆 (Southeast)", "climate": "Zone 4A 混合温和湿润，冷热双峰负荷明显",
    "foundation": "木结构架空层与地下室普及，平板地基极少",
    "best_products": "重载地面风口、高承重踏压构件、暖通换新件",
    "avoid_products": "天花板专用下送风扩散器（老宅基本无天花管道）",
    "channel_advice": "孟菲斯/纳什维尔物流核心区，适合设立主发货仓辐射全美"
  },
  {
    "abbr": "KY", "en": "Kentucky", "cn": "肯塔基州", "sales": 2579, "tier": "T1 黄金走廊 (>2000)",
    "region": "中东部内陆 (Midwest/South)", "climate": "Zone 4A 四季分明，冬季降雪多，夏季暴雨潮湿",
    "foundation": "全地下室比例超80%，主风管全在地下",
    "best_products": "地下室集中送风地面风口、哑光黑/铸铝复古装饰风口",
    "avoid_products": "无调风挡板的装饰空框",
    "channel_advice": "老宅翻修市场大，Pro承包商批量采购占比高"
  },
  {
    "abbr": "SC", "en": "South Carolina", "cn": "南卡罗来纳州", "sales": 2433, "tier": "T1 黄金走廊 (>2000)",
    "region": "东南大西洋沿海 (Southeast)", "climate": "Zone 3A 亚热带湿热，漫长酷暑高湿，冬温和短促",
    "foundation": "防潮架空层与沿海桩基为主",
    "best_products": "耐高盐雾工程ABS出风口、防锈铝合金五金、除湿配套件",
    "avoid_products": "易生锈冷轧铁板件",
    "channel_advice": "沿海与内陆差异大，沿海侧重防腐耐盐雾，内陆侧重地板配件"
  },
  {
    "abbr": "WV", "en": "West Virginia", "cn": "西弗吉尼亚州", "sales": 2248, "tier": "T1 黄金走廊 (>2000)",
    "region": "阿巴拉契亚山区 (Mid-Atlantic)", "climate": "Zone 5A 湿润山地高寒气候，冬季降雪深，温差巨大",
    "foundation": "依山而建，全地下室与深层桩基普及",
    "best_products": "高承重抗踩踏地面风口、防滑五金、耐严寒热胀冷缩件",
    "avoid_products": "易脆裂普通塑料件",
    "channel_advice": "传统耐用型五金需求大，价格敏感度高于沿海，主打坚固耐用"
  },
  {
    "abbr": "ID", "en": "Idaho", "cn": "爱达荷州", "sales": 2213, "tier": "T1 黄金走廊 (>2000)",
    "region": "西北高山内陆 (Mountain)", "climate": "Zone 5B/6B 大陆性干燥极寒，冬季漫长冰冻，空气干燥",
    "foundation": "全地下室防冻深层地基普及率超85%",
    "best_products": "大风量地面强排风口、防风密封胶条、耐低温防脆裂配件",
    "avoid_products": "高湿热专用除霉件",
    "channel_advice": "新兴人口流入州，新房建设与自建房比例高，成套采购多"
  },
  {
    "abbr": "VA", "en": "Virginia", "cn": "弗吉尼亚州", "sales": 2169, "tier": "T1 黄金走廊 (>2000)",
    "region": "中大西洋区 (Mid-Atlantic)", "climate": "Zone 4A 四季鲜明，冬冷夏热，年降雨量充沛",
    "foundation": "地下室与木结构架空层共存，老房多",
    "best_products": "中高端装饰性风口（拉丝镍、古铜黑）、精致硬装五金",
    "avoid_products": "外观粗糙廉价工程件",
    "channel_advice": "居民消费水准高，愿意为颜值与静音/防卡鞋跟设计支付溢价"
  },
  {
    "abbr": "KS", "en": "Kansas", "cn": "堪萨斯州", "sales": 2124, "tier": "T1 黄金走廊 (>2000)",
    "region": "中部大平原 (Midwest)", "climate": "Zone 4A/5A 极端大陆性气候，冬极寒多雪，夏酷热强风",
    "foundation": "几乎100%全地下室（兼做龙卷风与防寒避难所）",
    "best_products": "地下风管标配地面出风口、大风量耐压风门、结实金属件",
    "avoid_products": "轻飘易移位无固定槽的轻质件",
    "channel_advice": "农牧独栋大宅多，强调易清洗与大流通面积(Free Area)"
  },
  {
    "abbr": "DE", "en": "Delaware", "cn": "特拉华州", "sales": 2122, "tier": "T1 黄金走廊 (>2000)",
    "region": "中大西洋 (Mid-Atlantic)", "climate": "Zone 4A 温和湿润海洋过渡气候，冬冷夏潮",
    "foundation": "地下室与浅架空层混合",
    "best_products": "通用标称4x10/2x12/4x12尺寸风口、免税走量型热销款",
    "avoid_products": "非标异形定制件",
    "channel_advice": "免税州吸引跨州批发采购，单店流转效率极高"
  },
  {
    "abbr": "AL", "en": "Alabama", "cn": "阿拉巴马州", "sales": 2095, "tier": "T1 黄金走廊 (>2000)",
    "region": "东南深南内陆 (South)", "climate": "Zone 3A 亚热带湿热，夏季闷热潮湿持续5个月以上",
    "foundation": "北部山区架空层居多，南部平原混合",
    "best_products": "耐潮防霉ABS树脂风口、高性价比金属件、通用通风罩",
    "avoid_products": "易氧化表面未经保护的铜铁件",
    "channel_advice": "性价比敏感，对平价耐用型产品进店即买率高"
  },
  {
    "abbr": "IN", "en": "Indiana", "cn": "印第安纳州", "sales": 2020, "tier": "T1 黄金走廊 (>2000)",
    "region": "五大湖南部 (Midwest)", "climate": "Zone 5A 典型寒冷区，冬季连续结冰降雪，夏季湿热",
    "foundation": "全地下室普及率超85%，中央强排暖风为主",
    "best_products": "地面出风口、踩踏耐重五金、防结冰凝露构件",
    "avoid_products": "天花板专用风口（住宅地面占比超90%）",
    "channel_advice": "工业制造业底子好，家庭DIY普及，Menards与THD竞争激烈"
  },
  {
    "abbr": "MO", "en": "Missouri", "cn": "密苏里州", "sales": 1958, "tier": "T2 稳定支撑带 (1500-2000)",
    "region": "中西部大河汇合区 (Midwest)", "climate": "Zone 4A/5A 大陆性季风气候，冬冷夏酷暑",
    "foundation": "地下室为主，传统木框架独立住宅集聚",
    "best_products": "地面调风风口、管道连接件、多功能调风风门",
    "avoid_products": "纯热带建材", "channel_advice": "圣路易斯与堪萨斯城两大都市圈带动主力店动销"
  },
  {
    "abbr": "MD", "en": "Maryland", "cn": "马里兰州", "sales": 1935, "tier": "T2 稳定支撑带 (1500-2000)",
    "region": "中大西洋首都圈 (Mid-Atlantic)", "climate": "Zone 4A 湿润四季分明，冬寒冷偶有大暴雪",
    "foundation": "老房地下室多，联排镇屋(Townhouse)密集",
    "best_products": "中高档静音地面出风口、防卡鞋跟安全风口、装饰盖板",
    "avoid_products": "工业风粗狂件", "channel_advice": "老房升级改善多，重视审美匹配木地板色调"
  },
  {
    "abbr": "OH", "en": "Ohio", "cn": "俄亥俄州", "sales": 1768, "tier": "T2 稳定支撑带 (1500-2000)",
    "region": "五大湖东部 (Midwest)", "climate": "Zone 5A 寒冷多雪湿润，冬季供暖周期长达6个月",
    "foundation": "典型全地下室住宅结构，存量房房龄较长",
    "best_products": "金属冲压/铸铝地面风口、重载五金、暖通管道防锈配件",
    "avoid_products": "薄脆弱承重件", "channel_advice": "五金和建材传统大州，老旧翻新为第一大驱动力"
  },
  {
    "abbr": "UT", "en": "Utah", "cn": "犹他州", "sales": 1666, "tier": "T2 稳定支撑带 (1500-2000)",
    "region": "高原干旱盆地区 (Mountain)", "climate": "Zone 5B/6B 干燥高寒，高海拔日夜温差极端",
    "foundation": "全地下室为主，住宅人均面积大",
    "best_products": "抗干裂ABS出风口、大流量送风口、密封防风配件",
    "avoid_products": "湿热除霉配件（环境极干燥）",
    "channel_advice": "家庭人口多，儿童活动多，需重点突出防卡脚防异物设计"
  },
  {
    "abbr": "NE", "en": "Nebraska", "cn": "内布拉斯加州", "sales": 1601, "tier": "T2 稳定支撑带 (1500-2000)",
    "region": "中部大平原 (Midwest)", "climate": "Zone 5A 大陆性极寒多风，冬春暴雪多",
    "foundation": "地下室普及率极高，自建独立房多",
    "best_products": "大承重地面风口、防风防尘阀板、加厚耐磨五金",
    "avoid_products": "精细脆弱装饰件", "channel_advice": "注重产品实用寿命与抗踩踏能力，耐用性口碑最关键"
  },
  {
    "abbr": "CO", "en": "Colorado", "cn": "科罗拉多州", "sales": 1582, "tier": "T2 稳定支撑带 (1500-2000)",
    "region": "落基山高山区 (Mountain)", "climate": "Zone 5B/6B 高山半干旱，冬季漫长强积雪，夏季干爽",
    "foundation": "防冻深挖全地下室，建筑节能要求极高",
    "best_products": "高密封保温风口、大通风格栅、实木地板嵌入式风口",
    "avoid_products": "漏风串风严重劣质件", "channel_advice": "注重节能与绿色建材标准，对品质工艺认可度高"
  },
  {
    "abbr": "OK", "en": "Oklahoma", "cn": "俄克拉荷马州", "sales": 1543, "tier": "T2 稳定支撑带 (1500-2000)",
    "region": "中南部过渡平原 (South)", "climate": "Zone 3A/4A 温差大，夏季强风酷热，冬有寒潮",
    "foundation": "架空层与平板地基各半",
    "best_products": "防震耐风压配件、加固五金、通用标称风口",
    "avoid_products": "异形非标尺寸", "channel_advice": "春季极端天气修缮需求爆发，季节性补货规律明显"
  },
  {
    "abbr": "AR", "en": "Arkansas", "cn": "阿肯色州", "sales": 1514, "tier": "T2 稳定支撑带 (1500-2000)",
    "region": "中南内陆林区 (South)", "climate": "Zone 3A/4A 湿润多林区，冬温和夏闷热",
    "foundation": "架空层木结构普及率较高",
    "best_products": "防潮耐水ABS出风口、性价比金属配件、通用地垫配件",
    "avoid_products": "高溢价奢侈建材", "channel_advice": "性价比为主导，大众款标准化 4x10 尺寸走货最快"
  },
  {
    "abbr": "OR", "en": "Oregon", "cn": "俄勒冈州", "sales": 1476, "tier": "T3 常态中流带 (1000-1500)",
    "region": "太平洋西北岸 (Pacific)", "climate": "Zone 4C/5B 温带海洋性，秋冬持续阴雨高湿",
    "foundation": "木架空层(Crawl Space)为主，通风防潮需求高",
    "best_products": "耐潮防霉ABS风口、耐腐蚀不锈钢/铝配件、密封垫",
    "avoid_products": "未做防锈处理的廉价铁件", "channel_advice": "对环保环保标准(如无味ABS)要求严格，绿色理念受欢迎"
  },
  {
    "abbr": "MT", "en": "Montana", "cn": "蒙大拿州", "sales": 1436, "tier": "T3 常态中流带 (1000-1500)",
    "region": "北部大山高原 (Mountain)", "climate": "Zone 6B 亚寒带大陆气候，冬季极度严寒降雪极厚",
    "foundation": "深埋防冻土全地下室",
    "best_products": "耐严寒防脆化五金、大出风量格栅、坚固铁件",
    "avoid_products": "脆性塑料件", "channel_advice": "单店覆盖半径几百里，顾客单次采购量大，注重坚固"
  },
  {
    "abbr": "MI", "en": "Michigan", "cn": "密歇根州", "sales": 1378, "tier": "T3 常态中流带 (1000-1500)",
    "region": "五大湖中心区 (Midwest)", "climate": "Zone 5A/6A 严寒大雪带，大湖效应降雪极强",
    "foundation": "100%全地下室标配，地板风管贯通全屋",
    "best_products": "经典金属地板出风口、防化雪盐水腐蚀涂层风口",
    "avoid_products": "天花板专用件", "channel_advice": "底特律周边老屋改造基数庞大，换新频次极高"
  },
  {
    "abbr": "GA", "en": "Georgia", "cn": "乔治亚州", "sales": 1346, "tier": "T3 常态中流带 (1000-1500)",
    "region": "东南枢纽 (Southeast)", "climate": "Zone 3A 亚热带湿热，夏季长酷暑，冬季温和短暂",
    "foundation": "北部山区架空层多，亚特兰大以南以平板地基为主",
    "best_products": "天花板格栅与地面风口分品类销售、高耐湿五金",
    "avoid_products": "单押纯地面配件（南部平板无法装）", "channel_advice": "The Home Depot 全球总部所在地，标杆渠道必须深耕"
  },
  {
    "abbr": "WA", "en": "Washington", "cn": "华盛顿州", "sales": 1340, "tier": "T3 常态中流带 (1000-1500)",
    "region": "西北太平洋沿岸 (Pacific)", "climate": "Zone 4C 海洋多雨，西侧阴湿多雾，东侧干爽",
    "foundation": "架空层木结构多，现代独立新屋多",
    "best_products": "现代简约设计风口（极简线形/几何款）、防潮ABS件",
    "avoid_products": "过时老土粗糙款式", "channel_advice": "西雅图高科技中产多，偏好极简现代现代黑白灰色系"
  },
  {
    "abbr": "IL", "en": "Illinois", "cn": "伊利诺伊州", "sales": 1257, "tier": "T3 常态中流带 (1000-1500)",
    "region": "五大湖中枢 (Midwest)", "climate": "Zone 5A 典型温带大陆性寒冷区，冬风大寒冷",
    "foundation": "全地下室占压倒性多数",
    "best_products": "标准美标地面出风口、实木地板配合件、重型五金",
    "avoid_products": "薄型无卡槽风口", "channel_advice": "大芝加哥门店极为密集，虽单店被微稀释但全州总盘极大"
  },
  {
    "abbr": "PA", "en": "Pennsylvania", "cn": "宾夕法尼亚州", "sales": 1197, "tier": "T3 常态中流带 (1000-1500)",
    "region": "东北历史大州 (Northeast)", "climate": "Zone 5A/6A 寒冷多雪，老式建筑比例全美最高之一",
    "foundation": "石砌/混凝土深层地下室占主流",
    "best_products": "美式古典雕花风口（古铜/四叶草）、修缮替换件",
    "avoid_products": "超前极简不搭老屋的款式", "channel_advice": "注重传统复古美学，旧房木地板配金属风口是绝对主流"
  },
  {
    "abbr": "SD", "en": "South Dakota", "cn": "南达科他州", "sales": 1183, "tier": "T3 常态中流带 (1000-1500)",
    "region": "中北部高寒平原 (Midwest)", "climate": "Zone 5B/6B 严寒多风干旱，冬季零下20度多见",
    "foundation": "深挖全地下室",
    "best_products": "耐冻防裂金属风口、高强度密封阻风片",
    "avoid_products": "普通PVC脆化塑料件", "channel_advice": "门店数量少，单店客流稳定，实用主义第一"
  },
  {
    "abbr": "IA", "en": "Iowa", "cn": "爱荷华州", "sales": 1100, "tier": "T3 常态中流带 (1000-1500)",
    "region": "中部农业腹地 (Midwest)", "climate": "Zone 5A 寒冷大陆性，冬季长雪厚",
    "foundation": "几乎家家户户全地下室",
    "best_products": "实惠耐用型金属与ABS地面风口、标准尺寸套件",
    "avoid_products": "高价溢价概念品", "channel_advice": "Menards与THD渗透深，性价比走量款需求长盛不衰"
  },
  {
    "abbr": "NJ", "en": "New Jersey", "cn": "新泽西州", "sales": 1007, "tier": "T3 常态中流带 (1000-1500)",
    "region": "大纽约都会区 (Northeast)", "climate": "Zone 4A/5A 海洋微寒，冬雪夏热，高密度居住",
    "foundation": "老式地下室与紧凑地基并存",
    "best_products": "小巧精致型装饰风口、紧凑空间专用配件、高颜值五金",
    "avoid_products": "笨重大尺寸工业件", "channel_advice": "密度极高、通勤家庭翻修预算高，看重精致与易安装"
  },
  {
    "abbr": "NY", "en": "New York", "cn": "纽约州", "sales": 863, "tier": "T4 相对低周转区 (500-1000)",
    "region": "东北核心大州 (Northeast)", "climate": "Zone 5A/6A 严寒湿润，上州暴雪区，市区温和",
    "foundation": "市区多公寓(无独立暖通风管)，上州郊区独栋有地下室",
    "best_products": "郊区独栋地面风口、复古装饰盖板、散热暖气片罩",
    "avoid_products": "面向市区公寓销售的大型管道风口", "channel_advice": "纽约市区与上州完全割裂，需按店分发，市区店少铺地面件"
  },
  {
    "abbr": "WY", "en": "Wyoming", "cn": "怀俄明州", "sales": 846, "tier": "T4 相对低周转区 (500-1000)",
    "region": "高山草原荒漠 (Mountain)", "climate": "Zone 6B/7 极度干燥极寒大风高海拔",
    "foundation": "全地下室居多，但人口极其稀少",
    "best_products": "超耐寒工业级五金、结实铁构件", "avoid_products": "轻质薄件",
    "channel_advice": "全州人口不足60万，总体量受限，常规按需补货即可"
  },
  {
    "abbr": "MA", "en": "Massachusetts", "cn": "马萨诸塞州", "sales": 846, "tier": "T4 相对低周转区 (500-1000)",
    "region": "新英格兰核心 (Northeast)", "climate": "Zone 5A 寒冷多雪，近海湿冷",
    "foundation": "老洋房多，传统水暖暖气片(Boiler/Radiator)占比高",
    "best_products": "踢脚线出风口(Baseboard)、复古铸铁风口、局部升级件",
    "avoid_products": "强排热风专属塑料风口", "channel_advice": "老房很多不是强排风管系统，需查验当地供暖结构"
  },
  {
    "abbr": "NM", "en": "New Mexico", "cn": "新墨西哥州", "sales": 823, "tier": "T4 相对低周转区 (500-1000)",
    "region": "西南部沙漠高原 (Southwest)", "climate": "Zone 4B/5B 极端干旱少雨，昼夜温差极大，多沙尘",
    "foundation": "【图中标黄】土坯与水泥平板地基居多，极少地下室",
    "best_products": "防尘百叶出风口、耐晒耐高温五金、防沙密封件",
    "avoid_products": "标准地面下沉风口（地面无开孔管道）", "channel_advice": "天花板或高墙侧送风为主，主打防风沙密封性能"
  },
  {
    "abbr": "MN", "en": "Minnesota", "cn": "明尼苏达州", "sales": 771, "tier": "T4 相对低周转区 (500-1000)",
    "region": "中北部冰原区 (Midwest)", "climate": "Zone 6A/7 极寒雪原，全美最冷州之一",
    "foundation": "深层地下室占100%，但供暖以锅炉水暖+热风混合",
    "best_products": "重型防冷凝出风口、极耐寒五金", "avoid_products": "薄壁脆性塑料",
    "channel_advice": "虽然冷，但因门店密集且水暖分散了部分风管需求，店均平缓"
  },
  {
    "abbr": "NH", "en": "New Hampshire", "cn": "新罕布什尔州", "sales": 756, "tier": "T4 相对低周转区 (500-1000)",
    "region": "新英格兰北部 (Northeast)", "climate": "Zone 5A/6A 山地寒冷，林区多",
    "foundation": "地下室与石基为主，老木屋多",
    "best_products": "实木配套出风口、燃木炉辅助通风格栅", "avoid_products": "花哨塑料件",
    "channel_advice": "当地人动手能力强，偏好木质与金属自然质感"
  },
  {
    "abbr": "MS", "en": "Mississippi", "cn": "密西西比州", "sales": 737, "tier": "T4 相对低周转区 (500-1000)",
    "region": "深南墨西哥湾 (South)", "climate": "Zone 3A 极度闷热潮湿，无冬",
    "foundation": "平板地基与浅高架桩基",
    "best_products": "高抗湿防生锈件、天花排风罩、经济适用型五金",
    "avoid_products": "昂贵高端装饰品", "channel_advice": "人均收入偏低，走量款与极低客单价产品更易动销"
  },
  {
    "abbr": "VT", "en": "Vermont", "cn": "佛蒙特州", "sales": 717, "tier": "T4 相对低周转区 (500-1000)",
    "region": "新英格兰高山区 (Northeast)", "climate": "Zone 6A 寒冬多雪山区，人口少",
    "foundation": "全地下室，以乡村独栋木屋为主",
    "best_products": "生态环保无味风口、复古铸铝盖板", "avoid_products": "工业廉价塑料感产品",
    "channel_advice": "环保法令严，重视产品材质安全与耐久"
  },
  {
    "abbr": "ND", "en": "North Dakota", "cn": "北达科他州", "sales": 671, "tier": "T4 相对低周转区 (500-1000)",
    "region": "北部平原边境 (Midwest)", "climate": "Zone 6A/7 极寒冰封期长达半年",
    "foundation": "防冻深层地下室",
    "best_products": "超结实金属出风口、保温阻流构件", "avoid_products": "脆性塑料",
    "channel_advice": "人口仅70余万，大型商超网点少，单店绝对销售有限"
  },
  {
    "abbr": "CT", "en": "Connecticut", "cn": "康涅狄格州", "sales": 658, "tier": "T4 相对低周转区 (500-1000)",
    "region": "新英格兰南端 (Northeast)", "climate": "Zone 5A 海洋微寒，冬雪",
    "foundation": "地下室多，但高档独立住宅倾向专业施工定制",
    "best_products": "高档定制级装饰风格风口、拉丝金属构件", "avoid_products": "低档大众通用塑料件",
    "channel_advice": "DIY比例略低于中西部，Pro工程定制渠道占比较高"
  },
  {
    "abbr": "ME", "en": "Maine", "cn": "缅因州", "sales": 634, "tier": "T4 相对低周转区 (500-1000)",
    "region": "东北最边陲 (Northeast)", "climate": "Zone 6A 沿海湿冷多雾，冬漫长",
    "foundation": "传统地下室与岩石基底",
    "best_products": "防潮耐盐雾金属件、实木地板配合件", "avoid_products": "不耐湿五金",
    "channel_advice": "远离干线物流，运费成本较高，主推高客单长寿命品"
  },
  {
    "abbr": "RI", "en": "Rhode Island", "cn": "罗德岛州", "sales": 532, "tier": "T4 相对低周转区 (500-1000)",
    "region": "新英格兰沿海 (Northeast)", "climate": "Zone 5A 海洋性微寒湿润",
    "foundation": "传统老房，面积全美最小",
    "best_products": "常规标准修缮件", "avoid_products": "非标大件", "channel_advice": "全州仅几家大零售商超，整体容量小"
  },
  {
    "abbr": "LA", "en": "Louisiana", "cn": "路易斯安那州", "sales": 495, "tier": "T5 规避/需改良区 (<500)",
    "region": "墨西哥湾湿地平原 (South)", "climate": "Zone 2A/3A 极端湿热多雨，飓风与洪水多发",
    "foundation": "防洪高架柱或水泥平板，完全无地下室",
    "best_products": "天花板排风口、高耐蚀铝合金防锈构件、卫浴防霉件",
    "avoid_products": "地面直接下沉式出风口（水浸隐患，绝无地板风管）",
    "channel_advice": "绝不能铺地板风口；主推天花格栅和耐腐蚀户外建材"
  },
  {
    "abbr": "NV", "en": "Nevada", "cn": "内华达州", "sales": 460, "tier": "T5 规避/需改良区 (<500)",
    "region": "西南部沙漠干热带 (Mountain)", "climate": "Zone 3B 极端干旱酷热沙漠，夏季超42度",
    "foundation": "100%混凝土平板地基(Slab)，无地下空间",
    "best_products": "天花板可调风口、耐强紫外线防老化塑胶件、车库通风件",
    "avoid_products": "地面风口/地暖构件（本地无安装条件）",
    "channel_advice": "拉斯维加斯新城全为空调天花板下送风，按顶装逻辑选品"
  },
  {
    "abbr": "WI", "en": "Wisconsin", "cn": "威斯康星州", "sales": 456, "tier": "T5 规避/需改良区 (<500)",
    "region": "五大湖北部 (Midwest)", "climate": "Zone 5A/6A 漫长严寒多雪",
    "foundation": "全地下室普及", "best_products": "重型金属地板出风口、防冰冻五金", "avoid_products": "天花板专用风口",
    "channel_advice": "地处Menards核心发源腹地，本地本土品牌极强，需打价格差异化"
  },
  {
    "abbr": "TX", "en": "Texas", "cn": "德克萨斯州", "sales": 332, "tier": "T5 规避/需改良区 (<500)",
    "region": "南部阳光带核心 (South)", "climate": "Zone 2A/3A/3B 漫长干热与湿热，无冻土",
    "foundation": "80%+新建及存量住宅为混凝土平板(Slab-on-Grade)",
    "best_products": "天花板送风散流器、回风大滤网格栅、耐晒户外构件",
    "avoid_products": "地面下沉式出风口（全州几乎没有地板风管）",
    "channel_advice": "全美第二大州，总盘大但单店被极度稀释，品类必须切到天花与墙面"
  },
  {
    "abbr": "AZ", "en": "Arizona", "cn": "亚利桑那州", "sales": 289, "tier": "T5 规避/需改良区 (<500)",
    "region": "西南沙漠区 (Mountain)", "climate": "Zone 2B 极端干热少雨，酷暑期长达6个月",
    "foundation": "绝大多数为混凝土平板地基，无地下室",
    "best_products": "天花板空调扩散罩、抗高热变形ABS外壳、遮阳建材",
    "avoid_products": "地板风口（完全无地板开孔）",
    "channel_advice": "凤凰城等大区全面以顶装风口为主，强光紫外线耐受是测试红线"
  },
  {
    "abbr": "CA", "en": "California", "cn": "加利福尼亚州", "sales": 253, "tier": "T5 规避/需改良区 (<500)",
    "region": "太平洋沿岸 (Pacific)", "climate": "Zone 3B/4B 地中海温和干燥与内陆干热",
    "foundation": "南加基本全平板；北加部分木构架空；门店密度全美最密",
    "best_products": "Title 24节能合规密封风口、环保可回收材质、天花简约格栅",
    "avoid_products": "高铅低环保标准金属件、传统重工业风口",
    "channel_advice": "全美最大单一经济体，但门店极密摊薄单店，且加州法规(Prop 65)门槛高"
  },
  {
    "abbr": "FL", "en": "Florida", "cn": "佛罗里达州", "sales": 234, "tier": "T5 规避/需改良区 (<500)",
    "region": "东南半岛 (Southeast)", "climate": "Zone 1A/2A 全美最湿热，高盐雾高降雨飓风区，零供暖需求",
    "foundation": "由于高地下水位与无霜期，95%+为混凝土平板地基(Slab)",
    "best_products": "天花板出风口、防飓风抗风压配件、高抗盐雾工程塑料/阳极氧化铝配件",
    "avoid_products": "地面出风口（装无可装，一装就生锈受潮）",
    "channel_advice": "纯制冷市场，严禁把地面风口发往佛州；全面转战天花板出风与防腐五金"
  }
]

df_states = pd.DataFrame(STATES_DATA)
df_states["rank"] = df_states["sales"].rank(ascending=False, method="min").astype(int)

# ==============================================================================
# 3. 侧边栏模式切换
# ==============================================================================
with st.sidebar:
    st.header("⚙️ 功能导航")
    mode = st.radio(
        "选择查询维度：",
        ["🔍 按州/地区速查 (State Search)", "📦 按产品品类反查最适销售区 (Category Matrix)", "📊 全美 48 州全景大表 (Full Overview)"],
        index=0
    )
    st.markdown("---")
    st.info("""
    **💡 核心规律总结：**
    - **北方/中东部有地下室**：风管走地板，地面风口是刚需。
    - **南方阳光带(FL/TX)全为水泥平板**：风管走天花板，主推天花散流器与防潮五金。
    """)

# ==============================================================================
# 4. 模式一：按州 / 地区速查
# ==============================================================================
if mode == "🔍 按州/地区速查 (State Search)":
    st.subheader("🔍 单州详情与全景分析卡片")
    options = [f"{s['abbr']} - {s['cn']} ({s['en']})" for s in STATES_DATA]
    
    col1, col2 = st.columns()
    with col1:
        selected_option = st.selectbox("请选择或直接输入要查询的州（如输入 NC、CA、北卡、德州 等）：", options, index=0)
        selected_abbr = selected_option.split(" - ")[0]
    with col2:
        tier_filter = st.selectbox("或按梯队快速筛选：", ["全部梯队", "T1 黄金走廊 (>2000)", "T2 稳定支撑带 (1500-2000)", "T3 常态中流带 (1000-1500)", "T4 相对低周转区 (500-1000)", "T5 规避/需改良区 (<500)"])
        if tier_filter != "全部梯队":
            filtered_abbrs = [s["abbr"] for s in STATES_DATA if tier_filter[:2] in s["tier"]]
            if filtered_abbrs and selected_abbr not in filtered_abbrs:
                selected_abbr = filtered_abbrs[0]

    state = next((s for s in STATES_DATA if s["abbr"] == selected_abbr), STATES_DATA[0])
    rank = int(df_states[df_states["abbr"] == selected_abbr]["rank"].values[0])

    st.markdown(f"## 📌 {state['cn']} / {state['en']} (`{state['abbr']}`)")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📊 单店平均销量", f"{state['sales']:,} 件")
    m2.metric("🏆 全美48州销量排名", f"第 {rank} 名 / 48")
    m3.metric("🏷️ 业绩梯队", state["tier"].split(" ")[0])
    m4.metric("📍 所属大区", state["region"].split(" ")[0])

    st.markdown("---")
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("### 🌡️ 气候特征与负荷重点")
        st.write(f"**表现**：{state['climate']}")
        st.markdown("### 🏗️ 典型房屋地基与管网构造")
        st.write(f"**地基**：{state['foundation']}")
        
    with c_right:
        st.markdown("### ✅ 适销主推产品品类")
        st.success(f"{state['best_products']}")
        st.markdown("### ⚠️ 避坑/受限产品品类")
        st.warning(f"{state['avoid_products']}")

    st.markdown("### 🛒 零售渠道策略（The Home Depot / Lowe's / Menards）")
    st.info(f"**实战建议**：{state['channel_advice']}")

# ==============================================================================
# 5. 模式二：按产品品类反查销售区
# ==============================================================================
elif mode == "📦 按产品品类反查最适销售区 (Category Matrix)":
    st.subheader("📦 选择您的产品品类，一键查看全美推荐与避坑省份")
    category = st.selectbox(
        "请选择您的产品主攻品类方向：",
        [
            "1. 地面出风口/地面承重踏压配件 (Floor Registers & Grilles)",
            "2. 天花板/侧墙出风散流器与回风网 (Ceiling & Wall Diffusers)",
            "3. 高耐湿耐盐雾防腐五金/工程塑料 (Rust-Proof / Bath Hardware)",
            "4. 高寒防冻/抗暴雪大承重建材 (Cold & Freeze Resistant Supplies)",
            "5. 西南防晒耐高温/抗紫外线户外建材 (UV & Heat Resistant Supplies)"
        ]
    )
    
    if "地面出风口" in category:
        st.markdown("#### 🎯 针对品类：【地面出风口 / 地板承重配件】")
        c_top, c_avoid = st.columns(2)
        with c_top:
            st.success("🌟 **强烈推荐主推销售区域（Top 优先备货）**")
            t1_list = [s for s in STATES_DATA if "T1" in s["tier"]]
            for s in t1_list:
                st.markdown(f"- **{s['cn']} (`{s['abbr']}`)** - 单店销量: **{s['sales']:,}** | {s['foundation']}")
        with c_avoid:
            st.error("🚫 **受限/严禁盲目铺货区域（避坑警戒区）**")
            t5_list = [s for s in STATES_DATA if s["abbr"] in ["FL", "TX", "AZ", "NV", "LA"]]
            for s in t5_list:
                st.markdown(f"- **{s['cn']} (`{s['abbr']}`)** - 单店销量: **{s['sales']:,}** | {s['foundation']}，管道全在天花板")

    elif "天花板" in category:
        st.markdown("#### 🎯 针对品类：【天花板/侧墙散流出风口与回风网】")
        c_top, c_avoid = st.columns(2)
        with c_top:
            st.success("🌟 **主力增量市场（重点投放）**")
            st.markdown("- **佛罗里达 (FL)**、**德克萨斯 (TX)**、**亚利桑那 (AZ)**、**内华达 (NV)**、**乔治亚 (GA)**、**加利福尼亚 (CA)**\n- **核心理由**：这些州人口庞大，但全为水泥平板地基，风口全在天花板，市场容量极大！")
        with c_avoid:
            st.warning("⚠️ **北方传统大州注意事项**\n- 北方老房主力送风仍在地板，天花板多为回风口，铺货结构需平衡。")

    elif "耐湿耐盐雾" in category:
        st.markdown("#### 🎯 针对品类：【高耐湿耐盐雾防腐五金 / 工程ABS树脂配件】")
        st.success("🌟 **核心主攻区**：北卡 (NC)、南卡 (SC)、佛州 (FL)、路易斯安那 (LA)、阿拉巴马 (AL)、乔治亚 (GA) 沿海地区")

    elif "高寒防冻" in category:
        st.markdown("#### 🎯 针对品类：【高寒防冻 / 抗暴雪重载五金配件】")
        st.success("🌟 **核心主攻区**：明尼苏达 (MN)、北达科他 (ND)、爱达荷 (ID)、蒙大拿 (MT)、密歇根 (MI)、威斯康星 (WI)")

    elif "西南防晒" in category:
        st.markdown("#### 🎯 针对品类：【西南防晒耐高温 / 抗紫外线户外建材】")
        st.success("🌟 **核心主攻区**：亚利桑那 (AZ)、内华达 (NV)、新墨西哥 (NM)、德克萨斯 (TX)、南加州")

# ==============================================================================
# 6. 模式三：全美 48 州全景大表
# ==============================================================================
elif mode == "📊 全美 48 州全景大表 (Full Overview)":
    st.subheader("📊 全美 48 州单店销量与地理气候参数全景矩阵")
    
    avg_sales = int(df_states["sales"].mean())
    k1, k2, k3 = st.columns(3)
    k1.metric("全美 48 州平均单店销量", f"{avg_sales:,} 件")
    k2.metric("最高单店", "北卡罗来纳 NC (2,946 件)")
    k3.metric("最低单店", "佛罗里达 FL (234 件)")
    
    st.markdown("---")
    display_df = df_states[["rank", "abbr", "cn", "en", "sales", "tier", "region", "foundation", "best_products", "avoid_products"]]
    display_df.columns = ["排名", "缩写", "中文州名", "英文州名", "单店销量", "梯队", "地理大区", "地基结构", "适销主推品类", "避坑品类"]
    st.dataframe(display_df, use_container_width=True, height=600)
    
    csv = display_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 一键下载全美48州分析数据表 (.csv)",
        data=csv,
        file_name="US_48_States_Sales_Climate_Matrix.csv",
        mime="text/csv"
    )
