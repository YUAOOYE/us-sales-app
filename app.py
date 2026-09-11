import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 1. 页面配置与大零售 BI 科技蓝视觉风格
# ==============================================================================
st.set_page_config(
    page_title="北美大零售全品类与气候销售决策系统",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-title { font-size: 1.85rem; font-weight: 700; color: #0F172A; margin-bottom: 0.2rem; }
    .sub-title { font-size: 0.92rem; color: #475569; margin-bottom: 1rem; }
    
    .kpi-card {
        background: linear-gradient(135deg, #1E40AF, #3B82F6);
        color: white;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .kpi-title { font-size: 0.88rem; opacity: 0.92; margin-bottom: 4px; font-weight: 500; }
    .kpi-val { font-size: 1.75rem; font-weight: 700; }
    
    .cat-selector {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 14px;
    }
    .supply-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        background-color: #E2E8F0;
        font-size: 0.82rem;
        font-weight: 600;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏢 北美大零售多品类全属性与气候销售决策系统 (Pro Edition)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">覆盖北美 50 州建材消费画像 | 动态支持地基结构、气候分区、房屋年限、THD & Lowe\'s 渠道分销与仓储调拨策略</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. 全美 50 州基础数据库 (含阿拉斯加与夏威夷，补齐供应链与大区归属)
# ==============================================================================
STATES_DATA = [
  {"abbr": "NC", "en": "North Carolina", "cn": "北卡罗来纳州", "region": "美东南", "velocity": 2946, "thd_stores": 43, "lowes_stores": 112, "foundation": "架空层/地下室(75%+)", "climate": "Zone 4A/3A 混合湿润", "best": "地面出风口、地板耐磨五金", "avoid": "易锈冷轧薄铁件", "size_breakdown": "地面绝对主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "夏洛特枢纽"},
  {"abbr": "TN", "en": "Tennessee", "cn": "田纳西州", "region": "美中南", "velocity": 2902, "thd_stores": 31, "lowes_stores": 62, "foundation": "木结构架空层/地下室", "climate": "Zone 4A 混合温和", "best": "重载地面风口、承重踏压件", "avoid": "天花专用下送风口", "size_breakdown": "地面绝对主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "孟菲斯全美总仓"},
  {"abbr": "KY", "en": "Kentucky", "cn": "肯塔基州", "region": "美中", "velocity": 2579, "thd_stores": 18, "lowes_stores": 44, "foundation": "全地下室占80%+", "climate": "Zone 4A 四季鲜明多雪", "best": "地下管道地面风口、复古风口", "avoid": "无调节阀空框", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 3, "dc_hub": "路易斯维尔"},
  {"abbr": "SC", "en": "South Carolina", "cn": "南卡罗来纳州", "region": "美东南", "velocity": 2433, "thd_stores": 28, "lowes_stores": 52, "foundation": "架空层/沿海桩基", "climate": "Zone 3A 亚热带湿热", "best": "工程ABS风口、耐盐雾构件", "avoid": "未做防锈处理普通铁件", "size_breakdown": "通用型: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 40%, LVP 35%, 瓷砖 15%, 地毯 10%", "lead_days": 2, "dc_hub": "夏洛特枢纽"},
  {"abbr": "WV", "en": "West Virginia", "cn": "西弗吉尼亚州", "region": "美东", "velocity": 2248, "thd_stores": 7, "lowes_stores": 19, "foundation": "山地深地基/全地下室", "climate": "Zone 5A 湿润山地极寒", "best": "抗重压地面风口、防冻融五金", "avoid": "脆性塑料件", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "匹兹堡分仓"},
  {"abbr": "ID", "en": "Idaho", "cn": "爱达荷州", "region": "美西", "velocity": 2213, "thd_stores": 12, "lowes_stores": 14, "foundation": "深层地下室(85%+)", "climate": "Zone 5B/6B 干燥高寒", "best": "强排暖风风口、防风密封件", "avoid": "湿热除霉配件", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 4, "dc_hub": "盐湖城枢纽"},
  {"abbr": "VA", "en": "Virginia", "cn": "弗吉尼亚州", "region": "美东", "velocity": 2169, "thd_stores": 46, "lowes_stores": 68, "foundation": "地下室/架空层老房多", "climate": "Zone 4A 四季湿润冬冷", "best": "中高端装饰风口、精工硬装", "avoid": "粗糙低端工程件", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "里士满仓"},
  {"abbr": "KS", "en": "Kansas", "cn": "堪萨斯州", "region": "美中大平原", "velocity": 2124, "thd_stores": 16, "lowes_stores": 18, "foundation": "100%全地下室", "climate": "Zone 4A/5A 大陆性严寒大风", "best": "大风量地面风口、耐压风门", "avoid": "轻质易吹脱件", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "堪萨斯城枢纽"},
  {"abbr": "DE", "en": "Delaware", "cn": "特拉华州", "region": "美东", "velocity": 2122, "thd_stores": 6, "lowes_stores": 7, "foundation": "地下室/浅架空层", "climate": "Zone 4A 温和多潮", "best": "标准4x10尺寸风口、免税走量款", "avoid": "非标冷门异形件", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 2, "dc_hub": "费城分仓"},
  {"abbr": "AL", "en": "Alabama", "cn": "阿拉巴马州", "region": "美东南", "velocity": 2095, "thd_stores": 28, "lowes_stores": 40, "foundation": "山区架空层/平原混合", "climate": "Zone 3A 亚热带湿热", "best": "防潮ABS风口、通用通风罩", "avoid": "未保护易氧化金属", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "伯明翰仓"},
  {"abbr": "IN", "en": "Indiana", "cn": "印第安纳州", "region": "美中", "velocity": 2020, "thd_stores": 34, "lowes_stores": 47, "foundation": "全地下室占85%+", "climate": "Zone 5A 严寒多雪", "best": "地面暖风风口、防结冰构件", "avoid": "天花板专用散流器", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "印第安纳波利斯"},
  {"abbr": "MO", "en": "Missouri", "cn": "密苏里州", "region": "美中", "velocity": 1958, "thd_stores": 36, "lowes_stores": 42, "foundation": "传统全地下室木屋", "climate": "Zone 4A/5A 大陆季风冬冷", "best": "地面可调风口、管道连接件", "avoid": "纯热带建材", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "圣路易斯仓"},
  {"abbr": "MD", "en": "Maryland", "cn": "马里兰州", "region": "美东", "velocity": 1935, "thd_stores": 41, "lowes_stores": 31, "foundation": "老房地下室/联排镇屋", "climate": "Zone 4A 四季湿润冬寒", "best": "静音地面风口、防卡脚配件", "avoid": "粗矿工业件", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "巴尔的摩仓"},
  {"abbr": "OH", "en": "Ohio", "cn": "俄亥俄州", "region": "美中", "velocity": 1768, "thd_stores": 68, "lowes_stores": 82, "foundation": "全地下室为主", "climate": "Zone 5A 寒冷多雪长冬", "best": "冲压金属/铸铝地面风口", "avoid": "薄脆塑料", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "哥伦布核心仓"},
  {"abbr": "UT", "en": "Utah", "cn": "犹他州", "region": "美西", "velocity": 1666, "thd_stores": 22, "lowes_stores": 12, "foundation": "全地下室大户型", "climate": "Zone 5B/6B 高山干燥极寒", "best": "抗干裂ABS风口、密封防风件", "avoid": "湿热除湿件", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "盐湖城枢纽"},
  {"abbr": "NE", "en": "Nebraska", "cn": "内布拉斯加州", "region": "美中大平原", "velocity": 1601, "thd_stores": 11, "lowes_stores": 9, "foundation": "全地下室独立屋", "climate": "Zone 5A 极寒多暴风雪", "best": "大承重地面风口、加厚五金", "avoid": "精细易损件", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "奥马哈仓"},
  {"abbr": "CO", "en": "Colorado", "cn": "科罗拉多州", "region": "美西高地", "velocity": 1582, "thd_stores": 44, "lowes_stores": 30, "foundation": "防冻全地下室", "climate": "Zone 5B/6B 高海拔强积雪", "best": "高气密保温风口、实木嵌入风口", "avoid": "漏风劣质件", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "丹佛物流仓"},
  {"abbr": "OK", "en": "Oklahoma", "cn": "俄克拉荷马州", "region": "美中南", "velocity": 1543, "thd_stores": 17, "lowes_stores": 26, "foundation": "架空层与平板各半", "climate": "Zone 3A/4A 极端温差风大", "best": "防风压配件、加固五金", "avoid": "非标冷门尺寸", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "达拉斯辐射仓"},
  {"abbr": "AR", "en": "Arkansas", "cn": "阿肯色州", "region": "美中南", "velocity": 1514, "thd_stores": 14, "lowes_stores": 27, "foundation": "林区架空层木屋多", "climate": "Zone 3A/4A 湿润森林温和", "best": "防潮耐水ABS风口、平价金属件", "avoid": "高价奢侈品", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "小石城分仓"},
  {"abbr": "OR", "en": "Oregon", "cn": "俄勒冈州", "region": "美西北", "velocity": 1476, "thd_stores": 26, "lowes_stores": 15, "foundation": "架空层木结构(Crawl)", "climate": "Zone 4C 海洋湿冷多雨", "best": "耐水防霉ABS风口、不锈钢配件", "avoid": "易锈生铁件", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "波特兰仓"},
  {"abbr": "MT", "en": "Montana", "cn": "蒙大拿州", "region": "美西北高寒", "velocity": 1436, "thd_stores": 7, "lowes_stores": 5, "foundation": "深埋防冻全地下室", "climate": "Zone 6B 严寒多雪", "best": "超耐寒金属件、坚固大格栅", "avoid": "低温脆化塑料", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 4, "dc_hub": "比灵斯仓"},
  {"abbr": "MI", "en": "Michigan", "cn": "密歇根州", "region": "美中大湖", "velocity": 1378, "thd_stores": 70, "lowes_stores": 43, "foundation": "100%全地下室", "climate": "Zone 5A/6A 大湖雪带漫长冬", "best": "经典地面金属风口、防化雪盐件", "avoid": "天花专用风口", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "底特律仓"},
  {"abbr": "GA", "en": "Georgia", "cn": "乔治亚州", "region": "美东南", "velocity": 1346, "thd_stores": 89, "lowes_stores": 63, "foundation": "北架空层/南平板地基", "climate": "Zone 3A 亚热带长夏湿热", "best": "天花与地面品类分推、防腐五金", "avoid": "全推纯地面件", "size_breakdown": "地面天花混合: 4x10 (40%), 散流器 (40%)", "flooring_preference": "LVP 40%, 瓷砖 35%, 地毯 25%", "lead_days": 1, "dc_hub": "亚特兰大(THD全球总部)"},
  {"abbr": "WA", "en": "Washington", "cn": "华盛顿州", "region": "美西北", "velocity": 1340, "thd_stores": 43, "lowes_stores": 37, "foundation": "架空层与现代住宅", "climate": "Zone 4C 阴湿多雾", "best": "极简线形风口、环保无味ABS件", "avoid": "过时粗糙件", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "西雅图枢纽"},
  {"abbr": "IL", "en": "Illinois", "cn": "伊利诺伊州", "region": "美中", "velocity": 1257, "thd_stores": 82, "lowes_stores": 38, "foundation": "全地下室占多数", "climate": "Zone 5A 大陆性严寒冬风大", "best": "标准地面出风口、重型五金", "avoid": "薄型无卡槽风口", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "大芝加哥枢纽"},
  {"abbr": "PA", "en": "Pennsylvania", "cn": "宾夕法尼亚州", "region": "美东北", "velocity": 1197, "thd_stores": 69, "lowes_stores": 84, "foundation": "老房地下室比例高", "climate": "Zone 5A/6A 寒冷多雪老区", "best": "古典复古雕花风口、金属件", "avoid": "现代过于极简款", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "哈里斯堡仓"},
  {"abbr": "SD", "en": "South Dakota", "cn": "南达科他州", "region": "美中大平原", "velocity": 1183, "thd_stores": 4, "lowes_stores": 3, "foundation": "防冻深层地下室", "climate": "Zone 5B/6B 严寒干燥多风", "best": "耐低温防裂金属风口", "avoid": "易碎薄塑料", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 4, "dc_hub": "苏瀑仓"},
  {"abbr": "IA", "en": "Iowa", "cn": "爱荷华州", "region": "美中", "velocity": 1100, "thd_stores": 18, "lowes_stores": 17, "foundation": "几乎全地下室", "climate": "Zone 5A 寒冷长冬大雪", "best": "高性价比金属与ABS风口", "avoid": "昂贵概念品", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "得梅因仓"},
  {"abbr": "NJ", "en": "New Jersey", "cn": "新泽西州", "region": "美东北", "velocity": 1007, "thd_stores": 64, "lowes_stores": 41, "foundation": "紧凑型地下室多", "climate": "Zone 4A/5A 海洋微寒密集居住", "best": "小巧精致风口、美观五金", "avoid": "粗矿工业件", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "纽瓦克核心仓"},
  {"abbr": "NY", "en": "New York", "cn": "纽约州", "region": "美东北", "velocity": 863, "thd_stores": 102, "lowes_stores": 68, "foundation": "市区公寓无风管/郊区独栋地下室", "climate": "Zone 5A/6A 湿冷上州大雪", "best": "郊区独栋地面件、复古暖气罩", "avoid": "市区公寓推地板风管件", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "奥尔巴尼仓"},
  {"abbr": "WY", "en": "Wyoming", "cn": "怀俄明州", "region": "美西高地", "velocity": 846, "thd_stores": 4, "lowes_stores": 2, "foundation": "全地下室人口稀少", "climate": "Zone 6B/7 极寒干燥大风", "best": "超耐寒重型五金", "avoid": "轻质薄件", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 4, "dc_hub": "夏延仓"},
  {"abbr": "MA", "en": "Massachusetts", "cn": "马萨诸塞州", "region": "美东北", "velocity": 846, "thd_stores": 46, "lowes_stores": 26, "foundation": "水暖暖气片(Radiator)多", "climate": "Zone 5A 寒冷多雪近海湿冷", "best": "踢脚线出风口、复古铸铁风口", "avoid": "强排风管专属塑料件", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "波士顿分仓"},
  {"abbr": "NM", "en": "New Mexico", "cn": "新墨西哥州", "region": "美西南", "velocity": 823, "thd_stores": 13, "lowes_stores": 14, "foundation": "水泥平板地基(Slab)为主", "climate": "Zone 4B/5B 沙漠干旱多风沙", "best": "防尘百叶、耐晒高温五金", "avoid": "地面下沉式出风口", "size_breakdown": "天花散流器: 6x6, 8x8, 12x12; 墙面回风", "flooring_preference": "瓷砖 50%, 水泥抛光 30%, 地毯 20%", "lead_days": 3, "dc_hub": "阿尔伯克基仓"},
  {"abbr": "MN", "en": "Minnesota", "cn": "明尼苏达州", "region": "美中北高寒", "velocity": 771, "thd_stores": 33, "lowes_stores": 13, "foundation": "深层地下室但水暖多", "climate": "Zone 6A/7 极寒雪原", "best": "重型防冷凝风口、耐寒五金", "avoid": "易脆塑料", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 3, "dc_hub": "明尼阿波利斯仓"},
  {"abbr": "NH", "en": "New Hampshire", "cn": "新罕布什尔州", "region": "美东北", "velocity": 756, "thd_stores": 19, "lowes_stores": 12, "foundation": "石基与木屋", "climate": "Zone 5A/6A 林区寒冷", "best": "实木配风口、自然金属件", "avoid": "廉价塑料件", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 3, "dc_hub": "曼彻斯特仓"},
  {"abbr": "MS", "en": "Mississippi", "cn": "密西西比州", "region": "美东南", "velocity": 737, "thd_stores": 16, "lowes_stores": 24, "foundation": "平板地基与浅架空", "climate": "Zone 3A 闷热高湿无冬", "best": "高抗湿防生锈件、天花排风罩", "avoid": "高端奢侈品", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 3, "dc_hub": "杰克逊仓"},
  {"abbr": "VT", "en": "Vermont", "cn": "佛蒙特州", "region": "美东北", "velocity": 717, "thd_stores": 4, "lowes_stores": 2, "foundation": "全地下室山地木屋", "climate": "Zone 6A 寒冬多雪", "best": "环保无味风口、铸铝盖板", "avoid": "劣质塑料感产品", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 3, "dc_hub": "伯灵顿仓"},
  {"abbr": "ND", "en": "North Dakota", "cn": "北达科他州", "region": "美中北极寒", "velocity": 671, "thd_stores": 4, "lowes_stores": 3, "foundation": "防冻深层地下室", "climate": "Zone 6A/7 极寒半年冰封", "best": "结实金属风口、保温构件", "avoid": "脆性塑料", "size_breakdown": "标准通用: 4x10 (70%), 4x12 (15%), 2x12 (10%)", "flooring_preference": "LVP 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "lead_days": 4, "dc_hub": "法戈仓"},
  {"abbr": "CT", "en": "Connecticut", "cn": "康涅狄格州", "region": "美东北", "velocity": 658, "thd_stores": 30, "lowes_stores": 14, "foundation": "老房地下室但定制工程多", "climate": "Zone 5A 海洋微寒多雪", "best": "高档定制级拉丝金属风口", "avoid": "低档大众通用塑料", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "哈特福德仓"},
  {"abbr": "ME", "en": "Maine", "cn": "缅因州", "region": "美东北", "velocity": 634, "thd_stores": 11, "lowes_stores": 8, "foundation": "传统地下室与岩基", "climate": "Zone 6A 沿海湿冷多雾", "best": "防潮耐盐雾金属件", "avoid": "不耐湿五金", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 4, "dc_hub": "波特兰仓"},
  {"abbr": "RI", "en": "Rhode Island", "cn": "罗德岛州", "region": "美东北", "velocity": 532, "thd_stores": 7, "lowes_stores": 4, "foundation": "老房紧凑型", "climate": "Zone 5A 海洋微寒", "best": "常规标准修缮件", "avoid": "异形大件", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "普罗维登斯仓"},
  {"abbr": "LA", "en": "Louisiana", "cn": "路易斯安那州", "region": "美南沿海", "velocity": 495, "thd_stores": 27, "lowes_stores": 31, "foundation": "防洪高架柱/水泥平板", "climate": "Zone 2A/3A 极端湿热易涝", "best": "天花排风口、高耐蚀铝合金防锈件", "avoid": "地面下沉式出风口", "size_breakdown": "天花散流器: 6x6, 8x8, 12x12; 侧墙回风", "flooring_preference": "瓷砖 50%, 抛光强化 30%, 地毯 20%", "lead_days": 3, "dc_hub": "新奥尔良仓"},
  {"abbr": "NV", "en": "Nevada", "cn": "内华达州", "region": "美西南沙漠", "velocity": 460, "thd_stores": 19, "lowes_stores": 14, "foundation": "100%混凝土平板(Slab)", "climate": "Zone 3B 极端干旱酷热沙漠", "best": "天花板可调风口、抗紫外线塑料件", "avoid": "地面出风口", "size_breakdown": "天花散流器: 6x6, 8x8, 12x12", "flooring_preference": "瓷砖 50%, 强化复合 30%, 地毯 20%", "lead_days": 3, "dc_hub": "拉斯维加斯仓"},
  {"abbr": "WI", "en": "Wisconsin", "cn": "威斯康星州", "region": "美中大湖", "velocity": 456, "thd_stores": 28, "lowes_stores": 13, "foundation": "全地下室普及", "climate": "Zone 5A/6A 漫长严寒多雪", "best": "重型金属地板出风口、防冻五金", "avoid": "天花专用风口", "size_breakdown": "地面主力: 4x10 (65%); 4x12 (20%); 2x12 (10%)", "flooring_preference": "实木 45%, LVP 35%, 瓷砖 10%, 地毯 10%", "lead_days": 2, "dc_hub": "密尔沃基仓"},
  {"abbr": "TX", "en": "Texas", "cn": "德克萨斯州", "region": "美南核心", "velocity": 332, "thd_stores": 180, "lowes_stores": 142, "foundation": "80%+混凝土平板地基(Slab)", "climate": "Zone 2A/3A/3B 漫长干热湿热", "best": "天花散流器、回风滤网格栅", "avoid": "地面下沉式出风口", "size_breakdown": "天花散流器: 6x6, 8x8, 12x12; 墙面回风", "flooring_preference": "瓷砖 50%, 水泥抛光 30%, 地毯 20%", "lead_days": 2, "dc_hub": "达拉斯/休斯敦大仓"},
  {"abbr": "AZ", "en": "Arizona", "cn": "亚利桑那州", "region": "美西南沙漠", "velocity": 289, "thd_stores": 58, "lowes_stores": 33, "foundation": "绝大多数为混凝土平板", "climate": "Zone 2B 纯沙漠干热长酷暑", "best": "天花板空调扩散器、遮阳建材", "avoid": "地面风口", "size_breakdown": "天花散流器: 6x6, 8x8, 12x12", "flooring_preference": "瓷砖 50%, 强化地板 30%, 地毯 20%", "lead_days": 2, "dc_hub": "凤凰城枢纽"},
  {"abbr": "CA", "en": "California", "cn": "加利福尼亚州", "region": "美西海岸", "velocity": 253, "thd_stores": 232, "lowes_stores": 113, "foundation": "南加全平板/网点全美最密", "climate": "Zone 3B/4B 干燥温和干热", "best": "Title 24环保合规风口、天花格栅", "avoid": "高铅普通锻造件", "size_breakdown": "天花散流器: 6x6, 8x8, 10x10, 12x12", "flooring_preference": "瓷砖 45%, LVP 35%, 地毯 20%", "lead_days": 2, "dc_hub": "安大略/洛杉矶总仓"},
  {"abbr": "FL", "en": "Florida", "cn": "佛罗里达州", "region": "美东南半岛", "velocity": 234, "thd_stores": 154, "lowes_stores": 128, "foundation": "95%+混凝土平板地基(Slab)", "climate": "Zone 1A/2A 极湿热高盐雾飓风", "best": "天花出风口、防腐铝/ABS配件", "avoid": "地面出风口", "size_breakdown": "天花散流器: 6x6, 8x8, 12x12; 墙面滤网", "flooring_preference": "瓷砖 60%, 强化/LVP 25%, 地毯 15%", "lead_days": 2, "dc_hub": "奥兰多枢纽"},
  # 扩充：补齐第 49、50 州
  {"abbr": "AK", "en": "Alaska", "cn": "阿拉斯加州", "region": "非本土极寒", "velocity": 920, "thd_stores": 7, "lowes_stores": 5, "foundation": "永久冻土抬升/深基岩保温仓", "climate": "Zone 7/8 全美最高寒", "best": "超耐冻极温五金、重载保温出风件", "avoid": "常温塑料及薄冷轧铁", "size_breakdown": "重型金属: 4x10 (60%), 4x12 (25%), 6x12 (15%)", "flooring_preference": "强化保温地板 50%, 实木 30%, 瓷砖 20%", "lead_days": 7, "dc_hub": "安克雷奇港口驳运仓"},
  {"abbr": "HI", "en": "Hawaii", "cn": "夏威夷州", "region": "非本土海岛", "velocity": 410, "thd_stores": 7, "lowes_stores": 4, "foundation": "火山岩地基/架空防潮桩", "climate": "Zone 1 强热带高盐雾高腐蚀", "best": "316/304不锈钢、纯ABS高防腐构件", "avoid": "含铁电镀件、地面出风口", "size_breakdown": "天花抗盐雾格栅: 6x6, 8x8, 12x12", "flooring_preference": "耐水瓷砖 60%, 纯防水LVP 30%, 竹木 10%", "lead_days": 8, "dc_hub": "火奴鲁鲁海运仓"}
]

# ==============================================================================
# 3. 顶级产品品类配置
# ==============================================================================
CATEGORY_CONFIG = {
    "1. 暖通通风与空气分配 (HVAC & Ventilation)": {
        "tag": "HVAC",
        "short_name": "暖通通风",
        "intro": "包括地面出风口、天花散流器、回风百叶格栅及管道连接件。核心动销受【地基形态（全地下室 vs 水泥平板）】和【冷热空气对流】绝对支配。",
        "positions": ["(全选)", "Floor (地面)", "Ceiling (天花板)", "Sidewall/Ceiling (侧墙/天花通用)", "Baseboard (踢脚线)"],
        "materials": ["(全选)", "Aluminum (铝合金)", "Steel (冲压钢)", "Plastic (ABS工程树脂)", "Copper (紫铜/红铜)", "Wooden (实木)"],
        "finishes": ["(全选)", "BL (Matte Black 哑光黑)", "BN (Brushed Nickel 拉丝镍)", "WH (White 经典白)", "DO (Dark Bronze 深古铜)", "AB (Antique Brass 仿古黄铜)", "BR (Brass 亮黄铜)", "GA (Gray 铝原灰)"],
        "sizes": ["(全选)", "04X10 (主流大通货)", "04X12 (主流大通货)", "02X10 (狭长/紧凑区)", "02X12 (狭长/踢脚线)", "06X10 (大出风量)", "06X12 (大排风量)", "08X08 (天花板方型)", "12X12 (商业/天花大尺寸)"]
    },
    "2. 卫浴五金与地漏给排水 (Plumbing & Bath Hardware)": {
        "tag": "PLUMBING",
        "short_name": "卫浴给排水",
        "intro": "包括不锈钢淋浴地漏、长条隐形地漏、防臭下水器、防冻水阀与水暖构件。受【水质硬度、盐雾湿度、冬季深层冻结风险】决定。",
        "positions": ["(全选)", "Floor Drain (地面地漏/排水口)", "Linear Drain (长条隐形线性地漏)", "Wall Mount (墙面挂件/淋浴五金)", "Frost-Proof Valve (室外防冻阀/管道构件)"],
        "materials": ["(全选)", "Stainless Steel 304 (304不锈钢)", "Solid Brass (精铸黄铜)", "ABS/PVC (耐腐工程塑料)", "Zinc Alloy (锌合金)"],
        "finishes": ["(全选)", "BN (Brushed Nickel 拉丝镍)", "MB (Matte Black 哑光黑)", "CP (Chrome 抛光亮铬)", "BG (Brushed Gold 拉丝金)", "ORB (Oil Rubbed Bronze 古铜)"],
        "sizes": ["(全选)", "4x4 inch (标准方形地漏)", "6x6 inch (大排量地漏)", "24-36 inch (长条形隐形地漏)", "1/2 inch (常规进水接口)", "3/4 inch (主水管接口)"]
    },
    "3. 地面收口压条与瓷砖金属辅料 (Flooring & Tile Trim)": {
        "tag": "FLOORING",
        "short_name": "地面收口辅料",
        "intro": "包括实木/复合地板T型压条、高低过渡扣条、瓷砖防撞金属收边条、楼梯防滑包角。受【硬木地板普及率 vs 瓷砖大板偏好】决定。",
        "positions": ["(全选)", "T-Molding (同高地面平接T型条)", "Reducer (高低不平地面缓坡减速条)", "Tile Edge Trim (瓷砖L型防撞收边条)", "Stair Nosing (楼梯防滑包角踏步条)"],
        "materials": ["(全选)", "Anodized Aluminum (阳极氧化铝合金)", "Stainless Steel (高硬度不锈钢)", "Solid Hardwood (橡木/原木)", "Flexible PVC (高弹收边条)"],
        "finishes": ["(全选)", "Silver/Matte (哑光拉丝银)", "Titanium Black (钛黑/哑光黑)", "Champagne (香槟金)", "Dark Bronze (仿古深铜)", "Wood Grain (仿真木纹)"],
        "sizes": ["(全选)", "36 inch (单开门标准宽)", "72 inch (双扇门大跨度)", "96 inch (工程长条)", "8mm-10mm (常规瓷砖收口)", "12mm-15mm (大理石/厚砖收口)"]
    },
    "4. 门窗五金与密封防风防暴 (Doors, Windows & Hardware)": {
        "tag": "DOORS",
        "short_name": "门窗密封五金",
        "intro": "包括门底防冷风条、隔音密封条、防飓风加固角码、重型大门合页。受【北方冬季寒风密封节能 vs 东南沿海防飓风法规强制】决定。",
        "positions": ["(全选)", "Door Bottom Sweep (门底防风挡水刷/密封条)", "Weatherstripping (门框/窗框V型隔热密封条)", "Heavy Hinge (重型轴承门合页)", "Hurricane Tie (建筑防飓风抗风压连接件)"],
        "materials": ["(全选)", "Aluminum + Silicone (铝合金托底+耐候硅胶)", "Heavy Duty Steel (加厚冷轧钢)", "Solid Brass (重型纯铜)", "Stainless Steel (防锈不锈钢)"],
        "finishes": ["(全选)", "BL (Matte Black 哑光黑)", "Satin Nickel (缎面拉丝银)", "White (门框经典白)", "Zinc Galvanized (工业镀锌银)"],
        "sizes": ["(全选)", "36 inch (标准单门底条)", "42 inch (大入户门底条)", "3.5x3.5 inch (轻型室内合页)", "4x4 inch (重载大门合页)", "50 ft Roll (50英尺整卷密封条)"]
    },
    "5. 户外庭院、排水沟与结构件 (Outdoor Drainage & Patio)": {
        "tag": "OUTDOOR",
        "short_name": "庭院户外排水",
        "intro": "包括车道/泳池周边排水沟、排水格栅盖板、屋檐落水管防树叶滤网、地台立柱底座。受【暴雨排涝负荷、融雪量与室外高紫外线】决定。",
        "positions": ["(全选)", "Trench/Channel Drain (车道/泳池线性排水沟与格栅)", "Gutter Guard (屋檐排水天沟防叶滤网)", "Post Anchor Base (木亭地台立柱固定底座)", "Outdoor Wall Vent (室外防风雨冲压百叶)"],
        "materials": ["(全选)", "Hot-Dip Galvanized (热浸镀锌重钢)", "Polymer/HDPE (耐暴晒耐候塑料)", "Ductile Cast Iron (重载球墨铸铁)", "Cast Aluminum (耐候防腐铸铝)"],
        "finishes": ["(全选)", "Galvanized Silver (热镀锌防腐银)", "Black Asphalt (沥青防腐黑漆)", "Natural Cement Gray (水泥灰)"],
        "sizes": ["(全选)", "39 inch / 1 Meter (1米标准排水沟单元)", "4x4 inch (木方柱底座)", "6x6 inch (重型大立柱底座)", "5-6 inch (全美标准屋檐排水天沟网)"]
    }
}

st.markdown('<div class="cat-selector">', unsafe_allow_html=True)
c_sel, c_desc = st.columns([1.2, 2.8])
with c_sel:
    chosen_cat_name = st.selectbox(
        "📂 请选择您的核心产品品类：",
        list(CATEGORY_CONFIG.keys()),
        index=0
    )
cur_cat_conf = CATEGORY_CONFIG[chosen_cat_name]
with c_desc:
    st.markdown(f"**💡 品类应用与气象结构画像**：\n\n{cur_cat_conf['intro']}")
st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4. 第二层级：与当前品类动态绑定的四大属性筛选栏
# ==============================================================================
f_col1, f_col2, f_col3, f_col4 = st.columns(4)

with f_col1:
    selected_pos_raw = st.selectbox("1. 安装位置 (Position)：", cur_cat_conf["positions"], index=0)
    sel_pos = selected_pos_raw.split(" ")[0]

with f_col2:
    selected_mat_raw = st.selectbox("2. 材质 (Material)：", cur_cat_conf["materials"], index=0)
    sel_mat = selected_mat_raw.split(" ")[0]

with f_col3:
    selected_fin_raw = st.selectbox("3. 表面工艺/颜色 (Finish)：", cur_cat_conf["finishes"], index=0)
    sel_fin = selected_fin_raw.split(" ")[0]

with f_col4:
    selected_size_raw = st.selectbox("4. 规格尺寸 (Size)：", cur_cat_conf["sizes"], index=0)
    sel_size = selected_size_raw.split(" ")[0]

st.markdown("---")

# ==============================================================================
# 5. 全维多属性全美动销流速计算引擎
# ==============================================================================
calculated_states = []

for s in STATES_DATA:
    abbr = s["abbr"]
    base_velocity = s["velocity"]
    total_stores = s["thd_stores"] + s["lowes_stores"]
    
    weight = 1.0
    reasons = []
    
    # ---------------- A. 品类与安装位置 (Position) 逻辑 ----------------
    if cur_cat_conf["tag"] == "HVAC":
        if sel_pos == "Floor":
            if abbr in ["NC", "TN", "KY", "IN", "OH", "MI", "WV", "IL", "PA", "AK"]:
                weight *= 1.15
                reasons.append("全地下室/架空层主场，热气下沉刚需地面向上吹送")
            elif abbr in ["FL", "TX", "AZ", "NV", "LA", "HI"]:
                weight *= 0.12
                reasons.append("100%混凝土平板地基限制，地面无开孔管道")
        elif sel_pos == "Ceiling":
            if abbr in ["FL", "TX", "AZ", "NV", "CA", "GA", "HI"]:
                weight *= 2.6
                reasons.append("南方强冷气区域，出风口全部集中在天花板")
            elif abbr in ["MI", "ND", "MN", "WI", "AK"]:
                weight *= 0.5
                reasons.append("北方极寒地带一层以地面向上采暖送风为主")
        elif sel_pos == "Baseboard":
            if abbr in ["PA", "NY", "MA", "CT", "OH", "NJ", "RI"]:
                weight *= 1.8
                reasons.append("东北部老宅水暖踢脚线与狭长缝隙出风改造密集")

    elif cur_cat_conf["tag"] == "PLUMBING":
        if sel_pos in ["Linear Drain", "Floor Drain"]:
            if abbr in ["FL", "CA", "TX", "NC", "SC", "GA", "AZ"]:
                weight *= 1.9
                reasons.append("南部与西海岸无门槛淋浴房(Curbless Walk-in)现代大板翻新爆发")
        elif sel_pos == "Frost-Proof Valve":
            if abbr in ["MN", "WI", "MI", "ND", "SD", "IL", "OH", "AK"]:
                weight *= 2.8
                reasons.append("深冬极深冻土层，防冻水龙头是保险与建筑强制规范")
            elif abbr in ["FL", "TX", "AZ", "HI"]:
                weight *= 0.1
                reasons.append("常年无冻结风险，防冻阀几乎零出货")
        elif sel_pos == "Wall Mount":
            if abbr in ["CA", "NY", "WA", "CO"]:
                weight *= 1.4
                reasons.append("城市高密度公寓与高溢价浴室翻新，壁挂五金走货强劲")

    elif cur_cat_conf["tag"] == "FLOORING":
        if "Tile" in sel_pos:
            if abbr in ["FL", "TX", "AZ", "CA", "NV", "HI"]:
                weight *= 2.5
                reasons.append("大面积通铺大理石与瓷砖，金属收口防崩边极为刚需")
        elif "T-Molding" in sel_pos or "Reducer" in sel_pos:
            if abbr in ["NC", "TN", "KY", "OH", "IN", "PA", "MI", "VA"]:
                weight *= 1.7
                reasons.append("全美实木地板与LVP复合地板最大存量带，房间压条标配")
        elif "Stair" in sel_pos:
            if abbr in ["PA", "NY", "MA", "IL"]:
                weight *= 1.6
                reasons.append("多层老房住宅密集，木楼梯包角防滑踏步换新率极高")

    elif cur_cat_conf["tag"] == "DOORS":
        if "Sweep" in sel_pos or "Weatherstripping" in sel_pos:
            if abbr in ["KS", "NE", "ND", "SD", "MN", "IL", "OH", "MI", "NY", "AK"]:
                weight *= 2.2
                reasons.append("北方极寒与大平原穿堂狂风，门底防冷风倒灌是省电费第一刚需")
        elif "Hurricane" in sel_pos:
            if abbr in ["FL", "NC", "SC", "TX", "LA", "AL", "HI"]:
                weight *= 3.2
                reasons.append("大西洋与海岛飓风带 (HVHZ建筑标准) 强制必须安装抗风加固件")
        elif "Hinge" in sel_pos:
            if abbr in ["CA", "TX", "FL"]:
                weight *= 1.4
                reasons.append("新房开工与工程换门基数全美前三")

    elif cur_cat_conf["tag"] == "OUTDOOR":
        if "Trench" in sel_pos or "Channel" in sel_pos:
            if abbr in ["FL", "LA", "TX", "WA", "OR", "GA", "NC", "SC", "HI"]:
                weight *= 2.3
                reasons.append("热带强降雨、多泳池及雨林气候，车道防止内涝倒灌依赖线性深沟")
        elif "Gutter" in sel_pos:
            if abbr in ["NC", "GA", "TN", "VA", "PA", "OH", "MI", "OR", "WA"]:
                weight *= 1.9
                reasons.append("植被树冠茂密，秋季防落叶堵塞天沟大面积换装")
        elif "Post" in sel_pos:
            if abbr in ["TX", "NC", "GA", "TN", "CO"]:
                weight *= 1.6
                reasons.append("独栋后院露台(Deck)与木亭自建率全国领先")

    # ---------------- B. 材质 (Material) 影响 ----------------
    if "Stainless" in sel_mat or "Aluminum" in sel_mat or "ABS" in sel_mat:
        if abbr in ["FL", "HI", "SC", "NC", "LA", "AL"]:
            weight *= 1.25
            reasons.append("沿海高盐雾极湿环境，抗腐蚀不生锈属性带来高转化")
    elif "Steel" in sel_mat or "Cast" in sel_mat:
        if abbr in ["OH", "IN", "MI", "PA", "IL", "AK"]:
            weight *= 1.2
            reasons.append("传统重工业带与寒区偏好厚重扎实耐踩承重金属件")
    elif "Wooden" in sel_mat:
        if abbr in ["NC", "VA", "PA", "NH", "VT"]:
            weight *= 1.3
            reasons.append("高比例实木地板审美，原木嵌入式高度契合")

    # ---------------- C. 表面处理 / 颜色 (Finish) 影响 ----------------
    if sel_fin in ["BL", "Titanium"]:  # 哑光黑 / 钛黑
        if abbr in ["WA", "OR", "CA", "CO", "UT", "NC"]:
            weight *= 1.2
            reasons.append("西海岸与新兴科技都市偏好现代轻奢黑灰极简风")
    elif sel_fin in ["WH", "Silver/Matte"]:  # 白色 / 经典哑光银
        if abbr in ["FL", "TX", "AZ", "NV", "GA"]:
            weight *= 1.25
            reasons.append("阳光带白墙浅砖搭配主流，大众工程房标准款")
    elif sel_fin in ["AB", "BR", "DO", "ORB"]:  # 复古铜 / 黄铜
        if abbr in ["PA", "NY", "MA", "CT", "VA", "OH"]:
            weight *= 1.3
            reasons.append("美东历史老宅红砖硬木风格，传统复古五金溢价认可度高")

    # ---------------- D. 规格尺寸 (Size) 动销穿透 ----------------
    if sel_size in ["04X10", "36", "4x4", "39"]:  # 核心走量超级通货
        weight *= 1.15
    elif sel_size in ["02X12", "02X10", "12X12", "72", "96", "6x6"]:  # 细分/改善/大跨度规格
        if abbr in ["CA", "NY", "WA", "TX", "FL"]:
            weight *= 1.15
            reasons.append("大户型住宅或复杂户型集中，特殊规格走货顺畅")

    calc_velocity = max(int(base_velocity * weight), 35)
    calc_total_sales = calc_velocity * total_stores
    
    # 修正文案提取 Bug
    reason_str = "；".join(reasons) if reasons else f"符合【{cur_cat_conf['short_name']}】全美常规分销基线"
    
    item = dict(s)
    item["calc_velocity"] = calc_velocity
    item["calc_total_sales"] = calc_total_sales
    item["reason_desc"] = reason_str
    calculated_states.append(item)

df_res = pd.DataFrame(calculated_states)
df_res["rank_vel"] = df_res["calc_velocity"].rank(ascending=False, method="min").astype(int)
df_res["rank_total"] = df_res["calc_total_sales"].rank(ascending=False, method="min").astype(int)

# ==============================================================================
# 6. 大卡片 KPI 看板
# ==============================================================================
sum_total_units = int(df_res["calc_total_sales"].sum())
avg_vel = int(df_res["calc_velocity"].mean())
top_vel_state = df_res.sort_values(by="calc_velocity", ascending=False).iloc[0]
top_total_state = df_res.sort_values(by="calc_total_sales", ascending=False).iloc[0]

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">覆盖全美分析州数</div>
        <div class="kpi-val">{len(df_res)} 州 (含AK/HI)</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">当前组合·全美渠道总预估销量</div>
        <div class="kpi-val">{sum_total_units:,} 件</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">单店动销流速冠军 (Velocity)</div>
        <div class="kpi-val">{top_vel_state['cn']} ({top_vel_state['calc_velocity']:,} 件/店)</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">全渠道总容量榜首 (Total GMV)</div>
        <div class="kpi-val">{top_total_state['cn']} ({top_total_state['calc_total_sales']:,} 件)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 7. 排序与透视分析（提供单店流速 vs 全州总吞吐量双重视角）
# ==============================================================================
tab_table, tab_charts, tab_supply = st.tabs(["📋 全美零售动销主排行", "📊 渠道容量与流速透视图", "🚚 供应链 RDC 分仓补货决策"])

with tab_table:
    sort_mode = st.radio(
        "选择主排序指标：",
        ["单店平均流速 (件/店) - 适用于开店选品与单店平效测算", "全州渠道总吞吐量 (件) - 适用于工厂总备货与主仓分发"],
        horizontal=True
    )
    
    if "单店" in sort_mode:
        df_sorted = df_res.sort_values(by="rank_vel", ascending=True).reset_index(drop=True)
        rank_col_name = "rank_vel"
    else:
        df_sorted = df_res.sort_values(by="rank_total", ascending=True).reset_index(drop=True)
        rank_col_name = "rank_total"
        
    df_sorted["序号"] = df_sorted.index + 1
    
    col_table_view, col_detail_view = st.columns([1.1, 0.9])
    
    with col_table_view:
        view_table = df_sorted[[
            "序号", "abbr", "cn", "calc_velocity", "calc_total_sales", "thd_stores", "lowes_stores", "climate"
        ]]
        
        st.dataframe(
            view_table,
            height=580,
            use_container_width=True,
            column_config={
                "序号": st.column_config.NumberColumn(width=60),
                "abbr": st.column_config.TextColumn("州简称", width=70),
                "cn": st.column_config.TextColumn("中文全称", width=100),
                "calc_velocity": st.column_config.ProgressColumn(
                    "单店流速 (件/店)",
                    min_value=0,
                    max_value=int(df_res["calc_velocity"].max()),
                    format="%d"
                ),
                "calc_total_sales": st.column_config.NumberColumn("全州总出货量 (件)", format="%d"),
                "thd_stores": st.column_config.NumberColumn("THD", width=60),
                "lowes_stores": st.column_config.NumberColumn("Lowe's", width=70),
                "climate": st.column_config.TextColumn("气候分区", width=140)
            },
            hide_index=True
        )

    with col_detail_view:
        st.markdown("#### 🔍 选中州在当前品类与四维属性下的深度归因")
        inspect_abbr = st.selectbox("请选择要进行深度剖析的州：", df_sorted["abbr"].tolist(), index=0)
        cur = df_sorted[df_sorted["abbr"] == inspect_abbr].iloc[0]
        
        st.markdown(f"### 📌 {cur['cn']} ({cur['abbr']}) · {cur['region']}")
        
        m_c1, m_c2 = st.columns(2)
        with m_c1:
            st.metric("预估单店流速", f"{cur['calc_velocity']:,} 件/店", f"全美单店排名: #{cur['rank_vel']}")
        with m_c2:
            st.metric("该州全渠道总需求", f"{cur['calc_total_sales']:,} 件", f"全州容量排名: #{cur['rank_total']}")

        st.info(f"**💡 算法与气候地基归因**：\n{cur['reason_desc']}")
        st.write(f"**🏠 房屋基底结构**：{cur['foundation']}")
        st.write(f"**🌡️ 当地气象带**：{cur['climate']}")
        st.write(f"**🪵 地面材质偏好**：{cur['flooring_preference']}")
        st.write(f"**🏬 零售商网点**：The Home Depot: **{cur['thd_stores']}** 家 | Lowe's: **{cur['lowes_stores']}** 家 (合计: {cur['thd_stores']+cur['lowes_stores']} 家)")
        st.success(f"**✅ 当地常规主推品**：{cur['best']}")
        st.warning(f"**⚠️ 当地谨慎推展品**：{cur['avoid']}")

with tab_charts:
    st.markdown("#### 📊 全美 Top 15 动销规模与渠道结构分布")
    
    top15 = df_res.sort_values(by="calc_total_sales", ascending=False).head(15)
    chart_df = pd.DataFrame({
        "州简称": top15["abbr"],
        "THD门店销量贡献": top15["calc_velocity"] * top15["thd_stores"],
        "Lowe's门店销量贡献": top15["calc_velocity"] * top15["lowes_stores"],
    }).set_index("州简称")
    
    st.bar_chart(chart_df, height=360)
    st.caption("注：柱状图直观展示各大州在 The Home Depot 与 Lowe's 之间的渠道出货绝对总量（件），德州、加州、佛州由于门店基数超大，总出货量位列全美枢纽地位。")

with tab_supply:
    st.markdown("#### 🚚 大零售供应链 RDC 分仓与安全库存 (DOI) 决策")
    st.caption("根据美国各地理分区的物流前置期与该品类的流速表现，向供应商提供各区域配送中心（Regional Distribution Center）的库存策略。")
    
    reg_summary = df_res.groupby("region").agg({
        "abbr": "count",
        "thd_stores": "sum",
        "lowes_stores": "sum",
        "calc_total_sales": "sum",
        "calc_velocity": "mean"
    }).reset_index()
    
    reg_summary.columns = ["地理大区", "覆盖州数", "THD总店", "Lowe's总店", "该品类总需求量", "区均单店流速"]
    reg_summary["区均单店流速"] = reg_summary["区均单店流速"].astype(int)
    reg_summary["建议分仓备货比例"] = (reg_summary["该品类总需求量"] / reg_summary["该品类总需求量"].sum() * 100).round(1).astype(str) + "%"
    
    st.dataframe(reg_summary, use_container_width=True, hide_index=True)
    
    st.markdown("""
    > **采购运营策略建议 (Buyer Strategy)**：
    > 1. **美东南与美中枢纽**：针对高单店流速区域，建议维持 **45~60 天** 安全库存（DOI），主仓设在夏洛特或孟菲斯，优先锁定 Lowe's 与 THD 促销端架（Endcap）；
    > 2. **加利福尼亚与德克萨斯**：虽然单店流速被门店密度稀释，但总消耗盘子巨大，需采用高频次（每周补货）的 JIT 模式配送，防范单店缺货（Out-of-Stock）；
    > 3. **极寒区与海岛（AK/HI）**：海运补货前置期长达 7-10 天，单次起订量（MOQ）需以托盘整柜推进，规避零散补货产生的超额干线运费。
    """)

# ==============================================================================
# 8. 数据一键导出 (CSV)
# ==============================================================================
st.markdown("---")
csv_out = df_sorted[[
    "序号", "abbr", "cn", "en", "region", "calc_velocity", "calc_total_sales",
    "thd_stores", "lowes_stores", "climate", "foundation", "reason_desc", "dc_hub"
]].to_csv(index=False).encode('utf-8-sig')

st.download_button(
    label=f"📥 一键导出当前属性筛选结果报表 ({cur_cat_conf['tag']}_{sel_pos}_{sel_mat}_{sel_fin}.csv)",
    data=csv_out,
    file_name=f"Retail_Strategy_{cur_cat_conf['tag']}_{sel_pos}_{sel_mat}_{sel_size}.csv",
    mime="text/csv"
)
