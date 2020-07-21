# -*- coding = utf-8 -*-
# @Time :2020/7/14 4:23 下午
# @Author: XZL
# @File : baidu_query_interface.py
# @Software: PyCharm
from aip import AipOcr
import cv2 as cv
import numpy as np

"""  APPID AK SK """
APP_ID = '21334258'
API_KEY = '4ANuB62yAm3Bb3hEWnLlWkbK'
SECRET_KEY = 'RWx0enQkHddlEPGj5V7Gyw0iAQERSpGo'

# 创建客户端实例
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
file_path = '../images/ca.jpeg'


# 读取图片文件
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


# OCR服务 path:图片地址
def ocr_image(path):
    image = get_file_content(path)

    """ 调用通用文字识别（含位置高精度版） """
    client.general(image)
    # client.accurate(image)

    """ 如果有可选参数 """
    options = {}
    options["recognize_granularity"] = "big"
    options["language_type"] = "CHN_ENG"
    # options["detect_language"] = "true"
    options["vertexes_location"] = "true"
    options["probability"] = "true"

    """ 带参数调用通用文字识别（含位置高精度版） """
    res = client.general(image, options)
    # res = client.accurate(image, options)

    output = {'code': 0,
              'text': ''}
    # 出错情况
    if 'error_code' in res:
        output['code'] = 0
        if res['error_code'] == '17':
            output['text'] = "每天流量超限额"
        else:
            output['text'] = '错误代码：{}'.format(res['error_code'])
    # 正常情况
    else:
        print('识别总数为:%d' % res['words_result_num'])
        output['code'] = 1
        output['result'] = res.get('words_result')  # 所有识别信息塞进字典中
        for elem in res['words_result']:
            print('%s  置信度:%d' % (elem['words'], elem.get('probability')['min'] * 100))
    return output


def draw_location(img, info):
    draw_image = img.copy()
    for elem in info['result']:
        location_lists = elem['finegrained_vertexes_location']
        draw_location_lists = np.empty((1, 2), dtype=np.int32)
        for ll in location_lists:
            e_l = [[ll['x'], ll['y']]]
            ne_l = np.array(e_l)
            draw_location_lists = np.append(draw_location_lists, ne_l, axis=0)
        draw_location_lists = np.array([draw_location_lists], dtype=np.int32)
        cv.fillPoly(draw_image, draw_location_lists, (255, 0, 0))
    return draw_image


# 绘制方框区域
def draw_location_br(img, info):
    draw_image = img.copy()  # 图像副本
    for elem in info['result']:
        b = elem['vertexes_location']
        for i in range(3):
            cv.line(draw_image, (int(b[i].get('x')), int(b[i].get('y'))),
                    (int(b[i + 1].get('x')), int(b[i + 1].get('y'))), (0, 0, 255), 1, lineType=cv.LINE_AA)
        cv.line(draw_image, (b[3].get('x'), b[3].get('y')),
                (b[0].get('x'), b[0].get('y')), (0, 0, 255), 1, lineType=cv.LINE_AA)
        cv.putText(draw_image, str(int(elem.get('probability')['min'] * 100)) + '%', (b[0].get('x'), b[0].get('y')),
                   cv.FONT_HERSHEY_SIMPLEX,
                   0.5, (0, 0, 255), 1, lineType=cv.LINE_AA)
    return draw_image


# 格式化数据,和腾讯接口统一
def formate_data(data):
    result = data.get('result')
    formatted_data = []
    for i in result:
        add_conf = {}
        add_con = {}
        content = i.get('words')  # 内容
        confidence = i.get('probability')['min'] * 100  # 置信度
        pos_list = i.get('vertexes_location')  # 位置信息(内含4个坐标点)
        add_conf['confidence'] = confidence
        add_con['content'] = content
        pos_list.append(add_conf)
        pos_list.append(add_con)
        formatted_data.append(pos_list)
        print("内容:%s  置信度:%s  " % (content, confidence))
    return formatted_data


d_img = cv.imread(file_path, 1)
res = ocr_image(file_path)
f_img = draw_location_br(d_img, res)
formate_data(res)
cv.namedWindow("draw", 0)
cv.resizeWindow("draw", 1280, 720)

cv.imshow('draw', f_img)
cv.imwrite('wb.png', f_img, [int(cv.IMWRITE_PNG_COMPRESSION), 0])  # 保存图像质量 png 0-9
if cv.waitKey(0) == ord('q'):
    cv.destroyAllWindows()
