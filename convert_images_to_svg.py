import os
import base64
from pathlib import Path
from PIL import Image

def convert_images_to_svg(input_dir: Path, output_dir: Path):
    """
    将指定目录中的所有图片转换为SVG格式并保存到输出目录
    :param input_dir: 包含原始图片的目录
    :param output_dir: 保存SVG文件的目标目录
    :return: 转换的文件数量
    """
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.jpeg', '.webp']
    converted_count = 0

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    for file in input_dir.iterdir():
        if file.is_file() and file.suffix.lower() in image_extensions:

            svg_path = output_dir / file.with_suffix('.svg').name

            # 检查是否需要跳过已存在的文件
            if svg_path.exists():
                print(f"跳过已存在的文件: {svg_path.name}")
                continue

            try:
                # 打开图片获取尺寸
                img = Image.open(file)

                # 转换为RGBA格式以处理alpha通道
                img = img.convert("RGBA")
                # 获取图片数据
                datas = img.getdata()
                # 创建新的像素数据列表
                new_data = []
                # 白色阈值 - 值越低，只有更接近纯白色的像素才会被转换
                white_threshold = 240
                # 处理每个像素
                for item in datas:
                    # 如果像素是白色或接近白色，则将其设为透明
                    if item[0] > white_threshold and item[1] > white_threshold and item[2] > white_threshold:
                        new_data.append((0, 0, 0, 0))
                    else:
                        new_data.append(item)  # 保留原始像素
                # 应用新的像素数据
                img.putdata(new_data)
                # 创建临时文件保存处理后的图片
                temp_file = Path("temp_image.png")
                img.save(temp_file, "PNG")

                # 读取图片数据
                with open(temp_file, 'rb') as f:
                    img_data = f.read()
                
                # 构建Base64编码的SVG内容
                svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{img.width}" height="{img.height}">
    <image href="data:image/{file.suffix[1:]};base64,{base64.b64encode(img_data).decode('utf-8')}"/>
</svg>'''

                # 构造SVG文件路径
                svg_filename = file.with_suffix('.svg').name
                svg_path = output_dir / svg_filename

                # 写入SVG文件
                with open(svg_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)

                print(f"成功转换图片: {file.name} -> {svg_filename}")
                converted_count += 1
            except Exception as e:
                print(f"图片转换失败: {file.name} - {str(e)}")
                if temp_file.exists():
                    temp_file.unlink()

    return converted_count

def main():
    # 定义根目录、输入目录和输出目录
    root_dir = Path.cwd()
    input_dir = root_dir / "company" / "logos"
    output_dir = root_dir / "logos"

    # 检查输入目录是否存在
    if not input_dir.exists():
        print(f"错误：输入目录 {input_dir} 不存在")
        return

    # 调用转换函数
    total_converted = convert_images_to_svg(input_dir, output_dir)

    # 输出总计
    print(f"已完成图片转换，共转换 {total_converted} 个图片文件")

if __name__ == "__main__":
    main()