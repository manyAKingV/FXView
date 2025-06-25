import os
import re
import json
import glob

# ========================
# 日志函数
# ========================
def log_step(step_name):
    print(f"[INFO] 正在执行步骤: {step_name}")



# ========================
# 去除字符串开头的英文部分
# ========================
def extract_chinese(text):
    match = re.search(r'[\u4e00-\u9fff]', text)
    if match:
        return text[match.start():]
    return text.strip()


# ========================
# 替换 index.html 中的 category 层级名称
# ========================
def replace_category_in_html(html_file_path, replacements):
    """在 HTML 文件中替换指定的 category 名称"""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        modified_content = content
        for old_name in sorted(replacements, key=len, reverse=True):  # 按长度排序以避免短名称被优先替换
            new_name = replacements[old_name]
            modified_content = modified_content.replace(old_name, new_name)

        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        print("[SUCCESS] HTML 文件中 category 替换完成")

    except Exception as e:
        print(f"[ERROR] 处理 HTML 文件时发生错误: {e}")


# ========================
# JSON name 字段处理函数（去除英文前缀）
# ========================
def process_json_name_prefix(json_file_paths):
    def remove_prefix(name):
        for i, char in enumerate(name):
            if '\u4e00' <= char <= '\u9fff':
                return name[i:]
        return name

    try:
        for json_file_path in json_file_paths:
            if not os.path.exists(json_file_path):
                print(f"[ERROR] 找不到文件: {json_file_path}")
                continue

            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            for item in data.get('items', []):
                if 'name' in item:
                    original_name = item['name']
                    if any('\u4e00' <= char <= '\u9fff' for char in original_name):
                        new_name = remove_prefix(original_name)
                        item['name'] = new_name

            with open(json_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            print(f"[SUCCESS] 已完成对文件 {json_file_path} 的 name 字段处理")

    except Exception as e:
        print(f"[ERROR] 处理 JSON 文件时发生错误: {e}")


# ========================
# 执行文本替换任务（来自 replace_text.py）
# ========================
def perform_replace_tasks(tasks):
    for task in tasks:  
        file_pattern = task["file_path"]
        files = glob.glob(file_pattern)
        
        if not files:
            print(f"❌ 没有找到匹配的文件: {file_pattern}")
            continue

        if files:
            file_path = files[0]

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        matches = list(re.finditer(task["find"], content))
        if not matches:
            print(f"⚠️ 在文件 {file_path} 中未找到查找语句: {task['find']}")
            continue

        updated_content, num_replacements = re.subn(task["find"], task["replace"], content)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        for i, match in enumerate(matches):
            print(f"✅ 替换成功：文件 {file_path} 第 {i + 1} 处匹配，位置：{match.start()} - {match.end()}")
            print(f"   原内容: {content[match.start():match.end()]}")
            print(f"   新内容: {task['replace']}")

    print("🎉 文本替换任务已完成！")


# ========================
# 主程序入口
# ========================
def main():
    # 定义路径
    html_file_path = 'build/index.html'
    json_file_path = [
    'build/data/full.json'
    ]
    config_file = 'replace_config.json'

    # Step 2: 读取配置文件中的 fixed_categories
    if not os.path.exists(config_file):
        print(f"[ERROR] 找不到 {config_file}，请先运行 generate_landscape.py 或手动创建")
        return

    with open(config_file, 'r', encoding='utf-8') as f:
        fixed_categories = json.load(f)

    # Step 3: 替换 HTML 中的固定 category 名称
    log_step("替换 HTML 文件中的 category 名称")
    replace_category_in_html(html_file_path, fixed_categories)

    # Step 4: 处理 full.json 中的 name 字段（去英文前缀）
    log_step("处理 JSON 文件中的 name 字段（去除英文前缀）")
    process_json_name_prefix(json_file_path)

    # Step 5: 执行其他文本替换任务（如按钮文字等）
    replace_tasks = [
        {
            "file_path": "build/assets/index-*.js",
            "find": r'<div class="d-none d-lg-block fw-semibold ps-2">Filters',
            "replace": '<div class="d-none d-lg-block fw-semibold ps-2">筛选'
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r"Toe=S\('<div><small class=\"text-muted me-2\">GROUP",
            "replace": "Toe=S('<div><small class=\"text-muted me-2\">分组"
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r"Doe=S\('<div><small class=\"text-muted me-2\">ZOOM",
            "replace": "Doe=S('<div><small class=\"text-muted me-2\">大小"
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r'Rt.Grid',
            "replace": "\"grid\""
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r'Rt.Card',
            "replace": "\"card\"" 
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r'\bGrid\b',
            "replace": '行业景观图'
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r'\bCard\b',
            "replace": '企业名片'
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r'<button aria-label="Go to &quot;Stats&quot; page">Stats',
            "replace": '<button aria-label="Go to &quot;Stats&quot; page">统计数据'
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r'<button aria-label="Go to &quot;Explore&quot; page">Explore',
            "replace": '<button aria-label="Go to &quot;Explore&quot; page">生态图'
        },
        {
            "file_path": "build/assets/index-CtmZlmQ2.css",
            "find": r'_catTitle_1rhfx_1\s*\{[^}]*?height:\s*110px[^}]*?\}',
            "replace": '_catTitle_1rhfx_1{top:.5rem;left:7px;height:70px;width:30px;writing-mode:vertical-rl;text-orientation:mixed}'
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r'<div><small class="text-muted text-nowrap me-2">VIEW MODE:</small></div>',
            "replace": '<div><small class="text-muted text-nowrap me-2">视图模式:</small></div>'
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r'We couldn\'t find any items that match the criteria selected.',
            "replace": '我们找不到任何符合所选条件的项目。'
        },
        {
            "file_path": "build/assets/index-*.js",
            "find": r'<div>Type <small>/</small> to search items',
            "replace": '<div>使用 <small>/</small> 搜索公司'
        }
        
    ]
    log_step("执行预定义的文本替换任务")
    perform_replace_tasks(replace_tasks)

    print("✅ 所有替换操作已全部完成！")


if __name__ == "__main__":
    main()