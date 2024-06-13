import fitz  # PyMuPDF
import json
 
def is_table_block(b1, b2):
    # 检查连续相邻的文本块是否具有相同的行数，并且其 bbox 的高度也相同
    if len(b1["lines"]) == len(b2["lines"]) and b1["bbox"][3] - b1["bbox"][1] == b2["bbox"][3] - b2["bbox"][1]:
        return True
    return False
 
def extract_text_blocks(pdf_path):
    # 打开 PDF 文件
    pdf_document = fitz.open(pdf_path)
    
    # 存储文本块信息
    text_blocks = []
    line_blocks = []
    
    # 遍历 PDF 中的每一页
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        
        # 获取文本块和行块信息
        blocks = page.get_text("dict")["blocks"]
        
        # 对当前页面内的文本块按照坐标进行排序
        blocks.sort(key=lambda x: (x['bbox'][3], x['bbox'][0]))
        
        for i in range(len(blocks)):
            lines = blocks[i].get("lines")
            if lines is None:
                continue

            for line in lines:
                spans = line["spans"]
                for span in spans:
                    print(f"page {page_number} \001 {i} \001 {span['text']}")
                print('-----------------------')
                line_blocks.append({
                    "line": line["spans"],
                    "bbox": line["bbox"],
                    "height": line["bbox"][3] - line["bbox"][1],  # 计算行块的高度
                    "page_number": page_number + 1  # 记录页码信息
                })
            text_blocks.append({
                "block": lines,
                "bbox": blocks[i]["bbox"],
                "page_number": page_number + 1  # 记录页码信息
            })
    
    # 关闭 PDF 文件
    pdf_document.close()
    
    return text_blocks, line_blocks
 
def is_same_paragraph(line1, line2):
    # 判断相邻行是否属于同一个段落的逻辑
    # 这里提供一个简单的示例，你可以根据实际情况调整和扩展
    
    # 判断两行之间的垂直间距是否小于某个阈值
    vertical_threshold = 5  # 垂直间距阈值，根据实际情况调整
    if abs(line1['bbox'][3] - line2['bbox'][1]) < vertical_threshold:
        return True
    
    return False
 
# 示例用法
 

# pdf_path = '/Users/longfellow/Downloads/水利/节约用水__严格管水_本报记者__孙宇__牛思明.pdf'
pdf_path = '/Users/longfellow/Downloads/水利/抗御永定河特大洪水的实践与思考_孙国升.pdf'
# pdf_path = '/Users/longfellow/Downloads/水利/供水工程影响下中国北方地区耕地后备资源开发潜力_李溦.pdf'


text_blocks, line_blocks = extract_text_blocks(pdf_path)
 
exit()
# 用于检查两个文本块中的行是否相同
def check_lines_same(block1, block2):
    num_lines_block1 = len(block1["block"])
    num_lines_block2 = len(block2["block"])
    return num_lines_block1 == num_lines_block2
 
# 收集打印的 JSON
printed_json_list = []
 
for index, block in enumerate(text_blocks):
    # 获取当前文本块中行的个数
    num_lines = len(block["block"])
    
    # 如果当前文本块是表格，则继续检查下一个文本块是否是表格
    if num_lines > 1 and index < len(text_blocks) - 1:  # 需要多于一行，并且不是最后一个文本块
        next_block = text_blocks[index + 1]
        if check_lines_same(block, next_block):
            # 如果下一个文本块也是表格，则跳过，不进行打印输出
            continue
    
    # 如果当前文本块不是表格，则添加到打印的 JSON 列表中
    block_info = {
        "block_index": index + 1,
        "page_number": block['page_number'],
        "lines": [line['spans'] for line in block['block']],
        "bbox": block['bbox']
    }
    # print(block_info)
    printed_json_list.append(block_info)
 
previous_json = None  # 用于记录上一个非空 JSON
 
for printed_json in printed_json_list:
    # 获取 lines 的最后一个对象
    last_line_array = printed_json["lines"][-1]
 
    # 获取最后一个对象中的最后一个对象
    last_object_in_last_line = last_line_array[-1]
 
    # 获取最后一个对象中的 text 字段的值
    text_value = last_object_in_last_line["text"]
    # 输出截取到的最后一个text值
    #print("text字段的取值为>>>>>>>>>>>>..:", text_value)
 
    if text_value.strip() == "":
        # 如果 text_value 为空，则打印当前 JSON
        if previous_json is not None:
            # 合并当前 JSON 到上一个非空 JSON 上
            previous_json["lines"].extend(printed_json["lines"])
            previous_json["bbox"] = [min(previous_json["bbox"][0], printed_json["bbox"][0]),
                                     min(previous_json["bbox"][1], printed_json["bbox"][1]),
                                     max(previous_json["bbox"][2], printed_json["bbox"][2]),
                                     max(previous_json["bbox"][3], printed_json["bbox"][3])]
            # 更新页码信息
            previous_json["page_number"] = printed_json["page_number"]
 
            # print(json.dumps(previous_json, ensure_ascii=False))
            
             # 重置json
            previous_json = None
        # else:
            # print(json.dumps(printed_json, ensure_ascii=False))
        lines = printed_json["lines"]
        
        for line in lines:

            # print(json.dumps(line, ensure_ascii=False))
            for ll in lines:
                text = "" 
                for l in ll:
                # print(l)
                    text += l.get("text", "")
                print(text)
                print('--------')
    else:
        # 如果 text_value 不为空，则合并当前 JSON 到上一个非空 JSON 上
        if previous_json is not None:
            # 合并当前 JSON 到上一个非空 JSON 上
            previous_json["lines"].extend(printed_json["lines"])
            previous_json["bbox"] = [min(previous_json["bbox"][0], printed_json["bbox"][0]),
                                     min(previous_json["bbox"][1], printed_json["bbox"][1]),
                                     max(previous_json["bbox"][2], printed_json["bbox"][2]),
                                     max(previous_json["bbox"][3], printed_json["bbox"][3])]
            # 更新页码信息
            previous_json["page_number"] = printed_json["page_number"]
        else:
            # 如果没有上一个非空 JSON，则将当前 JSON 赋值给上一个非空 JSON
            previous_json = printed_json
 
