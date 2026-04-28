#!/usr/bin/env python3

import os, sys, re,datetime

def build_init():
    YUANWEN_FILE    = "披尋記.txt"
    PISHUN_FILE     = "披尋記-Text.txt"
    INDEX_FILE      = "披尋記-Index.txt"

    DIR_NAME = "Build"
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)
        
    return INDEX_FILE,YUANWEN_FILE,PISHUN_FILE,DIR_NAME


# --- 3. 样式 (保持 95% 精修版) ---
STYLE = """<style>
    :root {
        --main-gold: #c5a059; --dark-bg: #1a1a1a; --paper-bg: #f9f6f2; --content-white: #ffffff;
        --lun-text: #1b4d3e; --lun-bg: #f1f8f3; --pi-text: #1a1a1a; --tree-line: #e8e2d6;
        --box-shadow-v: 2px 2px 3px rgba(0, 0, 0, 0.3);
    }
    body { margin: 0; padding: 0; background-color: var(--paper-bg);  color: #333; }
    .page-header { background-color: var(--dark-bg); color: var(--main-gold); padding: 12px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid var(--main-gold); position: sticky; top: 0; z-index: 1000; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
    .progress-container { position: absolute; bottom: -3px; left: 0; width: 100%; height: 3px; background: transparent; }
    .progress-bar { height: 100%; background: var(--main-gold); width: 0%; transition: width 0.1s; }
    .back-btn { color: var(--main-gold); text-decoration: none; font-weight: bold; border: 1px solid var(--main-gold); padding: 4px 14px; border-radius: 4px; font-size: 0.85em; transition: 0.3s; }
    .back-btn:hover { background: var(--main-gold); color: #fff; }
    .scroll-container { 
        box-shadow: var(--box-shadow-v);
        max-width: 80%; margin: 40px auto; background-color: var(--content-white); padding: 60px 80px; min-height: 90vh; border-radius: 8px; position: relative;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://w3.org' width='4' height='4' viewBox='0 0 4 4'%3E%3Cpath fill='%23f0e6d2' fill-opacity='0.2' d='M1 3h1v1H1V3zm2-2h1v1H3V1z'%3E%3C/path%3E%3C/svg%3E"); }
    .scroll-container::before { content: ""; position: absolute; top: 0; bottom: 0; left: 0; width: 12px; background: linear-gradient(to right, rgba(197,160,89,0.15) 0%, rgba(197,160,89,0.05) 50%, transparent 100%); border-left: 1px solid rgba(197,160,89,0.1); }
    .tree-branch { margin-left: 18px; border-left: 1px solid var(--tree-line); padding-left: 12px; }
    .scroll-container > .tree-branch { margin-left: 0; border-left: none; padding-left: 0; }
    summary { list-style: none; outline: none; cursor: pointer; }
    .title-row { display: flex; align-items: baseline; gap: 12px; padding: 3px 0; margin-bottom: 2px; }
    .node-title { font-weight: 900; color: #3e2723; font-size: 1.3em; white-space: nowrap; letter-spacing: 1px; }
    .node-title:before { content: "◈"; font-size: 0.85em; margin-right: 8px; color: var(--main-gold); }
    .btn-self-toggle { font-size: 0.7em; color: #bbb; background: #fafafa; padding: 1px 10px; border-radius: 12px; user-select: none; cursor: pointer; border: 1px solid #eee; transition: 0.2s; }
    .btn-self-toggle:hover { color: var(--main-gold); border-color: var(--main-gold); background: #fff; }
    .content-wrapper { margin: 4px 0 12px 0; }
    .content-hidden { display: none !important; }
    .yuanwen { font-family: "STKaiti", "Source Han Serif SC", serif; box-shadow: var(--box-shadow-v);font-size: 1.25em; font-weight: 900; letter-spacing: 1px; background: var(--lun-bg); border-left: 6px solid #2e7d32; padding: 6px 15px; margin: 4px 0; color: var(--lun-text); }
    .zhushi { font-family: serif;font-size: 1.05em; font-weight: 400; line-height: 1.6; background: #fdfdfb; border-left: 3px solid var(--main-gold); padding: 6px 15px; margin: 0 0 4px 4px; color: var(--pi-text); white-space: pre-wrap; border: 1px solid #f0f0f0; border-radius: 0 4px 4px 0; }
    .tag { font-size: 0.8em; font-weight: 900; padding: 1px 5px; border-radius: 3px; margin-right: 12px; display: inline-block; vertical-align: middle; }
    .tag-y { background: #2e7d32; color: #fff; }
    .tag-p { background: var(--main-gold); color: #fff; }
    .page-footer { text-align: center; padding: 80px 20px; color: #bbb; font-size: 0.9em; letter-spacing: 3px; }
    .fab-top { position: fixed; bottom: 40px; right: 40px; width: 50px; height: 50px; background: #fff; color: var(--main-gold); border: 2px solid var(--main-gold); border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-weight: bold; box-shadow: 0 5px 20px rgba(0,0,0,0.1); transition: 0.3s; z-index: 2000; }
    .fab-top:hover { transform: scale(1.1); background: var(--main-gold); color: #fff; }
</style>"""



STYLE_JS = """<script>
window.onscroll = function() {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("progressBar").style.width = scrolled + "%";
};
function toggleContent(event, id) {
    event.stopPropagation();
    const el = document.getElementById(id);
    const btn = event.target;
    if (el.classList.contains('content-hidden')) {
        el.classList.remove('content-hidden'); btn.innerText = '隱藏';
    } else {
        el.classList.add('content-hidden'); btn.innerText = '展開';
    }
}
</script>"""


INDEX_STYLE = """
<style>
    :root { --main-gold: #c5a059; --dark-accent: #2c3e50; --bg-paper: #f9f6f2; --text-color: #3e2723; }
    body { background-color: var(--bg-paper); font-family: "I.MingCP", "Source Han Serif SC", serif; margin: 0; color: var(--text-color); line-height: 1.6; }
    .header { background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://metmuseum.org'); background-size: cover; background-position: center; color: var(--main-gold); text-align: center; padding: 40px 20px; border-bottom: 4px solid var(--main-gold); }
    .header h1 { font-size: 2.8em; margin: 0; letter-spacing: 8px; font-weight: 900; }
    .header p { font-size: 1.1em; opacity: 0.9; margin-top: 10px; letter-spacing: 4px; }
    .container { max-width: 1100px; margin: -20px auto 30px; background: white; padding: 30px 40px; box-shadow: 0 15px 40px rgba(0,0,0,0.15); border-radius: 4px; }
    .intro-section { display: flex; gap: 20px; margin-bottom: 25px; border-bottom: 1px double #ddd; padding-bottom: 20px; }
    .intro-card { flex: 1; padding: 15px; border: 1px solid #f0e6d2; background: #fffcf5; }
    .intro-card h3 { color: var(--main-gold); border-bottom: 2px solid var(--main-gold); display: inline-block; margin: 0 0 8px 0; font-size: 1.2em; }
    .intro-card p { font-size: 0.95em; color: #5d4037; margin: 0; text-align: justify; }
    .catalog-title { text-align: center; font-size: 1.6em; color: var(--dark-accent); margin: 30px 0 20px 0; letter-spacing: 2px; }
    .catalog-title:after { content: ""; display: block; width: 60px; height: 3px; background: var(--main-gold); margin: 10px auto; }
    .index-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
    .index-item { border: 1px solid #f0e6d2; padding: 10px 15px; transition: all 0.3s; display: flex; align-items: center; background: #fdfdfb; text-decoration: none; color: var(--text-color); font-weight: bold; font-size: 1em; border-radius: 2px; }
    .index-item:hover { background: var(--main-gold); color: white; transform: translateX(5px); }
    .index-item:before { content: "❧"; margin-right: 8px; color: var(--main-gold); }
    .future-section { margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; }
    .future-grid { display: flex; justify-content: center; gap: 15px; margin-top: 15px; }
    .future-card { padding: 10px 15px; background: #f8f9fa; border: 1px dashed var(--main-gold); color: #888; border-radius: 4px; flex: 1; max-width: 200px; font-size: 0.9em; }
    footer { text-align: center; padding: 30px; font-size: 0.9em; color: #999; border-top: 1px solid #eee; margin-top: 30px; }
    .gemini-badge { display: inline-block; margin-top: 10px; padding: 3px 12px; border: 1px solid #4285f4; color: #4285f4; border-radius: 20px; font-family: sans-serif; font-size: 0.8em; font-weight: bold; }
</style>"""

def clean_blank_key(text):
    return re.sub(r'[\s　]', '', text)

def get_clean_title(title):
    main_part = re.split(r'[ 　\t]', title)[0]
    main_part = re.sub(r'\d+$', '', main_part)
    return main_part

def get_safe_filename(title):
    clean_t = get_clean_title(title)
    return re.sub(r'[ \/\\:?*"<>|]', '_', clean_t)


def load_index_sequentially(filename):
    
    tree_data = {}
    index_sequence = []

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            c = clean_blank_key(line)
            # 即使 c 重复，我们也记录在 sequence 里
            unique_id = f"{len(index_sequence)}_{c}"
            tree_data[unique_id] = {"title": line, "key": c, "data": []}
            index_sequence.append(unique_id)
    
    return tree_data,index_sequence


# --- 2. 顺序加载内容函数 (解决同名 Bug) ---
def load_content_sequentially(filename, tag, tree_data, index_sequence):
    if not os.path.exists(filename): return
    
    current_ptr = 0 # 指向 index_sequence 的当前位置
    total_indices = len(index_sequence)
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line_s = line.strip()
            if not line_s: continue
            
            c_line = clean_blank_key(line_s)
            found_match_at = -1
            
            # 搜索范围：从当前指针向后找 100 个索引 (防止跨度太大的误差)
            search_limit = min(current_ptr + 100, total_indices)
            for i in range(current_ptr, search_limit):
                target_uid = index_sequence[i]
                if tree_data[target_uid]["key"] == c_line:
                    found_match_at = i
                    break
            
            if found_match_at != -1:
                # 匹配到了索引，更新指针到此位置
                current_ptr = found_match_at
            else:
                # 这一行是正文，挂在当前指针指向的索引下
                if current_ptr < total_indices:
                    target_uid = index_sequence[current_ptr]
                    tree_data[target_uid]["data"].append((tag, line_s))


# --- 4. 生成函数 ---
def render_output(include_pishun, tree_data, index_sequence,DIR_NAME):

    LEVELS_STR      = "甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥天地玄黃宇宙洪荒日月盈昃宿列張寒來暑往"
    level_map = {char: i + 1 for i, char in enumerate(LEVELS_STR)}

    links = []
    curr_fp = None
    stack = []
    suffix = "" if include_pishun else "_純論"
    tag_ver = "p" if include_pishun else "y"

    for uid in index_sequence:
        node = tree_data[uid]
        first_char = node["key"][0]
        
        if first_char == '甲':
            if curr_fp:
                while stack: curr_fp.write("</details></div>\n"); stack.pop()
                curr_fp.write('</div><div class="page-footer">般若常照 · 萬法唯識</div><div class="fab-top" onclick="window.scrollTo({top: 0, behavior: \'smooth\'})">▲</div></body></html>')
                curr_fp.close()
            
            title_text = get_clean_title(node["title"])
            fname = get_safe_filename(node["title"]) + suffix
            curr_fp = open(os.path.join(DIR_NAME, f"{fname}.html"), 'w', encoding='utf-8')
            curr_fp.write(f'<html><head><meta charset="UTF-8"><title>{title_text}</title>{STYLE}{STYLE_JS}</head><body>')
            curr_fp.write(f'<div class="page-header"><div class="progress-container"><div class="progress-bar" id="progressBar"></div></div><a href="index.html" class="back-btn">← 返回目錄</a><div class="nav-center"><div class="main-title">瑜伽師地論·披尋記</div><div class="sub-title">{title_text}</div></div><div style="width:100px;"></div></div><div class="scroll-container">')
            links.append(f'<a href="{fname}.html" class="index-item">{title_text}</a>')
            stack = []

        if not curr_fp: continue

        val = level_map.get(first_char, 999)
        while stack and val <= stack[-1]:
            curr_fp.write("</details></div>\n")
            stack.pop()

        stack.append(val)
        cid = f"c_{uid}_{tag_ver}"
        
        curr_fp.write(f'<div class="tree-branch"><details open><summary><div class="title-row"><div class="node-title">{node["title"]}</div>')
        if node["data"]:
            curr_fp.write(f'<div class="btn-self-toggle" onclick="toggleContent(event, \'{cid}\')">隱藏</div>')
        curr_fp.write('</div></summary>')
        
        if node["data"]:
            curr_fp.write(f'<div id="{cid}" class="content-wrapper">')
            for tag, text in node["data"]:
                if tag == "Y":
                    curr_fp.write(f'<div class="yuanwen"><span class="tag tag-y">論</span>{text}</div>')
                elif tag == "P" and include_pishun:
                    curr_fp.write(f'<div class="zhushi"><span class="tag tag-p">披</span>{text}</div>')
            curr_fp.write('</div>')

    if curr_fp:
        while stack: curr_fp.write("</details></div>\n"); stack.pop()
        curr_fp.write('</div></body></html>'); curr_fp.close()
    return links

def render_main_page(links_pure,links_pishun,DIR_NAME):

    with open(os.path.join(DIR_NAME, "index.html"), 'w', encoding='utf-8') as f:
        f.write(f'<html><head><meta charset="UTF-8">{INDEX_STYLE}</head><body>')
        f.write("""
            <div class="header"><h1>瑜伽師地論·披尋記</h1><p>彌勒菩薩說 · 玄奘大師譯 · 韓清淨科記</p></div>
            <div class="container">
                <div class="intro-section">
                    <div class="intro-card"><h3>慈氏彌勒</h3><p>唯識行派鼻祖。此論乃其於兜率天為無著菩薩所宣，統攝十七地修行境位，為瑜伽行者之根本依止。</p></div>
                    <div class="intro-card"><h3>韓清淨居士</h3><p>近代唯識大德。其《披尋記》耗數十年心血，彙集諸論證盟，科句嚴整，使千年難讀之論重放光明。</p></div>
                </div>
                
                <h2 class="catalog-title">全論五分 · 百卷目錄 (純論版)</h2>
                <div class="index-grid">
        """)
        f.write("\n".join(links_pure))
        f.write("""
                </div>
                <h2 class="catalog-title">披尋記五分 · 百卷目錄 (合刊版)</h2>
                <div class="index-grid">
        """)
        f.write("\n".join(links_pishun))

        now = datetime.datetime.now()
        build_number = now.strftime("%Y%m%d.%H%M")

        f.write(f'''
                </div>
                <div class="future-section">
                    <h2 class="catalog-title" style="font-size:1.3em;">法脈傳承 · 待增續部</h2>
                    <div class="future-grid">
                        <div class="future-card">顯揚聖教論披尋記</div>
                        <div class="future-card">攝大乘論校釋</div>
                        <div class="future-card">唯識三十頌略解</div>
                        <div class="future-card">成唯识论疏翼</div>
                        <div class="future-card">能断金刚般若波罗蜜多经论会释</div>
                    </div>
                </div>
            </div>
            <footer>數位輯錄版 · 般若常照 · 萬法唯識<br>
            <span style="font-size: 0.8em; color: #bbb; letter-spacing: 1px;">
                Build {build_number}
            </span><br>
            <br><div class="gemini-badge">Produced with Google Gemini</div></footer>
        </body></html>
        ''')


def main():
    idx_file,jing_file,pixun_file,DIR_NAME = build_init()

    data,index = load_index_sequentially(idx_file)
    load_content_sequentially(jing_file, "Y" ,data,index)
    load_content_sequentially(pixun_file, "P" ,data,index)

    render_main_page(
        render_output(False,data,index,DIR_NAME),
        render_output(True,data,index,DIR_NAME), DIR_NAME)

    print("修正版處理完成！已解決同名索引重複插入 Bug。")


if __name__ == '__main__':
    sys.exit(main())
