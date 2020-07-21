# -*- coding = utf-8 -*-
# @Time :2020/7/20 4:22 下午
# @Author: XZL
# @File : excel_handle.py
# @Software: PyCharm
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook  # from import 是导入的其中模块、函数、类(所以之后要实例化)


def pandas_excel():
    """
    用pandas操作excel方法
    """
    xls = pd.ExcelFile('../data.xls')
    df = pd.read_excel(xls, 'Sheet1')
    Name = df['NAME'].values
    print(Name)


def openpyxl_excel():
    wb = load_workbook('../data.xlsx')  # 加载工作簿
    # 取得指定sheet表
    work_sheet = wb.get_sheet_by_name('Sheet1')
    name_col = work_sheet['D']
    name = []
    for i in range(1, len(name_col)):
        xl_cell = name_col[i].value
        name.append(xl_cell)
    print(name)
    return name


if __name__ == '__main__':
    openpyxl_excel()
