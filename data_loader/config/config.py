"""
"""
import os
from typing import Dict

def get_files(dir_path: str) -> Dict:
    '''
    获取 dir_path 文件夹中的文档
    '''
    # args：dir_path，目标文件夹路径
    file_map = {}
    for root, _, files in os.walk(dir_path):
        for file in files:
            # 文件绝对路径
            file_path = os.path.join(root, file)
            # 文件所在文件夹路径
            folder_path = os.path.relpath(root, dir_path)

            file_map.setdefault(folder_path, []).append(file_path)

    return file_map
