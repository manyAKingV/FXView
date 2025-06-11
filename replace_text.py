import os

# 定义文件路径
file_path = '/Users/suyuchen/Product/FXView/build/assets/index-BmSWXqza.js'
keyword = '<div class="d-none d-lg-block fw-semibold ps-2">筛选'

# 检查文件是否存在
if os.path.exists(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 判断是否需要替换（假设英文为 'filter'）
    if keyword not in content:
        # 替换关键字
        updated_content = content.replace('<div class="d-none d-lg-block fw-semibold ps-2">Filters', keyword)

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print(f"关键字 'filter' 已被替换为 '{keyword}'。")
    else:
        print(f"文件中已包含关键字 '{keyword}'，无需替换。")
else:
    print(f"文件 {file_path} 不存在。")