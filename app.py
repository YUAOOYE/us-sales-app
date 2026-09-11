import streamlit as st
import pandas as pd
import json
import os
import io
from datetime import datetime

# ==============================================================================
# 1. 页面配置与美观样式
# ==============================================================================
st.set_page_config(
    page_title="全美大零售官方售卖点与气候销售决策系统 (Pro 增强版)",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 2.1rem; font-weight: 700; color: #0F172A; margin-bottom: 0.2rem; }
    .sub-header { font-size: 0.95rem; color: #475569; margin-bottom: 1.2rem; }
    .season-box { background: linear-gradient(135deg, #FFFBEB, #FEF3C7); border: 1px solid #FCD34D; border-radius: 8px; padding: 14px; margin-bottom: 15px; }
    .card-t1 { border-left: 5px solid #2563EB; background-color: #F8FAFC; padding: 16px; border-radius: 6px; margin-bottom: 12px; }
    .card-t5 { border-left: 5px solid #EF4444; background-color: #FEF2F2; padding: 16px; border-radius: 6px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏬 全美大零售官方售卖点与气候销售决策系统</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">动态联动 The Home Depot & Lowe\'s 官方售卖点 | 实时在售表上传解析 | 季节供暖时钟与海运备货窗口 | 开孔规格与地材矩阵</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. 全美 48 州权威基准数据库 (含官方售卖点与规格偏好)
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
# 3. 季节性补货时钟与海运周期模块 (Seasonality & Supply Chain Lead Time)
# ==============================================================================
now = datetime.now()
curr_month = now.month

season_months = {
    1: ("❄️ 1月·深冬高寒期", "北方极寒消耗高峰，以现货快速补仓为主；各大商超正对春季 (Spring Reset) 庭院与家装进行最终确认。"),
    2: ("❄️ 2月·供暖尾期与春季下单月", "商超开始下发春季家装首批大单；需抓紧锁定天花板散流器、户外建材与防潮卫浴生产排期。"),
    3: ("🌱 3月·春季翻新启动月", "南方制冷与全美地板更换全面启动；海运直发美西/美东中心仓，准备迎接复活节促销。"),
    4: ("🌱 4月·全美春季家装大爆发", "春季大促核心月，地板与墙面旧改高峰；北方开始转暖，南方进入强空调负荷期。"),
    5: ("☀️ 5月·初夏销售旺季", "阵亡将士纪念日促销期；防紫外线户外建材、耐高温塑料配件与防潮卫浴动销走高。"),
    6: ("☀️ 6月·盛夏制冷与除湿峰值", "深南阳光带(FL/TX/AZ)空调制冷满负荷运转；耐盐雾、天花板出风与大滤网回风高频补货。"),
    7: ("☀️ 7月·秋冬季暖通提报月", "各大商超采购经理（Merchant）开始锁定秋冬供暖（Fall/Winter Set）风口选品与装架图（POG）。"),
    8: ("🍂 8月·海外工厂大排产与订舱窗口", "出运美东美中必须在本月离港！海运耗时35-45天，确保货物在10月初进抵海外零售仓。"),
    9: ("🍁 9月·秋季供暖季备货攻坚窗口", "全美中东部与北方供暖设备启动；地面出风口、管道密封与暖通换新件第一波补货上架。"),
    10: ("🍁 10月·严冬前翻新与黑色星期五备货", "气温断崖下跌，地下室集中供热启动；商超为黑五网一促销锁死各店安全库存（Safety Stock）。"),
    11: ("❄️ 11月·黑五网一大促与寒潮爆发", "全美强寒潮袭击，中东部高产走廊（NC/TN/KY/OH/IN）地面出风口迎来年内出货最高峰。"),
    12: ("❄️ 12月·冬季抢险修缮与盘点月", "极寒冻裂与管道抢修高发；高耐寒金属配件出货稳健，同时准备次年春季改款。")
}

season_title, season_desc = season_months.get(curr_month, season_months[9])

with st.container():
    st.markdown(f"""
    <div class="season-box">
        <h4 style="margin:0 0 6px 0; color:#92400E;">⏰ 当前补货时钟：{season_title}</h4>
        <p style="margin:0 0 6px 0; color:#B45309; font-size:0.92rem;"><b>业务指引：</b>{season_desc}</p>
        <p style="margin:0; color:#78350F; font-size:0.85rem;">🚢 <b>供应链时钟建议：</b>国内港口（宁波/盐田）海运直发至美中/美东枢纽仓平均需 <b>35～45 天</b>，清关提柜需 <b>5～7 天</b>。当前出运批次可精准接轨后续 2 个月的核心促销周期！</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. 侧边栏：官方数据源配置与 Excel 导入
# ==============================================================================
with st.sidebar:
    st.header("⚙️ 官方售卖点数据配置")
    
    st.markdown("### 📤 导入官方在售明细 (可选)")
    uploaded_file = st.file_uploader(
        "上传商超官方在售表 (.csv 或 .xlsx)",
        type=["csv", "xlsx"],
        help="支持上传 The Home Depot Supplier Hub 或 Lowe's 后台导出的门店在售清单。只要表格中包含一列州名或缩写（如 State、省份），系统将自动替换基准测算，精准统计每州真实在售店数！"
    )
    
    uploaded_counts = {}
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                up_df = pd.read_csv(uploaded_file)
            else:
                up_df = pd.read_excel(uploaded_file)
                
            state_col = None
            for col in up_df.columns:
                c_clean = str(col).strip().lower()
                if c_clean in ["state", "st", "province", "州", "缩写", "state_code"]:
                    state_col = col
                    break
            
            if state_col:
                val_counts = up_df[state_col].astype(str).str.strip().str.upper().value_counts()
                uploaded_counts = val_counts.to_dict()
                st.success(f"✅ 成功识别在售点数据！共解析到 {len(uploaded_counts)} 个州的实时在售记录。")
            else:
                st.warning("⚠️ 表格中未识别到明确的「State / 州」列，已沿用商超官方基准数据库。")
        except Exception as e:
            st.error(f"解析失败: {str(e)}")
            
    st.markdown("---")
    calc_channel = st.selectbox(
        "若无上传文件，采用官方基准网点：",
        ["The Home Depot + Lowe's 官方总售卖点", "仅 The Home Depot 售卖点", "仅 Lowe's 售卖点"],
        index=0
    )
    
    coverage_rate = st.slider(
        "当前产品预估在售覆盖率 (%)：",
        min_value=10, max_value=100, value=85, step=5,
        help="若未上传在售表，系统将按该比例计算实际铺货门店数"
    )
    
    st.markdown("---")
    st.caption("💡 计算公式：全州实时总销能 = 真实在售门店数 × 单店出货流速 (件/店)")

# ==============================================================================
# 5. 动态计算全美销能与有效售卖点
# ==============================================================================
states_list = []
for s in STATES_DATA:
    abbr = s["abbr"]
    if "仅 The Home Depot" in calc_channel:
        base_stores = s["thd_stores"]
    elif "仅 Lowe's" in calc_channel:
        base_stores = s["lowes_stores"]
    else:
        base_stores = s["thd_stores"] + s["lowes_stores"]
        
    if abbr in uploaded_counts:
        active_stores = int(uploaded_counts[abbr])
        source_tag = "官方上传在售表"
    else:
        active_stores = int(base_stores * (coverage_rate / 100.0))
        source_tag = f"官方基准({coverage_rate}%覆盖)"
        
    total_sales_capacity = active_stores * s["velocity"]
    
    item = dict(s)
    item["base_stores"] = base_stores
    item["active_stores"] = active_stores
    item["total_capacity"] = total_sales_capacity
    item["source_tag"] = source_tag
    states_list.append(item)

df = pd.DataFrame(states_list)
df["capacity_rank"] = df["total_capacity"].rank(ascending=False, method="min").astype(int)

# ==============================================================================
# 6. 核心功能标签页导航
# ==============================================================================
tab_search, tab_specs, tab_table = st.tabs([
    "🔍 单州售卖点与气候详情下钻",
    "📐 规格尺寸与地材匹配指南",
    "📊 全美 48 州售卖点实时大屏"
])

# ---------------- Tab 1: 单州详情 ----------------
with tab_search:
    st.subheader("🔍 单州详情与全景分析卡片")
    options = [f"{s['abbr']} - {s['cn']} ({s['en']})" for s in states_list]
    
    col_sel, col_rank = st.columns()
    with col_sel:
        selected_option = st.selectbox("请选择要查询的州（支持输入州名或缩写）：", options, index=0)
        sel_abbr = selected_option.split(" - ")[0]
        cur = next(s for s in states_list if s["abbr"] == sel_abbr)
        cur_rank = int(df[df["abbr"] == sel_abbr]["capacity_rank"].values[0])
    with col_rank:
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption(f"当前数据源：`{cur['source_tag']}`")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("该州官方有效在售点", f"{cur['active_stores']} 家", f"商超总网点: {cur['base_stores']} 家")
    k2.metric("单店出货流速 (件/店)", f"{cur['velocity']:,} 件")
    k3.metric("全州实时总动销能级", f"{cur['total_capacity']:,} 件")
    k4.metric("全美实时动销总排名", f"第 {cur_rank} 名 / 48")

    st.markdown("---")
    
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("### 🌡️ 气候与住宅地基结构")
        st.write(f"**气候分类与表现**：{cur['climate']}")
        st.write(f"**地基与管网形式**：{cur['foundation']}")
        st.info(f"**🪵 地面材质偏好**：{cur['flooring_preference']}")
        
    with c_right:
        st.markdown("### 🎯 选品与货架策略")
        st.success(f"**✅ 适销主推产品**：{cur['best']}")
        st.warning(f"**⚠️ 避坑/受限产品**：{cur['avoid']}")
        st.markdown("### 📐 推荐主打规格分布")
        st.write(f"{cur['size_breakdown']}")

    st.markdown("### 🛒 零售商超渠道策略")
    st.info(f"**实战建议**：{cur['channel_advice']}")

# ---------------- Tab 2: 规格与地材矩阵 ----------------
with tab_specs:
    st.subheader("📐 北美出风口核心开孔规格与地材适配指南")
    st.markdown("""
    在北美大零售渠道，选品尺寸不精准是导致商超退货与积压的核心原因之一。各大区域因住宅建造年份不同，尺寸偏好差异显著：
    """)
    
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("#### 🌟 4x10 英寸（全美大通货）")
        st.write("- **全美占比**：约 65% - 70%")
        st.write("- **适用区域**：全美所有具备地面风管的独立住宅")
        st.write("- **备货建议**：任何首批进店必铺的核心规格，必须占单店 SKU 货架面积的一半以上。")
    with s2:
        st.markdown("#### 🏛️ 4x12 与 2x12 英寸（老宅与特殊区）")
        st.write("- **全美占比**：约 15% - 25%")
        st.write("- **适用区域**：中东部与东北部老州（PA、OH、NY、MA、IL）")
        st.write("- **结构特点**：4x12 适用于大挑高空间；2x12 多用于厨房橱柜底踢脚线（Toe-kick）或卫生间。")
    with s3:
        st.markdown("#### 🌀 6x6～12x12 顶装散流器（南方特供）")
        st.write("- **全美占比**：南方阳光带占 80%+")
        st.write("- **适用区域**：佛罗里达 (FL)、德州 (TX)、加州 (CA)、亚利桑那 (AZ)")
        st.write("- **结构特点**：天花板出风要求重量轻（ABS树脂/薄铝合金）、可调扩散叶片。")

    st.markdown("---")
    st.markdown("#### 🪵 地面材料配合与承重注意要点：")
    st.markdown("""
    1. **实木地板 (Hardwood) 与 LVP 锁扣地板**：在中东部（NC、TN、KY、IN）占 80% 以上。外框边缘法兰盘厚度严禁过厚（建议不超过 2.5mm），避免绊脚；
    2. **防卡鞋跟 (Heel-proof < 9.5mm)**：中高端社区（如 VA、MD、NJ）买家非常在意细高跟鞋被卡入格栅，缝隙必须经过防卡设计；
    3. **瓷砖地面 (Tile) 与高盐雾**：东南沿海浴室与厨房铺设较多，金属件需经受住盐雾测试，建议主推耐腐蚀 ABS 树脂或阳极氧化铝。
    """)

# ---------------- Tab 3: 全美大屏 ----------------
with tab_table:
    st.subheader("📊 全美 48 州售卖点与销能实时数据表")
    
    total_stores_sum = df["active_stores"].sum()
    total_cap_sum = df["total_capacity"].sum()
    
    m_a, m_b, m_c = st.columns(3)
    m_a.metric("全美有效在售门店总数", f"{total_stores_sum:,} 家")
    m_b.metric("全美实时预估总动销能级", f"{total_cap_sum:,} 件")
    m_c.metric("综合排名第一", f"{df.sort_values(by='total_capacity', ascending=False).iloc[0]['cn']}")
    
    st.markdown("---")
    
    show_df = df[["capacity_rank", "abbr", "cn", "en", "base_stores", "active_stores", "velocity", "total_capacity", "climate", "foundation", "best", "avoid", "size_breakdown"]]
    show_df.columns = ["实时总排名", "缩写", "中文州名", "英文州名", "商超基准店数", "有效在售店数", "单店流速(件/店)", "全州实时总动销(件)", "气候带", "房屋地基", "适销主推", "避坑品类", "开孔尺寸建议"]
    
    st.dataframe(show_df.sort_values(by="实时总排名"), use_container_width=True, height=550)
    
    csv_bytes = show_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 一键下载全美实时售卖点统计分析表 (.csv)",
        data=csv_bytes,
        file_name="US_RealTime_Store_Sales_Analysis_Pro.csv",
        mime="text/csv"
    )
