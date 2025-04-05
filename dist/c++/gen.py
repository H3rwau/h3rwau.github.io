import os

# 获取当前文件夹路径和名称
current_dir = os.getcwd()
folder_name = os.path.basename(current_dir)

# 获取所有文件（排除子目录）
files = [
    f for f in os.listdir(current_dir) 
    if os.path.isfile(os.path.join(current_dir, f))
]

# 生成格式化内容
output_lines = []
for file in files:
    # 去除文件扩展名
    name_without_ext = os.path.splitext(file)[0]
    # 按指定格式生成行
    output_lines.append(f'      - /{folder_name}/{name_without_ext}')

# 写入到新文件（默认命名为file_list.txt）
with open('file_list.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f'文件列表已生成到 {os.path.join(current_dir, "file_list.txt")}')