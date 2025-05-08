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