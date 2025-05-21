import json
from pathlib import Path
from datetime import datetime
import subprocess
from typing import List, Set
import requests
from PIL import Image
from io import BytesIO
import base64
import os


BASE_DIR = Path(__file__).parent.resolve()
COMPANY_BASE = BASE_DIR / "company"  
LOG_FILE = BASE_DIR / "process.log"

def generate_markdown(item: dict) -> str:
    """生成Markdown文件内容"""
    return f"""
名称: {item['name']}
描述: {item['description']}
成立时间: {item['creation_time']}
网站：{item['website']}
"""

def safe_filename(name: str) -> str:
    """生成安全文件名"""
    return "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in name).strip()

def get_all_company_dirs() -> List[Path]:
    """获取所有需要处理的公司目录路径（两层分类结构）"""
    company_dirs = []
    # 遍历所有分类/子分类/公司目录
    for dir_path in COMPANY_BASE.glob("*/*/*"):  # 匹配 category/subcategory/company_name
        if dir_path.is_dir():
            company_dirs.append(dir_path)
    return company_dirs

def is_company_valid(company_dir: Path) -> bool:
    """验证公司目录是否包含必要文件"""
    required_files = {
        f"{company_dir.name}.md",
        f"{company_dir.name}.svg"
    }
    existing_files = {f.name for f in company_dir.iterdir()}
    return required_files.issubset(existing_files)

def process_logo(logo_url: str, company_dir: Path):
    """处理公司logo并生成SVG文件"""
    try:
        # 下载原始图片
        response = requests.get(logo_url, timeout=15)
        img = Image.open(BytesIO(response.content))
        
        # 生成Base64编码的SVG
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" 
                          width="{img.width}" 
                          height="{img.height}">
            <image href="data:image/png;base64,{base64.b64encode(response.content).decode('utf-8')}"/>
        </svg>'''
        
        with open(company_dir / f"{company_dir.name}.svg", 'w', encoding='utf-8') as f:
            f.write(svg_content)
        return True
    except Exception as e:
        log(f"LOGO处理失败 {company_dir.name}: {str(e)}")
        return False

def convert_images_to_svg(company_dir: Path):
    """将公司目录中的所有图片转换为SVG格式"""
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    converted_count = 0
    
    for file in company_dir.iterdir():
        if file.is_file() and file.suffix.lower() in image_extensions:
            try:
                # 打开图片
                img = Image.open(file)
                
                # 创建Base64编码的SVG
                with open(file, 'rb') as f:
                    img_data = f.read()
                
                svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" 
                                  width="{img.width}" 
                                  height="{img.height}">
                    <image href="data:image/{file.suffix[1:]};base64,{base64.b64encode(img_data).decode('utf-8')}"/>
                </svg>'''
                
                # 生成SVG文件名（保持原文件名，替换扩展名）
                svg_filename = file.with_suffix('.svg').name
                svg_path = company_dir / svg_filename
                
                # 保存SVG文件
                with open(svg_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                
                converted_count += 1
                log(f"成功转换图片: {file.name} -> {svg_filename}")
            except Exception as e:
                log(f"图片转换失败: {file.name} - {str(e)}")
    
    return converted_count

def process_company_data(company_dir: Path, data: dict):
    """处理爬取数据并生成文件"""
    try:
        # 确保目录存在
        company_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成Markdown文件
        md_content = generate_markdown(data)
        with open(company_dir / f"{company_dir.name}.md", 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # 处理logo
        if data.get('logo_url'):
            return process_logo(data['logo_url'], company_dir)
        return True
    except Exception as e:
        log(f"文件生成失败 {company_dir.name}: {str(e)}")
        return False

def fetch_company_data(company_dir: Path) -> bool:
    """执行爬虫任务"""
    company_name = company_dir.name
    scrapy_project_path = BASE_DIR.parent / "scrapy"
    
    try:
        result = subprocess.run(
            [
                "scrapy", 
                "crawl",
                "company_spider",  
                "-a",
                f"company_name={company_name}",
                "-o",
                "temp.json",
                "--loglevel=INFO"  
            ],
            capture_output=True,
            text=True,
            cwd=scrapy_project_path, 
            timeout=300
        )
        print(f"{result}")
        # 结果处理逻辑保持原有不变
        if result.returncode == 0:
            temp_file = scrapy_project_path / "temp.json"
            with open(temp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)[0]
            
            success = process_company_data(company_dir, data)
            temp_file.unlink()
            return success
        else:
            error_msg = f"爬虫失败: {company_name}\nSTDERR: {result.stderr}\nSTDOUT: {result.stdout}"
            log(error_msg)
            return False
    except subprocess.TimeoutExpired:
        log(f"爬虫超时: {company_name}（超过5分钟）")
        return False
    except Exception as e:
        log(f"系统异常: {company_name} - {str(e)}")
        return False

def log(message: str):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

def main():
    """主程序逻辑"""
    # 获取所有公司目录
    all_company_dirs = get_all_company_dirs()
    
    print(f"发现 {len(all_company_dirs)} 个公司目录")
    
    # 步骤1：先转换所有图片为SVG
    total_converted = 0
    for company_dir in all_company_dirs:
        converted_count = convert_images_to_svg(company_dir)
        total_converted += converted_count
    
    print(f"已完成图片转换，共转换 {total_converted} 个图片文件")
    
    # 步骤2：筛选需要处理的目录
    process_list = [d for d in all_company_dirs if not is_company_valid(d)]
    
    print(f"总公司目录数: {len(all_company_dirs)}")
    print(f"需要处理数: {len(process_list)}")
    
    # 处理每个需要更新的公司
    for company_dir in process_list:
        print(f"正在处理: {company_dir.name}")
        if fetch_company_data(company_dir):
            log(f"成功更新: {company_dir.name}")
        else:
            log(f"更新失败: {company_dir.name}")
            
if __name__ == "__main__":
    main()