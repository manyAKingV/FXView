import os
import yaml

# 定义 company 和 logos 文件夹路径
company_dir = "company"
logos_dir = "logos"
output_file = "generated_landscape.yml"

# 初始化 landscape 数据结构
landscape_data = [
    {
        "category": {
            "name": "Application应用层",
            "subcategories": []
        }
    }
]

# 存储一级分类和二级分类的映射
category_map = {}

# 遍历 company 文件夹中的所有 .md 文件
for filename in os.listdir(company_dir):
    if filename.endswith(".md") or filename.endswith(".txt"):
        file_path = os.path.join(company_dir, filename)

        # 读取并解析 .md 文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            content = {}
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    content[key.strip()] = value.strip()

        # 获取公司名称和 logo 文件名
        company_name = content.get("名称", "未知公司")
        description = content.get("描述", "")
        founded_year = content.get("成立时间", "")
        homepage_url = content.get("官网网站", "")
        first_category = content.get("一级分类", "其他")
        second_category = content.get("二级分类", "其他")

        # 在 logos 文件夹中查找匹配的 logo 文件
        logo_filename = None
        for logo in os.listdir(logos_dir):
            company_name_logo = logo_filename+'logo'
            if company_name in logo or company_name_logo in logo:
                logo_filename = logo
                break

        # 构建 item 数据
        item_data = {
            "item": {
                "name": company_name,
                "homepage_url": homepage_url,
                "logo": logo_filename if logo_filename else ""
            }
        }

        # 按照一级分类和二级分类组织数据
        if first_category not in category_map:
            category_map[first_category] = {}
        if second_category not in category_map[first_category]:
            category_map[first_category][second_category] = []
        category_map[first_category][second_category].append(item_data)

# 将分类结构转换为 landscape.yml 格式
for first_cat, subcats in category_map.items():
    category_entry = {
        "category": {
            "name": first_cat,
            "subcategories": []
        }
    }
    for second_cat, items in subcats.items():
        subcategory_entry = {
            "subcategory": {
                "name": second_cat,
                "items": items
            }
        }
        category_entry["category"]["subcategories"].append(subcategory_entry)
    landscape_data.append(category_entry)

# 写入生成的 YAML 文件
with open(output_file, "w", encoding="utf-8") as f:
    yaml.dump({"landscape": landscape_data}, f, allow_unicode=True, sort_keys=False)

print(f"已成功生成 {output_file} 文件！")