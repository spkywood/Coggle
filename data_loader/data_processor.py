from config import get_files, process_document
import os

from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
from pdfminer.pdfparser import PDFSyntaxError
import pdfplumber
import re
import pandas as pd 
from tqdm import tqdm


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.layout import LTTextBoxHorizontal

DATA_BASE = "/home/wangxh/dataDownload"

file_list = get_files(DATA_BASE)

pattern = r'-\s*\d+\s*-'    # 匹配删除 页码 - \d+ - 

for key, values in file_list.items():
    os.makedirs(os.path.join('./output', key), exist_ok=True)

    # 处理读取pdf，并保存在output文件中
    for file in values:
        print(file)
        document = process_document(file)
        content = ""
        for k, v in document.items():
            v = re.sub(pattern, '', v)
            content+=v
        
        txt = '/'.join(file.split('/')[-2:]).replace('.pdf', '.txt')
        txt_filename = os.path.join('./output', txt)
        
        if not os.path.exists(txt_filename):
            with open(txt_filename, '+w') as fout:
                fout.write(content)
        # break
    break

# doc = process_document('/home/wangxh/dataDownload/中央水利建设投资统计月报/中央水利建设投资统计月报（2023-12）.pdf')
# content = ""
# for k, v in doc.items():
#     v = re.sub(pattern, '', v)
#     content+=v

# print(content)