from paddleocr import PaddleOCR
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from paddleocr import PaddleOCR, draw_ocr
font=cv2.FONT_HERSHEY_SIMPLEX

# Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
# 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
ocr = PaddleOCR(use_angle_cls=True, lang="ch",
                rec_model_dir='E:\copy1_msk\H_SLYT_s_programs\project\paddleOCR\PaddleOCR\inference\det\\',
                cls_model_dir='E:\copy1_msk\H_SLYT_s_programs\project\paddleOCR\PaddleOCR\inference\det\ch_ppocr_mobile_v2.0_cls_infer\\',
                det_model_dir='E:\copy1_msk\H_SLYT_s_programs\project\paddleOCR\PaddleOCR\inference\det\ch_PP-OCRv3_det_infer\\') # need to run only once to download and load model into memory

img_path = r'E:\\copy1_msk\\H_SLYT_s_programs\\project\\projectBackup\\AreaTextTool\\test1.jpg'
result = ocr.ocr(img_path, cls=True)
# print结果
# print(result)
# print(">>>>>>>>>>>>>>>>>>>>")
# counter=0
# for line in result:
#     if counter==0:
#         print(line)
#         print(line[0])
#         print(line[1][0])
#         print(line[1][1])
#         print(line[1][1][1])
#     counter+=1
# print(counter)
img=cv2.imread(img_path)
for x in result:
    boxes = [line[0] for line in x]
    txts = [line[1][0] for line in x]
    scores = [line[1][1] for line in x]
    img = draw_ocr(img, boxes, txts, scores)
    cv2.imshow("result",img)
    cv2.waitKey(0)
print(scores)
# 显示图片结果

