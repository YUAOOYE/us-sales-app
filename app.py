import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ==============================================================================
# 1. 页面配置与还原截图的企业级风格
# ==============================================================================
st.set_page_config(
    page_title="全美零售产品全品类与气候销售决策系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-title { font-size: 1.8rem; font-weight: 700; color: #0F172A; margin-bottom: 0.2rem; }
    .sub-title { font-size: 0.9rem; color: #64748B; margin-bottom: 1rem; }
    
    /* 还原截图中的科技蓝顶部看板风格 */
    .kpi-container { display: flex; gap: 12px; margin-bottom: 18px; }
    .kpi-card {
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
        color: white;
        border-radius: 8px;
        padding: 16px 20px;
        flex: 1;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .kpi-title { font-size: 0.88rem; opacity: 0.9; margin-bottom: 4px; font-weight: 500; }
    .kpi-val { font-size: 1.8rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 北美大零售多品类全属性与气候销售决策系统</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">支持按【安装位置】、【材质】、【表面颜色代码】、【开孔尺寸】四维自由交叉筛选 | 实时联动全美各州销量流速与气候适配逻辑</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. 基础数据库定义
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
# 3. 顶部筛选器横栏（完全匹配截图选项）
# ==============================================================================
st.markdown("### 🎛️ 产品多维度属性筛选面板")

f_col1, f_col2, f_col3, f_col4 = st.columns(4)

with f_col1:
    pos_options = ["(全选)", "Floor (地面)", "Ceiling (天花板)", "Sidewall/Ceiling (侧墙/天花)", "Baseboard (踢脚线)"]
    selected_pos_raw = st.selectbox("1. 安装类型 (Position)：", pos_options, index=0)
    sel_pos = selected_pos_raw.split(" ")[0]

with f_col2:
    mat_options = ["(全选)", "Aluminum (铝合金)", "Steel (冲压钢)", "Plastic (ABS工程树脂)", "Copper (紫铜/红铜)", "Wooden (实木)"]
    selected_mat_raw = st.selectbox("2. 材质 (Material)：", mat_options, index=0)
    sel_mat = selected_mat_raw.split(" ")[0]

with f_col3:
    fin_options = [
        "(全选)",
        "BL (Matte Black 哑光黑)",
        "BN (Brushed Nickel 拉丝镍)",
        "AB (Antique Brass 仿古黄铜)",
        "DO (Dark Oil-Rubbed Bronze 深古铜黑)",
        "BR (Polished Brass 亮黄铜)",
        "WH (White 经典白)",
        "CO (Copper 亮红铜)",
        "GA (Gray/Aluminum 铝原灰)"
    ]
    selected_fin_raw = st.selectbox("3. 表面颜色代码 (Finish)：", fin_options, index=0)
    sel_fin = selected_fin_raw.split(" ")[0]

with f_col4:
    size_options = [
        "(全选)",
        "04X10 (全美大通货标杆)",
        "04X12 (大空间高顶款)",
        "02X10 (狭窄通道款)",
        "02X12 (厨房橱柜踢脚线款)",
        "02X14 (老宅修缮款)",
        "06X10 (大风量回风款)",
        "06X12 (商住两用强排量)",
        "02X02 (方形小排气)",
        "02X04 (精凑空间)",
        "03X04 (特殊定制款)"
    ]
    selected_size_raw = st.selectbox("4. 开孔尺寸规格 (Size)：", size_options, index=0)
    sel_size = selected_size_raw.split(" ")[0]

st.markdown("---")

# ==============================================================================
# 4. 核心跨维度地理气候联动计算引擎
# ==============================================================================
calculated_states = []

for s in STATES_DATA:
    abbr = s["abbr"]
    base_velocity = s["velocity"]
    total_stores = s["thd_stores"] + s["lowes_stores"]
    
    weight = 1.0
    reasons = []
    
    # 1. 位置匹配逻辑 (Position Factor)
    if sel_pos == "Floor":
        if abbr in ["NC", "TN", "KY", "IN", "OH", "MI", "WV", "IL", "PA"]:
            weight *= 1.05
            reasons.append("全地下室/架空层核心主场")
        elif abbr in ["FL", "TX", "AZ", "NV", "LA"]:
            weight *= 0.15
            reasons.append("水泥平板地基限制，地面无开孔管道")
    elif sel_pos == "Ceiling":
        if abbr in ["FL", "TX", "AZ", "NV", "CA", "GA"]:
            weight *= 2.8
            reasons.append("南方制冷刚需，出风口100%在天花板")
        elif abbr in ["MI", "ND", "MN", "WI"]:
            weight *= 0.55
            reasons.append("北方一层主力为地板送风，天花板需求有限")
    elif sel_pos == "Baseboard":
        if abbr in ["PA", "NY", "MA", "CT", "OH", "NJ"]:
            weight *= 1.7
            reasons.append("东北部老宅水暖踢脚线与橱柜底特殊开孔密集")
        else:
            weight *= 0.65
            reasons.append("现代独栋建筑较少使用踢脚线出风")
            
    # 2. 材质匹配逻辑 (Material Factor)
    if sel_mat == "Plastic":
        if abbr in ["FL", "SC", "NC", "LA", "AL", "GA"]:
            weight *= 1.3
            reasons.append("高盐雾湿热防锈痛点，ABS塑料绝不生锈")
        elif abbr in ["MN", "ND", "WY"]:
            weight *= 0.7
            reasons.append("零下30度低温严寒，塑胶抗脆裂要求严苛")
    elif sel_mat == "Aluminum":
        if abbr in ["VA", "MD", "NC", "CA", "WA", "CO"]:
            weight *= 1.25
            reasons.append("中高端中产青睐质感，耐腐蚀且轻量化")
    elif sel_mat == "Steel":
        if abbr in ["KS", "NE", "MO", "OH", "IN", "IA"]:
            weight *= 1.2
            reasons.append("内陆干燥大陆气候，讲究承重耐踩与高性价比")
        elif abbr in ["FL", "LA"]:
            weight *= 0.6
            reasons.append("沿海极高湿度，普通薄钢件极易锈蚀")
    elif sel_mat == "Wooden":
        if abbr in ["NC", "TN", "PA", "OH", "MI", "OR", "WA"]:
            weight *= 1.35
            reasons.append("高比例实木地板铺装，木质风口与地板浑然一体")
        elif abbr in ["FL", "AZ", "NV"]:
            weight *= 0.3
            reasons.append("南方以瓷砖或水泥为主，木质风口缺少匹配场景")
            
    # 3. 颜色代码匹配逻辑 (Finish Factor)
    if sel_fin == "BL":
        if abbr in ["WA", "OR", "CA", "CO", "UT", "NC"]:
            weight *= 1.25
            reasons.append("现代极简建筑与农场工业风首选用色")
    elif sel_fin in ["DO", "AB", "BR"]:
        if abbr in ["TN", "KY", "NC", "VA", "PA", "SC", "GA"]:
            weight *= 1.2
            reasons.append("传统美式古典与复古庄园风格高频消耗色")
    elif sel_fin == "WH":
        if sel_pos in ["Ceiling", "Sidewall/Ceiling"] or abbr in ["FL", "TX", "AZ"]:
            weight *= 1.3
            reasons.append("天花板与浅色墙面通用隐形配色")
            
    # 4. 尺寸匹配逻辑 (Size Factor)
    if sel_size == "04X10":
        weight *= 1.0
    elif sel_size in ["04X12", "02X12"]:
        if abbr in ["PA", "NY", "OH", "MA", "IL", "IN"]:
            weight *= 1.35
            reasons.append("老宅大开间与踢脚线翻新专属规格")
        else:
            weight *= 0.75
            
    calc_velocity = int(base_velocity * weight)
    calc_total_sales = calc_velocity * total_stores
    
    item = dict(s)
    item["calc_velocity"] = calc_velocity
    item["calc_total_sales"] = calc_total_sales
    item["reason_desc"] = "；".join(reasons) if reasons else "符合全美标准基准流速"
    calculated_states.append(item)

df_res = pd.DataFrame(calculated_states)
df_res["rank"] = df_res["calc_velocity"].rank(ascending=False, method="min").astype(int)
df_sorted = df_res.sort_values(by="rank", ascending=True).reset_index(drop=True)
df_sorted["序号"] = df_sorted.index + 1

# ==============================================================================
# 5. 还原截图样式的大卡片 KPI 看板
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
        <div class="kpi-title">当前组合·全美同期流速指数</div>
        <div class="kpi-val">{sum_velocity:,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">最高动销榜首州</div>
        <div class="kpi-val">{top_1_state['abbr']} ({top_1_state['calc_velocity']:,})</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">全美单店平均销能</div>
        <div class="kpi-val">{avg_vel:,} 件/店</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 6. 数据结果展示：排行大表与单州详情
# ==============================================================================
col_table, col_detail = st.columns(2)

with col_table:
    st.markdown("#### 📋 全美各州【同期销量/铺店数】排行状况")
    st.caption("与商超后台报表完全一致的排名表：实时随上方【位置/材质/颜色/尺寸】动态重排")
    
    view_table = df_sorted[["序号", "abbr", "cn", "calc_velocity", "thd_stores", "lowes_stores", "climate"]]
    view_table.columns = ["序号", "州简称", "中文全名", "同期销量/铺店数", "THD门店", "Lowe's门店", "气候带"]
    st.dataframe(view_table, height=520, use_container_width=True)

with col_detail:
    st.markdown("#### 🔍 选中州在当前属性组合下的深度研判")
    inspect_abbr = st.selectbox("选择要深入透视的州：", df_sorted["abbr"].tolist(), index=0)
    cur = df_sorted[df_sorted["abbr"] == inspect_abbr].iloc[0]
    
    st.markdown(f"### 📌 {cur['cn']} (`{cur['abbr']}`)")
    st.metric("该属性组合下预估单店销能", f"{cur['calc_velocity']:,} 件/店", f"全美排名: 第 {cur['序号']} 名")
    
    st.info(f"**💡 算法归因分析**：\n{cur['reason_desc']}")
    st.write(f"**🏠 房屋构造**：{cur['foundation']}")
    st.write(f"**🌡️ 当地气候**：{cur['climate']}")
    st.write(f"**🪵 地面材质偏好**：{cur['flooring_preference']}")
    st.success(f"**✅ 当地常规主推**：{cur['best']}")
    st.warning(f"**⚠️ 当地规避品类**：{cur['avoid']}")
    st.markdown(f"**🛒 零售商超渠道建议**：{cur['channel_advice']}")

# ==============================================================================
# 7. 一键下载
# ==============================================================================
st.markdown("---")
csv_out = df_sorted[["序号", "abbr", "cn", "en", "calc_velocity", "calc_total_sales", "climate", "foundation", "reason_desc"]].to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 一键导出当前属性筛选下的全美销售数据表 (.csv)",
    data=csv_out,
    file_name=f"US_Sales_Matrix_{sel_pos}_{sel_mat}_{sel_fin}_{sel_size}.csv",
    mime="text/csv"
)
