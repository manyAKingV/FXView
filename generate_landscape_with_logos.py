import os
import base64
from pathlib import Path
from PIL import Image
import yaml

"""
功能：
    1. 将 company/logos 目录中的图片转换为 SVG 格式，输出到 logos/
    2. 解析 company/ 中的 .md 文件，结合生成的 logo，生成标准格式的 landscape.yml
"""

# ========================
# 第一部分：图片转 SVG 功能
# ========================

def convert_images_to_svg(input_dir: Path, output_dir: Path):
    """
    将指定目录中的所有图片转换为SVG格式并保存到输出目录
    :param input_dir: 包含原始图片的目录
    :param output_dir: 保存SVG文件的目标目录
    :return: 转换的文件数量
    """
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
    converted_count = 0

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    print("[INFO] 开始执行图片转 SVG 功能")
    for file in input_dir.iterdir():
        if file.is_file() and file.suffix.lower() in image_extensions:
            try:
                img = Image.open(file)
                with open(file, 'rb') as f:
                    img_data = f.read()

                svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{img.width}" height="{img.height}">
<image href="data:image/{file.suffix[1:]};base64,{base64.b64encode(img_data).decode('utf-8')}"/>
</svg>'''

                svg_filename = file.with_suffix('.svg').name
                svg_path = output_dir / svg_filename

                with open(svg_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)

                print(f"[SUCCESS] 成功转换图片: {file.name} -> {svg_filename}")
                converted_count += 1
            except Exception as e:
                print(f"[ERROR] 图片转换失败: {file.name} - {str(e)}")

    print(f"[INFO] 图片转 SVG 功能完成，共转换 {converted_count} 个文件\n")
    return converted_count


def run_image_conversion():
    root_dir = Path.cwd()
    input_dir = root_dir / "company" / "logos"
    output_dir = root_dir / "logos"

    if not input_dir.exists():
        print(f"[ERROR] 输入目录 {input_dir} 不存在，请检查路径或数据是否存在")
        return False

    print("[ACTION] 正在执行：图片转 SVG")
    convert_images_to_svg(input_dir, output_dir)
    print("[ACTION] 图片转 SVG 执行完毕\n")
    return True


# ========================
# 第二部分：生成 landscape.yml
# ========================

def ensure_protocol(url: str) -> str:
    """确保URL有协议头"""
    if not url:
        return ""
    if url.startswith(('http://', 'https://')):
        return url
    return f"https://{url}"

def generate_landscape_yaml(company_dir: str, logos_dir: str, output_file: str):
    """
    解析 .md 文件，生成 landscape.yml 结构
    """
    print("[INFO] 开始解析公司信息并生成 landscape.yml")

    category_map = {}
    landscape_data = []

    for filename in os.listdir(company_dir):
        if filename.endswith(".md") or filename.endswith(".txt"):
            file_path = os.path.join(company_dir, filename)

            content = {}
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip().replace("：", ":")
                    if ":" in line:
                        key, value = line.split(":", 1)
                        content[key.strip()] = value.strip()

            # 提取字段
            company_name = content.get("名称", "未知公司")
            raw_description = content.get("描述", "")
            founded_year = content.get("成立时间", "")
            homepage_url = ensure_protocol(content.get("官网网站", ""))  # 添加协议头
            first_category = content.get("一级分类", "其他")
            second_category = content.get("二级分类", "其他")
            display_size = content.get("展示大小", "").strip()
            display_priority_str = content.get("展示优先级", "").strip()

            display_priority = None
            if display_priority_str.isdigit():
                num = int(display_priority_str)
                if 1 <= num <= 5:
                    display_priority = num

            description_parts = []
            if raw_description:
                description_parts.append(raw_description)
            else:
                description_parts.append("科技公司")
            if founded_year:
                description_parts.append(f"成立于 {founded_year}")
            description = "，".join(description_parts)

            logo_filename = None
            for logo in os.listdir(logos_dir):
                if logo.lower().endswith((".svg", ".png", ".jpg")):
                    if company_name in logo or logo.replace(".svg", "") in company_name:
                        logo_filename = logo
                        break

            item_data = {
                "name": company_name,
                "homepage_url": homepage_url,
                "logo": logo_filename if logo_filename else "",
                "description": description
            }

            if display_size == "大" and display_priority is not None:
                item_data["project"] = f"level{display_priority}"

            if first_category not in category_map:
                category_map[first_category] = {}
            if second_category not in category_map[first_category]:
                category_map[first_category][second_category] = {"large_items": [], "small_items": []}

            if display_size == "大" and display_priority is not None:
                category_map[first_category][second_category]["large_items"].append(item_data)
            elif display_size == "小":
                category_map[first_category][second_category]["small_items"].append({
                    "item": item_data,
                    "priority": display_priority
                })
            else:
                category_map[first_category][second_category]["small_items"].append({
                    "item": item_data,
                    "priority": None
                })

    for first_cat, subcats in category_map.items():
        category_entry = {
            "name": first_cat,
            "subcategories": []
        }
        for second_cat, items_dict in subcats.items():
            subcategory_entry = {
                "name": second_cat,
                "items": []
            }

            large_items = sorted(
                items_dict["large_items"],
                key=lambda x: int(x.get("project", "level5").replace("level", ""))
            )

            small_items_sorted = sorted(
                [item for item in items_dict["small_items"] if item["priority"] is not None],
                key=lambda x: x["priority"]
            )
            small_items_invalid = [item for item in items_dict["small_items"] if item["priority"] is None]

            subcategory_entry["items"].extend(large_items)
            subcategory_entry["items"].extend([item["item"] for item in small_items_sorted])
            subcategory_entry["items"].extend([item["item"] for item in small_items_invalid])

            category_entry["subcategories"].append(subcategory_entry)
        landscape_data.append({
            "category": category_entry
        })

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump({"landscape": landscape_data}, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"[INFO] landscape.yml 已成功生成：{output_file}\n")


def run_generate_landscape():
    print("[ACTION] 正在执行：生成 landscape.yml")
    generate_landscape_yaml("company", "logos", "landscape.yml")
    print("[ACTION] landscape.yml 生成完毕\n")


# ========================
# 主程序入口
# ========================

def main():
    print("========== 开始执行：生成企业图谱流程 ==========\n")

    # Step 1: 图片转 SVG
    success = run_image_conversion()
    if not success:
        print("[ERROR] 图片转换失败，终止流程")
        return

    # Step 2: 生成 YML
    run_generate_landscape()

    print("========== 流程执行完毕：企业图谱已就绪 ==========")


if __name__ == "__main__":
    main()