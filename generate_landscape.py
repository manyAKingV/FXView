import os
import re
from pypinyin import lazy_pinyin, Style

# 定义路径
company_dir = "company"
logos_dir = "logos"
output_file = "landscape.yml"

# 提取中文字符的拼音首字母（最多前5个）
def get_chinese_prefix(name):
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', name)
    if not chinese_chars:
        return ''
    pinyin_list = lazy_pinyin(chinese_chars[:5], style=Style.FIRST_LETTER)
    return ''.join(pinyin_list)
# 判断网址是否有协议头，无则补充 https://
def ensure_protocol(url):
    if not url:
        return ""
    # 匹配 http:// 或 https:// 开头
    if not re.match(r'^https?://', url):
        return f'https://{url}'
    return url

# 构建最终结构
category_map = {}

# 遍历 .md 文件
for filename in os.listdir(company_dir):
    if filename.endswith(".md") or filename.endswith(".txt"):
        file_path = os.path.join(company_dir, filename)

        # 解析内容
        with open(file_path, "r", encoding="utf-8") as f:
            content = {}
            for line in f:
                line = line.strip().replace("：", ":")
                if ":" in line:
                    key, value = line.split(":", 1)
                    content[key.strip()] = value.strip()

        company_name = content.get("名称", "未知公司")
        raw_description = content.get("描述", "")
        founded_year = content.get("成立时间", "")
        homepage_url = content.get("官网网站", "")
        first_category = content.get("一级分类", "其他")
        second_category = content.get("二级分类", "其他")
        display_size = content.get("展示大小", "").strip()
        display_priority_str = content.get("展示优先级", "").strip()

        display_priority = None
        if display_priority_str.isdigit():
            num = int(display_priority_str)
            if 1 <= num <= 5:
                display_priority = num

        # 构造描述
        description_parts = []
        if raw_description:
            description_parts.append(raw_description)
        else:
            description_parts.append("科技公司")
        if founded_year:
            description_parts.append(f"成立于 {founded_year}")
        description = "，".join(description_parts)

        # 查找 logo
        logo_filename = None
        for logo in os.listdir(logos_dir):
            if logo.lower().endswith(".svg") and (company_name in logo or logo.replace(".svg", "") in company_name):
                logo_filename = logo
                break

        # 添加拼音前缀
        prefix = get_chinese_prefix(company_name)
        prefixed_company_name = prefix + company_name if prefix else company_name
        
        # 补全官网链接协议头
        homepage_url = ensure_protocol(homepage_url)

        # 构建公司对象
        company_obj = {
            "name": prefixed_company_name,
            "homepage_url": homepage_url,
            "logo": logo_filename if logo_filename else "",
            "description": description,
        }

        if display_size == "大" and display_priority is not None:
            company_obj["project"] = f"level{display_priority}"

        # 分类组织
        if first_category not in category_map:
            category_map[first_category] = {}
        if second_category not in category_map[first_category]:
            category_map[first_category][second_category] = {"large_items": [], "small_items": []}

        if display_size == "大" and display_priority is not None:
            category_map[first_category][second_category]["large_items"].append(company_obj)
        elif display_size == "小":
            category_map[first_category][second_category]["small_items"].append({
                "data": company_obj,
                "priority": display_priority
            })
        else:
            category_map[first_category][second_category]["small_items"].append({
                "data": company_obj,
                "priority": None
            })

# 手动构建 YAML 内容字符串
yaml_content = "landscape:\n"

for first_cat, subcats in category_map.items():
    yaml_content += f"    - category:\n"
    yaml_content += f"      name: {first_cat}\n"
    yaml_content += f"      subcategories:\n"

    for second_cat, items_dict in subcats.items():
        yaml_content += f"        - subcategory:\n"
        yaml_content += f"          name: {second_cat}\n"
        yaml_content += f"          items:\n"

        large_items = sorted(
            items_dict["large_items"],
            key=lambda x: int(x.get("project", "level5").replace("level", ""))
        )

        small_items_sorted = sorted(
            [item for item in items_dict["small_items"] if item["priority"] is not None],
            key=lambda x: x["priority"]
        )
        small_items_invalid = [item for item in items_dict["small_items"] if item["priority"] is None]

        all_items = [
            item for item in large_items
        ] + [
            item["data"] for item in small_items_sorted
        ] + [
            item["data"] for item in small_items_invalid
        ]

        for item in all_items:
            yaml_content += f"          - item:\n"
            yaml_content += f"            name: {item['name']}\n"
            yaml_content += f"            homepage_url: {item['homepage_url']}\n"
            yaml_content += f"            logo: {item['logo']}\n"
            yaml_content += f"            description: {item['description']}\n"
            if 'project' in item:
                yaml_content += f"            project: {item['project']}\n"

# 写入 YAML 文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write(yaml_content)

print(f"✅ 已成功生成 {output_file} 文件！")