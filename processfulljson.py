import json

def remove_prefix(name):
    # 找到第一个中文字符的位置（不限制长度）
    for i, char in enumerate(name):
        if '\u4e00' <= char <= '\u9fff':  # 判断是否为中文字符
            return name[i:]
    return name  # 如果全是非中文字符，返回原名称

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
                if any('\u4e00' <= char <= '\u9fff' for char in original_name):
                    # 处理名称，去除可能的前缀
                    new_name = remove_prefix(original_name)
                    item['name'] = new_name
        
        # 写回修改后的JSON
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            
        print("处理完成，已更新文件")
    
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    json_file_path = 'build/data/full.json'
    process_json_file(json_file_path)