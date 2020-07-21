# -*- coding = utf-8 -*-
# @Time :2020/7/13 1:19 下午
# @Author: XZL
# @File : draw_selected.py
# @Software: PyCharm
import cv2 as cv
import json
import numpy as np
from PIL import Image, ImageFont, ImageDraw

# json.dump()  把数据写入json文件
# json.load()  把json文件内容读入python
font_path = '/Users/apple/Documents/开发/资源/simsun.ttc'
font = ImageFont.truetype(font_path, 20)  # 加载字体, 字体大小


def adapt_threshold_demo(img):  # 全局的二值化
    # 自适应的局部阈值二值化
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    dst = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv.THRESH_BINARY, 25, 10)
    return dst


# 灰度化
def gray(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)


# 解析json数据
def analyze_json(json_data):
    text_detection = json_data.get('TextDetections')  # list -> dict(多个)
    draw_info = []
    for i in text_detection:
        add_conf = {}
        add_con = {}
        content = i.get('DetectedText')  # 内容
        confidence = i.get('Confidence')  # 置信度
        pos_list = i.get('Polygon')  # 位置信息(内含4个坐标点)
        add_conf['confidence'] = confidence
        add_con['content'] = content
        pos_list.append(add_conf)
        pos_list.append(add_con)
        draw_info.append(pos_list)
        print("内容:%s  置信度:%s  " % (content, confidence))
        # for p in pos_list:
        #     print("X:%s Y:%s " % (p.get('X'), p.get('Y')))
    return draw_info


def draw_location_tr(image, draw_info):
    draw_image = image.copy()  # 图像副本
    # 绘制识别选框
    for p in draw_info:
        for i in range(3):
            cv.line(draw_image, (int(p[i].get('X')), int(p[i].get('Y'))),
                    (int(p[i + 1].get('X')), int(p[i + 1].get('Y'))), (0, 0, 255), 1, lineType=cv.LINE_AA)
        cv.line(draw_image, (p[3].get('X'), p[3].get('Y')),
                (p[0].get('X'), p[0].get('Y')), (0, 0, 255), 1, lineType=cv.LINE_AA)

        # zeros1 = np.zeros(draw_image.shape, dtype=np.uint8)
        # zeros_mask1 = cv.rectangle(zeros1, (int(p[0].get('X')), int(p[0].get('Y'))),
        #                            (int(p[2].get('X')), int(p[2].get('Y'))),
        #                            (255, 0, 0), -1)
        # draw_image = cv.addWeighted(draw_image, 0.6, zeros_mask1, 0.5, 0)
        # 标注置信度
        cv.putText(draw_image, str(p[4].get('confidence')) + '%', (p[0].get('X'), p[0].get('Y')),
                   cv.FONT_HERSHEY_SIMPLEX,
                   0.5, (0, 0, 255), 1, lineType=cv.LINE_AA)
    return draw_image


def put_text(image, draw_info):
    draw_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)  # 图像副本
    img_pil = Image.fromarray(draw_image)
    dr = ImageDraw.Draw(img_pil)
    for p in draw_info:
        dr.text((p[2].get('X'), p[2].get('Y')), str(p[5].get('content')), font=font,
                fill=(0, 0, 255))  # xy坐标, 内容, 字体, 颜色
    cv2charimg = cv.cvtColor(np.array(img_pil), cv.COLOR_RGB2BGR)
    return cv2charimg


img_path = '../images/t_6.jpeg'
json_path = '../json/55.json'
img = cv.imread(img_path, 1)  # blue green red
data = json.load(open(json_path))
coord = analyze_json(data)

cv.namedWindow("draw", 0)
cv.resizeWindow("draw", 1280, 720)
gray_img = gray(img)
d_img = draw_location_tr(img, coord)
f_img = put_text(d_img, coord)
# dst = adapt_threshold_demo(img)
cv.imshow('draw', f_img)
# cv.imwrite('otp.png', f_img, [int(cv.IMWRITE_PNG_COMPRESSION), 0]) #保存图像质量 png 0-9

if cv.waitKey(0) == ord('q'):
    cv.destroyAllWindows()
