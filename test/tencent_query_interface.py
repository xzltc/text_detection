# -*- coding = utf-8 -*-
# @Time :2020/7/13 9:56 上午
# @Author: XZL
# @File : tencent_query_interface.py
# @Software: PyCharm

# SecretId:AKIDwdGfopwkR6VYO04bXCbia4IJD43wOCH7
# SecretKey:XcXAWcSWaFl0yhYDdnLdeQXquiHYT8Yl

"""腾讯OCR识别服务接口"""
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
from PIL import Image, ImageFont, ImageDraw
import base64
import cv2 as cv
import numpy as np


def recognition():
    try:
        # 生成证书
        cred = credential.Credential("AKIDwdGfopwkR6VYO04bXCbia4IJD43wOCH7", "XcXAWcSWaFl0yhYDdnLdeQXquiHYT8Yl")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        # 初始化客户端实例
        clientProfile = ClientProfile("TC3-HMAC-SHA256")
        # 按就近的使用，所以我用的是ap-shanghai
        client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

        req = models.GeneralAccurateOCRRequest()

        with open("../images/t_2.jpeg", 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data
        params = '{"ImageBase64":"' + str(s, 'utf-8') + '"}'
        req.from_json_string(params)

        resp = client.GeneralAccurateOCR(req)
        result = resp.TextDetections
        # 将官网文档里输出字符串格式的转换为字典，如果不需要可以直接print(resp)
        return result

    except TencentCloudSDKException as err:
        print(err)


def formate_data(data):
    # text_detection = data.get('TextDetections')  # list -> dict(多个)
    formated_data = []
    out_put = []
    for i in data:
        add_conf = {}
        add_con = {}
        content = i.DetectedText  # 内容
        confidence = i.Confidence  # 置信度
        pos_list = i.Polygon  # 位置信息(内含4个坐标点)
        add_conf['confidence'] = confidence
        add_con['content'] = content

        out_put.append(content)

        pos_list.append(add_conf)
        pos_list.append(add_con)
        formated_data.append(pos_list)
        print("内容:%s  置信度:%s  " % (content, confidence))
    print(out_put)
    return formated_data


def draw_location_tr(image, draw_info):
    draw_image = image.copy()  # 图像副本
    # 绘制识别选框
    for p in draw_info:
        for i in range(3):
            cv.line(draw_image, (int(p[i].X), int(p[i].Y)),
                    (int(p[i + 1].X), int(p[i + 1].Y)), (0, 0, 255), 1, lineType=cv.LINE_AA)
        cv.line(draw_image, (p[3].X, p[3].Y),
                (p[0].X, p[0].Y), (0, 0, 255), 1, lineType=cv.LINE_AA)
        # 标注置信度
        cv.putText(draw_image, str(p[4].get('confidence')) + '%', (p[0].X, p[0].Y),
                   cv.FONT_HERSHEY_SIMPLEX,
                   0.5, (0, 0, 255), 1, lineType=cv.LINE_AA)
    return draw_image


def put_text(image, draw_info):
    font_path = '/Users/apple/Documents/开发/资源/simsun.ttc'
    font = ImageFont.truetype(font_path, 20)  # 加载字体, 字体大小
    draw_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)  # 图像副本
    img_pil = Image.fromarray(draw_image)
    dr = ImageDraw.Draw(img_pil)
    for p in draw_info:
        dr.text((p[2].X, p[2].Y), str(p[5].get('content')), font=font,
                fill=(0, 0, 255))  # xy坐标, 内容, 字体, 颜色
    cv2charimg = cv.cvtColor(np.array(img_pil), cv.COLOR_RGB2BGR)
    return cv2charimg


if __name__ == '__main__':
    ret = recognition()
    fd = formate_data(ret)
    img_path = '../images/t_2.jpeg'
    img = cv.imread(img_path, 1)  # blue green red

    cv.namedWindow("draw", 0)
    cv.resizeWindow("draw", 1280, 720)
    d_img = draw_location_tr(img, fd)
    f_img = put_text(d_img, fd)
    cv.imshow('draw', f_img)

    if cv.waitKey(0) == ord('q'):
        cv.destroyAllWindows()
