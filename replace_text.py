import os
import re

# 替换任务定义
replace_tasks = [
    {
        "file_path": "build/assets/index-BmSWXqza.js",
        "find": r'<div class="d-none d-lg-block fw-semibold ps-2">Filters',
        "replace": '<div class="d-none d-lg-block fw-semibold ps-2">筛选'
    },
    {
        "file_path": "build/assets/index-BmSWXqza.js",
        "find": r"Toe=S\('<div><small class=\"text-muted me-2\">GROUP",
        "replace": "Toe=S('<div><small class=\"text-muted me-2\">分组"
    },
    {
        "file_path": "build/assets/index-BmSWXqza.js",
        "find": r"Doe=S\('<div><small class=\"text-muted me-2\">ZOOM",
        "replace": "Doe=S('<div><small class=\"text-muted me-2\">大小"
    },
    {
        "file_path": "build/assets/index-BmSWXqza.js",
        "find": r'<button aria-label="Go to &quot;Stats&quot; page">Stats',
        "replace": '<button aria-label="Go to &quot;Stats&quot; page">统计数据'
    },
    {
        "file_path": "build/assets/index-BmSWXqza.js",
        "find": r'<button aria-label="Go to &quot;Explore&quot; page">Explore',
        "replace": '<button aria-label="Go to &quot;Explore&quot; page">生态图'
    },
    {
        "file_path": "build/assets/index-CtmZlmQ2.css",
        "find": r"_catTitle_1rhfx_1\{top:.5rem;left:7px;height:110px;width:30px;-moz-transform:scale$-1,-1$;-webkit-transform:scale$-1,-1$;-o-transform:scale$-1,-1$;-ms-transform:scale$-1,-1$;transform:scale$-1$;writing-mode:vertical-rl;text-orientation:mixed\}",
        "replace": "catTitle_1rhfx_1{top:.5rem;left:7px;height:110px;width:30px;writing-mode:vertical-rl;text-orientation:mixed}"
    },
    {
        "file_path": "build/assets/index-BmSWXqza.js",
        "find": r'div><small class="text-muted text-nowrap me-2">VIEW MODE:</small></div>',
        "replace": '<div><small class="text-muted text-nowrap me-2">视图模式:</small></div>'
    }
]

# 执行替换
for task in replace_tasks:
    file_path = task["file_path"]
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"❌ 文件 {file_path} 不存在。跳过此任务。")
        continue
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 查找所有匹配项
    matches = list(re.finditer(task["find"], content))
    
    if not matches:
        print(f"⚠️ 在文件 {file_path} 中未找到查找语句: {task['find']}")
        continue
    
    # 进行替换
    updated_content, num_replacements = re.subn(task["find"], task["replace"], content)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    # 输出日志
    for i, match in enumerate(matches):
        print(f"✅ 替换成功：文件 {file_path} 第 {i + 1} 处匹配，位置：{match.start()} - {match.end()}")
        print(f"   原内容: {content[match.start():match.end()]}")
        print(f"   新内容: {task['replace']}")

print("🎉 所有替换任务已完成！")