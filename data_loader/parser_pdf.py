from io import BytesIO
from pathlib import Path

import cv2
import fitz
import PyPDF2
import pdfplumber

# fnm = '/Users/longfellow/Downloads/水利/节约用水__严格管水_本报记者__孙宇__牛思明.pdf'
fnm = '/Users/longfellow/Downloads/水利/农田水利河道治理护岸防护施工技术思考探讨_韩鹏程.pdf'
# fnm = '/Users/longfellow/Downloads/水利/供水工程影响下中国北方地区耕地后备资源开发潜力_李溦.pdf'


pdf = pdfplumber.open(fnm) if isinstance(fnm, str) else pdfplumber.open(BytesIO(fnm))

for page in pdf.pages:
    text = page.extract_text(layout=True)
    print(text)
    print('------------')

exit()

def test_pypdf2():
    with open(fnm, 'rb') as pdf_file:
        pdf = PyPDF2.PdfReader(pdf_file, strict=False)
        for page in pdf.pages:
            text = page.extract_text()
            print(text)
            print('--'*10)


test_pypdf2()