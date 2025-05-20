# import os
# import json
# import requests
# from urllib.parse import urlparse
# from PIL import Image # type: ignore
# from io import BytesIO
# import base64

# class CompanyInfoPipeline:
#     def process_item(self, item, spider):
#         output_dir = os.path.join(os.getcwd(), "output")
#         os.makedirs(output_dir, exist_ok=True)

#         # 保存 JSON 文件
#         self.save_json(item, output_dir)
        
#         # 处理 logo 图片
#         logo_dir = os.path.join(output_dir, "logos")
#         os.makedirs(logo_dir, exist_ok=True)
#         self.process_logo(item, logo_dir, spider)

#         return item

#     def save_json(self, item, output_dir):
#         file_path = os.path.join(output_dir, f"{item['name']}.json")
#         with open(file_path, 'w', encoding='utf-8') as f:
#             json.dump(dict(item), f, ensure_ascii=False, indent=2)

#     def process_logo(self, item, save_dir, spider):
#         try:
#             # 下载原始图片
#             response = requests.get(item['logo_url'], timeout=10)
#             if response.status_code != 200:
#                 raise ValueError(f"HTTP状态码异常: {response.status_code}")

#             # 保存原始图片
#             ext = os.path.splitext(item['logo_url'])[1] or '.ico'
#             original_path = self.save_original_image(response, item['name'], save_dir)
#             item['original_logo_path'] = os.path.basename(original_path)
#             spider.logger.info(f"原始图片已保存：{original_path}")

#             # 转换为SVG
#             svg_path = self.convert_to_svg(response.content, item['name'], save_dir)
#             item['svg_logo_path'] = os.path.basename(svg_path)
#             spider.logger.info(f"SVG图片已保存：{svg_path}")

#         except Exception as e:
#             spider.logger.error(f"图片处理失败：{str(e)}")
#             raise

#     def save_original_image(self, response, company_name, save_dir):
#         content_type = response.headers.get('content-type', '')
#         ext = 'bin'
        
#         # 根据Content-Type确定扩展名
#         if '/x-icon' in content_type:
#             ext = 'ico'
#         elif 'image/' in content_type:
#             ext = content_type.split('/')[-1].replace('jpeg', 'jpg')
#         else:
#             #根据URL推断扩展名
#             parsed = urlparse(response.url)
#             ext = os.path.splitext(parsed.path)[1].lstrip('.').lower() or 'ico'

#         filename = f"{company_name}_original.{ext}"
#         path = os.path.join(save_dir, filename)
#         with open(path, 'wb') as f:
#             f.write(response.content)
#         return path

#     def convert_to_svg(self, image_data, company_name, save_dir):
#         try:
#             img = Image.open(BytesIO(image_data))
        
#             # 获取原始尺寸
#             original_width, original_height = img.size
        
#             # 提高分辨率（放大2倍）
#             new_size = (original_width*2, original_height*2)
#             img = img.resize(new_size, Image.Resampling.LANCZOS)
#             buffered = BytesIO()
#             img.save(buffered, format="PNG", dpi=(300, 300))  # 提高保存质量
#             base64_str = base64.b64encode(buffered.getvalue()).decode()
        
#             # 使用原始尺寸+放大后的尺寸组合
#             final_width = original_width * 2
#             final_height = original_height * 2
        
#             svg_filename = f"{company_name}.svg"
#             svg_path = os.path.join(save_dir, svg_filename)
        
#             with open(svg_path, 'w') as f:
#                 f.write(self._create_svg_wrapper(
#                     base64_str,
#                     final_width,
#                     final_height
#                 ))
        
#             return svg_path

#         except Exception as e:
#             raise ValueError(f"SVG转换失败：{str(e)}")
    

#     def _create_svg_wrapper(self, base64_data, company_name, save_dir):
#         width, height = 500, 500  
#         return f'''\
# <svg xmlns="http://www.w3.org/2000/svg" 
#      width="{width}" 
#      height="{height}"
#      viewBox="0 0 {width} {height}">
#     <image href="data:image/png;base64,{base64_data}" 
#            x="0" 
#            y="0" 
#            width="{width}" 
#            height="{height}"/>
# </svg>'''
    
 
 
 # pipelines.py 完整修改版
import os
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import base64

class CompanyFilesPipeline:
    def process_item(self, item, spider):
        # 构建公司目录路径
        company_dir = Path(spider.settings.get('FILES_STORE')) / item['name']
        company_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成Markdown文件
        self.generate_markdown(item, company_dir)
        
        # 处理Logo文件
        if item.get('logo_url'):
            self.process_logo(item, company_dir, spider)
        
        return item

    def generate_markdown(self, item, company_dir):
        """生成标准Markdown文件"""
        content = f"""# {item['name']}
        
**官方网站**: [{item['website']}]({item['website']})
**成立时间**: {item['creation_time']}
**公司简介**: {item['description'] or "暂无信息"}

![公司Logo](./{item['name']}.svg)
"""
        with open(company_dir / f"{item['name']}.md", 'w', encoding='utf-8') as f:
            f.write(content)

    def process_logo(self, item, company_dir, spider):
        """处理Logo转换逻辑"""
        try:
            # 下载原始图片
            response = requests.get(item['logo_url'], timeout=10)
            response.raise_for_status()
            
            # 保存并转换SVG
            img = Image.open(BytesIO(response.content))
            self.generate_svg(img, item['name'], company_dir)
            
        except Exception as e:
            spider.logger.error(f"Logo处理失败: {str(e)}")
            raise

    def generate_svg(self, image, company_name, company_dir):
        """生成SVG文件"""
        # 将图片转换为Base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        base64_str = base64.b64encode(buffered.getvalue()).decode()
        
        # SVG模板
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" 
            width="{image.width}" 
            height="{image.height}"
            viewBox="0 0 {image.width} {image.height}">
            <image href="data:image/png;base64,{base64_str}" 
                width="100%" 
                height="100%"/>
        </svg>'''
        
        with open(company_dir / f"{company_name}.svg", 'w') as f:
            f.write(svg_content)