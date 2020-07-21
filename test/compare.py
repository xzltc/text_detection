# -*- coding = utf-8 -*-
# @Time :2020/7/21 1:31 下午
# @Author: XZL
# @File : compare.py
# @Software: PyCharm
from excel_handle import openpyxl_excel


def Partial(pattern):
    """ 生成next数组"""
    ret = [0]

    for i in range(1, len(pattern)):
        j = ret[i - 1]
        while j > 0 and pattern[j] != pattern[i]:
            j = ret[j - 1]
        ret.append(j + 1 if pattern[j] == pattern[i] else j)
    return ret


def Search(T, P):
    """
    KMP匹配的主要算法 String -> String -> [Int]
    返回所有在T中匹配到的P
    """
    partial, ret, j = Partial(P), [], 0

    for i in range(len(T)):
        while j > 0 and T[i] != P[j]:
            j = partial[j - 1]
        if T[i] == P[j]: j += 1
        if j == len(P):
            ret.append(i - (j - 1))
            j = partial[j - 1]
    return ret


#快速匹配
def pattern_matching(ocr_text, res_data):
    res_length = len(res_data)
    correct_num = 0
    # 匹配算法
    for i in range(len(ocr_text)):
        for j in range(res_length):
            search_res = Search(ocr_text[i], res_data[j])
            if len(search_res):
                print('匹配成功 %s <==> %s' % (ocr_text[i], res_data[j]))
                print('下标:', search_res)
                del name[j]
                res_length -= 1
                correct_num += 1
                break

    print("匹配数:%d 匹配率:%d%%" % (correct_num, ((correct_num / len(ocr_text)) * 100)))


if __name__ == "__main__":
    txt = "东白湖0同山fd"  # 字符串
    pat = "山fd"  # 模式串
    fast_ocr_text = ['漓渚镇', '河上镇@', 'O店口镇之现', '◎常绿镇!', '应店街镇业6', '枫桥镇', '陶朱街道', '德记汉理广国赵家镇',
                     '暨阳街道沈东', '五泄镇卖', '大唐街道口', '暨南街道白调', '东和乡', '溧浦镇', '牌头镇', '同山镇', '道湖镇',
                     '安华镇', '璜山镇0', '陈宅镇O', '长乐镇', 'N南山风景区']

    accu_ocr = ['漓渚镇⑥', '大禹陵', '河上镇@', '、香炉峰', '店口镇', '鉴湖街道', '楼塔镇@', '森林', '亮国家', ':官乡', '湖', '6307', 'O次坞镇', '坑坞',
                '常绿镇', '桥', '若头岗', '5103', 'O姚江镇一回山下湖镇', '回店街镇', '水', '枫桥镇', '稽东镇', '森林', '国家', '头梅', '赵家镇', '博士越大山',
                '陶朱街道', 'J盏', '诸暨香榧', 'O', '国家森林公园', '铜', '诸暨站', '暨阳街道院东', '五泄风景区', '610街道', '强大诸暨市', '水宁', '骆家尖',
                '省五淮镇', '大唐街道回', '西施故里!', '东和乡', '笔架山', '南山暨南街道(', '包头', '嵊', '驼背岭', '溧浦镇', '羊上尖', '石柱山', '⑥牌头镇', '外鹰炮',
                '同山镇', '东首湖镇', '庆南头', '安', '璜山镇⑥', '陈', '水', '嵊L', '自玉尖', '白马镇', '浦', '镇', '郑家坞镇', '陈宅镇', '炮岗', '西郎',
                '风景', '底尖', '椰坑水库', '东白山', '姑坪', '长乐镇', '水', '回大陈镇', '加巧溪水库', '东方红水库', '苏溪镇', '南山风景区']

    name = openpyxl_excel()  # 正确数据

    pattern_matching(fast_ocr_text, name)
    # print(Search(txt, pat))
