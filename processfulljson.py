import json
import re

def remove_prefix(name):
    # 如果名称前5个字符中有英文或数字，去掉这些前缀
    if len(name) >= 5 and not all('\u4e00' <= char <= '\u9fff' for char in name[:5]):
        # 找到第一个中文字符的位置
        first_chinese_index = next((i for i, char in enumerate(name[:5]) if '\u4e00' <= char <= '\u9fff'), 0)
        return name[first_chinese_index:]
    return name

def process_json_file(file_path):
    try:
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 遍历所有items中的对象
        for item in data.get('items', []):
            if 'name' in item:
                original_name = item['name']
                # 检查名称中是否包含中文
                if re.search(r'[\u4e00-\u9fff]', original_name):
                    # 处理名称，去除可能的前缀
                    new_name = remove_prefix(original_name)
                    item['name'] = new_name
        
        # 写回修改后的JSON
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            
        print("处理完成，已更新文件")  # 修改这一行，避免使用未定义的变量
    
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    json_file_path = 'build/data/full.json'
    process_json_file(json_file_path)