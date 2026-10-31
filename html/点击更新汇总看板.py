
# -*- coding: utf-8 -*-
"""
自动重建 电商多维可视化汇总看板.html
扫描 html 目录下所有 *.html（自动排除看板自身），重新生成看板（保留样式与交互）
用法：新增图表后运行一次  python 更新汇总看板.py  或直接双击
"""
import sys, subprocess, os, io, json
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except AttributeError:
    pass

HTML_DIR = r"D:\HuaweiMoveData\Users\刘双江\Desktop\爬虫2\图片\动态图\html"
OUT = os.path.join(HTML_DIR, '电商多维可视化汇总看板.html')
SELF = os.path.basename(OUT)

# ---------- 扫描目录（排除看板自身） ----------
files = sorted(f for f in os.listdir(HTML_DIR)
               if f.lower().endswith('.html') and f != SELF)
names = [f[:-5] for f in files]      # 去掉 .html 作为标签名
urls = files
print(f'扫描到 {len(files)} 个 html 文件（已排除看板自身）')

# ---------- 看板模板（占位符 __NAMES__ / __URLS__ 由脚本填充） ----------
tpl = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>电商多维可视化汇总看板</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            font-family: "Microsoft YaHei", SimHei, sans-serif;
            background-color: #070c1a;
            color: #e8f0ff;
            padding: 24px;
            margin: 0;
        }
        h1 {
            text-align: center;
            color: #5ab8ff;
            margin-top: 0;
            margin-bottom: 6px;
            font-size: 24px;
        }
        .count {
            text-align: center;
            color: #8fa3c4;
            font-size: 13px;
            margin-bottom: 16px;
        }
        .tab-container {
            margin-bottom: 16px;
            text-align: center;
        }
        .tab-btn {
            padding: 10px 18px;
            margin: 4px;
            background: #142447;
            color: #e8f0ff;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: 0.2s;
        }
        .tab-btn:hover {
            background: #233b70;
        }
        .tab-btn.active {
            background-color: #5ab8ff;
            color: #070c1a;
            font-weight: bold;
        }
        .iframe-wrap {
            width: 100%;
        }
        iframe {
            width: 100%;
            height: 740px;
            border: 2px solid #203466;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <h1>电商多维可视化汇总看板</h1>
    <div class="count" id="countText"></div>
    <div class="tab-container" id="tabBox">
        <!-- 按钮由JS自动生成，不用手动在这里加按钮 -->
    </div>
    <div class="iframe-wrap">
        <iframe id="chartFrame" src=""></iframe>
    </div>
<script>
// 由 更新汇总看板.py 自动生成，请勿手改数组；新增图表后重新运行脚本即可
const name_list = __NAMES__;
const url_list = __URLS__;
// ======================================
const tabBox = document.getElementById("tabBox");
const frame = document.getElementById("chartFrame");
document.getElementById("countText").innerText = "共 " + name_list.length + " 张动态图表 · 点击切换";
name_list.forEach((name, idx) => {
    const btn = document.createElement("button");
    btn.className = "tab-btn";
    btn.innerText = name;
    btn.onclick = () => switchTab(idx);
    tabBox.appendChild(btn);
});
function switchTab(index) {
    frame.src = url_list[index];
    document.querySelectorAll(".tab-btn").forEach((b, i) => {
        b.classList.toggle("active", i === index);
    });
}
switchTab(0);
</script>
</body>
</html>
'''

html = (tpl
        .replace('__NAMES__', json.dumps(names, ensure_ascii=False))
        .replace('__URLS__', json.dumps(urls, ensure_ascii=False)))
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print('已重建:', OUT)
print('图表清单:')
for i, n in enumerate(names, 1):
    print(f'  {i:2d}. {n}')
