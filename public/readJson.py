import json
import os

def json_to_txt(input_file, output_file):
    try:
        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"输入文件 {input_file} 未找到")

        # 读取 JSON 文件
        with open(input_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)  # [3,5](@ref)

        # 写入 TXT 文件（带格式化）
        with open(output_file, 'w', encoding='utf-8') as txt_file:
            json.dump(data, txt_file, indent=4, ensure_ascii=False)  # [1,3,4](@ref)
            print(f"数据已成功写入 {output_file}")

    except json.JSONDecodeError as e:
        print(f"JSON 格式错误: {e}")  # [3](@ref)
    except IOError as e:
        print(f"文件操作失败: {e}")  # [1,8](@ref)
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 company.json 文件的路径
    input_json = os.path.join(script_dir, 'company.json')
    output_txt = os.path.join(script_dir, 'a.txt')
    json_to_txt(input_json, output_txt)


# import json
# import os
# import subprocess  # 新增：用于调用Scrapy命令行
# from pathlib import Path  # 新增：处理路径更安全

# def json_to_txt(input_file, output_file):
#     try:
#         with open(input_file, 'r', encoding='utf-8') as json_file:
#             data = json.load(json_file)
#         with open(output_file, 'w', encoding='utf-8') as txt_file:
#             json.dump(data, txt_file, indent=4, ensure_ascii=False)
#         print(f"数据已成功写入 {output_file}")
#     except Exception as e:
#         print(f"处理数据时出错: {e}")

# def run_scrapy_spider():
#     script_dir = Path(os.path.abspath(__file__)).parent
#     output_json = script_dir / "company.json"
    
#     # 清理旧文件
#     if output_json.exists():
#         output_json.unlink()
    
#     # 通过subprocess调用Scrapy命令行
#     try:
#         result = subprocess.run(
#             ["scrapy", "crawl", "company_spider", "-a", str(output_json)],
#             capture_output=True,
#             text=True,
#             check=True
#         )
#         print("爬虫输出:", result.stdout)
#     except subprocess.CalledProcessError as e:
#         print(f"爬虫运行失败: {e.stderr}")
#         raise  
    
# if __name__ == "__main__":
#     try:
#         # 运行爬虫
#         run_scrapy_spider()
        
#         # 步骤2：处理生成的JSON文件
#         script_dir = Path(os.path.abspath(__file__)).parent
#         input_json = script_dir / "company.json"
#         output_txt = script_dir / "a.txt"
        
#         json_to_txt(input_json, output_txt)
        
#     except Exception as e:
#         print(f"整体流程失败: {e}")