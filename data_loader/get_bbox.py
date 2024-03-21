import cv2
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import numpy as np
import matplotlib.pyplot as plt
from pdf2image import convert_from_path
 
image_path = 'literature.pdf'
 
layout_type = ['LTTextBox', 'LTFigure', 'LTImage', 'LTCurve', 'LTRect']
# Text：红色， Figure：绿色， Image：蓝色， Curve：黄色， Rect：紫色
color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (160, 32, 240)]
 
draw_color = dict(zip(layout_type, color))
 
 
def parse_obj(lt_objs):
 
    boxs = {x: [] for x in layout_type}
    # loop over the object list
    for obj in lt_objs:
 
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            boxs['LTTextBox'].append(obj.bbox)
        elif isinstance(obj, pdfminer.layout.LTFigure):
            boxs['LTFigure'].append(obj.bbox)
        elif isinstance(obj, pdfminer.layout.LTImage):
            boxs['LTImage'].append(obj.bbox)
        elif isinstance(obj, pdfminer.layout.LTCurve):
            boxs['LTCurve'].append(obj.bbox)
        elif isinstance(obj, pdfminer.layout.LTRect):
            boxs['LTRect'].append(obj.bbox)
        else:
            raise
    return boxs
 
 
# Open a PDF file.
fp = open(image_path, 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
# Supply the password for initialization.
password = '123'
document = PDFDocument(parser, password)
# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
 
# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
 
page_boxs = []
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()
    # extract text from this object
    boxs = parse_obj(layout._objs)
    page_sized = tuple([round(i) for i in layout.bbox])
    page_boxs.append((page_sized, boxs))
    pass
 
image = convert_from_path(image_path)
 
assert len(image) == len(page_boxs), "The number of boxes doesn't match the number of pictures"
for i in range(len(image)):
    # 得到这一页图片
    image_pil = image[i]
    # 把这一页的图片格式转成numpy类型
    image_numpy = np.array(image_pil)
    # 得到这一页图片德国高度，为了之后得到实际的box
    page_boxs_height = page_boxs[i][0][3]
    print(page_boxs[i][1])
 
    # 遍历这一页的框
    for key, values in page_boxs[i][1].items():
        # 把实际的图片大小resize到页面的大小
        image_numpy = cv2.resize(image_numpy, page_boxs[i][0][2:4], interpolation=cv2.INTER_AREA)
        for value in values:
            # The y-coordinates are given as the distance from the bottom of the page.
            real_box = (value[0], page_boxs_height-value[3], value[2], page_boxs_height-value[1])
            real_box_integer = tuple([round(jj) for jj in real_box])
            # 画图
            cv2.rectangle(image_numpy, real_box_integer[:2], real_box_integer[2:], draw_color[key], 2)
    plt.figure(), plt.imshow(image_numpy)
    plt.show()
