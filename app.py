import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ==============================================================================
# 1. 页面配置与还原大零售 BI 科技蓝风格
# ==============================================================================
st.set_page_config(
    page_title="全美零售全品类与气候销售决策系统",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-title { font-size: 1.85rem; font-weight: 700; color: #0F172A; margin-bottom: 0.2rem; }
    .sub-title { font-size: 0.92rem; color: #475569; margin-bottom: 1rem; }
    
    .kpi-card {
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
        color: white;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .kpi-title { font-size: 0.88rem; opacity: 0.9; margin-bottom: 4px; font-weight: 500; }
    .kpi-val { font-size: 1.8rem; font-weight: 700; }
    
    .cat-selector {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏢 北美大零售多品类全属性与气候销售决策系统</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">覆盖全品类家居建材（暖通通风、卫浴给排水、地面收口压条、门窗防风五金、庭院户外排水）| 实时四维属性交叉筛选与全美动销排名</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. 全美 48 州基础数据库
# ==============================================================================
STATES_DATA = [
  {"abbr": "NC", "en": "North Carolina", "cn": "北卡罗来纳州", "velocity": 2946, "thd_stores": 43, "lowes_stores": 112, "foundation": "架空层/地下室(75%+)", "climate": "Zone 4A/3A 混合湿润", "best": "地面出风口、地板耐磨五金", "avoid": "易锈冷轧薄铁件", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "Lowe's大本营核心州，THD门店流转极快，重度配置端架(Endcap)推广"},
  {"abbr": "TN", "en": "Tennessee", "cn": "田纳西州", "velocity": 2902, "thd_stores": 31, "lowes_stores": 62, "foundation": "木结构架空层/地下室", "climate": "Zone 4A 混合温和", "best": "重载地面风口、承重踏压件", "avoid": "天花专用下送风口", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "孟菲斯/纳什维尔物流核心区，适合设立主发货仓辐射全美"},
  {"abbr": "KY", "en": "Kentucky", "cn": "肯塔基州", "velocity": 2579, "thd_stores": 18, "lowes_stores": 44, "foundation": "全地下室占80%+", "climate": "Zone 4A 四季鲜明多雪", "best": "地下管道地面风口、复古风口", "avoid": "无调节阀空框", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "老宅翻修市场大，Pro承包商批量采购占比高"},
  {"abbr": "SC", "en": "South Carolina", "cn": "南卡罗来纳州", "velocity": 2433, "thd_stores": 28, "lowes_stores": 52, "foundation": "架空层/沿海桩基", "climate": "Zone 3A 亚热带湿热", "best": "工程ABS风口、耐盐雾构件", "avoid": "未做防锈处理普通铁件", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "沿海与内陆差异大，沿海侧重防腐耐盐雾，内陆侧重地板配件"},
  {"abbr": "WV", "en": "West Virginia", "cn": "西弗吉尼亚州", "velocity": 2248, "thd_stores": 7, "lowes_stores": 19, "foundation": "山地深地基/全地下室", "climate": "Zone 5A 湿润山地极寒", "best": "抗重压地面风口、防冻融五金", "avoid": "脆性塑料件", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "传统耐用型五金需求大，价格敏感度高于沿海，主打坚固耐用"},
  {"abbr": "ID", "en": "Idaho", "cn": "爱达荷州", "velocity": 2213, "thd_stores": 12, "lowes_stores": 14, "foundation": "深层地下室(85%+)", "climate": "Zone 5B/6B 干燥高寒", "best": "强排暖风风口、防风密封件", "avoid": "湿热除霉配件", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "新兴人口流入州，新房建设与自建房比例高，成套采购多"},
  {"abbr": "VA", "en": "Virginia", "cn": "弗吉尼亚州", "velocity": 2169, "thd_stores": 46, "lowes_stores": 68, "foundation": "地下室/架空层老房多", "climate": "Zone 4A 四季湿润冬冷", "best": "中高端装饰风口、精工硬装", "avoid": "粗糙低端工程件", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "居民消费水准高，愿意为颜值与静音/防卡鞋跟设计支付溢价"},
  {"abbr": "KS", "en": "Kansas", "cn": "堪萨斯州", "velocity": 2124, "thd_stores": 16, "lowes_stores": 18, "foundation": "100%全地下室", "climate": "Zone 4A/5A 大陆性严寒大风", "best": "大风量地面风口、耐压风门", "avoid": "轻质易吹脱件", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "农牧独栋大宅多，强调易清洗与大流通面积(Free Area)"},
  {"abbr": "DE", "en": "Delaware", "cn": "特拉华州", "velocity": 2122, "thd_stores": 6, "lowes_stores": 7, "foundation": "地下室/浅架空层", "climate": "Zone 4A 温和多潮", "best": "标准4x10尺寸风口、免税走量款", "avoid": "非标异形件", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "免税州吸引跨州批发采购，单店流转效率极高"},
  {"abbr": "AL", "en": "Alabama", "cn": "阿拉巴马州", "velocity": 2095, "thd_stores": 28, "lowes_stores": 40, "foundation": "山区架空层/平原混合", "climate": "Zone 3A 亚热带湿热", "best": "防潮ABS风口、通用通风罩", "avoid": "未保护易氧化金属", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "性价比敏感，对平价耐用型产品进店即买率高"},
  {"abbr": "IN", "en": "Indiana", "cn": "印第安纳州", "velocity": 2020, "thd_stores": 34, "lowes_stores": 47, "foundation": "全地下室占85%+", "climate": "Zone 5A 严寒多雪", "best": "地面暖风风口、防结冰构件", "avoid": "天花板专用散流器", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "工业制造业底子好，家庭DIY普及，Menards与THD竞争激烈"},
  {"abbr": "MO", "en": "Missouri", "cn": "密苏里州", "velocity": 1958, "thd_stores": 36, "lowes_stores": 42, "foundation": "传统全地下室木屋", "climate": "Zone 4A/5A 大陆季风冬冷", "best": "地面可调风口、管道连接件", "avoid": "纯热带建材", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "圣路易斯与堪萨斯城两大都市圈带动主力店动销"},
  {"abbr": "MD", "en": "Maryland", "cn": "马里兰州", "velocity": 1935, "thd_stores": 41, "lowes_stores": 31, "foundation": "老房地下室/联排镇屋", "climate": "Zone 4A 四季湿润冬寒", "best": "静音地面风口、防卡脚配件", "avoid": "粗狂工业件", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "老房升级改善多，重视审美匹配木地板色调"},
  {"abbr": "OH", "en": "Ohio", "cn": "俄亥俄州", "velocity": 1768, "thd_stores": 68, "lowes_stores": 82, "foundation": "全地下室为主", "climate": "Zone 5A 寒冷多雪长冬", "best": "冲压金属/铸铝地面风口", "avoid": "薄脆塑料", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "五金和建材传统大州，老旧翻新为第一大驱动力"},
  {"abbr": "UT", "en": "Utah", "cn": "犹他州", "velocity": 1666, "thd_stores": 22, "lowes_stores": 12, "foundation": "全地下室大户型", "climate": "Zone 5B/6B 高山干燥极寒", "best": "抗干裂ABS风口、密封防风件", "avoid": "湿热除湿件", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "家庭人口多，儿童活动多，需重点突出防卡脚防异物设计"},
  {"abbr": "NE", "en": "Nebraska", "cn": "内布拉斯加州", "velocity": 1601, "thd_stores": 11, "lowes_stores": 9, "foundation": "全地下室独立屋", "climate": "Zone 5A 极寒多暴风雪", "best": "大承重地面风口、加厚五金", "avoid": "精细易损件", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "注重产品实用寿命与抗踩踏能力，耐用性口碑最关键"},
  {"abbr": "CO", "en": "Colorado", "cn": "科罗拉多州", "velocity": 1582, "thd_stores": 44, "lowes_stores": 30, "foundation": "防冻全地下室", "climate": "Zone 5B/6B 高海拔强积雪", "best": "高气密保温风口、实木嵌入风口", "avoid": "漏风劣质件", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "注重节能与绿色建材标准，对品质工艺认可度高"},
  {"abbr": "OK", "en": "Oklahoma", "cn": "俄克拉荷马州", "velocity": 1543, "thd_stores": 17, "lowes_stores": 26, "foundation": "架空层与平板各半", "climate": "Zone 3A/4A 极端温差风大", "best": "防风压配件、加固五金", "avoid": "非标冷门尺寸", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "春季极端天气修缮需求爆发，季节性补货规律明显"},
  {"abbr": "AR", "en": "Arkansas", "cn": "阿肯色州", "velocity": 1514, "thd_stores": 14, "lowes_stores": 27, "foundation": "林区架空层木屋多", "climate": "Zone 3A/4A 湿润森林温和", "best": "防潮耐水ABS风口、平价金属件", "avoid": "高价奢侈品", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "性价比为主导，大众款标准化 4x10 尺寸走货最快"},
  {"abbr": "OR", "en": "Oregon", "cn": "俄勒冈州", "velocity": 1476, "thd_stores": 26, "lowes_stores": 15, "foundation": "架空层木结构(Crawl)", "climate": "Zone 4C 海洋湿冷多雨", "best": "耐水防霉ABS风口、不锈钢配件", "avoid": "易锈生铁件", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "对环保环保标准(如无味ABS)要求严格，绿色理念受欢迎"},
  {"abbr": "MT", "en": "Montana", "cn": "蒙大拿州", "velocity": 1436, "thd_stores": 7, "lowes_stores": 5, "foundation": "深埋防冻全地下室", "climate": "Zone 6B 严寒多雪", "best": "超耐寒金属件、坚固大格栅", "avoid": "低温脆化塑料", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "单店覆盖半径几百里，顾客单次采购量大，注重坚固"},
  {"abbr": "MI", "en": "Michigan", "cn": "密歇根州", "velocity": 1378, "thd_stores": 70, "lowes_stores": 43, "foundation": "100%全地下室", "climate": "Zone 5A/6A 大湖雪带漫长冬", "best": "经典地面金属风口、防化雪盐件", "avoid": "天花专用风口", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "底特律周边老屋改造基数庞大，换新频次极高"},
  {"abbr": "GA", "en": "Georgia", "cn": "乔治亚州", "velocity": 1346, "thd_stores": 89, "lowes_stores": 63, "foundation": "北架空层/南平板地基", "climate": "Zone 3A 亚热带长夏湿热", "best": "天花与地面品类分推、防腐五金", "avoid": "全推纯地面件", "size_breakdown": "地面与天花混合: 4x10 (40%), 6x6/8x8散流器 (40%), 14x6回风 (20%)", "flooring_preference": "LVP/复合地板 40%, 瓷砖 35%, 地毯 25%", "channel_advice": "The Home Depot 全球总部所在地，标杆渠道必须深耕"},
  {"abbr": "WA", "en": "Washington", "cn": "华盛顿州", "velocity": 1340, "thd_stores": 43, "lowes_stores": 37, "foundation": "架空层与现代住宅", "climate": "Zone 4C 阴湿多雾", "best": "极简线形风口、环保无味ABS件", "avoid": "过时粗糙件", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "西雅图高科技中产多，偏好极简现代现代黑白灰色系"},
  {"abbr": "IL", "en": "Illinois", "cn": "伊利诺伊州", "velocity": 1257, "thd_stores": 82, "lowes_stores": 38, "foundation": "全地下室占多数", "climate": "Zone 5A 大陆性严寒冬风大", "best": "标准地面出风口、重型五金", "avoid": "薄型无卡槽风口", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "大芝加哥门店极为密集，虽单店被微稀释但全州总盘极大"},
  {"abbr": "PA", "en": "Pennsylvania", "cn": "宾夕法尼亚州", "velocity": 1197, "thd_stores": 69, "lowes_stores": 84, "foundation": "老房地下室比例高", "climate": "Zone 5A/6A 寒冷多雪老区", "best": "古典复古雕花风口、金属件", "avoid": "现代过于极简款", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "注重传统复古美学，旧房木地板配金属风口是绝对主流"},
  {"abbr": "SD", "en": "South Dakota", "cn": "南达科他州", "velocity": 1183, "thd_stores": 4, "lowes_stores": 3, "foundation": "防冻深层地下室", "climate": "Zone 5B/6B 严寒干燥多风", "best": "耐低温防裂金属风口", "avoid": "易碎薄塑料", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "门店数量少，单店客流稳定，实用主义第一"},
  {"abbr": "IA", "en": "Iowa", "cn": "爱荷华州", "velocity": 1100, "thd_stores": 18, "lowes_stores": 17, "foundation": "几乎全地下室", "climate": "Zone 5A 寒冷长冬大雪", "best": "高性价比金属与ABS风口", "avoid": "昂贵概念品", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "Menards与THD渗透深，性价比走量款需求长盛不衰"},
  {"abbr": "NJ", "en": "New Jersey", "cn": "新泽西州", "velocity": 1007, "thd_stores": 64, "lowes_stores": 41, "foundation": "紧凑型地下室多", "climate": "Zone 4A/5A 海洋微寒密集居住", "best": "小巧精致风口、美观五金", "avoid": "粗狂工业件", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "密度极高、通勤家庭翻修预算高，看重精致与易安装"},
  {"abbr": "NY", "en": "New York", "cn": "纽约州", "velocity": 863, "thd_stores": 102, "lowes_stores": 68, "foundation": "市区公寓无风管/郊区独栋地下室", "climate": "Zone 5A/6A 湿冷上州大雪", "best": "郊区独栋地面件、复古暖气罩", "avoid": "对市区公寓推地板风管件", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "纽约市区与上州完全割裂，需按店分发，市区店少铺地面件"},
  {"abbr": "WY", "en": "Wyoming", "cn": "怀俄明州", "velocity": 846, "thd_stores": 4, "lowes_stores": 2, "foundation": "全地下室人口稀少", "climate": "Zone 6B/7 极寒干燥大风", "best": "超耐寒重型五金", "avoid": "轻质薄件", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "全州人口不足60万，总体量受限，常规按需补货即可"},
  {"abbr": "MA", "en": "Massachusetts", "cn": "马萨诸塞州", "velocity": 846, "thd_stores": 46, "lowes_stores": 26, "foundation": "水暖暖气片(Radiator)多", "climate": "Zone 5A 寒冷多雪近海湿冷", "best": "踢脚线出风口、复古铸铁风口", "avoid": "强排风管专属塑料件", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "老房很多不是强排风管系统，需查验当地供暖结构"},
  {"abbr": "NM", "en": "New Mexico", "cn": "新墨西哥州", "velocity": 823, "thd_stores": 13, "lowes_stores": 14, "foundation": "水泥平板地基(Slab)为主", "climate": "Zone 4B/5B 沙漠干旱多风沙", "best": "防尘百叶、耐晒高温五金", "avoid": "地面下沉式出风口", "size_breakdown": "天花板主推: 6x6, 8x8, 10x10, 12x12 散流器; 侧墙回风: 14x6, 20x20, 24x12", "flooring_preference": "瓷砖 (Tile) 50%, 水泥抛光/强化复合 30%, 地毯 20%", "channel_advice": "天花板或高墙侧送风为主，主打防风沙密封性能"},
  {"abbr": "MN", "en": "Minnesota", "cn": "明尼苏达州", "velocity": 771, "thd_stores": 33, "lowes_stores": 13, "foundation": "深层地下室但水暖多", "climate": "Zone 6A/7 极寒雪原", "best": "重型防冷凝风口、耐寒五金", "avoid": "易脆塑料", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "虽然冷，但因门店密集且水暖分散了部分风管需求，店均平缓"},
  {"abbr": "NH", "en": "New Hampshire", "cn": "新罕布什尔州", "velocity": 756, "thd_stores": 19, "lowes_stores": 12, "foundation": "石基与木屋", "climate": "Zone 5A/6A 林区寒冷", "best": "实木配风口、自然金属件", "avoid": "廉价塑料件", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "当地人动手能力强，偏好木质与金属自然质感"},
  {"abbr": "MS", "en": "Mississippi", "cn": "密西西比州", "velocity": 737, "thd_stores": 16, "lowes_stores": 24, "foundation": "平板地基与浅架空", "climate": "Zone 3A 闷热高湿无冬", "best": "高抗湿防生锈件、天花排风罩", "avoid": "高端奢侈品", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "人均收入偏低，走量款与极低客单价产品更易动销"},
  {"abbr": "VT", "en": "Vermont", "cn": "佛蒙特州", "velocity": 717, "thd_stores": 4, "lowes_stores": 2, "foundation": "全地下室山地木屋", "climate": "Zone 6A 寒冬多雪", "best": "环保无味风口、铸铝盖板", "avoid": "劣质塑料感产品", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "环保法令严，重视产品材质安全与耐久"},
  {"abbr": "ND", "en": "North Dakota", "cn": "北达科他州", "velocity": 671, "thd_stores": 4, "lowes_stores": 3, "foundation": "防冻深层地下室", "climate": "Zone 6A/7 极寒半年冰封", "best": "结实金属风口、保温构件", "avoid": "脆性塑料", "size_breakdown": "标准通用型: 4x10 (70%), 4x12 (15%), 2x12 (10%), 6x12 (5%)", "flooring_preference": "LVP/复合地板 40%, 实木 30%, 瓷砖 20%, 地毯 10%", "channel_advice": "人口仅70余万，大型商超网点少，单店绝对销售有限"},
  {"abbr": "CT", "en": "Connecticut", "cn": "康涅狄格州", "velocity": 658, "thd_stores": 30, "lowes_stores": 14, "foundation": "老房地下室但定制工程多", "climate": "Zone 5A 海洋微寒多雪", "best": "高档定制级拉丝金属风口", "avoid": "低档大众通用塑料", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "DIY比例略低于中西部，Pro工程定制渠道占比较高"},
  {"abbr": "ME", "en": "Maine", "cn": "缅因州", "velocity": 634, "thd_stores": 11, "lowes_stores": 8, "foundation": "传统地下室与岩基", "climate": "Zone 6A 沿海湿冷多雾", "best": "防潮耐盐雾金属件", "avoid": "不耐湿五金", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "远离干线物流，运费成本较高，主推高客单长寿命品"},
  {"abbr": "RI", "en": "Rhode Island", "cn": "罗德岛州", "velocity": 532, "thd_stores": 7, "lowes_stores": 4, "foundation": "老房紧凑型", "climate": "Zone 5A 海洋微寒", "best": "常规标准修缮件", "avoid": "异形大件", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "全州仅几家大零售商超，整体容量小"},
  {"abbr": "LA", "en": "Louisiana", "cn": "路易斯安那州", "velocity": 495, "thd_stores": 27, "lowes_stores": 31, "foundation": "防洪高架柱/水泥平板", "climate": "Zone 2A/3A 极端湿热易涝", "best": "天花排风口、高耐蚀铝合金防锈件", "avoid": "地面下沉式出风口", "size_breakdown": "天花板主推: 6x6, 8x8, 10x10, 12x12 散流器; 侧墙回风: 14x6, 20x20, 24x12", "flooring_preference": "瓷砖 (Tile) 50%, 水泥抛光/强化复合 30%, 地毯 20%", "channel_advice": "绝不能铺地板风口；主推天花格栅和耐腐蚀户外建材"},
  {"abbr": "NV", "en": "Nevada", "cn": "内华达州", "velocity": 460, "thd_stores": 19, "lowes_stores": 14, "foundation": "100%混凝土平板(Slab)", "climate": "Zone 3B 极端干旱酷热沙漠", "best": "天花板可调风口、抗紫外线塑料件", "avoid": "地面出风口", "size_breakdown": "天花板主推: 6x6, 8x8, 10x10, 12x12 散流器; 侧墙回风: 14x6, 20x20, 24x12", "flooring_preference": "瓷砖 (Tile) 50%, 水泥抛光/强化复合 30%, 地毯 20%", "channel_advice": "拉斯维加斯新城全为空调天花板下送风，按顶装逻辑选品"},
  {"abbr": "WI", "en": "Wisconsin", "cn": "威斯康星州", "velocity": 456, "thd_stores": 28, "lowes_stores": 13, "foundation": "全地下室普及", "climate": "Zone 5A/6A 漫长严寒多雪", "best": "重型金属地板出风口、防冻五金", "avoid": "天花专用风口", "size_breakdown": "地面绝对主力: 4x10 (65%); 换新大尺寸: 4x12 (20%); 踢脚线/狭窄区: 2x12 (10%); 回风: 6x10 (5%)", "flooring_preference": "实木 (Hardwood) 45%, 锁扣胶板 (LVP) 35%, 瓷砖 10%, 地毯 10%", "channel_advice": "地处Menards核心发源腹地，本地本土品牌极强，需打价格差异化"},
  {"abbr": "TX", "en": "Texas", "cn": "德克萨斯州", "velocity": 332, "thd_stores": 180, "lowes_stores": 142, "foundation": "80%+混凝土平板地基(Slab)", "climate": "Zone 2A/3A/3B 漫长干热湿热", "best": "天花散流器、回风滤网格栅", "avoid": "地面下沉式出风口", "size_breakdown": "天花板主推: 6x6, 8x8, 10x10, 12x12 散流器; 侧墙回风: 14x6, 20x20, 24x12", "flooring_preference": "瓷砖 (Tile) 50%, 水泥抛光/强化复合 30%, 地毯 20%", "channel_advice": "全美第二大州，总盘大但单店被极度稀释，品类必须切到天花与墙面"},
  {"abbr": "AZ", "en": "Arizona", "cn": "亚利桑那州", "velocity": 289, "thd_stores": 58, "lowes_stores": 33, "foundation": "绝大多数为混凝土平板", "climate": "Zone 2B 纯沙漠干热长酷暑", "best": "天花板空调扩散器、遮阳建材", "avoid": "地面风口", "size_breakdown": "天花板主推: 6x6, 8x8, 10x10, 12x12 散流器; 侧墙回风: 14x6, 20x20, 24x12", "flooring_preference": "瓷砖 (Tile) 50%, 水泥抛光/强化复合 30%, 地毯 20%", "channel_advice": "凤凰城等大区全面以顶装风口为主，强光紫外线耐受是测试红线"},
  {"abbr": "CA", "en": "California", "cn": "加利福尼亚州", "velocity": 253, "thd_stores": 232, "lowes_stores": 113, "foundation": "南加全平板/网点全美最密", "climate": "Zone 3B/4B 干燥温和干热", "best": "Title 24环保合规风口、天花格栅", "avoid": "传统重工业高铅风口", "size_breakdown": "天花板主推: 6x6, 8x8, 10x10, 12x12 散流器; 侧墙回风: 14x6, 20x20, 24x12", "flooring_preference": "瓷砖 (Tile) 50%, 水泥抛光/强化复合 30%, 地毯 20%", "channel_advice": "全美最大单一经济体，但门店极密摊薄单店，且加州法规(Prop 65)门槛高"},
  {"abbr": "FL", "en": "Florida", "cn": "佛罗里达州", "velocity": 234, "thd_stores": 154, "lowes_stores": 128, "foundation": "95%+混凝土平板地基(Slab)", "climate": "Zone 1A/2A 极湿热高盐雾飓风", "best": "天花出风口、防腐铝/ABS配件", "avoid": "地面出风口", "size_breakdown": "天花板主推: 6x6, 8x8, 10x10, 12x12 散流器; 侧墙回风: 14x6, 20x20, 24x12", "flooring_preference": "瓷砖 (Tile) 50%, 水泥抛光/强化复合 30%, 地毯 20%", "channel_advice": "纯制冷市场，严禁把地面风口发往佛州；全面转战天花板出风与防腐五金"}
]

# ==============================================================================
# 3. 第一层级：顶级产品大类选择 (Product Category)
# ==============================================================================
CATEGORY_CONFIG = {
    "1. 暖通通风与空气分配 (HVAC & Ventilation)": {
        "tag": "HVAC",
        "intro": "包括地面出风口、天花散流器、回风百叶格栅、踢脚线风口及管道连接件。核心动销受【地基形态（地下室vs平板）】和【冷热对流】决定。",
        "positions": ["(全选)", "Floor (地面)", "Ceiling (天花板)", "Sidewall/Ceiling (侧墙/天花通用)", "Baseboard (踢脚线)"],
        "materials": ["(全选)", "Aluminum (铝合金)", "Steel (冲压钢)", "Plastic (ABS工程树脂)", "Copper (紫铜/红铜)", "Wooden (实木)"],
        "finishes": ["(全选)", "BL (Matte Black 哑光黑)", "BN (Brushed Nickel 拉丝镍)", "WH (White 经典白)", "DO (Dark Bronze 深古铜)", "AB (Antique Brass 仿古黄铜)", "BR (Brass 亮黄铜)", "GA (Gray 铝原灰)"],
        "sizes": ["(全选)", "04X10", "04X12", "02X10", "02X12", "02X14", "06X10", "06X12", "08X08", "12X12"]
    },
    "2. 卫浴五金与地漏给排水 (Plumbing & Bath Hardware)": {
        "tag": "PLUMBING",
        "intro": "包括不锈钢淋浴地漏、长条线性隐形地漏、防臭下水器、防冻水阀、水槽与花洒五金配件。受【水质硬度、盐雾湿度、冻裂风险】决定。",
        "positions": ["(全选)", "Floor Drain (地面地漏/排水口)", "Linear Drain (长条隐形线性地漏)", "Wall Mount (墙面挂件/淋浴五金)", "Frost-Proof Valve (室外防冻阀/管道构件)"],
        "materials": ["(全选)", "Stainless Steel 304 (304不锈钢)", "Solid Brass (精铸黄铜)", "ABS/PVC (耐腐工程塑料)", "Zinc Alloy (锌合金)"],
        "finishes": ["(全选)", "BN (Brushed Nickel 拉丝镍)", "MB (Matte Black 哑光黑)", "CP (Chrome 抛光亮铬)", "BG (Brushed Gold 拉丝金)", "ORB (Oil Rubbed Bronze 古铜)"],
        "sizes": ["(全选)", "4x4 inch (标准方形地漏)", "6x6 inch (大排量地漏)", "24-36 inch (长条形隐形地漏)", "1/2 inch (常规进水接口)", "3/4 inch (主水管接口)"]
    },
    "3. 地面收口压条与瓷砖金属辅料 (Flooring & Tile Trim)": {
        "tag": "FLOORING",
        "intro": "包括实木/复合地板T型压条、高低过渡扣条、瓷砖防撞金属收边条、楼梯防滑包角。受【实木地板普及率 vs 瓷砖大板偏好】决定。",
        "positions": ["(全选)", "T-Molding (同高地面平接T型条)", "Reducer (高低不平地面缓坡减速条)", "Tile Edge Trim (瓷砖L型防撞收边条)", "Stair Nosing (楼梯防滑包角踏步条)"],
        "materials": ["(全选)", "Anodized Aluminum (阳极氧化铝合金)", "Stainless Steel (高硬度不锈钢)", "Solid Hardwood (橡木/原木)", "Flexible PVC (高弹收边条)"],
        "finishes": ["(全选)", "Silver/Matte (哑光拉丝银)", "Titanium Black (钛黑/哑光黑)", "Champagne (香槟金)", "Dark Bronze (仿古深铜)", "Wood Grain (仿真木纹)"],
        "sizes": ["(全选)", "36 inch (单开门标准宽)", "72 inch (双扇门大跨度)", "96 inch (工程长条)", "8mm-10mm (常规瓷砖收口)", "12mm-15mm (大理石/厚砖收口)"]
    },
    "4. 门窗五金与密封防风防暴 (Doors, Windows & Hardware)": {
        "tag": "DOORS",
        "intro": "包括门底防冷风条、门窗阻风隔音硅胶条、防飓风加固角码、重型入户门合页、推拉导轨。受【冬季寒风气密性 vs 沿海飓风防风暴标准】决定。",
        "positions": ["(全选)", "Door Bottom Sweep (门底防风挡水刷/密封条)", "Weatherstripping (门框/窗框V型隔热密封条)", "Heavy Hinge (重型轴承门合页)", "Hurricane Tie (建筑防飓风抗风压连接件)"],
        "materials": ["(全选)", "Aluminum + Silicone (铝合金托底+耐候硅胶)", "Heavy Duty Steel (加厚冷轧钢)", "Solid Brass (重型纯铜)", "Stainless Steel (防锈不锈钢)"],
        "finishes": ["(全选)", "BL (Matte Black 哑光黑)", "Satin Nickel (缎面拉丝银)", "White (门框经典白)", "Zinc Galvanized (工业镀锌银)"],
        "sizes": ["(全选)", "36 inch (标准单门底条)", "42 inch (大入户门底条)", "3.5x3.5 inch (轻型室内合页)", "4x4 inch (重载大门合页)", "50 ft Roll (50英尺整卷密封条)"]
    },
    "5. 户外庭院、排水沟与结构件 (Outdoor Drainage & Patio)": {
        "tag": "OUTDOOR",
        "intro": "包括室外车道/泳池周边排水沟、排水沟盖板、屋檐落水管防落叶过滤网、凉亭立柱防腐底座。受【暴雨洪水降雨量、融雪负荷与强紫外线】决定。",
        "positions": ["(全选)", "Trench/Channel Drain (车道/泳池线性排水沟与格栅)", "Gutter Guard (屋檐排水天沟防叶滤网)", "Post Anchor Base (木亭地台立柱固定底座)", "Outdoor Wall Vent (室外防风雨冲压百叶)"],
        "materials": ["(全选)", "Hot-Dip Galvanized (热浸镀锌重钢)", "Polymer/HDPE (耐暴晒耐候塑料)", "Ductile Cast Iron (重载球墨铸铁)", "Cast Aluminum (耐候防腐铸铝)"],
        "finishes": ["(全选)", "Galvanized Silver (热镀锌防腐银)", "Black Asphalt (沥青防腐黑漆)", "Natural Cement Gray (水泥灰)"],
        "sizes": ["(全选)", "39 inch / 1 Meter (1米标准排水沟单元)", "4x4 inch (木方柱底座)", "6x6 inch (重型大立柱底座)", "5-6 inch (全美标准屋檐排水天沟网)"]
    }
}

st.markdown('<div class="cat-selector">', unsafe_allow_html=True)
c_sel, c_desc = st.columns(2)
with c_sel:
    chosen_cat_name = st.selectbox(
        "📂 请选择您的核心产品品类：",
        list(CATEGORY_CONFIG.keys()),
        index=0
    )
cur_cat_conf = CATEGORY_CONFIG[chosen_cat_name]
with c_desc:
    st.markdown(f"**品类应用画像**：{cur_cat_conf['intro']}")
st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4. 第二层级：与当前品类动态绑定的四大属性筛选栏 (完全匹配截图体验)
# ==============================================================================
f_col1, f_col2, f_col3, f_col4 = st.columns(4)

with f_col1:
    selected_pos_raw = st.selectbox("1. 安装类型 (Position)：", cur_cat_conf["positions"], index=0)
    sel_pos = selected_pos_raw.split(" ")[0]

with f_col2:
    selected_mat_raw = st.selectbox("2. 材质 (Material)：", cur_cat_conf["materials"], index=0)
    sel_mat = selected_mat_raw.split(" ")[0]

with f_col3:
    selected_fin_raw = st.selectbox("3. 表面颜色代码 (Finish)：", cur_cat_conf["finishes"], index=0)
    sel_fin = selected_fin_raw.split(" ")[0]

with f_col4:
    selected_size_raw = st.selectbox("4. 规格尺寸 (Size)：", cur_cat_conf["sizes"], index=0)
    sel_size = selected_size_raw.split(" ")[0]

st.markdown("---")

# ==============================================================================
# 5. 多品类全美动销流速计算引擎
# ==============================================================================
calculated_states = []

for s in STATES_DATA:
    abbr = s["abbr"]
    base_velocity = s["velocity"]
    total_stores = s["thd_stores"] + s["lowes_stores"]
    
    weight = 1.0
    reasons = []
    
    # ---------------- 场景 1: 暖通系统 ----------------
    if cur_cat_conf["tag"] == "HVAC":
        if sel_pos == "Floor":
            if abbr in ["NC", "TN", "KY", "IN", "OH", "MI", "WV", "IL", "PA"]:
                weight *= 1.05
                reasons.append("全地下室/架空层核心主场，热风对流刚需")
            elif abbr in ["FL", "TX", "AZ", "NV", "LA"]:
                weight *= 0.15
                reasons.append("水泥平板地基限制，地面无开孔风管")
        elif sel_pos == "Ceiling":
            if abbr in ["FL", "TX", "AZ", "NV", "CA", "GA"]:
                weight *= 2.8
                reasons.append("南方强空调制冷区，出风口全部在天花板")
            elif abbr in ["MI", "ND", "MN", "WI"]:
                weight *= 0.55
                reasons.append("北方一层主力为地面送风")
        elif sel_pos == "Baseboard":
            if abbr in ["PA", "NY", "MA", "CT", "OH", "NJ"]:
                weight *= 1.7
                reasons.append("东北部老宅水暖踢脚线与橱柜底特殊开孔密集")

    # ---------------- 场景 2: 卫浴五金与给排水 ----------------
    elif cur_cat_conf["tag"] == "PLUMBING":
        if sel_pos in ["Linear Drain", "Floor Drain"]:
            if abbr in ["FL", "CA", "TX", "NC", "SC", "GA", "AZ"]:
                weight *= 1.8
                reasons.append("南部与西海岸瓷砖无门槛淋浴房(Curbless Shower)翻新量全美最大")
        elif sel_pos == "Frost-Proof Valve":
            if abbr in ["MN", "WI", "MI", "ND", "SD", "IL", "OH"]:
                weight *= 2.5
                reasons.append("冬季深层冻结，室外水龙头与水管防冻裂是硬性防险标准")
            elif abbr in ["FL", "TX", "AZ"]:
                weight *= 0.1
                reasons.append("南部无严重冻土冰封期，防冻阀几乎无需求")
        if "Stainless" in sel_mat or "ABS" in sel_mat:
            if abbr in ["FL", "SC", "NC", "LA", "AL"]:
                weight *= 1.3
                reasons.append("沿海极高湿度与盐雾，抗腐蚀不生锈优势压倒性")

    # ---------------- 场景 3: 地面收口与瓷砖辅料 ----------------
    elif cur_cat_conf["tag"] == "FLOORING":
        if "Tile" in sel_pos:
            if abbr in ["FL", "TX", "AZ", "CA", "NV"]:
                weight *= 2.4
                reasons.append("全美瓷砖大板铺设比例最高区域，防撞收边条极高频走货")
        elif "T-Molding" in sel_pos or "Reducer" in sel_pos:
            if abbr in ["NC", "TN", "KY", "OH", "IN", "PA", "MI"]:
                weight *= 1.6
                reasons.append("全美实木与LVP复合木地板主力大本营，房间交界压条标配")

    # ---------------- 场景 4: 门窗五金与防风密封 ----------------
    elif cur_cat_conf["tag"] == "DOORS":
        if "Sweep" in sel_pos or "Weatherstripping" in sel_pos:
            if abbr in ["KS", "NE", "ND", "SD", "MN", "IL", "OH", "MI", "NY"]:
                weight *= 2.0
                reasons.append("北方极寒与大平原狂风，门底防冷风漏风是家庭节能降电费刚需")
        elif "Hurricane" in sel_pos:
            if abbr in ["FL", "NC", "SC", "TX", "LA", "AL"]:
                weight *= 3.0
                reasons.append("沿海飓风防暴风法规 (HVHZ Code) 强制要求加固件")

    # ---------------- 场景 5: 户外庭院与排水 ----------------
    elif cur_cat_conf["tag"] == "OUTDOOR":
        if "Trench" in sel_pos or "Channel" in sel_pos:
            if abbr in ["FL", "LA", "TX", "WA", "OR", "GA", "NC", "SC"]:
                weight *= 2.2
                reasons.append("高降雨量与泳池庭院普及，车道防内涝线性排水需求巨大")
        elif "Gutter" in sel_pos:
            if abbr in ["NC", "GA", "TN", "VA", "PA", "OH", "MI"]:
                weight *= 1.8
                reasons.append("森林落叶树木茂密，秋季防堵网大面积换新")

    if sel_mat == "Plastic" and abbr in ["FL", "SC", "NC", "LA"]:
        weight *= 1.15
    if sel_fin == "BL" and abbr in ["WA", "OR", "CA", "CO", "UT", "NC"]:
        weight *= 1.15
        
    calc_velocity = max(int(base_velocity * weight), 50)
    calc_total_sales = calc_velocity * total_stores
    
    item = dict(s)
    item["calc_velocity"] = calc_velocity
    item["calc_total_sales"] = calc_total_sales
    item["reason_desc"] = "；".join(reasons) if reasons else f"符合【{chosen_cat_name.split(' ')}】全美常规流速"
    calculated_states.append(item)

df_res = pd.DataFrame(calculated_states)
df_res["rank"] = df_res["calc_velocity"].rank(ascending=False, method="min").astype(int)
df_sorted = df_res.sort_values(by="rank", ascending=True).reset_index(drop=True)
df_sorted["序号"] = df_sorted.index + 1

# ==============================================================================
# 6. 大卡片 KPI 看板 (完全还原截图样式)
# ==============================================================================
sum_velocity = int(df_sorted["calc_velocity"].sum())
top_1_state = df_sorted.iloc[0]
avg_vel = int(df_sorted["calc_velocity"].mean())

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">总铺店州数</div>
        <div class="kpi-val">48</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">当前品类属性·同期销量流速总值</div>
        <div class="kpi-val">{sum_velocity:,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">该品类全国榜首州</div>
        <div class="kpi-val">{top_1_state['abbr']} ({top_1_state['calc_velocity']:,})</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">单店平均出货能力</div>
        <div class="kpi-val">{avg_vel:,} 件/店</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 7. 排行状况大表与深度下钻透视 (完全还原截图列表)
# ==============================================================================
col_table, col_detail = st.columns(2)

with col_table:
    st.markdown("#### 📋 全美各州【同期销量/铺店数】排行状况")
    st.caption("与截图一致的零售报表：根据上方所选【品类+四维属性】实时全美重排")
    
    view_table = df_sorted[["序号", "abbr", "cn", "calc_velocity", "thd_stores", "lowes_stores", "climate"]]
    view_table.columns = ["序号", "州简称", "中文全名", "同期销量/铺店数", "THD门店", "Lowe's门店", "气候带"]
    st.dataframe(view_table, height=540, use_container_width=True)

with col_detail:
    st.markdown("#### 🔍 选中州在当前品类与属性下的深度归因")
    inspect_abbr = st.selectbox("选择要透视的州：", df_sorted["abbr"].tolist(), index=0)
    cur = df_sorted[df_sorted["abbr"] == inspect_abbr].iloc[0]
    
    st.markdown(f"### 📌 {cur['cn']} (`{cur['abbr']}`)")
    st.metric("该品类组合下单店预估流速", f"{cur['calc_velocity']:,} 件/店", f"全美排名: 第 {cur['序号']} 名")
    
    st.info(f"**💡 算法与气候归因**：\n{cur['reason_desc']}")
    st.write(f"**🏠 房屋结构基底**：{cur['foundation']}")
    st.write(f"**🌡️ 当地气象气候**：{cur['climate']}")
    st.write(f"**🪵 地面材质偏好**：{cur['flooring_preference']}")
    st.success(f"**✅ 当地常规主推**：{cur['best']}")
    st.warning(f"**⚠️ 当地规避品类**：{cur['avoid']}")

# ==============================================================================
# 8. 数据一键导出
# ==============================================================================
st.markdown("---")
csv_out = df_sorted[["序号", "abbr", "cn", "en", "calc_velocity", "calc_total_sales", "climate", "foundation", "reason_desc"]].to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 一键导出当前品类属性筛选结果 (.csv)",
    data=csv_out,
    file_name=f"US_Sales_{cur_cat_conf['tag']}_{sel_pos}_{sel_mat}_{sel_fin}.csv",
    mime="text/csv"
)
